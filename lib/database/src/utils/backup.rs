use std::{
  path::Path,
  sync::{Arc, atomic},
};

use anyhow::{Context, anyhow};
use async_compression::tokio::write::GzipEncoder;
use chrono::Local;
use futures_util::{
  SinkExt, StreamExt, TryStreamExt, stream::FuturesUnordered,
};
use mungos::mongodb::{
  Database,
  bson::{Document, RawDocumentBuf},
};
use tokio::io::{AsyncWriteExt, BufWriter};
use tokio_util::codec::{FramedWrite, LinesCodec};
use tracing::{error, info, warn};

pub async fn backup(
  db: &Database,
  backups_folder: &Path,
) -> anyhow::Result<()> {
  let collections = db
    .list_collection_names()
    .await
    .context("Failed to list collections on source db")?;

  let now_backups_folder = backups_folder
    .join(Local::now().format("%Y-%m-%d_%H-%M-%S").to_string());

  tokio::fs::create_dir_all(&now_backups_folder)
    .await
    .context("Failed to create backup folder")?;

  info!("Backing up to {now_backups_folder:?}...");

  let has_error = Arc::new(atomic::AtomicBool::new(false));

  let mut handles = collections
    .into_iter()
    .map(|collection| {
      let source = db.collection::<RawDocumentBuf>(&collection);
      let file_path = if collection == "Stats" {
        backups_folder.join("Stats.gz")
      } else {
        now_backups_folder.join(format!("{collection}.gz"))
      };
      let has_error = has_error.clone();
      tokio::spawn(async move {
        let res = async {
          let mut count = 0;
          let _ = tokio::fs::remove_file(&file_path).await;
          let file =
            tokio::fs::File::create(&file_path).await.with_context(
              || format!("Failed to create file at {file_path:?}"),
            )?;
          let mut writer = FramedWrite::new(
            BufWriter::new(GzipEncoder::with_quality(
              file,
              async_compression::Level::Best,
            )),
            LinesCodec::new(),
          );
          let mut cursor = source
            .find(Document::new())
            .await
            .context("Failed to query source collection")?;
          while let Some(doc) = cursor
            .try_next()
            .await
            .context("Failed to get next document")?
          {
            count += 1;
            let str = match serde_json::to_string(&doc)
              .context("Failed to serialize document")
            {
              Ok(str) => str,
              Err(e) => {
                warn!("{e:#}");
                continue;
              }
            };
            if let Err(e) = writer
              .send(str)
              .await
              .context("Failed to write document to file")
            {
              warn!("{e:#}");
            }
          }

          if let Err(e) = <_ as SinkExt<String>>::flush(&mut writer)
            .await
            .context("Failed to flush writer")
          {
            error!("{e:#}");
          };

          if let Err(e) = writer
            .into_inner()
            .shutdown()
            .await
            .context("Failed to shutdown writer compression")
          {
            error!("{e:#}");
          }

          anyhow::Ok(count)
        }
        .await;
        match res {
          Ok(count) => {
            if count > 0 {
              info!("[{collection}]: Backed up {count} items");
            }
          }
          Err(e) => {
            error!("[{collection}]: {e:#}");
            has_error.store(true, atomic::Ordering::Relaxed);
          }
        }
      })
    })
    .collect::<FuturesUnordered<_>>();

  loop {
    match handles.next().await {
      Some(Ok(())) => {}
      Some(Err(e)) => {
        error!("{e:#}");
      }
      None => break,
    }
  }

  if has_error.load(atomic::Ordering::Relaxed) {
    Err(anyhow!("Finished backing up database with errors 🚨"))
  } else {
    info!("Finished backing up database ✅");
    Ok(())
  }
}

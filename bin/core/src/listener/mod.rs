use std::sync::Arc;

use anyhow::anyhow;
use axum::{Router, http::HeaderMap};
use komodo_client::entities::resource::Resource;
use tokio::sync::Mutex;

use crate::{helpers::cache::Cache, resource::KomodoResource};

mod integrations;
mod resources;
mod router;

use integrations::*;

pub fn router() -> Router {
  Router::new()
    .nest("/github", router::router::<github::Github>())
    .nest("/gitlab", router::router::<gitlab::Gitlab>())
}

type ListenerLockCache = Cache<String, Arc<Mutex<()>>>;

/// Implemented for all resources which can recieve webhook.
trait CustomSecret: KomodoResource {
  fn custom_secret(
    resource: &Resource<Self::Config, Self::Info>,
  ) -> &str;
}

/// Implemented on the integration struct, eg [integrations::github::Github]
trait VerifySecret {
  fn verify_secret(
    headers: HeaderMap,
    body: &str,
    custom_secret: &str,
  ) -> anyhow::Result<()>;
}

/// Implemented on the integration struct, eg [integrations::github::Github]
trait ExtractBranch {
  fn extract_branch(body: &str) -> anyhow::Result<String>;
  fn verify_branch(body: &str, expected: &str) -> anyhow::Result<()> {
    let branch = Self::extract_branch(body)?;
    if branch == expected {
      Ok(())
    } else {
      Err(anyhow!("request branch does not match expected"))
    }
  }
}

/// For Procedures and Actions, incoming webhook
/// can be triggered by any branch by using `__ANY__`
/// as the branch in the webhook URL.
const ANY_BRANCH: &str = "__ANY__";

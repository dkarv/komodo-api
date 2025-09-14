use anyhow::Context;
use colored::Colorize;
use komodo_client::{
  api::write::{
    UpdateBuild, UpdateDeployment, UpdateRepo, UpdateResourceSync,
    UpdateServer, UpdateStack,
  },
  entities::{
    build::PartialBuildConfig,
    config::cli::args::update::UpdateResource,
    deployment::PartialDeploymentConfig, repo::PartialRepoConfig,
    server::PartialServerConfig, stack::PartialStackConfig,
    sync::PartialResourceSyncConfig,
  },
};
use serde::{Serialize, de::DeserializeOwned};

pub async fn update<
  T: std::fmt::Debug + Serialize + DeserializeOwned + ResourceUpdate,
>(
  UpdateResource {
    resource,
    update,
    yes,
  }: &UpdateResource,
) -> anyhow::Result<()> {
  println!("\n{}: Update {}\n", "Mode".dimmed(), T::resource_type());
  println!(" - {}: {resource}", "Name".dimmed());

  let config = serde_qs::from_str::<T>(update)
    .context("Failed to deserialize config")?;

  match serde_json::to_string_pretty(&config) {
    Ok(config) => {
      println!(" - {}: {config}", "Update".dimmed());
    }
    Err(_) => {
      println!(" - {}: {config:#?}", "Update".dimmed());
    }
  }

  crate::command::wait_for_enter("update resource", *yes)?;

  config.apply(resource).await
}

pub trait ResourceUpdate {
  fn resource_type() -> &'static str;
  async fn apply(self, resource: &str) -> anyhow::Result<()>;
}

impl ResourceUpdate for PartialBuildConfig {
  fn resource_type() -> &'static str {
    "Build"
  }
  async fn apply(self, resource: &str) -> anyhow::Result<()> {
    let client = crate::command::komodo_client().await?;
    client
      .write(UpdateBuild {
        id: resource.to_string(),
        config: self,
      })
      .await
      .context("Failed to update build config")?;
    Ok(())
  }
}

impl ResourceUpdate for PartialDeploymentConfig {
  fn resource_type() -> &'static str {
    "Deployment"
  }
  async fn apply(self, resource: &str) -> anyhow::Result<()> {
    let client = crate::command::komodo_client().await?;
    client
      .write(UpdateDeployment {
        id: resource.to_string(),
        config: self,
      })
      .await
      .context("Failed to update deployment config")?;
    Ok(())
  }
}

impl ResourceUpdate for PartialRepoConfig {
  fn resource_type() -> &'static str {
    "Repo"
  }
  async fn apply(self, resource: &str) -> anyhow::Result<()> {
    let client = crate::command::komodo_client().await?;
    client
      .write(UpdateRepo {
        id: resource.to_string(),
        config: self,
      })
      .await
      .context("Failed to update repo config")?;
    Ok(())
  }
}

impl ResourceUpdate for PartialServerConfig {
  fn resource_type() -> &'static str {
    "Server"
  }
  async fn apply(self, resource: &str) -> anyhow::Result<()> {
    let client = crate::command::komodo_client().await?;
    client
      .write(UpdateServer {
        id: resource.to_string(),
        config: self,
      })
      .await
      .context("Failed to update server config")?;
    Ok(())
  }
}

impl ResourceUpdate for PartialStackConfig {
  fn resource_type() -> &'static str {
    "Stack"
  }
  async fn apply(self, resource: &str) -> anyhow::Result<()> {
    let client = crate::command::komodo_client().await?;
    client
      .write(UpdateStack {
        id: resource.to_string(),
        config: self,
      })
      .await
      .context("Failed to update stack config")?;
    Ok(())
  }
}

impl ResourceUpdate for PartialResourceSyncConfig {
  fn resource_type() -> &'static str {
    "Sync"
  }
  async fn apply(self, resource: &str) -> anyhow::Result<()> {
    let client = crate::command::komodo_client().await?;
    client
      .write(UpdateResourceSync {
        id: resource.to_string(),
        config: self,
      })
      .await
      .context("Failed to update sync config")?;
    Ok(())
  }
}

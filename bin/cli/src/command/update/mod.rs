use komodo_client::entities::{
  build::PartialBuildConfig,
  config::cli::args::update::UpdateCommand,
  deployment::PartialDeploymentConfig, repo::PartialRepoConfig,
  server::PartialServerConfig, stack::PartialStackConfig,
  sync::PartialResourceSyncConfig,
};

mod resource;
mod user;
mod variable;

pub async fn handle(command: &UpdateCommand) -> anyhow::Result<()> {
  match command {
    UpdateCommand::Build(update) => {
      resource::update::<PartialBuildConfig>(update).await
    }
    UpdateCommand::Deployment(update) => {
      resource::update::<PartialDeploymentConfig>(update).await
    }
    UpdateCommand::Repo(update) => {
      resource::update::<PartialRepoConfig>(update).await
    }
    UpdateCommand::Server(update) => {
      resource::update::<PartialServerConfig>(update).await
    }
    UpdateCommand::Stack(update) => {
      resource::update::<PartialStackConfig>(update).await
    }
    UpdateCommand::Sync(update) => {
      resource::update::<PartialResourceSyncConfig>(update).await
    }
    UpdateCommand::Variable {
      name,
      value,
      secret,
      yes,
    } => variable::update(name, value, *secret, *yes).await,
    UpdateCommand::User { username, command } => {
      user::update(username, command).await
    }
  }
}

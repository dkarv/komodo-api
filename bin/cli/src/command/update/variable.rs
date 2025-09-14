use anyhow::Context;
use colored::Colorize;
use komodo_client::api::{
  read::GetVariable,
  write::{
    CreateVariable, UpdateVariableIsSecret, UpdateVariableValue,
  },
};

pub async fn update(
  name: &str,
  value: &str,
  secret: Option<bool>,
  yes: bool,
) -> anyhow::Result<()> {
  println!("\n{}: Update Variable\n", "Mode".dimmed());
  println!(" - {}:  {name}", "Name".dimmed());
  println!(" - {}: {value}", "Value".dimmed());
  if let Some(secret) = secret {
    println!(" - {}: {secret}", "Is Secret".dimmed());
  }

  crate::command::wait_for_enter("update variable", yes)?;

  let client = crate::command::komodo_client().await?;

  let Ok(existing) = client
    .read(GetVariable {
      name: name.to_string(),
    })
    .await
  else {
    // Create the variable
    client
      .write(CreateVariable {
        name: name.to_string(),
        value: value.to_string(),
        is_secret: secret.unwrap_or_default(),
        description: Default::default(),
      })
      .await
      .context("Failed to create variable")?;
    info!("Variable created ✅");
    return Ok(());
  };

  client
    .write(UpdateVariableValue {
      name: name.to_string(),
      value: value.to_string(),
    })
    .await
    .context("Failed to update variable 'value'")?;
  info!("Variable 'value' updated ✅");

  let Some(secret) = secret else { return Ok(()) };

  if secret != existing.is_secret {
    client
      .write(UpdateVariableIsSecret {
        name: name.to_string(),
        is_secret: secret,
      })
      .await
      .context("Failed to update variable 'is_secret'")?;
    info!("Variable 'is_secret' updated to {secret} ✅");
  }

  Ok(())
}

use std::{path::PathBuf, sync::OnceLock};

use clap::Parser;
use colored::Colorize;
use config::ConfigLoader;
use environment_file::maybe_read_list_from_file;
use komodo_client::entities::{
  config::periphery::{CliArgs, Env, PeripheryConfig},
  logger::{LogConfig, LogLevel},
};

pub fn periphery_config() -> &'static PeripheryConfig {
  static PERIPHERY_CONFIG: OnceLock<PeripheryConfig> =
    OnceLock::new();
  PERIPHERY_CONFIG.get_or_init(|| {
    let env: Env = envy::from_env()
      .expect("failed to parse periphery environment");
    let args = CliArgs::parse();
    let config_paths =
      args.config_path.unwrap_or(env.periphery_config_paths);

    let config = if config_paths.is_empty() {
      println!(
        "{}: No config paths found, using default config",
        "INFO".green(),
      );
      PeripheryConfig::default()
    } else {
      (ConfigLoader {
        paths: &config_paths
          .iter()
          .map(PathBuf::as_path)
          .collect::<Vec<_>>(),
        match_wildcards: &args
          .config_keyword
          .unwrap_or(env.periphery_config_keywords)
          .iter()
          .map(String::as_str)
          .collect::<Vec<_>>(),
        include_file_name: ".peripheryinclude",
        merge_nested: args
          .merge_nested_config
          .unwrap_or(env.periphery_merge_nested_config),
        extend_array: args
          .extend_config_arrays
          .unwrap_or(env.periphery_extend_config_arrays),
        debug_print: args
          .log_level
          .map(|level| {
            level == tracing::Level::DEBUG
              || level == tracing::Level::TRACE
          })
          .unwrap_or_default(),
      })
      .load()
      .expect("failed at parsing config from paths")
    };

    PeripheryConfig {
      port: env.periphery_port.unwrap_or(config.port),
      bind_ip: env.periphery_bind_ip.unwrap_or(config.bind_ip),
      root_directory: env
        .periphery_root_directory
        .unwrap_or(config.root_directory),
      repo_dir: env.periphery_repo_dir.or(config.repo_dir),
      stack_dir: env.periphery_stack_dir.or(config.stack_dir),
      build_dir: env.periphery_build_dir.or(config.build_dir),
      disable_terminals: env
        .periphery_disable_terminals
        .unwrap_or(config.disable_terminals),
      disable_container_exec: env
        .periphery_disable_container_exec
        .unwrap_or(config.disable_container_exec),
      stats_polling_rate: env
        .periphery_stats_polling_rate
        .unwrap_or(config.stats_polling_rate),
      container_stats_polling_rate: env
        .periphery_container_stats_polling_rate
        .unwrap_or(config.container_stats_polling_rate),
      legacy_compose_cli: env
        .periphery_legacy_compose_cli
        .unwrap_or(config.legacy_compose_cli),
      logging: LogConfig {
        level: args
          .log_level
          .map(LogLevel::from)
          .or(env.periphery_logging_level)
          .unwrap_or(config.logging.level),
        stdio: env
          .periphery_logging_stdio
          .unwrap_or(config.logging.stdio),
        pretty: env
          .periphery_logging_pretty
          .unwrap_or(config.logging.pretty),
        location: env
          .periphery_logging_location
          .unwrap_or(config.logging.location),
        otlp_endpoint: env
          .periphery_logging_otlp_endpoint
          .unwrap_or(config.logging.otlp_endpoint),
        opentelemetry_service_name: env
          .periphery_logging_opentelemetry_service_name
          .unwrap_or(config.logging.opentelemetry_service_name),
      },
      pretty_startup_config: env
        .periphery_pretty_startup_config
        .unwrap_or(config.pretty_startup_config),
      allowed_ips: env
        .periphery_allowed_ips
        .unwrap_or(config.allowed_ips),
      passkeys: maybe_read_list_from_file(
        env.periphery_passkeys_file,
        env.periphery_passkeys,
      )
      .unwrap_or(config.passkeys),
      include_disk_mounts: env
        .periphery_include_disk_mounts
        .unwrap_or(config.include_disk_mounts),
      exclude_disk_mounts: env
        .periphery_exclude_disk_mounts
        .unwrap_or(config.exclude_disk_mounts),
      ssl_enabled: env
        .periphery_ssl_enabled
        .unwrap_or(config.ssl_enabled),
      ssl_key_file: env
        .periphery_ssl_key_file
        .or(config.ssl_key_file),
      ssl_cert_file: env
        .periphery_ssl_cert_file
        .or(config.ssl_cert_file),
      secrets: config.secrets,
      git_providers: config.git_providers,
      docker_registries: config.docker_registries,
    }
  })
}

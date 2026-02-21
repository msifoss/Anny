import logging
import os
from pathlib import Path
from typing import Any

import yaml
from pydantic_settings import BaseSettings

logger = logging.getLogger("anny")


def _flatten_yaml(data: dict, parent_key: str = "", sep: str = "_") -> dict[str, Any]:
    """Flatten nested YAML dict: {'app': {'version': '0.8.0'}} -> {'app_version': '0.8.0'}."""
    items: list[tuple[str, Any]] = []
    for key, value in data.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(_flatten_yaml(value, new_key, sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def _load_yaml_config() -> dict[str, Any]:
    """Load config.yaml from project root (or Docker /app/), return flattened dict."""
    candidates = [
        Path(__file__).resolve().parents[3] / "config.yaml",  # src/anny/core -> project root
        Path.cwd() / "config.yaml",
        Path("/app/config.yaml"),  # Docker
    ]

    for path in candidates:
        if path.is_file():
            with open(path, encoding="utf-8") as f:
                raw = yaml.safe_load(f)
            if raw and isinstance(raw, dict):
                return _flatten_yaml(raw)
            return {}

    return {}


class Settings(BaseSettings):
    """Application settings.

    Precedence: env var > .env > config.yaml > code default
    """

    # App
    app_version: str = "0.8.0"
    app_port: int = 8000
    rate_limit_requests: int = 60
    rate_limit_window: int = 60
    cache_ttl: int = 3600
    cache_max_entries: int = 500
    memory_store_path: str = "~/.anny/memory.json"

    # Google
    ga4_property_id: str = ""
    search_console_site_url: str = ""

    # Secrets (only from .env / env vars)
    google_service_account_key_path: str = ""
    anny_api_key: str = ""
    sentry_dsn: str = ""

    # Deploy
    deploy_domain: str = "anny.membies.com"
    deploy_remote_dir: str = "/opt/anny"
    deploy_ssh_key: str = "~/.ssh/webengine_deploy"
    deploy_health_check_timeout: int = 60

    # Infra
    infra_vultr_plan: str = "vc2-1c-1gb"
    infra_vultr_region: str = "ewr"
    infra_vultr_os_id: str = "2284"
    infra_vultr_label: str = "anny"
    infra_parent_domain: str = "membies.com"
    infra_subdomain: str = "anny"
    infra_ssh_key_name: str = "webengine-deploy"

    # Backup
    backup_dir: str = "/opt/anny/backups"
    backup_container_name: str = "anny-anny-1"
    backup_memory_path: str = "/home/anny/.anny/memory.json"
    backup_retention_days: int = 7

    # Monitoring
    monitoring_health_url: str = "https://anny.membies.com/health"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    def __init__(self, **kwargs):
        # Inject YAML values as defaults below env/.env but above code defaults
        yaml_values = _load_yaml_config()
        # Only use YAML values for fields not already provided via kwargs or env
        for key, value in yaml_values.items():
            if key not in kwargs and key.upper() not in os.environ:
                kwargs.setdefault(key, value)
        super().__init__(**kwargs)


def validate_config(s: Settings) -> list[str]:
    """Check required settings and return a list of warning messages."""
    warnings = []
    if not s.google_service_account_key_path:
        warnings.append("GOOGLE_SERVICE_ACCOUNT_KEY_PATH is not set")
    elif not os.path.isfile(s.google_service_account_key_path):
        warnings.append(
            f"GOOGLE_SERVICE_ACCOUNT_KEY_PATH file not found: {s.google_service_account_key_path}"
        )
    if not s.ga4_property_id:
        warnings.append("GA4_PROPERTY_ID is not set")
    if not s.search_console_site_url:
        warnings.append("SEARCH_CONSOLE_SITE_URL is not set")
    if not s.anny_api_key:
        warnings.append("ANNY_API_KEY is not set — REST API and MCP HTTP auth disabled")
    return warnings


settings = Settings()

for _warning in validate_config(settings):
    logger.warning(_warning)

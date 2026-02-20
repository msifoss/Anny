import logging
import os

from pydantic_settings import BaseSettings

logger = logging.getLogger("anny")


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    google_service_account_key_path: str = ""
    ga4_property_id: str = ""
    search_console_site_url: str = ""
    memory_store_path: str = "~/.anny/memory.json"
    anny_api_key: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


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

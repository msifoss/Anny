from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    google_service_account_key_path: str = ""
    ga4_property_id: str = ""
    search_console_site_url: str = ""
    memory_store_path: str = "~/.anny/memory.json"
    anny_api_key: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

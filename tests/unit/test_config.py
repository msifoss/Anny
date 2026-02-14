import os
from unittest.mock import patch

from anny.core.config import Settings


def test_default_settings():
    with patch.dict(os.environ, {}, clear=True):
        s = Settings(_env_file=None)
    assert s.google_service_account_key_path == ""
    assert s.ga4_property_id == ""
    assert s.search_console_site_url == ""


def test_settings_from_env():
    env = {
        "GOOGLE_SERVICE_ACCOUNT_KEY_PATH": "/tmp/key.json",
        "GA4_PROPERTY_ID": "properties/999",
        "SEARCH_CONSOLE_SITE_URL": "https://example.com",
    }
    with patch.dict(os.environ, env, clear=True):
        s = Settings(_env_file=None)
    assert s.google_service_account_key_path == "/tmp/key.json"
    assert s.ga4_property_id == "properties/999"
    assert s.search_console_site_url == "https://example.com"

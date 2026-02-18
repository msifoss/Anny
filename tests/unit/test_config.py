import os
from unittest.mock import patch

from anny.core.config import Settings, validate_config


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


def test_validate_config_warns_on_missing_settings():
    with patch.dict(os.environ, {}, clear=True):
        s = Settings(_env_file=None)
    warnings = validate_config(s)
    assert any("GOOGLE_SERVICE_ACCOUNT_KEY_PATH" in w for w in warnings)
    assert any("GA4_PROPERTY_ID" in w for w in warnings)
    assert any("SEARCH_CONSOLE_SITE_URL" in w for w in warnings)
    assert any("ANNY_API_KEY" in w for w in warnings)


def test_validate_config_warns_on_missing_key_file():
    env = {
        "GOOGLE_SERVICE_ACCOUNT_KEY_PATH": "/nonexistent/key.json",
        "GA4_PROPERTY_ID": "properties/999",
        "SEARCH_CONSOLE_SITE_URL": "https://example.com",
        "ANNY_API_KEY": "some-key",
    }
    with patch.dict(os.environ, env, clear=True):
        s = Settings(_env_file=None)
    warnings = validate_config(s)
    assert any("file not found" in w for w in warnings)


def test_validate_config_no_warnings_when_complete(tmp_path):
    key_file = tmp_path / "key.json"
    key_file.write_text("{}")
    env = {
        "GOOGLE_SERVICE_ACCOUNT_KEY_PATH": str(key_file),
        "GA4_PROPERTY_ID": "properties/999",
        "SEARCH_CONSOLE_SITE_URL": "https://example.com",
        "ANNY_API_KEY": "some-key",
    }
    with patch.dict(os.environ, env, clear=True):
        s = Settings(_env_file=None)
    warnings = validate_config(s)
    assert not warnings

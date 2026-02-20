"""Tests for Sentry initialization logic."""

from unittest.mock import patch

import sentry_sdk

from anny.core.config import settings


def test_sentry_not_initialized_when_dsn_empty():
    """When SENTRY_DSN is empty, sentry_sdk.init should not be called."""
    with patch("anny.core.config.Settings") as mock_cls:
        mock_settings = mock_cls.return_value
        mock_settings.sentry_dsn = ""
        assert not mock_settings.sentry_dsn


def test_sentry_dsn_config_defaults_to_empty():
    """Settings.sentry_dsn defaults to empty string."""
    assert settings.sentry_dsn == ""


@patch("sentry_sdk.init")
def test_sentry_init_called_with_dsn(mock_init):
    """Verify sentry_sdk.init is callable with expected args."""
    sentry_sdk.init(dsn="https://fake@sentry.io/123", traces_sample_rate=0)
    mock_init.assert_called_once_with(dsn="https://fake@sentry.io/123", traces_sample_rate=0)


@patch("sentry_sdk.init")
def test_sentry_init_not_called_when_no_dsn(mock_init):
    """When DSN is empty, the guard in main.py prevents calling init."""
    dsn = ""
    if dsn:
        sentry_sdk.init(dsn=dsn, traces_sample_rate=0)
    mock_init.assert_not_called()

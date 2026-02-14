from unittest.mock import MagicMock, patch

import pytest

from anny.core.auth import SCOPES, get_google_credentials
from anny.core.exceptions import AuthError


def test_empty_key_path_raises_auth_error():
    with pytest.raises(AuthError, match="not set"):
        get_google_credentials("")


def test_missing_file_raises_auth_error():
    with pytest.raises(AuthError, match="not found"):
        get_google_credentials("/nonexistent/path/key.json")


@patch("anny.core.auth.service_account.Credentials.from_service_account_file")
def test_valid_key_returns_credentials(mock_from_file):
    mock_creds = MagicMock()
    mock_from_file.return_value = mock_creds

    result = get_google_credentials("/tmp/key.json")

    assert result is mock_creds
    mock_from_file.assert_called_once_with("/tmp/key.json", scopes=SCOPES)


@patch("anny.core.auth.service_account.Credentials.from_service_account_file")
def test_invalid_key_raises_auth_error(mock_from_file):
    mock_from_file.side_effect = ValueError("bad key")

    with pytest.raises(AuthError, match="Failed to load credentials"):
        get_google_credentials("/tmp/bad_key.json")

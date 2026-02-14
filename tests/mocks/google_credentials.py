from unittest.mock import MagicMock


def mock_credentials():
    """Create a mock Google service account Credentials object."""
    creds = MagicMock()
    creds.token = "fake-token"
    creds.valid = True
    creds.expired = False
    return creds

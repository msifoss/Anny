from google.oauth2 import service_account

from anny.core.exceptions import AuthError

SCOPES = [
    "https://www.googleapis.com/auth/analytics.readonly",
    "https://www.googleapis.com/auth/webmasters.readonly",
    "https://www.googleapis.com/auth/tagmanager.readonly",
]


def get_google_credentials(key_path: str) -> service_account.Credentials:
    """Load Google service account credentials from a JSON key file."""
    if not key_path:
        raise AuthError("GOOGLE_SERVICE_ACCOUNT_KEY_PATH is not set")
    try:
        return service_account.Credentials.from_service_account_file(key_path, scopes=SCOPES)
    except FileNotFoundError as exc:
        raise AuthError(f"Service account key file not found: {key_path}") from exc
    except Exception as exc:
        raise AuthError(f"Failed to load credentials: {exc}") from exc

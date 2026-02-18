import logging

from google.oauth2 import service_account

from anny.core.exceptions import AuthError

logger = logging.getLogger("anny")

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
        creds = service_account.Credentials.from_service_account_file(key_path, scopes=SCOPES)
        logger.info("Loaded service account credentials from %s", key_path)
        return creds
    except FileNotFoundError as exc:
        raise AuthError(f"Service account key file not found: {key_path}") from exc
    except (ValueError, KeyError) as exc:
        logger.error("Invalid service account key file: %s", exc)
        raise AuthError("Failed to load credentials: invalid key file format") from exc

import functools

from fastapi import Security
from fastapi.security import APIKeyHeader
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from googleapiclient.discovery import build

from anny.clients.ga4 import GA4Client
from anny.clients.memory import MemoryStore
from anny.clients.search_console import SearchConsoleClient
from anny.clients.tag_manager import TagManagerClient
from anny.core.auth import get_google_credentials
from anny.core.config import settings
from anny.core.exceptions import AuthError

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)):
    """Validate X-API-Key header. Auth is disabled when ANNY_API_KEY is empty."""
    if not settings.anny_api_key:
        return api_key
    if not api_key or api_key != settings.anny_api_key:
        raise AuthError("Invalid or missing API key")
    return api_key


@functools.lru_cache
def get_credentials():
    return get_google_credentials(settings.google_service_account_key_path)


@functools.lru_cache
def get_ga4_client() -> GA4Client:
    creds = get_credentials()
    client = BetaAnalyticsDataClient(credentials=creds)
    return GA4Client(client, settings.ga4_property_id)


@functools.lru_cache
def get_search_console_client() -> SearchConsoleClient:
    creds = get_credentials()
    service = build("searchconsole", "v1", credentials=creds)
    return SearchConsoleClient(service, settings.search_console_site_url)


@functools.lru_cache
def get_tag_manager_client() -> TagManagerClient:
    creds = get_credentials()
    service = build("tagmanager", "v2", credentials=creds)
    return TagManagerClient(service)


@functools.lru_cache
def get_memory_store() -> MemoryStore:
    return MemoryStore(settings.memory_store_path)

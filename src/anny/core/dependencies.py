import functools

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from googleapiclient.discovery import build

from anny.clients.ga4 import GA4Client
from anny.clients.search_console import SearchConsoleClient
from anny.clients.tag_manager import TagManagerClient
from anny.core.auth import get_google_credentials
from anny.core.config import settings


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

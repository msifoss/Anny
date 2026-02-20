import logging

from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError

from anny.core.exceptions import APIError

logger = logging.getLogger("anny")


class SearchConsoleClient:
    """Wraps the Google Search Console API."""

    def __init__(self, service: Resource, site_url: str):
        self._service = service
        self._site_url = site_url

    @property
    def site_url(self) -> str:
        return self._site_url

    def query(
        self,
        start_date: str,
        end_date: str,
        dimensions: list[str] | None = None,
        row_limit: int = 10,
    ) -> list[dict]:
        """Run a Search Console search analytics query."""
        body = {
            "startDate": start_date,
            "endDate": end_date,
            "rowLimit": row_limit,
        }
        if dimensions:
            body["dimensions"] = dimensions

        try:
            response = (
                self._service.searchanalytics().query(siteUrl=self._site_url, body=body).execute()
            )
        except HttpError as exc:
            logger.warning("Search Console query failed: %s %s", exc.status_code, exc.reason)
            raise APIError(
                "Search Console query failed",
                service="search_console",
            ) from exc

        logger.info("Search Console query returned %d rows", len(response.get("rows", [])))
        return self._flatten_response(response, dimensions or [])

    @staticmethod
    def _flatten_response(response: dict, dimensions: list[str]) -> list[dict]:
        """Convert Search Console API response to flat dicts."""
        rows = []
        for row in response.get("rows", []):
            flat = {}
            keys = row.get("keys", [])
            for i, dim in enumerate(dimensions):
                flat[dim] = keys[i] if i < len(keys) else ""
            flat["clicks"] = row.get("clicks", 0)
            flat["impressions"] = row.get("impressions", 0)
            flat["ctr"] = round(row.get("ctr", 0) * 100, 2)
            flat["position"] = round(row.get("position", 0), 1)
            rows.append(flat)
        return rows

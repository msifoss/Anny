import logging

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    RunReportResponse,
)
from google.api_core.exceptions import GoogleAPICallError

from anny.core.exceptions import APIError

logger = logging.getLogger("anny")


class GA4Client:
    """Wraps the Google Analytics Data API v1beta."""

    def __init__(self, client: BetaAnalyticsDataClient, property_id: str):
        self._client = client
        self._property_id = property_id

    @property
    def property_id(self) -> str:
        return self._property_id

    def run_report(
        self,
        metrics: list[str],
        dimensions: list[str],
        start_date: str,
        end_date: str,
        limit: int = 10,
    ) -> list[dict]:
        """Run a GA4 report and return rows as flat dicts."""
        request = RunReportRequest(
            property=f"properties/{self._property_id.removeprefix('properties/')}",
            metrics=[Metric(name=m) for m in metrics],
            dimensions=[Dimension(name=d) for d in dimensions],
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            limit=limit,
        )

        try:
            response: RunReportResponse = self._client.run_report(request)
        except GoogleAPICallError as exc:
            logger.error("GA4 report failed: %s", exc.message)
            raise APIError(f"GA4 report failed: {exc.message}", service="ga4") from exc

        logger.info("GA4 report returned %d rows", len(response.rows))
        return self._flatten_response(response, metrics, dimensions)

    @staticmethod
    def _flatten_response(
        response: RunReportResponse, metrics: list[str], dimensions: list[str]
    ) -> list[dict]:
        """Convert protobuf RunReportResponse to a list of flat dicts."""
        rows = []
        for row in response.rows:
            flat = {}
            for i, dim in enumerate(dimensions):
                flat[dim] = row.dimension_values[i].value
            for i, met in enumerate(metrics):
                flat[met] = row.metric_values[i].value
            rows.append(flat)
        return rows

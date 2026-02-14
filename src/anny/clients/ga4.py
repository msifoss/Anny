from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    RunReportResponse,
)

from anny.core.exceptions import APIError


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
        except Exception as exc:
            raise APIError(f"GA4 report failed: {exc}", service="ga4") from exc

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

from pydantic import BaseModel, Field


class GA4ReportRequest(BaseModel):
    metrics: str = Field(default="sessions,totalUsers", description="Comma-separated GA4 metrics")
    dimensions: str = Field(default="date", description="Comma-separated GA4 dimensions")
    date_range: str = Field(
        default="last_28_days", description="Named range or YYYY-MM-DD,YYYY-MM-DD"
    )
    limit: int = Field(default=10, ge=1, le=100, description="Max rows to return")


class GA4ReportResponse(BaseModel):
    rows: list[dict]
    row_count: int


class SCQueryRequest(BaseModel):
    dimensions: str = Field(
        default="query",
        description="Comma-separated dimensions (query, page, date, country, device)",
    )
    date_range: str = Field(
        default="last_28_days", description="Named range or YYYY-MM-DD,YYYY-MM-DD"
    )
    row_limit: int = Field(default=10, ge=1, le=1000, description="Max rows to return")


class SCQueryResponse(BaseModel):
    rows: list[dict]
    row_count: int


class GTMListResponse(BaseModel):
    items: list[dict]
    count: int


class GTMContainerSetupResponse(BaseModel):
    tags: list[dict]
    tag_count: int
    triggers: list[dict]
    trigger_count: int
    variables: list[dict]
    variable_count: int


class SitemapListResponse(BaseModel):
    sitemaps: list[dict]
    count: int


class SitemapDetailResponse(BaseModel):
    path: str
    type: str
    lastSubmitted: str = ""
    isPending: bool = False
    isSitemapsIndex: bool = False
    warnings: int = 0
    errors: int = 0
    contents: list[dict] = []

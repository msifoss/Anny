from fastapi import APIRouter, Query, Security

from anny.core.dependencies import verify_api_key
from anny.core.logging import get_recent_logs

router = APIRouter(prefix="/api", tags=["Logs"])


@router.get("/logs")
async def logs(
    limit: int = Query(default=100, ge=1, le=500),
    level: str = Query(default="DEBUG", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"),
    _: str = Security(verify_api_key),
):
    """Return recent log entries from the in-memory ring buffer."""
    return get_recent_logs(limit=limit, level=level)

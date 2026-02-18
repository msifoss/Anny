import logging
import os

from fastapi import FastAPI

from anny.api.error_handlers import anny_error_handler
from anny.api.ga4_routes import router as ga4_router
from anny.api.search_console_routes import router as sc_router
from anny.api.tag_manager_routes import router as gtm_router
from anny.core.config import settings
from anny.core.exceptions import AnnyError
from anny.mcp_server import mcp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("anny")

mcp_app = mcp.http_app(path="/mcp")
app = FastAPI(title="Anny", version="0.3.0", lifespan=mcp_app.lifespan)
logger.info("Anny v0.3.0 starting")

app.add_exception_handler(AnnyError, anny_error_handler)

app.include_router(ga4_router)
app.include_router(sc_router)
app.include_router(gtm_router)

app.mount("/mcp", mcp_app)


@app.get("/health")
async def health():
    checks = {}

    # Config: are required settings present?
    checks["config"] = bool(
        settings.google_service_account_key_path
        and settings.ga4_property_id
        and settings.search_console_site_url
    )

    # Credentials: does the key file exist?
    checks["credentials"] = bool(
        settings.google_service_account_key_path
        and os.path.isfile(settings.google_service_account_key_path)
    )

    # Memory: is the store path's parent directory writable?
    memory_dir = os.path.dirname(os.path.expanduser(settings.memory_store_path))
    checks["memory"] = os.path.isdir(memory_dir) and os.access(memory_dir, os.W_OK)

    all_healthy = all(checks.values())
    return {"status": "healthy" if all_healthy else "degraded", "checks": checks}

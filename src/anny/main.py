from fastapi import FastAPI

from anny.api.error_handlers import anny_error_handler
from anny.api.ga4_routes import router as ga4_router
from anny.api.search_console_routes import router as sc_router
from anny.api.tag_manager_routes import router as gtm_router
from anny.core.exceptions import AnnyError
from anny.mcp_server import mcp

app = FastAPI(title="Anny", version="0.1.0")

app.add_exception_handler(AnnyError, anny_error_handler)

app.include_router(ga4_router)
app.include_router(sc_router)
app.include_router(gtm_router)

mcp_app = mcp.http_app(path="/mcp")
app.mount("/mcp", mcp_app)


@app.get("/health")
async def health():
    return {"status": "healthy"}

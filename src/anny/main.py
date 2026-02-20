import logging
import os
import time
from collections import defaultdict

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from anny.api.error_handlers import anny_error_handler
from anny.api.ga4_routes import router as ga4_router
from anny.api.logs_routes import router as logs_router
from anny.api.search_console_routes import router as sc_router
from anny.api.tag_manager_routes import router as gtm_router
from anny.core.config import settings
from anny.core.dependencies import verify_mcp_bearer_token
from anny.core.exceptions import AnnyError
from anny.core.logging import new_request_id, set_request_id, setup_logging
from anny.mcp_server import mcp

setup_logging()
logger = logging.getLogger("anny")

# --- Sentry (only when DSN is configured) ---
if settings.sentry_dsn:
    sentry_sdk.init(dsn=settings.sentry_dsn, traces_sample_rate=0)
    logger.info("Sentry error tracking enabled")

if settings.anny_api_key:
    from fastmcp.server.auth.providers.debug import DebugTokenVerifier

    mcp.auth = DebugTokenVerifier(validate=verify_mcp_bearer_token)
    logger.info("MCP HTTP auth enabled (Bearer token)")

mcp_app = mcp.http_app(path="/")
app = FastAPI(title="Anny", version="0.6.0", lifespan=mcp_app.lifespan)
logger.info("Anny v0.6.0 starting")

# --- CORS middleware (restrictive defaults) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_methods=["GET", "POST"],
    allow_headers=["X-API-Key", "Authorization"],
    allow_credentials=False,
)

app.add_exception_handler(AnnyError, anny_error_handler)

app.include_router(ga4_router)
app.include_router(sc_router)
app.include_router(gtm_router)
app.include_router(logs_router)

app.mount("/mcp", mcp_app)


# --- Request-ID middleware ---
@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    rid = new_request_id()
    set_request_id(rid)
    try:
        response = await call_next(request)
        response.headers["X-Request-ID"] = rid
        return response
    finally:
        set_request_id("")


# --- Request logging middleware ---
@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    # Skip /health to reduce noise
    if request.url.path == "/health":
        return await call_next(request)

    start = time.monotonic()
    response = await call_next(request)
    duration_ms = round((time.monotonic() - start) * 1000, 1)
    client_ip = request.client.host if request.client else "unknown"

    log_data = {
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "duration_ms": duration_ms,
        "client_ip": client_ip,
    }

    if response.status_code >= 500:
        logger.error("HTTP request", extra=log_data)
    elif response.status_code >= 400:
        logger.warning("HTTP request", extra=log_data)
    else:
        logger.info("HTTP request", extra=log_data)

    return response


# --- Rate limiting for /api/* endpoints ---
RATE_LIMIT_REQUESTS = 60
RATE_LIMIT_WINDOW = 60  # seconds
_rate_limit_store: dict[str, list[float]] = defaultdict(list)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if not (request.url.path.startswith("/api/") or request.url.path.startswith("/mcp")):
        return await call_next(request)

    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW

    # Prune expired entries and add current request
    timestamps = _rate_limit_store[client_ip]
    _rate_limit_store[client_ip] = [t for t in timestamps if t > window_start]
    _rate_limit_store[client_ip].append(now)

    if len(_rate_limit_store[client_ip]) > RATE_LIMIT_REQUESTS:
        logger.warning("Rate limit exceeded for %s", client_ip)
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded. Try again later."},
        )

    return await call_next(request)


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

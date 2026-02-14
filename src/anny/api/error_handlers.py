from fastapi import Request
from fastapi.responses import JSONResponse

from anny.core.exceptions import AnnyError, APIError, AuthError


async def anny_error_handler(request: Request, exc: AnnyError):  # pylint: disable=unused-argument
    """Map AnnyError subtypes to appropriate HTTP status codes."""
    if isinstance(exc, AuthError):
        status_code = 401
    elif isinstance(exc, APIError):
        status_code = 502
    else:
        status_code = 500

    return JSONResponse(
        status_code=status_code,
        content={"error": exc.message},
    )

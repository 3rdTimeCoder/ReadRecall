from fastapi import Request
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from lib.responses.standard import StandardResponse


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handles HTTPException and returns a standardized JSON error response.

    Args:
        request: The incoming FastAPI request.
        exc: The HTTPException that was raised.

    Returns:
        A JSONResponse with the error details wrapped in a StandardResponse.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=StandardResponse(
            success=False,
            error={
                "code": "HTTP_ERROR",
                "message": exc.detail,
            }
        ).model_dump()
    )
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from lib.responses.standard import StandardResponse


async def validation_exception_error(
    request: Request,
    exc: RequestValidationError
):
    """Handles RequestValidationError and returns a standardized JSON error response.

    Args:
        request: The incoming FastAPI request.
        exc: The RequestValidationError that was raised.

    Returns:
        A JSONResponse with the validation error details wrapped in a StandardResponse.
    """
    return JSONResponse(
        status_code=400,
        content=StandardResponse(
            success=False,
            error={
                "code": "VALIDATION_ERROR",
                "message": exc.errors()[0]
            }
        ).model_dump()
    )
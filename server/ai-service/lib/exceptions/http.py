from fastapi import Request
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from lib.responses.standard import StandardResponse


async def http_exception_handler(request: Request, exc: HTTPException):
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

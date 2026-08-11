from fastapi.responses import JSONResponse
from typing import Any, Optional
from pydantic import BaseModel

class StandardResponse(BaseModel):
    """Standardized API response model.

    All API endpoints return responses in this format to ensure consistency.

    Attributes:
        success: Whether the request was successful.
        data: The response payload for successful requests.
        error: Error details for failed requests, containing 'code' and 'message'.
    """
    success: bool
    data: Optional[Any] = None
    error: Optional[Any] = None

    
def to_json(resp: StandardResponse, status_code=200):
    """Converts a StandardResponse to a FastAPI JSONResponse.

    Args:
        resp: The StandardResponse instance to serialize.
        status_code: The HTTP status code for the response. Defaults to 200.

    Returns:
        A JSONResponse with the serialized StandardResponse content.
    """
    return JSONResponse(
        status_code=status_code,
        content=resp.model_dump()
    )
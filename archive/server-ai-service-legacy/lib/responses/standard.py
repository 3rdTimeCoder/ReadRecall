from fastapi.responses import JSONResponse
from typing import Any, Optional
from pydantic import BaseModel

class StandardResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[Any] = None

    
def to_json(resp: StandardResponse, status_code=200):
    return JSONResponse(
        status_code=status_code,
        content=resp.model_dump()
    )
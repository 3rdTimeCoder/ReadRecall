from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Annotated
from ingestion.ingestion_pipeline import ingest_books
from retrieval.retrieval_pipeline import get_top_matching_chunks, get_book_suggestions
from lib.middleware.process_time import add_process_time_header
from lib.exceptions.http import http_exception_handler
from lib.exceptions.validation import validation_exception_error
from lib.IngestionType import IngestionType
from lib.responses.standard import StandardResponse, to_json
from tempfile import TemporaryDirectory
from pydantic import BaseModel
from pathlib import Path
import shutil


app = FastAPI()


# CORS configuration
origins = [
    "http://localhost:5713",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["*"] to allow all (not recommended for prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register Middlewares
app.middleware("http")(add_process_time_header)


# Register Exception Handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_error)


# Register Routes
@app.get("/")
async def root():
    return {"message": "Welcome to ReadRecall!"}



@app.post("/ingest")
async def ingest(
    files: List[UploadFile] = File(...),
    type: IngestionType = Form(...),
):
    """TODO: docstring"""

    success = False

    with TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        for file in files:
            file_path = f"{tmp_dir}/{file.filename}"
            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            success = ingest_books(dir_path=tmp_path, type=type)

    if success:
        res = StandardResponse(
            success=True,
            data={ "message": "File ingestion successful." }
        )
        return to_json(res)
    else:
        res = StandardResponse(
            success=False,
            error={ 
                "code": "PROCESSING_ERROR",
                "message": "File ingestion unsuccessful." 
            }
        )
        return to_json(res, status_code=422)


class RecallRequest(BaseModel):
    query: str


@app.post("/recall")
async def recall(
    req: RecallRequest
):
    """TODO: write docstring"""

    chunks = get_top_matching_chunks(query=req.query)
    suggestions = get_book_suggestions(chunks=chunks)

    res = StandardResponse(
        success=True,
        data={ 
            "message": "Recall completed successful",
            "results": suggestions
        }
    )

    return to_json(res)
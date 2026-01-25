from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.exceptions import RequestValidationError
from typing import List
from ingestion.ingestion_pipeline import ingest_books
from tempfile import TemporaryDirectory
from pathlib import Path
import shutil
from lib.middleware.process_time import add_process_time_header
from lib.exceptions.http import http_exception_handler
from lib.exceptions.validation import validation_exception_error
from lib.IngestionType import IngestionType


app = FastAPI()


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
        return { 
            "status": "success",
            "message": "File ingestion successful." 
        }
    else:
        return { 
            "code": 400,
            "status": "error",
            "message": "File ingestion unsuccessful." 
        }
    


@app.post("/recall")
async def recall():
    pass
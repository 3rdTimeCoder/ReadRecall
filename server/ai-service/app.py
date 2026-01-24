from fastapi import FastAPI, File, UploadFile, Form
from typing import List
from ingestion.ingestion_pipeline import ingest_books
from tempfile import TemporaryDirectory
from pathlib import Path
import shutil


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to ReadRecall!"}


@app.post("/ingest")
async def ingest(
        files: List[UploadFile] = File(...),
        type: str = Form(...),
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
        return { "message": "File ingestion successful." }
    else:
        return { "message": "File ingestion unsuccessful." }
    


@app.post("/recall")
async def recall():
    pass
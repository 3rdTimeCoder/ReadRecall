from typing import Union
from pathlib import Path
from ingestion.loaders import load_docs
from ingestion.chunking import chunk_docs
from ingestion.embedding import create_vector_store, persist_chunks


def ingest_books(
        dir_path: Union[str, Path], 
        type="epub", 
        persist_dir="db/chroma_db",
        collection="readrecall-book-chunks",
        is_initial_ingest=True
    ) -> bool:
    """TODO: write docstring"""
    print("initiating book ingestion...")

    try:
        #1. Load files
        files = load_docs(dir=dir_path, type=type, debug_mode=False)

        #2. Chunk files
        chunks = chunk_docs(files, debug_mode=True)

        #3. Embed and Store files in vector DB
        if is_initial_ingest: 
            _ = create_vector_store(
                chunks=chunks,
                persist_dir=persist_dir,
                collection=collection
            )
        else:
            _ = persist_chunks(
                chunks=chunks,
                persist_dir=persist_dir,
                collection=collection
            )
    except Exception as e:
        print(f"Error occurred while ingesting books: {e}")
        return False
    
    return True


if __name__ == "__main__":
    completed = ingest_books("./test-docs")
    if completed: print("Book ingestion completed successfully!")
    else: print("Oops! Something went wrong broke in the pipeline. Book ingestion unsuccessful.")
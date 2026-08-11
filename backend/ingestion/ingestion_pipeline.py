from typing import Union
from pathlib import Path
from ingestion.loaders import load_docs_from_dir
from ingestion.chunking import chunk_docs
from ingestion.embedding import create_vector_store, persist_chunks


def _dedupe_docs_by_book_id(docs: list):
    """Removes duplicate documents based on metadata book_id.

    If book_id is missing, the document is retained.
    """
    seen_book_ids = set()
    unique_docs = []

    for doc in docs:
        metadata = doc.get_metadata() if hasattr(doc, "get_metadata") else {}
        book_id = metadata.get("book_id") if isinstance(metadata, dict) else None

        if not book_id:
            unique_docs.append(doc)
            continue

        if book_id in seen_book_ids:
            continue

        seen_book_ids.add(book_id)
        unique_docs.append(doc)

    return unique_docs


def ingest_books(
        dir_path: Union[str, Path], 
        type="epub", 
        persist_dir="db/chroma_db",
        collection="readrecall-book-chunks",
        is_initial_ingest=True,
    ) -> bool:
    """Orchestrates the full ingestion pipeline: load, chunk, embed, and store.

    Loads all documents of the given type from the specified directory,
    splits them into semantic chunks, embeds the chunks using OpenAI's
    text-embedding-3-small model, and persists them to a ChromaDB vector store.

    Args:
        dir_path: Directory containing the book files to ingest.
        type: File type of the books ('epub' or 'pdf'). Defaults to 'epub'.
        persist_dir: Directory path for the ChromaDB persistent storage.
            Defaults to 'db/chroma_db'.
        collection: Name of the ChromaDB collection. Defaults to
            'readrecall-book-chunks'.
        is_initial_ingest: If True, creates a new vector store. If False,
            loads the existing store and appends chunks. Defaults to True.

    Returns:
        True if ingestion completed successfully, False otherwise.
    """
    print("initiating book ingestion...")

    try:
        #1. Load files
        files = load_docs_from_dir(dir=dir_path, type=type)

        #1.5. Remove duplicate books before chunking
        deduped_files = _dedupe_docs_by_book_id(files)
        skipped_books = len(files) - len(deduped_files)
        if skipped_books > 0:
            print(f"Skipped {skipped_books} duplicate books during ingestion.")

        #2. Chunk files
        chunks = chunk_docs(deduped_files, debug_mode=True)

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
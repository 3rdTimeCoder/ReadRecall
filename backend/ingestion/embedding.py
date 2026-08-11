import os
import getpass
import hashlib
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document


load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")


embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")


def _stable_chunk_id(chunk: Document) -> str:
    """Builds a deterministic id for a chunk.

    The id is derived from stable metadata and content, allowing the
    ingestion pipeline to safely skip duplicates across repeated ingests.
    """
    metadata = chunk.metadata or {}

    identity_parts = [
        str(metadata.get("book_id", "")),
        str(metadata.get("title", "")),
        str(metadata.get("author", "")),
        str(metadata.get("chapter", "")),
        str(metadata.get("chunk_index", "")),
        str(metadata.get("chunks_in_book", "")),
        chunk.page_content.strip(),
    ]

    payload = "||".join(identity_parts)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _dedupe_chunks(chunks: list[Document]) -> tuple[list[Document], list[str]]:
    """Removes duplicate chunks in-memory and returns aligned chunk ids."""
    deduped_chunks: list[Document] = []
    deduped_ids: list[str] = []
    seen_ids: set[str] = set()

    for chunk in chunks:
        chunk_id = _stable_chunk_id(chunk)
        if chunk_id in seen_ids:
            continue

        seen_ids.add(chunk_id)
        deduped_chunks.append(chunk)
        deduped_ids.append(chunk_id)

    return deduped_chunks, deduped_ids


def create_vector_store(
        chunks: list[Document], 
        persist_dir="db/chroma_db", 
        collection="readrecall-book-chunks"
    ) -> bool:
    """Creates a new ChromaDB vector store from a list of document chunks.

    Embeds the chunks using the OpenAI embedding model and persists the
    resulting vector store to disk with cosine similarity as the distance metric.

    Args:
        chunks: The document chunks to embed and store.
        persist_dir: Directory path for ChromaDB persistence. Defaults to 'db/chroma_db'.
        collection: Name of the ChromaDB collection. Defaults to 'readrecall-book-chunks'.

    Returns:
        True if the vector store was created successfully, False otherwise.
    """
    print("Embedding chunks and storing in vector db...")
    deduped_chunks, chunk_ids = _dedupe_chunks(chunks)

    skipped = len(chunks) - len(deduped_chunks)
    if skipped > 0:
        print(f"Skipped {skipped} duplicate chunks before initial persist.")

    try:
        _ = Chroma.from_documents(
            documents=deduped_chunks,
            ids=chunk_ids,
            embedding=embedding_model,
            persist_directory=persist_dir,
            collection_name=collection,
            collection_metadata={"hnsw:space": "cosine"}
        )
    except Exception as e:
        print(f"Error occurred while creating vector store: {e}")
        return False

    print(f"chunks persisted to db: {persist_dir}")
    return True


def load_vector_store(
        persist_dir="db/chroma_db", 
        collection="readrecall-book-chunks"
    ) -> Chroma:
    """Loads an existing ChromaDB vector store from disk.

    Args:
        persist_dir: Directory path where ChromaDB persists data. Defaults to 'db/chroma_db'.
        collection: Name of the ChromaDB collection. Defaults to 'readrecall-book-chunks'.

    Returns:
        The loaded Chroma vector store instance.
    """
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

    vector_store = Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding_model,
        collection_name=collection,
    )

    return vector_store


def persist_chunks(
        chunks: list[Document],
        persist_dir="db/chroma_db",
        collection="readrecall-book-chunks"
    ) -> bool:
    """Appends new document chunks to an existing ChromaDB vector store.

    Loads the existing vector store and adds the provided chunks to it.

    Args:
        chunks: The new document chunks to add.
        persist_dir: Directory path for ChromaDB persistence. Defaults to 'db/chroma_db'.
        collection: Name of the ChromaDB collection. Defaults to 'readrecall-book-chunks'.

    Returns:
        True if chunks were persisted successfully, False otherwise.
    """
    try:
        vector_store = load_vector_store(persist_dir=persist_dir, collection=collection)
        deduped_chunks, deduped_ids = _dedupe_chunks(chunks)

        existing_ids: set[str] = set()
        try:
            current = vector_store.get(include=[])
            existing_ids = set(current.get("ids", []))
        except Exception as read_error:
            print(f"Warning: unable to read existing ids for dedupe: {read_error}")

        new_chunks: list[Document] = []
        new_ids: list[str] = []

        for chunk, chunk_id in zip(deduped_chunks, deduped_ids):
            if chunk_id in existing_ids:
                continue
            new_chunks.append(chunk)
            new_ids.append(chunk_id)

        if len(new_chunks) == 0:
            print("No new chunks to persist. All candidate chunks already exist.")
            return True

        vector_store.add_documents(new_chunks, ids=new_ids)

        skipped = len(chunks) - len(new_chunks)
        if skipped > 0:
            print(f"Skipped {skipped} duplicate chunks already present in vector db.")
    except Exception as e:
        print(f"Error occurred while persisting chunks db: {e}")
        return False
    
    return True
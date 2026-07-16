import os
import getpass
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document


load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")


embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")


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

    try:
        _ = Chroma.from_documents(
            documents=chunks,
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
        vector_store.add_documents(chunks)
    except Exception as e:
        print(f"Error occurred while persisting chunks db: {e}")
        return False
    
    return True
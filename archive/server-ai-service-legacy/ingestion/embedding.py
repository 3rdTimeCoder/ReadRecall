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
    """TODO: write docstring"""

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
    """TODO: write docstring"""
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
    """TODO: write docstring"""
    try:
        vector_store = load_vector_store(persist_dir=persist_dir, collection=collection)
        vector_store.add_documents(chunks)
    except Exception as e:
        print(f"Error occurred while persisting chunks db: {e}")
        return False
    
    return True
    

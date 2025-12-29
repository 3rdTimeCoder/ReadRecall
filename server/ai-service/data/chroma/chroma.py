from langchain_chroma import Chroma
from config import embeddings

vector_store = Chroma(
    collection_name='my_library',
    embedding_function=embeddings
    persist_directory="./chroma_persistent_db"
)
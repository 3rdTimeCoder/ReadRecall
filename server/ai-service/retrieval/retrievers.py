from typing import Tuple
from langchain_core.documents import Document
from ingestion.embedding import load_vector_store


def get_retriever(k=5):
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": k,
            "score_threshold": 0.3
        }
    )

    return retriever


def query_db(query: str, k=5, threshold=0.3) -> list[Tuple[Document, float]]:
    vector_store = load_vector_store()
    results = vector_store.similarity_search_with_score(
        query=query,
        k=k
    )
    results_above_threshold = [(doc, score) for doc,score in results if score >= threshold]

    return results_above_threshold

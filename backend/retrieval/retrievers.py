from typing import Tuple
from langchain_core.documents import Document
from ingestion.embedding import load_vector_store


def get_retriever(k=5):
    """Creates a similarity-search retriever from the vector store.

    Configures the retriever with a score threshold filter to only return
    chunks with a similarity score above the threshold.

    Args:
        k: The number of top results to retrieve. Defaults to 5.

    Returns:
        A configured LangChain retriever object.
    """
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
    """Queries the vector store with a similarity search and filters by threshold.

    Embeds the query, searches the ChromaDB vector store for the top k chunks,
    and filters the results to only include those with a similarity score at
    or above the threshold.

    Args:
        query: The free-form text query (memory fragment) to search for.
        k: The number of top results to retrieve. Defaults to 5.
        threshold: The minimum similarity score threshold. Defaults to 0.3.

    Returns:
        A list of (Document, float) tuples where the float is the similarity
        score (lower is more similar), filtered to scores >= threshold.
    """
    vector_store = load_vector_store()
    results = vector_store.similarity_search_with_score(
        query=query,
        k=k
    )
    results_above_threshold = [(chunk, score) for chunk,score in results if score >= threshold]

    return results_above_threshold
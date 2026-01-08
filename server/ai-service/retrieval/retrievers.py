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


def query_db(query: str, k=5):
    retriever = get_retriever(k)
    results = retriever.invoke(query)
    return results

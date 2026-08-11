from math import log
from retrieval.retrievers import query_db
from langchain_core.documents import Document
from typing import Tuple


def get_user_query() -> str:
    """Gets query from user via stdin.

    Returns:
        The non-empty query string entered by the user.
    """
    query = ""
    while not query:
        query = input("What book are you looking for today?\n")
    return query


def get_top_matching_chunks(query: str, debug_mode=False) -> list[Document]:
    """Performs similarity search and returns the top matching chunks.

    Queries the vector store for the top 10 chunks matching the given query,
    optionally printing debug information about each match.

    Args:
        query: The free-form memory fragment to search for.
        debug_mode: If True, prints match details. Defaults to False.

    Returns:
        A list of (Document, float) tuples containing matching chunks and
        their similarity scores.
    """
    print("\nSearching your library...")
    
    chunks = query_db(query=query, k=10)

    if debug_mode:
        for i,m in enumerate(chunks):
            metadata = m.metadata
            print(f"\n\nmatch no.{i+1}: chunk from {metadata['title']} by {metadata['author']}")
            print(f"metadata: {metadata}")

    return chunks


def aggregate_similarity_scores(
        chunks: list[Tuple[Document, float]]
    ) -> dict[str, float]:
    """Aggregates similarity scores from chunks grouped by book ID.

    Sums the similarity scores of all chunks belonging to the same book.

    Args:
        chunks: A list of (Document, similarity_score) tuples.

    Returns:
        A dictionary mapping book_id to total aggregated similarity score.
    """
    book_scores = {}

    for chunk,similarity_score in chunks:
        book_id = chunk.metadata['book_id']
        book_scores[book_id] = book_scores.get(book_id, 0.0) + similarity_score
    
    return book_scores


def calculate_scores(chunks: list[Tuple[Document, float]], book_hits: dict):
    """Calculates final ranking scores for each book.

    Uses a heuristic formula: average similarity score per book multiplied
    by a logarithmic reinforcement factor for hit count. Books with more
    matching chunks get a boost, up to a cap of 5 hits.

    Args:
        chunks: A list of (Document, similarity_score) tuples.
        book_hits: A dictionary mapping book_id to number of chunk hits.

    Returns:
        A dictionary mapping book_id to final score, sorted descending by score.
    """
    book_scores = {}

    similarity_scores = aggregate_similarity_scores(chunks=chunks)

    for book_id, total_similarity in similarity_scores.items():
        avg_score = total_similarity / book_hits[book_id]
        reinforcement = log(1 + min(book_hits[book_id], 5))
        final_score = avg_score * reinforcement
        book_scores[book_id] = final_score
    
    ordered_book_scores = dict(sorted(book_scores.items(), key=lambda item: item[1], reverse=True))
    return ordered_book_scores


def group_chunks_by_book(chunks: list[Tuple[Document, float]]):
    """Groups chunk matches by book and counts hits per book.

    Args:
        chunks: A list of (Document, similarity_score) tuples.

    Returns:
        A tuple of (book_hits, book_info):
            - book_hits: dict mapping book_id to hit count.
            - book_info: dict mapping book_id to the metadata of the first chunk.
    """
    book_hits = {}
    book_info = {}
    
    for chunk,_ in chunks:
        metadata = chunk.metadata
        book_id = metadata['book_id']
        if book_hits.get(metadata['book_id']):
            book_hits[book_id] = book_hits[book_id] + 1
        else:
            book_hits[book_id] = 1
            book_info[book_id] = metadata

    return book_hits, book_info


def get_book_suggestions(chunks: list[Tuple[Document, float]]):
    """Generates book suggestions from a list of matching chunks.

    Groups chunks by book, calculates a ranking score for each book using
    a combination of hit count and similarity aggregation, and returns the
    top match plus other suggestions.

    Args:
        chunks: A list of (Document, similarity_score) tuples from the
            similarity search.

    Returns:
        A dict with:
            - 'top_match': metadata of the highest-scoring book.
            - 'other_suggestions': list of metadata for remaining books.
    """
    book_suggestions= {}
    book_hits, book_info = group_chunks_by_book(chunks)
    book_scores = calculate_scores(chunks=chunks, book_hits=book_hits)
    
    top_match_id = list(book_scores)[0]
    top_match_info = book_info[top_match_id]
    book_suggestions['top_match'] = top_match_info

    other_suggestions = []

    for i, key in enumerate(book_scores.keys()):
        if i == 0: continue
        other_suggestions.append(book_info[key])
        
    book_suggestions['other_suggestions'] = other_suggestions
    
    return book_suggestions


def display_results(results: dict) -> None:
    """Displays the search results on the terminal.

    Prints the top matching book and any other suggestions with their
    title, author, and truncated description.

    Args:
        results: A dict with 'top_match' and 'other_suggestions' keys,
            as returned by get_book_suggestions().
    """
    print(f"\nThe mostly likely book is {results['top_match']['title']} by {results['top_match']['author']}")
    print(f"Description: {results['top_match']['description'][:500]}...")

    other_suggestions = results['other_suggestions']
    if len(other_suggestions) > 0:
        print("\nOther suggestions:")
        for book in other_suggestions:
            print(f"\nBook: {book['title']} by {book['author']}")
            print(f"Description: {book['description'][:500]}...")


def recall(query: str):
    """Full recall pipeline: search, score, rank, and display results.

    Args:
        query: The free-form memory fragment to search for.
    """
    chunks =  get_top_matching_chunks(query=query)
    top_books = get_book_suggestions(chunks=chunks)
    display_results(top_books)
    

if __name__ == '__main__':
    print("Hello, welcome to ReadRecall!!!\n")
    query = get_user_query()
    recall(query=query)
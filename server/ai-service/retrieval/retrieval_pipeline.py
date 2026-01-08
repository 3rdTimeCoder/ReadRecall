from retrieval.retrievers import query_db
from langchain_core.documents import Document


def get_user_query() -> str:
    """Gets query from user"""
    query = ""
    while not query:
        query = input("What book are you looking for today?\n")
    return query


def get_top_matching_chunks(query: str, debug_mode=False) -> list[Document]:
    print("\nSearching your library...")
    chunks = query_db(query=query, k=10)

    print(f"matches retrieved: {len(chunks)}")

    if debug_mode:
        for i,m in enumerate(chunks):
            metadata = m.metadata
            print(f"\n\nmatch no.{i+1}: chunk from {metadata['title']} by {metadata['author']}")
            print(f"metadata: {metadata}")

    return chunks


def get_book_suggestions(chunks: list[Document]) -> list[Document]:
    book_count = {}
    book_info = {}
    book_suggestions = {}
    
    for chunk in chunks:
        metadata = chunk.metadata
        book = metadata['title']
        if book_count.get(metadata['title']):
            book_count[book] = book_count[book] + 1
        else:
            book_count[book] = 1
            book_info[book] = metadata
    
    ordered_book_count = dict(sorted(book_count.items(), key=lambda item: item[1], reverse=True))
    top_match = list(ordered_book_count)[0]
    top_match_info = book_info[top_match]
    book_suggestions['top_match'] = top_match_info

    print(f"\nThe mostly likely book is {top_match} by {top_match_info['author']}")
    print(f"Description: {top_match_info['description'][:500]}...")


    other_suggestions = []

    if len(ordered_book_count) > 1:
        print(f"\nOther suggestions:\n")

        for i, key in enumerate(ordered_book_count.keys()):
            if i == 0: continue
            other_suggestions.append(book_info[key])

            print(f"\n{key} by {book_info[key]['author']}")
            print(f"Description: {book_info[key]['description'][:500]}...")
        
        book_suggestions['other_suggestions'] = other_suggestions

    
    return book_suggestions


    

if __name__ == '__main__':
    print("Hello, welcome to ReadRecall!!!\n")
    query = get_user_query()
    chunks =  get_top_matching_chunks(query=query)
    top_books = get_book_suggestions(chunks=chunks)


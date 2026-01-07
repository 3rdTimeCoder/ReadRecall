from langchain_text_splitters import RecursiveCharacterTextSplitter
from lib.Document import Document

def split_text(text: str) -> list:
    """TODO: write docstring"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )

    chunks = text_splitter.split_documents(text)

    print(f"\nchunk {i + 1}: {chunk}" for i,chunk in enumerate(chunks))


def chunk_doc(doc: Document):
    # Reminder:
    # Each document has the structure (metadata : metadata, sections: sections)
    # Each section has the structure (metadata: metadata, content: content)
    # *metadata in section = the normal book metadata excl. desc & incl. chapter
    # So a Document contains a list of sections (chapters) and each section contains metadata (incl. chapter) and the actual content of that section which is just plain text
    pass
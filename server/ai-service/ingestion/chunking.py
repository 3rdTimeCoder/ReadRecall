from langchain_text_splitters import RecursiveCharacterTextSplitter
from lib.Document import Document
from langchain_core.documents import Document as LCDocument


def split_text(text: str, metadata) -> list[LCDocument]:
    """TODO: write docstring"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000,
        chunk_overlap=200,
        add_start_index=True
    )

    chunks = text_splitter.split_documents([LCDocument(
        page_content=text,
        metadata=metadata
    )])

    return chunks


def update_metadata(chunk: LCDocument, new_entry) -> LCDocument:
    updated_chunk = LCDocument(
        page_content=chunk.page_content,
        metadata={**chunk.metadata, **new_entry}
    )

    return updated_chunk
    

def chunk_doc(doc: Document) -> list[LCDocument]:
    """TODO: write docstring"""
    chunks = []
    sections = doc.get_sections()

    for section in sections:
        chunks.extend(split_text(section.get_content(), section.get_metadata()))
    
    chunks_in_book = len(chunks)

    for i,chunk in enumerate(chunks):
        updated_chunk = update_metadata(chunk, {'chunk_index': i+1, 'chunks_in_book': chunks_in_book})
        chunks[i] = updated_chunk
        print(f"\nchunk {i + 1}: {chunks[i]}")
        print(f"chars: {len(chunks[i].page_content)}")

    return chunks


def chunk_docs(docs: list[Document]):
    """TODO: write docstring"""
    pass


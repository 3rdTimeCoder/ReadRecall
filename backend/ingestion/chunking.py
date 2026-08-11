from langchain_text_splitters import RecursiveCharacterTextSplitter
from lib.Document import Document
from langchain_core.documents import Document as LCDocument


def split_text(text: str, metadata) -> list[LCDocument]:
    """Splits a text string into overlapping chunks using RecursiveCharacterTextSplitter.

    Each chunk is up to 10,000 characters with 200 characters of overlap,
    preserving start indices for traceability.

    Args:
        text: The text content to split.
        metadata: Metadata to attach to each resulting chunk.

    Returns:
        A list of LangChain Document objects representing the chunks.
    """
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
    """Merges new metadata into an existing chunk's metadata.

    Args:
        chunk: The LangChain Document whose metadata to update.
        new_entry: A dictionary of new metadata fields to merge in.

    Returns:
        A new LangChain Document with the combined metadata.
    """
    updated_chunk = LCDocument(
        page_content=chunk.page_content,
        metadata={**chunk.metadata, **new_entry}
    )

    return updated_chunk
    

def chunk_doc(doc: Document, debug_mode=False) -> list[LCDocument]:
    """Splits a single Document into multiple LangChain chunks.

    Iterates over each section in the document, splits the section text into
    overlapping chunks, and annotates each chunk with its index within the book.

    Args:
        doc: The Document (book) to split into chunks.
        debug_mode: If True, prints chunk index and character count. Defaults to False.

    Returns:
        A list of LangChain Document chunks with updated metadata.
    """
    chunks = []
    sections = doc.get_sections()

    for section in sections:
        chunks.extend(split_text(section.get_content(), section.get_metadata()))
    
    chunks_in_book = len(chunks)

    for i,chunk in enumerate(chunks):
        updated_chunk = update_metadata(chunk, {'chunk_index': i+1, 'chunks_in_book': chunks_in_book})
        chunks[i] = updated_chunk
        if debug_mode:
            print(f"\nchunk {i + 1}: {chunks[i]}")
            print(f"chars: {len(chunks[i].page_content)}")

    return chunks


def chunk_docs(docs: list[Document], debug_mode=False):
    """Splits a list of Documents into LangChain chunks.

    Args:
        docs: A list of Document objects (books) to split.
        debug_mode: If True, prints debug info for each chunk. Defaults to False.

    Returns:
        A list of LangChain Document chunks across all input documents.
    """
    chunks = []
    for doc in docs:
        chunks.extend(chunk_doc(doc, debug_mode=debug_mode))

    return chunks
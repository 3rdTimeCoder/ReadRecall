import os
from langchain_community.document_loaders import PyPDFLoader
from lib import EPubLoader, DirectoryLoader


def load_doc(doc: str, type="epub"):
    """Loads a single document from a file path.

    Supports EPUB files via EPubLoader and PDF files via PyPDFLoader.

    Args:
        doc: Path to the document file.
        type: File type of the document ('epub' or 'pdf'). Defaults to 'epub'.

    Returns:
        The loaded Document object.

    Raises:
        FileNotFoundError: If the specified path does not exist.
        Exception: If the file type is unsupported.
    """
    print(f"{os.path.basename(doc)} loading in initiated...")

    if not os.path.exists(doc):
        raise FileNotFoundError(f"path {doc} not found. Please ensure that the specified document exists.")

    if (type == "epub"):
        loader = EPubLoader(doc)
        data = loader.load()
        return data
    elif (type == "pdf"):
        loader = PyPDFLoader(doc)
        data = loader.load()
        return data[0]
    else: raise Exception(f"Unsupported file type: {type}")
    
    
def load_docs_from_dir(dir: str, type="epub", debug_mode=False):
    """Loads all documents of a given type from a directory.

    Uses the appropriate loader (EPubLoader or PyPDFLoader) based on the
    specified file type and loads all matching files in the directory.

    Args:
        dir: Path to the directory containing the documents.
        type: File type to load ('epub' or 'pdf'). Defaults to 'epub'.
        debug_mode: If True, prints metadata for each loaded document. Defaults to False.

    Returns:
        A list of Document objects loaded from the directory.

    Raises:
        FileNotFoundError: If the directory does not exist or contains no matching files.
    """
    print(f"Loading documents in directory {dir} initiated...")

    if not os.path.exists(dir):
        raise FileNotFoundError(f"path {dir} not found. Please ensure that the specified document exists.")
    
    loader_cls = EPubLoader if type == "epub" else PyPDFLoader
    loader = DirectoryLoader(
        dir_path=dir,
        loader=loader_cls
    )

    docs = loader.load()

    if (len(docs) == 0):
        raise FileNotFoundError(f"No .{type} files found. Please add documents.") 
    
    if debug_mode:
        for i, doc in enumerate(docs[:9]):
            print(f"{i+1}. Source: {doc.metadata['title']}\nAuthor: {doc.metadata['author']}")
            print(f"Metadata: {doc.metadata}\n")

    return docs


    
def main():
    print("loader.py main running...")
    load_docs_from_dir("./test-docs", type="epub", debug_mode=True)


if __name__ == "__main__":
    main()
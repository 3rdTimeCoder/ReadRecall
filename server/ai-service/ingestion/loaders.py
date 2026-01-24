import os
from langchain_community.document_loaders import PyPDFLoader
from lib import EPubLoader, DirectoryLoader


def load_doc(doc: str, type="epub"):
    """Load the document passed to this function"""
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
    """Loads all the documents in given directory"""
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
            # print(f"{i+1}. Source: {doc.metadata['source']}\nCharacters: {len(doc.page_content)}")
            # print(f"Preview: {doc.page_content.strip()[:300]}...\nMetadata: {doc.metadata}\n")
            print(f"{i+1}. Source: {doc.metadata['title']}\nAuthor: {doc.metadata['author']}")
            print(f"Metadata: {doc.metadata}\n")

    
    return docs


# def load_docs(files: list, type="epub", debug_mode=False):
#     """Loads all the given books/files as the correct Document format/type"""
#     print(f"Loading documents initiated...")
    
#     loader_cls = EPubLoader if type == "epub" else PyPDFLoader
#     loader = DirectoryLoader(loader=loader_cls)

#     docs = loader.load_files(files=files)

#     if (len(docs) == 0):
#         raise FileNotFoundError(f"No .{type} files found. Please add documents.") 
    
#     if debug_mode:
#         for i, doc in enumerate(docs[:9]):
#             # print(f"{i+1}. Source: {doc.metadata['source']}\nCharacters: {len(doc.page_content)}")
#             # print(f"Preview: {doc.page_content.strip()[:300]}...\nMetadata: {doc.metadata}\n")
#             print(f"{i+1}. Source: {doc.metadata['title']}\nAuthor: {doc.metadata['author']}")
#             print(f"Metadata: {doc.metadata}\n")

    
#     return docs

    
def main():
    print("loader.py main running...")
    load_docs("./test-docs", type="epub", debug_mode=True)


if __name__ == "__main__":
    main()

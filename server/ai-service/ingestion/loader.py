from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredEPubLoader


def load_doc(doc: str, type="epub"):
    if (type == "epub"):
        loader = UnstructuredEPubLoader(doc)
        data = loader.load()
        return data
    elif (type == "pdf"):
        loader = PyPDFLoader(doc)
        data = loader.load()
        return data
    else:
        return None  
    
    
# print(f"Total characters: {len(data[0].page_content)}")


from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredEPubLoader


def load_doc(doc: str, type="epub"):
    """Load the document passed to this function"""
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
    
    



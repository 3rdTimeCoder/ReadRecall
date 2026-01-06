

class Document:

    def __init__(self, metadata, sections):
        """
        Args:
            metadata: The epub's metadata
            sections: A list of the epub's different sections
        """
        self.metadata = metadata
        self.sections = sections

    
    def get_metadata(self):
        """Returns the Documents's metadata: 
        The book title, author, publisher and description
        """
        return self.metadata
    

    def get_sections(self):
        """Returns a list of the Document's sections"""
        return self.sections
    
    
    def __str__(self):
        return f"Document(metadata: {self.metadata}, sections: {self.sections})"
    
    
    def __repr__(self):
        return f"Document(metadata: {self.metadata}, sections: {self.sections})"
from uuid import uuid4
from lib.Section import Section


class Document:
    """Represents a book document composed of metadata and a list of sections.

    Each Document corresponds to one loaded book file (EPUB or PDF) and
    contains its bibliographic metadata and chapter-level sections.
    """

    def __init__(self, metadata, sections: list[Section]):
        """Initializes a Document.

        Args:
            metadata: A dictionary containing book metadata such as title,
                author, publisher, and description.
            sections: A list of Section objects representing the book's
                chapters or content divisions.
        """
        self.metadata = metadata
        self.sections = sections

    
    def get_metadata(self):
        """Returns the Document's metadata.

        The metadata includes the book title, author, publisher, and description.

        Returns:
            A dictionary of the book's metadata.
        """
        return self.metadata
    

    def get_sections(self):
        """Returns a list of the Document's sections.

        Returns:
            A list of Section objects comprising the document.
        """
        return self.sections
    
    
    def __str__(self):
        return f"Document(metadata: {self.metadata}, sections: {self.sections})"
    
    
    def __repr__(self):
        return f"Document(metadata: {self.metadata}, sections: {self.sections})"
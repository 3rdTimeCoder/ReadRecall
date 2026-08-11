class Section:
    """Represents a single section or chapter within a book document.

    Each Section holds the text content for one chapter (or document item)
    along with its associated metadata.
    """

    def __init__(self, metadata, content):
        """Initializes a Section.

        Args:
            metadata: A dictionary containing metadata for the section,
                including title, author, publisher, and chapter.
            content: The plain text content of the section.
        """
        self.metadata = metadata
        self.content = content

    
    def get_metadata(self):
        """Returns the Section's metadata.

        The metadata includes the book title, author, publisher, and chapter.

        Returns:
            A dictionary of the section's metadata.
        """
        return self.metadata
    

    def get_content(self):
        """Returns the Section's text content.

        Returns:
            The plain text string of the section.
        """
        return self.content
    
    
    def __str__(self):
        return f"Section(metadata: {self.metadata}, content: {self.content[:100]}...)"
    
    
    def __repr__(self):
        return f"Section(metadata: {self.metadata}, content: {self.content[:100]}...)"
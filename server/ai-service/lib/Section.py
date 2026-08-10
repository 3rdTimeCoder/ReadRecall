

class Section:

    def __init__(self, metadata, content):
        """
        Args:
            metadata: The given section's metadata
            content: The given section's text content
        """
        self.metadata = metadata
        self.content = content

    
    def get_metadata(self):
        """Returns Section's metadata: 
        The book title, author, publisher and chapter
        """
        return self.metadata
    

    def get_content(self):
        """Returns the Section's content"""
        return self.content
    
    
    def __str__(self):
        return f"Section(metadata: {self.metadata}, content: {self.content[:100]}...)"
    
    
    def __repr__(self):
        return f"Section(metadata: {self.metadata}, content: {self.content[:100]}...)"
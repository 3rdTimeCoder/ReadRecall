import os
from typing import Union
from pathlib import Path
from ebooklib import epub
import ebooklib
from bs4 import BeautifulSoup
from uuid import uuid4


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


class Document:

    def __init__(self, metadata, sections: list[Section]):
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


class EPubLoader:
    """Loads Epub files using ebooklib and BeautifulSoup.
    Documentation for ebooklib can be found here: https://docs.sourcefabric.org/projects/ebooklib/en/latest/tutorial.html#reading-epub
    """

    def __init__(self, file_path: Union[str, Path]):
        """Args:
            file_path: The path to the EPub file to load.
        """
        self.file_path = file_path


    def _get_value(self, book: epub.EpubBook, key: str) -> str:
        """Returns the value of the given key inside the epub's metadata
        Args:
            book: The epub we want to extract metadata from
            key: The key of the specific metadata to be returned.
        Returns:
            value: The value of the key in the metadata
        """
        data = book.get_metadata('DC', key)
        if len(data) <= 0 or len(data[0]) <= 0: return ""
        return book.get_metadata('DC', key)[0][0]


    def _parse_html(self, html: str) -> str:
        """Returns html as text"""
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text('\n')
        return text
    
    
    def get_metadata(self, book: epub.EpubBook) -> dict:
        """Extracts and returns the metadata from an epub file"""
        metadata = {
            'book_id': str(uuid4()),
            'title': self._get_value(book, 'title'),
            'author': self._get_value(book, 'creator'),
            'publisher': self._get_value(book, 'publisher'),
            'description': self._parse_html(self._get_value(book, 'description')),
            #TODO: add cover-img later on for frontend
        }
        
        return metadata


    def _split_text_into_chapters(self, book: epub.EpubBook) -> list[Section]: 
        """TODO: write docstring"""
        doc_data = []
        metadata = self.get_metadata(book)
        # metadata.pop('description') # Commenting this out because I think its beneficial for each chunk to contain the book's description

        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            text = self._parse_html(item.get_content())
            updated_metadata = { **metadata, 'chapter':  text.strip()[:100].split('\n')[0] }
            doc_data.append(Section(updated_metadata, text.strip()))

        return doc_data
    

    def load(self):
        """Extracts and returns the text from an epub file
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Error while loading file {os.path.basename(self.file_path)}. File not found.")
        
        book = epub.read_epub(self.file_path)
        metadata = self.get_metadata(book)

        doc_sections = self._split_text_into_chapters(book)
        doc_data = Document(metadata, doc_sections)
        return doc_data
        


def main():
    # doc = EPubLoader("../test-docs/Behind_the_Locked_Door.epub")
    doc = EPubLoader("../test-docs/I_Remember_Our_Love.epub")
    data = doc.load()


if __name__ == "__main__":
    main()
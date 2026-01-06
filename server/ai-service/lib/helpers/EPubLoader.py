import os
from typing import Union
from pathlib import Path
from ebooklib import epub
import ebooklib
from bs4 import BeautifulSoup


class EPubLoader:
    """Loads Epub files using ebooklib and BeautifulSoup.
    Documentation for ebooklib can be found here: https://docs.sourcefabric.org/projects/ebooklib/en/latest/tutorial.html#reading-epub
    """

    def __init__(self, file_path: Union[str, Path]):
        """Args:
            file_path: The path to the EPub file to load.
        """
        self.file_path = file_path

    def get_value(book: epub.EpubBook, key: str) -> str:
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
    
    def get_metadata() -> dict:
        """Extracts and returns the metadata from an epub file"""
        metadata = dict()
        #TODO



    def load(self):
        """Extracts and returns the text from an epub file
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Error while loading file {os.path.basename(self.file_path)}. File not found.")
        
        book = epub.read_epub(self.file_path)
        text_data = []
        metadata = dict()

        print(f"title: {book.get_metadata('DC', 'title')[0][0]}")
        print(f"author: {book.get_metadata('DC', 'creator')[0][0]}")
        print(f"publisher: {book.get_metadata('DC', 'publisher')}") #Most fanfiction will have the publisher 'Archive of our own'
        print(f"desc: {book.get_metadata('DC', 'description')}")
        # print(f"book cover: {book.get_item_with_id('cover-image').get_content()}")

        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            soup = BeautifulSoup(item.get_content(), "html.parser")
            text = soup.get_text('\n')
            text_data.append(text)
        
        full_text = "\n".join(text_data)
        

        print(f"characters: {len(full_text)}")
        print(f"preview: {full_text.strip()[:500]}")
        


def main():
    doc = EPubLoader("../../test-docs/The Faithless (C. L. Clark) (Z-Library).epub")
    # doc = EPubLoader("../../test-docs/I_Remember_Our_Love.epub")
    data = doc.load()


if __name__ == "__main__":
    main()
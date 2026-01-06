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
            'title': self._get_value(book, 'title'),
            'author': self._get_value(book, 'creator'),
            'publisher': self._get_value(book, 'publisher'),
            'description': self._parse_html(self._get_value(book, 'description'))
            #TODO: add cover-img later on for frontend
        }
        
        return metadata


    def _split_text_into_chapters(self, book: epub.EpubBook) -> list: 
        # TODO: return as list of "objects(JS terminology)", each object being a separate chapter, that look like this:
        # {'metadata': normal metadata excluding description and cover_img, 'content': the actual chapter text content}
        doc_data = []
        _metadata = self.get_metadata(book)
        _metadata.pop('description')
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            # print(f"item: {item}")
            text = self._parse_html(item.get_content())
            # print(f"item_preview: {text.strip()[:100]}\n")
            _metadata['chapter']  = text.strip()[:100].split('\n')[0]
            # print(text.strip()[:100].split('\n'))
            # print('\n\n')
           

            doc_data.append({
                'metadata': _metadata,
                'content': text.strip()
            })

        return doc_data

    def load(self):
        """Extracts and returns the text from an epub file
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Error while loading file {os.path.basename(self.file_path)}. File not found.")
        
        book = epub.read_epub(self.file_path)
        # toc = book.toc
        # print(f"toc: {toc}")
        metadata = self.get_metadata(book)
        print(f"metadata: {metadata}")

        doc_data = self._split_text_into_chapters(book)
        print(doc_data)
        # for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        #     print(f"item: {item}")
        #     text = self._parse_html(item.get_content())
        #     text_data.append(text)
        
        # full_text = "\n".join(text_data)
        

        # print(f"characters: {len(full_text)}")
        # print(f"preview: {full_text.strip()[:500]}")
        


def main():
    # doc = EPubLoader("../../test-docs/The Faithless (C. L. Clark) (Z-Library).epub")
    # doc = EPubLoader("../../test-docs/Behind_the_Locked_Door.epub")
    # doc = EPubLoader("../../test-docs/I_Remember_Our_Love.epub")
    doc = EPubLoader("../../ingestion/Those Who Wait (Haley Cass) (Z-Library).epub")
    data = doc.load()


if __name__ == "__main__":
    main()
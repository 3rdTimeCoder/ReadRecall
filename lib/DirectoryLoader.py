import os
from typing import Union
from pathlib import Path
from lib.EPubLoader import EPubLoader
from lib.Document import Document


class DirectoryLoader: 
    
    def __init__(self, dir_path:  Union[str, Path], loader):
        """Initializes a DirectoryLoader.

        Args:
            dir_path: Path to the directory containing files to load.
            loader: The loader class to use for individual files
                (e.g., EPubLoader or PyPDFLoader).
        """
        self.dir_path = dir_path
        self.loader = loader


    def _get_files(self):
        """Return list of files in directory.

        Returns:
            A list of Path objects for each file in the directory.
        """
        path = Path(self.dir_path)
        files = [p for p in path.iterdir() if p.is_file()]
        return files


    def _load_files(self, files: list) -> list[Document]:
        """Loads each file in the given list using the configured loader.

        Args:
            files: A list of file paths to load.

        Returns:
            A list of Document objects loaded from the files.
        """
        docs = []
        for f in files:
            loader = self.loader(Path(f))
            f_data = loader.load()
            docs.append(f_data)

        return docs
    

    def load(self):
        """Loads all files in the directory.

        Retrieves the list of files from the directory, loads each one
        using the configured loader class, and returns the resulting documents.

        Returns:
            A list of Document objects for all files in the directory.
        """
        files = self._get_files()
        docs = self._load_files(files)
        return docs


def main():
    d = DirectoryLoader("./test-docs", EPubLoader)
    d.load()



if __name__ == "__main__":
    main()
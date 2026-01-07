import os
from typing import Union
from pathlib import Path
from lib.EPubLoader import EPubLoader
from lib.Document import Document


class DirectoryLoader: 
    
    def __init__(self, dir_path:  Union[str, Path], loader):
        self.dir_path = dir_path
        self.loader = loader


    def _get_files(self):
        """Return list of files in directory"""
        path = Path(self.dir_path)
        files = [p for p in path.iterdir() if p.is_file()]
        return files


    def _load_files(self, files: list) -> list[Document]:
        docs = []
        """TODO: write docstring"""
        for f in files:
            loader = self.loader(Path(f))
            f_data = loader.load()
            docs.append(f_data)

        return docs
    

    def load(self):
        """TODO: write docstring"""
        files = self._get_files()
        docs = self._load_files(files)
        return docs


def main():
    d = DirectoryLoader("./test-docs", EPubLoader)
    d.load()



if __name__ == "__main__":
    main()
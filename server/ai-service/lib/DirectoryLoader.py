import os
from typing import Union
from pathlib import Path


class DirectoryLoader: 
    
    def __init__(self, dir_path:  Union[str, Path], loader):
        self.dir_path = dir_path
        self.loader = loader


    def _get_files(self):
        """Return list of file_paths (files) in directory"""
        pass


    def _load_files(self, files: list) -> list:
        docs = []
        """TODO: loop through files array and load each doc using loader and append to docs array"""
        pass
    

    def load(self):
        # 1. get list of file_paths
        files = self._get_files()
        print(f"files: {files}")
        # 2. loop through file_paths and use loader to load them one by one and append each to the docs array
        docs = self._load_files(files)
        
        return docs

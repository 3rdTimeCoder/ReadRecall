import os
from dotenv import load_dotenv
from ingestion.loaders import load_docs


load_dotenv()


def main():
    print("Inside main...")
    #1. Load files
    files = load_docs("./test-docs", type="epub", debug_mode=True)
    #2. Chunk files
    #3. Embedding and Storing in vector DB


if __name__ == "__main__":
    main()
import os
from dotenv import load_dotenv
from ingestion.loaders import load_docs
from ingestion.chunking import chunk_docs


# load_dotenv()


def main():
    print("Inside main...")
    #1. Load files
    files = load_docs("./test-docs", type="epub", debug_mode=False)
    #2. Chunk files
    chunks = chunk_docs(files, debug_mode=True)
    print(f"\n\nChunks:\n{len(chunks)}")
    #3. Embedding and Storing in vector DB


if __name__ == "__main__":
    main()
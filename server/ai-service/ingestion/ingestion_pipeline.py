import os
from dotenv import load_dotenv
from ingestion.loaders import load_docs
from ingestion.chunking import chunk_doc, split_text


# load_dotenv()


def main():
    print("Inside main...")
    #1. Load files
    files = load_docs("./test-docs", type="epub", debug_mode=False)
    #2. Chunk files
    # section = files[5].get_sections()[5]
    # print(f"Chunking section {section.get_metadata()['chapter']} from {section.get_metadata()['title']}...")
    # chunks = split_text(section.get_content(), section.get_metadata())
    chunks = chunk_doc(files[3])
    print(f"\n\nChunks:\n{len(chunks)}")

    #3. Embedding and Storing in vector DB


if __name__ == "__main__":
    main()
# ReadRecall

ReadRecall identifies which book you're thinking of from your personal library — based on nothing more than a vague memory fragment.

Users remember scenes, themes, quotes, or vibes — not titles or authors. ReadRecall bridges that gap.

## The Problem

> Users remember fragments of books (scenes, themes, quotes, vibes), not titles or authors.
> ReadRecall identifies which book they're thinking of from a personal library.

## How It Works

### 1. Ingestion (Books → Memory Units)

Books are uploaded, split into overlapping semantic chunks, enriched with metadata (title, author, chapter), embedded into vector representations, and stored in a ChromaDB vector store.

```
[Book files] → Load → Chunk → Embed → Store in ChromaDB
```

### 2. Recall (Fuzzy Memory → Book Suggestion)

A free-form memory description is embedded and used for similarity search against all chunks. The system retrieves many weak matches across books, then aggregates and scores them at the book level — because many moderate matches across a single book reflect true recall better than one strong match.

```
[Memory fragment] → Embed → Similarity search → Aggregate by book → Score → Rank → Suggest
```

### Key Design Decisions

- **Over-retrieval**: Retrieve a large number of weak matches rather than a few strong ones. Fuzzy memories rarely map cleanly to one chunk.
- **Book-level aggregation**: Group chunk matches by book, count hits, aggregate similarity scores. One strong match can be coincidence; many moderate matches across a book reflect true recall.
- **Ranking heuristics**: Score books by a combination of hit count, average similarity, and score reinforcement.

## Project Structure

```
readrecall-backend/
├── api.py                          # FastAPI server with /ingest and /recall endpoints
├── readrecall.py                   # CLI tool (Click-based)
├── requirements.txt                # Python dependencies
├── .gitignore
├── README.md
├── __tests__/
│   └── test_query_results.py       # Test suite
├── db/
│   └── chroma_db/                  # Persistent vector store (gitignored)
├── ingestion/
│   ├── __init__.py
│   ├── ingestion_pipeline.py       # Orchestrates load → chunk → embed → store
│   ├── loaders.py                  # Document loading (EPUB, PDF)
│   ├── chunking.py                 # Semantic text splitting with overlap
│   └── embedding.py                # Vector embedding and ChromaDB persistence
├── retrieval/
│   ├── retrieval_pipeline.py       # Query → aggregate → score → suggest
│   └── retrievers.py               # ChromaDB similarity search
├── lib/
│   ├── Document.py                 # Document model (metadata + sections)
│   ├── Section.py                  # Section model (chapter-level content)
│   ├── EPubLoader.py               # EPUB file parser (ebooklib + BeautifulSoup)
│   ├── DirectoryLoader.py          # Directory batch loader
│   ├── IngestionType.py            # Supported file type enum
│   ├── exceptions/
│   │   ├── http.py                 # HTTP exception handler
│   │   └── validation.py           # Validation error handler
│   ├── middleware/
│   │   └── process_time.py         # Request process time header middleware
│   └── responses/
│       └── standard.py             # Standardized API response format
├── notes/                          # Design notes and strategy documents
└── test-docs/                      # Sample book files for testing
```

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd readrecall-backend

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### CLI Mode

```bash
# Ingest books from a directory
python readrecall.py --action ingest

# Recall a book from memory
python readrecall.py --action recall
```

#### API Server

```bash
# Start the FastAPI server
uvicorn api:app --reload
```

The API will be available at `http://localhost:8000`.

**Endpoints:**

| Method | Path       | Description                              |
|--------|------------|------------------------------------------|
| GET    | `/`        | Health check                             |
| POST   | `/ingest`  | Upload books and ingest into the database |
| POST   | `/recall`  | Search books by memory fragment           |

### API Examples

**Ingest books:**
```bash
curl -X POST http://localhost:8000/ingest \
  -F "files=@/path/to/book.epub" \
  -F "type=epub"
```

**Recall a book:**
```bash
curl -X POST http://localhost:8000/recall \
  -H "Content-Type: application/json" \
  -d '{"query": "A book about power and religion in the desert"}'
```

## MVP Scope

### Included
- Book upload (EPUB, PDF)
- Fuzzy memory input
- Top 3–5 book suggestions with explanations
- CLI and API interfaces

### Explicitly Excluded (MVP)
- Conversational agents
- Conversational memory
- Summarization
- Fine-grained Q&A
- Recommendation systems

## Tech Stack

- **Framework**: FastAPI (API), Click (CLI)
- **Vector Store**: ChromaDB
- **Embeddings**: Sentence Transformers (via LangChain)
- **Document Processing**: ebooklib, BeautifulSoup, pypdf
- **Text Splitting**: LangChain RecursiveCharacterTextSplitter
- **Language**: Python

## License

MIT License

Copyright (c) 2026 Nomah S. aka 3rdTimeCoder

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
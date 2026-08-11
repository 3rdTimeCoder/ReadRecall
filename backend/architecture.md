# ReadRecall Architecture

## Overview

ReadRecall identifies which book a user is thinking of from their personal library — based on nothing more than a vague memory fragment. The system bridges the gap between fuzzy human recollection and precise book identification through a two-phase pipeline: **Ingestion** (books → searchable chunks) and **Recall** (memory fragment → book suggestions).

---

## System Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                        INTERFACES                            │
│  ┌──────────────────┐          ┌──────────────────────────┐  │
│  │  FastAPI Server   │          │     Click CLI Tool       │  │
│  │  (api.py)         │          │     (readrecall.py)      │  │
│  └──────┬───────────┘          └────────┬─────────────────┘  │
└─────────┼──────────────────────────────┼────────────────────┘
          │                              │
          ▼                              ▼
┌──────────────────────────────────────────────────────────────┐
│                     INGESTION PIPELINE                        │
│                                                              │
│  ┌─────────┐    ┌──────────┐    ┌───────────┐               │
│  │  Load    │───▶│  Chunk   │───▶│  Embed &  │               │
│  │  Files   │    │  Text    │    │  Store    │               │
│  └─────────┘    └──────────┘    └─────┬─────┘               │
│                                       │                      │
└───────────────────────────────────────┼──────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────┐
│                     VECTOR STORE (ChromaDB)                   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Collection: readrecall-book-chunks                   │   │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐       │   │
│  │  │ Chunk│ │ Chunk│ │ Chunk│ │ Chunk│ │ Chunk│  ...   │   │
│  │  │ BookA│ │ BookA│ │ BookB│ │ BookB│ │ BookC│       │   │
│  │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘       │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────┐
│                      RECALL PIPELINE                         │
│                                                              │
│  ┌──────────┐    ┌──────────────┐    ┌───────────────┐      │
│  │  Embed   │───▶│  Similarity  │───▶│  Aggregate &  │      │
│  │  Query   │    │  Search      │    │  Score by Book│      │
│  └──────────┘    └──────────────┘    └───────┬───────┘      │
│                                               │              │
│                                               ▼              │
│                                        ┌───────────────┐     │
│                                        │  Rank &       │     │
│                                        │  Suggest      │     │
│                                        └───────────────┘     │
└──────────────────────────────────────────────────────────────┘
```

---

## Core Principles

### 1. Over-Retrieval

Retrieve a large number of weak matches rather than a few strong ones. Fuzzy memories rarely map cleanly to a single chunk. The system accepts noise intentionally — many moderate matches across the same book are more meaningful than one isolated strong match.

### 2. Book-Level Aggregation

Chunk matches are grouped by book. One strong match can be coincidence; many moderate matches across a book reflect true recall. This is the core innovation distinguishing ReadRecall from standard RAG systems.

### 3. Ranked Hypothesis Output

The system proposes candidates with relative confidence, not absolute answers. It mirrors how humans recognize familiarity — through accumulated evidence rather than a single perfect match.

---

## Component Design

### 1. Interfaces

#### FastAPI Server (`api.py`)

Serves two endpoints:

| Method | Path      | Description                                    |
|--------|-----------|------------------------------------------------|
| GET    | `/`       | Health check                                   |
| POST   | `/ingest` | Upload books (EPUB/PDF) and ingest into ChromaDB |
| POST   | `/recall` | Search books by a free-form memory fragment    |

**Middleware:**
- **CORS**: Configured to allow cross-origin requests.
- **X-Process-Time**: Adds request duration header for observability.

**Exception Handling:**
- `HTTPException` → standardized JSON error response.
- `RequestValidationError` → standardized JSON validation error response.

**Response Format** (`lib/responses/standard.py`):
```json
{
  "success": true/false,
  "data": { ... },
  "error": { "code": "...", "message": "..." }
}
```

#### CLI Tool (`readrecall.py`)

A Click-based command-line interface with two actions:
- `--action ingest` — prompts for directory path and file type, then runs ingestion.
- `--action recall` — prompts for a memory fragment, then runs recall.

---

### 2. Data Models

#### Document (`lib/Document.py`)

Represents a single book after loading. Contains:
- `metadata`: Dictionary with `book_id`, `title`, `author`, `publisher`, `description`.
- `sections`: A list of `Section` objects (one per chapter/document item).

#### Section (`lib/Section.py`)

Represents a single chapter or document item within a book. Contains:
- `metadata`: Dictionary with `book_id`, `title`, `author`, `publisher`, `description`, `chapter`.
- `content`: Plain text of the chapter.

#### IngestionType (`lib/IngestionType.py`)

String enum restricting file types to:
- `epub`
- `pdf`

---

### 3. Ingestion Pipeline

The ingestion pipeline transforms raw book files into a searchable vector index.

```
[Book files] → Load → Chunk → Embed → Store in ChromaDB
```

#### Step 1: Load (`ingestion/loaders.py`)

**`load_docs_from_dir(dir, type)`**
- Uses `DirectoryLoader` to batch-load all files in a directory.
- For EPUB files: Uses `EPubLoader` (ebooklib + BeautifulSoup).
- For PDF files: Uses LangChain's `PyPDFLoader`.
- Returns a list of `Document` objects.

**`EPubLoader` (`lib/EPubLoader.py`)**
- Reads EPUB files using `ebooklib`.
- Extracts metadata: `book_id` (UUID4), `title`, `author` (creator), `publisher`, `description`.
- Splits content by `ITEM_DOCUMENT` items (one per chapter/web resource).
- Parses HTML content to plain text with BeautifulSoup.
- Returns a `Document` with chapter-level `Section` objects.

**`DirectoryLoader` (`lib/DirectoryLoader.py`)**
- Iterates over all files in a directory.
- Applies the configured loader class to each file.
- Returns a list of loaded `Document` objects.

#### Step 2: Chunk (`ingestion/chunking.py`)

**`chunk_docs(docs)`**
- Iterates over each `Document` and calls `chunk_doc()`.
- Concatenates all chunks into a single flat list.

**`chunk_doc(doc)`**
- Iterates over each `Section` in the document.
- Uses `LangChain RecursiveCharacterTextSplitter` with:
  - `chunk_size=10000` characters
  - `chunk_overlap=200` characters
  - `add_start_index=True` for traceability
- Annotates each chunk with:
  - `chunk_index`: Position of the chunk within the book.
  - `chunks_in_book`: Total number of chunks for the book.

**Why these parameters?** 10,000-character chunks with 200-character overlap balance semantic coherence with granularity. This is tuned for book-length texts where chapters can span many thousands of words.

#### Step 3: Embed & Store (`ingestion/embedding.py`)

**Embedding Model:** `text-embedding-3-small` (OpenAI), 1536-dimensional vectors.

**`create_vector_store(chunks, persist_dir, collection)`**
- Creates a new ChromaDB collection.
- Embeds all chunks and persists to disk.
- Uses cosine similarity (`hnsw:space: cosine`).

**`persist_chunks(chunks, persist_dir, collection)`**
- Loads an existing vector store.
- Appends new chunks (for incremental ingestion).

**`load_vector_store(persist_dir, collection)`**
- Loads and returns an existing ChromaDB instance from disk.

**Storage:** ChromaDB with local persistence at `db/chroma_db/`. Single collection named `readrecall-book-chunks` containing all chunks from all books.

---

### 4. Recall Pipeline

The recall pipeline transforms a vague memory fragment into ranked book suggestions.

```
[Memory fragment] → Embed → Similarity search → Aggregate by book → Score → Rank → Suggest
```

#### Step 1: Query Embedding & Similarity Search (`retrieval/retrievers.py`)

**`query_db(query, k=5, threshold=0.3)`**
- Loads the vector store.
- Embeds the query using the same embedding model.
- Performs `similarity_search_with_score` for top `k` results.
- Filters results to only include chunks with similarity score >= `threshold` (lower distance = more similar).
- Returns a list of `(Document, similarity_score)` tuples.

**`get_retriever(k=5)`**
- Creates a LangChain retriever with `similarity_score_threshold` search type.
- Returns a configured retriever object (used as an alternative approach).

#### Step 2: Aggregation & Scoring (`retrieval/retrieval_pipeline.py`)

**`get_top_matching_chunks(query, debug_mode)`**
- Queries the vector store for top matching chunks.
- Default `k=10` (configured for MVP, intended to increase to 30–50 for production).

**`group_chunks_by_book(chunks)`**
- Groups `(Document, score)` tuples by `book_id`.
- Returns:
  - `book_hits`: `{book_id: hit_count}` — how many chunks matched per book.
  - `book_info`: `{book_id: metadata}` — first chunk's metadata per book.

**`aggregate_similarity_scores(chunks)`**
- Sums similarity scores for chunks belonging to the same book.
- Returns `{book_id: total_similarity_score}`.

**`calculate_scores(chunks, book_hits)`**
- For each book with hits:
  1. Compute `avg_score = total_similarity / hit_count`
  2. Compute `reinforcement = log(1 + min(hit_count, 5))` — logarithmic bonus for multiple hits, capped at 5.
  3. Compute `final_score = avg_score * reinforcement`
- Returns books sorted descending by `final_score`.

**Scoring Heuristic Explained:**
```
final_score = avg_similarity × log(1 + min(hits, 5))
```
- **Avg similarity** rewards the strength of matches.
- **Logarithmic reinforcement** rewards multiple matches but with diminishing returns. Going from 1→2 hits matters more than going from 10→11.
- **Cap of 5** prevents long books from dominating by chance alone.

#### Step 3: Suggestion Generation

**`get_book_suggestions(chunks)`**
- Runs aggregation and scoring pipeline.
- Returns:
  - `top_match`: Metadata of the highest-scoring book.
  - `other_suggestions`: Metadata of remaining books, ordered by score.

---

### 5. Lib Layer (Shared Utilities)

#### `lib/__init__.py`

Package init that imports `EPubLoader` and `DirectoryLoader` for convenient access (used by `ingestion/loaders.py`).

#### `lib/exceptions/http.py` — HTTP Exception Handler

Catches `HTTPException` and returns standardized JSON:
```json
{ "success": false, "error": { "code": "HTTP_ERROR", "message": "..." } }
```

#### `lib/exceptions/validation.py` — Validation Exception Handler

Catches `RequestValidationError` and returns standardized JSON:
```json
{ "success": false, "error": { "code": "VALIDATION_ERROR", "message": "..." } }
```

#### `lib/middleware/process_time.py` — Process Time Middleware

Measures request processing time and adds an `X-Process-Time` header to all responses for observability.

#### `lib/responses/standard.py` — Standard Response Format

```python
class StandardResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[Any] = None
```

`to_json(resp, status_code)` → Converts to a FastAPI `JSONResponse`.

---

## Data Flow Diagrams

### Ingestion Flow

```
User Upload
    │
    ▼
api.py /ingest
    │
    ▼
Temporary Directory (files saved)
    │
    ▼
ingestion_pipeline.ingest_books()
    │
    ├── 1. loaders.load_docs_from_dir(dir, type)
    │        │
    │        ├── EPUB: lib/EPubLoader (ebooklib + BeautifulSoup)
    │        │        └── Returns Document (metadata + sections)
    │        │
    │        └── PDF: PyPDFLoader
    │                 └── Returns Document (metadata + sections)
    │
    ├── 2. chunking.chunk_docs(docs)
    │        │
    │        └── RecursiveCharacterTextSplitter
    │             chunk_size=10000, chunk_overlap=200
    │             └── Returns list[LCDocument] (annotated with book_id, chunk_index, etc.)
    │
    └── 3. embedding.create_vector_store(chunks)
                 │
                 └── OpenAI text-embedding-3-small → ChromaDB
                      Persist to db/chroma_db/
```

### Recall Flow

```
User Input (vague memory fragment)
    │
    ▼
api.py /recall OR readrecall.py --action recall
    │
    ▼
retrieval_pipeline.get_top_matching_chunks(query, k=10)
    │
    ├── 1. retrievers.query_db(query, k, threshold)
    │        │
    │        ├── Load vector store from disk
    │        ├── Embed query with text-embedding-3-small
    │        ├── similarity_search_with_score → top k chunks
    │        └── Filter: score >= threshold (0.3)
    │
    ├── 2. group_chunks_by_book(chunks)
    │        │
    │        └── {book_id: hit_count}, {book_id: metadata}
    │
    ├── 3. aggregate_similarity_scores(chunks)
    │        │
    │        └── {book_id: total_similarity_score}
    │
    ├── 4. calculate_scores(chunks, book_hits)
    │        │
    │        └── final_score = avg_score × log(1 + min(hits, 5))
    │        └── Sorted {book_id: final_score}
    │
    └── 5. get_book_suggestions(chunks)
             │
             └── { top_match: metadata, other_suggestions: [metadata, ...] }
```

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Single global ChromaDB collection** | Simpler than per-book collections. Metadata filtering can isolate books if needed. |
| **Chunk-level embeddings (not book-level)** | Enables fine-grained similarity matching. Human memory latches onto scenes, not entire books. |
| **Over-retrieval (many weak matches)** | Fuzzy memories rarely map cleanly to one chunk. Multiple weak signals are meaningful. |
| **Book-level aggregation** | One strong match can be coincidence; many moderate matches reflect true recall. |
| **Logarithmic scoring with hit cap** | Rewards multiple matches without letting long books dominate by chance. |
| **Cosine similarity (not L2 or IP)** | Standard for text embeddings; works well with normalized vectors. |
| **10,000-char chunks with 200-char overlap** | Balances semantic coherence with granularity for book-length texts. |
| **OpenAI embeddings (MVP)** | Fast to prototype. Architecture abstracts embedding so providers are swappable. |

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **API Framework** | FastAPI | Async Python web server |
| **CLI Framework** | Click | Command-line interface |
| **Vector Store** | ChromaDB (1.4.0) | Persistent local vector storage |
| **Embeddings** | OpenAI `text-embedding-3-small` | 1536-dim semantic embeddings |
| **PDF Loading** | PyPDFLoader (LangChain) | PDF text extraction |
| **EPUB Loading** | ebooklib + BeautifulSoup | EPUB parsing and HTML→text |
| **Text Splitting** | RecursiveCharacterTextSplitter (LangChain) | Semantic chunking with overlap |
| **Python** | 3.10+ | Runtime |

---

## Project Structure

```
readrecall-backend/
│
├── api.py                          # FastAPI server — /ingest, /recall endpoints
├── readrecall.py                   # CLI tool — Click-based interface
├── requirements.txt                # Python dependencies
├── .gitignore
├── README.md
├── architecture.md                 # This document
│
├── __tests__/
│   └── test_query_results.py       # Tests for retrieval results
│
├── db/
│   └── chroma_db/                  # ChromaDB persistent storage (gitignored)
│
├── ingestion/                      # Book → Chunks pipeline
│   ├── __init__.py
│   ├── ingestion_pipeline.py       # Orchestrator: load → chunk → embed → store
│   ├── loaders.py                  # Document loading (EPUB, PDF)
│   ├── chunking.py                 # Semantic text splitting with overlap
│   └── embedding.py                # Vector embedding and ChromaDB persistence
│
├── retrieval/                      # Query → Suggestions pipeline
│   ├── retrieval_pipeline.py       # Query → aggregate → score → suggest
│   └── retrievers.py               # ChromaDB similarity search
│
├── lib/                            # Shared utilities and models
│   ├── __init__.py
│   ├── Document.py                 # Book document model
│   ├── Section.py                  # Chapter/section model
│   ├── EPubLoader.py               # EPUB file parser
│   ├── DirectoryLoader.py          # Batch directory loader
│   ├── IngestionType.py            # Supported file type enum
│   ├── exceptions/
│   │   ├── http.py                 # HTTP exception handler
│   │   └── validation.py           # Validation error handler
│   ├── middleware/
│   │   └── process_time.py         # Request timing middleware
│   └── responses/
│       └── standard.py             # Standard API response format
│
├── notes/                          # Design notes and strategy documents
│   ├── problem-statement.txt
│   ├── scoring-strategy.txt
│   ├── strategy.txt
│   └── move-to-local-model.txt
│
└── test-docs/                      # Sample book files for testing
```

---

## Known Limitations & Future Work

### Current Limitations (MVP)

1. **`top_k=10` is too small** — With ~140 chunks per book and multiple books on similar themes, many books get only 1 chunk match, making results unstable. Intended to increase to 30–50.

2. **Pure scores lack normalization** — Books with more chunks have more chances to match. Score normalization by `chunks_in_book` is a planned improvement.

3. **No position-based downweighting** — Matches that cluster in one chapter vs. spread across the book are treated equally, but spread indicates broader recall.

4. **No explanation layer** — Users get suggestions but no insight into *why* each book matched, which would build trust.

### Planned Improvements

- Score normalization by `chunks_in_book`
- Position-based downweighting (spread across chapters = stronger signal)
- Book-level embeddings as a first-pass filter
- Explanation generation ("why this book?")
- Local embedding models (moving away from OpenAI API dependency)

---

## MVP Scope (Explicit)

### Included
- Book upload (EPUB, PDF)
- Fuzzy memory input
- Top 3–5 book suggestions with explanations
- CLI and API interfaces

### Excluded
- Conversational agents
- Conversational memory
- Summarization
- Fine-grained Q&A
- Recommendation systems
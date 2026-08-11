# ReadRecall Monorepo

This repository contains both the frontend client and backend service for ReadRecall.

ReadRecall helps users identify books from vague memory fragments by combining semantic retrieval with book-level scoring.

## Repository Layout

```text
ReadRecall/
├── client/
│   └── readrecall/                 # React + Vite frontend
├── backend/                        # FastAPI + CLI backend
│   ├── README.md                   # Backend documentation and API usage
│   ├── api.py
│   ├── readrecall.py
│   ├── requirements.txt
│   ├── ingestion/
│   ├── retrieval/
│   ├── lib/
│   ├── __tests__/
│   └── notes/
└── archive/
    └── server-ai-service-legacy/   # Archived legacy backend copy
```

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn api:app --reload
```

### Frontend

```bash
cd client/readrecall
npm install
npm run dev
```

For full backend details (architecture, endpoints, and CLI usage), see `backend/README.md`.

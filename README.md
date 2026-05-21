# Enterprise RAG Chatbot

A Python chatbot that answers questions using an internal document knowledge base (RAG) or live Google search, exposed through a FastAPI backend and a Streamlit chat UI.

## Features

- **RAG over PDF corpus** — Retrieves relevant chunks from an enterprise knowledge base stored in ChromaDB (AI, RAG, vector DBs, cloud, cybersecurity).
- **Google Search** — Fetches current web results via SerpAPI when questions need up-to-date public information.
- **Intelligent tool routing** — A LangChain agent (Groq `llama-3.3-70b-versatile`) picks `rag_retriever` or `google_search` based on each user message.
- **REST API** — FastAPI `POST /chat` endpoint for programmatic access.
- **Streamlit UI** — Simple chat interface that calls the FastAPI backend.

## Architecture

```
┌─────────────────┐     HTTP POST      ┌──────────────────┐
│  streamlit_app  │ ─────────────────► │  FastAPI (main)  │
│   (port 8501)   │   /chat            │   (port 8001)    │
└─────────────────┘                    └────────┬─────────┘
                                              │
                                              ▼
                                     ┌──────────────────┐
                                     │  LangChain Agent │
                                     │  (Groq LLM)      │
                                     └────────┬─────────┘
                          ┌──────────────────┼──────────────────┐
                          ▼                  ▼                  ▼
                   rag_retriever      google_search         (no tool)
                   ChromaDB +         SerpAPI               greetings
                   embeddings
```

## Project structure

```
chatbot/
├── app/
│   ├── main.py                 # FastAPI app
│   ├── agents/
│   │   └── main_agent.py       # Tool-calling agent + routing prompt
│   ├── rag/
│   │   ├── paths.py            # Project-relative data/chroma paths
│   │   ├── vectordb.py         # Chroma vector store
│   │   ├── retriever.py        # Document retriever
│   │   └── ingest.py           # PDF ingestion script
│   └── tools/
│       ├── rag_tool.py         # Internal knowledge retrieval
│       └── google_search_tool.py
├── data/
│   └── rag_enriched_corpus.pdf # Source document for RAG
├── chromadb/                   # Persisted vector index (created after ingest)
├── streamlit_app.py            # Chat UI
├── requirements.txt
├── .env                        # API keys (do not commit)
└── README.md
```

## Prerequisites

- Python 3.10+ (tested with 3.14)
- [Groq API key](https://console.groq.com/)
- [SerpAPI key](https://serpapi.com/) (for Google search)
- PDF placed at `data/rag_enriched_corpus.pdf` (or update paths in `ingest.py` / `vectordb.py`)

## Setup

### 1. Clone and create a virtual environment

```powershell
cd path\to\chatbot
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On Windows PowerShell you must use `.\Activate.ps1`, not `Activate.ps1`.

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
SERPAPI_API_KEY=your_serpapi_key_here
```

Never commit `.env` or share API keys publicly.

### 4. Ingest documents into ChromaDB

Run once (or again after updating the PDF):

```powershell
python -m app.rag.ingest
```

This chunks `data/rag_enriched_corpus.pdf` and stores embeddings in the `chromadb/` directory.

## Running the application

Use **two terminals**, both with the venv activated and working directory set to the project root.

### Terminal 1 — FastAPI backend

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

- API docs: http://127.0.0.1:8001/docs
- Health: server logs show `Uvicorn running on http://127.0.0.1:8001`

> **Note:** Run uvicorn from the **project root**, not `app/main.py` directly. Running the file as a script causes `ModuleNotFoundError: No module named 'app'`.
>
> If port `8000` fails with `WinError 10013`, use another port (e.g. `8001`).

### Terminal 2 — Streamlit UI

```powershell
streamlit run streamlit_app.py
```

Opens http://localhost:8501 by default. The UI calls `http://127.0.0.1:8001/chat` unless overridden:

```powershell
$env:CHATBOT_API_URL = "http://127.0.0.1:8001/chat"
streamlit run streamlit_app.py
```

## API reference

### `POST /chat`

**Request body:**

```json
{
  "query": "give key points from the knowledge base"
}
```

**Response:**

```json
{
  "response": "The key points from the knowledge base are: ..."
}
```

**Example (curl):**

```bash
curl -X POST "http://127.0.0.1:8001/chat" \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"What is RAG?\"}"
```

## Tool routing

The agent selects a tool from the user message:

| Tool | Use when |
|------|----------|
| `rag_retriever` | Questions about the internal corpus, knowledge base, uploaded documents, or topics in the PDF (AI, RAG, vector DBs, cloud, security). |
| `google_search` | Current events, news, weather, live web data, or general facts not in the corpus. |
| *(none)* | Simple greetings or casual chat. |

Example prompts:

- RAG: *"Summarize key points from our knowledge base"*
- Web: *"Latest news about OpenAI today"*

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `No module named 'app'` | Start the server from the project root with `uvicorn app.main:app`, not `python app/main.py`. |
| `WinError 10013` on port 8000 | Use `--port 8001` (or another free port). |
| `500` on `/chat` with tool errors | Restart uvicorn after code changes. Ensure tool names have no spaces (e.g. `rag_retriever`). |
| Streamlit cannot connect | Confirm FastAPI is running on the port set in `CHATBOT_API_URL`. |
| Empty RAG results | Run `python -m app.rag.ingest` and confirm `chromadb/` exists. |
| Google search fails | Verify `SERPAPI_API_KEY` in `.env`. |

## Tech stack

- **LLM:** Groq (`llama-3.3-70b-versatile`) via `langchain-groq`
- **Agent:** LangChain tool-calling agent (`langchain-classic`)
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` (HuggingFace)
- **Vector store:** ChromaDB (`langchain-chroma`)
- **API:** FastAPI + Uvicorn
- **UI:** Streamlit
- **Web search:** SerpAPI

## License

Private / personal project — add a license if you plan to distribute this repo.

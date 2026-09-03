# DocWise — RAG-Powered Document Assistant

A complete **Core Track** Retrieval-Augmented Generation application: raw PDF/TXT documents → cleaning/chunking → local embeddings → persistent Chroma vector store → semantic retrieval → local Ollama LLM → FastAPI → Streamlit chat UI with source citations.

## Architecture

```text
PDF/TXT corpus
    ↓
Jupyter ingestion + cleaning + 900-char chunks / 150 overlap
    ↓
SentenceTransformers all-MiniLM-L6-v2
    ↓
Persistent Chroma vector store
    ↓
Top-K semantic retrieval
    ↓
Strict grounded prompt + Ollama llama3.2:3b
    ↓
FastAPI /query
    ↓
Streamlit chat UI + cited sources
```

## Tech Stack
Python 3.10+, Jupyter, PyPDF, SentenceTransformers, ChromaDB, Ollama, FastAPI, Pydantic, Streamlit, pytest.

## Project Structure
```text
rag_assistant_project/
├── notebooks/rag_pipeline.ipynb
├── data/documents/
├── backend/
│   ├── app/main.py
│   ├── app/api/routes/query.py
│   ├── app/core/config.py
│   ├── app/schemas/query.py
│   ├── app/services/{retrieval.py,generation.py}
│   ├── data/vector_store/
│   ├── tests/test_query.py
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── frontend/{app.py,api_client.py,requirements.txt,.env.example}
└── README.md
```

## Domain & Data
The project is intentionally domain-flexible. Add your own open, text-extractable PDF/TXT documents to `data/documents/`. The notebook reports parsing failures and flags pages with no extractable text as likely OCR candidates. This submission is the **Core Track**, so YOLO is not required.

## Setup
1. Install Python 3.10+, Git and Ollama.
2. From the project root create and activate a virtual environment.
3. Install notebook dependencies:
   ```bash
   pip install jupyter pandas numpy chromadb sentence-transformers pypdf ollama python-dotenv
   ```
4. Pull the local LLM:
   ```bash
   ollama pull llama3.2:3b
   ```
5. Put documents in `data/documents/`.
6. Open `notebooks/rag_pipeline.ipynb` and use **Kernel → Restart & Run All**. Review and replace the 10 evaluation questions with domain-specific questions, then manually mark relevance/grounding/correctness.

## Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux
uvicorn app.main:app --reload
```
Open Swagger at `http://localhost:8000/docs`.

### Environment Variables
| Variable | Example | Purpose |
|---|---|---|
| `OLLAMA_MODEL` | `llama3.2:3b` | Local generation model |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Local embedding model |
| `VECTOR_STORE_PATH` | `data/vector_store` | Persisted Chroma directory |
| `TOP_K` | `4` | Retrieved chunks |
| `FRONTEND_ORIGIN` | `http://localhost:8501` | CORS origin |

### API Reference
`GET /health` returns service status and indexed chunk count.

`POST /query` request:
```json
{"question":"What does the document say about ...?"}
```
Response:
```json
{"answer":"Grounded answer [Source 1]","sources":["manual.pdf (page 3, chunk 1)"]}
```
Curl:
```bash
curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"question":"What is the main topic?"}'
```

### Tests
```bash
cd backend
pytest -q
```
Includes a happy-path API test and invalid-input `422` test.

## Frontend
In a second terminal:
```bash
cd frontend
python -m venv .venv
# activate it, then:
pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux
streamlit run app.py
```
The frontend reads `API_BASE_URL` from the environment, shows a loading state, catches API errors, and displays answer sources.

## Evaluation Results
The notebook contains a 10-question evaluation table with columns for question, retrieved source, answer, retrieval relevance, groundedness, and correctness. Because the final values depend on the student's chosen corpus, the table is generated after documents are added and requires manual review. Do **not** submit placeholder questions: replace them with real domain questions and record observed failure cases.

## Screenshots
Before submission, add screenshots of: (1) the Streamlit chat showing a cited answer, (2) Swagger `/query`, and (3) the notebook evaluation table.

## GitHub
Create `.gitignore` before committing, then:
```bash
git init
git add .
git commit -m "RAG assistant: notebook, FastAPI backend, frontend"
git branch -M main
git remote add origin https://github.com/<your-username>/rag-assistant-app.git
git push -u origin main
```

## Demo Checklist
Start Ollama → run backend on port 8000 → run Streamlit → ask a question whose answer is in the corpus → confirm the answer cites sources → ask an out-of-scope question and confirm the assistant refuses to invent an answer.

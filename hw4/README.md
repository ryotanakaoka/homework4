# Campus Customs — Homework 4

Campus Customs is a React/Vite storefront with a unified FastAPI and PydanticAI backend. It supports catalogue browsing, product details and inventory, account creation, login, customer chat, logged-in chat history, and an audit trail.

## Submission structure

The project is organized as follows:

```text
Homework 4/
├── backend/                 # FastAPI/PydanticAI application
├── backend/prompts/         # Agent system prompt
├── frontend/                # React/Vite application
├── data/                    # Local runtime data; database/images are ignored
├── output/                  # Reports, screenshots, harness, and audit trail
├── AI_prompts.md
├── .env.example
├── .gitignore
└── requirements.txt
```

## Local-only files

`.env`, `data/campus_customs.db`, `data/products/`, `frontend/node_modules/`, and Python `__pycache__/` directories are excluded by `.gitignore`. Do not commit API keys, the SQLite database, product images, installed dependencies, or generated frontend output. Obtain the supplied database and product-image files separately and place them under `data/` before running the application.

## Setup

From this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set the real `PORTKEY_API_KEY` in `.env`. Keep `.env` local.

Install frontend dependencies:

```bash
cd frontend
npm install
```

## Run

Start the unified backend from `backend/`:

```bash
cd backend
uvicorn main:app --reload --port 8000
```

In a second terminal, start the frontend from `frontend/`:

```bash
cd frontend
npm run dev
```

Open the Vite URL, normally `http://localhost:5173`. The backend health check is `http://localhost:8000/health`. The frontend uses the unified backend for products, authentication, chat, and chat history.

## Verification

```bash
cd frontend
npx tsc --noEmit
```

The backend uses `data/campus_customs.db` in read-only mode for catalogue/inventory lookups and writes only the intended account and logged-in chat-history records. Agent activity is summarized in `output/audit_trail.json`; existing audit entries should be preserved when new tests are run.

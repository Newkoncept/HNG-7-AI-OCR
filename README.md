# HNG-7 Siftline

AI-powered document upload, text extraction, and analysis service built with FastAPI, SQLAlchemy/SQLModel, and PostgreSQL.

## Features
- Upload PDF files and store them in S3-compatible storage.
- Extract text from PDFs using `pdf2image` + `pytesseract`.
- Run LLM-based analyses and store summaries or structured data.
- Query combined document metadata, extracted text, and analyses.
- Alembic for database schema migrations.

## Tech Stack
- Python 3.11, FastAPI, SQLModel, SQLAlchemy
- PostgreSQL
- S3-compatible storage (AWS/Railway)
- pdf2image, pytesseract, pillow, pypdf
- Uvicorn for serving
- Alembic migrations

## Project Structure
```
app/
 ├── main.py
 ├── routes/
 │     └── document_route.py
 ├── models/
 │     ├── upload_model.py
 │     └── analysis_model.py
 ├── clients/
 │     ├── llm_client.py
 │     └── client.py
 ├── utils/
 │     └── extractor.py
 ├── db.py
alembic/
```

## Environment Variables
Create a `.env` file with:
```
DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/dbname
AWS_ENDPOINT_URL=...
AWS_S3_BUCKET_NAME=...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_DEFAULT_REGION=...
```

## Setup (Local)
```
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Database & Migrations
```
alembic revision --autogenerate -m "init tables"
alembic upgrade head
```

## Run the API
```
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Docker
```
docker build -t hng-siftline .
docker run -p 8000:8000 --env-file .env hng-siftline
```

## Key Endpoints
- POST /documents/upload — upload PDF and extract text
- POST /documents/{upload_id}/analyze — run LLM analysis
- GET /documents/{upload_id} — retrieve metadata + text + analyses

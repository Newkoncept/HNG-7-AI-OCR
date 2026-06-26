# HNG-7 Siftline API

A FastAPI-based document analysis API built during the HNG Backend Internship Stage 7.

This project allows users to upload PDF documents, extract text, store files in S3-compatible storage, run LLM-powered document analysis, and retrieve document metadata, extracted text, and analysis results through API endpoints.

It demonstrates backend work with file uploads, PDF processing, OCR fallback, database persistence, external API integration, and structured API responses.

---

## Overview

Siftline is a document processing backend API designed to handle:

* PDF file uploads
* PDF text extraction
* OCR fallback for scanned documents
* S3-compatible file storage
* LLM-based document analysis
* Document summary generation
* Document type classification
* Structured attribute extraction
* Database-backed document and analysis records

---

## Core Features

* Upload PDF documents through a FastAPI endpoint
* Validate uploaded files by content type and file size
* Extract text directly from readable PDFs
* Use OCR fallback for scanned/image-based PDFs
* Store uploaded PDF files in S3-compatible storage
* Save document metadata and extracted text in PostgreSQL
* Analyze extracted document text with an LLM through OpenRouter
* Store document summaries, document type, and extracted attributes
* Retrieve document metadata, extracted text, and previous analyses
* Alembic-based database migration support
* Docker support for containerized deployment

---

## Tech Stack

| Area                  | Technology             |
| --------------------- | ---------------------- |
| Backend Framework     | FastAPI                |
| Language              | Python 3.11            |
| Database              | PostgreSQL             |
| ORM                   | SQLAlchemy / SQLModel  |
| Migrations            | Alembic                |
| File Storage          | S3-compatible storage  |
| PDF Text Extraction   | pypdf                  |
| OCR Processing        | pdf2image, pytesseract |
| Image Processing      | Pillow                 |
| LLM Integration       | OpenRouter API         |
| HTTP Client           | HTTPX                  |
| Server                | Uvicorn                |
| Containerization      | Docker                 |
| Dependency Management | uv, pyproject.toml     |

---

## Project Structure

```txt
HNG-7-AI-OCR/
├── alembic/                  # Database migrations
├── app/
│   ├── clients/              # S3 and LLM API clients
│   │   ├── client.py
│   │   └── llm_client.py
│   ├── models/               # Upload and analysis database models
│   │   ├── upload_model.py
│   │   └── analysis_model.py
│   ├── routes/               # API route handlers
│   │   └── document_route.py
│   ├── utils/                # PDF text extraction and OCR utilities
│   │   └── extractor.py
│   ├── db.py                 # Database configuration
│   └── main.py               # FastAPI application entry point
├── dockerfile
├── pyproject.toml
├── uv.lock
├── alembic.ini
├── .env.example
└── README.md
```

---

## API Routes

### Default

| Method | Endpoint  | Description              |
| ------ | --------- | ------------------------ |
| `GET`  | `/`       | API information endpoint |
| `GET`  | `/health` | Health check endpoint    |

### Documents

| Method | Endpoint                         | Description                                                      |
| ------ | -------------------------------- | ---------------------------------------------------------------- |
| `POST` | `/documents/upload`              | Upload a PDF, extract text, store the file, and save metadata    |
| `POST` | `/documents/{upload_id}/analyze` | Analyze extracted document text with an LLM                      |
| `GET`  | `/documents/{doc_id}`            | Retrieve document metadata, extracted text, and analysis history |

---

## Document Upload Flow

1. A user uploads a PDF file.
2. The API validates that the file is a PDF.
3. The API checks the file size limit.
4. The PDF file is read into memory.
5. Text extraction is attempted using standard PDF text extraction.
6. If normal extraction fails, OCR is used as a fallback.
7. The original PDF is uploaded to S3-compatible storage.
8. Document metadata and extracted text are saved in PostgreSQL.
9. The API returns the document ID and upload details.

---

## Document Analysis Flow

1. A document is uploaded and stored.
2. The extracted text is retrieved from the database.
3. The text is sent to an LLM through OpenRouter.
4. The LLM returns structured JSON containing:

   * Summary
   * Document type
   * Extracted attributes
5. The analysis result is saved in the database.
6. The API returns the analysis record details.

---

## Text Extraction Strategy

The project uses two extraction paths:

1. **Standard PDF extraction**
   Attempts to extract text directly from readable PDF pages.

2. **OCR fallback**
   If direct extraction does not return usable text, the PDF is converted into images and processed with Tesseract OCR.

This allows the API to handle both text-based PDFs and scanned/image-based PDFs.

---

## Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/siftline

AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_DEFAULT_REGION=your_aws_region
AWS_ENDPOINT_URL=your_s3_compatible_endpoint
AWS_S3_BUCKET_NAME=your_bucket_name

OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=gpt-4o-mini
```

Do not commit real API keys, storage credentials, database URLs, or environment secrets.

---

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/Newkoncept/HNG-7-AI-OCR.git
cd HNG-7-AI-OCR
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies with uv

```bash
pip install uv
uv sync
```

Alternative:

```bash
uv pip install .
```

### 4. Configure environment variables

Create a `.env` file using the environment variable guide above.

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the development server

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API should be available at:

```txt
http://127.0.0.1:8000
```

Swagger documentation should be available at:

```txt
http://127.0.0.1:8000/docs
```

---

## Docker

Build the Docker image:

```bash
docker build -t hng-siftline .
```

Run the container:

```bash
docker run -p 8000:8000 --env-file .env hng-siftline
```

---

## Example Workflow

1. Upload a PDF document:

```http
POST /documents/upload
```

2. Run LLM analysis on the uploaded document:

```http
POST /documents/{upload_id}/analyze
```

3. Retrieve the document with metadata, extracted text, and analysis history:

```http
GET /documents/{doc_id}
```

---

## Security & Reliability Notes

This project includes:

* File type validation for PDF uploads
* File size validation
* Environment-based secret management
* Database-backed document and analysis records
* Server-side LLM request handling
* S3-compatible object storage
* Dockerized runtime support

---

## Current Status

This project was built as part of the HNG Backend Internship Stage 7 document processing task.

It demonstrates practical backend patterns around file upload handling, PDF text extraction, OCR fallback, external API integration, database persistence, and structured API responses.

Planned improvements include:

* Better error response consistency
* Automated tests
* Postman collection
* API screenshots
* Deployment guide
* Authentication and user-owned document access
* Background task processing for long document analysis
* Better handling for very large PDFs
* Improved OCR performance and cleanup
* Cleaner response schemas

---

## Author

Built by [Oluwagbemiga Taiwo](https://github.com/Newkoncept)

LinkedIn: https://www.linkedin.com/in/hermmanuel

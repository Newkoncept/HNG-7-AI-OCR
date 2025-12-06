# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps for pdf2image/pytesseract (poppler + tesseract + X libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    tesseract-ocr \
    libtesseract-dev \
    libglib2.0-0 libsm6 libxext6 libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps (mirrors pyproject.toml)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
        boto3 \
        fastapi \
        pdf2image \
        pillow \
        pypdf \
        pytesseract \
        python-dotenv \
        python-multipart \
        sqlmodel \
        uvicorn[standard]

# Copy code
COPY . .

# Run the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

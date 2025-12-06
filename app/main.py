from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv() 
from app.routes import document_route as document

app = FastAPI(title="AI Document Summarization Service")

app.include_router(document.router)


@app.get("/", tags=["Info"])
def root():
    return {
        "app_name": "HNG-7 Siftline",
        "description": "Upload PDFs, extract text, run LLM analysis, and fetch results.",
        "version": "1.0.0",
        "api_base": "/documents",
        "docs": "/docs",
        "health": "/health",
    }

@app.get("/health", tags=["Info"])
def health():
    return {"status": "ok"}

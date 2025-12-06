from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv() 
from app.routes import document_route as document
from app.db import engine, get_session

app = FastAPI(title="AI Document Summarization Service")

app.include_router(document.router)


# Root endpoint for basic info
@app.get("/", tags=["Info"])
def root():
    return {
        "app_name": "HNG-7 SIFTLINE",
        "description": "AI-powered website health auditor for non-technical users.",
        "version": "1.0.0",
        "docs_url": "/docs",
        "api_base": "/api",
    }
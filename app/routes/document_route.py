import os
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from sqlmodel import Session, select
from dotenv import load_dotenv

# from app.schemas.document_schema import DocumentResponse, AnalyzeResponse
from app.db import get_session
from app.clients.client import upload_bytes_to_s3
from app.utils.extractor import extract_text_from_pdf
from app.models.upload_model import Upload
from app.models.analysis_model import Analysis
from app.clients.llm_client import analyze_document_text


load_dotenv()

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload")
async def upload_document(
        file: UploadFile = File(...),
        session: Session = Depends(get_session),
    ):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Only PDF files allowed"
        )

    if file.size > 5242880:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="The file is greater than 5 MB."
        )
    

    pdf_bytes = await file.read()
    if not pdf_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Uploaded PDF is empty"
        )

    
    content = extract_text_from_pdf(pdf_bytes)

    s3_key = f"documents/{uuid4()}{file.filename}"

    upload_bytes_to_s3(
        key=s3_key,
        data=pdf_bytes,
        content_type=file.content_type,
    )

    new_upload = Upload(
        s3_key=s3_key,
        original_filename=file.filename,
        content_type=file.content_type,
        size_bytes=len(pdf_bytes),
        extracted_text=content,
        extra_metadata=None,
    )
    session.add(new_upload)
    session.commit()
    session.refresh(new_upload)

    return {
        "status_code": status.HTTP_201_CREATED,
        "message": "Upload successfully done",
        "data": {
            "id": new_upload.id,
            "s3_key": new_upload.s3_key,
            "original_filename": new_upload.original_filename,
            "content_type": new_upload.content_type,
            "size_bytes": new_upload.size_bytes,
            "created_at": new_upload.created_at,
        }   
    }


@router.post("/{upload_id}/analyze")
async def analyze_document(upload_id: str, session: Session = Depends(get_session)):
    stmt = select(Upload.extracted_text).where(Upload.id == upload_id)
    db_result = session.exec(stmt).first()
    if db_result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Upload not found"
        )
    

    try:
        result = await analyze_document_text(db_result)
    
        new_analysis = Analysis(
        document_id=upload_id,
        model_name=os.getenv("OPENROUTER_MODEL"),
        summary=result["summary"],
        doc_type=result["doc_type"],
        attributes=result.get("attributes"))
        
        session.add(new_analysis)
        session.commit()
        session.refresh(new_analysis)

        return {
            "status_code": status.HTTP_201_CREATED,
            "message": "Upload successfully done",
            "data": {
                "id": new_analysis.id,
                "document_id": new_analysis.document_id,
                "model_name": new_analysis.model_name,
                "doc_type": new_analysis.doc_type,
                "created_at": new_analysis.created_at,
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"LLM analysis failed: {e}"
        )



@router.get("/{doc_id}")
async def get_document(doc_id: str, session: Session = Depends(get_session)):
    upload = session.get(Upload, doc_id)
    if not upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail= "Document not found"
        )

    analyses = session.exec(
        select(Analysis).where(Analysis.document_id == upload.id).
        order_by(Analysis.created_at.desc())
    ).all()

    return {
        "id": upload.id,
        "s3_key": upload.s3_key,
        "original_filename": upload.original_filename,
        "content_type": upload.content_type,
        "size_bytes": upload.size_bytes,
        "extracted_text": upload.extracted_text,
        "metadata": upload.extra_metadata,
        "created_at": upload.created_at,
        "updated_at": upload.updated_at,
        "analyses": [
            {
                "id": a.id,
                "model_name": a.model_name,
                "summary": a.summary,
                "doc_type": a.doc_type,
                "attributes": a.attributes,
                "created_at": a.created_at,
            }
            for a in analyses
        ],
    }

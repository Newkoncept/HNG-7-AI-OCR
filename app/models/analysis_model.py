from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
import uuid

from app.models.upload_model import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(
        String(50),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
        index=True
    )
    document_id = Column(
        String(50),
        ForeignKey("uploads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    model_name = Column(String(100), nullable=False)  # e.g., gpt-4o-mini
    summary = Column(Text, nullable=False)            # LLM summary text
    doc_type = Column(String(50), nullable=False)     # invoice, cv, report, etc.
    attributes = Column(JSONB, nullable=True)         # structured fields from LLM

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # document = relationship("Document", back_populates="analyses")

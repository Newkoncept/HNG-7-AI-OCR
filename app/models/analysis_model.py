import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

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
    model_name = Column(String(100), nullable=False)  
    summary = Column(Text, nullable=False)            
    doc_type = Column(String(50), nullable=False)     
    attributes = Column(JSONB, nullable=True)         

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # document = relationship("Document", back_populates="analyses")

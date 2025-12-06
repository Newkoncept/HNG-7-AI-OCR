
# # Pydantic models for request/response bodies
# class DocumentBase(BaseModel):
#     s3_key: str
#     original_filename: str
#     content_type: str
#     size_bytes: int = Field(ge=0)
#     extracted_text: str
#     metadata: Optional[Dict[str, Any]] = None


# class DocumentCreate(DocumentBase):
#     pass


# class DocumentRead(DocumentBase):
#     id: int
#     created_at: datetime
#     updated_at: datetime

#     class Config:
#         orm_mode = True





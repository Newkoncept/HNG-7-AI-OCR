# # Pydantic schemas
# class AnalysisBase(BaseModel):
#     document_id: int
#     model_name: str
#     summary: str
#     doc_type: str
#     attributes: Optional[Dict[str, Any]] = None


# class AnalysisCreate(AnalysisBase):
#     pass


# class AnalysisRead(AnalysisBase):
#     id: int
#     created_at: datetime

#     class Config:
#         orm_mode = True
# In app/schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional

# A reusable model for any field that includes a value and a confidence score
class FieldWithConfidence(BaseModel):
    value: Optional[str] = Field(None, description="The extracted value of the field.")
    confidence: float = Field(..., ge=0, le=1, description="The confidence score (0-1) for the extraction.")

# Model for individual subject marks
class SubjectMark(BaseModel):
    subject: FieldWithConfidence
    max_marks: Optional[FieldWithConfidence] = None
    obtained_marks: FieldWithConfidence
    grade: Optional[FieldWithConfidence] = None

# Main model for the candidate's details
class CandidateDetails(BaseModel):
    name: Optional[FieldWithConfidence] = None
    fathers_name: Optional[FieldWithConfidence] = None
    roll_no: Optional[FieldWithConfidence] = None
    registration_no: Optional[FieldWithConfidence] = None
    date_of_birth: Optional[FieldWithConfidence] = None
    exam_year: Optional[FieldWithConfidence] = None
    board_university: Optional[FieldWithConfidence] = None
    institution: Optional[FieldWithConfidence] = None

# The final, top-level response model for the API output
class ExtractionResponse(BaseModel):
    candidate_details: CandidateDetails
    marks: List[SubjectMark]
    overall_result: Optional[FieldWithConfidence] = None
    issue_date: Optional[FieldWithConfidence] = None
    issue_place: Optional[FieldWithConfidence] = None
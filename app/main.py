# In app/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from . import processing, schemas
import uvicorn

app = FastAPI(
    title="AI-Based Marksheet Extraction API",
    description="An API that takes a marksheet image or PDF and returns extracted fields in JSON format."
)

@app.get("/", tags=["General"])
def read_root():
    return {"message": "Welcome to the Marksheet Extraction API. Go to /docs for the API documentation."}

@app.post("/extract/", response_model=schemas.ExtractionResponse, tags=["Extraction"])
async def extract_marksheet_data(file: UploadFile = File(...)):
    """
    Takes a marksheet file (JPG, PNG, PDF) as input and returns a JSON output
    containing extracted fields along with confidence scores.
    """
    # Requirement: Check file size, max 10 MB 
    if file.size > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds the 10MB limit."
        )

    # Requirement: Check file format 
    if file.content_type not in ["image/jpeg", "image/png", "application/pdf"]:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file format. Please upload a JPG, PNG, or PDF file."
        )

    try:
        contents = await file.read()
        # This is where we will call our core logic. We will implement process_document next.
        extracted_data = processing.process_document(contents, file.content_type)
        return extracted_data
    except Exception as e:
        # General error handling
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
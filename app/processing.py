# In app/processing.py
import os
import json
import io
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
from dotenv import load_dotenv
import google.generativeai as genai
from . import schemas # We will use our Pydantic schemas for validation

# Load environment variables from .env file
load_dotenv()

# Configure the Google Gemini API
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    model = None

def get_prompt(ocr_text: str) -> str:
    """Generates the detailed prompt for the LLM."""
    # This prompt is engineered to guide the LLM in extracting and structuring the data
    # according to the required JSON schema  and fields.
    return f"""
    You are an expert AI system for extracting information from academic marksheets.
    Your task is to analyze the provided OCR text and convert it into a structured JSON object.

    **Instructions:**
    1.  Carefully parse the OCR text. It may contain errors or formatting issues.
    2.  Extract the information for all fields defined in the JSON schema below.
    3.  For each field, provide a `value` and a `confidence` score (from 0.0 to 1.0).
    4.  The confidence score should reflect your certainty. 1.0 means absolute certainty, 0.0 means no information found.
    5.  If a field's value is not found in the text, its `value` must be `null` and its `confidence` must be `0.0`.
    6.  The final output MUST be a single, valid JSON object and nothing else. Do not add any extra text, explanations, or markdown formatting like ```json.

    **OCR Text to Analyze:**
    ---
    {ocr_text}
    ---

    **Required JSON Output Schema:**
    {{
      "candidate_details": {{
        "name": {{"value": "string | null", "confidence": "float"}},
        "fathers_name": {{"value": "string | null", "confidence": "float"}},
        "roll_no": {{"value": "string | null", "confidence": "float"}},
        "registration_no": {{"value": "string | null", "confidence": "float"}},
        "date_of_birth": {{"value": "DD/MM/YYYY | null", "confidence": "float"}},
        "exam_year": {{"value": "string | null", "confidence": "float"}},
        "board_university": {{"value": "string | null", "confidence": "float"}},
        "institution": {{"value": "string | null", "confidence": "float"}}
      }},
      "marks": [
        {{
          "subject": {{"value": "string", "confidence": "float"}},
          "max_marks": {{"value": "string | null", "confidence": "float"}},
          "obtained_marks": {{"value": "string", "confidence": "float"}},
          "grade": {{"value": "string | null", "confidence": "float"}}
        }}
      ],
      "overall_result": {{"value": "PASS/FAIL/DIVISION | null", "confidence": "float"}},
      "issue_date": {{"value": "DD/MM/YYYY | null", "confidence": "float"}},
      "issue_place": {{"value": "string | null", "confidence": "float"}}
    }}
    """

def extract_text_from_document(contents: bytes, content_type: str) -> str:
    """Extracts text from different document types."""
    if content_type in ["image/jpeg", "image/png"]:
        image = Image.open(io.BytesIO(contents))
        return pytesseract.image_to_string(image)
    elif content_type == "application/pdf":
        text = ""
        with fitz.open(stream=contents, filetype="pdf") as pdf_doc:
            for page in pdf_doc:
                text += page.get_text()
        return text
    else:
        raise ValueError("Unsupported content type for text extraction")

def process_document(contents: bytes, content_type: str) -> schemas.ExtractionResponse:
    """The main processing pipeline for a document."""
    if model is None:
        raise ConnectionError("LLM model is not configured. Check API key.")

    # 1. Extract raw text via OCR
    ocr_text = extract_text_from_document(contents, content_type)
    if not ocr_text.strip():
        raise ValueError("Could not extract any text from the document.")

    # 2. Generate the prompt and get structured data from LLM
    prompt = get_prompt(ocr_text)
    try:
        response = model.generate_content(prompt)
        # Clean the response to get a valid JSON string
        json_string = response.text.strip().lstrip("```json").rstrip("```").strip()
        json_data = json.loads(json_string)
    except Exception as e:
        raise ValueError(f"Failed to get a valid JSON response from the LLM: {e}")

    # 3. Validate the data against our Pydantic schema
    try:
        validated_data = schemas.ExtractionResponse(**json_data)
        return validated_data
    except Exception as e:
        raise ValueError(f"LLM output failed Pydantic validation: {e}")
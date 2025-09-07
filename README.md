# AI-Based Marksheet Extraction API

An API that takes a marksheet (image or PDF) as input and returns a structured JSON output containing extracted fields along with confidence scores, as per the AI Engineer Intern assignment.

## Features

- [cite_start]Extracts data from **JPG, PNG, and PDF** files[cite: 6].
- [cite_start]Powered by **Google's Gemini LLM** for high-accuracy structured data extraction[cite: 24, 29].
- [cite_start]Built with **Python and FastAPI**, ensuring high performance and concurrency[cite: 23].
- [cite_start]Provides **confidence scores** for each extracted field[cite: 14].
- [cite_start]Includes robust **error handling** for invalid file types and oversized files[cite: 34].

## Tech Stack

- [cite_start]**Backend**: Python, FastAPI [cite: 23]
- **OCR**: Tesseract, PyMuPDF
- [cite_start]**AI/LLM**: Google Gemini [cite: 24]
- **Schema Validation**: Pydantic

## API Usage

### Running Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Rcbash/marksheet-extractor.git
    cd marksheet-extractor
    ```
2.  **Create a virtual environment and install dependencies:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3.  **Set up your environment variables:**
    Create a `.env` file in the root directory and add your API key. [cite_start]This is required to keep secrets out of the repository[cite: 35].
    ```
    GOOGLE_API_KEY="your_gemini_api_key"
    ```
4.  **Run the server:**
    ```bash
    uvicorn app.main:app --reload
    ```
5.  Access the interactive API documentation (Fast API Docs) at `http://127.0.0.1:8000/docs`.

### API Endpoint: `/extract/`

-   **Method**: `POST`
-   **Body**: `multipart/form-data`
-   **Parameter**: `file` (The marksheet file to be uploaded)

#### Sample JSON Response
```json
{
  "candidate_details": {
    "name": {"value": "John Doe", "confidence": 0.95},
    "fathers_name": {"value": "Richard Doe", "confidence": 0.95},
    "roll_no": {"value": "123456", "confidence": 1.0}
  },
  "marks": [
    {
      "subject": {"value": "PHYSICS", "confidence": 1.0},
      "max_marks": {"value": "100", "confidence": 0.9},
      "obtained_marks": {"value": "85", "confidence": 1.0},
      "grade": {"value": "A", "confidence": 0.9}
    }
  ],
  "overall_result": {"value": "PASS", "confidence": 0.98},
  "issue_date": null,
  "issue_place": null
}


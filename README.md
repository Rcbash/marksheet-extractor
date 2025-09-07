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

#### **Step 2: Write the Approach Note (`APPROACH.md`)**

This is a mandatory 1-2 page document explaining your design choices[cite: 59].

1.  In the VS Code explorer, create a new file named `APPROACH.md`.
2.  Paste the template below into this new file.
3.  **Important**: Read through this and make sure it accurately reflects your understanding. You should rephrase parts of it in your own words to demonstrate your personal thought process.

```markdown
# Approach and Design Choices

This document outlines the technical approach, design choices, and logic behind the AI Marksheet Extraction API, as required for the assignment submission[cite: 59].

### 1. Overall Architecture

I chose a two-step hybrid architecture for this task to ensure both accuracy and efficiency:

1.  **Optical Character Recognition (OCR):** First, a specialized OCR engine (`Tesseract` for images, `PyMuPDF` for text-based PDFs) extracts the raw text from the document. This separation of concerns ensures we get the best possible text extraction before any interpretation happens.
2.  **LLM for Structuring and Validation:** The raw text is then passed to a Large Language Model (Google Gemini). The LLM's role is not to read the image, but to act as a reasoning engine to understand, parse, and structure the often messy OCR output into a clean, predefined JSON format. The LLM is used specifically for structuring, normalizing, and validating extracted data[cite: 24].

This approach is more robust and cost-effective than using a multi-modal model for everything, as it leverages the best tool for each part of the job.

### 2. Confidence Score Logic

The confidence score for each field is a mandatory requirement [cite: 14], and its logic must be explained[cite: 36]. My approach is **LLM Self-Evaluation**.

-   **Method:** The prompt explicitly instructs the Gemini model to return a confidence score between 0.0 and 1.0 for every field it extracts.
-   **Justification:** The LLM can assess its own confidence based on several factors, such as ambiguity in the OCR text (e.g., "Nane" vs. "Name"), the proximity of a label to its value, and whether the extracted value fits an expected pattern (like a date). This provides a more context-aware confidence score than a simple statistical probability. This method avoids relying solely on regex or rules[cite: 49].

### 3. Key Technology Choices

-   **FastAPI:** Chosen for its high performance, asynchronous support (which helps handle concurrent requests as required [cite: 33]), and automatic interactive documentation, which is perfect for API development.
-   **Pydantic:** Used to define a strict, well-prepared JSON schema[cite: 15, 46]. This ensures that the API always returns a consistent and predictable output, and it helps validate the LLM's response before sending it to the client.
-   **Tesseract & PyMuPDF:** A combination of powerful, open-source tools to handle both image-based and text-based documents, fulfilling the requirement to support both images and PDFs[cite: 32].

### 4. Project Structure and Error Handling

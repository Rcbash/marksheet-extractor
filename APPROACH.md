# Approach and Design Choices

[cite_start]This document outlines the technical approach, design choices, and logic behind the AI Marksheet Extraction API, as required for the assignment submission[cite: 59].

### 1. Overall Architecture & Extraction Approach

For the core extraction task, I implemented a two-step hybrid architecture to ensure both accuracy and efficiency. This approach separates the task of reading the document from understanding its content.

1.  **Optical Character Recognition (OCR):** The first step is to convert the input document (image or PDF) into raw, machine-readable text. I used a combination of powerful open-source libraries to handle this: `Tesseract` for image-based files (JPG/PNG) and `PyMuPDF` for extracting text directly from PDF files. [cite_start]This fulfills the requirement to support both images and PDFs[cite: 32].

2.  **LLM for Structuring and Validation:** The raw text from the OCR step is then passed to a Large Language Model (Google Gemini). The LLM's primary role is to act as a reasoning engine. It parses the often messy and unstructured OCR output, identifies the required entities, and structures them into the predefined JSON format. [cite_start]This aligns with the specified use of an LLM for structuring, normalizing, and validating extracted data[cite: 24].

This hybrid approach is more robust than using a single model for everything, as it leverages specialized tools for each part of the job: OCR for text extraction and an LLM for semantic understanding.

### 2. Confidence Score Logic

[cite_start]A key requirement of the project is that each extracted field must include a confidence score (0-1) [cite: 14][cite_start], and the logic for this must be explained[cite: 36].

My approach is **LLM Self-Evaluation**.

* **Method:** Instead of calculating a score using external rules or statistics, I engineered the prompt to explicitly instruct the Gemini model to return a confidence score for every piece of information it extracts. The model itself provides a float value between 0.0 and 1.0, reflecting its own certainty about the accuracy of the value.

* **Justification:** An LLM's confidence is context-aware. It can assess factors like ambiguity in the OCR text (e.g., "Nane" vs. "Name"), the proximity of a label to its value, and whether the extracted value fits an expected pattern (like a date). [cite_start]This provides a more meaningful confidence metric than simple regular expressions and avoids relying solely on rules[cite: 49].

### 3. Key Technology & Design Choices

Several key design choices were made to ensure the final API is reliable, maintainable, and meets all technical specifications.

* **FastAPI Framework:** I chose the FastAPI framework for the backend. [cite_start]Its primary advantages are its high performance and native asynchronous support, which is ideal for handling multiple concurrent requests as required[cite: 33]. Furthermore, its automatic generation of interactive API documentation (Swagger UI) is invaluable for testing and demonstration.

* [cite_start]**Pydantic for Schema Definition:** To ensure a consistent and well-prepared JSON schema[cite: 15, 46], I used Pydantic models. [cite_start]These models define the exact structure of the API's output, including all required fields like candidate details, subject-wise marks, and the overall result[cite: 10, 11, 12]. This also provides robust data validation for the LLM's response before it is sent back to the client.

* **Modular Project Structure:** The codebase is organized into distinct modules (`main.py` for API routes, `processing.py` for the core logic, `schemas.py` for data models). [cite_start]This clean, modular structure makes the code easier to read, maintain, and debug, adhering to best practices for software development[cite: 44].

* **Error Handling:** The API includes meaningful error handling to manage various failure scenarios. [cite_start]This includes checks for invalid file formats, files that exceed the 10 MB size limit [cite: 6][cite_start], and internal errors during the OCR or LLM processing stages, all of which return clear HTTP error codes and messages to the user[cite: 34].
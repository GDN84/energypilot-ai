# 📄 Document Intelligence API

**Version:** 4.0 (In Development)

A production-ready FastAPI application that extracts text, metadata, summaries, entities, and document intelligence from PDF files.

---

# Features

✔ PDF Upload

✔ Text Extraction

✔ Metadata Extraction

✔ AI Document Summarization

✔ Document Classification

✔ Named Entity Recognition

✔ JSON Storage

✔ REST API

✔ Interactive Swagger Documentation

---

# Who is this API for?

This API is designed for:

- Software developers
- AI engineers
- Document management systems
- Legal technology
- Financial technology
- Insurance companies
- Research organizations
- Government departments
- API marketplaces
- AI Agents (MCP)

---

# Technologies Used

- Python 3.12
- FastAPI
- Uvicorn
- PDFPlumber
- Transformers
- Hugging Face
- spaCy
- Sentence Transformers

---

# Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/energypilot-ai.git

cd energypilot-ai
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Linux / Mac

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the API

Start the server

```bash
uvicorn app:app --reload
```

or

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Open Swagger

```
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## GET /

Returns API information.

Example

```json
{
  "application": "Document Intelligence API",
  "status": "running",
  "version": "4.0"
}
```

---

## GET /health

Returns the health status.

Example

```json
{
  "application": "Document Intelligence API",
  "status": "healthy",
  "version": "4.0"
}
```

---

## POST /upload

Uploads a PDF and returns document intelligence.

Request

```
multipart/form-data
```

Parameter

| Name | Type | Description |
|------|------|-------------|
| file | PDF | Document to analyze |

---

# Example Response

```json
{
  "filename": "example.pdf",
  "upload_status": "uploaded",
  "number_of_pages": 12,
  "word_count": 5280,
  "character_count": 32451,
  "title": "",
  "author": "",
  "document_type": "Technical Report",
  "confidence": 0.94,
  "summary": "...",
  "entities": [
    {
      "text": "OpenAI",
      "label": "Organization"
    }
  ],
  "saved_as": "20260725_122419.json"
}
```

---

# Project Structure

```
energypilot-ai/

app.py

extractor.py

classifier.py

summarizer.py

entities.py

storage.py

utils.py

requirements.txt

database/

tests/

ai/
```

---

# Roadmap

## Version 4.0

- AI Summarization
- AI Classification
- AI Entity Recognition

## Version 5.0

- OCR
- Image Support
- Word Documents
- Excel Support

## Version 6.0

- Semantic Search
- Vector Database
- Similar Documents

## Version 7.0

- Chat with Documents (RAG)

## Version 8.0

- Multi-user Authentication
- API Keys
- Billing
- MCP Server
- RapidAPI Publishing

---

# Future Marketplace Support

The API is being prepared for publication on:

- RapidAPI
- MCP Ecosystem
- AI Agent Platforms
- Enterprise Document Processing
- Internal Business Systems

---

# License

MIT License

---

# Author

TeutonicTech

Document Intelligence API

Copyright © 2026
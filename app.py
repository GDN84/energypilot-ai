from fastapi import FastAPI, File, UploadFile, HTTPException

from extractor import extract_pdf_data
from classifier import classify_document
from summarizer import summarize
from entities import extract_entities

app = FastAPI(
    title="Document Intelligence API",
    version="3.0",
    description="AI-powered PDF extraction, classification, summarization and entity recognition."
)

# Maximum upload size (10 MB)
MAX_FILE_SIZE = 10 * 1024 * 1024


@app.get("/")
def read_root():
    return {
        "application": "Document Intelligence API",
        "status": "running",
        "version": "3.0"
    }


@app.get("/health")
def health():
    return {
        "application": "Document Intelligence API",
        "status": "healthy",
        "version": "3.0"
    }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename supplied."
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    pdf_bytes = await file.read()

    if len(pdf_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Maximum upload size is 10 MB."
        )

    try:

        # Extract everything from the PDF
        data = extract_pdf_data(pdf_bytes)

        # Classify document
        document_type, confidence = classify_document(
            data["extracted_text"]
        )

        # Generate summary
        summary = summarize(
            data["extracted_text"]
        )

        # Extract entities
        entities = extract_entities(
            data["extracted_text"]
        )

        return {

            "filename": file.filename,

            "upload_status": "uploaded",

            "number_of_pages": data["number_of_pages"],

            "word_count": data["word_count"],

            "character_count": data["character_count"],

            "title": data["title"],

            "author": data["author"],

            "subject": data["subject"],

            "creator": data["creator"],

            "producer": data["producer"],

            "creation_date": data["creation_date"],

            "modification_date": data["modification_date"],

            "document_type": document_type,

            "confidence": confidence,

            "summary": summary,

            "entities": entities,

            "extracted_text": data["extracted_text"]

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
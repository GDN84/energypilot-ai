from fastapi import FastAPI, File, UploadFile

from extractor import extract_pdf_data
from classifier import classify_document
from summarizer import summarize
from utils import get_metadata


app = FastAPI(
    title="Document Intelligence API",
    version="2.0"
)


@app.get("/")
def read_root():
    return {
        "application": "Document Intelligence API",
        "status": "running",
        "version": "2.0"
    }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Read uploaded PDF
        pdf_bytes = await file.read()

        # Extract PDF data
        pdf_data = extract_pdf_data(pdf_bytes)

        extracted_text = pdf_data["text"]
        number_of_pages = pdf_data["pages"]
        metadata = pdf_data["metadata"]

        # Metadata
        title = get_metadata(metadata, "Title")
        author = get_metadata(metadata, "Author")
        subject = get_metadata(metadata, "Subject")
        creator = get_metadata(metadata, "Creator")
        producer = get_metadata(metadata, "Producer")
        creation_date = get_metadata(metadata, "CreationDate")
        modification_date = get_metadata(metadata, "ModDate")

        # Statistics
        word_count = len(extracted_text.split()) if extracted_text else 0
        character_count = len(extracted_text)

        # Classification
        document_type, confidence = classify_document(extracted_text)

        # Summary
        summary = summarize(extracted_text)

        return {
            "filename": file.filename,
            "number_of_pages": number_of_pages,
            "word_count": word_count,
            "character_count": character_count,
            "title": title,
            "author": author,
            "subject": subject,
            "creator": creator,
            "producer": producer,
            "creation_date": creation_date,
            "modification_date": modification_date,
            "document_type": document_type,
            "confidence": confidence,
            "summary": summary,
            "extracted_text": extracted_text,
            "upload_status": "uploaded"
        }

    except Exception as e:
        return {
            "filename": file.filename,
            "number_of_pages": 0,
            "word_count": 0,
            "character_count": 0,
            "title": "",
            "author": "",
            "subject": "",
            "creator": "",
            "producer": "",
            "creation_date": "",
            "modification_date": "",
            "document_type": "Unknown",
            "confidence": 0.50,
            "summary": "",
            "extracted_text": "",
            "upload_status": "failed",
            "error": str(e)
        }
from fastapi import FastAPI, File, UploadFile, HTTPException

from extractor import extract_pdf_data
from classifier import classify_document
from summarizer import summarize
from entities import extract_entities
from storage import save_document


app = FastAPI(
    title="Document Intelligence API",
    version="3.2"
)


@app.get("/")
def read_root():
    return {
        "application": "Document Intelligence API",
        "status": "running",
        "version": "3.2"
    }


@app.get("/health")
def health():
    return {
        "application": "Document Intelligence API",
        "status": "healthy",
        "version": "3.2"
    }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:

        pdf_bytes = await file.read()

        data = extract_pdf_data(pdf_bytes)

        extracted_text = data["extracted_text"]

        summary = summarize(extracted_text)

        document_type, confidence = classify_document(extracted_text)

        entities = extract_entities(extracted_text)

        response = {
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

            "extracted_text": extracted_text
        }

        saved_file = save_document(response)

        response["saved_as"] = saved_file

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
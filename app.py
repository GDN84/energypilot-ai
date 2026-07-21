from fastapi import FastAPI, File, UploadFile
import pdfplumber
from io import BytesIO

# Initialize the FastAPI application with the existing API metadata.
app = FastAPI(
    title="Document Intelligence API",
    version="1.1"
)


# Root endpoint preserved for health checks and API identification.
@app.get("/")
def read_root():
    return {
        "application": "Document Intelligence API",
        "status": "running",
        "version": "1.1"
    }


# Helper function to safely fetch PDF metadata values without raising errors.
def _get_metadata_value(metadata, key, fallback=""):
    if not metadata:
        return fallback

    value = metadata.get(key)

    if value is None:
        return fallback

    return str(value)


# Upload endpoint preserved with enhanced PDF text and metadata extraction.
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        pdf_bytes = await file.read()

        extracted_text = ""
        number_of_pages = 0

        with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
            number_of_pages = len(pdf.pages)

            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"

            metadata = pdf.metadata or {}
            title = _get_metadata_value(metadata, "Title")
            author = _get_metadata_value(metadata, "Author")
            subject = _get_metadata_value(metadata, "Subject")
            creator = _get_metadata_value(metadata, "Creator")
            producer = _get_metadata_value(metadata, "Producer")
            creation_date = _get_metadata_value(metadata, "CreationDate")
            modification_date = _get_metadata_value(metadata, "ModDate")

        word_count = len(extracted_text.split()) if extracted_text else 0
        character_count = len(extracted_text)

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
            "extracted_text": extracted_text,
            "upload_status": "uploaded"
        }

    except Exception as e:
        return {
            "filename": file.filename,
            "number_of_pages": 0,
            "extracted_text": "",
            "upload_status": "failed",
            "error": str(e)
        }
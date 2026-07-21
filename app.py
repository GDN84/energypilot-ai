from fastapi import FastAPI, File, UploadFile
import pdfplumber
from io import BytesIO

# Initialize the FastAPI application with the existing API metadata.
app = FastAPI(
    title="Document Intelligence API",
    version="1.2"
)


# Root endpoint preserved for health checks and API identification.
@app.get("/")
def read_root():
    return {
        "application": "Document Intelligence API",
        "status": "running",
        "version": "1.2"
    }


# Helper function to safely fetch PDF metadata values without raising errors.
def _get_metadata_value(metadata, key, fallback=""):
    if not metadata:
        return fallback

    value = metadata.get(key)

    if value is None:
        return fallback

    return str(value)


# Classify the extracted document text using simple keyword matching.
# This keeps the logic lightweight and deterministic while still adding
# a basic document type hint to the response payload.
def _classify_document(extracted_text: str):
    if not extracted_text:
        return "Unknown", 0.50

    normalized_text = extracted_text.lower()

    # Each category uses a small set of keywords. If multiple keywords are found,
    # the confidence increases slightly to reflect the stronger match.
    categories = [
        ("Invoice", ["invoice", "bill", "amount due", "invoice date", "vendor"]),
        ("Contract", ["contract", "agreement", "party", "effective date", "terms and conditions"]),
        ("CV", ["curriculum vitae", "resume", "experience", "employment", "skills"]),
        ("Bank Statement", ["bank statement", "account number", "statement date", "balance", "transaction"]),
        ("Insurance", ["insurance", "policy", "claim", "premium", "coverage"]),
        ("Technical Report", ["technical report", "technical", "analysis", "findings", "summary"]),
        ("Solar Report", ["solar", "photovoltaic", "panel", "inverter", "energy generation"]),
        ("Research Paper", ["abstract", "introduction", "methodology", "results", "conclusion", "references", "doi"]),
        ("Purchase Order", ["purchase order", "po number", "purchase", "vendor", "order number"]),
    ]

    best_document_type = "Unknown"
    best_confidence = 0.50

    for document_type, keywords in categories:
        matched_keywords = [keyword for keyword in keywords if keyword in normalized_text]
        if matched_keywords:
            confidence = min(1.00, 0.50 + (0.10 * len(matched_keywords)))
            if confidence > best_confidence:
                best_document_type = document_type
                best_confidence = confidence

    return best_document_type, round(best_confidence, 2)


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
        document_type, confidence = _classify_document(extracted_text)

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
            "upload_status": "uploaded",
            "document_type": document_type,
            "confidence": confidence
        }

    except Exception as e:
        return {
            "filename": file.filename,
            "number_of_pages": 0,
            "extracted_text": "",
            "upload_status": "failed",
            "error": str(e),
            "document_type": "Unknown",
            "confidence": 0.50
        }
from fastapi import FastAPI, File, UploadFile
import pdfplumber
from io import BytesIO

app = FastAPI(title="EnergyPilot API", version="0.1")


@app.get("/")
def read_root():
    return {
        "application": "EnergyPilot API",
        "status": "running",
        "version": "0.1",
    }


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

        return {
            "filename": file.filename,
            "number_of_pages": number_of_pages,
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

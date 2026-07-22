import pdfplumber
from io import BytesIO


def extract_pdf_data(pdf_bytes):
    extracted_text = ""

    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:

        number_of_pages = len(pdf.pages)

        for page in pdf.pages:
            text = page.extract_text()

            if text:
                extracted_text += text + "\n"

        metadata = pdf.metadata or {}

    return {
        "text": extracted_text,
        "pages": number_of_pages,
        "metadata": metadata
    }
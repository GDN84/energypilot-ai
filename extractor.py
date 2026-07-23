import pdfplumber
from io import BytesIO

from utils import (
    get_metadata,
    count_words,
    count_characters,
)


def extract_pdf_data(pdf_bytes):
    """
    Extract text, metadata and statistics from a PDF.
    """

    extracted_text = ""

    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:

        number_of_pages = len(pdf.pages)

        for page in pdf.pages:

            text = page.extract_text()

            if text:
                extracted_text += text + "\n"

        metadata = pdf.metadata or {}

    return {

        "number_of_pages": number_of_pages,

        "word_count": count_words(extracted_text),

        "character_count": count_characters(extracted_text),

        "title": get_metadata(metadata, "Title"),

        "author": get_metadata(metadata, "Author"),

        "subject": get_metadata(metadata, "Subject"),

        "creator": get_metadata(metadata, "Creator"),

        "producer": get_metadata(metadata, "Producer"),

        "creation_date": get_metadata(metadata, "CreationDate"),

        "modification_date": get_metadata(metadata, "ModDate"),

        "extracted_text": extracted_text

    }
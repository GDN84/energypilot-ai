def classify_document(text):

    text = text.lower()

    if "invoice" in text:
        return "Invoice", 0.90

    if "contract" in text:
        return "Contract", 0.90

    if "report" in text:
        return "Report", 0.90

    return "Unknown", 0.50
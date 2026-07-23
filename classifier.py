def classify_document(text):
    """
    Simple keyword-based classifier.
    """

    if not text:
        return "Unknown", 0.50

    text = text.lower()

    document_types = {

        "Invoice": [
            "invoice",
            "amount due",
            "vat",
            "invoice number",
            "subtotal",
        ],

        "Contract": [
            "agreement",
            "contract",
            "party",
            "terms",
        ],

        "Report": [
            "report",
            "analysis",
            "summary",
            "findings",
        ],

        "CV": [
            "curriculum vitae",
            "resume",
            "education",
            "employment",
        ],

        "Bank Statement": [
            "statement",
            "balance",
            "account number",
            "transaction",
        ],

    }

    best_type = "Unknown"
    best_score = 0

    for document_type, keywords in document_types.items():

        score = sum(keyword in text for keyword in keywords)

        if score > best_score:
            best_score = score
            best_type = document_type

    if best_score == 0:
        return "Unknown", 0.50

    confidence = min(0.60 + (best_score * 0.10), 0.95)

    return best_type, round(confidence, 2)
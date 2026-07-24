def extract_entities(text):
    """
    Very simple entity extraction (Version 3.0).
    Later this will be replaced with spaCy or another NLP library.
    """

    entities = []

    keywords = {
        "Location": [
            "Upington",
            "Northern Cape",
            "Johannesburg",
            "Cape Town",
            "Pretoria",
            "South Africa"
        ],
        "Organization": [
            "SACAA",
            "Verra",
            "Microsoft",
            "OpenAI"
        ]
    }

    for entity_type, words in keywords.items():
        for word in words:
            if word.lower() in text.lower():
                entities.append({
                    "text": word,
                    "label": entity_type
                })

    return entities
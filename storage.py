import json
import os
from datetime import datetime


DATABASE_FOLDER = "database"


os.makedirs(DATABASE_FOLDER, exist_ok=True)


def save_document(document):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{timestamp}.json"

    filepath = os.path.join(DATABASE_FOLDER, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(document, f, indent=4, ensure_ascii=False)

    return filename
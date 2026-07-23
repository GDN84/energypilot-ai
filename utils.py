def get_metadata(metadata, key, fallback=""):
    """
    Safely retrieve a metadata value from a PDF.
    """

    if metadata is None:
        return fallback

    value = metadata.get(key)

    if value is None:
        return fallback

    return str(value)


def count_words(text):
    if not text:
        return 0

    return len(text.split())


def count_characters(text):
    if not text:
        return 0

    return len(text)
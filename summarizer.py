def summarize(text, max_words=75):
    """
    Lightweight extractive summary.
    """

    if not text:
        return ""

    words = text.split()

    if len(words) <= max_words:
        return text

    return " ".join(words[:max_words]) + "..."
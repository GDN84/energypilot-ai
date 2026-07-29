from transformers import pipeline

from ai.config import (
    SUMMARIZER_MODEL,
    MAX_INPUT_CHARACTERS,
    SUMMARY_MAX_LENGTH,
    SUMMARY_MIN_LENGTH,
)

summarizer = pipeline(
    "text2text-generation",
    model=SUMMARIZER_MODEL
)


def summarize_ai(text: str) -> str:
    """
    Generate an AI summary using Hugging Face.
    """

    if not text.strip():
        return ""

    text = text[:MAX_INPUT_CHARACTERS]

    prompt = (
        "Summarize the following document in one concise paragraph:\n\n"
        + text
    )

    result = summarizer(
        prompt,
        max_length=SUMMARY_MAX_LENGTH,
        min_length=SUMMARY_MIN_LENGTH,
        do_sample=False,
    )

    return result[0]["generated_text"]
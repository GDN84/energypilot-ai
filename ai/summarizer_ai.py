from transformers import pipeline

summarizer = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)


def summarize_ai(text):

    text = text[:3000]

    prompt = (
        "Summarize the following document in a concise paragraph:\n\n"
        + text
    )

    result = summarizer(
        prompt,
        max_new_tokens=150,
        do_sample=False
    )

    return result[0]["generated_text"]
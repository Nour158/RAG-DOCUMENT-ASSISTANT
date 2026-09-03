import ollama
from app.core.config import get_settings


SYSTEM = """
You are Mars Explorer, a grounded RAG assistant.

Rules:
1. Answer ONLY from the supplied retrieved context.
2. Do not use outside knowledge.
3. If the answer is not in the context, say:
   "I don't know based on the provided NASA documents."
4. Cite factual claims using [Source 1], [Source 2], etc.
5. Keep answers clear and concise.
"""


def generate(question, chunks):

    if not chunks:
        return (
            "I don't know based on the provided NASA documents.",
            []
        )

    context = []
    sources = []

    for i, c in enumerate(chunks, start=1):

        label = f"{c['source']} | {c['chunk']}"

        sources.append(
            f"{label} | {c.get('url', '')}"
        )

        context.append(
            f"[Source {i}]\n"
            f"Document: {c['source']}\n"
            f"Chunk: {c['chunk']}\n"
            f"URL: {c.get('url', '')}\n"
            f"Content:\n{c['text']}"
        )

    context_text = "\n\n".join(context)

    prompt = f"""
RETRIEVED CONTEXT
-----------------
{context_text}

USER QUESTION
-------------
{question}

ANSWER
------
"""

    s = get_settings()

    response = ollama.chat(
        model=s.ollama_model,
        messages=[
            {
                "role": "system",
                "content": SYSTEM
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.1
        }
    )

    return response["message"]["content"], sources
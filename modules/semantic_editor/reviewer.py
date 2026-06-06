import json
import ollama

from .prompts import SYSTEM_PROMPT


def review_chunks(chunks):

    prompt = f"""
Transcript Segments:

{json.dumps(chunks, indent=2)}

Return JSON only.
"""

    response = ollama.chat(
        model="gemma3",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response["message"]["content"]

    return json.loads(content)
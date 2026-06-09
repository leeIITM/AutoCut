


import json
import re
import ollama

from .prompts import SYSTEM_PROMPT


def review_chunks(chunks):

    prompt = f"""
Analyze these transcript chunks.

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

    match = re.search(
        r'\{.*\}',
        content,
        re.DOTALL
    )

    if not match:
        raise ValueError(content)

    return json.loads(match.group())
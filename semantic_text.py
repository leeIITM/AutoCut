from modules.captions import transcribe_video

from modules.semantic_editor.chunker import (
    build_chunks
)

from modules.semantic_editor.reviewer import (
    review_chunks
)

segments = list(
    transcribe_video(
        "output/no_silence.mp4"
    )
)

chunks = build_chunks(segments)

decision = review_chunks(chunks)

remove_ids = set(
    decision["remove"]
)

print()

for chunk in chunks:

    if chunk["id"] in remove_ids:
        print(
            f"[REMOVE] {chunk['text']}"
        )
    else:
        print(
            f"[KEEP] {chunk['text']}"
        )
from modules.captions import transcribe_video

from modules.semantic_editor.chunker import (
    build_semantic_chunks
)

from modules.semantic_editor.reviewer import (
    review_chunks
)


segments = list(
    transcribe_video(
        "output/no_silence.mp4"
    )
)

chunks = build_semantic_chunks(
    segments
)

print("\n===== CHUNKS =====\n")

for c in chunks:

    print("-" * 60)
    print(
        f"{c['start']:.2f} -> {c['end']:.2f}"
    )
    print(c["text"])

print()

decision = review_chunks(
    chunks
)

print("\n===== LABELS =====\n")

for item in decision["chunks"]:

    print(
        item["id"],
        item["label"],
        item["reason"]
    )
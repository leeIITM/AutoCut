def build_semantic_chunks(segments):
    """
    Merge whisper segments into larger semantic chunks.

    Chunk boundaries:
    - punctuation
    - max length
    """

    chunks = []

    current_text = []
    current_start = None
    current_end = None
    current_segment_ids = []

    chunk_id = 0

    for seg_id, seg in enumerate(segments):

        text = seg.text.strip()

        if current_start is None:
            current_start = seg.start

        current_end = seg.end

        current_text.append(text)
        current_segment_ids.append(seg_id)

        merged_text = " ".join(current_text)

        should_close = False

        if merged_text.endswith((".", "!", "?")):
            should_close = True

        if len(merged_text.split()) > 40:
            should_close = True

        if should_close:

            chunks.append({
                "id": chunk_id,
                "start": current_start,
                "end": current_end,
                "text": merged_text,
                "segment_ids": current_segment_ids
            })

            chunk_id += 1

            current_text = []
            current_segment_ids = []
            current_start = None
            current_end = None

    if current_text:

        chunks.append({
            "id": chunk_id,
            "start": current_start,
            "end": current_end,
            "text": " ".join(current_text),
            "segment_ids": current_segment_ids
        })

    return chunks
def build_chunks(segments):
    chunks = []

    for idx, segment in enumerate(segments):
        chunks.append({
            "id": idx,
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip()
        })

    return chunks
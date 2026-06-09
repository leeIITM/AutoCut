from faster_whisper import WhisperModel

# Given a video file path, transcribe the audio and return the segments with word timestamps.
def transcribe_video(video_path):

    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8"
    )

    segments, info = model.transcribe(
        video_path,
        word_timestamps=True
    )

    return list(segments)

def seconds_to_srt(seconds):

    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    ms = int((seconds - int(seconds)) * 1000)

    return (
        f"{hrs:02}:{mins:02}:{secs:02},"
        f"{ms:03}"
    )


def generate_srt(segments, output_file):

    captions = []
    idx = 1

    for segment in segments:

        words = segment.words

        if not words:
            continue

        current_words = []
        start_time = words[0].start

        for word in words:

            current_words.append(word.word)

            should_split = (
                len(current_words) >= 7
                or word.word.endswith(
                    (".", "!", "?")
                )
            )

            if should_split:

                captions.append(
                    {
                        "id": idx,
                        "start": start_time,
                        "end": word.end,
                        "text": " ".join(current_words)
                    }
                )

                idx += 1

                current_words = []

                start_time = word.end

    with open(output_file, "w", encoding="utf-8") as f:

        for cap in captions:

            f.write(f"{cap['id']}\n")

            f.write(
                f"{seconds_to_srt(cap['start'])}"
                f" --> "
                f"{seconds_to_srt(cap['end'])}\n"
            )

            f.write(cap["text"] + "\n\n")
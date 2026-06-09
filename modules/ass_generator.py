def ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60

    return f"{h}:{m:02d}:{s:05.2f}"


ASS_HEADER = """[Script Info]
Title: AutoCut Subtitles
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding

Style: Default,Arial,24,&H00FFFFFF,&H0000FFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,2,0,2,20,20,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def generate_ass(segments, output_path):
    lines = [ASS_HEADER]



    for seg in segments:

        words = seg.words

        for i in range(0, len(words), 3):

            chunk = words[i:i+3]

            start = ass_time(float(chunk[0].start))
            end = ass_time(float(chunk[-1].end))

            text = " ".join(
                w.word.strip().upper()
                for w in chunk
            )

            lines.append(
                f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}"
            )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"ASS subtitle written to {output_path}")
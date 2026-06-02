'''from modules.transcriber import Transcriber

transcriber = Transcriber()

result = transcriber.transcribe("input/test_video.mp4")

for segment in result["segments"]:
    print(
        f"{segment['start']:.2f} --> "
        f"{segment['end']:.2f} | "
        f"{segment['text']}"
    )'''

from modules.silence import detect_silence, get_keep_intervals, get_video_duration

silent = detect_silence("output/audio.wav", threshold=2000)

duration = get_video_duration("input/test_video.mp4")
keep = get_keep_intervals(
    silent_intervals=silent,
    video_duration=duration   # replace with actual duration
)

print("Silent:", silent)
print("Keep:", keep)

from modules.video import cut_video_segments

segments = cut_video_segments(
    "input/test_video.mp4",
    keep
)

print(segments)
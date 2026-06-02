import os
import subprocess
import sys

from modules.silence import detect_speech_silero, add_padding,get_video_duration
from modules.video import cut_video_segments


def extract_audio(video_path, output_audio):
    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        output_audio
    ]

    subprocess.run(cmd, check=True)


def concatenate_segments(segment_paths, output_video):
    concat_file = "output/segments.txt"

    with open(concat_file, "w") as f:
        for segment in segment_paths:
            abs_path = os.path.abspath(segment)
            f.write(f"file '{abs_path}'\n")

    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-c", "copy",
        output_video
    ]

    subprocess.run(cmd, check=True)


def main(video_path):
    os.makedirs("output", exist_ok=True)

    audio_path = "output/audio.wav"
    video_duration = get_video_duration(video_path)

    print("[1/4] Extracting audio...")
    extract_audio(video_path, audio_path)

    print("[2/4] Detecting speech...")
    speech_intervals = detect_speech_silero(audio_path)

    speech_intervals = add_padding(
        speech_intervals,
        video_duration,
        before=0.2,
        after=0.2
    )

    print(f"Found {len(speech_intervals)} speech segments")

    print("[3/4] Cutting video...")
    segment_paths = cut_video_segments(
        video_path,
        speech_intervals
    )

    print("[4/4] Stitching segments...")
    concatenate_segments(
        segment_paths,
        "output/no_silence.mp4"
    )

    print("\nDone!")
    print("Output: output/no_silence.mp4")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py input/video.mp4")
        sys.exit(1)

    main(sys.argv[1])
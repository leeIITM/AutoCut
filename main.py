import os
import subprocess
import sys

from modules.silence import (
    detect_speech_silero,
    add_padding,
    get_video_duration
)

from modules.video import cut_video_segments

from modules.captions import (
    transcribe_video,
    generate_srt
)

from modules.utils import run_ffmpeg


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


def burn_captions(
        input_video,
        srt_file,
        output_video):

    run_ffmpeg([
        "ffmpeg",
        "-y",
        "-i",
        input_video,
        "-vf",
        (
            f"subtitles={srt_file}:"
            "force_style='"
            "Alignment=2,"
            "FontSize=22,"
            "Outline=2'"
        ),
        "-c:a",
        "copy",
        output_video
    ])


def process_video(video_path):

    os.makedirs("output", exist_ok=True)

    audio_path = "output/audio.wav"

    no_silence_video = "output/no_silence.mp4"

    srt_file = "output/captions.srt"

    final_video = "output/final.mp4"

    video_duration = get_video_duration(video_path)

    print("[1/6] Extracting audio...")
    extract_audio(video_path, audio_path)

    print("[2/6] Detecting speech...")
    speech_intervals = detect_speech_silero(audio_path)

    '''speech_intervals = add_padding(
        speech_intervals,
        video_duration,
        before=0.2,
        after=0.2
    )'''

    print(
        f"Found {len(speech_intervals)} speech segments"
    )

    print("[3/6] Cutting video...")
    segment_paths = cut_video_segments(
        video_path,
        speech_intervals
    )

    print("[4/6] Stitching segments...")
    concatenate_segments(
        segment_paths,
        no_silence_video
    )

    print("[5/6] Generating captions...")

    segments = transcribe_video(
        no_silence_video
    )

    generate_srt(
        segments,
        srt_file
    )

    print("[6/6] Burning captions...")

    burn_captions(
        no_silence_video,
        srt_file,
        final_video
    )

    print("\nDone!")
    print(f"Output: {final_video}")
    return os.path.abspath(final_video)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(
            "Usage: python main.py input/video.mp4"
        )
        sys.exit(1)

    process_video(sys.argv[1])
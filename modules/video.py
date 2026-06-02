import os
import subprocess


def cut_video_segments(video_path, keep_intervals, output_dir="output/segments"):
    os.makedirs(output_dir, exist_ok=True)

    segment_paths = []

    for i, (start, end) in enumerate(keep_intervals):
        output_file = os.path.join(output_dir, f"segment_{i}.mp4")

        cmd = [
    "ffmpeg",
    "-y",
    "-ss", str(start),
    "-to", str(end),
    "-i", video_path,
    "-c:v", "libx264",
    "-c:a", "aac",
    output_file
]

        subprocess.run(cmd, check=True)

        segment_paths.append(output_file)

    return segment_paths
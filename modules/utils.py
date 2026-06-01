import subprocess

def run_ffmpeg(cmd):
    print("Running:", " ".join(cmd))

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return result
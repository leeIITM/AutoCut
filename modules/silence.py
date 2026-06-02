import numpy as np
from scipy.io import wavfile


def detect_silence(
    audio_path,
    threshold=2000,
    min_silence_duration=0.5,
    window_size=0.05
):
    sample_rate, audio = wavfile.read(audio_path)

    if len(audio.shape) > 1:
        audio = audio.mean(axis=1)

    window_samples = int(window_size * sample_rate)

    rms_values = []
    times = []

    for i in range(0, len(audio), window_samples):
        chunk = audio[i:i + window_samples]

        if len(chunk) == 0:
            continue

        rms = np.sqrt(np.mean(chunk.astype(np.float64) ** 2))

        rms_values.append(rms)
        times.append(i / sample_rate)

    silent_intervals = []
    silence_start = None

    for t, rms in zip(times, rms_values):

        if rms < threshold:
            if silence_start is None:
                silence_start = t
        else:
            if silence_start is not None:
                duration = t - silence_start

                if duration >= min_silence_duration:
                    silent_intervals.append((silence_start, t))

                silence_start = None

    return silent_intervals

import cv2

def get_video_duration(video_path):
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    cap.release()

    return frames / fps

def get_keep_intervals(silent_intervals, video_duration):
    keep = []

    current = 0

    for start, end in silent_intervals:
        if start > current:
            keep.append((current, start))
        current = end

    if current < video_duration:
        keep.append((current, video_duration))

    return keep


### ======================================================================== ###
###                         Alternative using silero-vad
### ========================================================================== ###
from silero_vad import load_silero_vad, get_speech_timestamps
import torchaudio


def detect_speech_silero(audio_path):
    """
    Returns:
    [
        (start_sec, end_sec),
        ...
    ]
    """

    model = load_silero_vad()

    wav, sr = torchaudio.load(audio_path)

    # Convert stereo -> mono if needed
    if wav.shape[0] > 1:
        wav = wav.mean(dim=0, keepdim=True)

    speech_timestamps = get_speech_timestamps(
        wav[0],
        model,
        sampling_rate=sr
    )

    speech_intervals = []

    for segment in speech_timestamps:
        start_sec = segment["start"] / sr
        end_sec = segment["end"] / sr

        speech_intervals.append(
            (start_sec, end_sec)
        )

    return speech_intervals

def add_padding(speech_intervals, video_duration,
                before=0.15, after=0.15):

    padded = []

    for start, end in speech_intervals:
        new_start = max(0, start - before)
        new_end = min(video_duration, end + after)

        padded.append((new_start, new_end))

    return padded
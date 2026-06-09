<div align="center">

# ✂️ AutoCut

### AI-Assisted Video Editing Pipeline

**Automatically remove pauses, fillers, repetitions, and dead air — entirely local, no API costs.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Whisper](https://img.shields.io/badge/Faster--Whisper-ASR-412991?style=flat-square)](https://github.com/SYSTRAN/faster-whisper)
[![Ollama](https://img.shields.io/badge/Ollama-Gemma%203-black?style=flat-square)](https://ollama.com)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Video%20Processing-007808?style=flat-square&logo=ffmpeg&logoColor=white)](https://ffmpeg.org)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

</div>

---

## 🎬 Demo

> *AutoCut in action — Gradio interface walkthrough*

<!-- Replace the path below with your actual video file or a GIF export -->
https://github.com/user-attachments/assets/YOUR_VIDEO_ASSET_ID_HERE

> **💡 Tip:** To embed your local `.mp4` — go to your GitHub repo → open any Issue or the README edit view → drag-and-drop your video file → GitHub generates a hosted URL you can paste above.

---

## ✨ What It Does

Manual video editing of educational and technical content is slow. A one-hour recording typically takes 2–3 hours to clean up. AutoCut handles it automatically.

| Without AutoCut | With AutoCut |
|---|---|
| *"Today we are going to... umm... discuss neural networks."* | *"Today we are going to discuss neural networks."* |
| *"The answer is... ahhh... 42."* | *"The answer is... 42."* *(dramatic pause preserved)* |

**AutoCut is not a silence cutter.** It combines speech recognition, voice activity detection, and a local LLM to approximate how a human editor thinks — understanding *context and meaning*, not just audio amplitude.

---

## 🧠 How It Works

```
Video Input
    │
    ▼
Audio Extraction (FFmpeg)
    │
    ▼
Faster-Whisper ASR  ──►  Word-Level Timestamps
    │
    ▼
Semantic Chunk Generation  (sentence boundaries)
    │
    ▼
Gemma 3 via Ollama  ──►  Edit Recommendations
    │
    ▼
Timestamp Reconstruction  (chunk → frame mapping)
    │
    ▼
FFmpeg Video Reconstruction
    │
    ▼
Final Output Video ✓
```

### Key Technical Components

| Component | Tool | Role |
|---|---|---|
| Speech Recognition | Faster-Whisper | Word-level transcription + timestamps |
| Voice Activity Detection | Silero VAD | Speech / non-speech segmentation |
| Semantic Reasoning | Gemma 3 (Ollama) | Identifies redundancy, restarts, dead content |
| Video Processing | FFmpeg | Frame-accurate trimming and reconstruction |
| User Interface | Gradio | Interactive review and edit approval |

---

## 🔍 Key Technical Finding — The Whisper Suppression Problem

One of the most significant discoveries during development:

> **Faster-Whisper intentionally suppresses filler speech** — `umm`, `uh`, `ah`, breathing sounds — from output transcripts. This improves readability for humans but creates a critical mismatch for automated editing: the filler *audio* remains in the video while no transcript *token* exists for it.

This means an LLM reasoning purely over the transcript cannot detect or timestamp filler regions. AutoCut's hybrid architecture addresses this by combining transcript-level semantic reasoning with audio-level VAD signals.

---

## ⚙️ Installation

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally
- FFmpeg on your system PATH

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/autocut.git
cd autocut

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Pull the Gemma 3 model via Ollama
ollama pull gemma3
```

### `requirements.txt`

```
faster-whisper
silero-vad
torch
torchaudio
gradio
ffmpeg-python
ollama
```

---

## 🚀 Usage

### Option A — Gradio UI (Recommended)

```bash
python app.py
```

Then open `http://localhost:7860` in your browser. Upload a video, review the AI-generated edit recommendations, approve or reject cuts, and export.

### Option B — CLI / Programmatic

```python
from autocut import pipeline

result = pipeline.run(
    input_video="lecture.mp4",
    output_video="lecture_edited.mp4",
    model="gemma3",          # Ollama model name
    whisper_model="small",   # or base / medium / large-v3
    min_silence_ms=500,      # silence threshold in ms
)

print(result.edit_decisions)   # list of (start, end, reason) tuples
```

### CLI

```bash
python -m autocut \
  --input lecture.mp4 \
  --output lecture_edited.mp4 \
  --whisper-model small \
  --llm gemma3
```

---

## 🔄 Development Iterations

AutoCut was built through four architectural iterations, each exposing concrete failure modes:

```
Iteration 1 — Silence Detection
  ✅ Removes dead air
  ❌ Fillers have audio energy — not detected
  ❌ No semantic understanding

Iteration 2 — Voice Activity Detection (Silero VAD)
  ✅ Better noise robustness
  ✅ More accurate speech boundaries
  ❌ Correctly classifies "umm" as speech — not helpful for editing

Iteration 3 — Speech Recognition (Faster-Whisper)
  ✅ Word-level timestamps
  ⚠️  Discovery: Whisper suppresses fillers → audio-transcript mismatch

Iteration 4 — Semantic LLM Editing (Current)
  ✅ Content-aware decisions (redundancy, restarts, false starts)
  ✅ Fully local inference via Ollama
  ⚙️  Timestamp reconstruction in progress
```

---

## 📊 Project Status

| Feature | Status |
|---|---|
| Faster-Whisper integration | ✅ Done |
| Silero VAD experimentation | ✅ Done |
| Silence-removal baseline | ✅ Done |
| Semantic chunk generation | ✅ Done |
| Gemma 3 via Ollama | ✅ Done |
| Automated edit recommendations | ✅ Done |
| Improved timestamp alignment | 🔄 In Progress |
| Semantic confidence scoring | 🔄 In Progress |
| Automated video reconstruction | 🔄 In Progress |
| Gradio UI | 🔄 In Progress |
| Forced alignment (filler detection) | 📋 Planned |
| Multi-speaker editing | 📋 Planned |

---

## 🗺️ Roadmap

**Short-term**
- Gradio UI with timeline visualisation and per-cut approval
- Automated FFmpeg rendering pipeline

**Medium-term**
- Forced alignment (e.g. Montreal Forced Aligner) for filler detection independent of transcript
- Confidence-based edit scoring — let users dial a threshold

**Long-term**
- Multi-speaker support
- Learning from user feedback (approved/rejected cuts)
- Real-time editing assistance

---

## 🗂️ Project Structure

```
autocut/
├── app.py                  # Gradio interface entry point
├── autocut/
│   ├── pipeline.py         # Main orchestration
│   ├── transcribe.py       # Faster-Whisper wrapper
│   ├── vad.py              # Silero VAD integration
│   ├── chunker.py          # Semantic chunk generation
│   ├── llm.py              # Gemma 3 / Ollama interface
│   ├── editor.py           # FFmpeg reconstruction
│   └── align.py            # Timestamp mapping (WIP)
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

- **[Faster-Whisper](https://github.com/SYSTRAN/faster-whisper)** — CTranslate2-optimised Whisper for fast local ASR
- **[Silero VAD](https://github.com/snakers4/silero-vad)** — Lightweight ML-based voice activity detection
- **[Gemma 3 via Ollama](https://ollama.com/library/gemma3)** — Local LLM for semantic edit reasoning
- **[FFmpeg](https://ffmpeg.org)** — Frame-accurate video trimming and reconstruction
- **[Gradio](https://gradio.app)** — Rapid UI for interactive edit review

---

## 👤 Author

**Kutraleeswaran N. Harikrishnan**
B.Tech Aerospace Engineering + IDDD Robotics — IIT Madras

---

<div align="center">
<sub>Built with 🤖 local AI — no cloud APIs, no subscription fees, no data leaving your machine.</sub>
</div>

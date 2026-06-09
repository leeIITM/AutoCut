<div align="center">

# ✂️ AutoCut

### AI-Assisted Video Editing Pipeline

**A local AI pipeline for intelligent video editing — combining speech recognition, VAD, and LLM reasoning to cut pauses, fillers, and dead air. Semantic editing under active development.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Whisper](https://img.shields.io/badge/Faster--Whisper-ASR-412991?style=flat-square)](https://github.com/SYSTRAN/faster-whisper)
[![Ollama](https://img.shields.io/badge/Ollama-Gemma%203-black?style=flat-square)](https://ollama.com)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Video%20Processing-007808?style=flat-square&logo=ffmpeg&logoColor=white)](https://ffmpeg.org)
[![Status](https://img.shields.io/badge/Status-Active%20Development-orange?style=flat-square)]()
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

Manual video editing of educational and technical content is slow. A one-hour recording typically takes 2–3 hours to clean up. AutoCut is being built to automate that.

| Without AutoCut | With AutoCut *(target behaviour)* |
|---|---|
| *"Today we are going to... umm... discuss neural networks."* | *"Today we are going to discuss neural networks."* |
| *"The answer is... ahhh... 42."* | *"The answer is... 42."* *(dramatic pause preserved)* |

AutoCut is **not** a simple silence cutter. The goal is to combine speech recognition, voice activity detection, and a local LLM to approximate how a human editor thinks — understanding *context and meaning*, not just audio amplitude.

**Current state:** The acoustic pipeline (VAD + Whisper ASR + silence removal) is fully functional. The semantic LLM editing layer — Gemma 3 reasoning over transcript chunks to detect redundancy and restarts — is integrated but under active development.

---

## 🧠 Architecture

### What's Working Now

```
Video Input
    │
    ▼
Audio Extraction (FFmpeg)
    │
    ▼
Silero VAD  ──►  Speech / Non-speech Segments
    │
    ▼
Faster-Whisper ASR  ──►  Word-Level Timestamps
    │
    ▼
Silence-Based Edit Decisions
    │
    ▼
FFmpeg Video Reconstruction  ──►  Output ✓
```

### Target Architecture *(in progress)*

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
Gemma 3 via Ollama  ──►  Edit Recommendations   ← WIP
    │
    ▼
Timestamp Reconstruction  (chunk → frame mapping)   ← WIP
    │
    ▼
FFmpeg Video Reconstruction  ──►  Output ✓
```

### Key Technical Components

| Component | Tool | Status |
|---|---|---|
| Speech Recognition | Faster-Whisper | ✅ Working |
| Voice Activity Detection | Silero VAD | ✅ Working |
| Silence-based editing | FFmpeg | ✅ Working |
| Semantic chunk generation | Custom (Python) | ✅ Working |
| LLM edit reasoning | Gemma 3 via Ollama | 🔄 In Progress |
| Timestamp reconstruction | Custom (Python) | 🔄 In Progress |
| User Interface | Gradio | 🔄 In Progress |

---

## 🔍 Key Technical Finding — The Whisper Suppression Problem

One of the most significant discoveries during development:

> **Faster-Whisper intentionally suppresses filler speech** — `umm`, `uh`, `ah`, breathing sounds — from output transcripts. This improves readability for humans but creates a critical mismatch for automated editing: the filler *audio* remains in the video while no transcript *token* exists for it.

```
Audio:       "Today... umm... we discuss AI."
Transcript:  "Today we discuss AI."
                       ^^^
                  gap — no token, no timestamp
```

This means an LLM reasoning purely over the transcript **cannot detect or timestamp filler regions**. AutoCut's hybrid architecture addresses this by pairing transcript-level semantic reasoning with audio-level VAD signals — the VAD catches what Whisper silently drops.

---

## ⚙️ Installation

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally *(for semantic features)*
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

# 4. (Optional) Pull the Gemma 3 model for semantic editing
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

### Gradio UI

```bash
python app.py
```

Open `http://localhost:7860` in your browser. Upload a video, review the detected segments, and export the trimmed result.

> ⚠️ The semantic LLM edit approval flow is still being wired up. Currently the UI supports acoustic-based editing (silence + VAD). Semantic cut review coming soon.

### Programmatic *(acoustic pipeline)*

```python
from autocut import pipeline

result = pipeline.run(
    input_video="lecture.mp4",
    output_video="lecture_edited.mp4",
    whisper_model="small",    # base / small / medium / large-v3
    min_silence_ms=500,
)

print(result.edit_decisions)  # list of (start_s, end_s, reason) tuples
```

---

## 🔄 Development Iterations

AutoCut progressed through four architectural stages, each driven by concrete failure modes:

```
Iteration 1 — Silence Detection
  ✅ Removes dead air
  ❌ Fillers (umm, uh) have audio energy — not caught
  ❌ Meaningful dramatic pauses also removed

Iteration 2 — Voice Activity Detection (Silero VAD)
  ✅ More robust to background noise
  ✅ Better speech boundary accuracy
  ❌ Correctly classifies fillers as speech — no editing benefit

Iteration 3 — Speech Recognition (Faster-Whisper)
  ✅ Word-level timestamps
  ⚠️  Key finding: Whisper suppresses fillers → audio-transcript mismatch
      LLMs cannot reason about content that isn't in the transcript

Iteration 4 — Semantic LLM Editing  ← current focus
  🔄 Gemma 3 integrated, prompting transcript chunks for edit decisions
  🔄 Timestamp reconstruction (semantic decision → frame range) in progress
  📋 Hybrid VAD + ASR filler detection planned next
```

---

## 📊 Project Status

| Feature | Status |
|---|---|
| Faster-Whisper integration | ✅ Done |
| Word-level timestamp extraction | ✅ Done |
| Silero VAD integration | ✅ Done |
| Silence-removal baseline | ✅ Done |
| Semantic chunk generation | ✅ Done |
| Gemma 3 via Ollama — integration | ✅ Done |
| Gemma 3 — reliable edit decisions | 🔄 In Progress |
| Timestamp reconstruction (semantic → frame) | 🔄 In Progress |
| Automated video reconstruction pipeline | 🔄 In Progress |
| Gradio UI | 🔄 In Progress |
| Semantic confidence scoring | 🔄 In Progress |
| Forced alignment (filler detection) | 📋 Planned |
| Multi-speaker editing | 📋 Planned |

---

## 🗺️ Roadmap

**Short-term**
- Complete semantic timestamp reconstruction
- Gradio UI with per-cut approve/reject and timeline visualisation
- End-to-end automated rendering pipeline

**Medium-term**
- Forced alignment (Montreal Forced Aligner) for filler detection independent of transcript
- Confidence-based edit scoring — let users dial the aggressiveness threshold

**Long-term**
- Multi-speaker support
- Learning from user feedback (approved/rejected cuts → fine-tuning)
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
│   ├── llm.py              # Gemma 3 / Ollama interface  (WIP)
│   ├── editor.py           # FFmpeg reconstruction
│   └── align.py            # Timestamp mapping  (WIP)
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

- **[Faster-Whisper](https://github.com/SYSTRAN/faster-whisper)** — CTranslate2-optimised Whisper for fast local ASR with word timestamps
- **[Silero VAD](https://github.com/snakers4/silero-vad)** — Lightweight ML-based voice activity detection
- **[Gemma 3 via Ollama](https://ollama.com/library/gemma3)** — Local LLM for semantic edit reasoning *(in progress)*
- **[FFmpeg](https://ffmpeg.org)** — Frame-accurate video trimming and reconstruction
- **[Gradio](https://gradio.app)** — Rapid UI for interactive edit review *(in progress)*

---

## 👤 Author

**Kutraleeswaran Nattamai Harikrishnan**
B.Tech Aerospace Engineering + IDDD Robotics — IIT Madras

---

<div align="center">
<sub>Built with 🤖 local-first AI — no cloud APIs, no subscription fees, no data leaving your machine.</sub>
</div>

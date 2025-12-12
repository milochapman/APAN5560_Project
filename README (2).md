# APAN5560 Movie Poster Generator

_A full pipeline for generating multi-variant movie posters from text summaries using fine-tuned NLP models and HuggingFace SDXL._

## Overview

This project implements an end-to-end **movie poster campaign generation system** for APAN 5560.  
Given a short movie summary, the system:

1. **Analyzes the narrative** using a fine-tuned **DistilBERT genre classifier**
2. Extracts **mood, genre, keywords, and visual style cues**
3. Generates **multiple cinematic prompt variants**
4. Produces **high-quality poster images** using HuggingFace SDXL
5. Returns a structured response through a **FastAPI service**

---

## System Architecture

```
User Summary
     │
     ▼
Text Analysis (Fine-Tuned DistilBERT)
     │  → genre, mood, keywords
     ▼
Prompt Generator
     │  → multiple template-based variants
     ▼
Poster Generator (HuggingFace SDXL)
     │  via InferenceClient → base64 PNG
     ▼
FastAPI Output (single or multi-poster campaign)
```

---

## Model Download (Fine-Tuned DistilBERT)

The fine-tuned classifier is too large to host on GitHub, so it is stored externally.

### **Download the full model here:**

🔗 **Google Drive:** https://drive.google.com/drive/folders/1RG3DJukukk2-JKQUz7oKN7MKN4N5Tu_G?usp=sharing

Place the downloaded folder into:

```
models/genre_classifier_distilbert/
```

Your directory should look like:

```
models/
└── genre_classifier_distilbert/
    ├── config.json
    ├── model.safetensors
    ├── tokenizer.json
    ├── tokenizer_config.json
    └── special_tokens_map.json
```

---

## Fine-Tuned Model

We fine-tuned:

```
distilbert-base-uncased
```

on the **IMDB Genres dataset (`jquigl/imdb-genres`)** to classify movie summaries into 16 genres.

### Training Setup

- 60,000 training samples
- 8,000 validation, 8,000 test
- Batch size: 32
- Max sequence length: 128
- 1 epoch (optimized for Apple M-series GPU via MPS)

### Performance (Test Set)

| Metric            | Score                |
| ----------------- | -------------------- |
| Accuracy          | ~0.387               |
| Macro F1          | ~0.315               |
| Strongest classes | War, Crime, Thriller |

---

## Image Generation — HuggingFace SDXL

Posters are produced using **HuggingFace InferenceClient**:

```python
from huggingface_hub import InferenceClient

client = InferenceClient(api_key=HF_API_KEY)
image = client.text_to_image(
    prompt,
    model="stabilityai/stable-diffusion-xl-base-1.0"
)
```

Outputs are encoded as base64 PNG strings for easy transport.

---

## Running Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create `.env`

```
IMAGE_PROVIDER=huggingface
HF_API_KEY=YOUR_HF_KEY
HF_MODEL_ID=stabilityai/stable-diffusion-xl-base-1.0
```

### 3. Start API

```bash
uvicorn app.main:app --reload
```

### 4. API Docs

```
http://127.0.0.1:8000/docs
```

---

## Docker Deployment

### Build

```bash
docker build -t movie-poster-generator .
```

### Run

```bash
docker run --env-file .env -p 8000:8000 movie-poster-generator
```

---

## Downloading Posters

After generating prompts and receiving the download links from the API, you can save the posters using the helper script.

### Save Posters

```bash
# Open a new terminal window
python save_poster.py
```

This script will:

- Read the returned image URLs
- Download each generated poster
- Save them automatically into the `posters/` directory

### 📁 Output Location

All posters will be saved in:

```
posters/
```

---

## 🧪 Example Request

```json
{
  "summary": "In a near-future metropolis drowning in neon lights, an unemployed engineer discovers a device that can record human memories. As powerful corporations hunt her down, she must decide whether to expose a secret that could collapse the entire city.",
  "style_hint": "cyberpunk, neon glow, cinematic atmosphere, dark futuristic aesthetic"
}
```

---

## 📁 Project Structure

```
.
├── app/
│   ├── main.py
│   ├── poster_generator.py
│   ├── text_analysis.py
│   ├── prompt_generator.py
│   ├── schemas.py
│   └── config.py
├── models/
│   └── genre_classifier_distilbert/
├── train_text_classifier.py
├── save_campaign_posters.py
├── save_poster.py
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🌟 Highlights

- End-to-end multimodal generation
- Fine-tuned NLP classifier guiding SDXL outputs
- Template-driven prompt engineering
- Highly consistent poster variants
- Full FastAPI backend + Docker deployment

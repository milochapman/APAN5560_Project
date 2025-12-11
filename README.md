# APAN5560 Movie Poster Generator
*A full pipeline for generating multi-variant movie posters from text summaries using fine-tuned NLP models and HuggingFace SDXL.*

## 📌 Overview

This project implements an end-to-end **movie poster campaign generation system** for APAN 5560.  
Given a short movie summary, the system:

1. **Analyzes the narrative** using a **fine-tuned DistilBERT genre classifier**  
2. Extracts **title, tagline, moods, keywords, color palettes**  
3. Generates **multiple cinematic prompt variants**  
4. Produces **high-quality poster images** using **HuggingFace SDXL** via `InferenceClient`  
5. Returns a structured response through a **FastAPI service**

This project demonstrates:

- Fine-tuning a transformer model on a public dataset  
- Designing a prompt generation pipeline  
- Integrating HuggingFace text-to-image  
- Building an API-based generative application  
- Packaging everything into a **Docker-deployable system**

---

## 🧠 System Architecture

```
User Summary
     │
     ▼
Text Analysis (Fine-Tuned DistilBERT)
     │  genre, mood, keywords
     ▼
Prompt Generator
     │  multiple variants per movie
     ▼
Poster Generator (HuggingFace SDXL)
     │  via InferenceClient → base64 images
     ▼
FastAPI Response (single or multi-poster campaign)
```

---

## 🧪 Fine-Tuned Model

We fine-tuned:

```
distilbert-base-uncased
```

on the **IMDB Genres dataset (`jquigl/imdb-genres`)** to classify movie summaries into 16 genres.

### Training setup
- 60,000 training samples  
- 8,000 validation, 8,000 test  
- Batch size: 32  
- Max length: 128  
- Epochs: 1 (optimized for Apple M-series GPU via MPS)

### Performance (test set)

| Metric | Score |
|--------|--------|
| Accuracy | ~0.387 |
| Macro F1 | ~0.32 |
| Best classes | War, Crime, Thriller (~0.50 F1) |

The fine-tuned model is stored in:

```
models/genre_classifier_distilbert/
```

---

## 🎨 Image Generation — HuggingFace SDXL (InferenceClient)

The system uses **HuggingFace’s InferenceClient** to generate images:

```python
from huggingface_hub import InferenceClient

client = InferenceClient(api_key=HF_API_KEY)
image = client.text_to_image(prompt, model="stabilityai/stable-diffusion-xl-base-1.0")
```

Outputs are returned as base64 PNG data URLs.

---

## 🚀 Running Locally

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

### 4. Open Docs
```
http://127.0.0.1:8000/docs
```

---

## 🐳 Docker Deployment

### Build
```bash
docker build -t movie-poster-generator .
```

### Run
```bash
docker run --env-file .env -p 8000:8000 movie-poster-generator
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
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🌟 Highlights

- Full multimodal generation pipeline  
- Fine-tuned transformer model  
- Clean modular FastAPI architecture  
- HuggingFace SDXL image generation  
- Reproducible Docker deployment  

---

## 🔮 Future Work

- Image scoring (CLIP)  
- LoRA fine-tuning  
- Multi-poster layout generation  
- Reinforcement learning for prompt optimization  

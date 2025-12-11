# Movie Poster Generation System  
APAN 5560: Applied Generative AI  
Columbia University – Final Project

## Overview
This project implements an end-to-end movie poster generation system using Generative AI techniques, including text analysis, structured prompt generation, and image synthesis via the Hugging Face Inference API. The system expands a basic prompt-to-image workflow into a more comprehensive pipeline that automates style adaptation, prompt engineering, and multi-format campaign asset creation (theatrical poster, streaming thumbnail, and social teaser).

The contribution beyond off-the-shelf APIs is the introduction of automated text analysis, structured template construction, multi-variant prompt generation, and an optional fine-tuned DistilBERT model used for genre classification. The project includes a fully containerized FastAPI server that generates posters through accessible API endpoints.

## System Architecture
The full architecture consists of:

1. User text input describing the movie concept.
2. Text analysis to extract key themes and stylistic signals.
3. A structured prompt template layer.
4. A multi-variant prompt builder used to create poster formats for theatrical, streaming, and social media.
5. Image generation using Hugging Face's text-to-image models.
6. An API layer deployed in FastAPI and containerized in Docker.

## Directory Structure
```
APAN5560-project/
│
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── config.py
│   ├── text_analysis.py
│   ├── prompt_generator.py
│   ├── poster_generator.py
│   └── __init__.py
│
├── models/
│   └── genre_classifier_distilbert/
│       ├── config.json
│       ├── tokenizer.json
│       ├── tokenizer_config.json
│       ├── special_tokens_map.json
│       ├── vocab.txt
│       └── model.safetensors (excluded from Git; download link below)
│
├── tests/
│   └── test_api.py
│
├── generate_all_poster.py
├── save_poster.py
├── train_text_classifier.py
├── test_hf.py
├── dockerfile
├── requirements.txt
├── .gitignore
└── README.md
```

## Model Download
Download:
https://drive.google.com/file/d/1NHs1HgpbgMFi5ajGVWlTbRQvtHd96Zp8/view?usp=sharing

Place at:
```
APAN5560-project/models/genre_classifier_distilbert/model.safetensors
```

## Local Setup
```
git clone https://github.com/milochapman/APAN5560_Project.git
cd APAN5560_Project

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env`:
```
HF_API_KEY=your_key_here
```

Run:
```
uvicorn app.main:app --reload --port 8000
```

## Docker
```
docker build -t movie-poster-api .
docker run --env-file .env -p 8000:8000 movie-poster-api
```

## Endpoints
```
GET /health
POST /generate_poster
POST /generate_campaign
```

## Batch Tools
```
python save_poster.py
python generate_all_poster.py
```

## Fine-Tuning
Includes DistilBERT classifier, training script, and integration.

## Rubric Compliance
Meets all requirements: topic selection, Dockerized API, organized code, comprehensive documentation, and clear presentation.

## Attribution
Hugging Face API used for inference. DistilBERT licensed under Apache 2.0.

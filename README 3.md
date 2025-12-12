# APAN 5560 – Generative AI Movie Poster Campaign Generator

## 1. Project Overview

This project implements a FastAPI-based Generative AI system for creating movie poster marketing campaigns using structured prompt engineering. The system demonstrates applied concepts from APAN 5560, including API design, prompt modularization, reproducibility, and separation of concerns in machine learning systems.

The project supports generating multi-format campaign assets such as theatrical posters, streaming thumbnails, and social media teaser images. Image generation and image persistence are intentionally decoupled to reflect real-world ML pipeline design.

## 2. System Design and Workflow

The system consists of two independent stages.

**Stage 1: Image Generation (FastAPI + Swagger UI)**  
Users interact with the system through Swagger UI. Structured requests containing `summary` and `style_hint` fields are submitted. The API generates one or more images and returns them encoded as base64 data URLs in a JSON response.

**Stage 2: Image Persistence (save_poster.py)**  
A standalone Python utility responsible only for decoding and saving images from an existing API response. The script does not call the API, define prompts, or hard-code any movie styles.

## 3. Directory Structure

```text
APAN5560-project/
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── config.py
│   ├── text_analysis.py
│   ├── prompt_generator.py
│   ├── poster_generator.py
│   └── __init__.py
├── models/
│   └── genre_classifier_distilbert/
│       ├── config.json
│       ├── tokenizer.json
│       ├── tokenizer_config.json
│       ├── special_tokens_map.json
│       ├── vocab.txt
│       └── model.safetensors (excluded from Git; downloaded at runtime if required)
├── tests/
│   └── test_api.py
├── save_poster.py
├── generate_all_poster.py
├── requirements.txt
├── Dockerfile
├── README.md
├── outputs/                 # Generated images (created at runtime)
└── response_*.json          # Swagger response JSON files (user-generated)
```

## 4. Recommended Execution Path (For Grading)

Docker is the recommended execution method for instructors and TAs, as it provides a consistent and reproducible environment.

### Build the Docker Image

```
docker build -t movie-poster-api .
```

### Run the Container

```
docker run -p 8000:8000 movie-poster-api
```

### Open Swagger UI

```
http://127.0.0.1:8000/docs
```

## 5. Generating a Movie Poster Campaign

Using Swagger UI, locate the endpoint:

```
POST /generate_campaign
```

Submit a structured request containing both content and style information.

Example request:

```json
{
  "summary": "MOVIE TITLE (use exactly): TRANSFORMERS: STEEL REBORN
TAGLINE (use exactly): THE WAR EVOLVES
BADGE: FILMED FOR IMAX

Design a Transformers movie poster campaign featuring Cybertronian robots with industrial mechanical realism. Optimus Prime is the central hero mid-transformation in a collapsing modern city.",
  "style_hint": "Industrial sci-fi action, metallic realism, IMAX blockbuster poster. Avoid space opera aesthetics."
}
```

Upon execution, the API returns a JSON response containing one or more images encoded as `data:image/png;base64,...`.

## 6. Saving Generated Images Locally

The `save_poster.py` script does not generate images and does not call the API. Its sole responsibility is to decode and persist images from an existing API response.

### Steps

1. After executing the request in Swagger UI, copy the full response body.
2. Save the response as a JSON file in the project root directory (e.g., `response_transformers.json`).
3. Run the save utility:

```
python3 save_poster.py --input response_transformers.json --outdir outputs --prefix transformers
```

The decoded images will be written to the `outputs` directory.

## 7. Local Development (Optional)

For local execution without Docker:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Then open:

```
http://127.0.0.1:8000/docs
```

## 8. Design Rationale

The project emphasizes separation of concerns, reproducibility, and transparent system behavior. Swagger UI supports interactive prompt experimentation, while Docker ensures consistent grading environments.

## 9. Notes for Instructors and TAs

- Docker is the preferred execution method.
- The system is stateless and requires no external API keys.
- `save_poster.py` does not influence generation results.
- All outputs are reproducible using the provided instructions.

## 10. License

Academic use only – APAN 5560 coursework.

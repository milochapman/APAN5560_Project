APAN 5560 – Generative AI Movie Poster Campaign Generator

1. Project Overview

This project implements a FastAPI-based Generative AI system for creating movie poster marketing campaigns using structured prompt engineering. The system demonstrates practical concepts from APAN 5560, including API design, prompt modularization, reproducibility, and separation of concerns in applied machine learning systems.

The project supports generating multi-format campaign assets, including theatrical posters, streaming thumbnails, and social media teaser images. Image generation and image persistence are intentionally decoupled to reflect real-world ML pipeline design.

2. System Design and Workflow

The system consists of two independent stages.

Stage 1: Image Generation (FastAPI + Swagger UI)
Users interact with the system through Swagger UI. Structured requests containing summary and style_hint fields are submitted. The API generates one or more images and returns them encoded as base64 data URLs in a JSON response.

Stage 2: Image Persistence (save_poster.py)
A standalone Python utility that decodes and saves images from an existing API response. The script does not call the API, define prompts, or hard-code any movie styles.

3. Project Structure

APAN5560-project/
app/                    FastAPI application source code
save_poster.py          Utility script for saving generated images
requirements.txt        Python dependencies
Dockerfile              Docker configuration
README.md               Project documentation
outputs/                Generated images (created at runtime)
response_*.json         Swagger response files

4. Recommended Execution Path (For Grading)

Docker is the recommended execution method for instructors and TAs.

Build the Docker image:
docker build -t movie-poster-api .

Run the container:
docker run -p 8000:8000 movie-poster-api

Open Swagger UI:
http://127.0.0.1:8000/docs

5. Generating a Movie Poster Campaign

Use POST /generate_campaign in Swagger UI with a structured request.

Example request:

{
  "summary": "MOVIE TITLE (use exactly): TRANSFORMERS: STEEL REBORN
TAGLINE (use exactly): THE WAR EVOLVES
BADGE: FILMED FOR IMAX

Design a Transformers movie poster campaign featuring Cybertronian robots with industrial mechanical realism.",
  "style_hint": "Industrial sci-fi action, metallic realism, IMAX blockbuster poster."
}

The API returns a JSON response containing one or more images encoded as base64 data URLs.

6. Saving Generated Images Locally

The save_poster.py script only saves images. It does not generate images or call the API.

Step 1. Save the Swagger response body as a JSON file, for example:
response_transformers.json

Step 2. Run the save utility:
python3 save_poster.py --input response_transformers.json --outdir outputs --prefix transformers

The decoded images will be written to the outputs directory.

7. Local Development (Optional)

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

8. Design Rationale

The project emphasizes separation of concerns, reproducibility, and transparent system behavior. Swagger UI supports interactive prompt experimentation, while Docker ensures consistent grading environments.

9. Notes for Instructors and TAs

Docker is the preferred execution method. The system is stateless, requires no API keys, and produces deterministic outputs given identical inputs. The save_poster.py script does not influence generation results.

10. License

Academic use only – APAN 5560 coursework.

APAN 5560 – Generative AI Movie Poster Campaign Generator

This project demonstrates a FastAPI-based Generative AI system for creating movie poster marketing campaigns using structured prompt engineering. The system is designed with clear separation of responsibilities to ensure reproducibility, transparency, and ease of grading.

----------------------------------------------------------------
Project Overview
----------------------------------------------------------------

The project consists of two independent stages:

1. Image Generation (FastAPI + Swagger UI)
   - Users interact with the API via Swagger UI.
   - Structured prompts (summary and style_hint) are submitted.
   - The API returns generated images encoded as base64 strings.

2. Image Persistence (save_poster.py)
   - A standalone Python utility.
   - Responsible only for decoding and saving images from an API response.
   - Does not generate images or contain any hard-coded movie styles.

This separation ensures that prompt experimentation and image storage are decoupled, mirroring real-world ML system design.

----------------------------------------------------------------
Project Structure
----------------------------------------------------------------

APAN5560-project/
├── app/                    # FastAPI application
├── save_poster.py          # Utility for saving images from API response JSON
├── requirements.txt
├── Dockerfile
├── README.md
├── outputs/                # Generated images (created at runtime)
└── response_*.json         # Swagger response files (user-generated)

----------------------------------------------------------------
Recommended Execution Path (For Grading)
----------------------------------------------------------------

Docker is the recommended execution method for grading, as it provides a consistent and reproducible environment.

1. Build the Docker image

docker build -t movie-poster-api .

2. Run the container

docker run -p 8000:8000 movie-poster-api

3. Open Swagger UI

http://127.0.0.1:8000/docs

----------------------------------------------------------------
Generating a Movie Poster Campaign
----------------------------------------------------------------

Using Swagger UI, locate POST /generate_campaign and submit a structured request. Example:

{
  "summary": "MOVIE TITLE (use exactly): TRANSFORMERS: STEEL REBORN
TAGLINE (use exactly): THE WAR EVOLVES
BADGE: FILMED FOR IMAX

Design a Transformers movie poster campaign featuring Cybertronian robots with industrial mechanical realism. Optimus Prime is the central hero mid-transformation in a collapsing modern city.",
  "style_hint": "Industrial sci-fi action, metallic realism, IMAX blockbuster poster. Avoid space opera aesthetics."
}

Upon execution, the API returns a JSON response containing one or more images encoded as data URLs.

----------------------------------------------------------------
Saving Generated Images Locally
----------------------------------------------------------------

The save_poster.py script is intentionally limited in scope. It does not call the API or define any movie styles.

To persist generated images:

1. After executing the request in Swagger UI, copy the full response body.
2. Save the response as a JSON file in the project root directory.
   Example: response_transformers.json

3. Run the save utility:

python3 save_poster.py --input response_transformers.json --outdir outputs --prefix transformers

The decoded images will be written to the outputs directory.

----------------------------------------------------------------
Local Development (Optional)
----------------------------------------------------------------

For local execution without Docker:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

Then open http://127.0.0.1:8000/docs.

----------------------------------------------------------------
Design Rationale
----------------------------------------------------------------

- Separation of generation and persistence aligns with real-world ML pipelines.
- No hard-coded prompts or movie styles are present in the saving utility.
- Swagger UI enables transparent prompt experimentation.
- Docker ensures grading reproducibility across environments.

----------------------------------------------------------------
Notes for Instructors and TAs
----------------------------------------------------------------

- Docker is the preferred execution method.
- The system is stateless and deterministic given the same prompts.
- save_poster.py is a pure utility and does not influence generation results.
- No API keys or external services are required.

Academic use only – APAN 5560 coursework.
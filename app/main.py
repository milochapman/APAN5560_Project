from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .schemas import (
    PosterRequest,
    PosterResponse,
    CampaignResponse,
    PosterVariant,
)
from .poster_generator import generate_poster, generate_images_for_campaign
from .text_analysis import analyze_summary
from .prompt_generator import generate_prompts

app = FastAPI(title="Movie Poster Campaign System", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate_poster", response_model=PosterResponse)
def generate(request: PosterRequest):
    """
    Backwards-compatible single-poster endpoint.
    """
    try:
        return generate_poster(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate_campaign", response_model=CampaignResponse)
def generate_campaign(request: PosterRequest):
    """
    Full campaign endpoint:

    1) Text Analysis (finetuned classifier + rules) -> PosterAnalysis
    2) Prompt Generator -> multiple prompt variants
    3) Image Generation -> multiple posters
    4) Return all posters
    """
    try:
        # Step 1: Text analysis
        analysis = analyze_summary(request.summary, request.style_hint)

        # Step 2: Prompt generator
        prompt_dicts = generate_prompts(request.summary, analysis, request.style_hint)

        # Step 3: Image generation
        images = generate_images_for_campaign(prompt_dicts, num_images_per_variant=1)

        variants: list[PosterVariant] = []
        for idx, img in enumerate(images):
            variants.append(
                PosterVariant(
                    id=idx,
                    variant=img["variant"],
                    prompt=img["prompt"],
                    image_url=img["image_url"],
                )
            )

        return CampaignResponse(
            title=analysis.title,
            tagline=analysis.tagline,
            genre=analysis.genre,
            mood=analysis.mood,
            color_palette=analysis.color_palette,
            visual_style_keywords=analysis.visual_style_keywords,
            variants=variants,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

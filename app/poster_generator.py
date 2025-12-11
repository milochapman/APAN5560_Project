import base64
from typing import Literal
import io

from openai import OpenAI
from huggingface_hub import InferenceClient

from .config import settings
from .schemas import PosterRequest, PosterResponse


def build_poster_prompt(request: PosterRequest) -> str:
    base = (
        "Movie poster, cinematic composition, dramatic lighting, high detail, 4k. "
        'Design a poster for a movie with the following description: "{summary}". '
        "Include a central character and bold typography."
    )
    if request.style_hint:
        base += f" The style should feel {request.style_hint}."
    return base.format(summary=request.summary)


# ---------- OpenAI ----------


def _generate_with_openai(prompt: str) -> PosterResponse:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY not set, IMAGE_PROVIDER=openai")

    client = OpenAI(api_key=settings.openai_api_key)

    result = client.images.generate(
        model=settings.image_model,
        prompt=prompt,
        size=settings.image_size,
        n=1,
    )
    url = result.data[0].url

    return PosterResponse(image_url=url, prompt=prompt)


# ---------- Hugging Face (HF Inference API, via InferenceClient) ----------


def _hf_client() -> InferenceClient:

    if not settings.hf_api_key:
        raise RuntimeError("HF_API_KEY not set, IMAGE_PROVIDER=huggingface")

    return InferenceClient(api_key=settings.hf_api_key)


def _generate_with_hf(prompt: str) -> PosterResponse:
    client = _hf_client()

    image = client.text_to_image(
        prompt=prompt,
        model=settings.hf_model,
    )

    # Encode image to base64 data URL (PNG)
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    data_url = f"data:image/png;base64,{b64}"

    return PosterResponse(image_url=data_url, prompt=prompt)


# ---------- Public entry ----------


def generate_poster(request: PosterRequest) -> PosterResponse:
    prompt = build_poster_prompt(request)

    provider: Literal["openai", "huggingface"] = (
        "huggingface"
        if settings.image_provider.lower() == "huggingface"
        else "openai"
    )

    if provider == "openai":
        return _generate_with_openai(prompt)
    else:
        return _generate_with_hf(prompt)


def generate_images_for_campaign(
    prompts: list[dict],
    num_images_per_variant: int = 1
) -> list[dict]:
    """
    Generate images for each prompt in a campaign.
    Returns a flat list of {"variant", "prompt", "image_url"}.
    """
    images: list[dict] = []

    provider: Literal["openai", "huggingface"] = (
        "huggingface"
        if settings.image_provider.lower() == "huggingface"
        else "openai"
    )

    openai_client = None
    hf_client = None
    if provider == "openai":
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY not set, IMAGE_PROVIDER=openai")
        openai_client = OpenAI(api_key=settings.openai_api_key)
    else:
        hf_client = _hf_client()

    for item in prompts:
        variant = item["variant"]
        prompt = item["prompt"]

        for _ in range(num_images_per_variant):
            if provider == "openai":
                result = openai_client.images.generate(
                    model=settings.image_model,
                    prompt=prompt,
                    size=settings.image_size,
                    n=1,
                )
                image_url = result.data[0].url
            else:
                image = hf_client.text_to_image(
                    prompt=prompt,
                    model=settings.hf_model,
                )
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
                image_url = f"data:image/png;base64,{b64}"

            images.append(
                {
                    "variant": variant,
                    "prompt": prompt,
                    "image_url": image_url,
                }
            )

    return images
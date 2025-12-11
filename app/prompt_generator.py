from __future__ import annotations

from typing import List, Dict

from .schemas import PosterAnalysis


def build_poster_prompt(
    summary: str,
    analysis: PosterAnalysis,
    variant: str,
    extra_style_hint: str | None = None,
) -> str:
    base = (
        f"Movie poster, {variant} key art, cinematic composition, dramatic lighting, high detail, 4k. "
        f"Genre: {analysis.genre}. Mood: {analysis.mood}. "
        f"Color palette: {analysis.color_palette}. "
        f"Visual style: {', '.join(analysis.visual_style_keywords)}. "
        f'Title text on poster: \"{analysis.title}\". '
        f'Tagline on the poster: \"{analysis.tagline}\". '
        f"Design a poster for the following movie summary: {summary}. "
    )
    if extra_style_hint:
        base += f"The overall style should feel {extra_style_hint}."
    return base


def generate_prompts(
    summary: str,
    analysis: PosterAnalysis,
    extra_style_hint: str | None = None,
) -> List[Dict]:
    """
    Generate multiple prompt variants (theatrical, streaming thumbnail, social teaser).
    """
    variants = [
        "theatrical poster",
        "streaming thumbnail",
        "social media teaser",
    ]
    prompts = []
    for v in variants:
        prompt = build_poster_prompt(summary, analysis, v, extra_style_hint)
        prompts.append({"variant": v, "prompt": prompt})
    return prompts

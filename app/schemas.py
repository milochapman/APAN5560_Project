from pydantic import BaseModel, Field
from typing import List, Optional


class PosterRequest(BaseModel):
    summary: str = Field(..., description="Movie plot summary or keywords")
    style_hint: Optional[str] = Field(
        default=None,
        description="Optional extra style hint for the campaign",
    )


class PosterResponse(BaseModel):
    image_url: str
    prompt: str


class PosterAnalysis(BaseModel):
    title: str
    tagline: str
    genre: str
    mood: str
    color_palette: str
    visual_style_keywords: List[str]


class PosterVariant(BaseModel):
    id: int
    variant: str
    prompt: str
    image_url: str


class CampaignResponse(BaseModel):
    title: str
    tagline: str
    genre: str
    mood: str
    color_palette: str
    visual_style_keywords: List[str]
    variants: List[PosterVariant]

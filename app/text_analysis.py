from __future__ import annotations

import os
import re

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from .schemas import PosterAnalysis

# Model directory produced by train_text_classifier.py
MODEL_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "models",
    "genre_classifier_distilbert",
)

_tokenizer = None
_model = None
_id2label = None


def _load_classifier():
    """Lazy load finetuned classifier."""
    global _tokenizer, _model, _id2label
    if _tokenizer is not None and _model is not None:
        return

    if not os.path.isdir(MODEL_DIR):
        raise RuntimeError(
            f"Genre classifier not found at {MODEL_DIR}. "
            "Please run `python train_text_classifier.py` first."
        )

    _tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    _model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    _model.eval()

    id2label = _model.config.id2label
    # HF config may use string keys: {"0": "Action", "1": "Drama", ...}
    if isinstance(id2label, dict):
        id2label = {int(k): v for k, v in id2label.items()}
    _id2label = id2label


def predict_genre(summary: str) -> str:
    """Predict a primary genre label for the given movie summary."""
    _load_classifier()
    inputs = _tokenizer(
        summary,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256,
    )
    with torch.no_grad():
        outputs = _model(**inputs)
        logits = outputs.logits
        pred_id = int(torch.argmax(logits, dim=-1).item())
    return _id2label[pred_id]


# ---------- simple rule-based mappings based on genre ----------

def _normalize_genre(genre: str) -> str:
    return genre.lower().strip()


def _infer_mood(genre: str) -> str:
    g = _normalize_genre(genre)
    if "horror" in g:
        return "dark and suspenseful"
    if "thriller" in g or "mystery" in g or "crime" in g:
        return "tense and gripping"
    if "comedy" in g:
        return "light-hearted and playful"
    if "romance" in g:
        return "romantic and emotional"
    if "action" in g or "adventure" in g:
        return "dynamic and energetic"
    if "sci" in g or "fantasy" in g:
        return "futuristic and imaginative"
    if "documentary" in g:
        return "serious and realistic"
    return "dramatic"


def _infer_color_palette(genre: str) -> str:
    g = _normalize_genre(genre)
    if "horror" in g or "thriller" in g or "crime" in g:
        return "dark reds, deep blacks and muted blues"
    if "comedy" in g or "family" in g:
        return "bright and warm yellows, oranges and light blues"
    if "romance" in g:
        return "soft pinks, warm reds and gentle purples"
    if "action" in g or "adventure" in g:
        return "high-contrast oranges and blues"
    if "sci" in g or "fantasy" in g:
        return "cool neon blues, purples and cyans"
    if "documentary" in g:
        return "natural, muted earth tones and soft blues"
    return "balanced warm and cool tones"


def _infer_style_keywords(genre: str):
    g = _normalize_genre(genre)
    if "horror" in g:
        return ["gritty", "high contrast", "moody lighting", "distressed textures"]
    if "thriller" in g or "crime" in g or "mystery" in g:
        return ["noir-inspired", "shadowy", "dramatic lighting", "cinematic close-up"]
    if "comedy" in g:
        return ["colorful", "bold typography", "playful composition"]
    if "romance" in g:
        return ["soft focus", "glowing highlights", "gentle gradients"]
    if "action" in g or "adventure" in g:
        return ["dynamic composition", "motion blur", "epic scale"]
    if "sci" in g or "fantasy" in g:
        return ["futuristic", "high contrast", "neon glow", "surreal elements"]
    if "documentary" in g:
        return ["minimalist", "photographic", "clean layout"]
    return ["cinematic", "atmospheric", "high contrast"]


def _make_title(summary: str, genre: str) -> str:
    """
    Simple heuristic title generator from summary:
    - Take first 3–6 words, title-case them.
    - Fallback to "Untitled <Genre> Film" if too short.
    """
    clean = re.sub(r'["\n\r]', " ", summary).strip()
    words = clean.split()
    if len(words) >= 3:
        base = " ".join(words[: min(6, len(words))])
        title = base.title()
    elif words:
        title = " ".join(words).title()
    else:
        title = ""

    title = title[:60].strip()
    if not title:
        title = f"Untitled {genre} Film"
    return title


def _make_tagline(genre: str, mood: str) -> str:
    """
    Generate a simple tagline based on genre + mood.
    """
    g = _normalize_genre(genre)
    core = "story"

    if "horror" in g:
        core = "nightmare"
    elif "thriller" in g or "crime" in g:
        core = "game of secrets"
    elif "comedy" in g:
        core = "ride of laughter"
    elif "romance" in g:
        core = "journey of hearts"
    elif "action" in g or "adventure" in g:
        core = "mission you'll never forget"
    elif "sci" in g or "fantasy" in g:
        core = "world beyond imagination"

    return f"A {mood} {core}."


def analyze_summary(summary: str, style_hint: str | None = None) -> PosterAnalysis:
    """
    Full Text Analysis pipeline WITHOUT OpenAI:

    1) Predict genre using finetuned classifier.
    2) Use simple rules (based on genre) to derive:
       mood, color palette, visual style keywords, title, tagline.
    """
    genre = predict_genre(summary)
    mood = _infer_mood(genre)
    color_palette = _infer_color_palette(genre)
    visual_style_keywords = _infer_style_keywords(genre)
    title = _make_title(summary, genre)
    tagline = _make_tagline(genre, mood)

    return PosterAnalysis(
        title=title,
        tagline=tagline,
        genre=genre,
        mood=mood,
        color_palette=color_palette,
        visual_style_keywords=visual_style_keywords,
    )

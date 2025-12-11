# app/config.py

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Which image backend to use: "openai" or "huggingface"
    image_provider: str = Field("huggingface", env="IMAGE_PROVIDER")

    # OpenAI (optional – not used by default)
    openai_api_key: str | None = Field(default=None, env="OPENAI_API_KEY")
    image_model: str = "gpt-image-1"
    image_size: str = "1024x1024"

    # Hugging Face Inference API (Stable Diffusion XL)
    hf_api_key: str | None = Field(default=None, env="HF_API_KEY")
    # Default to SDXL base 1.0 as requested
    hf_model: str = "stabilityai/stable-diffusion-xl-base-1.0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

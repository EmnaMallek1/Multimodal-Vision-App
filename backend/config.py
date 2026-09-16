from pydantic_settings import BaseSettings
import torch


class Settings(BaseSettings):
    clip_model: str = "openai/clip-vit-base-patch32"
    caption_model: str = "Salesforce/blip-image-captioning-base"
    vqa_model: str = "Salesforce/blip-vqa-base"

    cors_origins: list[str] = ["http://localhost:3000"]
    max_image_bytes: int = 10 * 1024 * 1024  # 10 Mo

    class Config:
        env_file = ".env"


settings = Settings()

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
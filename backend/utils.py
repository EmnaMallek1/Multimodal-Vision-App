import io
from PIL import Image, UnidentifiedImageError
from fastapi import HTTPException

from config import settings

#input : the raw binary content of an uploaded image file (e.g. what you get from file.file.read() in a router)
#output : a PIL Image object guaranteed to be in RGB mode, or raises an HTTPException if the image is invalid or too large
def load_image_from_bytes(data: bytes) -> Image.Image:
    if not data:
        raise HTTPException(status_code=400, detail="Fichier vide.")
    if len(data) > settings.max_image_bytes:
        raise HTTPException(status_code=413, detail="Image trop volumineuse (max 10 Mo).")
    try:
        image = Image.open(io.BytesIO(data))
        image.load()
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status_code=400, detail="Fichier image invalide ou corrompu.")
    return image.convert("RGB")

# input : a raw string containing multiple candidate texts writen by the user, separated by newlines
# output : a list of non-empty, stripped candidate texts "cleaned texts"
def parse_candidate_texts(raw_text: str) -> list[str]:
    return [line.strip() for line in raw_text.split("\n") if line.strip()]
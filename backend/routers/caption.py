from fastapi import APIRouter, UploadFile, File

from services.captioner import generate_caption
from utils import load_image_from_bytes
from schemas import CaptionResponse

router = APIRouter(prefix="/api", tags=["caption"])


@router.post("/caption", response_model=CaptionResponse)
def caption(file: UploadFile = File(...)):
    image = load_image_from_bytes(file.file.read())
    return CaptionResponse(caption=generate_caption(image))
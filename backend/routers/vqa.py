from fastapi import APIRouter, UploadFile, File, Form

from services.vqa import answer_question
from utils import load_image_from_bytes
from schemas import VQAResponse

router = APIRouter(prefix="/api", tags=["vqa"])


@router.post("/vqa", response_model=VQAResponse)
def vqa(file: UploadFile = File(...), question: str = Form(...)):
    if not question.strip():
        return VQAResponse(answer="")

    image = load_image_from_bytes(file.file.read())
    answer = answer_question(image, question)
    return VQAResponse(answer=answer)
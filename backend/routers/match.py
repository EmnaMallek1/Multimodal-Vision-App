from fastapi import APIRouter, UploadFile, File, Form

from services.clip_matcher import match_image_to_texts
from utils import load_image_from_bytes, parse_candidate_texts
from schemas import MatchResponse, MatchItem

router = APIRouter(prefix="/api", tags=["match"])


@router.post("/match", response_model=MatchResponse)
def match(file: UploadFile = File(...), texts: str = Form(...)):
    image = load_image_from_bytes(file.file.read())
    candidates = parse_candidate_texts(texts)

    if not candidates:
        return MatchResponse(results=[])

    ranked = match_image_to_texts(image, candidates)
    return MatchResponse(results=[MatchItem(text=t, score=s) for t, s in ranked])
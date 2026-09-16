from pydantic import BaseModel


class CaptionResponse(BaseModel):
    caption: str

class MatchItem(BaseModel):
    text: str
    score: float

class MatchResponse(BaseModel):
    results: list[MatchItem]

class VQARequest:
    pass  # not needed — question arrives as a Form field, not JSON body

class VQAResponse(BaseModel):
    answer: str
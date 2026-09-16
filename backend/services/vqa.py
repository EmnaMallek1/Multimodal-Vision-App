"""
Visual Question Answering using Salesforce's BLIP-VQA model.
"""
import torch
from transformers import BlipForQuestionAnswering, BlipProcessor

from config import settings, DEVICE

MODEL_NAME = settings.vqa_model
_model = None
_processor = None


def load_model():
    """Lazily load and cache the BLIP-VQA model + processor."""
    global _model, _processor
    if _model is None:
        _processor = BlipProcessor.from_pretrained(MODEL_NAME)
        _model = BlipForQuestionAnswering.from_pretrained(MODEL_NAME).to(DEVICE)
        _model.eval()
    return _model, _processor


def answer_question(image, question: str, max_new_tokens: int = 15) -> str:
    """
    Answer a natural-language question about the given image.

    Args:
        image: PIL.Image in RGB mode.
        question: the user's question as a string.
        max_new_tokens: answer length cap.

    Returns:
        A short answer string.
    """
    if not question or not question.strip():
        return ""

    model, processor = load_model()

    inputs = processor(image, question, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        output_ids = model.generate(**inputs, max_new_tokens=max_new_tokens)

    answer = processor.decode(output_ids[0], skip_special_tokens=True)
    return answer.strip()

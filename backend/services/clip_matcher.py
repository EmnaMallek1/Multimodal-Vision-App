"""
Image-text matching using OpenAI's CLIP model.

Given an image and a list of candidate text descriptions, CLIP scores how
well each description matches the image and returns them ranked by
probability.
"""
import torch
from config import settings, DEVICE

from transformers import CLIPModel, CLIPProcessor

MODEL_NAME = settings.clip_model
_model = None
_processor = None


def load_model():
    """Lazily load and cache the CLIP model + processor (module-level singleton)."""
    global _model, _processor
    if _model is None:
        _model = CLIPModel.from_pretrained(MODEL_NAME).to(DEVICE)
        _processor = CLIPProcessor.from_pretrained(MODEL_NAME)
        _model.eval()
    return _model, _processor


def match_image_to_texts(image, candidate_texts: list[str]) -> list[tuple[str, float]]:
    """
    Score each candidate text against the image.

    Args:
        image: PIL.Image in RGB mode.
        candidate_texts: list of strings to compare against the image.

    Returns:
        List of (text, probability) tuples, sorted by probability descending.
    """
    if not candidate_texts:
        return []

    model, processor = load_model()

    inputs = processor(text=candidate_texts, images=image, return_tensors="pt", padding=True).to(DEVICE)

    with torch.no_grad():
        outputs = model(**inputs)
        logits_per_image = outputs.logits_per_image  # shape: [1, num_texts]
        probs = logits_per_image.softmax(dim=1).squeeze(0).tolist()

    ranked = sorted(zip(candidate_texts, probs), key=lambda pair: pair[1], reverse=True)
    return ranked

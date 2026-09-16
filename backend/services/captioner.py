"""
Automatic image captioning using Salesforce's BLIP model.
"""


from config import settings, DEVICE

import torch
from transformers import BlipForConditionalGeneration, BlipProcessor

MODEL_NAME = settings.caption_model
_model = None
_processor = None


def load_model():
    """Lazily load and cache the BLIP captioning model + processor."""
    global _model, _processor
    if _model is None:
        _processor = BlipProcessor.from_pretrained(MODEL_NAME)
        _model = BlipForConditionalGeneration.from_pretrained(MODEL_NAME).to(DEVICE)
        _model.eval()
    return _model, _processor


def generate_caption(image, max_new_tokens: int = 30) -> str:
    """
    Generate a natural-language caption describing the image.

    Args:
        image: PIL.Image in RGB mode.
        max_new_tokens: caption length cap.

    Returns:
        A single caption string.
    """
    model, processor = load_model()

    inputs = processor(image, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        output_ids = model.generate(**inputs, max_new_tokens=max_new_tokens)

    caption = processor.decode(output_ids[0], skip_special_tokens=True)
    return caption.strip()

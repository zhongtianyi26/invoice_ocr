import numpy as np
from paddleocr import PaddleOCR
import os
from pathlib import Path

from app.core.engines.base import OCREngine


PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent.parent.parent
MODELS_DIR = PROJECT_ROOT / "models"

class PaddleOCREngine(OCREngine):
    def __init__(self):
        self.ocr = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            text_detection_model_dir=str(MODELS_DIR / "det" / "PP-OCRv6_medium_det"),
            text_recognition_model_dir=str(MODELS_DIR / "rec" / "PP-OCRv6_medium_rec"),
        )

    def predict(self, image: np.ndarray) -> dict:
        result = self.ocr.predict(image)
        first_result = result[0] if result else {}

        return {
            "texts": first_result.get("rec_texts", []),
            "boxes": first_result.get("rec_boxes", []),
            "raw": result,
        }

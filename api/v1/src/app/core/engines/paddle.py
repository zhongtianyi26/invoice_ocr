import numpy as np
from paddleocr import PaddleOCR

from app.core.engines.base import OCREngine


class PaddleOCREngine(OCREngine):
    def __init__(self):
        self.ocr = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
        )

    def predict(self, image: np.ndarray) -> dict:
        result = self.ocr.predict(image)
        first_result = result[0] if result else {}

        return {
            "texts": first_result.get("rec_texts", []),
            "boxes": first_result.get("rec_boxes", []),
            "raw": result,
        }

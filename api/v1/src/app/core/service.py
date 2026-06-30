from typing import Optional

from app.core.manager import OCRManager
from app.utils.image import image_bytes_to_array


class OCRService:
    def __init__(self):
        self.manager = OCRManager()

    def recognize(self, image_data: bytes) -> list[str]:
        image = image_bytes_to_array(image_data)
        result = self.manager.predict(image)
        return result.get("texts", [])


_ocr_service: Optional[OCRService] = None


def get_ocr_service() -> OCRService:
    global _ocr_service
    if _ocr_service is None:
        _ocr_service = OCRService()
    return _ocr_service


def process_image(image_data: bytes) -> list[str]:
    return get_ocr_service().recognize(image_data)

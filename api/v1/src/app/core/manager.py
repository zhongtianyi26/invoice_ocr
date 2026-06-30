from app.config.config import OCR_ENGINE
from app.core.engines.base import OCREngine


class OCRManager:
    _instance = None
    _initialized = False

    ENGINE_PADDLE = "paddle"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, engine_type: str = OCR_ENGINE):
        if self._initialized:
            return

        self.engine_type = engine_type
        self.engine = self._create_engine(engine_type)
        OCRManager._initialized = True

    def _create_engine(self, engine_type: str) -> OCREngine:
        if engine_type == self.ENGINE_PADDLE:
            from app.core.engines.paddle import PaddleOCREngine

            return PaddleOCREngine()

        raise ValueError(f"Unsupported OCR engine: {engine_type}")

    def predict(self, image):
        return self.engine.predict(image)

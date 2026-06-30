from abc import ABC, abstractmethod

import numpy as np


class OCREngine(ABC):
    @abstractmethod
    def predict(self, image: np.ndarray) -> dict:
        """Return OCR texts, boxes, and the raw engine result."""
        raise NotImplementedError

import io

import numpy as np
from PIL import Image


def image_bytes_to_array(image_data: bytes) -> np.ndarray:
    image = Image.open(io.BytesIO(image_data))
    return np.array(image)

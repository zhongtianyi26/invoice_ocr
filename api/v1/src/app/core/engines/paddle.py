import os
import numpy as np
from pathlib import Path
from paddleocr import PaddleOCR

from app.core.engines.base import OCREngine


def get_project_root(marker="pyproject.toml") -> Path:
    """向上查找包含标记文件的目录作为项目根目录"""
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        if (parent / marker).exists():
            return parent.parent
    # 如果找不到，回退到当前文件的父目录的父...（作为后备）
    raise RuntimeError(f"未找到项目根目录（标记: {marker}）")


class PaddleOCREngine(OCREngine):
    def __init__(self):
        # 1. 确定模型根目录（优先使用环境变量 PADDLE_HOME）
        paddle_home = os.environ.get("PADDLE_HOME")
        if paddle_home:
            models_root = Path(paddle_home)
        else:
            project_root = get_project_root()
            models_root = project_root / "models"

        # 2. 确定具体模型子目录（可通过环境变量覆盖）
        det_model_dir = os.environ.get(
            "DET_MODEL_DIR",
            str(models_root / "det" / "PP-OCRv6_medium_det")
        )
        rec_model_dir = os.environ.get(
            "REC_MODEL_DIR",
            str(models_root / "rec" / "PP-OCRv6_medium_rec")
        )

        # 3. 设置 PADDLE_HOME 环境变量（便于 PaddleOCR 内部缓存）
        os.environ["PADDLE_HOME"] = str(models_root)

        # 4. 初始化 OCR 引擎
        self.ocr = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            text_detection_model_dir=det_model_dir,
            text_recognition_model_dir=rec_model_dir,
        )

    def predict(self, image: np.ndarray) -> dict:
        result = self.ocr.predict(image)
        first_result = result[0] if result else {}

        return {
            "texts": first_result.get("rec_texts", []),
            "boxes": first_result.get("rec_boxes", []),
            "raw": result,
        }
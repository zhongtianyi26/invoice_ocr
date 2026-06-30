import os

from dotenv import load_dotenv


load_dotenv()

ROOT_PATH = os.getenv("OCR_ROOT_PATH", "")
API_HOST = os.getenv("OCR_HOST", "0.0.0.0")
API_PORT = int(os.getenv("OCR_PORT", "8000"))

OCR_ENGINE = os.getenv("OCR_ENGINE", "paddle")
OCR_DEVICE = os.getenv("OCR_DEVICE", "cpu")

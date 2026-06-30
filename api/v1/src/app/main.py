from fastapi import FastAPI

from app.config.config import ROOT_PATH
from app.routers import ocr


app = FastAPI(
    title="PP-OCRv6 Service",
    description="OCR service supporting Base64 strings and image uploads.",
    root_path=ROOT_PATH,
)

app.include_router(ocr.router, prefix="/ocr/v1")


@app.get("/")
async def root():
    return {
        "message": "PP-OCRv6 OCR Service is running.",
        "endpoints": ["/ocr/v1/base64", "/ocr/v1/upload"],
    }

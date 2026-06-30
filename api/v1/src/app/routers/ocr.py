import base64

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.core.service import process_image
from app.schemas.ocr import OCRResponse


router = APIRouter(tags=["OCR"])


@router.post("/base64", response_model=OCRResponse)
async def ocr_base64(base64_string: str = Form(...)):
    try:
        if "," in base64_string:
            base64_string = base64_string.split(",", 1)[1]

        image_data = base64.b64decode(base64_string)
        results = process_image(image_data)
        return OCRResponse(status="success", results=results)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/upload", response_model=OCRResponse)
async def ocr_upload(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only jpg and png images are supported.")

    try:
        image_data = await file.read()
        results = process_image(image_data)
        return OCRResponse(status="success", results=results)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

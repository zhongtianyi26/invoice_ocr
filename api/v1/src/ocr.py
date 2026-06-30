import os
import base64
import io
import uvicorn
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np

from dotenv import load_dotenv

load_dotenv() 
# 初始化 PaddleOCR 实例（全局复用，避免重复加载）
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)

ROOT_PATH = os.getenv("OCR_ROOT_PATH", "")        
API_HOST = os.getenv("OCR_HOST", "0.0.0.0")
API_PORT = int(os.getenv("OCR_PORT", "8000"))

app = FastAPI(title="PP-OCRv6 Service", description="支持 Base64 或文件上传的 OCR 服务")

def process_image(image_data: bytes) -> list:
    """
    接收图片二进制数据，调用 OCR 并返回结构化结果
    """
    # 将字节数据转为 PIL Image，再转成 numpy 数组（PaddleOCR 接受 numpy 数组或文件路径）
    try:
        img = Image.open(io.BytesIO(image_data))
        img_array = np.array(img)
        # 调用预测
        result = ocr.predict(img_array)
        # 解析结果，提取文本、置信度、坐标
        ocr_results = result[0].get("rec_texts")
        return ocr_results
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"图片处理失败: {str(e)}")

@app.post("/ocr/v1/base64")
async def ocr_base64(base64_string: str = Form(...)):
    """
    接受 Base64 编码的图片字符串（不含 data:image/... 前缀）
    """
    try:
        # 如果包含数据头，去除
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        # 解码
        image_data = base64.b64decode(base64_string)
        results = process_image(image_data)
        return JSONResponse(content={"status": "success", "results": results})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/ocr/v1/upload")
async def ocr_upload(file: UploadFile = File(...)):
    """
    接受图片文件上传 (支持 jpg, png 等)
    """
    # 验证文件类型
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="仅支持 jpg 或 png 图片")
    try:
        image_data = await file.read()
        results = process_image(image_data)
        return JSONResponse(content={"status": "success", "results": results})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    return {"message": "PP-OCRv6 OCR Service is running. Use /ocr/base64 (POST form-data with base64_string) or /ocr/upload (POST file) to perform OCR."}

if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT)
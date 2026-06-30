from pydantic import BaseModel


class OCRResponse(BaseModel):
    status: str
    results: list[str]

import uvicorn

from app.config.config import API_HOST, API_PORT
from app.core.service import process_image
from app.main import app


if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT)

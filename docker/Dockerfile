# 使用轻量级 Python 基础镜像
FROM python:3.13-slim

# 设置工作目录
WORKDIR /app



# 安装系统依赖（PaddleOCR 需要一些基础库）
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

ENV UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
# 安装 uv（推荐使用官方安装脚本）
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 复制项目依赖文件（先复制依赖文件，利用 docker 缓存）
COPY . .
# 安装 Python 依赖（使用 uv sync --frozen 以锁定版本）
RUN uv sync --frozen --no-dev


# 设置环境变量（用于指定模型目录，方便挂载）
ENV PADDLE_HOME=/app/models

# 暴露 FastAPI 默认端口
EXPOSE 8000

# 启动命令（假设 API 入口在 api/v1/src/app/main.py）
# CMD ["uv", "run", "--no-sync", "uvicorn", "api.v1.src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
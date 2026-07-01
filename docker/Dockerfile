# 使用轻量级 Python 基础镜像
FROM python:3.13-slim


# 设置工作目录
WORKDIR /app

# 优化 2：设置 uv 的环境变量，修复潜在的网络挂起问题
ENV UV_NATIVE_TLS=1
ENV UV_CONCURRENT_DOWNLOADS=4
ENV UV_DEFAULT_INDEX=https://mirrors.aliyun.com/pypi/simple/

# 安装 uv
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --no-cache-dir uv

# 复制项目依赖文件
COPY api/ .
COPY README.md ./README.md

# 优化 3：移除 --refresh，降低非必要的网络 I/O。增加 -v (verbose) 输出，如果再卡住，你能清晰看到报错
RUN uv sync --frozen --no-dev
# 设置环境变量
ENV PADDLE_HOME=/app/models

# 暴露端口
EXPOSE 8000

CMD ["uv", "run", "--no-sync", "uvicorn", "api.v1.src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
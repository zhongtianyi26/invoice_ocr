# OCR API 服务 Docker 部署说明

本文档介绍如何使用 Docker 和 Docker Compose 部署基于 PP-OCRv6 的 OCR API 服务。

---

## 目录结构

项目根目录结构如下：

    项目根目录/
    ├── api/                          # API 源码目录
    │   ├── v1/src/app/               # FastAPI 应用代码
    │   ├── pyproject.toml
    │   └── uv.lock
    ├── models/                       # 模型文件目录（需自行下载）
    │   ├── det/
    │   └── rec/
    ├── docker/                       # Docker 相关文件
    │   ├── Dockerfile
    │   └── docker-compose.yml
    └── README.md

---

## 前提条件

- **Docker** (版本 20.10 或更高)
- **Docker Compose** (版本 2.0 或更高)
- 已下载好的 PP-OCRv6 模型文件（存放于 `models/` 目录）

---

## 模型准备

服务需要预训练的 PP-OCRv6 模型文件，请从[下载](#模型下载)并解压到 `models/` 目录，确保目录结构如下：

    models/
    ├── det/
    │   └── PP-OCRv6_medium_det/      # 包含 inference.pdmodel 等文件
    └── rec/
        └── PP-OCRv6_medium_rec/      # 包含 inference.pdmodel 等文件

## 模型下载
```bash
cd <repository_name>
uv run modelscope download --model PaddlePaddle/PP-OCRv6_medium_det --local_dir models/det/PP-OCRv6_medium_det
uv run modelscope download --model PaddlePaddle/PP-OCRv6_medium_rec --local_dir models/rec/PP-OCRv6_medium_rec
```


> 模型文件较大，建议使用卷挂载（已在 compose 中配置），避免将模型打包进镜像。

---

## 快速启动

### 1. 构建镜像

在项目根目录（即 `docker/` 的上一级）执行：

    docker build -f docker/Dockerfile -t ocr-api .

或使用 Docker Compose 一键构建并启动：

    docker-compose -f docker/docker-compose.yml up -d --build

### 2. 启动服务

    docker-compose -f docker/docker-compose.yml up -d

### 3. 验证服务

    curl http://localhost:8000/

应返回服务运行信息。

---

## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `PADDLE_HOME` | PaddleOCR 模型根目录 | `/app/models` |
| `PYTHONPATH` | Python 模块搜索路径 | `/app/api/v1/src` |


### 卷挂载

`docker-compose.yml` 中定义了两个挂载点：

| 宿主机路径 | 容器路径 | 用途 |
|------------|----------|------|
| `../models` | `/app/models` | 挂载模型文件（只读） |
| `../api`    | `/app/api`   | 挂载代码目录 |


---

## 常用命令

| 操作 | 命令 |
|------|------|
| 构建并启动 | `docker-compose -f docker/docker-compose.yml up -d --build` |
| 停止服务 | `docker-compose -f docker/docker-compose.yml down` |
| 查看日志 | `docker-compose -f docker/docker-compose.yml logs -f` |
| 进入容器 | `docker exec -it ocr-api /bin/bash` |
| 重启服务 | `docker-compose -f docker/docker-compose.yml restart` |
| 查看状态 | `docker-compose -f docker/docker-compose.yml ps` |

---

## API 测试

服务启动后，可通过以下方式测试：

### 文件上传识别

    curl -X POST "http://localhost:8000/ocr/upload" \
      -F "file=@/path/to/your/image.jpg"

### Base64 字符串识别

    curl -X POST "http://localhost:8000/ocr/base64" \
      -F "base64_string=<base64.txt"

具体接口文档请参考 `api/docs/接口文档.md`。

---

## 常见问题

### 1. 容器启动失败，提示 `ModuleNotFoundError: No module named 'api'`

确保 `api/` 目录下所有子目录（`v1/`, `src/`, `app/`）都包含 `__init__.py` 文件（可为空）。检查 `docker-compose.yml` 中 `PYTHONPATH` 是否正确。

### 2. 模型文件加载失败

检查 `models/` 目录是否挂载正确，以及模型子目录名称是否与代码中的 `text_detection_model_dir` 和 `text_recognition_model_dir` 一致。

### 3. 下载依赖时卡住

如果构建镜像时 `uv sync` 下载缓慢，可修改 `Dockerfile` 中的 `UV_DEFAULT_INDEX` 环境变量，更换为更快的镜像源（如清华、阿里云）。

---

## 生产环境建议

- 移除 `docker-compose.yml` 中 `../api` 的挂载，避免运行时修改代码。
- 使用多阶段构建进一步缩小镜像体积。
- 为容器设置资源限制（如 `deploy.resources`）。
- 配置健康检查（`healthcheck`）以便编排工具监控服务状态。

---

## 许可证

本项目基于 PP-OCRv6 开发，请遵守 PaddleOCR 的许可证要求。
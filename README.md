# PP-OCRv6 OCR 服务

基于 PaddleOCR 的 OCR 识别服务，提供 FastAPI 接口和 Streamlit 测试页面，支持图片文件上传和 Base64 字符串识别。项目已按入口层、路由层、核心服务层、OCR 引擎层进行解耦，FastAPI 和 Streamlit 共用同一套 OCR 服务逻辑。

## 目录结构

```text
ppr_v6_ocr/
├── README.md
├── main.py
└── api/
    ├── pyproject.toml
    ├── uv.lock
    ├── docs/
    │   └── 接口文档.md
    ├── test/
    │   └── base64/
    │       └── base64_trans.py
    └── v1/
        └── src/
            ├── ocr.py                  # 兼容入口：启动 FastAPI 服务
            ├── test_time_script.py     # Streamlit OCR 测试页面
            └── app/
                ├── main.py             # FastAPI 应用入口
                ├── config/
                │   └── config.py       # 环境变量和服务配置
                ├── routers/
                │   └── ocr.py          # OCR API 路由
                ├── core/
                │   ├── manager.py      # OCR 引擎单例管理
                │   ├── service.py      # OCR 核心服务
                │   └── engines/
                │       ├── base.py     # OCR 引擎基类
                │       └── paddle.py   # PaddleOCR 引擎实现
                ├── schemas/
                │   └── ocr.py          # API 响应模型
                └── utils/
                    └── image.py        # 图片转换工具
```

## 快速开始

### 安装依赖

```bash
cd api
uv sync
```

如果本机 `uv` 缓存目录异常，可以临时指定缓存目录：

```bash
$env:UV_CACHE_DIR = "../.uv-cache"
uv sync
```
### 模型下载
```bash
cd <repository_name>
uv run modelscope download --model PaddlePaddle/PP-OCRv6_medium_det --local_dir models/det/PP-OCRv6_medium_det
uv run modelscope download --model PaddlePaddle/PP-OCRv6_medium_rec --local_dir models/rec/PP-OCRv6_medium_rec
```


### 运行 API 服务

```bash
cd api/v1/src
uv run python ocr.py
```

服务默认监听：

```text
http://127.0.0.1:8000
```

也可以直接通过 uvicorn 启动：

```bash
cd api/v1/src
uv run python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 运行 Streamlit 测试页面

```bash
cd api/v1/src
uv run streamlit run test_time_script.py
```

Streamlit 页面会直接调用 `app.core.service.process_image`，不经过 HTTP 请求，和 FastAPI 接口复用同一个 OCR 核心服务。

## 核心功能

### OCR 引擎

| 引擎类型 | 技术基础 |
| --- | --- |
| PaddleOCR | PP-OCRv6 |


### 服务解耦

- `app/main.py` 只负责创建 FastAPI 应用和注册路由。
- `app/routers/ocr.py` 只负责处理 HTTP 请求和响应。
- `app/core/service.py` 负责图片识别业务入口。
- `app/core/manager.py` 负责 OCR 引擎单例管理，避免重复加载模型。
- `app/core/engines/paddle.py` 负责 PaddleOCR 的具体调用。
- `test_time_script.py` 作为页面层，只调用核心服务，不耦合 FastAPI。

## [API 接口](api/docs/接口文档.md)

详见[接口文档.md](api/docs/接口文档.md)

## 配置说明

配置文件位置：

```text
api/v1/src/app/config/config.py
```

支持的环境变量：

| 变量名 | 默认值 | 说明 |
| --- | --- | --- |
| `OCR_ROOT_PATH` | 空字符串 | FastAPI root_path |
| `OCR_HOST` | `0.0.0.0` | API 服务监听地址 |
| `OCR_PORT` | `8000` | API 服务监听端口 |
| `OCR_ENGINE` | `paddle` | OCR 引擎类型 |
| `OCR_DEVICE` | `cpu` | 预留设备配置 |

## 工具脚本

### Base64 转换

脚本位置：

```text
api/test/base64/base64_trans.py
```

用于将图片转为 Base64 文本，或将 Base64 文本还原为图片，便于测试 `/ocr/v1/base64` 接口。

## 测试与验证

语法检查：

```bash
python -m compileall api/v1/src
```

导入检查：

```bash
cd api/v1/src
uv run python -c "from ocr import app, process_image; print(app.title, callable(process_image))"
```

## 返回格式说明

当前接口返回 PaddleOCR 识别出的纯文本列表：

```json
{
  "status": "success",
  "results": ["文本1", "文本2"]
}
```

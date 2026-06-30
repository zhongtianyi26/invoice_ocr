import os
import time
import requests

# ================= 配置项 =================
API_URL = "http://127.0.0.1:8000/ocr/v1/upload"
IMAGE_DIR = "./image"  # 存放测试图片的文件夹路径
# =========================================

def run_ocr_benchmark():
    # 检查测试文件夹是否存在
    if not os.path.exists(IMAGE_DIR):
        print(f"❌ 错误: 找不到文件夹 '{IMAGE_DIR}'")
        print(f"💡 请在当前目录下创建 '{IMAGE_DIR}' 文件夹，并放入几张 jpg 或 png 图片。")
        return

    # 过滤出支持的图片格式 (FastAPI 限制了 image/jpeg 和 image/png)
    supported_extensions = ('.jpg', '.jpeg', '.png')
    image_files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(supported_extensions)]

    if not image_files:
        print(f"⚠️ 警告: '{IMAGE_DIR}' 文件夹中没有找到符合要求的图片 (.jpg, .jpeg, .png)")
        return

    print(f"🚀 找到 {len(image_files)} 张测试图片，开始进行循环性能测试...\n")
    print(f"{'序号':<6}{'图片名称':<25}{'状态':<8}{'识别行数':<10}{'耗时 (ms)':<10}")
    print("-" * 65)

    latencies = []
    success_count = 0
    i = 0
    for i in range(33):  # 循环测试 3 次
        for idx, filename in enumerate(image_files, 1):
            file_path = os.path.join(IMAGE_DIR, filename)
            
            # 根据后缀简单判断 content-type，防止 FastAPI 报 400 错
            content_type = "image/png" if filename.lower().endswith('.png') else "image/jpeg"

            try:
                with open(file_path, 'rb') as f:
                    # 按照 FastAPI 的 UploadFile 格式组装数据
                    files = {'file': (filename, f, content_type)}
                    
                    # 测算精准时间
                    start_time = time.perf_counter()
                    response = requests.post(API_URL, files=files)
                    end_time = time.perf_counter()
                    
                elapsed_ms = (end_time - start_time) * 1000  # 转换为毫秒

                if response.status_code == 200:
                    res_data = response.json()
                    lines_count = len(res_data.get("results", []))
                    latencies.append(elapsed_ms)
                    success_count += 1
                    print(f"{idx:<6}{filename:<25}{'成功':<8}{lines_count:<10}{elapsed_ms:>.2f}")
                else:
                    print(f"{idx:<6}{filename:<25}{'失败':<8}{'-':<10}{'状态码: ' + str(response.status_code)}")

            except Exception as e:
                print(f"{idx:<6}{filename:<25}{'异常':<8}{'-':<10}{str(e)}")

    # ================= 统计结果 =================
    print("-" * 65)
    if success_count > 0:
        total_images = len(image_files)
        avg_time = sum(latencies) / success_count
        min_time = min(latencies)
        max_time = max(latencies)

        print(f"📊 测试报告:")
        print(f"  - 总图片数 / 成功数: {total_images} / {success_count}")
        print(f"  - 最快耗时: {min_time:.2f} ms")
        print(f"  - 最慢耗时: {max_time:.2f} ms")
        print(f"  - ✨ 平均每张图片耗时: {avg_time:.2f} ms")
    else:
        print("❌ 所有图片均未测试成功，请检查 OCR 服务是否正常启动。")

if __name__ == "__main__":
    run_ocr_benchmark()
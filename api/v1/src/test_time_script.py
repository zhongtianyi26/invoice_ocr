import time

import streamlit as st
from PIL import Image

from app.core.service import process_image


st.set_page_config(page_title="PP-OCRv6 测试页面", layout="wide")


def run_uploaded_image(uploaded_file):
    image_bytes = uploaded_file.getvalue()
    start_time = time.perf_counter()
    results = process_image(image_bytes)
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    return results, elapsed_ms


def main():
    st.title("PP-OCRv6 测试页面")

    uploaded_files = st.file_uploader(
        "上传图片",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
    )

    if not uploaded_files:
        st.info("请选择一张或多张 jpg、jpeg、png 图片。")
        return

    if st.button("开始识别", type="primary", width='stretch'):
        total_elapsed = 0.0
        success_count = 0
        total_files = len(uploaded_files)  # 获取总图片数

        # ==================== 1. 新增：初始化进度条和状态占位符 ====================
        progress_bar = st.progress(0.0)    # 初始化进度条为 0%
        status_message = st.empty()         # 创建一个动态文本占位符
        # =========================================================================

        for idx, uploaded_file in enumerate(uploaded_files):
            # ==================== 2. 新增：动态更新“识别中”状态 ====================
            # 使用 .info() 让提示框变成蓝色，更显眼
            status_message.info(
                f"⏳ 正在识别中... 进度: {idx}/{total_files} | "
                f"当前正在处理: `{uploaded_file.name}`"
            )
            # =========================================================================

            st.divider()
            left, right = st.columns([1, 1])

            with left:
                st.subheader(uploaded_file.name)
                st.image(Image.open(uploaded_file), width='stretch')

            with right:
                try:
                    results, elapsed_ms = run_uploaded_image(uploaded_file)
                    total_elapsed += elapsed_ms
                    success_count += 1

                    st.metric("耗时", f"{elapsed_ms:.2f} ms")
                    st.metric("识别行数", len(results))

                    if results:
                        st.text_area(
                            "识别结果",
                            "\n".join(results),
                            height=240,
                            key=f"result_{uploaded_file.name}",
                        )
                    else:
                        st.warning("未识别到文字。")
                except Exception as exc:
                    st.error(f"识别失败：{exc}")

            # ==================== 3. 新增：每跑完一张图，推进进度条 ====================
            current_progress = (idx + 1) / total_files
            progress_bar.progress(current_progress)
            # =========================================================================

        # ==================== 4. 新增：全部完成后更新状态 ====================
        status_message.success(f"🎉 所有图片识别完成！(成功: {success_count}/{total_files})")
        # =========================================================================

        if success_count:
            st.divider()
            st.success(
                f"完成 {success_count}/{len(uploaded_files)} 张图片，"
                f"平均耗时 {total_elapsed / success_count:.2f} ms。"
            )


if __name__ == "__main__":
    main()
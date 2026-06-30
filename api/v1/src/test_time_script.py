import time

import streamlit as st
from PIL import Image

from ocr import process_image


st.set_page_config(page_title="PP-OCRv6 测试页面", page_icon="OCR", layout="wide")


def run_uploaded_image(uploaded_file):
    image_bytes = uploaded_file.getvalue()
    start_time = time.perf_counter()
    results = process_image(image_bytes)
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    return results, elapsed_ms


def main():
    st.title("PP-OCRv6 测试页面")
    st.caption("直接复用 ocr.py 中的同一个 PaddleOCR 实例，不经过 FastAPI 接口。")

    uploaded_files = st.file_uploader(
        "上传图片",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
    )

    if not uploaded_files:
        st.info("请选择一张或多张 jpg、jpeg、png 图片。")
        return

    if st.button("开始识别", type="primary", use_container_width=True):
        total_elapsed = 0.0
        success_count = 0

        for uploaded_file in uploaded_files:
            st.divider()
            left, right = st.columns([1, 1])

            with left:
                st.subheader(uploaded_file.name)
                st.image(Image.open(uploaded_file), use_container_width=True)

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

        if success_count:
            st.divider()
            st.success(
                f"完成 {success_count}/{len(uploaded_files)} 张图片，"
                f"平均耗时 {total_elapsed / success_count:.2f} ms。"
            )


if __name__ == "__main__":
    main()

import base64
import os

def image_to_base64_txt(image_path, txt_path, add_prefix=False):
    """
    将图片文件编码为 Base64 字符串，保存到 txt 文件。
    
    :param image_path: 图片文件路径（如 'photo.jpg'）
    :param txt_path:   输出的 txt 文件路径（如 'photo.txt'）
    :param add_prefix: 是否添加 Data URL 前缀（如 'data:image/png;base64,'）
    """
    # 读取图片二进制数据
    with open(image_path, 'rb') as img_file:
        img_bytes = img_file.read()
        base64_str = base64.b64encode(img_bytes).decode('utf-8')
    
    # 可选添加前缀（便于直接用于网页 <img src="...">）
    if add_prefix:
        # 根据文件扩展名猜测 MIME 类型
        ext = os.path.splitext(image_path)[1].lower()
        mime_map = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
                    '.png': 'image/png', '.gif': 'image/gif',
                    '.bmp': 'image/bmp', '.webp': 'image/webp'}
        mime = mime_map.get(ext, 'application/octet-stream')
        base64_str = f'data:{mime};base64,' + base64_str
    
    # 写入 txt 文件
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(base64_str)
    
    print(f"✅ Base64 已保存至: {txt_path}")
    print(f"   字符串长度: {len(base64_str)} 字符")


def base64_txt_to_image(txt_path, output_image_path):
    """
    从 txt 文件读取 Base64 字符串，还原为图片文件。
    """
    with open(txt_path, 'r', encoding='utf-8') as txt_file:
        base64_str = txt_file.read().strip()
    
    # 如果包含 Data URL 前缀（如 data:image/png;base64,xxx），去除前缀
    if base64_str.startswith('data:'):
        # 找到第一个逗号的位置
        comma_idx = base64_str.find(',')
        if comma_idx != -1:
            base64_str = base64_str[comma_idx+1:]
    
    # 解码并写入图片
    img_bytes = base64.b64decode(base64_str)
    with open(output_image_path, 'wb') as img_file:
        img_file.write(img_bytes)
    
    print(f"✅ 图片已还原至: {output_image_path}")


# ---------- 使用示例 ----------
if __name__ == '__main__':
    # 1. 编码：图片 → Base64.txt
    image_to_base64_txt(
        image_path='../image/invoice1.jpg',      # 你的图片路径
        txt_path='example_base64.txt',
        add_prefix=False               # 设为 True 可生成带 data:image 前缀的字符串
    )
    
    # 2. 解码：Base64.txt → 图片（验证用）
    # base64_txt_to_image('example_base64.txt', 'restored_example.jpg')
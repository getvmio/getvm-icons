import os
import io
import cairosvg
from PIL import Image
from rich import print
from collections import Counter


def convert_svg_to_png(svg_path, max_size):
    """转换图片格式"""
    png_data = cairosvg.svg2png(
        url=svg_path, output_width=max_size, output_height=max_size
    )
    return Image.open(io.BytesIO(png_data))


def resize_with_aspect_ratio(image, max_size):
    """重设图片大小"""
    if max(image.size) > max_size:
        ratio = max_size / max(image.size)
        new_size = (int(image.width * ratio), int(image.height * ratio))
        return image.resize(new_size, Image.LANCZOS)
    return image


def get_main_color(image):
    # 打开图片
    # 确保图片是RGB模式
    img = image.convert("RGB")
    # 获取所有像素
    pixels = list(img.getdata())
    # 计算每种颜色的出现次数
    color_counts = Counter(pixels)
    # 去除透明像素
    color_counts.pop((0, 0, 0), None)
    # 去除白色
    color_counts.pop((255, 255, 255), None)
    # 获取出现次数最多的颜色
    try:
        main_color = color_counts.most_common(1)[0][0]
    except:
        # 如果没有颜色，返回 (0, 0, 0)
        main_color = (0, 0, 0)
    return main_color


def apply_color_to_image(image, color, fill_opacity):
    """填充颜色"""
    # 确保图片有透明通道
    img = image.convert("RGBA")
    # 获取图片数据
    data = img.getdata()
    # 创建新的图片数据，将非透明像素替换为主色
    new_data = []
    for item in data:
        if item[3] != 0:  # 如果像素不是完全透明的
            # 计算新的 alpha 值，考虑原始 alpha 和填充不透明度
            new_alpha = int(item[3] * (fill_opacity / 255))
            # 使用新的 RGB 值和计算出的 alpha 值
            new_data.append(color + (new_alpha,))
        else:
            # 如果是完全透明的，保持不变
            new_data.append(item)
    # 更新图片数据
    img.putdata(new_data)
    return img


def merge_icons(base_icon_paths, logo_path, output_path):
    # 打开基础图标
    base_icons = [Image.open(path).convert("RGBA") for path in base_icon_paths]
    # 确保所有基础图标大小相同
    base_size = base_icons[0].size
    for icon in base_icons[1:]:
        if icon.size != base_size:
            raise ValueError("All base icons must have the same size")
    # 处理logo（支持SVG和其他格式）
    if logo_path.lower().endswith(".svg"):
        # 对于SVG，我们按比例转换为PNG，最长边为380px
        logo = convert_svg_to_png(logo_path, max_size=380)
    else:
        logo = Image.open(logo_path).convert("RGBA")
        # 调整其他格式图片大小，最大边长为380px
        logo = resize_with_aspect_ratio(logo, max_size=380)
    # 调整logo大小以适应基础图标，保持宽高比
    logo_size = max(logo.size)
    scale = min(min(base_size) / logo_size, 1)  # 确保logo不会比基础图标大
    new_size = (int(logo.width * scale), int(logo.height * scale))
    logo = logo.resize(new_size, Image.LANCZOS)
    # 获取logo的主色
    main_color = get_main_color(logo)
    # 创建一个新的透明图层，大小与基础图标相同
    merged_icon = Image.new("RGBA", base_size, (0, 0, 0, 0))
    # 按顺序叠加基础图标
    for i, base_icon in enumerate(base_icons):
        if i == 1:
            # 如果是 layer1.png，使用半透明主色替换非透明像素
            base_icon = apply_color_to_image(base_icon, main_color, 100)
        if i == 2:
            # 如果是 layer2.png，使用主色替换非透明像素
            base_icon = apply_color_to_image(base_icon, main_color, 255)
        merged_icon = Image.alpha_composite(merged_icon, base_icon)

    # 计算logo的位置（居中）
    x = (base_size[0] - logo.width) // 2
    y = (base_size[1] - logo.height) // 2

    # 创建一个与基础图标大小相同的透明图层
    logo_layer = Image.new("RGBA", base_size, (0, 0, 0, 0))
    # 将logo粘贴到这个图层上
    logo_layer.paste(logo, (x, y), logo)

    # 使用alpha_composite方法合并图层，这会保留透明度信息
    merged_icon = Image.alpha_composite(merged_icon, logo_layer)

    # 保存结果
    merged_icon.save(output_path, "PNG")


def process_logos(base_icon_paths, raw_logos_dir, output_dir):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历raw_logos目录
    for filename in os.listdir(raw_logos_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".svg")):
            try:
                logo_path = os.path.join(raw_logos_dir, filename)
                output_path = os.path.join(
                    output_dir, f"{os.path.splitext(filename)[0]}.png"
                )
                merge_icons(base_icon_paths, logo_path, output_path)
                print(f"Processed: {output_path}")
            except Exception as e:
                print(f"[red]Error processing:[/red] {logo_path}, {e}")


# 使用示例
base_icon_paths = ["layer0.png", "layer1.png", "layer2.png"]
raw_logos_dir = "raw-logos"
output_dir = "logos"

process_logos(base_icon_paths, raw_logos_dir, output_dir)

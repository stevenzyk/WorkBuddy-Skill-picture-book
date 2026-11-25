#!/usr/bin/env python3
"""
把绘本插画直接合成为打印级 PDF（不依赖浏览器，稳定可靠）。

背景：早期用 Playwright/Chromium headless 把 HTML 导出 PDF，但在部分
Windows 环境下 Chromium 进程会静默退出、不写文件，导致导出失败。
因此改为「直接用 PIL 把每页插画图按顺序合成 PDF」，稳定且体积小
（150dpi 下 20 页约 7MB，比浏览器导出的 78MB 更适合打印/传输）。

依赖：Pillow（pip install Pillow）

用法：
    python build_pdf.py <图片目录> <输出pdf路径> [页面宽mm] [页面高mm] [dpi]

示例（横款 12 寸，305mm × 229mm）：
    python build_pdf.py ./book ./book.pdf 305 229

说明：
    - 图片目录里按文件名排序（page_01_cover.png、page_02.png、...）逐页拼入 PDF。
    - 封底若无独立图片，会自动跳过；若需要纯色封底，可传入 --blank-back。
    - 默认 dpi=150，兼顾清晰度与体积；如需更高清可调到 200。
"""
import sys
import os
import glob


def build_pdf(image_dir: str, pdf_path: str, width_mm: float = 200.0,
              height_mm: float = 200.0, dpi: int = 150):
    try:
        from PIL import Image
    except ImportError:
        print("错误：未安装 Pillow。请先运行： pip install Pillow")
        sys.exit(1)

    image_dir = os.path.abspath(image_dir)
    if not os.path.isdir(image_dir):
        print(f"错误：找不到图片目录 {image_dir}")
        sys.exit(1)

    # 收集并按文件名排序（page_01_cover < page_02 < ... < page_20）
    exts = ("*.png", "*.jpg", "*.jpeg")
    files = []
    for ext in exts:
        files.extend(glob.glob(os.path.join(image_dir, ext)))
    files = sorted(set(files))

    if not files:
        print(f"错误：目录 {image_dir} 下没有找到任何图片（png/jpg/jpeg）")
        sys.exit(1)

    # 目标页面像素尺寸
    px_w = int(width_mm / 25.4 * dpi)
    px_h = int(height_mm / 25.4 * dpi)

    images = []
    for f in files:
        img = Image.open(f).convert("RGB")
        # 等比缩放并居中贴到目标页面尺寸（白底），避免拉伸变形
        img.thumbnail((px_w, px_h), Image.LANCZOS)
        canvas = Image.new("RGB", (px_w, px_h), "white")
        x = (px_w - img.width) // 2
        y = (px_h - img.height) // 2
        canvas.paste(img, (x, y))
        images.append(canvas)

    if not images:
        print("错误：没有可用的图片")
        sys.exit(1)

    # 合成 PDF（所有页尺寸统一）
    first, rest = images[0], images[1:]
    first.save(
        pdf_path,
        "PDF",
        save_all=True,
        append_images=rest,
        resolution=dpi,
        quality=95,
    )
    print(f"✅ 已生成 PDF（{len(images)} 页，{dpi}dpi）：{os.path.abspath(pdf_path)}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    img_dir = sys.argv[1]
    out = sys.argv[2]
    w = float(sys.argv[3]) if len(sys.argv) > 3 else 200.0
    h = float(sys.argv[4]) if len(sys.argv) > 4 else w
    dpi = int(sys.argv[5]) if len(sys.argv) > 5 else 150
    build_pdf(img_dir, out, w, h, dpi)

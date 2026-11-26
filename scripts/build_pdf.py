#!/usr/bin/env python3
"""
把绘本插画与故事文案合成为打印级 PDF（纯 Pillow 实现，不依赖浏览器，跨平台稳定）。

支持两种用法：

1. 推荐：基于 book.json 生成「含完整封面标题 + 正文文案 + 页码 + 封底寄语」的打印级绘本 PDF：
    python build_pdf.py --book ./book/book.json --out ./book/book.pdf [--dpi 150] [--bleed 0]

2. 兼容模式：直接将目录下的插画图片按页码顺序合成 PDF（自动排除 ref_* 等参考图）：
    python build_pdf.py <图片目录> <输出pdf路径> [页面宽mm] [页面高mm] [dpi] [--blank-back]

预设尺寸对照（--size）：
    square8     : 203mm × 203mm（方款 8 寸，默认）
    square10    : 254mm × 254mm（方款 10 寸）
    landscape12 : 305mm × 229mm（横款 12 寸）
    portrait12  : 229mm × 305mm（竖款 12 寸）

依赖：Pillow（pip install Pillow）
"""
import argparse
import glob
import json
import os
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

SIZE_PRESETS = {
    "square8": (203.0, 203.0),
    "square10": (254.0, 254.0),
    "landscape12": (305.0, 229.0),
    "portrait12": (229.0, 305.0),
}

EXCLUDE_PREFIXES = ("ref_", "reference_", "avatar", "source", "orig_", "photo_")

# 跨平台常见中文字体路径（优先衬线标题体 / 无衬线正文字体）
SERIF_FONT_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
    "/usr/share/fonts/noto-cjk/NotoSerifCJK-Bold.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Songti.ttc",
    "C:/Windows/Fonts/STZHONGS.TTF",
    "C:/Windows/Fonts/simsun.ttc",
    "C:/Windows/Fonts/msyhbd.ttc",
]

SANS_FONT_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",
]


def _load_pil():
    try:
        from PIL import Image, ImageDraw, ImageFont
        return Image, ImageDraw, ImageFont
    except ImportError:
        print("错误：未安装 Pillow。请先运行：pip install Pillow", file=sys.stderr)
        sys.exit(1)


def _find_font(candidates: List[str], size: int):
    _, _, ImageFont = _load_pil()
    for path in candidates:
        if os.path.isfile(path):
            try:
                return ImageFont.truetype(path, size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def _natural_key(path: str):
    name = os.path.basename(path).lower()
    return [int(tok) if tok.isdigit() else tok for tok in re.split(r"(\d+)", name)]


def crop_watermark(img, ratio: float = 0.065):
    """等比裁去右下角平台水印区域（默认裁去右侧与底部各 6.5%，保持原图宽高比且不裁人物头部）。"""
    src_w, src_h = img.size
    new_w = max(1, int(round(src_w * (1.0 - ratio))))
    new_h = max(1, int(round(src_h * (1.0 - ratio))))
    return img.crop((0, 0, new_w, new_h))


def _fit_cover(img, target_w: int, target_h: int, vertical_focus: float = 0.5):
    """等比放大并裁切铺满目标区域（vertical_focus=0.65 时略偏下保留脚部与前景地面道具，防止切脚尖）。"""
    Image, _, _ = _load_pil()
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    new_w = max(1, int(round(src_w * scale)))
    new_h = max(1, int(round(src_h * scale)))
    resized = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = int(round((new_h - target_h) * max(0.0, min(1.0, vertical_focus))))
    return resized.crop((left, top, left + target_w, top + target_h))


def _fit_contain(img, target_w: int, target_h: int, bg_color="white"):
    """等比缩放并居中贴到目标画布（类似 CSS object-fit: contain）。"""
    Image, _, _ = _load_pil()
    copy = img.copy()
    copy.thumbnail((target_w, target_h), Image.LANCZOS)
    canvas = Image.new("RGB", (target_w, target_h), bg_color)
    x = (target_w - copy.width) // 2
    y = (target_h - copy.height) // 2
    canvas.paste(copy, (x, y))
    return canvas


# 中文排版行首禁则（避头点）与行尾禁则（避尾点）字符集
CJK_NO_LINE_START = set("。，、！？；：”’）》】〉」』〕…—·.,!?;:)]}%~")
CJK_NO_LINE_END = set("“‘（《【〈「『〔([{#")


def _wrap_text(draw, text: str, font, max_width: int) -> List[str]:
    """按像素宽度自动换行，内置中文标点避头/避尾禁则与末行孤字平衡（杜绝单独句号或单字占一行）。"""
    def text_w(s: str) -> int:
        if not s:
            return 0
        bbox = draw.textbbox((0, 0), s, font=font)
        return bbox[2] - bbox[0]

    # 允许避头标点轻微外挂（最多放宽 7% 行宽），放不下时则连同前字一起折入下一行
    hang_limit = int(max_width * 1.07)
    lines: List[str] = []

    for paragraph in text.replace("\r\n", "\n").split("\n"):
        if not paragraph:
            lines.append("")
            continue

        para_lines: List[str] = []
        current = ""
        for ch in paragraph:
            test = current + ch
            w = text_w(test)
            if w <= max_width or not current:
                current = test
            elif ch in CJK_NO_LINE_START and w <= hang_limit:
                # 避头标点紧贴行尾，不单掉下一行
                current = test
            else:
                # 若当前行末尾是左引号/左括号等避尾标点，将其移到下一行开头
                if len(current) > 1 and current[-1] in CJK_NO_LINE_END:
                    moved = current[-1]
                    para_lines.append(current[:-1])
                    current = moved + ch
                elif ch in CJK_NO_LINE_START and len(current) > 1:
                    # 连同前一个字符一起带入下一行，杜绝标点站行首
                    moved = current[-1]
                    para_lines.append(current[:-1])
                    current = moved + ch
                else:
                    para_lines.append(current)
                    current = ch
        if current:
            para_lines.append(current)

        # 末行孤字平衡：若最后一行只有 1~2 个字符（如“。”或“甜。”），从上一行匀 1~2 个字下来
        if len(para_lines) >= 2 and len(para_lines[-1]) <= 2 and len(para_lines[-2]) >= 6:
            prev_line = para_lines[-2]
            last_line = para_lines[-1]
            shift = 2 if len(last_line) == 1 else 1
            while shift < len(prev_line) - 2 and prev_line[-shift] in CJK_NO_LINE_START:
                shift += 1
            while shift > 1 and prev_line[-shift - 1] in CJK_NO_LINE_END:
                shift += 1
            candidate_last = prev_line[-shift:] + last_line
            if text_w(candidate_last) <= max_width:
                para_lines[-2] = prev_line[:-shift]
                para_lines[-1] = candidate_last

        lines.extend(para_lines)
    return lines


def _create_warm_gradient(w: int, h: int):
    Image, _, _ = _load_pil()
    top_rgb = (251, 233, 221)
    bot_rgb = (244, 214, 190)
    grad = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        r = int(top_rgb[0] + (bot_rgb[0] - top_rgb[0]) * t)
        g = int(top_rgb[1] + (bot_rgb[1] - top_rgb[1]) * t)
        b = int(top_rgb[2] + (bot_rgb[2] - top_rgb[2]) * t)
        grad.putpixel((0, y), (r, g, b))
    return grad.resize((w, h), Image.BILINEAR)


def _render_cover_page(img_path: str, title: str, subtitle: str, px_w: int, px_h: int):
    Image, ImageDraw, _ = _load_pil()
    art = Image.open(img_path).convert("RGB")
    canvas = _fit_cover(art, px_w, px_h, vertical_focus=0.72).convert("RGBA")

    # 顶部柔和渐变遮罩，保证标题清晰可读且不遮挡下方人物
    scrim_h = int(px_h * 0.42)
    scrim = Image.new("RGBA", (1, scrim_h))
    for y in range(scrim_h):
        alpha = int(125 * (1.0 - y / max(1, scrim_h - 1)) ** 1.4)
        scrim.putpixel((0, y), (0, 0, 0, alpha))
    scrim = scrim.resize((px_w, scrim_h), Image.BILINEAR)
    canvas.alpha_composite(scrim, (0, 0))

    draw = ImageDraw.Draw(canvas)
    base_dim = min(px_w, px_h)
    title_font = _find_font(SERIF_FONT_CANDIDATES, max(28, int(base_dim * 0.068)))
    sub_font = _find_font(SANS_FONT_CANDIDATES, max(16, int(base_dim * 0.028)))

    y_cursor = int(px_h * 0.06)
    max_text_w = int(px_w * 0.86)

    for line in _wrap_text(draw, title, title_font, max_text_w):
        bbox = draw.textbbox((0, 0), line, font=title_font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        tx = (px_w - tw) // 2
        # 柔和投影
        draw.text((tx + 2, y_cursor + 3), line, font=title_font, fill=(0, 0, 0, 140))
        draw.text((tx, y_cursor), line, font=title_font, fill=(255, 255, 255, 255))
        y_cursor += int(th * 1.35)

    if subtitle:
        y_cursor += int(base_dim * 0.012)
        for line in _wrap_text(draw, subtitle, sub_font, max_text_w):
            bbox = draw.textbbox((0, 0), line, font=sub_font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            tx = (px_w - tw) // 2
            draw.text((tx + 1, y_cursor + 2), line, font=sub_font, fill=(0, 0, 0, 130))
            draw.text((tx, y_cursor), line, font=sub_font, fill=(255, 255, 255, 240))
            y_cursor += int(th * 1.4)

    return canvas.convert("RGB")


def _render_body_page(img_path: str, text: str, page_no: int, px_w: int, px_h: int):
    Image, ImageDraw, _ = _load_pil()
    canvas = Image.new("RGB", (px_w, px_h), "white")
    art_h = int(px_h * 0.78)
    text_h = px_h - art_h

    art = Image.open(img_path).convert("RGB")
    art_fitted = _fit_cover(art, px_w, art_h, vertical_focus=0.80)
    canvas.paste(art_fitted, (0, 0))

    draw = ImageDraw.Draw(canvas)
    base_dim = min(px_w, px_h)
    body_font = _find_font(SANS_FONT_CANDIDATES, max(16, int(base_dim * 0.032)))
    num_font = _find_font(SANS_FONT_CANDIDATES, max(12, int(base_dim * 0.020)))

    max_text_w = int(px_w * 0.84)
    lines = _wrap_text(draw, text.strip(), body_font, max_text_w)
    line_heights = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line or "字", font=body_font)
        line_heights.append(bbox[3] - bbox[1])
    line_gap = max(6, int(base_dim * 0.014))
    total_text_h = sum(line_heights) + max(0, len(lines) - 1) * line_gap

    # 文案在底部白区居中偏上，留出页码空间
    page_no_area = int(text_h * 0.24)
    avail_h = text_h - page_no_area
    y_cursor = art_h + max(10, (avail_h - total_text_h) // 2)

    for idx, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=body_font)
        tw = bbox[2] - bbox[0]
        tx = (px_w - tw) // 2
        draw.text((tx, y_cursor), line, font=body_font, fill=(58, 52, 46))
        y_cursor += line_heights[idx] + line_gap

    # 页码
    no_str = f"— {page_no} —"
    nb = draw.textbbox((0, 0), no_str, font=num_font)
    nw, nh = nb[2] - nb[0], nb[3] - nb[1]
    nx = (px_w - nw) // 2
    ny = px_h - nh - max(12, int(text_h * 0.12))
    draw.text((nx, ny), no_str, font=num_font, fill=(182, 172, 160))

    return canvas


def _render_back_page(img_path: Optional[str], ending: str, px_w: int, px_h: int):
    Image, ImageDraw, _ = _load_pil()
    if img_path and os.path.isfile(img_path):
        art = Image.open(img_path).convert("RGB")
        canvas = _fit_cover(art, px_w, px_h).convert("RGBA")
    else:
        canvas = _create_warm_gradient(px_w, px_h).convert("RGBA")

    if not ending:
        return canvas.convert("RGB")

    draw = ImageDraw.Draw(canvas)
    base_dim = min(px_w, px_h)
    end_font = _find_font(SERIF_FONT_CANDIDATES, max(20, int(base_dim * 0.038)))
    max_text_w = int(px_w * 0.72)
    lines = _wrap_text(draw, ending.strip(), end_font, max_text_w)

    widths, heights = [], []
    for line in lines:
        bbox = draw.textbbox((0, 0), line or "字", font=end_font)
        widths.append(bbox[2] - bbox[0])
        heights.append(bbox[3] - bbox[1])

    line_gap = max(10, int(base_dim * 0.02))
    block_w = max(widths) if widths else 100
    block_h = sum(heights) + max(0, len(lines) - 1) * line_gap

    pad_x = max(28, int(base_dim * 0.055))
    pad_y = max(22, int(base_dim * 0.045))
    card_w = block_w + pad_x * 2
    card_h = block_h + pad_y * 2
    cx0 = (px_w - card_w) // 2
    cy0 = (px_h - card_h) // 2
    cx1 = cx0 + card_w
    cy1 = cy0 + card_h

    overlay = Image.new("RGBA", (px_w, px_h), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    radius = max(12, int(base_dim * 0.022))
    odraw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=radius, fill=(255, 255, 255, 215))
    canvas.alpha_composite(overlay)

    draw = ImageDraw.Draw(canvas)
    y_cursor = cy0 + pad_y
    for idx, line in enumerate(lines):
        tw = widths[idx]
        tx = (px_w - tw) // 2
        draw.text((tx, y_cursor), line, font=end_font, fill=(110, 79, 58, 255))
        y_cursor += heights[idx] + line_gap

    return canvas.convert("RGB")


def _resolve_dimensions(
    size_name: Optional[str], width_mm: Optional[float], height_mm: Optional[float]
) -> Tuple[float, float]:
    if width_mm is not None:
        return width_mm, (height_mm if height_mm is not None else width_mm)
    if size_name:
        if size_name not in SIZE_PRESETS:
            print(f"错误：不支持的尺寸预设 '{size_name}'，可选：{', '.join(SIZE_PRESETS)}", file=sys.stderr)
            sys.exit(1)
        return SIZE_PRESETS[size_name]
    return SIZE_PRESETS["square8"]


def build_pdf_from_book(
    book_json_path: str,
    pdf_path: str,
    size_override: Optional[str] = None,
    width_mm: Optional[float] = None,
    height_mm: Optional[float] = None,
    dpi: int = 150,
    bleed_mm: float = 0.0,
    remove_watermark: bool = False,
):
    Image, _, _ = _load_pil()
    book_file = Path(book_json_path).resolve()
    if not book_file.is_file():
        print(f"错误：找不到 book.json：{book_file}", file=sys.stderr)
        sys.exit(1)

    base_dir = book_file.parent
    data = json.loads(book_file.read_text(encoding="utf-8"))

    w_mm, h_mm = _resolve_dimensions(size_override or data.get("size"), width_mm, height_mm)
    total_w_mm = w_mm + bleed_mm * 2
    total_h_mm = h_mm + bleed_mm * 2
    px_w = int(round(total_w_mm / 25.4 * dpi))
    px_h = int(round(total_h_mm / 25.4 * dpi))

    import tempfile
    with tempfile.TemporaryDirectory() as tmp_dir:
        def prep_img(src: Path) -> str:
            if not remove_watermark:
                return str(src)
            im = crop_watermark(Image.open(src).convert("RGB"))
            dst = Path(tmp_dir) / src.name
            im.save(dst, "PNG")
            return str(dst)

        rendered = []

        # 1. 封面
        cover = data.get("cover", {})
        cover_img = base_dir / cover.get("image", "")
        if not cover_img.is_file():
            print(f"错误：找不到封面图片：{cover_img}", file=sys.stderr)
            sys.exit(1)
        rendered.append(
            _render_cover_page(
                prep_img(cover_img),
                data.get("title", "我的童话故事"),
                data.get("subtitle", ""),
                px_w,
                px_h,
            )
        )

        # 2. 正文页
        for idx, page in enumerate(data.get("pages", []), start=1):
            img_file = base_dir / page.get("image", "")
            if not img_file.is_file():
                print(f"错误：找不到第 {idx} 页图片：{img_file}", file=sys.stderr)
                sys.exit(1)
            rendered.append(_render_body_page(prep_img(img_file), page.get("text", ""), idx, px_w, px_h))

        # 3. 封底
        back = data.get("back", {})
        back_img_rel = back.get("image", "").strip()
        back_img_path = prep_img(base_dir / back_img_rel) if back_img_rel else None
        rendered.append(_render_back_page(back_img_path, back.get("ending", ""), px_w, px_h))

    out_path = Path(pdf_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    first, rest = rendered[0], rendered[1:]
    first.save(
        str(out_path),
        "PDF",
        save_all=True,
        append_images=rest,
        resolution=dpi,
        quality=95,
    )
    print(
        f"✅ 已生成完整图文 PDF（{len(rendered)} 页，{total_w_mm:.0f}×{total_h_mm:.0f}mm，{dpi}dpi）：{out_path}"
    )


def build_pdf(
    image_dir: str,
    pdf_path: str,
    width_mm: float = 203.0,
    height_mm: float = 203.0,
    dpi: int = 150,
    blank_back: bool = False,
    bleed_mm: float = 0.0,
    remove_watermark: bool = False,
):
    Image, _, _ = _load_pil()
    image_dir = os.path.abspath(image_dir)
    if not os.path.isdir(image_dir):
        print(f"错误：找不到图片目录 {image_dir}", file=sys.stderr)
        sys.exit(1)

    exts = ("*.png", "*.jpg", "*.jpeg")
    files = []
    for ext in exts:
        files.extend(glob.glob(os.path.join(image_dir, ext)))

    # 排除基准参考图与原照，并按自然页码排序
    filtered = []
    for f in set(files):
        base = os.path.basename(f).lower()
        if any(base.startswith(prefix) for prefix in EXCLUDE_PREFIXES):
            continue
        filtered.append(f)
    files = sorted(filtered, key=_natural_key)

    if not files:
        print(f"错误：目录 {image_dir} 下没有找到任何绘本页面图片（png/jpg/jpeg）", file=sys.stderr)
        sys.exit(1)

    total_w_mm = width_mm + bleed_mm * 2
    total_h_mm = height_mm + bleed_mm * 2
    px_w = int(round(total_w_mm / 25.4 * dpi))
    px_h = int(round(total_h_mm / 25.4 * dpi))

    images = []
    for f in files:
        img = Image.open(f).convert("RGB")
        if remove_watermark:
            img = crop_watermark(img)
        images.append(_fit_contain(img, px_w, px_h, bg_color="white"))

    if blank_back:
        images.append(_create_warm_gradient(px_w, px_h))

    out_path = Path(pdf_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    first, rest = images[0], images[1:]
    first.save(
        str(out_path),
        "PDF",
        save_all=True,
        append_images=rest,
        resolution=dpi,
        quality=95,
    )
    print(
        f"✅ 已生成 PDF（{len(images)} 页，{total_w_mm:.0f}×{total_h_mm:.0f}mm，{dpi}dpi）：{out_path}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="将童话绘本插画与文案合成为打印级 PDF（不依赖浏览器）。"
    )
    parser.add_argument("--book", help="book.json 路径（推荐：输出含封面标题/正文文案/页码/封底寄语的完整 PDF）")
    parser.add_argument("--out", help="输出 PDF 路径（与 --book 搭配使用）")
    parser.add_argument("--size", choices=list(SIZE_PRESETS.keys()), help="绘本尺寸预设")
    parser.add_argument("--dpi", type=int, default=None, help="输出分辨率 DPI（默认 150）")
    parser.add_argument("--bleed", type=float, default=0.0, help="四边印刷出血位（mm，默认 0，实体印刷常用 3）")
    parser.add_argument("--blank-back", action="store_true", help="目录模式下自动追加温暖纯色渐变封底页")
    parser.add_argument("--crop-watermark", action="store_true", help="等比裁去图片右下角约 6.5% 的平台水印区域")
    parser.add_argument("positional", nargs="*", help="兼容模式位置参数：<图片目录> <输出pdf> [宽mm] [高mm] [dpi]")

    args = parser.parse_args()

    if args.book:
        out_pdf = args.out or str(Path(args.book).with_suffix(".pdf"))
        build_pdf_from_book(
            book_json_path=args.book,
            pdf_path=out_pdf,
            size_override=args.size,
            dpi=args.dpi or 150,
            bleed_mm=args.bleed,
            remove_watermark=args.crop_watermark,
        )
        return

    if len(args.positional) < 2:
        parser.print_help()
        sys.exit(1)

    img_dir = args.positional[0]
    out_pdf = args.positional[1]
    w = float(args.positional[2]) if len(args.positional) > 2 else None
    h = float(args.positional[3]) if len(args.positional) > 3 else None
    dpi = args.dpi or (int(args.positional[4]) if len(args.positional) > 4 else 150)

    w_mm, h_mm = _resolve_dimensions(args.size, w, h)
    build_pdf(
        image_dir=img_dir,
        pdf_path=out_pdf,
        width_mm=w_mm,
        height_mm=h_mm,
        dpi=dpi,
        blank_back=args.blank_back,
        bleed_mm=args.bleed,
        remove_watermark=args.crop_watermark,
    )


if __name__ == "__main__":
    main()

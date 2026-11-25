#!/usr/bin/env python3
"""
童话绘本一键校验与构建工具（HTML 电子绘本 + 打印级 PDF）。

功能：
  1. 硬校验 book.json 的字段完整性、面数一致性（封面 1 + 正文 N + 封底 1 == total_pages）
     以及所有引用图片文件在磁盘上是否存在且可读。
  2. 基于 assets/picture_book_template.html 生成可单页翻页 / 双页对开 / 全书滚动的 HTML 电子绘本。
  3. 调用 scripts/build_pdf.py 生成含完整封面标题、正文文案、页码与封底寄语的打印级 PDF。

用法：
  # 仅做排版前硬校验
  python scripts/build_book.py --book ./book/book.json --check-only

  # 一键校验并输出 HTML + PDF（默认输出到 book.json 所在目录）
  python scripts/build_book.py --book ./book/book.json [--out-dir ./book] [--dpi 150] [--bleed 0]
"""
import argparse
import html
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
TEMPLATE_PATH = SKILL_ROOT / "assets" / "picture_book_template.html"

sys.path.insert(0, str(SCRIPT_DIR))
from build_pdf import SIZE_PRESETS, EXCLUDE_PREFIXES, build_pdf_from_book  # noqa: E402

VALID_PAGE_COUNTS = {
    8, 10, 12, 14, 16, 18, 20, 22, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72
}


def validate_book(book_json_path: Path) -> Dict:
    errors: List[str] = []
    warnings: List[str] = []

    if not book_json_path.is_file():
        print(f"❌ 找不到 book.json：{book_json_path}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(book_json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"❌ book.json 解析失败：{exc}", file=sys.stderr)
        sys.exit(1)

    base_dir = book_json_path.parent

    title = (data.get("title") or "").strip()
    if not title:
        errors.append("缺少必填字段：title（绘本标题）")

    size = data.get("size", "square8")
    if size not in SIZE_PRESETS:
        errors.append(f"size '{size}' 无效，可选值：{', '.join(SIZE_PRESETS)}")

    total_pages = data.get("total_pages")
    pages = data.get("pages")
    if not isinstance(pages, list) or not pages:
        errors.append("pages 必须为非空数组")
        pages = []

    actual_total = len(pages) + 2  # 封面 1 + 正文 N + 封底 1
    if total_pages is not None:
        if total_pages not in VALID_PAGE_COUNTS:
            warnings.append(f"total_pages={total_pages} 不在常见印刷面数档位中（8~72 面）")
        if actual_total != total_pages:
            errors.append(
                f"面数不匹配：承诺 total_pages={total_pages}，但实际为 封面(1) + 正文({len(pages)}) + 封底(1) = {actual_total} 面"
            )

    def check_image(rel_path: str, label: str, required: bool = True):
        rel_path = (rel_path or "").strip()
        if not rel_path:
            if required:
                errors.append(f"{label} 缺少 image 路径")
            return
        name_lower = os.path.basename(rel_path).lower()
        if any(name_lower.startswith(p) for p in EXCLUDE_PREFIXES):
            warnings.append(f"{label} 引用了疑似参考图的文件：{rel_path}")
        full_path = base_dir / rel_path
        if not full_path.is_file():
            errors.append(f"{label} 引用的图片不存在：{full_path}")
            return
        try:
            from PIL import Image
            with Image.open(full_path) as im:
                im.verify()
        except ImportError:
            pass
        except Exception as exc:
            errors.append(f"{label} 图片损坏或无法读取（{rel_path}）：{exc}")

    cover = data.get("cover") or {}
    check_image(cover.get("image", ""), "封面 (cover)", required=True)

    for idx, page in enumerate(pages, start=1):
        if not isinstance(page, dict):
            errors.append(f"正文第 {idx} 页格式必须为对象")
            continue
        check_image(page.get("image", ""), f"正文第 {idx} 页", required=True)
        if not (page.get("text") or "").strip():
            warnings.append(f"正文第 {idx} 页文案为空")

    back = data.get("back") or {}
    if (back.get("image") or "").strip():
        check_image(back.get("image", ""), "封底 (back)", required=False)

    for w in warnings:
        print(f"⚠️  警告：{w}")

    if errors:
        print("❌ 校验未通过：", file=sys.stderr)
        for err in errors:
            print(f"   - {err}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ 校验通过：《{title}》共 {actual_total} 面（尺寸：{size}），全部图片文件完整可读。")
    return data


def _replace_marker(content: str, start_marker: str, end_marker: str, replacement: str) -> str:
    pattern = re.compile(re.escape(start_marker) + r".*?" + re.escape(end_marker), re.DOTALL)
    if not pattern.search(content):
        raise RuntimeError(f"模板缺少标记：{start_marker} ... {end_marker}")
    return pattern.sub(lambda _: f"{start_marker}{replacement}{end_marker}", content, count=1)


def _format_multiline_html(text: str) -> str:
    escaped = html.escape(text.strip())
    return escaped.replace("\r\n", "\n").replace("\n", "<br>")


def build_html(data: Dict, book_dir: Path, out_html_path: Path):
    if not TEMPLATE_PATH.is_file():
        print(f"❌ 找不到 HTML 模板：{TEMPLATE_PATH}", file=sys.stderr)
        sys.exit(1)

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    title = data.get("title", "我的童话故事").strip()
    subtitle = (data.get("subtitle") or "").strip()
    size = data.get("size", "square8")
    w_mm, h_mm = SIZE_PRESETS[size]

    def rel_src(img_rel: str) -> str:
        full = (book_dir / img_rel).resolve()
        try:
            rel = os.path.relpath(full, out_html_path.parent.resolve())
        except ValueError:
            rel = str(full)
        return rel.replace("\\", "/")

    blocks: List[str] = []

    # 封面
    cover_img = rel_src(data["cover"]["image"])
    sub_html = f'\n          <div class="subtitle">{_format_multiline_html(subtitle)}</div>' if subtitle else ""
    blocks.append(
        f"""    <!-- 封面 -->
    <div class="page cover">
      <div class="art">
        <img src="{html.escape(cover_img)}" alt="封面">
        <div class="cover-overlay">
          <h1>{html.escape(title)}</h1>{sub_html}
        </div>
      </div>
    </div>"""
    )

    # 正文页
    for idx, page in enumerate(data["pages"], start=1):
        img_src = rel_src(page["image"])
        text_html = _format_multiline_html(page.get("text", ""))
        blocks.append(
            f"""    <!-- 第 {idx} 页 -->
    <div class="page">
      <div class="art"><img src="{html.escape(img_src)}" alt="第 {idx} 页"></div>
      <div class="text">
        {text_html}
        <span class="page-no">— {idx} —</span>
      </div>
    </div>"""
        )

    # 封底
    back = data.get("back") or {}
    back_img_rel = (back.get("image") or "").strip()
    ending = (back.get("ending") or "").strip()
    back_img_tag = f'\n        <img src="{html.escape(rel_src(back_img_rel))}" alt="封底">' if back_img_rel else ""
    ending_html = f'<div class="ending">{_format_multiline_html(ending)}</div>' if ending else ""
    blocks.append(
        f"""    <!-- 封底 -->
    <div class="page back">
      <div class="art">{back_img_tag}
        <div class="back-overlay">
          {ending_html}
        </div>
      </div>
    </div>"""
    )

    rendered = template
    rendered = _replace_marker(rendered, "<!--__BOOK_TITLE__-->", "<!--__BOOK_TITLE_END__-->", html.escape(title))
    rendered = _replace_marker(rendered, "<!--__BOOK_HEADER__-->", "<!--__BOOK_HEADER_END__-->", html.escape(title))
    rendered = _replace_marker(
        rendered,
        "/*__PAGE_SIZE_CSS__*/",
        "/*__PAGE_SIZE_CSS_END__*/",
        f"{w_mm:g}mm {h_mm:g}mm",
    )
    rendered = _replace_marker(rendered, "/*__SIZE_CLASS__*/", "/*__SIZE_CLASS_END__*/", f"size-{size}")
    rendered = _replace_marker(
        rendered,
        "<!--__BOOK_PAGES__-->",
        "<!--__BOOK_PAGES_END__-->",
        "\n" + "\n\n".join(blocks) + "\n    ",
    )

    out_html_path.parent.mkdir(parents=True, exist_ok=True)
    out_html_path.write_text(rendered, encoding="utf-8")
    print(f"✅ 已生成可翻页 HTML 电子绘本：{out_html_path}")


def _safe_filename(title: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]+', "_", title).strip()
    return cleaned or "picture_book"


def main():
    parser = argparse.ArgumentParser(description="童话绘本一键校验与构建工具（HTML + 打印级 PDF）。")
    parser.add_argument("--book", required=True, help="book.json 路径")
    parser.add_argument("--out-dir", help="输出目录（默认与 book.json 同目录）")
    parser.add_argument("--name", help="输出文件名前缀（默认使用绘本标题）")
    parser.add_argument("--dpi", type=int, default=150, help="PDF 分辨率 DPI（默认 150）")
    parser.add_argument("--bleed", type=float, default=0.0, help="PDF 四边出血位 mm（默认 0）")
    parser.add_argument("--check-only", action="store_true", help="仅校验 book.json 与图片，不生成文件")
    parser.add_argument("--skip-pdf", action="store_true", help="仅生成 HTML，跳过 PDF 合成")

    args = parser.parse_args()
    book_path = Path(args.book).resolve()
    data = validate_book(book_path)

    if args.check_only:
        return

    out_dir = Path(args.out_dir).resolve() if args.out_dir else book_path.parent
    stem = _safe_filename(args.name or data["title"])

    html_path = out_dir / f"{stem}.html"
    build_html(data, book_path.parent, html_path)

    if not args.skip_pdf:
        pdf_path = out_dir / f"{stem}.pdf"
        build_pdf_from_book(
            book_json_path=str(book_path),
            pdf_path=str(pdf_path),
            dpi=args.dpi,
            bleed_mm=args.bleed,
        )


if __name__ == "__main__":
    main()

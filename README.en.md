# workbuddy-skill-picture-book

[中文](README.md) | English

**Fairy Tale Picture Book (Photo-Customized) / 童话故事绘本（照片定制）** — A WorkBuddy skill package (compatible with Agent Skill conventions) for creating personalized fairy tale picture books from uploaded photos.

Turn an uploaded portrait or group photo into the protagonist(s) of an original fairy tale, craft a complete page-by-page script, generate style-consistent illustrations across every spread, and deliver both an **interactive HTML e-book** and a **print-ready PDF**.

---

## Key Features

- **Photo-Personalized Protagonist(s) (Single & Multi-Character)**
  - Supports single-protagonist stories as well as multi-character scenes featuring **2 or more human characters** (families, parent-child, siblings, friends).
  - Cartoonizes uploaded photos into a unified illustration style while preserving recognizable facial features, hairstyles, and signature details.
- **End-to-End Cross-Page Consistency System**
  - **Story Bible First**: Locks character appearances, visual anchors, scene lists (with baked-in time-of-day and lighting), prop-holding timelines, and state continuity before scripting any page.
  - **Multi-Tier Reference Image Reuse**: Reuses single-character reference sheets, synthesized all-character group reference sheets, and dedicated reference sheets for 4 high-drift element types (core props/vehicles, animal/fantasy sidekicks, fixed centerpiece objects, and recurring plot props) via `image-to-image`.
  - **Positive Whitelist Prompting**: Names every character with individual positions and actions in group scenes, explicitly declares always-worn gear, and isolates progressive states across similar characters to avoid missing characters, look-alike faces, or prop drift.
  - **Generate-and-Verify Loop**: Inspects illustrations immediately during generation for character, prop, action, and lighting consistency, and validates file existence, page count, and page-to-image mapping before layout.
- **Flexible Formats & Illustration Styles**
  - **4 Illustration Styles**: Soft Watercolor (default), Bright Cartoon, Realistic Illustration, and Beautiful Storybook.
  - **4 Print Sizes**: Square 8" (default), Square 10", Landscape 12", and Portrait 12".
  - **21 Standard Page Counts**: Supports 8–72 pages/sides (default 12 pages).
- **Dual Deliverable Formats**
  - **HTML E-Book**: Responsive browser-ready storybook template with built-in print/PDF export support.
  - **Print-Ready PDF**: Assembled directly from page images using pure Python + Pillow (`scripts/build_pdf.py`) — no headless browser required, reliable across platforms, and compact in file size.

---

## Showcase

Examples below are generated from a real 20-page family storybook (*Starlight Rescue Team*, Landscape 12", multi-character family cast) — all visuals are AI-painted illustrations:

### HTML E-Book Layout Preview

![HTML E-Book Layout Preview](docs/images/demo_html_preview.jpg)

### Reference Sheet Reuse & Cross-Page Consistency

![Reference Sheet Reuse and Cross-Page Consistency](docs/images/demo_consistency.jpg)

---

## Repository Structure

```text
workbuddy-skill-picture-book/
├── SKILL.md                           # Core skill entry (WorkBuddy spec, v2.3.0): 4-step workflow & CLI triggers
├── assets/
│   └── picture_book_template.html     # Interactive HTML e-book template (single-page flip, double spread, scroll & print)
├── docs/
│   └── images/                        # Showcase images for README
│       ├── demo_html_preview.jpg
│       └── demo_consistency.jpg
├── references/
│   ├── story_prompts.md               # 4 Story Blueprints, complexity budget, story_plan.json schema & specs
│   ├── consistency_rules.md           # Identity + Look decoupling, anti-kinship-bias, anti-pose-lock & 4 ref types
│   └── qa_checklist.md                # 4 quality gates & 5-question fact-answer QA checklist
├── scripts/
│   ├── compile_prompts.py             # story_plan.json validator + zero-loss prompt compiler + book.json generator
│   ├── build_book.py                  # One-command book.json validator + HTML & printable PDF builder
│   └── build_pdf.py                   # Pillow-based full-text printable PDF builder (backwards-compatible dir mode)
├── LICENSE                            # Apache License 2.0
├── README.md                          # Chinese README
└── README.en.md                       # English README
```

---

## Book Specifications

### 1. Illustration Styles

| Style | Characteristics |
|-------|----------------|
| **Soft Watercolor** *(default)* | Gentle pastel palette, hand-painted texture, dreamy and warm classic storybook feel |
| **Bright Cartoon** | Clean bold outlines, vibrant saturated colors, cute rounded shapes for younger kids |
| **Realistic Illustration** | Soft natural lighting, rich textures, higher portrait likeness fidelity |
| **Beautiful Storybook** | Delicate painterly strokes, soft dreamy lighting, warm emotional mood |

### 2. Print Sizes & Recommended Aspect Ratios

| Size Name | `size` Arg | Print Dimensions | Recommended Generation Aspect Ratio |
|-----------|------------|------------------|-------------------------------------|
| **Square 8"** *(default)* | `square8` | ~203mm × 203mm | `1:1` |
| **Square 10"** | `square10` | ~254mm × 254mm | `1:1` |
| **Landscape 12"** | `landscape12` | ~305mm × 229mm | `4:3` or `3:2` |
| **Portrait 12"** | `portrait12` | ~229mm × 305mm | `3:4` or `2:3` |

### 3. Page Counts (Sides)

- **Supported values**: `8 / 10 / 12 / 14 / 16 / 18 / 20 / 22 / 24 / 28 / 32 / 36 / 40 / 44 / 48 / 52 / 56 / 60 / 64 / 68 / 72` pages (default **12**).
- **Page breakdown**: Total pages = Front Cover (`1`) + Story Body (`Total - 2`) + Back Cover (`1`).
- **File naming**: `page_01_cover.png` for the front cover, followed by `page_02.png`, `page_03.png`, ... for body pages (the back cover can use the warm gradient template or a dedicated image).

---

## Workflow

The skill follows a strict four-step closed loop engineered to perform reliably across both frontier and lightweight models:

1. **Photo Pre-Check & Creative Specifications**
   - Evaluate uploaded photos for clarity, angle, and headcount (1–4 characters work best) and confirm **illustration style, book size, page count, and story theme/source**.
2. **[Checkpoint 1] Combined Profile, Look & Script Confirmation → `compile_prompts.py`**
   - Confirm **objective character profiles (exact numeric age, gender, relative heights) + outfit `Looks` (1–3 looks supporting seasonal changes, barefoot wading, or costume swaps) + page captions** in a single user checkpoint.
   - Write `story_plan.json` and run `scripts/compile_prompts.py` to auto-synthesize bias-free subject tags (blocking `son/daughter` juvenile shrinkage on adults), verify zero missing character actions and 100% caption-noun coverage, and output `prompts_manifest.md` + `book.json`.
3. **[Checkpoint 2] Approve Standing Look Sheets + Sample Pages → Batch Generation**
   - Generate full-body standing `Look` reference sheets (chained from `look_1` to lock faces and heights across outfit changes) + element sheets + **cover & Page 1 samples** for user sign-off, then generate remaining pages in batches of 2–3 with 5-question fact-answer QA.
4. **Automated Validation, Dual Export & Single-Page Revisions**
   - Run `scripts/build_book.py` to validate and export both the interactive HTML e-book and full-text printable PDF (with optional `--crop-watermark` & `--bleed`). Supports targeted single-page redraws and one-command repackaging.

---

## Installation & Usage

### Use as a WorkBuddy Skill

1. **Clone or download this repository into your WorkBuddy skills directory**:
   ```bash
   git clone https://github.com/stevenzyk/workbuddy-skill-picture-book.git ~/.workbuddy/skills/fairy-tale-picture-book
   ```
   > Alternatively, package the skill files as a `.zip` archive (with top-level folder `fairy-tale-picture-book/`) and upload it via WorkBuddy desktop or the WorkBuddy Open Platform.

2. **Trigger in conversation**:
   Upload a clear, well-lit front-facing portrait or family photo and describe your book request, for example:
   - *"Turn this photo of my child into an 8-inch square, 12-page forest adventure fairy tale picture book in soft watercolor style."*
   - *"Create a printable 20-page landscape 12-inch family fairy tale picture book based on this family photo."*

### Run the Compiler, Builder & PDF Scripts Standalone

**Prerequisite**:
```bash
pip install Pillow
```

**Full Deterministic Pipeline (`story_plan.json` → `prompts_manifest.md` + `book.json` → HTML + PDF)**:
```bash
# 1. Validate story_plan.json, compile zero-loss ImageGen prompts, and auto-generate book.json
python scripts/compile_prompts.py --plan ./book/story_plan.json

# 2. Validate page count & disk images after image generation
python scripts/build_book.py --book ./book/book.json --check-only

# 3. Generate interactive HTML e-book + full-text printable PDF (optional --crop-watermark & --bleed 3)
python scripts/build_book.py --book ./book/book.json --out-dir ./book --dpi 150 --crop-watermark --bleed 3
```

**Legacy Mode: Stitch an image directory directly into a PDF (automatically excludes `ref_*` sheets)**:
```bash
# Square 8" (203mm × 203mm, 150dpi)
python scripts/build_pdf.py ./book ./book_8inch.pdf --size square8

# Landscape 12" (305mm × 229mm, 150dpi) with watermark crop & auto warm-gradient back cover
python scripts/build_pdf.py ./book ./book_12inch.pdf 305 229 150 --crop-watermark --blank-back
```

---

## Maintenance Guidelines

When iterating on or extending this skill, follow the **"Separate Rules from Story Content"** and **Deterministic Code Guardrails** principles:

- **`SKILL.md`**: Keep lean with the 4-step workflow, 2 user checkpoints, and CLI commands.
- **`scripts/compile_prompts.py` & `scripts/build_book.py`**: Handle prompt assembly, placeholder expansion, noun checks, and layout validation deterministically in Python.
- **`references/`**: Maintain reusable story blueprints, Identity + `Look` rules, and fact-answer QA checklists.

---

## Privacy & License

- **Privacy & Portraits**: User-uploaded personal photos must be used strictly for creating the requested picture book and never shared externally.
- **Author**: Steven的能量场 (Skill `v2.3.0`)
- **License**: Licensed under the [Apache License 2.0](LICENSE).

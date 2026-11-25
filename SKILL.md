---
name: fairy-tale-picture-book
display_name: 童话故事绘本（照片定制）
display_name_en: Fairy Tale Picture Book
description: 将用户上传的人物照片变成童话故事绘本主角，创作完整童话故事并生成可翻页 HTML 电子绘本与可打印装订的 PDF 绘本。支持单人主角与多人物同框（全家福、亲子、兄弟、朋友），内置故事圣经、多级基准图复用与全流程防漂移机制。
description_zh: 把人物照片变成童话绘本主角，创作完整故事并生成可翻页 HTML 电子绘本与可打印 PDF。支持单人或多人同框，内置跨页一致性防漂移闭环。
description_en: Turn personal photos into fairy tale picture book protagonists, write a complete story, and deliver both an interactive HTML e-book and a print-ready PDF with built-in cross-page consistency.
examples_zh:
  - "把这张宝宝照片做成一本方款 8 寸、12 面的森林冒险童话绘本，温馨水彩风"
  - "用这张全家福定制一本横款 12 寸、20 面的可打印亲子绘本，写实插画风"
  - "我有一个故事大纲，帮我结合孩子照片扩写成 16 面唯美绘本并导出 PDF"
examples_en:
  - "Turn this child photo into an 8-inch square, 12-page forest adventure picture book in soft watercolor style"
  - "Create a printable 20-page landscape 12-inch family fairy tale book from this family photo"
  - "Expand my story outline with this portrait into a 16-page printable storybook PDF"
version: 2.1.0
author: Steven的能量场
agent_created: true
---

# 童话故事绘本（人物照片定制）

将用户上传的人物照片融入原创童话故事，通过「需求确认 → 故事圣经与脚本 → 基准图与插画生成 → 自动化校验与双格式交付」四步闭环，输出**可翻页浏览的 HTML 电子绘本**与**含完整图文排版的可打印 PDF**。

## 何时使用本技能

- 用户上传人物照片（单人或全家福/多人合照），希望定制个性化童话绘本或可打印实体书素材。
- 若用户表达了意图但尚未上传照片，先礼貌请用户提供一张正面、清晰、光线良好的人像照片再继续。

---

## 核心工作流（四步不可跳步闭环）

### 第一步：确认创作需求（4 项必问）

动手前用 `AskUserQuestion`（或简洁对话）一次性确认以下 4 项关键信息，**尺寸与页数不可擅自替用户拍板**（若用户未明确说明而采用默认值，交付时必须显式注明所用的默认值）：

1. **插画风格**：温馨水彩风（默认） / 明亮卡通风 / 写实插画风 / 唯美绘本风。
2. **绘本尺寸**（同步决定生图画幅、HTML `@page` 与 PDF 印刷尺寸）：

| 尺寸名称 | `size` 参数 | 印刷尺寸 | 推荐生图画幅 |
|---|---|---|---|
| **方款 8 寸**（默认） | `square8` | 203mm × 203mm | `1:1` |
| **方款 10 寸** | `square10` | 254mm × 254mm | `1:1` |
| **横款 12 寸** | `landscape12` | 305mm × 229mm | `4:3` 或 `3:2` |
| **竖款 12 寸** | `portrait12` | 229mm × 305mm | `3:4` 或 `2:3` |

3. **页数（面数）**：可选 **8 / 10 / 12 / 14 / 16 / 18 / 20 / 22 / 24 / 28 / 32 / 36 / 40 / 44 / 48 / 52 / 56 / 60 / 64 / 68 / 72 面**（默认 **12 面**）。向用户说明：总面数包含封面 1 面 + 封底 1 面，正文面数 = `总面数 - 2`。
4. **故事主题与来源**：AI 原创（冒险 / 勇气 / 友谊 / 善良 / 成长 / 魔法 / 四季旅行）或基于用户大纲扩写。

---

### 第二步：编写「故事圣经」与分页脚本（先确认，后生图）

> **执行本步前，务必先读取本技能目录下的两份参考文件**：
> - `@references/story_prompts.md`（故事圣经模板、分页脚本模板、风格前缀与 `book.json` 规范）
> - `@references/consistency_rules.md`（防漂移、相对身高锁死、防摆拍、跨季节换装等细则）

1. **分析照片**：用 `ViewImage` 提取人物外貌、年龄感与相对身高差写入故事圣经。
2. **编写故事圣经（Story Bible）**：必须包含四份清单——人物设定（含相对身高、恒穿装备或分季服装）、视觉锚点（固定英文描述）、场景清单（内嵌昼夜/光线词）、道具持有与状态连续性时间线。
   - **成人身高锁死红线**：若主角含成年子女/成年家人，风格前缀中**不要写 `children's book`**（改用 `storybook illustration`），并在角色锚点显式写死 `full-grown adult, as tall as the father/mother, NOT a child`，防止模型把成人子女缩水成小学生。
   - **季节与场景常识红线**：单日故事服装固定；**跨季节故事（如四季旅行）必须按季节设分季服装锚点**，严禁冬天雪地穿短袖/无袖；踩水场景全员一致光脚（`all barefoot`），严禁有人穿运动鞋踩海水。
3. **编写分页脚本（强制填空防漏项）**：每页必须同时列出：
   - **文案（中文）**（1–3 句，30–60 字）
   - **文案核心名词清单**（文案里出现的每个具体物体/环境如「午饭食物」「树荫」「贝壳」，必须 **100%** 写入英文 Prompt，禁止漏画或偷换成别物）
   - **视线与互动方向**（除封面/合影结局外，强制写清人物看谁/看什么，如 `looking down at the picnic food, candid natural moment, NOT looking at the camera`，打破全员直视镜头的「棚拍贴图感」）
4. **用户确认红线**：**必须先将完整分页脚本展示给用户并获得确认，才可进入第三步生图**；禁止未经确认批量生图。

---

### 第三步：生成基准图与各页插画（事实反问式边生边审）

> **执行本步前，先读取本技能目录下的 `@references/qa_checklist.md`**。

1. **先建基准图，再画正页（铁律）**：
   - **人物基准图**：用 `ImageGen`（`image-to-image`，低保真 `low`）将照片转绘为干净纯色背景的基准图。**≥2 个人类角色时，必须优先合成「自然站姿全身」的全员基准图（`ref_family.png`）**，以锁死相对身高并避免坐姿棚拍导致全书机械复刻坐姿。
   - **四类要素基准图**：反复出现的①核心载体/道具、②动物/幻想配角、③核心固定物体、④贯穿性剧情道具，各自生成一张干净特写基准图（`ref_*.png`），并在锚点中相对人体部位锁死尺寸（如 `palm-sized`，防道具画得像人头一样大）。有分阶段状态的角色/道具采用初始/无状态形态。
2. **逐页生图五段式 Prompt**：
   - 公式：`风格前缀 + 人物锚点（多人同框逐个点名位置与动作、含相对身高） + 道具/配角锚点（含持有状态） + 场景锚点（内嵌光词） + 本页核心动作与互动视线`。
   - **参考图传入**：出现人物的页面以人物/全员基准图作 `image1`，关键道具/配角/固定物基准图作 `image2`/`image3`（上限 3 张，低保真）。仅纯风景/空镜页可用纯文生图，且不附带人物照片参考。
   - **封面构图**：显式写 `leave clear empty space at the top of the image for the title text`，人物置于画面中下部，避免顶部标题遮挡面部。
   - **命名规范**：封面 `page_01_cover.png`，正文 `page_02.png` ～ `page_{N+1}.png`，可选封底 `page_{N+2}_back.png`（与 `ref_*.png` 区分）。
3. **事实反问式审图（每 1–3 页必做，严禁走过场）**：
   每生成 1–3 页立刻用 `ViewImage` 逐条回答以下 5 个事实问题，任意一项异常**当场重生成**：
   1. 画面共几人？成人身高是否与设定年龄一致（有无缩水成儿童或撞脸）？
   2. 人物眼睛在看哪里？（正文页有无全员直视镜头、复刻基准图坐姿的「棚拍贴图感」？）
   3. 本页文案的核心名词（如午饭/树荫/西瓜）是否在图里肉眼清晰可见？
   4. 衣鞋与当前天气/场景是否符合常识（有无雪地短袖、穿鞋踩水）？
   5. 核心道具尺寸比例、人物肢体数量、分阶段状态是否全部正常？

---

### 第四步：自动化校验与双格式交付（严禁自写构建脚本）

> **强制约束**：**严禁自行编写 `make_print_pages.py`、`verify.py` 或手拼 HTML/PDF 代码**。必须先定位本技能目录（`<SKILL_DIR>`，即当前 `SKILL.md` 所在目录），直接调用技能内置脚本 `scripts/build_book.py`，确保产出具备单页翻页/双页对开/滚动模式与完整图文排版的 PDF。

1. **生成 `book.json`**：按 `@references/story_prompts.md` 第三节格式在绘本目录下写入 `book.json`（含 `title`、`subtitle`、`size`、`total_pages`、`cover`、`pages`、`back`）。
2. **执行排版前硬校验**：
   ```bash
   python <SKILL_DIR>/scripts/build_book.py --book ./book/book.json --check-only
   ```
   并核对每页图片内容与页码文案一一对应（封面不挡脸、结局图文一致）。
3. **一键生成可翻页 HTML 与完整图文 PDF**：
   ```bash
   python <SKILL_DIR>/scripts/build_book.py --book ./book/book.json --out-dir ./book --dpi 150 --crop-watermark
   ```
   - `--crop-watermark`：如生图工具在右下角带有平台水印，开启后自动等比裁去右下角 6.5% 水印区，**HTML 与 PDF 同步生效且不裁人物头部**。
   - `--bleed 3`：如需实体印刷 3mm 出血位，按需追加。
   - 依赖：`pip install Pillow`（纯 Pillow 合成，不依赖 Playwright/Chromium）。
   - 如仅需将纯图片目录合成为 PDF，可运行兼容命令：
     ```bash
     python <SKILL_DIR>/scripts/build_pdf.py <图片目录> <输出.pdf> --size landscape12 --dpi 150 --crop-watermark
     ```
4. **交付文件**：使用 `present_files` 展示生成的 HTML 电子绘本与 PDF 文件，并在交付说明中列出成品尺寸、总面数与插画风格。

---

## 参考资料与工具文件

- `@references/story_prompts.md`：故事圣经模板、分页脚本模板、`book.json` 模板、4 种中性风格前缀、尺寸画幅对照表。
- `@references/consistency_rules.md`：正面写全白名单、成人身高锁死、防棚拍贴图感、季节换装常识与四类基准图复用细则。
- `@references/qa_checklist.md`：5 题事实反问审图法与排版前全书总检清单。
- `assets/picture_book_template.html`：支持单页翻页/双页对开/滚动阅读与 `<img>` 打印样式的 HTML 绘本模板。
- `scripts/build_book.py`：绘本硬校验 + 水印处理 + HTML/PDF 一键构建脚本。
- `scripts/build_pdf.py`：基于 Pillow 的打印级图文 PDF 合成脚本。

---

## 隐私与维护规范

- **隐私与肖像**：用户上传的人物照片仅用于本次绘本创作，严禁擅自外传或挪作他用。
- **规则与故事分离**：`SKILL.md` 与 `references/consistency_rules.md` 只写可迁移的通用原则与占位符（`<角色>`、`<道具>`、`<场景>`）；写完做「换词测试」，把具体名词换成无关词仍成立才算通用规则，否则归入示例并显式标注。

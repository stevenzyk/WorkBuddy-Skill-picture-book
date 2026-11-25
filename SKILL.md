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
version: 2.0.0
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
4. **故事主题与来源**：AI 原创（冒险 / 勇气 / 友谊 / 善良 / 成长 / 魔法）或基于用户大纲扩写。

---

### 第二步：编写「故事圣经」与分页脚本（先确认，后生图）

开始前加载模板与防漂移规范：
- `@references/story_prompts.md`（故事圣经模板、分页脚本模板、风格前缀与 `book.json` 规范）
- `@references/consistency_rules.md`（多角色防撞脸、四类高漂移元素、正面写全白名单等细则）

1. **分析照片**：使用 `ViewImage` 观察人物照片，提取固定外貌特征（发型、发色、脸型、五官、年龄感、身高差）写入故事圣经。
2. **编写故事圣经（Story Bible）**：必须包含四份清单——人物设定（含恒穿装备与多角色区分句）、视觉锚点（固定英文描述，全书一字不改复用）、场景清单（内嵌昼夜/光线词与固定背景细节）、道具持有与状态连续性时间线。
3. **编写分页脚本**：每页 1 个独立场景，正文文案精炼（1–3 句，30–60 字），画面描述与中文文案必须指向**同一核心动作**，相邻两页避免雷同构图。
4. **用户确认红线**：**必须先将完整分页脚本展示给用户并获得确认，才可进入第三步生图**；禁止未经确认批量生图。

---

### 第三步：生成基准图与各页插画（边生成边核验）

所有一致性细则严格遵循 `@references/consistency_rules.md`，核验流程遵循 `@references/qa_checklist.md`：

1. **先建基准图，再画正页（铁律）**：
   - **人物基准图**：用 `ImageGen`（`image-to-image`，`input_fidelity: low`）将照片卡通化为干净纯色背景的主角基准图（`ref_main.png`）。若故事含 **≥2 个人类角色**，必须先合成一张**全员同框基准图**（`ref_family.png`）校准身高差与五官比例。
   - **四类要素基准图**：故事中反复出现的①核心载体/道具、②动物/幻想配角、③核心固定物体、④贯穿性剧情道具，各自生成一张干净特写基准图（`ref_*.png`）；有分阶段状态的角色/道具采用初始/无状态形态。
2. **逐页生图五段式 Prompt**：
   - 拼接公式：`风格前缀 + 人物锚点（多人同框逐个点名位置与动作） + 道具/配角锚点（含持有状态） + 场景锚点（内嵌光词） + 本页具体动作与空间关系`。
   - **必须传入参考图**：所有出现人物的页面以人物/全员基准图作 `image1`，关键道具/动物/固定物基准图作 `image2`/`image3`（`input_fidelity: low`，上限 3 张）。仅纯风景/空镜页可用纯文生图，且不附带人物照片参考以防带入实景背景。
   - **封面构图**：Prompt 显式写 `leave clear empty space at the top of the image for the title text`，让人物位于画面中下部，避免顶部标题遮挡面部。
   - **命名规范**：封面 `page_01_cover.png`，正文依次 `page_02.png` ～ `page_{N+1}.png`，可选封底 `page_{N+2}_back.png`（与 `ref_*.png` 区分命名）。
3. **边生成边核验**：每生成 1–3 页立即用 `ViewImage` 按 `@references/qa_checklist.md` 阶段 A 检查人数、五官、肢体、道具状态与图文对应，发现问题当场重生成，禁止攒到最后统一返工。

---

### 第四步：自动化校验、排版与双格式交付

完成全部插画后，不再手拼 HTML 或纯图 PDF，统一通过 `book.json` + 构建脚本交付：

1. **生成 `book.json`**：按 `@references/story_prompts.md` 第三节格式在绘本目录下写入 `book.json`（含 `title`、`subtitle`、`size`、`total_pages`、`cover`、`pages`、`back`）。
2. **执行排版前硬校验**：
   ```bash
   python scripts/build_book.py --book ./book/book.json --check-only
   ```
   同时对照 `@references/qa_checklist.md` 阶段 B/C，确认每页图片内容与页码文案一一对应。
3. **一键生成可翻页 HTML 与打印级 PDF**：
   ```bash
   python scripts/build_book.py --book ./book/book.json --out-dir ./book --dpi 150
   ```
   - 自动基于 `assets/picture_book_template.html` 生成支持**单页翻页 / 双页对开 / 全书滚动**且标题顶置的 HTML 电子绘本（采用 `<img>` 标签，浏览器打印不丢图）。
   - 自动调用 `scripts/build_pdf.py`（纯 Pillow，不依赖 Playwright/Chromium）输出**含完整封面标题、正文文案、页码与封底寄语**的打印级 PDF；如需实体印刷出血位，可加 `--bleed 3`。
   - 若仅需把纯图片目录合成 PDF，也可直接运行兼容命令：
     ```bash
     python scripts/build_pdf.py <图片目录> <输出.pdf> --size landscape12 --dpi 150
     ```
4. **交付文件**：使用 `present_files` 展示 HTML 电子绘本与 PDF 打印文件，并在交付说明中列出成品尺寸、总面数与插画风格。

---

## 参考资料与工具文件

- `@references/story_prompts.md`：故事圣经模板、分页脚本模板、`book.json` 模板、4 种风格前缀、尺寸画幅对照表。
- `@references/consistency_rules.md`：正面写全白名单、多角色防撞脸、恒穿装备、状态连续性与四类基准图复用细则。
- `@references/qa_checklist.md`：边生成边核验与排版前全书总检清单。
- `assets/picture_book_template.html`：支持单页/对开/滚动与打印样式的 HTML 电子绘本模板。
- `scripts/build_book.py`：绘本硬校验 + HTML/PDF 一键构建脚本。
- `scripts/build_pdf.py`：基于 Pillow 的打印级图文 PDF 合成脚本（依赖 `pip install Pillow`）。

---

## 隐私与维护规范

- **隐私与肖像**：用户上传的人物照片仅用于本次绘本创作，严禁擅自外传或挪作他用。
- **规则与故事分离（改 Skill 必读）**：
  - **规则回答「怎么做」，示例回答「某个具体故事的 X 是什么」**。
  - `SKILL.md` 与 `references/consistency_rules.md` 中只写可迁移的通用原则与占位符（`<角色>`、`<道具>`、`<场景>`）；写完做「换词测试」，把具体名词换成无关词仍成立才算通用规则，否则归入示例并显式标注。

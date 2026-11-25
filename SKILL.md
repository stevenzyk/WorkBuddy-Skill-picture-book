---
name: fairy-tale-picture-book
display_name: 童话故事绘本（照片定制）
display_name_en: Fairy Tale Picture Book
description: 将用户上传的人物照片变成童话故事绘本主角，创作完整童话故事并生成可翻页 HTML 电子绘本与可打印装订的 PDF 绘本。支持单人主角与多人物同框（全家福、亲子、兄弟、朋友），内置照片体检、样张先验确认、多级基准图复用与全流程防漂移机制。
description_zh: 把人物照片变成童话绘本主角，创作完整故事并生成可翻页 HTML 电子绘本与可打印 PDF。支持单人或多人同框，内置照片体检、样张先验确认与跨页一致性防漂移闭环。
description_en: Turn personal photos into fairy tale picture book protagonists, write a complete story, and deliver both an interactive HTML e-book and a print-ready PDF with photo pre-check, sample-page approval, and built-in cross-page consistency.
examples_zh:
  - "把这张宝宝照片做成一本方款 8 寸、12 面的森林冒险童话绘本，温馨水彩风"
  - "用这张全家福定制一本横款 12 寸、16 面的海边野餐亲子绘本，唯美绘本风"
  - "我有一个故事大纲，帮我结合孩子照片扩写成 16 面可打印绘本并导出 PDF"
examples_en:
  - "Turn this child photo into an 8-inch square, 12-page forest adventure picture book in soft watercolor style"
  - "Create a printable 16-page landscape 12-inch family beach picnic book from this family photo"
  - "Expand my story outline with this portrait into a 16-page printable storybook PDF"
version: 2.2.0
author: Steven的能量场
agent_created: true
---

# 童话故事绘本（人物照片定制）

将用户上传的人物照片融入原创童话故事，通过「照片体检与需求确认 → 故事圣经与脚本确认 → 基准图与 2 页样张先验 → 批量生图与一键交付（支持单页精修）」闭环，输出**可翻页浏览的 HTML 电子绘本**与**含完整图文排版的可打印 PDF**。

## 何时使用本技能

- 用户上传人物照片（单人或全家福/多人合照），希望定制个性化童话绘本或可打印实体书素材。
- 若用户尚未上传照片，先礼貌请用户提供一张正面、清晰、光线良好的人像照片再继续。

---

## 核心工作流（四步不可跳步闭环）

### 第一步：照片体检与确认创作需求

1. **先做照片体检（收到照片后立即用 `ViewImage` 评估）**：
   - **清晰度与角度**：若照片模糊、严重逆光、五官被遮挡或大角度侧脸，礼貌提醒效果会受限，建议换一张清晰正面照。
   - **人数边界**：AI 稳定同框上限为 **1–4 人**；若合照超过 4 人，建议用户选定 1–4 位核心主角，其余家人仅在关键页客串，避免强行每页多人同框导致崩坏。
2. **确认 4 项创作规格（必问，尺寸与页数不可擅自拍板）**：
   - **插画风格**：温馨水彩风（默认，容错率最高） / 明亮卡通风 / 唯美绘本风 / 写实插画风（人物还原度高，但对比例与光影更敏感；多人合照优先推荐温馨水彩或唯美绘本风）。
   - **绘本尺寸**（同步决定生图画幅、HTML `@page` 与 PDF 印刷尺寸）：

| 尺寸名称 | `size` 参数 | 印刷尺寸 | 推荐生图画幅 |
|---|---|---|---|
| **方款 8 寸**（默认） | `square8` | 203mm × 203mm | `1:1` |
| **方款 10 寸** | `square10` | 254mm × 254mm | `1:1` |
| **横款 12 寸** | `landscape12` | 305mm × 229mm | `4:3` 或 `3:2` |
| **竖款 12 寸** | `portrait12` | 229mm × 305mm | `3:4` 或 `2:3` |

   - **页数（面数）**：可选 **8 / 10 / 12 / 14 / 16 / 18 / 20 / 22 / 24 / 28 / 32 / 36 / 40 / 44 / 48 / 52 / 56 / 60 / 64 / 68 / 72 面**（默认 **12 面**；总面数含封面 1 面 + 封底 1 面，正文面数 = `总面数 - 2`；首次体验推荐 12–16 面）。
   - **故事主题与来源**：默认推荐**单日/同场景主题**（如森林冒险、海边野餐、星空露营，一致性最稳）；也支持跨季节旅行或基于用户大纲扩写。

---

### 第二步：编写「故事圣经」与分页脚本（检查点 1：确认脚本）

> **执行本步前，务必先读取本技能目录下的两份参考文件**：
> - `@references/story_prompts.md`（故事圣经模板、分页脚本模板、风格前缀与 `book.json` 规范）
> - `@references/consistency_rules.md`（防漂移、相对身高锁死、防摆拍、跨季节换装等细则）

1. **编写故事圣经（Story Bible）**：包含人物设定（含相对身高、恒穿装备或分季服装）、视觉锚点（固定英文描述）、场景清单（内嵌昼夜/光线词）、道具持有与状态连续性时间线。
   - **成人身高锁死红线**：主角含成年子女/成年家人时，风格前缀**不要写 `children's book`**（改用 `storybook illustration`），并在角色锚点写死 `full-grown adult, as tall as the father/mother, NOT a child`，防止缩水成小学生。
   - **季节与场景常识红线**：单日故事服装固定；**跨季节故事必须按季节设分季服装锚点**，严禁雪地穿短袖/无袖；踩水场景全员一致光脚（`all barefoot`），严禁有人穿运动鞋踩海水。
2. **编写分页脚本（强制填空防漏项）**：每页必须同时列出：
   - **文案（中文）**（1–3 句，30–60 字）
   - **文案核心名词清单**（文案里每个具体物体/环境如「午饭食物」「树荫」「贝壳」，必须 **100%** 写入英文 Prompt，禁止漏画或偷换）
   - **视线与互动方向**（除封面/合影结局外，强制写清人物看谁/看什么，如 `looking down at the picnic food, candid natural moment, NOT looking at the camera`，打破全员直视镜头的「棚拍贴图感」）
3. **【检查点 1】确认脚本**：**必须先将完整分页脚本展示给用户并获得确认，才可进入第三步生图**；禁止未经确认批量生图。

---

### 第三步：先验样张，再批量生图（检查点 2：确认基准图 + 2 页样张）

> **执行本步前，先读取本技能目录下的 `@references/qa_checklist.md`**。

1. **阶段 3A：生成基准图 + 2 页样张，先请用户确认（严禁直接盲跑全书）**：
   - **人物基准图**：用 `ImageGen`（`image-to-image`，低保真 `low`）转绘干净纯色背景基准图。**≥2 个人类角色时，优先合成「自然站姿全身」全员基准图（`ref_family.png`）**，锁死相对身高并避免坐姿棚拍导致全书机械复刻坐姿。
   - **要素基准图**：反复出现的①核心载体/道具、②动物/幻想配角、③核心固定物体、④贯穿性剧情道具，各自生成干净特写基准图（`ref_*.png`），锚点相对人体部位锁死尺寸（如 `palm-sized`）。有分阶段状态的角色/道具采用初始/无状态形态。
   - **试画 2 页样张**：先生成 **封面（`page_01_cover.png`）+ 1 页典型正文互动页（如 `page_02.png` 或核心互动页）**，连同基准图用 `present_files` 展示给用户确认：**长相是否认可、身高比例是否准确、画风与自然互动感是否满意**。用户确认后再批量生成其余页面；若不满意，先调基准图与风格再继续。
2. **阶段 3B：批量生成其余页面 + 事实反问审图**：
   - **五段式 Prompt 公式**：`风格前缀 + 人物锚点（多人同框逐个点名位置与动作、含相对身高） + 道具/配角锚点（含持有状态） + 场景锚点（内嵌光词） + 本页核心动作与互动视线`。
   - **参考图传入**：出现人物的页面以人物/全员基准图作 `image1`，关键道具/配角/固定物基准图作 `image2`/`image3`（上限 3 张，低保真）。纯风景/空镜页不附带人物照片参考。
   - **封面构图**：显式写 `leave clear empty space at the top of the image for the title text`，人物置于画面中下部，避免标题挡脸。
   - **命名规范**：封面 `page_01_cover.png`，正文 `page_02.png` ～ `page_{N+1}.png`，可选封底 `page_{N+2}_back.png`（与 `ref_*.png` 区分）。
   - **事实反问式审图（每 1–3 页必做）**：用 `ViewImage` 逐条回答 5 个事实问题，任意异常**当场重生成**：
     1. 画面共几人？成人身高是否与年龄一致（有无缩水成儿童或撞脸）？
     2. 人物眼睛在看哪里？（正文页有无全员直视镜头、复刻基准图坐姿的「棚拍贴图感」？）
     3. 本页文案的核心名词（如午饭/树荫/西瓜）是否在图里肉眼清晰可见？
     4. 衣鞋与当前天气/场景是否符合常识（有无雪地短袖、穿鞋踩水）？
     5. 核心道具尺寸比例、人物肢体数量、分阶段状态是否全部正常？

---

### 第四步：自动化校验、双格式交付与单页精修

> **强制约束**：**严禁自行编写 `make_print_pages.py`、`verify.py` 或手拼 HTML/PDF 代码**。必须先定位本技能目录（`<SKILL_DIR>`，即当前 `SKILL.md` 所在目录），直接调用技能内置脚本 `scripts/build_book.py`。

1. **生成 `book.json`**：按 `@references/story_prompts.md` 第三节格式在绘本目录下写入 `book.json`。
2. **排版前硬校验**：
   ```bash
   python <SKILL_DIR>/scripts/build_book.py --book ./book/book.json --check-only
   ```
   并核对每页图片内容与页码文案一一对应（封面不挡脸、结局图文一致）。
3. **一键生成可翻页 HTML 与完整图文 PDF**：
   ```bash
   python <SKILL_DIR>/scripts/build_book.py --book ./book/book.json --out-dir ./book --dpi 150 --crop-watermark
   ```
   - `--crop-watermark`：生图工具若带右下角平台水印，开启后自动等比裁去 6.5% 水印区，**HTML 与 PDF 同步生效且不裁人物头部**。
   - `--bleed 3`：如需实体印刷 3mm 出血位，按需追加。依赖：`pip install Pillow`。
   - 纯图片目录兼容命令：`python <SKILL_DIR>/scripts/build_pdf.py <图片目录> <输出.pdf> --size landscape12 --dpi 150 --crop-watermark`。
4. **交付与单页精修闭环**：
   - 使用 `present_files` 展示 HTML 电子绘本与 PDF 文件，说明成品尺寸、总面数与插画风格。
   - **主动告知用户**：如对其中某 1–2 页不满意，直接回复「第 X 页 + 修改意见」，即可仅重画该页并重新运行 `build_book.py` 一键更新 HTML 和 PDF，无需整本重做。

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

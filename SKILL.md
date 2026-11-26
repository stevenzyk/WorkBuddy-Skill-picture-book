---
name: fairy-tale-picture-book
display_name: 童话故事绘本（照片定制）
display_name_en: Fairy Tale Picture Book
description: 将用户上传的人物照片变成童话故事绘本主角，创作富有绘本文学美感的完整故事，并生成可翻页 HTML 电子绘本与可打印装订的 PDF 绘本。支持单人主角与多人物同框（全家福、亲子、兄弟、朋友），内置三种可选绘本文风、人物与造型确认、Prompt 零丢失编译器与全流程防漂移机制。
description_zh: 把人物照片变成童话绘本主角，创作有温度的绘本故事并生成可翻页 HTML 与可打印 PDF。支持单人或多人同框，内置三种绘本文风选择与跨页一致性防漂移闭环。
description_en: Turn personal photos into fairy tale picture book protagonists, craft warm literary storybooks, and deliver both an interactive HTML e-book and a print-ready PDF with deterministic prompt compilation and cross-page consistency.
examples_zh:
  - "把这张宝宝照片做成一本方款 8 寸、12 面的森林冒险童话绘本，温馨水彩风"
  - "用这张全家福定制一本横款 12 寸、16 面的海边野餐绘本，温暖收集文风"
  - "我有一个故事大纲，帮我结合家人照片扩写成四季旅行绘本并导出可打印 PDF"
examples_en:
  - "Turn this child photo into an 8-inch square, 12-page forest adventure picture book in soft watercolor style"
  - "Create a printable 16-page landscape 12-inch family beach storybook with warm poetic captions"
  - "Expand my story outline with this family photo into a printable four-seasons storybook PDF"
version: 2.4.0
author: Steven的能量场
agent_created: true
---

# 童话故事绘本（人物照片定制）

将用户上传的人物照片融入富有绘本韵味的原创故事，通过**「照片体检与规格/文风确认 → 人物造型与文学脚本合并确认（`compile_prompts.py` 编译锁死）→ 站姿基准图与样张确认 → 分批生图与 `build_book.py` 一键交付」**四步闭环，输出**可翻页 HTML 电子绘本**与**含完整图文排版的可打印 PDF**。

## 何时使用本技能

- 用户上传人物照片（单人或全家福/多人合照），希望定制个性化童话绘本或可打印实体书素材。
- 若用户尚未上传照片，先礼貌请用户提供一张正面、清晰、光线良好的人像照片再继续。
- 先定位本技能根目录 `<SKILL_DIR>`（即当前 `SKILL.md` 所在目录），后续直接调用 `<SKILL_DIR>/scripts/` 下的内置 Python 脚本。

---

## 核心工作流（两次用户确认 + 两个确定性脚本收口）

### 第一步：照片体检与创作规格确认（含绘本文风推荐）

1. **照片体检（用 `ViewImage` 观察上传照片）**：
   - 若照片模糊、严重逆光、遮挡五官或大角度侧脸，提醒换清晰正面照效果更佳。
   - **人数边界**：稳定同框上限为 **1–4 人**；超 4 人建议选 1–4 位核心主角，其余家人仅在关键页客串。
   - 识别照片中每人的**称呼、大致数字年龄、性别、相对身高关系**，供下一步核对。
2. **一次性确认 4 项规格（尺寸与页数不可擅自拍板；若用默认值须在交付时注明）**：
   - **插画风格**：温馨水彩风 `watercolor`（默认，容错最高） / 唯美绘本风 `storybook` / 明亮卡通风 `cartoon` / 写实插画风 `realistic`（多人合照优先推荐水彩或唯美绘本风）。
   - **绘本尺寸**：方款 8 寸 `square8`（203×203mm，默认） / 方款 10 寸 `square10`（254×254mm） / 横款 12 寸 `landscape12`（305×229mm） / 竖款 12 寸 `portrait12`（229×305mm）。
   - **页数（面数）**：可选 **8 / 10 / 12 / 14 / 16 / 18 / 20 / 22 / 24 / 28 / 32 / 36 / 40 / 44 / 48 / 52 / 56 / 60 / 64 / 68 / 72 面**（默认 **12 面**；含封面 1 + 封底 1，正文面数 = `总面数 - 2`；首次推荐 12–16 面）。
   - **故事方向与绘本文风**（**向用户提问时必须完整展示以下 4 项的“适用年龄 + 风格说明”，并按照片人物年龄在最契合项标注【推荐】，不可只写 4 字名称**）：
     1. **童趣韵律风 `rhythm`（适合 2–5 岁低幼宝宝）**：短句轻快、带拟声词与重复节奏，适合亲子大声朗读。
     2. **好奇寻宝风 `curiosity`（适合 5–10 岁儿童）**：开头埋下小秘密或小任务，带着悬念与对话翻页揭晓。
     3. **温暖收集风 `poetic`（适合全年龄亲子 / 全家福 / 成年家庭纪念）**：用一条温暖线索串联点滴，有轻对话与五感温度，走心不流水账。
     4. **自由发挥 / 按我的想法写 `custom`**：不指定时，按照片主角年龄自动匹配最契合的文风。

---

### 第二步：【检查点 1】合并确认档案、造型与文学脚本 → 运行 `compile_prompts.py`

> **执行本步前，务必先读取本技能目录下的两份参考文件**：
> - `@references/story_prompts.md`（绘本文学「1 锚定 + 2 禁止 + 1 增味」金标准、正反对比范例与 `story_plan.json` 模板）
> - `@references/consistency_rules.md`（角色本体与 `Look` 解耦、页级赤脚覆盖、随身小道具防巨型贴图、时间线规范）

1. **创作绘本文案铁律（「事件同源、繁简分流」，严禁写成监控画面说明书）**：
   - 先定一句话全书串珠线 `story_thread` 与每页唯一瞬间事件 `event_core`。
   - **英文描述写满细节，中文 `text_zh` 提纯文学感**：锚定本页正在发生的同一动作（防图文错位），**严禁把“红白格子/藤编/奶油白”等生图参数抄进中文台词**，禁止连续两页用 `XX 做了 YY` 汇报句，每页融入**拟声/环境声、角色短对话、触觉温度或温柔比喻**。
2. **一次性向用户展示以下 3 项并请用户确认（合并提问，避免零碎打扰）**：
   - **① 人物客观档案卡**：每人称呼、**具体数字年龄**、性别、相对身高关系。
   - **② 造型服装方案（`Looks` 1–3 套 + 单页微调）**：跨季/变装拆独立 `Look`；单页涉水赤脚、戴帽等直接用页级 `outfit_overrides_en`（含 `barefoot` 自动剥离鞋袜，防穿鞋踩浪）。
   - **③ 全书串珠线与逐页绘本文案**。
3. **用户确认后，写入 `story_plan.json` 并运行编译器（严禁手写散装长 Prompt）**：
   ```bash
   python <SKILL_DIR>/scripts/compile_prompts.py --plan ./book/story_plan.json
   ```
   - 编译器自动完成：合成客观年龄主语（拦截 `son/daughter` 防成人缩水）、校验在场角色无漏人、核验 `caption_nouns_en` 100% 进图、强制在场道具填写 `prop_states_en` 位置（随身小件标 `is_small_accessory: true` 防角落巨型相机）、拦截同一天内 `(day, time_of_day)` 时间倒流，并按封面/正文实际画框分别匹配画幅（方形绘本封面 `1:1`、正文 `4:3` 横画幅防切脚尖）。
   - 如有报错按终端提示修正直至输出 `✅ 编译通过`，自动生成 **`prompts_manifest.md`** 与 **`book.json`**。

---

### 第三步：【检查点 2】先验基准图 + 样张 → 按清单小批生图

> **执行本步前，先读取 `@references/qa_checklist.md`。全程必须严格按照 `prompts_manifest.md` 标注的 `画幅`、`Prompt` 与 `必传参考图` 调用 `ImageGen`，严禁手改或缩写！**

1. **阶段 3A：生成全套基准图 + 2 页样张，交给用户做第 2 次确认**：
   - 按清单依次生成：**全部 `Look` 平地自然站姿全身基准图**（第 2 套起传第 1 套站姿图作 `image1` 链式锁脸锁身高）+ 道具/配角基准图 + **封面 `page_01_cover.png` + 正文第 1 页 `page_02.png`**。
   - 用 `present_files` 展示给用户确认长相、身高比例、换装效果与构图留白，点头后再批量生成剩余正页。
2. **阶段 3B：小批生成剩余页面（每次 2–3 页）+ 5 题事实反问审图**：
   - 每生成 2–3 页立即用 `ViewImage` 逐页回答 `@references/qa_checklist.md` 关口 3 的 **5 个事实问题**（人数身高、视线互动与脚部留白、图文元素、衣鞋/赤脚状态、道具比例与肢体），任一异常**当场重生成**。

---

### 第四步：一键硬校验、双格式交付与单页精修（严禁自写构建脚本）

> **强制约束**：`book.json` 已由 `compile_prompts.py` 自动生成。**严禁自行编写 HTML/PDF 脚本**，直接调用内置 `build_book.py`。

1. **硬校验与一键构建 HTML + 完整图文打印级 PDF**：
   ```bash
   python <SKILL_DIR>/scripts/build_book.py --book ./book/book.json --check-only
   python <SKILL_DIR>/scripts/build_book.py --book ./book/book.json --out-dir ./book --dpi 150 --crop-watermark
   ```
   - `--crop-watermark`：自动等比裁去右下角 6.5% 水印，HTML 与 PDF 同步干净且正文裁切重心保护脚部不切边；实体印刷出血位可加 `--bleed 3`。依赖：`pip install Pillow`。
2. **交付与单页精修**：用 `present_files` 交付 HTML 与 PDF，注明尺寸、总面数、画风与文风；告知用户如需微调某页，直接报页码即可单页重画并一键重打包。

---

## 参考资料与工具文件

- `@references/story_prompts.md`：绘本文学创作金标准、3 种可选文风、4 套故事骨架与 `story_plan.json` 完整模板。
- `@references/consistency_rules.md`：角色与 `Look` 解耦、页级赤脚覆盖、随身小件防巨型贴图、时间线与防切脚规范。
- `@references/qa_checklist.md`：文学去说明书化自检与 5 题事实反问审图清单。
- `assets/picture_book_template.html`：支持单页翻页/双页对开/滚动阅读与 `<img>` 打印样式的 HTML 模板。
- `scripts/compile_prompts.py`：`story_plan.json` 校验器 + 零丢失 Prompt 编译器 + `book.json` 生成器。
- `scripts/build_book.py` & `scripts/build_pdf.py`：硬校验、去水印、防切脚排版与 HTML/PDF 构建器。

---

## 隐私与维护规范

- **隐私与肖像**：用户上传的人物照片仅用于本次绘本创作，严禁擅自外传或挪作他用。
- **规则与故事分离**：文档与脚本保持普适，不写入特定故事死规则；具体故事状态一律通过 `story_plan.json` 表达。

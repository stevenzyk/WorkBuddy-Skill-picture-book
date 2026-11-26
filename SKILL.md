---
name: fairy-tale-picture-book
display_name: 童话故事绘本（照片定制）
display_name_en: Fairy Tale Picture Book
description: 将用户上传的人物照片变成童话故事绘本主角，创作完整童话故事并生成可翻页 HTML 电子绘本与可打印装订的 PDF 绘本。支持单人主角与多人物同框（全家福、亲子、兄弟、朋友），内置人物档案与造型确认、Prompt 零丢失编译器、样张先验与全流程防漂移机制。
description_zh: 把人物照片变成童话绘本主角，创作完整故事并生成可翻页 HTML 电子绘本与可打印 PDF。支持单人或多人同框，内置造型切换、Prompt 自动编译校验与防漂移闭环。
description_en: Turn personal photos into fairy tale picture book protagonists, write a complete story, and deliver both an interactive HTML e-book and a print-ready PDF with deterministic prompt compilation and cross-page consistency.
examples_zh:
  - "把这张宝宝照片做成一本方款 8 寸、12 面的森林冒险童话绘本，温馨水彩风"
  - "用这张全家福定制一本横款 12 寸、16 面的海边野餐亲子绘本，唯美绘本风"
  - "我有一个故事大纲，帮我结合家人照片扩写成四季旅行绘本并导出可打印 PDF"
examples_en:
  - "Turn this child photo into an 8-inch square, 12-page forest adventure picture book in soft watercolor style"
  - "Create a printable 16-page landscape 12-inch family beach picnic book from this family photo"
  - "Expand my story outline with this family photo into a printable four-seasons storybook PDF"
version: 2.3.0
author: Steven的能量场
agent_created: true
---

# 童话故事绘本（人物照片定制）

将用户上传的人物照片融入原创童话故事，通过**「照片体检与规格确认 → 人物造型方案与脚本合并确认（`compile_prompts.py` 编译锁死）→ 站姿基准图与样张确认 → 分批生图与 `build_book.py` 一键交付」**四步闭环，输出**可翻页 HTML 电子绘本**与**含完整图文排版的可打印 PDF**。

## 何时使用本技能

- 用户上传人物照片（单人或全家福/多人合照），希望定制个性化童话绘本或可打印实体书素材。
- 若用户尚未上传照片，先礼貌请用户提供一张正面、清晰、光线良好的人像照片再继续。
- 先定位本技能根目录 `<SKILL_DIR>`（即当前 `SKILL.md` 所在目录），后续必须直接调用 `<SKILL_DIR>/scripts/` 下的内置 Python 脚本。

---

## 核心工作流（两次用户确认 + 两个确定性脚本收口）

### 第一步：照片体检与创作规格确认

1. **照片体检（用 `ViewImage` 观察上传照片）**：
   - 若照片模糊、严重逆光、遮挡五官或大角度侧脸，提醒用户换清晰正面照效果更好。
   - **人数边界**：稳定同框上限为 **1–4 人**；超过 4 人时建议选 1–4 位核心主角，其余家人仅在关键页客串。
   - 初步识别照片中每人的**称呼、大致年龄（数字）、性别、相对身高关系**，供下一步核对。
2. **确认 4 项规格（尺寸与页数不可擅自拍板；若用默认值须在交付时注明）**：
   - **插画风格**：温馨水彩风 `watercolor`（默认，容错最高） / 唯美绘本风 `storybook` / 明亮卡通风 `cartoon` / 写实插画风 `realistic`（多人合照优先推荐水彩或唯美绘本风）。
   - **绘本尺寸**：方款 8 寸 `square8`（203×203mm，画幅 `1:1`，默认） / 方款 10 寸 `square10`（254×254mm，`1:1`） / 横款 12 寸 `landscape12`（305×229mm，`3:2` 或 `4:3`） / 竖款 12 寸 `portrait12`（229×305mm，`2:3` 或 `3:4`）。
   - **页数（面数）**：可选 **8 / 10 / 12 / 14 / 16 / 18 / 20 / 22 / 24 / 28 / 32 / 36 / 40 / 44 / 48 / 52 / 56 / 60 / 64 / 68 / 72 面**（默认 **12 面**；含封面 1 + 封底 1，正文面数 = `总面数 - 2`；首次推荐 12–16 面）。
   - **故事主题**：默认推荐高胜率骨架（单日冒险/救助伙伴/勇气成长/家庭出游）；也支持跨季节或用户大纲扩写。

---

### 第二步：【检查点 1】合并确认档案、造型与脚本 → 运行 `compile_prompts.py`

> **执行本步前，先读取本技能目录下的两份参考文件**：
> - `@references/story_prompts.md`（4 套高胜率故事骨架、极简剧场预算与 `story_plan.json` 完整模板）
> - `@references/consistency_rules.md`（角色本体与 `Look` 造型解耦、防摆拍、四类元素与动作规范）

1. **一次性向用户展示以下 3 项内容并请用户确认（合并提问，避免反复打扰）**：
   - **① 人物客观档案卡**：每人称呼、**具体数字年龄**、性别、相对身高关系（如「儿子 24 岁男性，与 55 岁爸爸同高」）。
   - **② 全书造型服装方案（`Looks`，建议 1–3 套）**：AI 先拟好合理默认方案请用户确认——单日故事 1 套；跨季节、入水赤脚、变身等场景拆为独立造型（如 `look_summer` 夏装、`look_beach_barefoot` 挽裤脚赤脚无鞋、`look_winter` 羽绒服雪地靴）。
   - **③ 完整分页故事文案与画面梗概**（控制视觉复杂度预算：核心场景 ≤ 4 个、核心道具/配角 ≤ 2–3 个、每页仅 1 个瞬时动作）。
2. **用户确认后，编写 `story_plan.json` 并运行编译器（严禁手写散装长 Prompt）**：
   ```bash
   python <SKILL_DIR>/scripts/compile_prompts.py --plan ./book/story_plan.json
   ```
   - 编译器会根据 `(age, gender)` 自动生成客观视觉主语（如 `the 24-year-old adult man`）并展开 `{c1}` 占位符，**自动拦截 `son/daughter` 等诱发成人身高缩水的辈分词**，核验每页在场角色均写了动作且 `caption_nouns_en`（文案核心物体词）100% 进图。
   - 若编译报错，按终端提示修正 `story_plan.json` 直至输出 `✅ 编译通过`，自动产出 **`prompts_manifest.md`** 与 **`book.json`**。

---

### 第三步：【检查点 2】先验基准图 + 样张 → 按清单小批生图

> **执行本步前，先读取 `@references/qa_checklist.md`。全程必须原样复制 `prompts_manifest.md` 中的 Prompt 与必传参考图调用 `ImageGen`，严禁手改、简化或缩写！**

1. **阶段 3A：生成全套基准图 + 2 页样张，交给用户做第 2 次确认**：
   - 按 `prompts_manifest.md` 第一部分依次生成：**全部 `Look` 平地自然站姿全身基准图**（第 1 套传用户原照；第 2 套起传第 1 套站姿基准图作 `image1`，锁死同一张脸与身高差并完成换装）+ 道具/配角基准图（`ref_*.png`）。
   - 再按清单生成 **封面 `page_01_cover.png` + 正文第 1 页 `page_02.png`**。
   - 用 `present_files` 将**所有造型站姿基准图 + 封面与第 1 页样张**展示给用户确认（脸像不像、身高比例对不对、各套换装是否满意、画面是否自然不僵硬）。用户点头后再批量画剩余正页。
2. **阶段 3B：小批生成剩余页面（每次 2–3 页）+ 5 题事实反问审图**：
   - 每次仅连续生成 2–3 页，立即用 `ViewImage` 逐页回答 `@references/qa_checklist.md` 关口 3 的 **5 个事实问题**（人数与身高、视线非摆拍、文案核心名词可见、衣鞋与当前 `look_id` 一致、道具比例与肢体正常）。发现任一异常**当场重生成该页**，再继续下一批。

---

### 第四步：一键硬校验、双格式交付与单页精修（严禁自写构建脚本）

> **强制约束**：`book.json` 已由 `compile_prompts.py` 自动生成。**严禁自行编写 `make_print_pages.py`、`verify.py` 或手拼 HTML/PDF**，直接调用内置 `build_book.py`。

1. **排版前硬校验**：
   ```bash
   python <SKILL_DIR>/scripts/build_book.py --book ./book/book.json --check-only
   ```
2. **一键生成可翻页 HTML 电子绘本 + 完整图文打印级 PDF**：
   ```bash
   python <SKILL_DIR>/scripts/build_book.py --book ./book/book.json --out-dir ./book --dpi 150 --crop-watermark
   ```
   - `--crop-watermark`：自动等比裁去图片右下角 6.5% 平台水印，HTML 与 PDF 同步干净且不裁人物头部；如需实体印刷出血位可加 `--bleed 3`。依赖：`pip install Pillow`。
3. **交付与单页精修**：
   - 用 `present_files` 交付 HTML 与 PDF，注明尺寸、总面数与插画风格。
   - 告知用户：若某页需微调，直接回复「第 X 页 + 修改意见」，修改 `story_plan.json` 重跑该页与 `build_book.py` 即可一键更新。

---

## 参考资料与工具文件

- `@references/story_prompts.md`：4 套高胜率故事骨架、极简剧场预算、`story_plan.json` 完整模板与规格表。
- `@references/consistency_rules.md`：角色本体与 `Look` 造型解耦、防辈分词缩水、防棚拍贴图感与四类元素规范。
- `@references/qa_checklist.md`：四道质量关口与 5 题事实反问审图清单。
- `assets/picture_book_template.html`：支持单页翻页/双页对开/滚动阅读与 `<img>` 打印样式的 HTML 模板。
- `scripts/compile_prompts.py`：`story_plan.json` 校验器 + 零丢失 Prompt 编译器 + `book.json` 生成器。
- `scripts/build_book.py` & `scripts/build_pdf.py`：硬校验、去水印、HTML 与 Pillow 完整图文 PDF 构建器。

---

## 隐私与维护规范

- **隐私与肖像**：用户上传的人物照片仅用于本次绘本创作，严禁擅自外传或挪作他用。
- **规则与故事分离**：本技能所有文档与脚本保持普适，不写入特定故事死规则；具体故事状态一律通过 `story_plan.json` 的 `characters / looks / scenes / props` 表达。

# workbuddy-skill-picture-book

中文 | [English](README.en.md)

**童话故事绘本（照片定制） / Fairy Tale Picture Book** —— 一个面向 WorkBuddy（兼容 Agent Skill 规范）的定制绘本创作技能包。

将用户上传的一张人物照片转化为童话绘本主角，创作完整故事脚本与分镜，生成风格统一、跨页高度一致的绘本插画，并最终输出**可在线翻页浏览的 HTML 电子绘本**与**可直接打印装订的 PDF 绘本文件**。

---

## 核心特性

- **照片定制主角（单人 & 多人同框）**
  - 支持单人主角，也支持全家福、亲子、兄弟姐妹、朋友等 **2 人及以上多角色同框**故事。
  - 将人物照片卡通化为与整本书画风统一的角色形象，同时保留可辨识的面部、发型与标志性特征。
- **全流程防漂移一致性体系**
  - **故事圣经（Story Bible）前置驱动**：先固定人物设定、视觉锚点、场景清单（含昼夜光线）、道具持有时间线与状态连续性，再编写分页脚本。
  - **多级基准图逐页复用**：支持单人基准图、多角色「全员基准图（全家福）」以及四类高漂移元素（核心道具/载体、动物/幻想生物配角、核心固定物体、贯穿性剧情道具）的独立基准图参考（`image-to-image`）。
  - **「正面写全」白名单提示词原则**：多人同框逐个点名位置与动作、恒穿装备显式声明、阶段状态跨角色隔离，减少模型自由发挥导致的漏人、撞脸、穿帮或道具变形。
  - **边生成边核验闭环**：每生成一批插画即核对人物/道具/动作/光照，排版前强校验图片数量、文件名映射与图文一一对应。
- **多种规格与画风可选**
  - **4 种插画风格**：温馨水彩风（默认）、明亮卡通风、写实插画风、唯美绘本风。
  - **4 种印刷尺寸**：方款 8 寸（默认）、方款 10 寸、横款 12 寸、竖款 12 寸。
  - **丰富页数档位**：支持 8–72 面共 21 种标准印刷面数（默认 12 面）。
- **双格式成品交付**
  - **HTML 电子绘本**：基于响应式网页模板，支持屏幕阅读与浏览器打印导出。
  - **打印级 PDF**：通过纯 Python + Pillow 的 `scripts/build_pdf.py` 直接拼合页面图片，不依赖 headless 浏览器，输出稳定、体积轻巧。

---

## 效果展示

以下示例均来自真实生成案例《星光救援队》（横款 12 寸 · 20 面 · 一家四口多人同框），均为 AI 绘制插画效果：

### HTML 电子绘本排版效果

![HTML 电子绘本排版效果](docs/images/demo_html_preview.jpg)

### 多级基准图复用与跨页一致性

![多级基准图与跨页一致性效果](docs/images/demo_consistency.jpg)

---

## 目录结构

```text
workbuddy-skill-picture-book/
├── SKILL.md                           # 技能核心入口（WorkBuddy 规范，v2.5.0）：四步工作流与脚本调用
├── assets/
│   └── picture_book_template.html     # 可单页翻页 / 双页对开 / 滚动阅读与打印的 HTML 电子绘本模板
├── docs/
│   └── images/                        # README 效果展示图片
│       ├── demo_html_preview.jpg
│       └── demo_consistency.jpg
├── references/
│   ├── story_prompts.md               # 绘本文学创作金标准、3 种可选文风、4 套故事骨架与 story_plan.json 规范
│   ├── consistency_rules.md           # 角色与 Look 解耦、空间装修锚定、室内外物理常识、防排排站与时间线细则
│   └── qa_checklist.md                # 文学去说明书化自检与 6 题事实反问审图清单
├── scripts/
│   ├── compile_prompts.py             # story_plan.json 校验器 + 零丢失 Prompt 编译器 + book.json 生成器
│   ├── build_book.py                  # 一键校验 book.json 并生成可翻页 HTML + 图文 PDF
│   └── build_pdf.py                   # 基于 Pillow 的打印级图文 PDF 合成脚本（内置中文避头点与防孤字排版）
├── LICENSE                            # Apache License 2.0 开源协议
├── README.md                          # 中文说明文档
└── README.en.md                       # 英文说明文档
```

---

## 绘本规格对照

### 1. 插画风格

| 风格名称 | 适用场景与特点 |
|---------|----------------|
| **温馨水彩风**（默认） | 柔和粉彩色调、手绘质感、梦幻温暖的经典童话氛围 |
| **明亮卡通风** | 线条干净利落、色彩饱满明快、圆润可爱，适合低龄儿童 |
| **写实插画风** | 自然柔和光影、丰富纹理细节、人物外貌还原度更高 |
| **唯美绘本风** | 柔美光影与细腻笔触、情感氛围柔和治愈 |

### 2. 绘本尺寸与生图画幅（封面全出血 vs 正文 78% 插画框精准匹配）

| 尺寸名称 | `size` 参数 | 实际印刷尺寸 | 封面/封底生图画幅 | 正文插画生图画幅 |
|---------|-------------|-------------|-------------------|-----------------|
| **方款 8 寸**（默认） | `square8` | 约 203mm × 203mm | `1:1` | `4:3`（防切脚尖） |
| **方款 10 寸** | `square10` | 约 254mm × 254mm | `1:1` | `4:3`（防切脚尖） |
| **横款 12 寸** | `landscape12` | 约 305mm × 229mm | `4:3` 或 `3:2` | `16:9` 或 `3:2` |
| **竖款 12 寸** | `portrait12` | 约 229mm × 305mm | `3:4` 或 `2:3` | `1:1` 或 `4:3` |

### 3. 页数（面数）

- **可选值**：`8 / 10 / 12 / 14 / 16 / 18 / 20 / 22 / 24 / 28 / 32 / 36 / 40 / 44 / 48 / 52 / 56 / 60 / 64 / 68 / 72` 面（默认 **12 面**）。
- **页数计算**：总面数 = 封面（1 面）+ 正文（`总面数 - 2` 面）+ 封底（1 面）。
- **文件命名**：封面为 `page_01_cover.png`，正文依次为 `page_02.png`、`page_03.png` ……（封底可使用纯色渐变模板或独立插画）。

---

## 工作流程

本技能严格按照以下四步闭环执行（兼顾绘本文学灵气与跨模型确定性）：

1. **照片体检与确认创作规格（含 3 种带适用年龄段的绘本文风推荐）**
   - 评估照片清晰度、角度与人数（1–4 人同框最稳），确认 **插画风格、绘本尺寸、页数（面数）** 以及 **绘本文风**（童趣韵律风 2–5 岁 / 好奇寻宝风 5–10 岁 / 温暖收集风全年龄亲子与成年家庭）。
2. **【检查点 1】合并确认档案、造型与文学脚本 → `compile_prompts.py` 确定性编译**
   - 采用**「事件同源、繁简分流 + 严守室内外物理常识」**法则编写全书串珠线 `story_thread` 与去说明书化的绘本文案 `text_zh`，一次性请用户确认 **人物客观档案卡 + 造型服装方案（`Looks` + 页级 `outfit_overrides_en` 微调）+ 逐页文案**。
   - 写入 `story_plan.json` 并运行 `scripts/compile_prompts.py`：自动合成客观年龄主语、校验同一 `location_group` 空间装修一致、拦截室内户外道具升空违和词、注入多人防排排站错落构图、强制校验道具位置与单向时间线 `(day, time_of_day)`、按封面/正文画框匹配画幅与底部 15% 地面留白，输出 `prompts_manifest.md` 与 `book.json`。
3. **【检查点 2】先验站姿基准图 + 样张 → 小批生图与 6 题事实审图**
   - 按清单生成各套 `Look` 平地站姿全身基准图 + 要素基准图 + **封面与首张样张**请用户确认，随后每次 2–3 页小批生成并逐页执行 6 题事实审图。
4. **自动化校验、双格式交付与单页精修**
   - 运行 `scripts/build_book.py` 硬校验并一键输出可翻页 HTML 电子绘本与含中文避头点防孤字排版的打印级 PDF（支持 `--crop-watermark` 与 `--bleed`）；支持按页码单页重画并一键重打包。

---

## 安装与使用

### 作为 WorkBuddy Skill 使用

1. **克隆或下载本仓库到 WorkBuddy 技能目录**：
   ```bash
   git clone https://github.com/stevenzyk/workbuddy-skill-picture-book.git ~/.workbuddy/skills/fairy-tale-picture-book
   ```
   > 也可以将技能文件打包为 `.zip`（顶层目录为 `fairy-tale-picture-book/`），在 WorkBuddy 客户端或开放平台直接上传导入。

2. **在对话中触发**：
   上传一张清晰正面的人物照片，并说明需求，例如：
   - 「把这张宝宝照片做成一本方款 8 寸、12 面的森林冒险童话绘本，温馨水彩风。」
   - 「用这张全家福定制一本横款 12 寸、16 面的海边野餐绘本，温暖收集文风。」

### 单独运行编译、构建与 PDF 脚本

**前置依赖**：
```bash
pip install Pillow
```

**完整确定性流水线（`story_plan.json` → `prompts_manifest.md` + `book.json` → HTML + PDF）**：
```bash
# 1. 校验结构化剧本，零丢失编译全套生图 Prompt 清单并自动生成 book.json
python scripts/compile_prompts.py --plan ./book/story_plan.json

# 2. 生图完成后，仅校验面数与磁盘图片完整性
python scripts/build_book.py --book ./book/book.json --check-only

# 3. 一键生成可翻页 HTML 与打印级完整图文 PDF（可选 --crop-watermark 同步去右下角水印、--bleed 3 添加 3mm 印刷出血位）
python scripts/build_book.py --book ./book/book.json --out-dir ./book --dpi 150 --crop-watermark --bleed 3
```

**兼容模式：直接把纯插画目录合成为 PDF（自动排除 `ref_*` 参考图）**：
```bash
# 方款 8 寸 (203mm × 203mm, 150dpi)
python scripts/build_pdf.py ./book ./book_8inch.pdf --size square8

# 横款 12 寸 (305mm × 229mm, 150dpi) 并自动去水印 + 追加渐变封底
python scripts/build_pdf.py ./book ./book_12inch.pdf 305 229 150 --crop-watermark --blank-back
```

---

## 维护与二次开发规范

若需对本技能规则进行迭代优化，请遵循 `SKILL.md` 中规定的**「规则与故事分离」**与**「代码确定性兜底」**原则：

- **`SKILL.md`**：只保留精炼的四步工作流、两次用户确认关口与脚本调用入口。
- **`scripts/compile_prompts.py` & `scripts/build_book.py`**：将字符串拼装、赤脚去鞋、时间线检查、画幅匹配与排版校验收归 Python 脚本确定性执行。
- **`references/`**：维护绘本文学金标准、高胜率故事骨架、角色与 `Look` 解耦规则及事实反问核验清单。

---

## 隐私与协议

- **肖像与隐私**：用户上传的人物照片仅用于当前绘本创作流程，严禁擅自外传或挪作他用。
- **作者**：Steven的能量场（Skill 版本 `v2.4.0`）
- **开源协议**：本项目基于 [Apache License 2.0](LICENSE) 开源。

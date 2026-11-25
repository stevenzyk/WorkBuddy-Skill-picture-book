# 童话故事绘本创作参考与提示词模板

本文件提供创作「故事圣经」、分页脚本、`book.json` 数据结构、插画风格前缀与规格对照表。
一致性防漂移细则见 `@references/consistency_rules.md`，核验清单见 `@references/qa_checklist.md`。

---

## 一、故事圣经模板（Story Bible）

编写分页脚本与生成任何插画之前，先填写这份故事圣经。以下示例中的具体角色/道具仅为格式示范，实际按当前故事内容填写。

```markdown
【人物设定清单】
- 主角外貌（从照片提取，全书逐页一字不改）：<发型、发色、脸型、五官、标志性特征>
- 主角固定服装与随身道具：<如：浅绿色短袖 T 恤 + 白色长裤 + 黄色小背包>
- 恒穿装备（如有，全书任何页面均穿着，含休息/睡觉/上岸场景）：<如：橙色救生衣 — wearing an orange life vest>
- 配角设定：<每个配角的固定外貌、体型与标志性特征>
- 多角色区分锚点（≥2 个人类角色时必填）：<对比年龄、身高、体型、脸型与发型差异，防撞脸>

【基准图规划（image-to-image 参考图）】
- 人物基准图：单人主角生成 `ref_main.png`；多人同框先合成 `ref_family.png`（全员同框校准比例）
- 要素基准图（按需）：核心载体 `ref_vehicle.png`、动物配角 `ref_sidekick.png`、固定核心物 `ref_centerpiece.png`、贯穿道具 `ref_prop.png`
  （注意：有分阶段状态的角色/道具，基准图采用初始/无状态形态）

【视觉锚点清单（固定英文描述，逐页原样复用）】
- 主角锚点：<英文，外貌 + 固定服装 + 随身道具>
- 多角色区分句（如有）：<如：an older chubby boy with bangs..., clearly taller and bigger ↔ a younger small boy with a buzz cut..., clearly shorter and smaller>
- 载体 / 道具锚点：<颜色 + 形状 + 结构部件数 + 细节 + 尺寸 + 数量(one single / exactly N)>
- 动物 / 幻想配角锚点：<造型风格类型 + 绝对/相对体型 + 标志性部位 + 特效状态>
- 核心固定物体锚点：<one single + 颜色(含暗光保色) + 位置 + 相对大小；不在场页写 not visible>

【场景清单（每个场景锚点内嵌时间与光线词，逐字复用）】
- 场景 A（第 X–Y 页，白天）：<英文地形 + 固定细节物件 + bright warm daylight>
- 场景 B（第 X–Y 页，黄昏）：<英文地形 + 固定细节物件 + golden sunset sky at dusk>
- 场景 C（第 X–Y 页，夜晚）：<英文地形 + 固定细节物件 + deep dark night sky filled with many twinkling stars>

【道具持有与状态连续性时间线】
- 道具 1：<来源> → 第 X 页在谁手里 → 第 Y 页放下/传递 → <去向>
- 状态链：<如：第 1–4 页正常 → 第 5 页受伤(裸伤) → 第 8 页包扎(缠白纱布) → 第 12 页愈合>
- 标志性动作归属页：<如：「许愿」仅第 9 页；「挥手告别」仅第 16 页>
```

---

## 二、分页脚本模板

基于故事圣经输出分页脚本，展示给用户确认后再开始生图。画面描述与中文文案必须严格指向同一核心动作。

```markdown
【封面】
- 标题：<故事标题>
- 副标题：<可选，如：献给最勇敢的你>
- 画面描述（英文）：<含 leave clear empty space at the top of the image for the title text>

【第 1 页】
- 所属场景：<场景 A>
- 画面描述（英文）：<风格前缀 + 人物锚点 + 道具/配角锚点 + 场景锚点 + 本页动作与空间关系>
- 道具持有状态：<本页每件关键道具在谁手里 / 已放下 / 不可见>
- 文案（中文）：<1–3 句，30–60 字，与画面严格对应>
- 状态变化：<本页新增或变化的状态>

【封底】
- 文案：<一句温暖寄语 / 故事寓意>
```

**图文对应示范**：
- ✅ 画面：`the child carrying the injured little animal into a cave` ↔ 文案：「小朋友把小动物背进山洞」
- ❌ 画面：`the child warming himself by a campfire` ↔ 文案：「小朋友把小动物背进山洞」（图文错位）

---

## 三、`book.json` 数据模板（供 `scripts/build_book.py` 使用）

生成完插画并完成核验后，在绘本图片目录下写入 `book.json`，即可一键校验并同时生成可翻页 HTML 与带完整文字的打印级 PDF：

```json
{
  "title": "我的童话故事",
  "subtitle": "献给最勇敢的你",
  "size": "square8",
  "total_pages": 12,
  "cover": {
    "image": "page_01_cover.png"
  },
  "pages": [
    {
      "image": "page_02.png",
      "text": "从前有一个小朋友，她有一双明亮的大眼睛。"
    },
    {
      "image": "page_03.png",
      "text": "这一天，她背上小背包，走进了会发光的魔法森林。"
    }
  ],
  "back": {
    "image": "",
    "ending": "善良的心，\n是世界上最亮的灯。"
  }
}
```

> 说明：`size` 可选 `square8` / `square10` / `landscape12` / `portrait12`；`back.image` 留空字符串时，HTML 与 PDF 会自动使用温暖渐变纯色封底呈现寄语；`pages` 长度必须等于 `total_pages - 2`。

---

## 四、童话故事结构与语言技巧

经典四段式结构（适合 3–8 岁读者）：
1. **开头（1–2 页）**：介绍主角与日常生活，建立亲切感。
2. **冲突（2–4 页）**：主角遇到困难或奇遇（迷路、帮助小动物、魔法冒险等）。
3. **高潮（2–3 页）**：主角凭借勇气、智慧或善良解决问题。
4. **结尾（1–2 页）**：温暖收束，获得成长或友谊，点出寓意。

**年龄适配**：
- **低龄（3–5 岁）**：短句、重复句式（「走啊走……走啊走……」）、拟声词（「哗啦」「咕噜咕噜」）。
- **儿童（5–8 岁）**：可加入简短对话与画面感形容词，但每页仍控制在 30–60 字以内。

**常见主题方向**：冒险（森林/深海/天空）、勇气（克服胆小/独立完成挑战）、友谊（结识新伙伴）、善良（帮助迷路或受伤的小动物/分享）、成长（学会新本领/承担责任）、魔法（奇幻世界奇遇）。

---

## 五、插画风格前缀与人物卡通化模板

### 1. 四种插画风格前缀（拼接在每页 Prompt 最前）

- **温馨水彩风（默认）**：
  ```text
  soft watercolor children's book illustration, gentle pastel colors, dreamy and warm atmosphere, soft edges, hand-painted texture, whimsical storybook style, high quality picture book art
  ```
- **明亮卡通风**：
  ```text
  bright cheerful cartoon children's book illustration, bold clean outlines, vibrant saturated colors, cute rounded character design, playful and lively, flat color storybook style
  ```
- **写实插画风**：
  ```text
  realistic detailed children's book illustration, soft natural lighting, rich textures, expressive realistic characters, warm cinematic atmosphere, high-detail storybook art
  ```
- **唯美绘本风**：
  ```text
  beautiful storybook illustration, soft dreamy lighting, pastel and warm color palette, delicate painterly style, gentle emotional mood, high quality picture book art
  ```

### 2. 人物照片卡通化基准图模板（`image-to-image`，`input_fidelity: low`）

```text
<style_prefix>, <character appearance & fixed outfit description>,
portrait of a <age/gender> as the main character in a fairy tale picture book,
keep the recognizable facial features from the reference photo (hairstyle, hair color, face shape, eyes),
full body standing pose, clean plain warm cream background, no real photo background, suitable as a character reference sheet
```

### 3. 分页画面 Prompt 示范（温馨水彩风）

- **封面**：`soft watercolor children's book illustration, a cute little girl with shoulder-length black hair, round face, big bright eyes, wearing a yellow dress with a small red bow, standing in the lower center of a magical glowing forest, leave clear empty space at the top of the image for the title text, dreamy warm atmosphere`
- **正文页**：`soft watercolor children's book illustration, a cute little girl with shoulder-length black hair, round face, big bright eyes, wearing a yellow dress with a small red bow, walking along a winding sunlit forest path, waving her right hand toward a small friendly fox beside the path, bright warm daylight`

---

## 六、绘本规格、生图画幅与页数对照表

### 1. 尺寸与生图画幅映射

| 尺寸名称 | `size` 参数值 | 实际印刷尺寸 | HTML `@page` / PDF 参数 | 推荐生图画幅 |
|---|---|---|---|---|
| **方款 8 寸**（默认） | `square8` | 约 203mm × 203mm | `203mm 203mm` | `1:1` |
| **方款 10 寸** | `square10` | 约 254mm × 254mm | `254mm 254mm` | `1:1` |
| **横款 12 寸** | `landscape12` | 约 305mm × 229mm | `305mm 229mm` | `4:3` 或 `3:2` |
| **竖款 12 寸** | `portrait12` | 约 229mm × 305mm | `229mm 305mm` | `3:4` 或 `2:3` |

### 2. 页数（面数）可选值

**8 / 10 / 12 / 14 / 16 / 18 / 20 / 22 / 24 / 28 / 32 / 36 / 40 / 44 / 48 / 52 / 56 / 60 / 64 / 68 / 72 面**（默认 **12 面**）

- 「面」= 印刷的每一页（含封面 1 面 + 封底 1 面）；正文面数 = `总面数 - 2`。
- 图片命名约定：封面 `page_01_cover.png`，正文 `page_02.png` ～ `page_{N+1}.png`，可选封底 `page_{N+2}_back.png`。

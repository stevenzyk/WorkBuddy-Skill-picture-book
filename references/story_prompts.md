# 童话故事绘本创作参考与提示词模板

本文件提供创作「故事圣经」、分页脚本、`book.json` 数据结构、插画风格前缀与规格对照表。
一致性防漂移细则见 `references/consistency_rules.md`，核验清单见 `references/qa_checklist.md`。

---

## 一、故事圣经模板（Story Bible）

编写分页脚本与生成任何插画之前，先填写这份故事圣经。以下示例中的具体角色/道具仅为格式示范，实际按当前故事内容填写。

```markdown
【人物设定清单】
- 主角外貌（从照片提取，全书逐页一字不改）：<发型、发色、脸型、五官、年龄感>
- 相对身高锁定（≥2 人必填）：<如：爸爸最高，成年儿子与爸爸几乎同高，成年女儿略高于妈妈，四人均为成年人、非儿童；或：哥哥比弟弟高一头>
- 服装方案（二选一）：
  - 单日故事固定服装：<全书固定同款服装>
  - 跨季节故事分季服装：<春装 / 夏装 / 秋装 / 冬装羽绒服与冬靴，严禁雪地穿短袖>
- 恒穿装备（如有，全书任何页面均穿着）：<如：橙色救生衣 — wearing an orange life vest>
- 配角设定：<每个配角的固定外貌、体型与标志性特征>

【基准图规划（image-to-image 参考图）】
- 人物基准图：单人生成站姿 `ref_main.png`；多人同框优先合成**自然站姿全身**的 `ref_family.png`（校准相对身高，避免坐姿棚拍导致站立页缩水或全书复制坐姿）
- 要素基准图（按需）：核心载体 `ref_vehicle.png`、动物配角 `ref_sidekick.png`、固定核心物 `ref_centerpiece.png`、贯穿道具 `ref_prop.png`
  （注意：有分阶段状态的角色/道具，基准图采用初始/无状态形态）

【视觉锚点清单（固定英文描述，逐页原样复用）】
- 主角锚点：<英文，外貌 + 年龄身份(如 full-grown adult, NOT a child) + 相对身高 + 对应服装>
- 多角色区分句（如有）：<对比年龄、身高、脸型与发型差异，防撞脸>
- 载体 / 道具锚点：<颜色 + 形状 + 结构部件数 + 相对人体尺寸(如 palm-sized) + 数量(one single / exactly N)>
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

## 二、分页脚本模板（强制填空防漏项）

基于故事圣经输出分页脚本，展示给用户确认后再开始生图。**强制填写「文案核心名词清单」与「视线与互动方向」**，防止漏画物体或全员直视镜头摆拍。

```markdown
【封面】
- 标题：<故事标题>
- 副标题：<可选，如：献给最勇敢的你>
- 画面描述（英文）：<含 leave clear empty space at the top of the image for the title text>

【第 1 页】
- 所属场景：<场景 A>
- 文案（中文）：<1–3 句，30–60 字，与画面严格对应>
- 文案核心名词清单（必须 100% 写入下方英文 Prompt）：<如：格子野餐布、野餐篮、三明治、水果、饮品>
- 视线与互动方向：<如：妈妈低头摆食物，爸爸递水果给女儿，四人自然互动，NOT looking at the camera>
- 画面描述（英文）：<风格前缀 + 人物锚点(含相对身高与当季衣鞋) + 道具/配角锚点 + 场景锚点 + 本页动作与互动视线>
- 道具持有状态：<本页每件关键道具在谁手里 / 已放下 / 不可见>
- 状态变化：<本页新增或变化的状态>

【封底】
- 文案：<一句温暖寄语 / 故事寓意>
```

**图文对应示范**：
- ✅ 文案：「妈妈铺开餐布，风把花香吹过来，连午饭都变甜了。」→ 核心名词：`野餐布、野餐篮、三明治与水果午饭` → 英文 Prompt 完整写出食物与用餐互动。
- ❌ 文案写「午饭」但英文 Prompt 只写了空野餐布；或文案写「树荫下」但英文 Prompt 写成「遮阳伞下」。

---

## 三、`book.json` 数据模板（供 `scripts/build_book.py` 使用）

生成完插画并完成核验后，在绘本目录下写入 `book.json`，**直接调用技能内置脚本**一键校验并生成可翻页 HTML 与带完整文字的打印级 PDF：

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

经典四段式结构：
1. **开头（1–2 页）**：介绍主角与日常生活，建立亲切感。
2. **冲突（2–4 页）**：主角遇到困难、奇遇或开启一段旅程。
3. **高潮（2–3 页）**：主角凭借勇气、智慧、善良或家人协作完成挑战。
4. **结尾（1–2 页）**：温暖收束，获得成长或珍贵回忆，点出寓意。

**读者年龄适配**：
- **低龄（3–5 岁）**：短句、重复句式（「走啊走……走啊走……」）、拟声词（「哗啦」「咕噜咕噜」）。
- **儿童/亲子（5–8 岁及全家福纪念书）**：可加入简短对话与画面感形容词，每页仍控制在 30–60 字以内。

**常见主题方向**：冒险（森林/深海/天空）、勇气、友谊、善良（帮助小动物/分享）、成长、魔法、四季家庭旅行。

---

## 五、插画风格前缀与人物卡通化模板

### 1. 四种插画风格前缀（中性措辞，兼容儿童主角与成人全家福）

> **注意**：故意避免在通用前缀中写死 `children's book`，防止成人主角/成年子女被模型偏置画成小学生。仅当主角确为幼儿时，可在人物锚点中写明年龄。

- **温馨水彩风（默认）**：
  ```text
  soft watercolor storybook illustration, gentle pastel colors, dreamy and warm atmosphere, soft edges, hand-painted texture, whimsical picture book art, high quality illustration
  ```
- **明亮卡通风**：
  ```text
  bright cheerful cartoon storybook illustration, bold clean outlines, vibrant saturated colors, cute rounded character design, playful and lively, flat color picture book style
  ```
- **写实插画风**：
  ```text
  realistic detailed storybook illustration, soft natural lighting, rich textures, expressive realistic characters, warm cinematic atmosphere, hand-painted picture book art, no photorealistic photo background
  ```
- **唯美绘本风**：
  ```text
  beautiful painterly storybook illustration, soft dreamy lighting, pastel and warm color palette, delicate hand-painted brushstrokes, gentle emotional mood, high quality picture book art
  ```

### 2. 人物照片卡通化基准图模板（`image-to-image`，推荐低保真 `low`）

```text
<style_prefix>, <character appearance, age/adult stature, relative heights, and outfit description>,
full-body natural standing pose (not sitting), keep the recognizable facial features from the reference photo (hairstyle, hair color, face shape, eyes),
clean plain warm cream background, no real photo background, suitable as a character reference sheet
```

### 3. 分页画面 Prompt 示范（温馨水彩风）

- **封面**：`soft watercolor storybook illustration, a cute little girl around 5 years old with shoulder-length black hair, round face, big bright eyes, wearing a yellow dress with a small red bow, standing in the lower center of a magical glowing forest looking up with wonder, leave clear empty space at the top of the image for the title text, dreamy warm atmosphere`
- **正文页**：`soft watercolor storybook illustration, a cute little girl around 5 years old with shoulder-length black hair, round face, big bright eyes, wearing a yellow dress with a small red bow, walking along a winding sunlit forest path, waving her right hand toward a small friendly fox beside the path, candid natural moment looking at the fox, NOT looking at the camera, bright warm daylight`

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

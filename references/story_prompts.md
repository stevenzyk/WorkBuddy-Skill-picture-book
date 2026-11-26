# 童话故事绘本创作参考、故事骨架与 `story_plan.json` 模板

本文件提供高胜率故事骨架（Blueprints）、`story_plan.json` 完整模板、插画风格与规格对照表。
一致性细则见 `references/consistency_rules.md`，核验清单见 `references/qa_checklist.md`。

---

## 一、极简剧场预算与 4 套高胜率故事骨架（Story Blueprints）

除非用户明确要求复杂长篇，编剧时优先遵守**「极简剧场预算」**，确保任何模型下都能稳定产出：
- **造型（`looks`）套数**：默认 **1 套**（单日故事），跨季节/入水/变装故事 **≤ 3 套**。
- **核心场景（`scenes`）数量**：**≤ 4 个**。
- **跨页核心道具 + 动物配角（`props` + `sidekicks`）**：**≤ 2–3 个**。
- **单页动作唯一**：每页只画 **1 个瞬时可定格动作**（禁止写「先走过去、再抱起来、最后包扎」的跨时间连续动作）。

### 4 套经典高胜率骨架（可直接套用并替换为用户的照片角色）

1. **奇遇寻物归还型（适合 1–2 名主角 + 1 只动物配角，12–16 面）**
   - 场景：森林小径 → 发光大树下 → 溪边草地。
   - 脉络：出发散步 → 捡到一件特别的小信物（如发光松果/小铃铛）→ 沿路遇到寻找信物的小动物 → 归还信物并一起玩耍 → 温暖挥手告别。
2. **善良救助伙伴型（适合家庭/亲子 + 1 只动物配角，12–20 面）**
   - 场景：阳光河湾/草坡 → 岸边芦苇/树丛 → 星空营地。
   - 脉络：全家出游 → 发现受困/受伤的小动物 → 温柔靠近与包扎照顾 → 帮小动物找回妈妈团聚 → 星空下温暖收束。
3. **小小勇气成长型（适合单人儿童或兄弟姐妹，12–16 面）**
   - 场景：温馨卧室/客厅 → 花园/公园草坡 → 山坡观景台。
   - 脉络：收到新挑战（如放风筝/骑平衡车/夜晚看星星）→ 第一次尝试遇到小挫折 → 鼓起勇气或家人鼓励再试一次 → 成功完成挑战收获自信笑容。
4. **家庭温馨时光型（适合 2–4 人全家福，12–24 面）**
   - 单日版（最稳，1 套 Look）：海边野餐 / 森林露营 / 果园采摘的一天（出发 → 发现美景 → 野餐分享美食 → 拍照定格 → 夕阳返程）。
   - 四季版（进阶，2–3 套 Look）：春野踏青野餐（春装）→ 夏日海边踩浪吃瓜（夏装/赤脚装）→ 秋林采果登高（秋装）→ 冬雪堆雪人围炉（冬装羽绒服雪地靴）。

---

## 二、`story_plan.json` 完整模板（供 `scripts/compile_prompts.py` 编译）

在用户完成**【检查点 1】确认「人物客观档案卡 + 造型服装方案 + 分页文案」**后，按以下结构写入 `story_plan.json` 并运行 `compile_prompts.py`。

> **关键规则**：
> 1. 角色统一用代号（`c1`, `c2`...），填写真实数字 `age` 与 `gender`（`male` / `female`）。编译器会自动合成 `the 24-year-old adult man` 等客观标签，**严禁在任何英文字段中对成年人写 `son / daughter / boy / girl`**。
> 2. 角色间互动或引用道具时，直接使用 `{c1}`、`{c2}`、`{camera}` 占位符，编译器会自动展开。
> 3. 每页 `character_actions` 必须为 `present_characters` 中的**每一个人**写出独立位置、动作与视线方向，且 `caption_nouns_en` 列出的中文文案核心物体词必须全部写入该页英文描述。

```json
{
  "title": "春日山坡野餐记",
  "subtitle": "献给相亲相爱的一家人",
  "size": "landscape12",
  "style": "watercolor",
  "total_pages": 12,
  "characters": [
    {
      "id": "c1",
      "label_zh": "爸爸",
      "age": 55,
      "gender": "male",
      "appearance_en": "short neat black hair, lean elongated face, warm crinkled smile",
      "height_en": "tallest in the group, 178cm adult build"
    },
    {
      "id": "c2",
      "label_zh": "妈妈",
      "age": 53,
      "gender": "female",
      "appearance_en": "short wavy dark-brown bob hair, round gentle face, warm smiling eyes",
      "height_en": "reaching up to {c1}'s chin level, 162cm adult build"
    },
    {
      "id": "c3",
      "label_zh": "儿子",
      "age": 24,
      "gender": "male",
      "appearance_en": "short black buzz cut, square jaw, bright toothy smile",
      "height_en": "standing at the exact same shoulder and eye height as {c1}, 178cm build"
    }
  ],
  "pairwise_distinctions_en": [
    "{c1} is in his mid-50s with laugh lines around his eyes, whereas {c3} is a young man in his 20s with a short buzz cut and square jaw"
  ],
  "looks": {
    "look_spring": {
      "description_zh": "春日出游装（白上衣+牛仔裤+运动鞋）",
      "ref_image": "ref_look_spring.png",
      "outfits_en": {
        "c1": "wearing a white short-sleeve polo shirt, dark blue jeans, and casual gray sneakers",
        "c2": "wearing a cream-white knit cardigan over a light top, blue jeans, and flat white shoes",
        "c3": "wearing a plain white short-sleeve t-shirt, light blue jeans, and white sneakers"
      }
    }
  },
  "props": {
    "camera": {
      "label_zh": "奶油白复古相机",
      "short_en": "cream-white vintage camera",
      "ref_image": "ref_prop_camera.png",
      "explicit_absence": true,
      "anchor_en": "one single small cream-white vintage compact camera with a round silver lens and a thin brown leather strap, smaller than an adult's palm"
    }
  },
  "sidekicks": {},
  "scenes": {
    "spring_hill": {
      "anchor_en": "a sunlit spring hillside full of small wildflowers and fresh green grass with a few blooming cherry trees, clear pale blue sky, bright warm daylight"
    },
    "hill_sunset": {
      "anchor_en": "the same grassy spring hillside under a warm golden sunset sky at dusk, soft golden evening light"
    }
  },
  "cover": {
    "image": "page_01_cover.png",
    "scene_id": "spring_hill",
    "look_id": "look_spring",
    "present_characters": ["c1", "c2", "c3"],
    "present_props": ["camera"],
    "character_actions": {
      "c1": "standing in the lower-left center with {camera} hanging around his neck, smiling warmly",
      "c2": "standing in the lower middle beside {c1}, smiling gently",
      "c3": "standing on the lower right beside {c2}, smiling brightly"
    },
    "shot_and_gaze_en": "medium-wide portrait framing"
  },
  "pages": [
    {
      "image": "page_02.png",
      "scene_id": "spring_hill",
      "look_id": "look_spring",
      "present_characters": ["c1", "c2", "c3"],
      "present_props": ["camera"],
      "prop_states_en": {
        "camera": "hanging safely from {c1}'s neck, not held in hands"
      },
      "text_zh": "春风吹过开满野花的山坡，妈妈铺开餐布，摆好三明治和新鲜草莓。",
      "caption_nouns_en": ["wildflowers", "checkered picnic blanket", "sandwiches", "strawberries"],
      "scene_extras_en": "a light checkered picnic blanket spread on the grass, an open woven picnic basket with plates of sandwiches and red strawberries",
      "character_actions": {
        "c1": "sitting on the left of the checkered picnic blanket, pouring juice into a cup and looking down at the cup",
        "c2": "kneeling in the middle of the blanket, arranging plates of sandwiches and red strawberries with both hands, looking at the food with a warm smile",
        "c3": "sitting on the right of the blanket, reaching one hand toward a strawberry and looking happily at {c2}"
      },
      "shot_and_gaze_en": "medium candid shot, natural family interaction around the food, NOT looking at the camera"
    }
  ],
  "back": {
    "image": "",
    "ending": "最美的风景，\n是每一次和你一起出发。"
  }
}
```

> 说明：`pages` 数组实际需填满 `total_pages - 2` 项；运行 `compile_prompts.py` 后会自动在同目录生成 `prompts_manifest.md`、`prompts_manifest.json` 和供第四步直接使用的 `book.json`。

---

## 三、风格代号与规格对照表

### 1. 四种插画风格（填在 `story_plan.json` 的 `"style"` 字段）

| `"style"` 值 | 中文名称 | 风格特点与适用建议 |
|---|---|---|
| `"watercolor"` | **温馨水彩风**（默认） | 柔和粉彩、手绘水彩质感，**容错率最高，单人/多人合照首选** |
| `"storybook"` | **唯美绘本风** | 细腻笔触、柔和梦幻光影，适合亲子与家庭纪念绘本 |
| `"cartoon"` | **明亮卡通风** | 干净轮廓线、色彩饱满圆润，适合低龄儿童主角 |
| `"realistic"` | **写实插画风** | 五官还原度最高，但对透视和姿态更敏感，建议照片极清晰时选用 |

### 2. 尺寸与画幅映射（填在 `story_plan.json` 的 `"size"` 字段）

| 尺寸名称 | `"size"` 值 | 实际印刷尺寸 | HTML `@page` / PDF 参数 | 推荐生图画幅 |
|---|---|---|---|---|
| **方款 8 寸**（默认） | `square8` | 203mm × 203mm | `203mm 203mm` | `1:1` |
| **方款 10 寸** | `square10` | 254mm × 254mm | `254mm 254mm` | `1:1` |
| **横款 12 寸** | `landscape12` | 305mm × 229mm | `305mm 229mm` | `3:2` 或 `4:3` |
| **竖款 12 寸** | `portrait12` | 229mm × 305mm | `229mm 305mm` | `2:3` 或 `3:4` |

### 3. 页数（面数）可选值

**8 / 10 / 12 / 14 / 16 / 18 / 20 / 22 / 24 / 28 / 32 / 36 / 40 / 44 / 48 / 52 / 56 / 60 / 64 / 68 / 72 面**（默认 **12 面**；正文页数 = `total_pages - 2`）。

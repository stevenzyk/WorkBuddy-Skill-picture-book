# 童话故事绘本创作参考、绘本文学指南与 `story_plan.json` 模板

本文件提供绘本文学创作金标准、4 套高胜率故事骨架、`story_plan.json` 完整模板与规格对照表。
一致性细则见 `references/consistency_rules.md`，核验清单见 `references/qa_checklist.md`。

---

## 一、绘本文学创作金标准（「事件同源、繁简分流」，拒绝监控说明书）

好绘本的图与文既不是**「复读机（把生图参数直译成中文）」**，也不是**「各说各话（文字脱离画面乱抒情）」**，而是**「同一个瞬间的分工互补」**：
- **图画（英文 Prompt）做加法**：负责交代「谁、穿什么、红白格子还是藤编、站在左还是右」等一切客观视觉细节。
- **绘本正文（`text_zh`）做减法与提纯**：负责传递**图画画不出来的声音、对话、触感、温度与心绪**。

### 1. 三种可选绘本文风（按照片主角年龄智能推荐给用户选择）

| `"literary_tone"` | 文风名称 | 适配人群与智能推荐规则 | 文学特征与语言示范 |
|---|---|---|---|
| `"rhythm"` | **童趣韵律风** | **2–5 岁低幼宝宝主角（推荐）** | 短句轻快、带拟声词与轻重复韵律，适合亲子大声朗读（例：*“哗啦——哗啦——小海浪跑过来，挠了挠宝宝的小脚丫！”*） |
| `"curiosity"` | **好奇寻宝风** | **5–10 岁儿童冒险主角（推荐）** | 开头埋下小秘密或小任务，带着悬念与角色对话一页页揭晓（例：*“咦，草丛后面的藤篮动了一下——是谁在里面偷偷打喷嚏？”*） |
| `"poetic"` | **温暖收集风** | **亲子合照 / 成年家庭纪念（推荐）** | 用一条温暖线索串联日常微光，有简短对话与五感细节，走心不矫情（例：*“海风帮妈妈托起餐布的一角，把阳光和草莓的甜味一起铺在了沙滩上。”*） |

### 2. 单页写作「1 锚定 + 2 禁止 + 1 增味」法则

编写每页时，必须先写 10 字以内的 **`event_core`（本页唯一瞬间事件）**，再同源派生英文视觉描述与中文 `text_zh`：
- **1 锚定（防图文错位）**：`text_zh` 必须锚定在当前页 `event_core` 正在发生的动作或物体上，**严禁写当前画面未发生的异时空回忆或无关抒情**；凡 `text_zh` 明确点出的具象物体，必须同步列入 `caption_nouns_en` 确保画进图里。
- **2 禁止（去说明书化）**：
  1. **禁止把生图修饰词抄进正文**：图里已经画了“红白格子”“藤编”“奶油白复古”，中文正文只写“餐布”“篮子”“小相机”。
  2. **禁止连续两页用 `XX 做了 YY` 的监控汇报句式**（如连续写“妈妈铺开餐布”“爸爸倒出果汁”“女儿举起相机”）。
- **1 增味（每页至少挑 1 样融入）**：① 拟声与环境声（咔嚓、哗啦、咕嘟） ② 角色开口说的一句短对话 ③ 触觉/温度/气味（烫脚心的沙子、冒水珠的冰果汁、咸咸的海风） ④ 温柔贴切的小比喻。

### 3. 去说明书化正反对比示范（同一张画的两种写法）

| 本页核心事件 `event_core` | ❌ 监控说明书写法（生硬干瘪，严禁） | ✅ 绘本文学写法（同源互补，生动有余韵） |
|---|---|---|
| 妈妈在沙滩铺餐布摆野餐篮 | 「妈妈铺开红白格子野餐布，摆好藤编野餐篮。」 | 「哗啦——海风帮妈妈托起餐布的一角，把阳光和咸咸的香气一起铺在了沙滩上。」 |
| 爸爸给大家倒冰果汁 | 「爸爸从野餐篮里拿出果汁，倒进玻璃杯。」 | 「咕嘟咕嘟，琥珀色的橘子汁跳进杯子里，连杯壁上的小水珠都在发亮。」 |
| 姐姐举相机给家人拍照 | 「女儿举起奶油白相机，为家人拍下一张照片。」 | 「“一、二，看大海——咔嚓！”姐姐把吹乱的头发和大家的笑声，一起锁进了小小的镜头里。」 |
| 一家人赤脚走进浅浪 | 「一家人手拉手走进浅浅的海浪里。」 | 「踢掉鞋子，我们手拉手踩进白花花的浪沫里——哎呀，微凉的海水正在给脚心挠痒痒呢！」 |

---

## 二、极简剧场预算与 4 套高胜率故事骨架（Story Blueprints）

除非用户明确要求复杂长篇，编剧时遵守**「极简剧场预算」**，并先定一句话的 **`story_thread`（全书串珠线索）**：
- **造型（`looks`）套数**：默认 **1 套**，跨季节/变装故事 **≤ 3 套**（单页脱鞋赤脚/戴帽等微调直接用页级 `outfit_overrides_en`，无需新建 `Look`）。
- **核心场景（`scenes`）**：**≤ 4 个**（每个场景必填 `time_of_day`: `morning / day / sunset / night`）。
- **跨页核心道具 + 配角（`props` + `sidekicks`）**：**≤ 2–3 个**；每页只画 **1 个瞬时定格动作**。

1. **奇遇寻物归还型（适合 1–2 名主角 + 1 只动物配角，12–16 面）**：串珠线示例——*跟随一串金色小脚印，把迷路的发光松果送回家*。
2. **善良救助伙伴型（适合家庭/亲子 + 1 只动物配角，12–20 面）**：串珠线示例——*用温柔的双手护送受伤的小动物找回妈妈，点亮心里的星光*。
3. **小小勇气成长型（适合单人儿童或兄弟姐妹，12–16 面）**：串珠线示例——*三次鼓起勇气的深呼吸，让跌落的小风筝飞上最高的云朵*。
4. **家庭时光收集型（适合 2–4 人全家福，12–24 面）**：串珠线示例——*把今天海边的四种声音（浪花声、汽水声、海螺声、快门咔嚓声）装进小相机带回家*。

---

## 三、`story_plan.json` 完整模板（供 `scripts/compile_prompts.py` 编译）

在用户完成**【检查点 1】确认「人物客观档案卡 + 造型服装方案 + 故事串珠线与分页文案」**后，写入 `story_plan.json` 并运行 `compile_prompts.py`。

> **关键规则**：
> 1. 角色用代号（`c1`, `c2`...），填写真实数字 `age` 与 `gender`（`male` / `female`）。编译器自动合成 `the 24-year-old adult man` 等客观标签，**严禁在任何英文字段对成年人写 `son / daughter / boy / girl`**；中文 `text_zh` 对成年儿女也避免生硬旁白点名“儿子/女儿”，优先用亲切昵称或“我们/姐姐/弟弟”。
> 2. 随身小配件（如掌心相机、钥匙、贝壳）设 `"is_small_accessory": true`；**风筝、雨伞、帐篷、单车等户外激活道具设 `"outdoor_active_only": true`**——在室内场景中，`prop_states_en` **必须写明平放桌面/拿在手中/挂在墙面等收纳准备态，严禁在室内写升空飞翔（如在客厅放飞风筝会被编译器直接报错拦截）**！
> 3. 凡某页启用了 `present_props`，**必填** `prop_states_en` 交代具体挂载/持握/放置位置；单页赤脚踩水、回家上床脱鞋只需填 `"outfit_overrides_en": {"c1": "barefoot, no shoes"}` 或 `"wearing cozy indoor slippers, NO outdoor sneakers"`。
> 4. `scenes` 必填 `time_of_day`（`morning < day < sunset < night`）与 `environment`（`"indoor"` / `"outdoor"`）。**同一个家或同一片公园跨时段出现时，必填相同的 `"location_group"` 并原样复用同一套窗框材质、窗帘、沙发或标志性树林描述**（仅改光线），编译器会硬校验共享陈设词防中途换装修。
> 5. **严禁全书照抄基准图“从左到右一字排开罚站”**：相邻多人页必须主动变换站位队形（如围坐野餐垫半圆、前后景奔跑呼应、侧身行走、聚拢看同一件物品）。

```json
{
  "title": "把大海装进口袋",
  "subtitle": "献给相亲相爱的一家人",
  "story_thread": "一家人去海边收集四种夏天的声音（浪花声、冰果汁声、小海螺声、快门咔嚓声），全部装进相机带回家",
  "literary_tone": "poetic",
  "size": "square8",
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
      "label_zh": "姐姐",
      "age": 26,
      "gender": "female",
      "appearance_en": "long straight chestnut-brown hair, oval face, bright eyes",
      "height_en": "slightly taller than {c2}, reaching {c1}'s ear level, 166cm adult build"
    },
    {
      "id": "c4",
      "label_zh": "弟弟",
      "age": 24,
      "gender": "male",
      "appearance_en": "short black buzz cut, square jaw, bright toothy smile",
      "height_en": "standing at the exact same shoulder and eye height as {c1}, 178cm build"
    }
  ],
  "pairwise_distinctions_en": [
    "{c1} is in his mid-50s with laugh lines, whereas {c4} is in his 20s with a short buzz cut; {c2} has short wavy bob hair, whereas {c3} has long straight chestnut-brown hair"
  ],
  "looks": {
    "look_beach": {
      "description_zh": "夏日海边清爽白上衣+浅蓝牛仔裤+小白鞋",
      "ref_image": "ref_look_beach.png",
      "outfits_en": {
        "c1": "wearing a white short-sleeve polo shirt, blue jeans, and casual white sneakers",
        "c2": "wearing a white sleeveless lace top with a pearl necklace, light blue jeans, and flat white shoes",
        "c3": "wearing a plain white short-sleeve t-shirt, light blue jeans, and white sneakers",
        "c4": "wearing a plain white short-sleeve t-shirt, light blue jeans, and white sneakers"
      }
    }
  },
  "props": {
    "camera": {
      "label_zh": "奶油白复古小相机",
      "short_en": "cream-white vintage camera",
      "ref_image": "ref_prop_camera.png",
      "is_small_accessory": true,
      "outdoor_active_only": false,
      "explicit_absence": true,
      "anchor_en": "one single small cream-white vintage compact camera with a round silver lens and a thin brown leather neck strap, smaller than an adult's palm"
    }
  },
  "sidekicks": {},
  "scenes": {
    "beach_morning": {
      "time_of_day": "morning",
      "environment": "outdoor",
      "location_group": "family_beach",
      "anchor_en": "a gentle golden sandy beach with distant coastal pine trees beside a clear turquoise sea with soft white foam waves, pale blue morning sky, soft morning daylight"
    },
    "beach_day": {
      "time_of_day": "day",
      "environment": "outdoor",
      "location_group": "family_beach",
      "anchor_en": "the same golden sandy beach with distant coastal pine trees beside a calm turquoise sea with soft white foam waves, clear sky with soft white clouds, bright warm daylight"
    },
    "beach_sunset": {
      "time_of_day": "sunset",
      "environment": "outdoor",
      "location_group": "family_beach",
      "anchor_en": "the same golden sandy beach with distant coastal pine trees beside the calm sea with soft foam waves, glowing under a warm golden-orange sunset sky"
    }
  },
  "cover": {
    "image": "page_01_cover.png",
    "scene_id": "beach_day",
    "look_id": "look_beach",
    "present_characters": ["c1", "c2", "c3", "c4"],
    "present_props": ["camera"],
    "prop_states_en": {
      "camera": "hanging neatly on {c1}'s chest from its thin brown leather neck strap, palm-sized against his shirt"
    },
    "character_actions": {
      "c2": "standing slightly in front on the left, smiling warmly",
      "c1": "standing beside {c2} with one arm gently around her shoulder, smiling warmly",
      "c3": "standing in a relaxed pose beside {c1}, smiling gently",
      "c4": "standing on the right turned slightly inward toward the family, grinning brightly"
    },
    "shot_and_gaze_en": "medium-wide family portrait framing"
  },
  "pages": [
    {
      "image": "page_02.png",
      "event_core": "姐姐半蹲在前景举相机给身后聚拢的家人拍海边合影",
      "scene_id": "beach_day",
      "look_id": "look_beach",
      "present_characters": ["c1", "c2", "c3", "c4"],
      "present_props": ["camera"],
      "focus_props": ["camera"],
      "prop_states_en": {
        "camera": "held up in both of {c3}'s hands at her eye level, palm-sized"
      },
      "text_zh": "“一、二，看大海——咔嚓！”姐姐把海风吹乱的刘海和大家的笑声，一起锁进了小小的镜头里。",
      "caption_nouns_en": ["sea", "camera"],
      "character_actions": {
        "c3": "crouching playfully in the right foreground in 3/4 back-side view, raising {camera} to her eye with both hands aimed at the family",
        "c2": "standing in the center midground leaning close to {c1}, laughing happily toward {c3}'s lens",
        "c1": "standing in the midground beside {c2} with a warm grin toward {c3}",
        "c4": "leaning in cheerfully next to {c1} in the midground, making a joyful wave toward {c3}"
      },
      "shot_and_gaze_en": "layered foreground-to-midground storybook framing, lively natural cluster rather than a flat horizontal row, NOT staring at the viewer"
    },
    {
      "image": "page_03.png",
      "event_core": "一家四口赤脚手拉手踩进夕阳海浪",
      "scene_id": "beach_sunset",
      "look_id": "look_beach",
      "present_characters": ["c1", "c2", "c3", "c4"],
      "present_props": [],
      "outfit_overrides_en": {
        "c1": "rolled-up jeans cuffs, completely barefoot with NO shoes and NO socks",
        "c2": "rolled-up jeans cuffs, completely barefoot with NO shoes and NO socks",
        "c3": "rolled-up jeans cuffs, completely barefoot with NO shoes and NO socks",
        "c4": "rolled-up jeans cuffs, completely barefoot with NO shoes and NO socks"
      },
      "text_zh": "踢掉鞋子，我们手拉手踩进金灿灿的浪沫里——哎呀，微凉的海水正在给脚心挠痒痒呢！",
      "caption_nouns_en": ["barefoot", "holding hands", "foam"],
      "scene_extras_en": "shallow golden-lit sea foam swirling around their bare ankles",
      "character_actions": {
        "c1": "standing barefoot in shallow waves on the left, holding {c2}'s hand and laughing down at the water",
        "c2": "standing barefoot in the middle-left holding hands with {c1} and {c3}, smiling joyfully",
        "c3": "standing barefoot in the middle-right holding hands with {c2} and {c4}, looking down at the splashing foam",
        "c4": "standing barefoot on the right holding {c3}'s hand, grinning happily"
      },
      "shot_and_gaze_en": "wide candid shot from the front-side, natural movement, NOT staring stiffly at the viewer"
    }
  ],
  "back": {
    "image": "",
    "ending": "最美的风景，\n是每一次和你一起出发。"
  }
}
```

---

## 四、画风与画幅规格对照表（方案 A：封面与正文画框精准匹配）

| 尺寸名称 | `"size"` 值 | 实际印刷尺寸 | 封面/封底生图画幅（全出血） | 正文插画生图画幅（78% 插画框） |
|---|---|---|---|---|
| **方款 8 寸**（默认） | `square8` | 203mm × 203mm | `1:1` | **`4:3`**（防 `1:1` 裁掉脚尖） |
| **方款 10 寸** | `square10` | 254mm × 254mm | `1:1` | **`4:3`**（防 `1:1` 裁掉脚尖） |
| **横款 12 寸** | `landscape12` | 305mm × 229mm | `4:3` 或 `3:2` | `16:9` 或 `3:2` |
| **竖款 12 寸** | `portrait12` | 229mm × 305mm | `3:4` 或 `2:3` | `1:1` 或 `4:3` |

**可选页数（面数）**：`8 / 10 / 12 / 14 / 16 / 18 / 20 / 22 / 24 / 28 / 32 / 36 / 40 / 44 / 48 / 52 / 56 / 60 / 64 / 68 / 72` 面（默认 **12 面**；正文页数 = `total_pages - 2`）。

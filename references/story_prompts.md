# 童话故事绘本创作参考

本文件提供创作童话故事脚本与生成插画时可复用的提示词模板和示例。

## 〇、故事圣经模板（一致性的根基，先写这个）

在编写分页脚本、生成任何插画之前，先填写这份「故事圣经」。它贯穿全书，是画面与文字的唯一依据。

```
【人物设定清单】
- 主角外貌（固定，逐页一字不改）：<发型、发色、脸型、五官、标志性特征>
- 主角服装与随身道具（固定）：<如：灰色毛衣 + 一条红色围巾 + 帆布包>
- 恒穿装备（如有，单独标注，全书任何页面都穿着，含睡觉/休息/上岸等"看似可脱"的场景）：<如：橙色救生衣——全书恒穿，每页 prompt 都写 wearing an orange life vest>
- 配角 1（如小松鼠）：<外观描述>
- 配角 2（如冬爷爷）：<外观描述>
- 【多主角场景】多人角色「区分性锚点」+「全员基准图」说明：<当有 ≥2 个人类角色时，先合成一张全员同框基准图；若多个角色外貌相似，写一条区分性对比句钉死年龄/身高/脸型/发型差异>

【视觉锚点清单】（每个反复出现的元素，写一段可直接粘贴进 prompt 的英文描述，逐页一字不改复用；以下示例中的「雾婆婆/灯笼/椅子」等仅为格式示范，实际按本故事的角色和道具填写）
- 主角锚点：<英文，覆盖外貌+服装+随身道具，如：a gentle Chinese man in his 30s with short black hair, round face, a small mole between his eyebrows, wearing a dark blue long coat and a mustard-yellow scarf>
- 配角锚点：<英文，覆盖该配角外貌+标志性服装/特征>
- 多角色「区分性锚点」（≥2 个相似的人类角色，防撞脸）：<如：an older chubby boy with bangs covering his forehead, clearly taller and bigger ↔ a younger small boy with a buzz cut showing a wide forehead, clearly shorter and smaller —— 每页同框时同时写两人的对比句，防止画成同一个人>
- 多角色「全员基准图」说明（≥2 个人类角色）：<先用各角色基准图合成一张全员同框图，作为多人同框页的 image1 参考；单人特写页用对应单人基准图；禁止多人同框页只传 1 张参考图靠文字兜底>
- 动物类配角锚点（体型+标志性部位+特效状态，三者缺一不可）：<英文，如：a small young fawn much smaller than the children, only reaching up to their chest, with tiny little antlers and white spots on its back, glowing softly with a warm golden light —— 必须写清①体型相对人物的比例 ②角/耳/尾等标志性部位的大小形态 ③是否发光，防止跨页变幼崽/成年大兽/有角变没角/发光变不发光。**注意：动物处于游泳/飞行/奔跑等动态姿态或水下/空中环境时，体型锚点要加「绝对尺寸+相对比例+动态下保持很小」三重锁定，如 a very small young dolphin that is tiny, no bigger than a small puppy, clearly much smaller than the boys, only reaching up to their knees, keeping its small size even while swimming。另外，若剧情要求配角「驮人/抱人/载人」，其体型必须与动作自洽——不能设定成「比人还小」却又要驮人，否则模型会在驮人页把它放大。要么把配角设定得足够大，要么换一种不需要它变大的动作方式（如改「骑龙」为「龙喷星光、人物乘星光飞行」）**>
- 动物/幻想生物「风格类型」锚点（对有多种常见造型的生物，必须锁死「哪种造型」）：<如：卡通龙 → a chubby round-bodied cartoon baby dragon with big cute eyes, tiny pink bat-like wings, and two tiny horns；中式龙 → a long slender Chinese dragon with whiskers, antler-like horns and scales —— 两者绝不能混用，否则这一页是 Q 版卡通龙、下一页变成细长中式龙，跨页风格横跳>
- 翅膀归属/隔离锚点（带翅膀配角与主角同框，防翅膀漂移到人身上）：<如：the <会飞配角> flying beside them, its wings attached to its own body, the <主角> standing with a clean bare back —— 配角尽量画在主角旁边而非正背后，避免翅膀与主角身体重叠、看起来像主角长了翅膀。**注意：`NO wings` 这类否定写法效果有限，根本手段是正面写清翅膀归属 + 调整位置让翅膀不与人重叠**>
- 服装纯净性锚点（动态动作页防「加戏」多出披肩/飘带/围巾）：<如：飞行的孩子穿短袖 T 恤 + 长裤，要正面写 wearing exactly his short-sleeve t-shirt and long pants, nothing else。**注意：真正触发加披风的是 "clothes fluttering in the wind / flowing fabric" 这类「飘动」词，`NO cape` 这类否定词不如正面写清服装 + 删掉 fluttering 有效——飞行姿态只用 feet clearly off the ground 表达，不写「衣服/头发飘动」**>
- 遮挡关系锚点（「A 绕 B 转」防身体被遮挡断裂）：<如：小鸟绕塔转 → 要么写 the bird flying to the left side of the tower, its whole body fully visible in front of the tower，要么写 flying in front of the tower, its full body clearly visible, not hidden behind the tower —— 避免 A 绕到 B 背后导致身体被截断、左右各露一截像断成两段>
- 肢体数量锚点（多人并肩做伸手动作防「多手」）：<如：两人挥手告别 → each character has exactly two arms and two hands, <角色A> raising his right hand, <角色B> raising his right hand, no extra arms or hands —— 防止某人被画成三只手、或手长到别人身上>
- 多角色「逐个点名」锚点（共享载体防漏人/多人，关键）：<多人同框页要**正面写全、逐个点名每个角色 + 各自位置/动作**，如：the father sits at the back holding a black paddle, the mother sits in the middle holding the little boy, the older boy sits at the front looking to the left, the little boy sits on the mother's lap pointing at the reeds —— 每人一句话、一个都不能少。**判断标准不是"有没有某个词"，而是"该有的每个角色是否都被正面写出来"**——「一家四口」「全家」「大家」这类说法本质上是"没把每个人写出来"，等于把"画谁"交给模型自由发挥，就会漏掉「叙事焦点之外」的角色；不要靠穷举禁用这类词（说法无限、堵不完），而要反过来强制逐个点名。同时**配角/动物的空间位置也要正面写死 + 写清不该出现的位置**，如：`<动物配角> standing on the reedy riverbank, NOT on the <载体>` —— 防止配角被模型挪到载体上（乱入）>
- 核心物体「唯一性」重申（动作复杂页也要防「一个变两个」）：<如：唯一的一颗星星 → only one single star in the sky, no other stars —— 人物动作再复杂也不能省略唯一性声明>
- 动作姿态锚点（飞、跑、跳、挥手、吹、绕圈等动态动作，要把姿态写具体）：<如：飞 → flying through the air, feet off the ground, floating upward；挥手 → waving their hands high in the air；绕圈 → flying in circles around the star；流星 → a shooting star streaking across the sky with a bright glowing trail —— 否则会画成「站着没离地/手垂身侧/原地站着」的弱动作>
- 方向性锚点（上山/下山、走进/走出、面向/背向等有方向含义的动作）：<如：上山写 walking uphill toward the mountaintop, seen from behind, moving away from the viewer；走出写 walking out of the cave, the cave entrance behind them —— 避免画反方向>
- 标志性动作归属页（全书只出现一次的标志性动作，要锁死发生在第几页）：<如：「许愿」只发生在第 9 页，第 8 页绝不能画许愿动作；「挥手告别」只发生在第 14 页，且第 14 页必须真的画出挥手。生成后逐页核验动作没有提前/延后/对调>
- 核心物体「唯一性+位置+大小+颜色」锚点（全书唯一、反复出现的固定物体）：<如：one single large golden-yellow flower with a bright golden center growing in the exact center of the cave floor, as tall as the children；该物体不该出现时显式写 the flower is not visible in this scene —— 防止位置漂移/大小突变/从一个变两个/换色。**核心物体每一页都必须交代（要么嵌入完整锚点、要么显式 not visible），禁止因镜头焦点转移而省略；其颜色在夜晚/黄昏/水下等特殊光照页也要原样锁死，如 keeping its golden-yellow petals even in the dim night light**>
- 核心道具/载体/动物配角/固定物「基准图」锚点（四类反复出现、结构复杂或外形有辨识度的元素，除文字锚点外都**必须单独生成一张干净特写基准图**，并逐页作为 image2/image3 传入 input_fidelity: low）：<如船/漂流艇/车/飞艇/房/灯笼等道具载体：文字锚点如 one single inflatable orange raft with exactly three separate air chambers, a blunt rounded bow and stern, and a ring of grab-rope around its rim, no writing or pattern on its hull —— 文字锁死「结构部件数+两端形状+边沿+颜色+数量(exactly one)」，但图片参考才是防漂移硬约束；如动物/幻想生物配角（狐狸/龙/精灵/海豚等）：也要配「配角基准图」，文字锚点锁死体型+部位+特效+风格类型；如核心固定物体（洞中央的花/灯塔/魔法树）：也要配基准图，文字锚点锁死唯一性+位置+大小+颜色；如贯穿性道具（种子/钥匙/贝壳）：也要配基准图，文字锚点锁死类型+形状+颜色+大小。四类元素共同的判断标准：读者在每一页能否认出是「同一个」>
- 相似元素「区分性锚点」（两个形象相似、易混淆的元素）：<如：小精灵 a very small flying fairy about the size of a child's hand, with a cute face and hanging tendrils ↔ 大花 a very large flower fixed to the ground, no face, much bigger than the children —— 防止模型把 A 画成 B 或让两者合体>

【场景清单】（本次新增，明确全书有哪几个场景、各出现在哪几页；场景由本故事剧情决定。**每个场景锚点必须内嵌「时间/光线」——把 deep dark night sky / bright daylight 这类光词焊死进场景锚点里，逐字复用，否则某段场景会集体漂移成白天/黄昏**）
- 场景 A：第 X-Y 页（夜晚 → 场景锚点含 deep dark night sky）
- 场景 B：第 X-Y 页（白天 → 场景锚点含 bright daylight）
- ...

【道具持有状态时间线】（本次新增，逐页明确道具在谁手里；按本故事实际道具填写）
- 道具 1：第 X 页在谁手里 → 第 Y 页…… → 第 Z 页放下/传递
- 道具 2：……

【道具清单与贯穿规则】
- 道具 A：来源<谁在何时给> → 出现<哪几页> → 去向<最终结果>
- 道具 B：来源<…> → 变化<…> → 去向<…>

【状态连续性清单】（按页列出时间线，含环境变化）
- 第 X-Y 页：<服装状态 / 健康状态 / 环境>
- 第 Z 页：<状态变化，须有前页铺垫>
- 【状态类特征分阶段】<若某角色/道具有「受伤→包扎→愈合」「干净→脏→洗净」这类递进状态，逐页写清本页处于哪个阶段；前期页禁止出现后期状态（如包扎前的页面绝不能写"缠纱布"，只能写"裸露受伤"）。若该角色/道具有基准图，基准图应采用「初始/无状态」形态，后期状态在对应页用 prompt 临时追加>
- 【状态跨角色隔离】<若故事里有两个同类角色（如两只同种动物、妈妈和小崽），且其中一个有「受伤→包扎→愈合」这类递进状态，必须把「状态 + 所属角色」绑定写死：受伤那只写成 the injured baby otter with its front paw wrapped in white bandage，同框的健康同类角色显式写 the mother otter is healthy, with no bandage and no injury —— 防止状态从 A 串到 B。基准图不能用后期状态形态，否则会连带着把状态「传染」给同框同类角色>
```

**使用规则**：后续每页的画面描述和文案都必须「回查」这份圣经——道具不能凭空出现、服装状态要有铺垫、健康状态要连贯、环境要用场景锚点统一。**生成图片时，prompt 里出现的每个角色/道具/场景/动作，都必须原样嵌入对应的视觉锚点英文描述，禁止改写。**

**【强制】主角基准图逐页复用**：主角基准图生成后，所有「出现主角」的页面都必须把基准图作为 image-to-image 参考图（`image1` + `input_fidelity: low/medium`）传入，**禁止用纯 text-to-image 独立生成人物页**；否则人脸、画风、道具细节（条纹横竖、包型等）会逐页漂移。只有纯风景/空镜页可用纯文字生成。

**【强制·本次新增】四类元素基准图逐页复用**：除主角基准图外，以下四类「反复出现、结构复杂或外形有辨识度」的元素也要各自单独生成一张「基准图」（干净特写）：①核心道具/载体（船、漂流艇、车、飞艇、房、灯笼等）②动物/幻想生物配角（狐狸、龙、精灵、海豚等）③核心固定物体（洞中央的花、灯塔、魔法树等）④贯穿性剧情道具（种子、钥匙、贝壳等）。并在所有出现该元素的页面作为 image-to-image 参考图（`image2`/`image3` + `input_fidelity: low`）传入，与人物基准图一起用。**文字锚点无法替代图片参考**——文字写死「颜色+形状+部件数+两端形状+边沿圈数」仍兜不住模型在复杂动作页/特殊光照页的自由发挥（圆头船变尖头船、两段气囊变三段气囊、卡通龙变中式龙）。判断标准：这四类元素在每一页读者能否认出是「同一个」。

**风格统一约束（本次新增，重要）**：全书插画必须统一为**同一种手绘风格**，禁止任何页面出现「照片实景背景」。用照片做参考图时 `input_fidelity` 建议设为 **low**，且**纯风景/环境页（特写道具、场景空镜）不要附带人物照片参考图**，避免照片原背景（真实木栈道、石墙、树）被照搬进画面。

## 一、分页脚本模板

基于故事圣经，按以下结构输出分页脚本（画面描述与文案必须指向同一场景）：

```
【封面】
- 标题：<故事标题>
- 副标题 / 作者署名：<可选>
- 画面描述（英文）：<用于文生图>

【第 1 页】
- 画面描述（英文）：<精确到服装、道具、动作、状态、环境>
- 文案（中文）：<与画面描述完全对应，1-3 句，30-60 字>
- 涉及道具/状态：<本页新增或变化的道具、服装、健康状态>

【第 2 页】
...

【封底】
- 文案：<一句温暖的话 / 寓意>
```

**画面描述与文案对应示例**（以下仅为「图文必须指向同一动作」的格式示范，实际按本故事内容填写）：
- ✅ 画面：`the child carrying the injured little animal into a cave` ↔ 文案：「小朋友把小动物背进山洞」（动作一致）
- ❌ 画面：`the child warming himself by a campfire` ↔ 文案：「小朋友把小动物背进山洞」（错位！文字是「背」，画面却是「烤火」）

## 二、童话故事结构参考

经典三段式结构，适合 3-8 岁读者：

1. **开头（1-2 页）**：介绍主角（名字、住在哪里、平凡但有特点的生活），建立亲切感。
2. **冲突（2-4 页）**：主角遇到一个困难或一场奇遇（迷路、帮助他人、得到魔法、森林冒险）。
3. **高潮（2-3 页）**：主角鼓起勇气/用智慧/靠善良解决问题。
4. **结尾（1-2 页）**：温暖收束，主角成长或获得友谊，点出一句寓意（如「善良的心，是世界上最亮的灯」）。

**语言技巧**：
- 低龄（3-5 岁）：短句、重复句式（「小狐狸走啊走……走啊走……」）、拟声词（「哗啦」「咕噜咕噜」）。
- 儿童（5-8 岁）：可加入简单对话、更多形容词，但每页仍控制在 60 字以内。

## 三、插画风格文生图提示词参考

以下为不同风格的「风格前缀」，可拼接在每页画面描述之前。

**温馨水彩风**：
```
soft watercolor children's book illustration, gentle pastel colors, dreamy and warm atmosphere, soft edges, hand-painted texture, whimsical storybook style, high quality picture book art
```

**明亮卡通风**：
```
bright cheerful cartoon children's book illustration, bold clean outlines, vibrant saturated colors, cute rounded character design, playful and lively, flat color storybook style
```

**写实插画风**：
```
realistic detailed children's book illustration, soft natural lighting, rich textures, expressive realistic characters, warm cinematic atmosphere, high-detail storybook art
```

**唯美绘本风**：
```
beautiful storybook illustration, soft dreamy lighting, pastel and warm color palette, delicate painterly style, gentle emotional mood, high quality picture book art
```

## 四、人物照片卡通化提示词模板

将照片卡通化为主角形象时使用（image-to-image，参考图为用户照片）：

```
A <style_prefix>, <character description>,
portrait of a <age/gender> child as the main character in a fairy tale,
keep the recognizable facial features from the reference photo (hairstyle, hair color, face shape, eyes),
full body or half body, clean simple background, suitable for picture book page
```

**人物特征描述**（从照片提取后固定复用）：发型、发色、脸型、眼睛大小、肤色、标志性服饰或配饰。例如：

> a cute little girl with shoulder-length black hair, round face, big bright eyes, wearing a yellow dress with a small red bow

**角色一致性原则**：每页插画 prompt 中都**完整重复**这段人物特征描述，并在正文页描述该页场景动作。

## 五、分页画面描述示例

以「温馨水彩风 + 黑发小女孩主角」为例：

- 封面：`soft watercolor children's book illustration, a cute little girl with shoulder-length black hair, round face, big bright eyes, wearing a yellow dress with a red bow, standing in a magical glowing forest, title space at top, dreamy warm atmosphere`
- 正文第 2 页：`soft watercolor children's book illustration, the same cute little girl with shoulder-length black hair, round face, big bright eyes, yellow dress with red bow, walking along a winding forest path, talking to a friendly little fox, soft pastel colors`

## 六、常见主题方向（供用户选择时列举）

- 冒险：去森林 / 深海 / 天空探险
- 勇气：克服胆小 / 夜晚不害怕 / 第一次独立完成某事
- 友谊：与新朋友（小动物 / 小伙伴）结下友谊
- 善良：帮助迷路的小动物 / 分享 / 照顾他人
- 成长：学会新本领 / 承担责任 / 变得勇敢自信
- 魔法：得到魔法道具 / 会魔法的孩子 / 奇幻世界奇遇

## 七、排版前一致性自检清单（必做）

生成完所有插画、排版之前，逐条核对，发现问题立即重生成对应页：

**元素视觉一致性**
- [ ] 同一个道具（如灯笼）在不同页的图里，外观是否一致？（颜色、形状、有无脸、大小）
- [ ] 同一个配角在不同页的图里，形象是否统一？
- [ ] 主角的服装、随身道具在全书各页是否统一？

**人物一致性检查（本次新增，关键）**
- [ ] 任意两页（尤其封面 vs 正文、正文各页之间）的主角，脸型、五官、发型、服装、随身道具是否一致？
- [ ] 有没有「封面一个样、正文另一个样」「某页人物明显画风不同」的漂移？
- [ ] 若有漂移，说明该页没用基准图做参考，须改用基准图（image-to-image）重生成。

**道具外观逐维度检查（本次新增）**
- [ ] 同一件道具在每页，颜色、形状、盖子/提手等细节、尺寸是否始终如一？
- [ ] 专属某角色的随身道具，是否每页都在同一个人手里、连人带物一起出现？
- [ ] 有没有「这页一种形状、下页变另一种形状」的外观漂移？

**贯穿性道具一致性检查（本次新增）**
- [ ] 被拿起/传递/使用的剧情道具（种子、魔法花、钥匙、贝壳等）在每页，种类、形状、颜色、大小是否始终如一？
- [ ] 有没有「这页海螺、下页变扇贝」的悄悄变形？该道具不在场的页有没有凭空冒出？

**动物配角体型/部位/特效检查（本次新增）**
- [ ] 同一只动物配角在每页，体型（相对人物比例）、标志性部位（角/耳/尾大小形态）、是否发光，是否始终如一？
- [ ] 有没有「这页是幼崽、下页变成年大兽」「这页有角下页没角」「这页发光下页不发光」的漂移？

**动物配角「风格类型」检查（本次新增，关键）**
- [ ] 同一只生物配角（龙/凤凰/狐狸/精灵等）在每页，是否始终是「同一种造型风格」？
- [ ] 有没有「这一页是圆滚滚 Q 版卡通龙、下一页变成细长中式龙（龙须/鹿角/鳞片）」的风格横跳？

**翅膀归属/隔离检查（本次新增，关键）**
- [ ] 带翅膀的配角与主角同框的页，那对翅膀是否清晰地「长」在配角身上，而非错位到主角肩/背上？
- [ ] 主角的背部是否干净，有没有「凭空多出一对翅膀」？（尤其检查「配角飞在主角身后、身体被挡住只露出翅膀」的页）

**服装纯净性检查（本次新增）**
- [ ] 动态动作页（飞行/腾空/奔跑）里，人物有没有被模型凭空加上披肩、斗篷、飘带、彩带、围巾等本不存在的服饰？
- [ ] 人物的服装是否与静态页完全一致？

**遮挡断裂检查（本次新增）**
- [ ] 「A 绕着 B 转」的动作页里，A 的身体是否完整、连贯，没有被 B 遮挡导致「身体断裂/多出尾巴/缺一段身体」？

**人物肢体数量检查（本次新增）**
- [ ] 多人并肩做「伸手类」动作的页，每个人是否都恰好只有两只手两条腿？有没有「某人三只手」「某人的手长到别人身上」？

**多人同框「漏人/多人」检查（本次新增，关键）**
- [ ] 共享载体（船/车/桌）的多角色页，载体上的人数是否恒等于角色总数？有没有「这页少 1 人、那页少 2 人」的漏人？
- [ ] 反向核对：有没有「多出不该出现在载体/位置的角色或道具」（示例：某动物配角本该在岸边、却被画到了船上）？
- [ ] 生成前核对多人同框页 prompt 是否「把每个该出现的角色都逐个点名 + 各自位置/动作」正面写全（而非用「一家四口/全家/大家」这类一笔带过的说法）？该有的 N 个人是否各自都有一句位置+动作？

**核心物体唯一性（复杂动作页）检查（本次新增）**
- [ ] 含「唯一性物体」的页（尤其动作复杂页），该物体是否恰好只有「一个」？有没有被画成两个？

**场景/背景一致性（本次新增，重点）**
- [ ] 同一场景在相邻页的背景是否一致？（有没有「场景 A→场景 B→场景 A」的跳变）
- [ ] 有没有出现「照片实景背景」与手绘插画风格割裂的情况？
- [ ] 每个场景是否都用同一段「场景锚点」描述生成，而非各页自由发挥？

**物理关系检查（本次新增）**
- [ ] 人物与道具的空间关系是否正确？（坐姿是否真的坐在椅子上、有没有穿模、有没有「人陷进椅子里/站在椅子前」）
- [ ] 人物拿、抱、背等动作与道具是否吻合？

**道具类型一致性（本次新增）**
- [ ] 同一种道具在全书是否类型统一、外观一致？（有没有同一件东西在某页换了种类或变了样）

**四类元素基准图复用检查（本次新增，关键）**
- [ ] ①核心道具/载体（船/漂流艇/车/飞艇/房/灯笼等）②动物/幻想生物配角（狐狸/龙/精灵/海豚等）③核心固定物体（洞中央的花/灯塔/魔法树等）④贯穿性剧情道具（种子/钥匙/贝壳等），是否每一页都用了对应的「基准图」做 image-to-image 参考（而非只靠文字）？
- [ ] 有没有「某页元素明显变样、和基准图对不上」？有则该页没传基准图，须改用基准图重生成。

**道具持有状态（本次新增）**
- [ ] 逐页核对：该拿道具的页有没有拿？该放下的页有没有放下？
- [ ] 多人「一起用同一件道具」的页，是不是共握同一件（而非各拿各的）？
- [ ] 有没有某页道具凭空消失？

**场景切换检查（本次新增）**
- [ ] 场景切换的页有没有残留上一个场景的物件？
- [ ] 切换后的场景是否只包含「本场景该有的东西」？

**动作 ↔ 文案逐字检查（本次新增）**
- [ ] 文案的核心动作画面是否精确呈现？
- [ ] 有没有「文字写一起用同一件、画面各拿各的」的错位？

**标志性动作归属检查（本次新增，关键）**
- [ ] 全书只出现一次的标志性动作（许愿、挥手告别、吹出星光等），是否恰好出现在它该在的那一页？
- [ ] 有没有「第 N 页该许愿却没许愿、第 N-1 页不该许愿却许愿」的提前/延后/对调错位？

**动作姿态检查（本次新增）**
- [ ] 文案写的「飞/跑/跳/挥手/吹/绕圈」等动态动作，画面是否真的呈现了该姿态（脚离地、手高举、在绕圈、有流星轨迹）？
- [ ] 有没有「飞」画成「站着没离地」、「挥手」画成「手垂身侧」、「绕圈」画成「原地站」的弱化？

**时间/光线一致性检查（本次新增）**
- [ ] 文案写「天黑了」画面是否真的是黑夜（而非黄昏亮天）？文案写「黄昏」是否真的是黄昏？
- [ ] 有没有时间词与画面光线矛盾？
- [ ] **按「场景」整段核验**：同一个场景（如「屋顶」段）的所有页，天空色/光线是否全部一致，有没有「某一段场景集体漂移成白天/黄昏」的整段错误？

**星空陪衬检查（本次新增）**
- [ ] 「看星星/仰望星空」的画面里，是否有一片星空（许多普通星星），而不是只有孤零零一颗核心星？

**方向性检查（本次新增）**
- [ ] 涉及「上山/下山、走进/走出、面向/背向」的页，画面朝向是否与文案一致？
- [ ] 有没有「文字写上山、画面像下山」「文字写走出洞、画面像刚到洞口」的错位？

**核心物体「唯一性+位置+大小+颜色」检查（本次新增）**
- [ ] 全书「唯一」的固定物体（洞中央的花、山顶的灯塔等）在每一页出现时，位置、大小、数量、颜色是否始终如一？
- [ ] 有没有位置漂移、大小突变、从一个变两个？
- [ ] 该物体不该出现的页，有没有凭空冒出？

**核心物体颜色一致性检查（本次新增）**
- [ ] 核心物体（魔法花、灯塔等）在白天页 vs 夜晚/黄昏/水下页，颜色是否始终如一？
- [ ] 有没有「白天金黄、夜晚变蓝紫、黄昏变淡绿」的换色漂移？

**核心物体逐页存在性检查（本次新增，硬约束）**
- [ ] 逐页核对核心物体：它在该页要么在画面里且外观一致，要么 prompt 有显式 `not visible` 声明。
- [ ] 有没有「剧情没提它、它就凭空消失」的情况（如剧情进入后续阶段后，作为核心的那一个物体悄悄不见了）？

**相似元素区分检查（本次新增）**
- [ ] 两个形象相似的元素（花形精灵 vs 冰晶花等），读者能否一眼区分？
- [ ] 有没有在某一页被画成同一个东西、或形象在两者间漂移？

**相邻页重复检查（本次新增）**
- [ ] 有没有两页画面/构图高度相似？有则应在脚本阶段调整。

**环境连贯性**
- [ ] 每页的环境/背景是否与画面描述、前后页逻辑一致？
- [ ] 有没有环境跳变？（森林里发生的事，背景突然变成室内/海底）
- [ ] 环境与设定是否矛盾？（山顶的灯塔不能画在海里、雪原场景不能画成室内房间）

**封面排版**
- [ ] 封面标题是否放在顶部留白区、没有遮挡人物脸部或身体？

**道具贯穿检查**
- [ ] 每件道具是否都有「来源 → 出现 → 去向」的完整链条？
- [ ] 有没有某页凭空冒出前文从未交代的新道具？

**状态连续性**
- [ ] 健康状态变化是否有铺垫？（「某状态 → 某状态 → 某状态」逐页衔接，而非突然跳变）
- [ ] 【状态类特征分阶段检查】有没有把「后期状态」提前到「前期页面」？（如「包扎」前却已经缠了纱布、「洗净」前却已经干净）。若有，说明该页 prompt 或基准图把后期状态写成了固定特征，须按状态链改为「本页所处阶段」的状态描述。
- [ ] 【状态跨角色隔离检查】两个同类角色里，只有一个有「受伤/脏污/破损」等状态时，那个状态是否始终只属于「那一个」角色？同框的健康同类角色有没有被「传染」上同样的状态？（如受伤的小水獭和健康的水獭妈妈同框，妈妈是否被画成也受伤了）若有，须重生成，并把「受伤的是谁、健康的是谁」写死。
- [ ] 时间 / 天气 / 环境是否连贯？

**画面 ↔ 文案对应**
- [ ] 逐页对照：文字提到的关键元素（道具、服装、动作、状态、环境）是否都出现在画面里？
- [ ] 有没有「文字写 A，画面画 B」的错位？
- [ ] 最后一页（结局）尤其要重点核验，最常出现画面与文案脱节。

**数量与命名**
- [ ] 图片数量是否与「封面 + 正文面数 + 封底」一致？
- [ ] 文件名是否按页码正确映射（page_01_cover / page_02 / ...），无错位、无遗漏？
- [ ] **排版前是否把 HTML 每页引用的图片文件名与磁盘真实文件逐一比对，任何「引用了不存在文件」的页都要补齐，杜绝「某页只有文字没有图」？**

## 八、绘本尺寸对照表

| 尺寸名称 | 实际印刷尺寸 | HTML @page / PDF 尺寸 |
|---------|-------------|---------------------|
| 方款 8 寸 | 约 203mm × 203mm | `203mm 203mm` |
| 方款 10 寸 | 约 254mm × 254mm | `254mm 254mm` |
| 横款 12 寸 | 约 305mm × 229mm | `305mm 229mm` |
| 竖款 12 寸 | 约 229mm × 305mm | `229mm 305mm` |

## 九、页数（面数）可选值

**8 / 10 / 12 / 14 / 16 / 18 / 20 / 22 / 24 / 28 / 32 / 36 / 40 / 44 / 48 / 52 / 56 / 60 / 64 / 68 / 72 面**

说明：
- 「面」= 印刷的每一页（含封面 + 封底）。正文面数 = 总面数 − 2。
- 例如「12 面」= 封面 + 10 页正文 + 封底。
- 生成插画数量 = 总面数（封面 1 张 + 正文 N 张 + 封底可用纯色/文案，不一定要生成图）。


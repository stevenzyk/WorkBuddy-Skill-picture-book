#!/usr/bin/env python3
"""
童话绘本结构化方案编译器（story_plan.json -> prompts_manifest.json / prompts_manifest.md / book.json）。

核心作用（专为跨模型稳定性设计，彻底消除弱模型手抄缩写、张冠李戴与人设漂移）：
  1. 结构与引用硬校验：核对总面数、角色 ID、造型 Look ID、场景 ID、道具/配角 ID 的完整性。
  2. 客观身份自动合成：基于用户确认的 (age, gender) 自动生成客观视觉主语（如 "the 24-year-old adult man"），
     自动展开 {c1} / {prop_id} 占位符，并拦截成年角色误用 son/daughter/boy/girl 等诱发幼童缩水的辈分词。
  3. 造型（Look）与人衣解耦：自动生成每套 Look 的「全身平地站姿基准图」Prompt（第 2 套起自动链接第 1 套基准图锁脸锁身高），
     正页按 look_id 自动切换对应服装描述与基准图，杜绝忘记换装或把鞋穿进水里。
  4. 防漏人与防漏画物体：强制核验每页在场角色均已填写独立动作，且中文文案对应的 caption_nouns_en 100% 落入编译后的英文 Prompt。
  5. 自动导出 book.json：直接衔接 scripts/build_book.py，无需二次手写。

用法：
  python scripts/compile_prompts.py --plan ./book/story_plan.json [--out-dir ./book]
"""
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from build_pdf import SIZE_PRESETS  # noqa: E402

STYLE_PREFIXES = {
    "watercolor": (
        "soft watercolor storybook illustration, gentle pastel colors, dreamy and warm atmosphere, "
        "soft edges, hand-painted texture, whimsical picture book art, high quality illustration, "
        "no photorealistic photo background"
    ),
    "cartoon": (
        "bright cheerful cartoon storybook illustration, bold clean outlines, vibrant saturated colors, "
        "cute rounded character design, playful and lively, flat color picture book style, "
        "no photorealistic photo background"
    ),
    "realistic": (
        "realistic detailed storybook illustration, soft natural lighting, rich textures, "
        "expressive realistic characters, warm cinematic atmosphere, hand-painted picture book art, "
        "no photorealistic photo background"
    ),
    "storybook": (
        "beautiful painterly storybook illustration, soft dreamy lighting, pastel and warm color palette, "
        "delicate hand-painted brushstrokes, gentle emotional mood, high quality picture book art, "
        "no photorealistic photo background"
    ),
}

ASPECT_RATIOS = {
    "square8": "1:1",
    "square10": "1:1",
    "landscape12": "3:2 (or 4:3)",
    "portrait12": "2:3 (or 3:4)",
}

# 封闭语法集合：英文家庭辈分词会强烈诱导生图模型将成年人画成幼童
KINSHIP_BIAS_WORDS = re.compile(
    r"\b(son|sons|daughter|daughters|grandson|grandsons|granddaughter|granddaughters)\b",
    re.IGNORECASE,
)
JUVENILE_WORDS = re.compile(
    r"\b(boy|boys|girl|girls|kid|kids|child|children|toddler|toddlers)\b",
    re.IGNORECASE,
)


def _build_subject_tag(char: Dict, collision_index: int = 0) -> str:
    """由确认后的客观年龄与性别生成不含辈分偏置的英文视觉主语标签。"""
    custom = (char.get("tag_prefix_en") or "").strip()
    age = int(char["age"])
    gender = char["gender"].strip().lower()
    is_female = gender in ("female", "f", "woman", "girl")

    if age <= 2:
        noun = "baby girl" if is_female else "baby boy"
    elif age <= 12:
        noun = "girl" if is_female else "boy"
    elif age <= 17:
        noun = "teenage girl" if is_female else "teenage boy"
    elif age <= 34:
        noun = "adult woman" if is_female else "adult man"
    elif age <= 59:
        noun = "woman" if is_female else "man"
    else:
        noun = "senior woman" if is_female else "senior man"

    prefix = f"{custom} " if custom else ""
    ordinal = f" (#{collision_index})" if collision_index > 0 and not custom else ""
    return f"the {prefix}{age}-year-old {noun}{ordinal}"


def _expand_placeholders(text: str, token_map: Dict[str, str]) -> str:
    if not text:
        return ""

    def repl(match):
        key = match.group(1).strip()
        return token_map.get(key, match.group(0))

    return re.sub(r"\{([a-zA-Z0-9_-]+)\}", repl, text)


def compile_plan(plan_path: Path, out_dir: Path) -> Tuple[Dict, Dict]:
    errors: List[str] = []
    warnings: List[str] = []

    if not plan_path.is_file():
        print(f"❌ 找不到 story_plan.json：{plan_path}", file=sys.stderr)
        sys.exit(1)

    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"❌ story_plan.json JSON 解析失败：{exc}", file=sys.stderr)
        sys.exit(1)

    title = (plan.get("title") or "").strip()
    subtitle = (plan.get("subtitle") or "").strip()
    if not title:
        errors.append("缺少必填字段：title")

    size = (plan.get("size") or "square8").strip()
    if size not in SIZE_PRESETS:
        errors.append(f"size '{size}' 无效，可选：{', '.join(SIZE_PRESETS)}")

    raw_style = (plan.get("style") or "watercolor").strip()
    style_prefix = STYLE_PREFIXES.get(raw_style, raw_style)
    if "children's book" in style_prefix.lower():
        warnings.append("风格前缀包含 \"children's book\"，若含成年角色建议改用 storybook illustration 以免身高缩水")

    # 1. 解析角色清单
    chars_list = plan.get("characters") or []
    if not isinstance(chars_list, list) or not chars_list:
        errors.append("characters 必须为非空数组")
        chars_list = []

    characters: Dict[str, Dict] = {}
    age_gender_counts: Dict[Tuple[int, str], int] = {}
    for ch in chars_list:
        cid = (ch.get("id") or "").strip()
        if not cid:
            errors.append("characters 中存在缺少 id 的条目")
            continue
        if cid in characters:
            errors.append(f"角色 id 重复：{cid}")
            continue
        if "age" not in ch or "gender" not in ch:
            errors.append(f"角色 {cid} 必须包含用户确认后的 age（数字）与 gender（male/female）")
            continue
        key = (int(ch["age"]), ch["gender"].strip().lower())
        age_gender_counts[key] = age_gender_counts.get(key, 0) + 1
        characters[cid] = ch

    seen_ag: Dict[Tuple[int, str], int] = {}
    subject_tags: Dict[str, str] = {}
    for cid, ch in characters.items():
        key = (int(ch["age"]), ch["gender"].strip().lower())
        if age_gender_counts[key] > 1:
            seen_ag[key] = seen_ag.get(key, 0) + 1
            subject_tags[cid] = _build_subject_tag(ch, seen_ag[key])
        else:
            subject_tags[cid] = _build_subject_tag(ch, 0)

    # 2. 解析道具与动物配角
    props: Dict[str, Dict] = plan.get("props") or {}
    sidekicks: Dict[str, Dict] = plan.get("sidekicks") or {}
    scenes: Dict[str, Dict] = plan.get("scenes") or {}
    looks: Dict[str, Dict] = plan.get("looks") or {}

    if not looks:
        errors.append("looks 不能为空，至少需定义 1 套造型（如 look_default）")
    if not scenes:
        errors.append("scenes 不能为空，至少需定义 1 个场景锚点")

    # 视觉复杂度预算温和提醒
    if len(looks) > 3:
        warnings.append(f"当前定义了 {len(looks)} 套造型（建议 ≤ 3 套，造型过多会增加换装漂移风险）")
    if len(scenes) > 5:
        warnings.append(f"当前定义了 {len(scenes)} 个场景（建议 ≤ 4–5 个核心场景以提升全书连贯度）")
    if len(props) + len(sidekicks) > 4:
        warnings.append(f"当前跨页道具+配角共 {len(props) + len(sidekicks)} 个（建议 ≤ 2–3 个核心元素）")

    # 构造全局占位符映射：{c1} -> 客观主语标签，{prop_id} -> 道具简短指代或完整锚点
    token_map: Dict[str, str] = dict(subject_tags)
    for pid, pinfo in props.items():
        token_map[pid] = (pinfo.get("short_en") or pinfo.get("anchor_en") or pid).strip()
    for sid, sinfo in sidekicks.items():
        token_map[sid] = (sinfo.get("short_en") or sinfo.get("anchor_en") or sid).strip()

    has_adult = any(int(c["age"]) >= 18 for c in characters.values())

    def check_bias_words(text: str, field_label: str, all_present_adults: bool):
        if not text:
            return
        if has_adult:
            m = KINSHIP_BIAS_WORDS.search(text)
            if m:
                errors.append(
                    f"{field_label} 中检测到家庭辈分词 '{m.group(0)}'（会诱发生图模型把成年人缩水成小孩）。"
                    f"请改用角色占位符（如 {{c1}}）或客观年龄外貌描述。"
                )
        if all_present_adults:
            m2 = JUVENILE_WORDS.search(text)
            if m2:
                errors.append(
                    f"{field_label} 全员均为成年人，禁止出现幼童词 '{m2.group(0)}'，请改用角色占位符或 adult man/woman。"
                )

    # 校验角色外观与高度描述
    char_identity_full: Dict[str, str] = {}
    for cid, ch in characters.items():
        app = _expand_placeholders((ch.get("appearance_en") or "").strip(), token_map)
        hgt = _expand_placeholders((ch.get("height_en") or "").strip(), token_map)
        if not app:
            errors.append(f"角色 {cid} 缺少 appearance_en（外貌特征）")
        if len(characters) >= 2 and not hgt:
            errors.append(f"多角色故事中，角色 {cid} 必须填写 height_en（相对身高对齐标尺，防跨页身高缩水）")
        is_adult = int(ch["age"]) >= 18
        check_bias_words(app, f"角色 {cid}.appearance_en", is_adult)
        check_bias_words(hgt, f"角色 {cid}.height_en", is_adult)

        adult_guard = ", full-grown adult stature (NOT a child)" if is_adult else ""
        hgt_clause = f", {hgt}" if hgt else ""
        char_identity_full[cid] = f"{subject_tags[cid]} with {app}{hgt_clause}{adult_guard}"

    distinctions_raw = plan.get("pairwise_distinctions_en") or []
    distinctions_expanded = [_expand_placeholders(d, token_map) for d in distinctions_raw if d.strip()]

    # 3. 编译基准图任务单（Look 站姿全身基准图 + 道具/配角基准图）
    ref_tasks: List[Dict] = []
    look_ids = list(looks.keys())
    primary_look_ref = ""

    for idx, lid in enumerate(look_ids):
        linfo = looks[lid]
        ref_img = (linfo.get("ref_image") or f"ref_{lid}.png").strip()
        linfo["ref_image"] = ref_img
        if idx == 0:
            primary_look_ref = ref_img

        outfits = linfo.get("outfits_en") or {}
        char_specs = []
        for cid in characters:
            if cid not in outfits or not outfits[cid].strip():
                errors.append(f"造型 '{lid}' 中缺少角色 {cid} 的服装描述 outfits_en.{cid}")
                continue
            outfit_str = _expand_placeholders(outfits[cid].strip(), token_map)
            check_bias_words(outfit_str, f"looks.{lid}.outfits_en.{cid}", int(characters[cid]["age"]) >= 18)
            char_specs.append(f"{char_identity_full[cid]}, {outfit_str}")

        dist_str = (" " + "; ".join(distinctions_expanded) + ".") if distinctions_expanded else ""
        ref_prompt = (
            f"{style_prefix}, character reference sheet showing {len(characters)} person(s) standing side by side "
            f"on a flat level floor in a relaxed natural full-body standing pose (head to toe including shoes/feet "
            f"fully visible, NOT sitting): {'; '.join(char_specs)}.{dist_str} "
            f"Keep recognizable facial features and exact relative height proportions, "
            f"clean plain warm cream background, no real photo background."
        )
        ref_tasks.append(
            {
                "id": lid,
                "type": "character_look_sheet",
                "label_zh": linfo.get("description_zh", lid),
                "output_image": ref_img,
                "reference_images": ["<USER_UPLOADED_PHOTO(S)>"] if idx == 0 else [primary_look_ref],
                "input_fidelity": "low",
                "aspect_ratio": ASPECT_RATIOS.get(size, "1:1"),
                "prompt": ref_prompt,
            }
        )

    for pid, pinfo in props.items():
        anchor = _expand_placeholders((pinfo.get("anchor_en") or "").strip(), token_map)
        if not anchor:
            errors.append(f"道具 '{pid}' 缺少 anchor_en")
            continue
        pref = (pinfo.get("ref_image") or "").strip()
        if pref:
            ref_tasks.append(
                {
                    "id": pid,
                    "type": "prop_sheet",
                    "label_zh": pinfo.get("label_zh", pid),
                    "output_image": pref,
                    "reference_images": [],
                    "aspect_ratio": "1:1",
                    "prompt": (
                        f"{style_prefix}, isolated reference sheet of {anchor}, "
                        f"complete object clearly visible at a 3/4 angle, clean plain warm cream background, "
                        f"no people, no clutter."
                    ),
                }
            )

    for sid, sinfo in sidekicks.items():
        anchor = _expand_placeholders((sinfo.get("anchor_en") or "").strip(), token_map)
        if not anchor:
            errors.append(f"配角 '{sid}' 缺少 anchor_en")
            continue
        sref = (sinfo.get("ref_image") or "").strip()
        if sref:
            ref_tasks.append(
                {
                    "id": sid,
                    "type": "sidekick_sheet",
                    "label_zh": sinfo.get("label_zh", sid),
                    "output_image": sref,
                    "reference_images": [],
                    "aspect_ratio": "1:1",
                    "prompt": (
                        f"{style_prefix}, isolated character reference sheet of {anchor}, "
                        f"full body clearly visible, clean plain warm cream background, no human characters."
                    ),
                }
            )

    # 4. 校验页数并编译封面 + 正文 + 可选封底
    pages_raw = plan.get("pages") or []
    total_pages = plan.get("total_pages")
    if total_pages is not None and len(pages_raw) + 2 != int(total_pages):
        errors.append(
            f"总面数不匹配：total_pages={total_pages}，但 封面(1) + pages({len(pages_raw)}) + 封底(1) = {len(pages_raw) + 2}"
        )

    def compile_single_page(spec: Dict, page_label: str, is_cover: bool = False, is_back: bool = False) -> Dict:
        img_name = (spec.get("image") or "").strip()
        if not img_name and not is_back:
            errors.append(f"{page_label} 缺少 image 文件名")

        scene_id = (spec.get("scene_id") or "").strip()
        if scene_id and scene_id not in scenes:
            errors.append(f"{page_label} 引用了未定义的 scene_id：'{scene_id}'")
        scene_anchor = _expand_placeholders(
            (scenes.get(scene_id, {}).get("anchor_en") or spec.get("scene_override_en") or "").strip(),
            token_map,
        )
        if not scene_anchor and img_name:
            errors.append(f"{page_label} 缺少有效的 scene_id 或 scene_override_en")

        present_chars: List[str] = spec.get("present_characters") or []
        present_props: List[str] = spec.get("present_props") or []
        present_sidekicks: List[str] = spec.get("present_sidekicks") or []

        for cid in present_chars:
            if cid not in characters:
                errors.append(f"{page_label} 引用了未定义的角色 ID：'{cid}'")
        for pid in present_props:
            if pid not in props:
                errors.append(f"{page_label} 引用了未定义的道具 ID：'{pid}'")
        for sid in present_sidekicks:
            if sid not in sidekicks:
                errors.append(f"{page_label} 引用了未定义的配角 ID：'{sid}'")

        all_adults_here = bool(present_chars) and all(
            int(characters[c]["age"]) >= 18 for c in present_chars if c in characters
        )

        look_id = (spec.get("look_id") or "").strip()
        char_segments: List[str] = []
        ref_imgs: List[str] = []

        if present_chars:
            if not look_id or look_id not in looks:
                errors.append(f"{page_label} 有在场人物，必须指定有效的 look_id（当前：'{look_id}'）")
            else:
                ref_imgs.append(looks[look_id]["ref_image"])

            char_actions = spec.get("character_actions") or {}
            missing_act = [c for c in present_chars if not (char_actions.get(c) or "").strip()]
            extra_act = [c for c in char_actions if c not in present_chars]
            if missing_act:
                errors.append(f"{page_label} 漏写了在场角色的独立动作 character_actions：{missing_act}（防漏人红线）")
            if extra_act:
                errors.append(f"{page_label} 的 character_actions 包含了不在 present_characters 中的角色：{extra_act}")

            for cid in present_chars:
                if cid not in characters or look_id not in looks:
                    continue
                outfit = _expand_placeholders(looks[look_id]["outfits_en"].get(cid, ""), token_map)
                act = _expand_placeholders((char_actions.get(cid) or "").strip(), token_map)
                check_bias_words(act, f"{page_label}.character_actions.{cid}", all_adults_here)
                char_segments.append(f"{char_identity_full[cid]} ({outfit}) is {act}")

            absent_chars = [subject_tags[c] for c in characters if c not in present_chars]
            if absent_chars:
                char_segments.append(
                    f"focused framing showing ONLY {', '.join(subject_tags[c] for c in present_chars)}; "
                    f"{', '.join(absent_chars)} are outside the frame and NOT visible in this scene"
                )

            if len(present_chars) >= 2:
                if distinctions_expanded:
                    char_segments.append("; ".join(distinctions_expanded))
                char_segments.append(
                    f"exactly {len(present_chars)} human characters in the scene, "
                    f"each character has exactly two arms and two hands, no extra limbs"
                )
        else:
            char_segments.append("no human characters in this scene")

        # 道具与配角片段 + 参考图（上限 3 张）
        prop_segments: List[str] = []
        prop_states = spec.get("prop_states_en") or {}
        for pid in present_props:
            if pid not in props:
                continue
            p_anchor = _expand_placeholders(props[pid]["anchor_en"], token_map)
            p_state = _expand_placeholders((prop_states.get(pid) or "").strip(), token_map)
            check_bias_words(p_state, f"{page_label}.prop_states_en.{pid}", all_adults_here)
            prop_segments.append(f"{p_anchor}" + (f" ({p_state})" if p_state else ""))
            pref = (props[pid].get("ref_image") or "").strip()
            if pref and pref not in ref_imgs and len(ref_imgs) < 3:
                ref_imgs.append(pref)

        for pid, pinfo in props.items():
            if pid not in present_props and pinfo.get("explicit_absence", True):
                short_name = (pinfo.get("short_en") or pid).strip()
                prop_segments.append(f"the {short_name} is not visible in this scene")

        sidekick_actions = spec.get("sidekick_actions") or {}
        for sid in present_sidekicks:
            if sid not in sidekicks:
                continue
            s_anchor = _expand_placeholders(sidekicks[sid]["anchor_en"], token_map)
            s_act = _expand_placeholders((sidekick_actions.get(sid) or "").strip(), token_map)
            prop_segments.append(f"{s_anchor}" + (f" is {s_act}" if s_act else ""))
            sref = (sidekicks[sid].get("ref_image") or "").strip()
            if sref and sref not in ref_imgs and len(ref_imgs) < 3:
                ref_imgs.append(sref)

        extras = _expand_placeholders((spec.get("scene_extras_en") or "").strip(), token_map)
        gaze = _expand_placeholders((spec.get("shot_and_gaze_en") or "").strip(), token_map)
        check_bias_words(extras, f"{page_label}.scene_extras_en", all_adults_here)
        check_bias_words(gaze, f"{page_label}.shot_and_gaze_en", all_adults_here)

        if is_cover:
            cover_rule = "leave clear empty space at the top of the image for the title text, main figures placed in the lower two-thirds of the frame"
            gaze = f"{gaze}, {cover_rule}" if gaze else cover_rule
        elif not is_back and present_chars and not gaze:
            gaze = "candid natural storybook moment, characters engaged in the scene action, NOT staring stiffly at the camera"

        parts = [
            style_prefix,
            f"Scene: {scene_anchor}" + (f", with {extras}" if extras else ""),
            "Characters: " + "; ".join(char_segments),
        ]
        if prop_segments:
            parts.append("Props & Companions: " + "; ".join(prop_segments))
        if gaze:
            parts.append("Composition & Gaze: " + gaze)

        compiled_prompt = ". ".join(p.rstrip(".") for p in parts if p) + "."

        # 核验中文文案核心名词是否 100% 落入编译后的英文 Prompt
        if not is_cover and not is_back:
            if "caption_nouns_en" not in spec:
                errors.append(f"{page_label} 缺少必填字段 caption_nouns_en（请列出本页中文文案对应的英文核心物体词，无具体物体填 []）")
            else:
                prompt_lower = compiled_prompt.lower()
                for noun in spec.get("caption_nouns_en") or []:
                    n_clean = noun.strip().lower()
                    if n_clean and n_clean not in prompt_lower:
                        errors.append(
                            f"{page_label} 文案核心名词 '{noun}' 未出现在该页英文描述（scene_extras_en / character_actions / props）中，请补全以防漏画！"
                        )

        return {
            "page_label": page_label,
            "output_image": img_name,
            "look_id": look_id,
            "scene_id": scene_id,
            "text_zh": (spec.get("text_zh") or "").strip(),
            "reference_images": ref_imgs,
            "input_fidelity": "low" if ref_imgs else None,
            "aspect_ratio": ASPECT_RATIOS.get(size, "1:1"),
            "prompt": compiled_prompt,
        }

    page_tasks: List[Dict] = []

    cover_spec = plan.get("cover") or {}
    if not cover_spec:
        errors.append("缺少必填字段：cover")
    else:
        page_tasks.append(compile_single_page(cover_spec, "封面 (cover)", is_cover=True))

    for idx, p_spec in enumerate(pages_raw, start=1):
        if not (p_spec.get("text_zh") or "").strip():
            errors.append(f"第 {idx} 页缺少中文文案 text_zh")
        page_tasks.append(compile_single_page(p_spec, f"正文第 {idx} 页"))

    back_spec = plan.get("back") or {}
    if (back_spec.get("image") or "").strip():
        page_tasks.append(compile_single_page(back_spec, "封底 (back)", is_back=True))

    for w in warnings:
        print(f"⚠️  提示：{w}")

    if errors:
        print("❌ story_plan.json 编译校验未通过，请修正以下问题后重试：", file=sys.stderr)
        for err in errors:
            print(f"   - {err}", file=sys.stderr)
        sys.exit(1)

    manifest = {
        "title": title,
        "subtitle": subtitle,
        "size": size,
        "aspect_ratio": ASPECT_RATIOS.get(size, "1:1"),
        "total_pages": len(pages_raw) + 2,
        "subject_tags": subject_tags,
        "reference_sheet_tasks": ref_tasks,
        "page_tasks": page_tasks,
    }

    book_data = {
        "title": title,
        "subtitle": subtitle,
        "size": size,
        "total_pages": len(pages_raw) + 2,
        "cover": {"image": cover_spec["image"]},
        "pages": [{"image": p["image"], "text": p["text_zh"]} for p in pages_raw],
        "back": {
            "image": (back_spec.get("image") or "").strip(),
            "ending": (back_spec.get("ending") or "").strip(),
        },
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_json_path = out_dir / "prompts_manifest.json"
    manifest_md_path = out_dir / "prompts_manifest.md"
    book_json_path = out_dir / "book.json"

    manifest_json_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    book_json_path.write_text(json.dumps(book_data, ensure_ascii=False, indent=2), encoding="utf-8")

    # 输出可读性极强的 Markdown 任务单，方便任意模型直接照单调用 ImageGen
    md_lines = [
        f"# 《{title}》生图执行清单（自动编译，请勿手改缩写）",
        "",
        f"- **规格**：`{size}` ｜ **推荐画幅**：`{ASPECT_RATIOS.get(size, '1:1')}` ｜ **总面数**：`{len(pages_raw) + 2}` 面",
        "- **执行铁律**：逐项原样复制下方 `Prompt` 与 `参考图` 调用 `ImageGen`；先完成「阶段 3A（全部基准图 + 封面 + 正文第 1 页）」交给用户确认，确认后再分批生成其余正页。",
        "",
        "## 一、基准图生成任务（Reference Sheets）",
        "",
    ]
    for rt in ref_tasks:
        refs_str = ", ".join(f"`{r}`" for r in rt["reference_images"]) if rt["reference_images"] else "无（纯文生图）"
        md_lines.extend(
            [
                f"### [{rt['type']}] `{rt['output_image']}` — {rt['label_zh']}",
                f"- **必传参考图**：{refs_str}（`input_fidelity: low`）",
                f"- **画幅**：`{rt['aspect_ratio']}`",
                "- **Prompt**：",
                f"  ```text\n  {rt['prompt']}\n  ```",
                "",
            ]
        )

    md_lines.extend(["## 二、绘本页面生成任务（Pages）", ""])
    for pt in page_tasks:
        refs_str = ", ".join(f"`{r}`" for r in pt["reference_images"]) if pt["reference_images"] else "无（纯文生图，勿传人物照）"
        md_lines.extend(
            [
                f"### {pt['page_label']} → `{pt['output_image']}`",
                f"- **绑定造型**：`{pt['look_id'] or '无'}` ｜ **场景**：`{pt['scene_id']}`",
                f"- **中文文案**：{pt['text_zh'] or '（封面/封底）'}",
                f"- **必传参考图**：{refs_str}",
                f"- **画幅**：`{pt['aspect_ratio']}`",
                "- **Prompt**：",
                f"  ```text\n  {pt['prompt']}\n  ```",
                "",
            ]
        )

    manifest_md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"✅ 编译通过！客观角色标签：{subject_tags}")
    print(f"✅ 已生成生图任务单：{manifest_md_path}（及 {manifest_json_path.name}）")
    print(f"✅ 已同步生成排版数据：{book_json_path}")
    return manifest, book_data


def main():
    parser = argparse.ArgumentParser(
        description="校验 story_plan.json，零丢失编译全套生图 Prompt 清单并自动导出 book.json。"
    )
    parser.add_argument("--plan", required=True, help="story_plan.json 文件路径")
    parser.add_argument("--out-dir", help="输出目录（默认与 story_plan.json 同目录）")
    args = parser.parse_args()

    plan_path = Path(args.plan).resolve()
    out_dir = Path(args.out_dir).resolve() if args.out_dir else plan_path.parent
    compile_plan(plan_path, out_dir)


if __name__ == "__main__":
    main()

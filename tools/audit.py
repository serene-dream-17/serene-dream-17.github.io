# -*- coding: utf-8 -*-
"""全站审计：结构、链接、锚点、来源覆盖、基础可访问性。"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from registry import LANGUAGES, BUILT_SLUGS  # noqa: E402
from data import sources, fw_a, fw_b, fw_c, fw_d, fw_e, depth_1, depth_2, depth_3  # noqa: E402
from data import verified, dev_scenarios, stacks  # noqa: E402

FW = {}
for _m in (fw_a, fw_b, fw_c, fw_d, fw_e):
    FW.update(_m.DETAIL)
DEEP = {}
for _m in (depth_1, depth_2, depth_3):
    DEEP.update(_m.DEEP)


def contrast(fg, bg):
    def lum(hex_color):
        h = hex_color.lstrip("#")
        rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        rgb = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
        return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
    a, b = lum(fg), lum(bg)
    hi, lo = max(a, b), min(a, b)
    return round((hi + 0.05) / (lo + 0.05), 2)


def main():
    pages = [ROOT / "index.html", ROOT / "sources.html", ROOT / "verified.html",
             ROOT / "scenarios.html", ROOT / "404.html"]
    for name in ("languages", "frameworks", "stacks"):
        pages += sorted((ROOT / name).glob("*.html"))
    failures = []
    warnings = []
    stats = {
        "pages": len(pages),
        "index_pages": 9,
        "language_pages": 0,
        "framework_pages": 0,
        "h1_ok": 0,
        "duplicate_ids": 0,
        "broken_internal": 0,
        "missing_sources": 0,
        "external_without_rel": 0,
    }

    for page in pages:
        rel = page.relative_to(ROOT).as_posix()
        s = page.read_text(encoding="utf-8")
        is_framework = page.parent.name == "frameworks" and page.name != "index.html"
        is_lang = (page.parent.name == "languages"
                   and page.name not in ("index.html", "formats.html"))

        if is_framework:
            stats["framework_pages"] += 1
        elif is_lang:
            stats["language_pages"] += 1

        if '<html lang="zh-CN">' not in s:
            failures.append(f"{rel}: 缺少 lang=zh-CN")
        if not re.search(r"<title>[^<]+</title>", s):
            failures.append(f"{rel}: 缺少 title")
        if 'name="description"' not in s:
            failures.append(f"{rel}: 缺少 meta description")
        if 'data-cmdk' not in s:
            failures.append(f"{rel}: 缺少全站搜索按钮")
        if 'property="og:title"' not in s or 'favicon.svg' not in s:
            failures.append(f"{rel}: 缺少 favicon/OG 元数据")

        h1 = len(re.findall(r"<h1\b", s))
        if h1 != 1:
            failures.append(f"{rel}: h1 数量 {h1}")
        else:
            stats["h1_ok"] += 1

        ids = re.findall(r'\bid="([^"]+)"', s)
        dup = sorted({x for x in ids if ids.count(x) > 1})
        if dup:
            stats["duplicate_ids"] += len(dup)
            failures.append(f"{rel}: 重复 id {dup[:5]}")

        for href in re.findall(r'href="([^"]*)"', s):
            if href.startswith(("http://", "https://", "mailto:", "data:", "tel:")):
                continue
            if href == "":
                failures.append(f"{rel}: 空 href")
                continue
            path, _, frag = href.partition("#")
            target = (page.parent / path).resolve() if path else page
            if not target.exists():
                stats["broken_internal"] += 1
                failures.append(f"{rel}: 链接目标不存在 {href}")
                continue
            if frag and target.suffix == ".html":
                t = target.read_text(encoding="utf-8")
                if f'id="{frag}"' not in t:
                    stats["broken_internal"] += 1
                    failures.append(f"{rel}: 锚点不存在 {href}")

        for tag in re.findall(r"<a\b[^>]*target=\"_blank\"[^>]*>", s):
            if "rel=" not in tag or "noopener" not in tag:
                stats["external_without_rel"] += 1
                failures.append(f"{rel}: target=_blank 缺少 rel=noopener")

        if is_lang:
            if 'tag--verified' not in s and 'tag--level' not in s:
                failures.append(f"{rel}: 缺少内容等级标签")
            if 'class="sources"' not in s:
                stats["missing_sources"] += 1
                failures.append(f"{rel}: 缺少参考来源")
            if sources.LAST_VERIFIED not in s:
                failures.append(f"{rel}: 缺少最后核对日期")
            if s.count('class="deep-feature"') != 4:
                failures.append(f"{rel}: 语言深读特性不是 4 项")

        if is_framework:
            if 'tag--level' not in s:
                failures.append(f"{rel}: 缺少编者判断标签")
            cards = s.count('class="fw-card"')
            srcs = s.count('class="fw-source"')
            if cards and srcs != cards:
                stats["missing_sources"] += 1
                failures.append(f"{rel}: 框架卡 {cards} 张，来源 {srcs} 条")
            if cards:
                badges = s.count('class="fw-badge"')
                if badges != cards * 3:
                    failures.append(f"{rel}: 徽章 {badges}，预期 {cards * 3}")

    # 开发场景
    sc_page = ROOT / "scenarios.html"
    if not sc_page.exists():
        failures.append("缺少 scenarios.html")
    else:
        txt = sc_page.read_text(encoding="utf-8")
        expect = sum(len(a["entries"]) for s in dev_scenarios.SCENARIOS for a in s["architectures"])
        if txt.count('class="stack-card dev-card"') != expect:
            failures.append("开发场景卡片数量与数据不一致")
        for sc in dev_scenarios.SCENARIOS:
            if f'id="dev-{sc["key"]}"' not in txt:
                failures.append(f"开发场景缺少 {sc['key']}")

    # 三级结构
    lang_idx = ROOT / "languages" / "index.html"
    if not lang_idx.exists():
        failures.append("缺少 languages/index.html")
    else:
        txt = lang_idx.read_text(encoding="utf-8")
        lang_cards = (txt.count('class="lang-card is-open"')
                      + txt.count('class="lang-card is-pending"'))
        if lang_cards != len(LANGUAGES):
            failures.append("语言总览卡片数与数据不一致")
        if 'class="pipeline"' not in txt:
            failures.append("语言总览缺少编译管线")
    fw_idx = ROOT / "frameworks" / "index.html"
    if not fw_idx.exists():
        failures.append("缺少 frameworks/index.html")
    else:
        txt = fw_idx.read_text(encoding="utf-8")
        if txt.count('class="fw-index-card"') != sum(len(d["cards"]) for d in FW.values()):
            failures.append("框架总览卡片数与数据不一致")
    stack_idx = ROOT / "stacks" / "index.html"
    if not stack_idx.exists():
        failures.append("缺少 stacks/index.html")
    else:
        txt = stack_idx.read_text(encoding="utf-8")
        if txt.count('class="stack-card stack-entry"') != len(stacks.STACKS):
            failures.append("技术栈总览卡片数与数据不一致")
    for st in stacks.STACKS:
        page = ROOT / "stacks" / f"{st['key']}.html"
        if not page.exists():
            failures.append(f"缺少技术栈页 {st['key']}")
            continue
        text = page.read_text(encoding="utf-8")
        if 'class="pick-table stack-table"' not in text:
            failures.append(f"技术栈 {st['key']} 缺少构成表")
        if text.count('class="depth-block"') != 4:
            failures.append(f"技术栈 {st['key']} 深度段不是 4 个")
        if st["source"][1] not in text:
            failures.append(f"技术栈 {st['key']} 缺少官方来源")

    fmt_page = ROOT / "languages" / "formats.html"
    if not fmt_page.exists():
        failures.append("缺少 languages/formats.html")
    else:
        txt = fmt_page.read_text(encoding="utf-8")
        if txt.count('class="stage-details"') != len(LANGUAGES):
            failures.append("产物索引阶段总表不是 78 组")
        if 'id="unclassified"' not in txt:
            failures.append("产物索引缺少未归类阶段")

    # 数据覆盖
    if len(sources.LANG) != 78:
        failures.append(f"语言来源 {len(sources.LANG)} ≠ 78")
    if len(sources.FW) != 142:
        failures.append(f"框架来源 {len(sources.FW)} ≠ 142")
    if len(DEEP) != 78:
        failures.append(f"语言深读 {len(DEEP)} ≠ 78")
    cards = [(slug, c["name"]) for slug, d in FW.items() for c in d["cards"]]
    if len(cards) != 142:
        failures.append(f"框架卡 {len(cards)} ≠ 142")
    missing = [x for x in cards if x not in sources.FW]
    if missing:
        failures.append(f"缺来源框架 {len(missing)}")
    for slug, d in FW.items():
        names = [c["name"] for c in d["cards"]]
        if len(names) != len(set(names)):
            failures.append(f"{slug}: 框架重名")
        for need, pick, _why in d["picks"]:
            if pick not in names:
                failures.append(f"{slug}: 选型推荐 {pick} 无对应卡片")
        for c in d["cards"]:
            if not (1900 <= c["year"] <= 2030):
                failures.append(f"{slug}/{c['name']}: 年份异常 {c['year']}")

    # 实测覆盖
    for slug, info in verified.VERIFIED.items():
        if slug not in BUILT_SLUGS:
            failures.append(f"实测条目不存在：{slug}")
        for field in ("tool", "command", "output", "artifacts", "date"):
            if field not in info:
                failures.append(f"实测 {slug}: 缺少 {field}")
    vpage = (ROOT / "verified.html")
    if vpage.exists():
        txt = vpage.read_text(encoding="utf-8")
        if txt.count('class="verify-card"') != len(verified.VERIFIED):
            failures.append("实测页卡片数与数据不一致")
        if 'cov-legend' not in txt:
            failures.append("实测页缺少覆盖图例")

    # 基础对比度
    checks = {
        "正文 ink/paper": contrast("#1c1a16", "#f3ede1"),
        "次要 muted/paper": contrast("#5d5547", "#f3ede1"),
        "标签 faint/paper": contrast("#6f6656", "#f3ede1"),
        "代码 code/code-bg": contrast("#e7dfcc", "#17150f"),
        "侧栏 spine-ink/spine": contrast("#d9d0bd", "#1d1b16"),
    }
    for name, ratio in checks.items():
        if ratio < 4.5:
            warnings.append(f"对比度 {name}: {ratio} < 4.5")

    print(json.dumps({
        "stats": stats,
        "sources": {"languages": len(sources.LANG), "frameworks": len(sources.FW)},
        "deep_blocks": len(DEEP),
        "framework_cards": len(cards),
        "contrast": checks,
    }, ensure_ascii=False, indent=2))
    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print(" -", w.encode("gbk", "replace").decode("gbk"))
    if failures:
        print("\nFAILURES:")
        for f in failures[:80]:
            print(" -", f)
        sys.exit(1)
    print("\nAUDIT PASS")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""框架总览页：142 张决策卡，按语言与类型筛选。"""

import html
import re

import ui
from data import fw_meta


def e(value):
    return html.escape(str(value), quote=True)


def slugify(value):
    s = re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")
    return s or "item"


def render_frameworks_index(frameworks, languages, catalog_html, batch_label):
    lang_names = {l["slug"]: l["name"] for l in languages}
    cards = []
    used_langs = []
    types = set()
    for slug in sorted(frameworks, key=lambda s: lang_names.get(s, s)):
        detail = frameworks[slug]
        used_langs.append(slug)
        for card in detail["cards"]:
            anchor = slugify(card["name"])
            m = fw_meta.META.get((slug, card["name"]), {})
            types.add(card["type"])
            search = " ".join([
                card["name"], lang_names.get(slug, slug), card["type"],
                card["tagline"], m.get("license", ""),
            ]).lower()
            cards.append(f"""<a class="fw-index-card" href="{e(slug)}.html#{e(anchor)}" data-lang="{e(slug)}" data-type="{e(card["type"])}" data-search="{e(search)}">
        <span class="fw-index-card__top"><span class="fw-index-card__lang">{e(lang_names.get(slug, slug))}</span><span class="fw-type">{e(card["type"])}</span></span>
        <span class="fw-index-card__name">{e(card["name"])}</span>
        <span class="fw-index-card__why">{e(card["tagline"])}</span>
        <span class="fw-index-card__meta">学习 {e(m.get("learn", "—"))} · 生态 {e(m.get("eco", "—"))} · 许可 {e(m.get("license", "—"))}</span>
      </a>""")

    lang_options = "".join(
        f'<option value="{e(slug)}">{e(lang_names.get(slug, slug))}</option>'
        for slug in used_langs
    )
    type_options = "".join(
        f'<option value="{e(t)}">{e(t)}</option>' for t in sorted(types)
    )
    total = len(cards)

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{ui.head_snippet()}
<title>框架总览 — {total} 张决策卡</title>
<meta name="description" content="按语言与类型浏览 {len(used_langs)} 门语言的 {total} 个框架与应用框架：适用、不适用、最小产物链与许可。">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body data-page="frameworks" data-root="../">
<a class="skip-link" href="#main">跳到正文</a>
<div class="progress" aria-hidden="true"><span></span></div>
<button class="menu-toggle" type="button" aria-label="打开目录" aria-expanded="false" aria-controls="catalog"><span></span></button>
<div class="scrim"></div>
{ui.font_ui()}
<button class="cmdk-btn" type="button" data-cmdk aria-label="全站搜索">搜索全站 <kbd>⌘K</kbd></button>
{catalog_html}
<main class="page" id="main">
  <div class="page__inner">
    <nav class="plate-nav" aria-label="框架总览导航">
      <a class="plate-nav__link" href="../index.html">← <span>首页</span></a>
      <span class="plate-nav__counter">FRAMEWORKS · {len(used_langs)} 门语言</span>
      <a class="plate-nav__link" href="../scenarios.html"><span>开发场景</span> →</a>
    </nav>
    <header class="hero">
      <p class="hero__kicker">FRAMEWORKS · 语言 → 框架 → 栈</p>
      <h1 class="hero__title">框架<br><em>总览</em></h1>
      <p class="hero__sub">同一个框架在不同语言与场景里的取舍不同。这里按语言与类型汇总全部决策卡，点进去看完整对比与来源。</p>
      <div class="hero__meta">
        <div class="stat"><span class="stat__num">{total}</span><span class="stat__label">张决策卡</span></div>
        <div class="stat"><span class="stat__num">{len(used_langs)}</span><span class="stat__label">门语言</span></div>
        <div class="stat"><span class="stat__num">{len(types)}</span><span class="stat__label">种类型</span></div>
        <div class="stat"><span class="stat__num">{len(frameworks)}</span><span class="stat__label">个框架页</span></div>
      </div>
    </header>

    <div class="index-tools matrix-tools">
      <label class="index-search" for="fwIndexSearch">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="7" cy="7" r="4.5"></circle><path d="M10.5 10.5 14 14"></path></svg>
        <input id="fwIndexSearch" type="search" placeholder="搜索框架、语言、类型或关键词（按 / 聚焦）" autocomplete="off" spellcheck="false" aria-label="搜索框架">
      </label>
      <label class="matrix-select" for="fwIndexLang">
        <span>语言</span>
        <select id="fwIndexLang"><option value="all">全部语言</option>{lang_options}</select>
      </label>
      <label class="matrix-select" for="fwIndexType">
        <span>类型</span>
        <select id="fwIndexType"><option value="all">全部类型</option>{type_options}</select>
      </label>
      <span class="era-head__count" id="fwIndexCount">{total} 张</span>
      <a class="matrix-link" href="security.html">安全工具 →</a>
    </div>

    <div class="fw-index-grid" id="fwIndexGrid">{''.join(cards)}</div>
    <p class="index-empty" id="fwIndexEmpty">没有匹配的框架。试试「Rust」「Web」「游戏」，或把筛选切回全部。</p>

    <footer class="pagefoot">
      <p class="stamp">学习 / 生态为编者判断，非官方评级；许可与事实以官方文档为准。最后核对 2026-10-30。</p>
      <p>{batch_label} · 框架总览</p>
    </footer>
  </div>
</main>
<script src="../assets/font.js"></script>
<script src="../assets/data.js"></script>
<script src="../assets/search-index.js"></script>
<script src="../assets/app.js"></script>
<script src="../assets/search.js"></script>
</body>
</html>
"""
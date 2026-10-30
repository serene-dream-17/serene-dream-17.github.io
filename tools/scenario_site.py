# -*- coding: utf-8 -*-
"""开发场景总览页：开发场景 → 架构模式 → 语言 / 框架。"""

import html
import re

from data import dev_scenarios


def e(value):
    return html.escape(str(value), quote=True)


def slugify(value):
    s = re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")
    return s or "item"


# 由 build.py 注入
ALL_LANGS = []


def _card(entry, scenario, arch, frameworks):
    slug, fw, why = entry[0], entry[1], entry[2]
    explicit = entry[3] if len(entry) > 3 else ""
    lang = next((l for l in ALL_LANGS if l["slug"] == slug), None)
    lang_name = lang["name"] if lang else slug
    if explicit:
        href = explicit
        ftype = arch["title"]
    else:
        detail = frameworks.get(slug)
        card = None
        if detail:
            card = next((c for c in detail["cards"] if c["name"] == fw), None)
        href = f"langs/{slug}-frameworks.html" + (f"#{slugify(fw)}" if card else "")
        ftype = card["type"] if card else "生态 / 工具"
    pattern = dev_scenarios.PATTERN_BY_KEY[arch["pattern"]]
    search = " ".join([
        lang_name, slug, fw, why, scenario["title"], arch["title"],
        pattern["title"], ftype,
    ]).lower()
    return f"""<a class="stack-card dev-card" href="{e(href)}" data-search="{e(search)}" data-scenario="{e(scenario["key"])}" data-arch="{e(pattern["key"])}">
        <span class="stack-top"><span class="stack-lang">{e(lang_name)}</span><span class="stack-type">{e(arch["title"])}</span></span>
        <span class="stack-fw">{e(fw)}</span>
        <span class="stack-why">{e(why)}</span>
      </a>"""


def render_scenarios(catalog_html, frameworks, batch_label):
    sections = []
    lang_count = set()
    entry_count = 0
    arch_count = 0
    for idx, scenario in enumerate(dev_scenarios.SCENARIOS, start=1):
        arch_html = []
        for arch in scenario["architectures"]:
            arch_count += 1
            cards = []
            for entry in arch["entries"]:
                lang_count.add(entry[0])
                entry_count += 1
                cards.append(_card(entry, scenario, arch, frameworks))
            pattern = dev_scenarios.PATTERN_BY_KEY[arch["pattern"]]
            arch_html.append(f"""<div class="dev-arch" data-pattern="{e(pattern["key"])}">
        <div class="dev-arch__head">
          <h3 class="dev-arch__title">{e(arch["title"])}</h3>
          <span class="dev-arch__pattern" title="{e(pattern["desc"])}">模式 · {e(pattern["title"])}</span>
          <span class="dev-arch__desc">{e(arch["desc"])}</span>
          <span class="era-head__count">{len(cards)} 组</span>
        </div>
        <div class="stack-grid">{''.join(cards)}</div>
      </div>""")
        sections.append(f"""<section class="dev-section matrix-section" id="dev-{e(scenario["key"])}" data-scenario="{e(scenario["key"])}">
      <div class="era-head">
        <span class="era-head__num">{idx:02d}</span>
        <h2 class="era-head__title">{e(scenario["title"])}</h2>
        <span class="era-head__range">{e(scenario["en"])}</span>
        <span class="era-head__count">{len(scenario["architectures"])} 种架构</span>
      </div>
      <p class="matrix-desc">{e(scenario["desc"])}</p>
      {''.join(arch_html)}
    </section>""")

    scenario_options = "".join(
        f'<option value="{e(sc["key"])}">{e(sc["title"])}</option>'
        for sc in dev_scenarios.SCENARIOS
    )
    arch_options = "".join(
        f'<option value="{e(p["key"])}">{e(p["title"])}</option>'
        for p in dev_scenarios.PATTERNS
    )
    legend = "".join(
        f"""<span class="dev-legend__item"><b>{idx:02d} {e(p["title"])}</b>{e(p["desc"])}</span>"""
        for idx, p in enumerate(dev_scenarios.PATTERNS, start=1)
    )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>
try {{
  var r = JSON.parse(localStorage.getItem("archive-reading") || "{{}}");
  var h = document.documentElement;
  if (r.font) h.dataset.font = r.font;
  if (r.size) h.dataset.size = r.size;
  if (r.line) h.dataset.line = r.line;
}} catch (e) {{}}
</script>
<title>开发场景 — 场景 × 架构 × 语言</title>
<meta name="description" content="按开发场景浏览：后端、前端、移动、桌面、游戏、数据 AI、嵌入式、系统基础设施、安全、区块链、科学计算、硬件 GPU；每个场景下按 12 种统一架构模式组合语言与框架。">
<link rel="stylesheet" href="assets/style.css">
</head>
<body data-page="scenarios">
<a class="skip-link" href="#main">跳到正文</a>
<div class="progress" aria-hidden="true"><span></span></div>
<button class="menu-toggle" type="button" aria-label="打开目录" aria-expanded="false" aria-controls="catalog"><span></span></button>
<div class="scrim"></div>
<button class="cmdk-btn" type="button" data-cmdk aria-label="全站搜索">搜索全站 <kbd>⌘K</kbd></button>
<button class="font-toggle" type="button" aria-label="阅读设置" aria-expanded="false" aria-controls="fontPanel">Aa</button>
<div class="font-panel" id="fontPanel" hidden>
  <div class="font-panel__head"><strong>阅读设置</strong>
    <button class="font-panel__close" type="button" data-font-close aria-label="关闭">×</button></div>
  <div class="font-panel__group"><span class="font-panel__label">字体</span>
    <div class="font-panel__opts">
      <button type="button" data-font="sans" aria-pressed="true">思源黑体</button>
      <button type="button" data-font="serif" aria-pressed="false">思源宋体</button>
      <button type="button" data-font="system" aria-pressed="false">系统字体</button>
    </div></div>
  <div class="font-panel__group"><span class="font-panel__label">字号</span>
    <div class="font-panel__opts">
      <button type="button" data-size="s" aria-pressed="false">小</button>
      <button type="button" data-size="m" aria-pressed="true">标准</button>
      <button type="button" data-size="l" aria-pressed="false">大</button>
      <button type="button" data-size="xl" aria-pressed="false">特大</button>
    </div></div>
  <div class="font-panel__group"><span class="font-panel__label">行距</span>
    <div class="font-panel__opts">
      <button type="button" data-line="tight" aria-pressed="false">紧凑</button>
      <button type="button" data-line="normal" aria-pressed="true">标准</button>
      <button type="button" data-line="loose" aria-pressed="false">宽松</button>
    </div></div>
  <button class="font-panel__reset" type="button" data-font-reset>恢复默认</button>
</div>
{catalog_html}
<main class="page" id="main">
  <div class="page__inner">
    <header class="hero">
      <p class="hero__kicker">DEVELOPMENT MAP · 场景 → 架构 → 语言</p>
      <h1 class="hero__title">开发<br><em>场景</em></h1>
      <p class="hero__sub">先选开发场景，再看架构模式，最后落到语言与框架。场景不是语言分类，而是「你要做什么」；同一个框架可以出现在多个场景里，但取舍不同。每个场景的架构分组都归入 12 种统一模式，便于跨场景比较。</p>
      <div class="hero__meta">
        <div class="stat"><span class="stat__num">{len(dev_scenarios.SCENARIOS)}</span><span class="stat__label">个开发场景</span></div>
        <div class="stat"><span class="stat__num">{arch_count}</span><span class="stat__label">个架构组合</span></div>
        <div class="stat"><span class="stat__num">{entry_count}</span><span class="stat__label">组推荐</span></div>
        <div class="stat"><span class="stat__num">{len(lang_count)}</span><span class="stat__label">门语言</span></div>
      </div>
    </header>

    <div class="dev-legend" aria-label="12 种统一架构模式">
      <p class="dev-legend__head">12 种统一架构模式 · 场景保留各自焦点，模式用于跨场景比较</p>
      <div class="dev-legend__grid">{legend}</div>
    </div>

    <div class="index-tools matrix-tools">
      <label class="index-search" for="devSearch">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="7" cy="7" r="4.5"></circle><path d="M10.5 10.5 14 14"></path></svg>
        <input id="devSearch" type="search" placeholder="搜索场景、架构、语言或框架（按 / 聚焦）" autocomplete="off" spellcheck="false" aria-label="搜索开发场景">
      </label>
      <label class="matrix-select" for="devScenario">
        <span>场景</span>
        <select id="devScenario"><option value="all">全部场景</option>{scenario_options}</select>
      </label>
      <label class="matrix-select" for="devArch">
        <span>架构</span>
        <select id="devArch"><option value="all">全部架构</option>{arch_options}</select>
      </label>
      <span class="era-head__count" id="devCount">{entry_count} 组</span>
    </div>

    <div class="matrix-grid" id="devSections">{''.join(sections)}</div>
    <p class="index-empty" id="devEmpty">没有匹配的组合。试试「后端」「微服务」「Rust」，或把场景切回全部。</p>

    <footer class="pagefoot">
      <p class="stamp">开发场景与架构模式为策展视角，不是官方分类；学习/生态为编者判断，许可与事实以官方文档为准。最后核对 2026-10-30。</p>
      <p>{batch_label} · 开发场景</p>
    </footer>
  </div>
</main>
<script src="assets/font.js"></script>
<script src="assets/data.js"></script>
<script src="assets/search-index.js"></script>
<script src="assets/app.js"></script>
<script src="assets/search.js"></script>
</body>
</html>
"""
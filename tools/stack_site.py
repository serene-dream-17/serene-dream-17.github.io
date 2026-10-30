# -*- coding: utf-8 -*-
"""技术栈总览与详情页。"""

import html
import re

import ui
from data import stacks


def e(value):
    return html.escape(str(value), quote=True)


def slugify(value):
    s = re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")
    return s or "item"


# 由 build.py 注入
ALL_LANGS = []
FRAMEWORKS = {}


def _domain(key):
    return next(d for d in stacks.DOMAINS if d["key"] == key)


def _resolve(item):
    """('slug', '名称') → (label, href, kind)；字符串 → 站外组件。"""
    if isinstance(item, tuple):
        slug, name = item
        detail = FRAMEWORKS.get(slug)
        card = None
        if detail:
            card = next((c for c in detail["cards"] if c["name"] == name), None)
        if card:
            return name, f"../frameworks/{slug}.html#{slugify(name)}", "框架"
        lang = next((l for l in ALL_LANGS if l["slug"] == slug), None)
        label = lang["name"] if lang and name == lang["name"] else name
        return label, f"../languages/{slug}.html", "语言"
    return str(item), "", "组件"


def _stack_summary(stack):
    parts = []
    for layer in stack["layers"]:
        for item in layer["items"]:
            if isinstance(item, tuple):
                parts.append(item[1])
    return " · ".join(dict.fromkeys(parts[:3]))


def render_stacks_index(catalog_html, batch_label):
    total = len(stacks.STACKS)
    domains = []
    for domain in stacks.DOMAINS:
        items = [s for s in stacks.STACKS if s["domain"] == domain["key"]]
        if not items:
            continue
        cards = []
        for st in items:
            search = " ".join([
                st["title"], st["summary"], domain["title"], _stack_summary(st),
                " ".join(st["fit"]),
            ]).lower()
            cards.append(f"""<a class="stack-card stack-entry" href="{e(st["key"])}.html" data-search="{e(search)}" data-domain="{e(domain["key"])}">
        <span class="stack-top"><span class="stack-lang">{e(domain["title"])}</span><span class="stack-type">技术栈</span></span>
        <span class="stack-fw">{e(st["title"])}</span>
        <span class="stack-why">{e(st["summary"])}</span>
        <span class="stack-meta">{e(_stack_summary(st))}</span>
      </a>""")
        domains.append(f"""<section class="dev-section matrix-section" id="domain-{e(domain["key"])}" data-domain="{e(domain["key"])}">
      <div class="era-head">
        <h2 class="era-head__title">{e(domain["title"])}</h2>
        <span class="era-head__range">{len(items)} 个栈</span>
        <span class="era-head__count">{e(domain["desc"])}</span>
      </div>
      <div class="stack-grid">{''.join(cards)}</div>
    </section>""")

    options = "".join(
        f'<option value="{e(d["key"])}">{e(d["title"])}</option>'
        for d in stacks.DOMAINS if any(s["domain"] == d["key"] for s in stacks.STACKS)
    )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{ui.head_snippet()}
<title>技术栈 — 语言 × 框架 × 基础设施</title>
<meta name="description" content="按组合浏览技术栈：语言、框架、数据与部署的推荐搭配，覆盖 Web、移动、桌面、游戏、数据、AI、嵌入式、安全、区块链与科学计算。">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body data-page="stacks" data-root="../">
<a class="skip-link" href="#main">跳到正文</a>
<div class="progress" aria-hidden="true"><span></span></div>
<button class="menu-toggle" type="button" aria-label="打开目录" aria-expanded="false" aria-controls="catalog"><span></span></button>
<div class="scrim"></div>
{ui.font_ui()}
<button class="cmdk-btn" type="button" data-cmdk aria-label="全站搜索">搜索全站 <kbd>⌘K</kbd></button>
{catalog_html}
<main class="page" id="main">
  <div class="page__inner">
    <nav class="plate-nav" aria-label="技术栈导航">
      <a class="plate-nav__link" href="../index.html">← <span>首页</span></a>
      <span class="plate-nav__counter">STACKS · {total}</span>
      <a class="plate-nav__link" href="../languages/index.html"><span>编程语言</span> →</a>
    </nav>
    <header class="hero">
      <p class="hero__kicker">TECH STACKS · 语言 → 框架 → 落地</p>
      <h1 class="hero__title">技术<br><em>栈</em></h1>
      <p class="hero__sub">栈是「能直接开工的组合」：语言、框架、数据库、运行环境与交付方式。同一个框架可以出现在不同栈里，取舍写在每一页。</p>
      <div class="hero__meta">
        <div class="stat"><span class="stat__num">{total}</span><span class="stat__label">个技术栈</span></div>
        <div class="stat"><span class="stat__num">{len({s["domain"] for s in stacks.STACKS})}</span><span class="stat__label">个领域</span></div>
        <div class="stat"><span class="stat__num">{len({i[0] for s in stacks.STACKS for l in s["layers"] for i in l["items"] if isinstance(i, tuple)})}</span><span class="stat__label">门语言</span></div>
        <div class="stat"><span class="stat__num">{len(FRAMEWORKS)}</span><span class="stat__label">个框架页</span></div>
      </div>
    </header>

    <div class="index-tools matrix-tools">
      <label class="index-search" for="stackSearch">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="7" cy="7" r="4.5"></circle><path d="M10.5 10.5 14 14"></path></svg>
        <input id="stackSearch" type="search" placeholder="搜索栈、语言、框架或领域（按 / 聚焦）" autocomplete="off" spellcheck="false" aria-label="搜索技术栈">
      </label>
      <label class="matrix-select" for="stackDomain">
        <span>领域</span>
        <select id="stackDomain"><option value="all">全部领域</option>{options}</select>
      </label>
      <span class="era-head__count" id="stackCount">{total} 个栈</span>
    </div>

    <div class="matrix-grid" id="stackSections">{''.join(domains)}</div>
    <p class="index-empty" id="stackEmpty">没有匹配的技术栈。试试「Web」「Rust」「数据」，或把领域切回全部。</p>

    <footer class="pagefoot">
      <p class="stamp">技术栈是策展组合，不是官方认证；组件版本与许可以官方文档为准。最后核对 2026-10-30。</p>
      <p>{batch_label} · 技术栈</p>
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


def render_stack(stack, catalog_html, batch_label):
    domain = _domain(stack["domain"])
    rows = []
    for layer in stack["layers"]:
        cells = []
        for item in layer["items"]:
            label, href, kind = _resolve(item)
            if href:
                cells.append(
                    f'<a class="stack-comp" href="{e(href)}">{e(label)}<span>{e(kind)}</span></a>'
                )
            else:
                cells.append(f'<span class="stack-comp is-plain">{e(label)}<span>组件</span></span>')
        rows.append(
            f"<tr><th scope=\"row\">{e(layer['role'])}</th><td>{''.join(cells)}</td></tr>"
        )

    fit = "".join(f"<li>{e(x)}</li>" for x in stack["fit"])
    avoid = "".join(f"<li>{e(x)}</li>" for x in stack["avoid"])
    layout = "".join(f"<li><code>{e(x)}</code></li>" for x in stack["layout"])
    by_key = {s["key"]: s for s in stacks.STACKS}
    alts = "".join(
        f'<a class="stack-card stack-entry" href="{e(key)}.html">'
        f'<span class="stack-top"><span class="stack-lang">{e(_domain(by_key[key]["domain"])["title"])}</span>'
        f'<span class="stack-type">技术栈</span></span>'
        f'<span class="stack-fw">{e(by_key[key]["title"])}</span>'
        f'<span class="stack-why">{e(by_key[key]["summary"])}</span></a>'
        for key in stack["alternatives"] if key in by_key
    )
    def _depth_list(items):
        return "".join(f"<li>{e(x)}</li>" for x in items)

    depth_blocks = "".join(
        f'<article class="depth-block"><h3 class="depth-block__title">{title}<em>{en}</em></h3>'
        f'<ul class="fw-list">{_depth_list(stack[items_attr])}</ul></article>'
        for title, en, items_attr in (
            ("版本基线", "Baseline", "baseline"),
            ("测试与 CI", "Testing", "testing"),
            ("部署与运维", "Operations", "ops"),
            ("团队与成本", "Team", "team"),
            ("数据与请求链路", "Flow", "chain"),
            ("性能与容量", "Capacity", "perf"),
            ("可观测性与 SLO", "Observability", "observe"),
            ("安全与合规", "Security", "secure"),
        )
    )
    sec_link = ('<a class="matrix-link" href="../frameworks/security.html">安全工具 →</a>'
                if stack["domain"] == "security" else "")
    src_title, src_url = stack["source"]

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{ui.head_snippet()}
<title>{e(stack["title"])} — 技术栈</title>
<meta name="description" content="{e(stack["title"])}：{e(stack["summary"])}">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body data-page="stack" data-root="../">
<a class="skip-link" href="#main">跳到正文</a>
<div class="progress" aria-hidden="true"><span></span></div>
<button class="menu-toggle" type="button" aria-label="打开目录" aria-expanded="false" aria-controls="catalog"><span></span></button>
<div class="scrim"></div>
{ui.font_ui()}
<button class="cmdk-btn" type="button" data-cmdk aria-label="全站搜索">搜索全站 <kbd>⌘K</kbd></button>
{catalog_html}
<main class="page" id="main">
  <div class="page__inner">
    <nav class="plate-nav" aria-label="技术栈导航">
      <a class="plate-nav__link" href="index.html">← <span>技术栈总览</span></a>
      <span class="plate-nav__counter">STACK · {e(domain["title"])}</span>
      <a class="plate-nav__link" href="../index.html"><span>首页</span> →</a>
    </nav>
    <header class="dossier fw-dossier">
      <div class="dossier__eyebrow">
        <span>TECH STACK</span><span class="dot"></span>
        <span class="era">{e(domain["title"])}</span><span class="dot"></span>
        <span>组合栈</span>
      </div>
      <h1 class="dossier__name">{e(stack["title"])}<span class="cn">技术栈</span></h1>
      <p class="dossier__tagline">{e(stack["summary"])}</p>
      <div class="dossier__meta">
        <div class="meta-item"><span class="meta-label">领域</span><span class="meta-value">{e(domain["title"])}</span></div>
        <div class="meta-item"><span class="meta-label">构成</span><span class="meta-value">{e(_stack_summary(stack))}</span></div>
        <div class="meta-item"><span class="meta-label">来源</span><span class="meta-value"><a href="{e(src_url)}" target="_blank" rel="noopener noreferrer">{e(src_title)}</a></span></div>
      </div>
    </header>

    <section class="block reveal" id="layers">
      <div class="block__head"><span class="block__num">01</span><h2 class="block__title">栈的构成<em>Layers</em></h2><span class="block__rule"></span></div>
      <div class="table-wrap">
        <table class="pick-table stack-table">
          <caption>层 → 组件 → 站内链接</caption>
          <thead><tr><th scope="col">层</th><th scope="col">组件</th></tr></thead>
          <tbody>{''.join(rows)}</tbody>
        </table>
      </div>
      <p class="table-hint">表格可横向滑动 →</p>
    </section>

    <section class="block reveal" id="fit">
      <div class="block__head"><span class="block__num">02</span><h2 class="block__title">适用与规避<em>Tradeoffs</em></h2><span class="block__rule"></span></div>
      <div class="fw-cols">
        <div><h4 class="fw-label">适用</h4><ul class="fw-list">{fit}</ul></div>
        <div><h4 class="fw-label">不适用</h4><ul class="fw-list fw-list--avoid">{avoid}</ul></div>
      </div>
    </section>

    <section class="block reveal" id="layout">
      <div class="block__head"><span class="block__num">03</span><h2 class="block__title">落地结构<em>Layout</em></h2><span class="block__rule"></span></div>
      <p class="prose">目录结构是示意，不是强制约定；按团队与构建工具调整。</p>
      <ul class="stack-layout">{layout}</ul>
      <div class="stack-links"><a class="matrix-link" href="../frameworks/index.html">框架总览 →</a>{sec_link}<a class="matrix-link matrix-link--ghost" href="../scenarios.html">开发场景 →</a></div>
    </section>

    <section class="block reveal" id="alternatives">
      <div class="block__head"><span class="block__num">04</span><h2 class="block__title">替代栈<em>Alternatives</em></h2><span class="block__rule"></span></div>
      <div class="stack-grid">{alts}</div>
    </section>

    <section class="block reveal" id="depth">
      <div class="block__head"><span class="block__num">05</span><h2 class="block__title">工程化深度<em>Engineering</em></h2><span class="block__rule"></span></div>
      <p class="prose">版本是策展建议线（LTS 或当前稳定线）；链路、容量与 SLO 为示意口径，具体数值需按实测与官方文档校准。</p>
      <div class="stack-depth">{depth_blocks}</div>
    </section>

    <footer class="pagefoot">
      <p class="stamp">技术栈为策展组合；组件版本、许可与默认配置以官方文档为准。</p>
      <p>{batch_label} · 技术栈 · {e(stack["title"])}</p>
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
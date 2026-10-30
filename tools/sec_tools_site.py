# -*- coding: utf-8 -*-
"""安全工具页（位于 frameworks/ 下）：渗透、网络、逆向、漏洞挖掘等。"""

import html

import ui
from data import sec_tools


def e(value):
    return html.escape(str(value), quote=True)


def _card(tool):
    search = " ".join([
        tool["name"], sec_tools.CAT_BY_KEY[tool["cat"]]["title"],
        tool["summary"], tool["license"], " ".join(tool["fit"]),
    ]).lower()
    fit = " · ".join(e(x) for x in tool["fit"])
    src_title, src_url = tool["source"]
    return f"""<article class="stack-card sec-tool-card" id="{e(tool["slug"])}" data-cat="{e(tool["cat"])}" data-search="{e(search)}">
        <span class="stack-top"><span class="stack-lang">{e(sec_tools.CAT_BY_KEY[tool["cat"]]["title"])}</span><span class="stack-type">{e(tool["license"])}</span></span>
        <span class="stack-fw">{e(tool["name"])}</span>
        <span class="stack-why">{e(tool["summary"])}</span>
        <span class="stack-meta">{fit}</span>
        <span class="sec-tool__meta"><a href="{e(src_url)}" target="_blank" rel="noopener noreferrer">{e(src_title)}</a></span>
      </article>"""


def render_security_tools(catalog_html, batch_label):
    sections = []
    for cat in sec_tools.CATEGORIES:
        items = sec_tools.BY_CAT.get(cat["key"], [])
        if not items:
            continue
        sections.append(f"""<section class="dev-section matrix-section" id="cat-{e(cat["key"])}" data-cat="{e(cat["key"])}">
      <div class="era-head">
        <h2 class="era-head__title">{e(cat["title"])}</h2>
        <span class="era-head__range">{len(items)} 个工具</span>
        <span class="era-head__count">{e(cat["desc"])}</span>
      </div>
      <div class="stack-grid">{''.join(_card(t) for t in items)}</div>
    </section>""")

    options = "".join(
        f'<option value="{e(c["key"])}">{e(c["title"])}</option>'
        for c in sec_tools.CATEGORIES if c["key"] in sec_tools.BY_CAT
    )
    total = len(sec_tools.TOOLS)

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{ui.head_snippet()}
<title>安全工具 — 渗透 / 网络 / 逆向 / 漏洞挖掘</title>
<meta name="description" content="安全工具索引：渗透测试、网络与流量、逆向与二进制、漏洞挖掘、移动与固件、应急与情报，共 {total} 个工具。仅限授权测试。">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body data-page="sectools" data-root="../">
<a class="skip-link" href="#main">跳到正文</a>
<div class="progress" aria-hidden="true"><span></span></div>
<button class="menu-toggle" type="button" aria-label="打开目录" aria-expanded="false" aria-controls="catalog"><span></span></button>
<div class="scrim"></div>
{ui.font_ui()}
<button class="cmdk-btn" type="button" data-cmdk aria-label="全站搜索">搜索全站 <kbd>⌘K</kbd></button>
{catalog_html}
<main class="page" id="main">
  <div class="page__inner">
    <nav class="plate-nav" aria-label="安全工具导航">
      <a class="plate-nav__link" href="index.html">← <span>框架总览</span></a>
      <span class="plate-nav__counter">SECURITY TOOLS · {total}</span>
      <a class="plate-nav__link" href="../stacks/index.html"><span>技术栈</span> →</a>
    </nav>
    <header class="hero">
      <p class="hero__kicker">SECURITY TOOLS · 攻防与验证</p>
      <h1 class="hero__title">安全<br><em>工具</em></h1>
      <p class="hero__sub">渗透、流量、逆向、漏洞挖掘、移动固件与应急情报。工具只是执行面，范围与授权先行：仅用于自有资产或取得书面授权的目标。</p>
      <div class="hero__meta">
        <div class="stat"><span class="stat__num">{total}</span><span class="stat__label">个工具</span></div>
        <div class="stat"><span class="stat__num">{len(sec_tools.CATEGORIES)}</span><span class="stat__label">个类别</span></div>
        <div class="stat"><span class="stat__num">{len(sec_tools.BY_CAT.get("pentest", []))}</span><span class="stat__label">个渗透工具</span></div>
        <div class="stat"><span class="stat__num">{len(sec_tools.BY_CAT.get("vuln", []))}</span><span class="stat__label">个漏洞挖掘工具</span></div>
      </div>
    </header>

    <p class="sec-auth-note">授权提示：渗透、扫描、逆向与无线类工具仅可用于自有资产或书面授权目标；不提供具体利用步骤。</p>

    <div class="index-tools matrix-tools">
      <label class="index-search" for="secToolSearch">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="7" cy="7" r="4.5"></circle><path d="M10.5 10.5 14 14"></path></svg>
        <input id="secToolSearch" type="search" placeholder="搜索工具、类别或用途（按 / 聚焦）" autocomplete="off" spellcheck="false" aria-label="搜索安全工具">
      </label>
      <label class="matrix-select" for="secToolCat">
        <span>类别</span>
        <select id="secToolCat"><option value="all">全部类别</option>{options}</select>
      </label>
      <span class="era-head__count" id="secToolCount">{total} 个工具</span>
    </div>

    <div class="matrix-grid" id="secToolSections">{''.join(sections)}</div>
    <p class="index-empty" id="secToolEmpty">没有匹配的工具。试试「Burp」「逆向」「流量」，或把类别切回全部。</p>

    <footer class="pagefoot">
      <p class="stamp">安全工具为策展索引；许可、版本与用法以官方文档为准。攻防类工具仅限自有资产或书面授权测试。</p>
      <p>{batch_label} · 安全工具</p>
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
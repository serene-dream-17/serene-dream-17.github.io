# -*- coding: utf-8 -*-
"""来源索引页渲染。"""

import html
import re

from data import sources, fw_a, fw_b, fw_c, fw_d, fw_e

FW = {}
for _m in (fw_a, fw_b, fw_c, fw_d, fw_e):
    FW.update(_m.DETAIL)


def e(value):
    return html.escape(str(value), quote=True)


def render_sources_index(langs, catalog_html, batch_label):
    total = len(sources.LANG) + len(sources.FW)
    groups = []
    for lang in langs:
        slug = lang["slug"]
        rows = []
        src = sources.LANG.get(slug)
        if src:
            hay = f"{lang['name']} {lang['cn']} {src[0]} 语言".lower()
            rows.append(
                f'<li data-search="{e(hay)}"><span class="src-kind">语言</span>'
                f'<a href="{e(src[1])}" target="_blank" rel="noopener noreferrer">{e(src[0])} ↗</a>'
                f'<a class="src-page" href="langs/{slug}.html#sources">查看页面</a></li>'
            )
        detail = FW.get(slug)
        if detail:
            for card in detail["cards"]:
                item = sources.FW.get((slug, card["name"]))
                if not item:
                    continue
                anchor = re.sub(r"[^a-z0-9]+", "-", card["name"].lower()).strip("-")
                hay = f"{lang['name']} {lang['cn']} {card['name']} {item[0]} 框架".lower()
                rows.append(
                    f'<li data-search="{e(hay)}"><span class="src-kind">框架</span>'
                    f'<a href="{e(item[1])}" target="_blank" rel="noopener noreferrer">{e(item[0])} ↗</a>'
                    f'<a class="src-page" href="langs/{slug}-frameworks.html#{anchor}">{e(card["name"])} 决策卡</a></li>'
                )
        if not rows:
            continue
        groups.append(
            f'<section class="src-group" data-search="{e((lang["name"] + " " + lang["cn"] + " " + slug).lower())}">'
            f'<h2 class="src-group__title">{lang["plate"]:02d} · {e(lang["name"])}'
            f'<span>{e(lang["cn"])}</span></h2>'
            f'<ul class="src-list">{"".join(rows)}</ul></section>'
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
<title>来源索引 — {total} 条官方来源</title>
<meta name="description" content="全站 {total} 条参考来源索引：按语言与框架列出官方文档、规范与页面链接，供逐条核对。">
<link rel="stylesheet" href="assets/style.css">
</head>
<body data-page="sources">
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
    <header class="hero src-hero">
      <p class="hero__kicker">REFERENCES · 来源索引</p>
      <h1 class="hero__title">引用<br><em>索引</em></h1>
      <p class="hero__sub">全站 {total} 条参考来源：{len(sources.LANG)} 条语言、{len(sources.FW)} 条框架。每条都指向官方文档或规范，并可跳回对应页面。</p>
      <div class="hero__meta">
        <div class="stat"><span class="stat__num">{total}</span><span class="stat__label">条来源</span></div>
        <div class="stat"><span class="stat__num">{len(sources.LANG)}</span><span class="stat__label">语言</span></div>
        <div class="stat"><span class="stat__num">{len(sources.FW)}</span><span class="stat__label">框架</span></div>
        <div class="stat"><span class="stat__num">{sources.LAST_VERIFIED}</span><span class="stat__label">最后核对</span></div>
      </div>
    </header>
    <div class="index-tools">
      <label class="index-search" for="srcSearch">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="7" cy="7" r="4.5"></circle><path d="M10.5 10.5 14 14"></path></svg>
        <input id="srcSearch" type="search" placeholder="搜索语言、框架或来源（按 / 聚焦）" autocomplete="off" spellcheck="false" aria-label="搜索来源">
      </label>
      <span class="era-head__count" id="srcCount">{total} 条</span>
    </div>
    <div class="src-groups">{"".join(groups)}</div>
    <p class="index-empty" id="srcEmpty">没有匹配的来源。</p>
    <footer class="pagefoot">
      <p class="stamp">来源用于指向权威资料，不代表对每条断言做了逐句引用。许可以与事实请以官方文档为准；内容口径见 AUDIT.md。</p>
      <p>{batch_label} · 来源索引</p>
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

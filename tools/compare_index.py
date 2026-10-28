# -*- coding: utf-8 -*-
"""跨语言 / 跨框架对比器页面。"""

import html


def e(value):
    return html.escape(str(value), quote=True)


def render_compare(catalog_html, batch_label, batch_no, lang_count, fw_count):
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
<title>对比器 — 语言与框架并排</title>
<meta name="description" content="并排对比 2–3 门语言或 2–3 个框架：类型、内存、并发、里程碑、学习曲线、生态、许可与最小产物链。">
<link rel="stylesheet" href="assets/style.css">
</head>
<body data-page="compare">
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
      <p class="hero__kicker">COMPARE · 并排阅读</p>
      <h1 class="hero__title">对比<br><em>器</em></h1>
      <p class="hero__sub">选 2–3 门语言或 2–3 个框架，并排看类型、内存、并发、里程碑、学习曲线、生态、许可与最小产物链。</p>
      <div class="hero__meta">
        <div class="stat"><span class="stat__num">{lang_count}</span><span class="stat__label">门语言</span></div>
        <div class="stat"><span class="stat__num">{fw_count}</span><span class="stat__label">个框架</span></div>
        <div class="stat"><span class="stat__num">3</span><span class="stat__label">最多并排</span></div>
        <div class="stat"><span class="stat__num">{batch_no}</span><span class="stat__label">当前批次</span></div>
      </div>
    </header>

    <div class="cmp-controls">
      <div class="cmp-modes" role="group" aria-label="对比类型">
        <button class="filter" type="button" data-cmp-mode="language" aria-pressed="true">语言</button>
        <button class="filter" type="button" data-cmp-mode="framework" aria-pressed="false">框架</button>
      </div>
      <div class="cmp-presets" role="group" aria-label="快速对比预设">
        <span class="cmp-presets__label">快速对比</span>
        <button type="button" data-preset="web">Web 后端</button>
        <button type="button" data-preset="frontend">Web 前端</button>
        <button type="button" data-preset="mobile">移动</button>
        <button type="button" data-preset="data">数据 / AI</button>
        <button type="button" data-preset="systems">系统语言</button>
        <button type="button" data-preset="science">科学计算</button>
      </div>
      <div class="cmp-selects">
        <label>对比项 1<select id="cmp1" aria-label="对比项 1"></select></label>
        <label>对比项 2<select id="cmp2" aria-label="对比项 2"></select></label>
        <label>对比项 3（可选）<select id="cmp3" aria-label="对比项 3"></select></label>
      </div>
      <span class="era-head__count" id="cmpCount"></span>
    </div>

    <div class="cmp-table-wrap" id="cmpTableWrap"></div>

    <p class="cmp-note">学习曲线 / 生态成熟度为编者判断；许可、年份与产物链以各页来源为准。语言对比使用「语言深读」数据，框架对比使用决策卡与元信息。</p>

    <footer class="pagefoot">
      <p class="stamp">对比基于站内结构化数据；字段缺失显示为「—」。最后核对 2026-10-28。</p>
      <p>{batch_label} · 对比器</p>
    </footer>
  </div>
</main>
<script src="assets/font.js"></script>
<script src="assets/data.js"></script>
<script src="assets/search-index.js"></script>
<script src="assets/compare-data.js"></script>
<script src="assets/app.js"></script>
<script src="assets/search.js"></script>
<script src="assets/compare.js"></script>
</body>
</html>
"""

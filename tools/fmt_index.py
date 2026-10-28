# -*- coding: utf-8 -*-
"""产物格式索引页。"""

import html

import formats


def e(value):
    return html.escape(str(value), quote=True)


def render_formats(data, langs_by_slug, catalog_html, batch_label, batch_no, total_langs):
    index = formats.build(data)
    total = len(index)
    sections = []
    for key, title, desc in formats.GROUPS:
        items = [f for f in index if f["group"] == key]
        if not items:
            continue
        cards = []
        for f in items:
            chips = []
            for slug, no, stage_label, _file in f["hits"][:10]:
                href = (f"langs/{slug}.html#stage-{no}" if no else f"langs/{slug}.html")
                chips.append(
                    f'<a class="fmt-chip" href="{href}">'
                    f'<b>{e(langs_by_slug[slug]["name"])}</b>'
                    f'<span>{e(stage_label)}</span></a>'
                )
            chips = "".join(chips)
            more = ""
            if len(f["hits"]) > 10:
                more = f'<span class="fmt-more">+{len(f["hits"]) - 10}</span>'
            cards.append(f"""<article class="fmt-card" id="{e(f["key"])}" data-search="{e((f['name'] + ' ' + f['desc'] + ' ' + ' '.join(f['langs'])).lower())}">
        <header class="fmt-head">
          <h3 class="fmt-name">{e(f["name"])}</h3>
          <span class="fmt-count">{len(f["langs"])} 门语言</span>
        </header>
        <p class="fmt-desc">{e(f["desc"])}</p>
        <div class="fmt-chips">{chips}{more}</div>
      </article>""")
        sections.append(f"""<section class="fmt-section" data-group="{key}">
      <div class="era-head">
        <span class="era-head__num">{formats.GROUPS.index((key, title, desc)) + 1:02d}</span>
        <h2 class="era-head__title">{e(title)}</h2>
        <span class="era-head__range">{e(desc)}</span>
        <span class="era-head__count">{len(items)} 种格式</span>
      </div>
      <div class="fmt-grid">{"".join(cards)}</div>
    </section>""")

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
<title>产物格式索引 — {total} 种格式的反向索引</title>
<meta name="description" content="按产物格式反查语言与阶段：ELF、PE、Mach-O、.class、.beam、wasm、LLVM IR、SPIR-V、EVM 字节码、PTX 等。">
<link rel="stylesheet" href="assets/style.css">
</head>
<body data-page="formats">
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
      <p class="hero__kicker">ARTIFACT INDEX · 格式 → 语言 → 阶段</p>
      <h1 class="hero__title">产物<br><em>索引</em></h1>
      <p class="hero__sub">按产物反查：哪些语言、在哪个阶段，产生了这种格式。点任意语言标签，直接跳到对应的阶段卡。</p>
      <div class="hero__meta">
        <div class="stat"><span class="stat__num">{total}</span><span class="stat__label">种格式</span></div>
        <div class="stat"><span class="stat__num">{len(formats.GROUPS)}</span><span class="stat__label">个分组</span></div>
        <div class="stat"><span class="stat__num">{total_langs}</span><span class="stat__label">门语言</span></div>
        <div class="stat"><span class="stat__num">{batch_no}</span><span class="stat__label">当前批次</span></div>
      </div>
    </header>

    <div class="index-tools">
      <label class="index-search" for="fmtSearch">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="7" cy="7" r="4.5"></circle><path d="M10.5 10.5 14 14"></path></svg>
        <input id="fmtSearch" type="search" placeholder="搜索格式、说明或语言（按 / 聚焦）" autocomplete="off" spellcheck="false" aria-label="搜索产物格式">
      </label>
      <span class="era-head__count" id="fmtCount">{total} 种</span>
    </div>

    {"".join(sections)}
    <p class="index-empty" id="fmtEmpty">没有匹配的格式。试试「ELF」「class」「GPU」。</p>

    <footer class="pagefoot">
      <p class="stamp">格式与语言的对应关系基于本档案的阶段样例与策展；同一种格式可能还有其它产生者，此处只收录站内条目。</p>
      <p>{batch_label} · 产物格式索引</p>
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

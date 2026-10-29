# -*- coding: utf-8 -*-
"""安全专题页渲染。"""

import html

from data import security


def e(value):
    return html.escape(str(value), quote=True)


def _topic_points(topic):
    if not topic["points"]:
        return ""
    lis = "".join(f"<li>{e(p)}</li>" for p in topic["points"])
    return f'<ul class="sec-points">{lis}</ul>'


def _by_language_table():
    rows = []
    for lang in sorted(security.BY_LANG, key=lambda x: x.lower()):
        tools = security.BY_LANG[lang]
        names = "、".join(
            f'<a href="#{e(t["slug"])}">{e(t["name"])}</a>' for t in tools
        )
        cats = "、".join(e(t["category"]) for t in tools)
        rows.append(
            f"<tr><td>{e(lang)}</td><td>{names}</td><td>{cats}</td></tr>"
        )
    return "".join(rows)


def _tool_cards():
    cards = []
    for tool in security.TOOLS:
        search = " ".join([
            tool["name"], tool["lang"], tool["category"], tool["summary"],
            tool["license"], " ".join(tool["fit"]),
        ]).lower()
        cards.append(f"""<article class="stack-card sec-tool" id="{e(tool["slug"])}" data-search="{e(search)}" data-cat="{e(tool["category"])}">
        <span class="stack-top"><span class="stack-lang">{e(tool["lang"])}</span><span class="stack-type">{e(tool["category"])}</span></span>
        <span class="stack-fw">{e(tool["name"])}</span>
        <span class="stack-why">{e(tool["summary"])}</span>
        <span class="sec-tool__meta">许可 {e(tool["license"])} · {' → '.join(e(x) for x in tool["chain"])}</span>
      </article>""")
    return "".join(cards)


def _sources_list():
    items = []
    for tool in security.TOOLS:
        title, url = tool["source"]
        items.append(
            f'<li><a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(title)}</a>'
            f'<span>{e(tool["name"])}</span></li>'
        )
    return "".join(items)


def render_security(catalog_html, batch_label):
    topics = []
    for idx, topic in enumerate(security.TOPICS, start=1):
        if topic["key"] == "by-language":
            extra = f"""<div class="table-wrap">
      <table class="pick-table">
        <caption>语言 → 安全工具 → 类别</caption>
        <thead><tr><th scope="col">语言</th><th scope="col">工具</th><th scope="col">类别</th></tr></thead>
        <tbody>{_by_language_table()}</tbody>
      </table>
    </div>
    <p class="table-hint">表格可横向滑动 →</p>"""
        else:
            extra = _topic_points(topic)
        topics.append(f"""<section class="block reveal" id="{e(topic["key"])}">
      <div class="block__head">
        <span class="block__num">{idx:02d}</span>
        <h2 class="block__title">{e(topic["title"])}<em>{e(topic["en"])}</em></h2>
        <span class="block__rule"></span>
      </div>
      <p class="prose">{e(topic["desc"])}</p>
      {extra}
    </section>""")

    categories = sorted({t["category"] for t in security.TOOLS})
    options = "".join(
        f'<option value="{e(c)}">{e(c)}</option>' for c in categories
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
<title>安全专题 — 从编码到审计</title>
<meta name="description" content="应用安全、安全编码、密码学、身份与访问、供应链、安全测试、审计合规，以及按语言的安全工具选型。">
<link rel="stylesheet" href="assets/style.css">
</head>
<body data-page="security">
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
    <header class="hero" id="security">
      <p class="hero__kicker">SECURITY · 从编码到审计</p>
      <h1 class="hero__title">安全<br><em>专题</em></h1>
      <p class="hero__sub">安全不是上线前的一道扫描，而是从输入边界、密钥管理、依赖供应链到审计日志的一整条链。这里按主题整理原则、工具与按语言的选型。</p>
      <div class="hero__meta">
        <div class="stat"><span class="stat__num">{len(security.TOPICS)}</span><span class="stat__label">个主题</span></div>
        <div class="stat"><span class="stat__num">{len(security.TOOLS)}</span><span class="stat__label">个工具</span></div>
        <div class="stat"><span class="stat__num">{len(security.BY_LANG)}</span><span class="stat__label">门语言</span></div>
        <div class="stat"><span class="stat__num">{len(security.TOOLS)}</span><span class="stat__label">条官方来源</span></div>
      </div>
    </header>

    {"".join(topics)}

    <section class="block reveal" id="tools">
      <div class="block__head">
        <span class="block__num">09</span>
        <h2 class="block__title">安全工具<em>Toolkit</em></h2>
        <span class="block__rule"></span>
      </div>
      <div class="index-tools matrix-tools">
        <label class="index-search" for="secSearch">
          <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="7" cy="7" r="4.5"></circle><path d="M10.5 10.5 14 14"></path></svg>
          <input id="secSearch" type="search" placeholder="搜索工具、语言或类别（按 / 聚焦）" autocomplete="off" spellcheck="false" aria-label="搜索安全工具">
        </label>
        <label class="matrix-select" for="secCategory">
          <span>类别</span>
          <select id="secCategory"><option value="all">全部类别</option>{options}</select>
        </label>
        <span class="era-head__count" id="secCount">{len(security.TOOLS)} 个工具</span>
      </div>
      <div class="stack-grid sec-grid">{_tool_cards()}</div>
      <p class="index-empty" id="secEmpty">没有匹配的工具。试试「TLS」「Java」「扫描」。</p>
    </section>

    <section class="block reveal" id="sources">
      <div class="block__head">
        <span class="block__num">10</span>
        <h2 class="block__title">参考来源<em>Sources</em></h2>
        <span class="block__rule"></span>
      </div>
      <p class="prose">安全工具与规范变化很快；下列为各工具官方文档入口，最后核对 {security.LAST_VERIFIED}。具体版本、默认配置与许可请以官方文档为准。</p>
      <ul class="sec-sources">{_sources_list()}</ul>
    </section>

    <footer class="pagefoot">
      <p class="stamp">安全建议为编者整理，不构成针对具体系统的安全保证；涉及生产系统请结合威胁建模、代码审计与授权测试。</p>
      <p>{batch_label} · 安全专题</p>
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
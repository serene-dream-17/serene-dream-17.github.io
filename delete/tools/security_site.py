# -*- coding: utf-8 -*-
"""安全专题页渲染。"""

import html

from data import security


TOPIC_BY_KEY = {t["key"]: t for t in security.TOPICS}

# 攻防类方向在卡片上标注授权前提。
AUTH_DIRECTIONS = {"pentest", "network", "reversing", "vuln-research", "mobile", "iot"}


def e(value):
    return html.escape(str(value), quote=True)


def _topic_tools(topic):
    tools = security.BY_DIRECTION.get(topic["key"], [])
    if not tools:
        return ""
    links = " · ".join(
        f'<a href="#{e(t["slug"])}">{e(t["name"])}</a>' for t in tools
    )
    return f'<p class="sec-topic-tools">代表工具：{links}</p>'


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
        direction = TOPIC_BY_KEY.get(tool["direction"], {})
        search = " ".join([
            tool["name"], tool["lang"], tool["category"], tool["summary"],
            tool["license"], direction.get("title", ""), " ".join(tool["fit"]),
        ]).lower()
        flag = ('<span class="sec-tool__flag">仅限授权测试</span>'
                if tool["direction"] in AUTH_DIRECTIONS else "")
        cards.append(f"""<article class="stack-card sec-tool" id="{e(tool["slug"])}" data-search="{e(search)}" data-dir="{e(tool["direction"])}">
        <span class="stack-top"><span class="stack-lang">{e(tool["lang"])}</span><span class="stack-type">{e(tool["category"])}</span></span>
        <span class="stack-fw">{e(tool["name"])}{flag}</span>
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
      {_topic_tools(topic)}
    </section>""")

    direction_options = "".join(
        f'<option value="{e(t["key"])}">{e(t["title"])}</option>'
        for t in security.TOPICS if t["key"] in security.BY_DIRECTION
    )
    tools_num = len(security.TOPICS) + 1
    sources_num = len(security.TOPICS) + 2

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
<title>安全专题 — 方向 × 工具 × 来源</title>
<meta name="description" content="按安全大类方向浏览：渗透测试与红队、网络与流量、逆向与二进制、漏洞挖掘、云原生、移动、嵌入式与工控、数据隐私、应急取证、威胁情报，以及应用安全、密码学、供应链与合规。">
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
      <p class="hero__kicker">SECURITY · 方向 × 工具</p>
      <h1 class="hero__title">安全<br><em>专题</em></h1>
      <p class="hero__sub">安全不只有应用安全：渗透测试与红队、网络与流量、逆向与二进制、漏洞挖掘、云原生、移动、嵌入式与工控、数据隐私、应急取证、威胁情报，各有各的工具链与前置条件。攻防类工具仅用于自有资产或书面授权测试。</p>
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
        <span class="block__num">{tools_num:02d}</span>
        <h2 class="block__title">安全工具<em>Toolkit</em></h2>
        <span class="block__rule"></span>
      </div>
      <div class="index-tools matrix-tools">
        <label class="index-search" for="secSearch">
          <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="7" cy="7" r="4.5"></circle><path d="M10.5 10.5 14 14"></path></svg>
          <input id="secSearch" type="search" placeholder="搜索工具、语言、方向或类别（按 / 聚焦）" autocomplete="off" spellcheck="false" aria-label="搜索安全工具">
        </label>
        <label class="matrix-select" for="secDirection">
          <span>方向</span>
          <select id="secDirection"><option value="all">全部方向</option>{direction_options}</select>
        </label>
        <span class="era-head__count" id="secCount">{len(security.TOOLS)} 个工具</span>
      </div>
      <div class="stack-grid sec-grid">{_tool_cards()}</div>
      <p class="index-empty" id="secEmpty">没有匹配的工具。试试「TLS」「Ghidra」「渗透」。</p>
    </section>

    <section class="block reveal" id="sources">
      <div class="block__head">
        <span class="block__num">{sources_num:02d}</span>
        <h2 class="block__title">参考来源<em>Sources</em></h2>
        <span class="block__rule"></span>
      </div>
      <p class="prose">安全工具与规范变化很快；下列为各工具官方文档入口，最后核对 {security.LAST_VERIFIED}。具体版本、默认配置与许可请以官方文档为准。</p>
      <ul class="sec-sources">{_sources_list()}</ul>
    </section>

    <footer class="pagefoot">
      <p class="stamp">安全建议为编者整理，不构成针对具体系统的安全保证；涉及生产系统请结合威胁建模、代码审计与授权测试。渗透、逆向与扫描类工具仅用于自有资产或取得书面授权的目标。</p>
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
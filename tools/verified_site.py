# -*- coding: utf-8 -*-
"""本机实测记录：页面区块与索引页。"""

import html

from data import verified as verified_data
from data import sources


def e(value):
    return html.escape(str(value), quote=True)


def by_slug():
    return getattr(verified_data, "VERIFIED", {})


INSTALLED_UNSCHEDULED = {
    "vb": "dotnet 已安装，未安排 VB 项目",
    "fsharp": "dotnet 已安装，未安排 F# 项目",
}

INSTALLABLE = {
    "rust": "rustc", "php": "php", "ruby": "ruby", "swift": "swift",
    "kotlin": "kotlinc", "scala": "scala", "haskell": "ghc", "lua": "lua",
    "r": "Rscript", "perl": "perl", "erlang": "erl", "elixir": "elixir",
    "julia": "julia", "dart": "dart", "zig": "zig", "nim": "nim",
    "crystal": "crystal", "elm": "elm", "groovy": "groovy", "clojure": "clojure",
    "d": "dmd", "ada": "gnat", "ocaml": "ocaml", 
     "delphi": "dcc", "pascal": "fpc", "tcl": "tclsh",
    "smalltalk": "Pharo", "prolog": "swipl", "scheme": "scheme", "ml": "sml",
    "commonlisp": "sbcl", "apl": "Dyalog", "matlab": "matlab", "cobol": "cobc",
    "modula2": "gm2", "eiffel": "ec", "actionscript": "mxmlc", "mojo": "mojo",
    "gleam": "gleam", "carbon": "carbon", "odin": "odin", "roc": "roc",
    "v": "v", "solidity": "solc", "verilog": "iverilog", "cuda": "nvcc",
    "glsl": "glslang", "markdown": "pandoc", "less": "lessc",
}


def verified_tag(slug):
    v = by_slug().get(slug)
    if not v:
        return ""
    return (
        f'<a class="tag tag--verified" href="#verify">已实测 Hello · {e(v["tool"])}</a>'
    )


def verified_block(slug):
    v = by_slug().get(slug)
    if not v:
        return ""
    artifacts = "".join(f"<li>{e(a)}</li>" for a in v.get("artifacts", []))
    return f"""<div class="verify" id="verify">
      <div class="verify__head">
        <span class="verify__badge">已实测</span>
        <b>本机复现记录</b>
        <span class="verify__meta">{e(v["date"])} · {e(v["tool"])}</span>
      </div>
      <div class="verify__grid">
        <div class="verify__item"><span class="verify__key">命令</span><code>{e(v["command"])}</code></div>
        <div class="verify__item"><span class="verify__key">输出</span><code>{e(v["output"])}</code></div>
      </div>
      <div class="verify__item"><span class="verify__key">产物 / 观察</span><ul class="verify__list">{artifacts}</ul></div>
      <p class="verify__note">{e(v.get("note", ""))}</p>
    </div>"""


def render_verified_page(langs, catalog_html, batch_label, batch_no):
    data = by_slug()
    coverage_rows = []
    for lang in sorted(langs.values(), key=lambda l: l["plate"]):
        if lang["slug"] in data:
            status, cls, reason = "已实测", "ok", data[lang["slug"]]["tool"]
        elif lang["slug"] in INSTALLED_UNSCHEDULED:
            status, cls, reason = "已装未测", "installed", INSTALLED_UNSCHEDULED[lang["slug"]]
        elif lang["slug"] in INSTALLABLE:
            status, cls, reason = "工具链未安装", "missing", "需要 " + INSTALLABLE[lang["slug"]]
        else:
            status, cls, reason = "仅文档", "doc", "历史/特定平台，暂未安排"
        src = sources.LANG.get(lang["slug"])
        src_html = (
            f'<a href="{e(src[1])}" target="_blank" rel="noopener noreferrer">{e(src[0])} ↗</a>'
            if src else '<span class="cmp-none">—</span>'
        )
        coverage_rows.append(
            f'<tr><td>{lang["plate"]:02d}</td>'
            f'<td><a href="langs/{lang["slug"]}.html">{e(lang["name"])}</a></td>'
            f'<td>{lang["year"]}</td>'
            f'<td><span class="cov cov--{cls}">{status}</span></td>'
            f'<td>{e(reason)}</td>'
            f'<td class="coverage-source">{src_html}</td></tr>'
        )
    counts = {"ok": 0, "installed": 0, "missing": 0, "doc": 0}
    for lang in langs.values():
        if lang["slug"] in data:
            counts["ok"] += 1
        elif lang["slug"] in INSTALLED_UNSCHEDULED:
            counts["installed"] += 1
        elif lang["slug"] in INSTALLABLE:
            counts["missing"] += 1
        else:
            counts["doc"] += 1
    coverage = (
        '<p class="cov-legend">'
        f'<span><span class="cov cov--ok">已实测</span>{counts["ok"]}</span>'
        f'<span><span class="cov cov--installed">已装未测</span>{counts["installed"]}</span>'
        f'<span><span class="cov cov--missing">未安装</span>{counts["missing"]}</span>'
        f'<span><span class="cov cov--doc">仅文档</span>{counts["doc"]}</span>'
        '</p>'
        '<div class="table-wrap"><table class="coverage-table">'
        '<caption>78 个条目的实测覆盖</caption>'
        '<thead><tr><th>#</th><th>条目</th><th>年份</th><th>状态</th><th>说明</th><th>官方来源</th></tr></thead>'
        f'<tbody>{"".join(coverage_rows)}</tbody></table></div>'
    )
    cards = []
    for slug, v in data.items():
        lang = langs.get(slug)
        if not lang:
            continue
        artifacts = "".join(f"<li>{e(a)}</li>" for a in v.get("artifacts", []))
        cards.append(f"""<article class="verify-card">
      <header class="verify-card__head">
        <h2><a href="langs/{slug}.html">{e(lang["name"])}</a></h2>
        <span class="verify__badge">已实测</span>
      </header>
      <p class="verify-card__tool">{e(v["tool"])} · {e(v["date"])}</p>
      <dl class="verify-card__dl">
        <dt>命令</dt><dd><code>{e(v["command"])}</code></dd>
        <dt>输出</dt><dd><code>{e(v["output"])}</code></dd>
        <dt>产物 / 观察</dt><dd><ul class="verify__list">{artifacts}</ul></dd>
        <dt>说明</dt><dd>{e(v.get("note", ""))}</dd>
      </dl>
      <a class="verify-card__link" href="langs/{slug}.html#verify">查看语言页的完整产物链 →</a>
    </article>""")

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
<title>实测记录 — {len(cards)} 门语言的本机复现</title>
<meta name="description" content="用本机工具链实际编译/运行 Hello 程序的记录：命令、输出、产物与平台差异。">
<link rel="stylesheet" href="assets/style.css">
</head>
<body data-page="verified">
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
      <p class="hero__kicker">VERIFIED · 本机实测</p>
      <h1 class="hero__title">实测<br><em>记录</em></h1>
      <p class="hero__sub">以下 {len(cards)} 门语言由本机已有工具链实际编译或运行；其余条目以官方文档为准，<b>不额外安装工具链</b>。</p>
      <div class="hero__meta">
        <div class="stat"><span class="stat__num">{len(cards)}</span><span class="stat__label">门已实测</span></div>
        <div class="stat"><span class="stat__num">{len(langs) - len(data)}</span><span class="stat__label">仅官方文档</span></div>
        <div class="stat"><span class="stat__num">2026-10-28</span><span class="stat__label">实测日期</span></div>
        <div class="stat"><span class="stat__num">{batch_no}</span><span class="stat__label">当前批次</span></div>
      </div>
    </header>

    <section class="block reveal" id="scope">
      <div class="block__head">
        <span class="block__num">00</span>
        <h2 class="block__title">实测范围<em>Scope</em></h2>
        <span class="block__rule"></span>
      </div>
      <div class="prose">
        <p>实测对象是每门语言的 Hello 程序与最基本的产物（源码 → 编译/运行 → 输出/目标文件）。它验证的是「这条链在本机跑得通」，不是对页面中每个示意地址、偏移或字节数的背书。</p>
        <p>平台差异会被明确记录：例如 Windows/MinGW 的 C/C++ 产物是 PE/COFF，而页面中的 ELF 样例是 Linux 口径；Shell 实测使用 Git Bash 而非 WSL。未安装工具链的语言不写入实测记录。</p>
      </div>
    </section>

    <section class="block reveal" id="coverage">
      <div class="block__head">
        <span class="block__num">01</span>
        <h2 class="block__title">覆盖范围<em>Coverage</em></h2>
        <span class="block__rule"></span>
      </div>
      <div class="prose">
        <p>已实测 {len(data)} / {len(langs)} 个条目。状态分为四级：已实测、已装未测（工具链存在但未安排）、未安装、仅文档。<b>不安装额外工具链</b>；未实测条目以官方文档为准。</p>
      </div>
      {coverage}
    </section>

    <section class="block reveal" id="records">
      <div class="block__head">
        <span class="block__num">02</span>
        <h2 class="block__title">复现记录<em>Records</em></h2>
        <span class="block__rule"></span>
      </div>
      <div class="verify-grid">{"".join(cards)}</div>
    </section>

    <footer class="pagefoot">
      <p class="stamp">实测脚本：tools/verify.py。记录只包含本机真正跑通的条目；重新运行会覆盖 tools/data/verified.py。</p>
      <p>{batch_label} · 实测记录</p>
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

# -*- coding: utf-8 -*-
"""语言谱系图：从 lineage 数据生成静态 SVG + 交互数据。"""

import html
import re

import formats  # noqa: F401  仅用于保持工具目录导入一致

WIDTH = 2200
HEIGHT = 1120
LEFT = 168
RIGHT = 64
TOP = 118
BAND_H = 100
YEAR_MIN = 1949
YEAR_MAX = 2023

ALIASES = {
    "c++": "cpp", "c#": "csharp", "f#": "fsharp", "objective-c": "objectivec",
    "common lisp": "commonlisp", "visual basic": "vb", "modula-2": "modula2",
    "simula 67": "simula", "algol 60": "algol60", "pl/i": "pli",
    "standard ml": "ml", "emacs lisp": "lisp", "racket": "scheme",
    "fortran 77 / 90 / 2018": "fortran", "fortran 77": "fortran",
    "javascript": "javascript", "typescript": "typescript",
    "go": "go", "rust": "rust", "swift": "swift", "kotlin": "kotlin",
    "elixir": "elixir", "gleam": "gleam", "reasonml / rescript": "",
    "lua": "lua", "r": "r", "delphi": "delphi", "ocaml": "ocaml",
    "haskell": "haskell", "scala": "scala", "clojure": "clojure",
    "groovy": "groovy", "julia": "julia", "dart": "dart", "zig": "zig",
    "nim": "nim", "crystal": "crystal", "elm": "elm", "solidity": "solidity",
    "mojo": "mojo", "carbon": "carbon", "odin": "odin", "roc": "roc", "v": "v",
    "sql": "sql", "assembly": "assembly", "shell": "shell", "verilog": "verilog",
    "cuda": "cuda", "glsl": "glsl", "html": "html", "css": "css",
    "xml": "xml", "svg": "svg", "yaml": "yaml", "markdown": "markdown",
    "sass": "sass", "scss": "sass", "less": "less",
}


def _norm(value):
    s = re.sub(r"[（(].*?[）)]", "", str(value))
    s = s.lower()
    s = s.replace("fortran 77 / 90 / 2018", "fortran")
    s = re.sub(r"[^a-z0-9+#\- ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def build_edges(languages, lineage_by_slug):
    by_name = {}
    for l in languages:
        by_name[_norm(l["name"])] = l["slug"]
        by_name[l["slug"]] = l["slug"]
    by_name.update(ALIASES)
    by_name = {k: v for k, v in by_name.items() if v}

    def resolve(text):
        s = _norm(text)
        if s in by_name:
            return by_name[s]
        # 前缀匹配：Fortran 77 / 90 / 2018 → Fortran
        for name, slug in sorted(by_name.items(), key=lambda x: -len(x[0])):
            if s.startswith(name + " "):
                return slug
        return None

    edges = []
    seen = set()
    for slug, lineage in lineage_by_slug.items():
        for target in lineage.get("to", []):
            dest = resolve(target)
            if dest and dest != slug and (slug, dest) not in seen:
                seen.add((slug, dest))
                edges.append({"from": slug, "to": dest, "label": str(target)})
        for source in lineage.get("from", []):
            src = resolve(source)
            if src and src != slug and (src, slug) not in seen:
                seen.add((src, slug))
                edges.append({"from": src, "to": slug, "label": str(source)})
    return edges


def layout(languages, eras):
    era_order = {e["key"]: i for i, e in enumerate(eras)}
    bands = {}
    for l in languages:
        bands.setdefault(l["era"], []).append(l)
    nodes = {}
    for era, items in bands.items():
        items.sort(key=lambda l: (l["year"], l["plate"]))
        band_y = TOP + era_order[era] * BAND_H
        for i, l in enumerate(items):
            x = LEFT + (l["year"] - YEAR_MIN) / (YEAR_MAX - YEAR_MIN) * (WIDTH - LEFT - RIGHT)
            offsets = [-24, 0, 24, -12, 12, -30, 30, -6, 6]
            y = band_y + 50 + offsets[i % len(offsets)]
            nodes[l["slug"]] = {
                "x": round(x, 1), "y": round(y, 1),
                "lang": l, "band_y": band_y,
                "label_above": i % 2 == 0,
            }
    return nodes


def render_svg(languages, eras, nodes, edges):
    parts = []
    # 年代带
    for i, era in enumerate(eras):
        y = TOP + i * BAND_H
        parts.append(f'<rect x="0" y="{y - 18}" width="{WIDTH}" height="{BAND_H}" class="lineage-band"/>')
        parts.append(f'<text x="24" y="{y + 6}" class="lineage-era">{html.escape(era["title"])}</text>')
        parts.append(f'<text x="24" y="{y + 22}" class="lineage-era-range">{html.escape(era["range"])}</text>')

    # 年刻度
    for year in range(1950, 2024, 10):
        x = LEFT + (year - YEAR_MIN) / (YEAR_MAX - YEAR_MIN) * (WIDTH - LEFT - RIGHT)
        parts.append(f'<line x1="{x:.0f}" y1="{TOP - 34}" x2="{x:.0f}" y2="{HEIGHT - 46}" class="lineage-tick"/>')
        parts.append(f'<text x="{x:.0f}" y="{TOP - 42}" class="lineage-year">{year}</text>')

    # 边
    for e in edges:
        a, b = nodes.get(e["from"]), nodes.get(e["to"])
        if not a or not b:
            continue
        mx = (a["x"] + b["x"]) / 2
        my = (a["y"] + b["y"]) / 2 - 26
        parts.append(
            f'<path class="lineage-edge" data-from="{e["from"]}" data-to="{e["to"]}" '
            f'd="M{a["x"]:.1f},{a["y"]:.1f} Q{mx:.1f},{my:.1f} {b["x"]:.1f},{b["y"]:.1f}"/>'
        )

    # 节点与标签
    for slug, n in nodes.items():
        l = n["lang"]
        color = {
            "compiled": "#2f4a3c", "interpreted": "#8c3324",
            "domain": "#a8812f", "markup": "#4f5b7a",
        }.get(l["family"], "#1c1a16")
        label_y = n["y"] - 10 if n["label_above"] else n["y"] + 16
        anchor = "middle"
        parts.append(
            f'<g class="lineage-node" data-slug="{slug}" data-family="{l["family"]}" '
            f'data-name="{html.escape(l["name"])}" data-year="{l["year"]}" tabindex="0" role="link" '
            f'aria-label="{html.escape(l["name"])} {l["year"]}">'
            f'<circle class="lineage-hit" cx="{n["x"]:.1f}" cy="{n["y"]:.1f}" r="9" fill="transparent"/>'
            f'<circle cx="{n["x"]:.1f}" cy="{n["y"]:.1f}" r="4.5" fill="{color}"/>'
            f'<text x="{n["x"]:.1f}" y="{label_y:.1f}" text-anchor="{anchor}" class="lineage-label">'
            f'{html.escape(l["name"])}</text></g>'
        )
    return "".join(parts)


def render_page(languages, eras, lineage_by_slug, catalog_html, batch_label, batch_no, total):
    edges = build_edges(languages, lineage_by_slug)
    nodes = layout(languages, eras)
    svg = render_svg(languages, eras, nodes, edges)
    families = [("compiled", "编译型"), ("interpreted", "解释 / 字节码"), ("domain", "领域专用"), ("markup", "标记 / 配置")]
    filters = "".join(
        f'<button class="filter" type="button" data-lineage-filter="{k}" aria-pressed="false">{label}</button>'
        for k, label in families
    )
    edge_json = html.escape(__import__("json").dumps(edges, ensure_ascii=False))

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
<title>语言谱系图 — 影响关系与时间轴</title>
<meta name="description" content="78 门语言的影响关系图：按年代与家族排布，悬停高亮传承关系，点击进入语言档案。">
<link rel="stylesheet" href="assets/style.css">
</head>
<body data-page="lineage">
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
      <p class="hero__kicker">LINEAGE · 影响关系 × 时间轴</p>
      <h1 class="hero__title">语言<br><em>谱系</em></h1>
      <p class="hero__sub">78 门语言按年代横轴、家族分带排布；曲线是「谁影响了谁」。悬停节点看传承，点击进入档案。</p>
      <div class="hero__meta">
        <div class="stat"><span class="stat__num">{len(languages)}</span><span class="stat__label">个节点</span></div>
        <div class="stat"><span class="stat__num">{len(edges)}</span><span class="stat__label">条影响边</span></div>
        <div class="stat"><span class="stat__num">{len(eras)}</span><span class="stat__label">个年代带</span></div>
        <div class="stat"><span class="stat__num">{batch_no}</span><span class="stat__label">当前批次</span></div>
      </div>
    </header>

    <div class="lineage-tools">
      <div class="filters" role="group" aria-label="按家族筛选">
        <button class="filter" type="button" data-lineage-filter="all" aria-pressed="true">全部</button>
        {filters}
      </div>
      <span class="lineage-count" id="lineageCount">{len(nodes)} 个节点 · {len(edges)} 条边</span>
    </div>

    <div class="lineage-wrap">
      <svg class="lineage-graph" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="语言影响关系图">
        {svg}
      </svg>
      <div class="lineage-tip" id="lineageTip" hidden></div>
    </div>
    <p class="lineage-scrollhint">横向滚动查看 2000s–2020s →</p>

    <div class="lineage-legend">
      <span><i style="background:#2f4a3c"></i>编译型</span>
      <span><i style="background:#8c3324"></i>解释 / 字节码</span>
      <span><i style="background:#a8812f"></i>领域专用</span>
      <span><i style="background:#4f5b7a"></i>标记 / 配置</span>
      <span class="lineage-hint">曲线方向：旧 → 新；只显示能对应到站内条目的关系。</span>
    </div>

    <section class="block reveal" id="howto">
      <div class="block__head">
        <span class="block__num">01</span>
        <h2 class="block__title">怎么读<em>How to read</em></h2>
        <span class="block__rule"></span>
      </div>
      <div class="prose">
        <p>横轴是首次发布年份，纵轴按「创世纪 / 系统 / 个人电脑 / 互联网 / 托管运行时 / 现代工程化 / 新一波 / 领域 / 标记」分带。节点颜色表示家族；曲线表示 <code>lineage.from / to</code> 中能映射到站内条目的影响关系。</p>
        <p>这不是完整的学术谱系：只收录本站 78 个条目之间的边，非语言来源（如 λ 演算、汇编、数学记法）不会画成节点；同名不同义的条目也不会强行连线。</p>
      </div>
    </section>

    <footer class="pagefoot">
      <p class="stamp">谱系基于各语言页的「源自 / 影响」字段；年代为首次发布年，不同资料的诞生年口径可能不同。最后核对 2026-10-28。</p>
      <p>{batch_label} · 语言谱系</p>
    </footer>
  </div>
</main>
<script src="assets/font.js"></script>
<script src="assets/data.js"></script>
<script src="assets/search-index.js"></script>
<script src="assets/app.js"></script>
<script src="assets/search.js"></script>
<script src="assets/lineage.js"></script>
<script type="application/json" id="lineageEdges">{edge_json}</script>
</body>
</html>
"""

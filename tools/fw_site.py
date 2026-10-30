# -*- coding: utf-8 -*-
"""框架页与场景矩阵的 HTML 渲染。"""

import html
import re

import ui
import sources_site
from data import fw_meta, sources, stacks


def e(value):
    return html.escape(str(value), quote=True)


def slugify(value):
    s = re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")
    return s or "item"


def _card_by_name(cards, name):
    for card in cards:
        if card["name"] == name:
            return card
    return None


def _stacks_section(slug):
    hits = []
    for st in stacks.STACKS:
        for layer in st["layers"]:
            if any(isinstance(i, tuple) and i[0] == slug for i in layer["items"]):
                hits.append(st)
                break
    if not hits:
        return ""
    chips = "".join(
        f'<a class="fw-chip" href="../stacks/{e(st["key"])}.html">{e(st["title"])}</a>'
        for st in hits
    )
    return f"""<section class="block reveal" id="stacks">
    <div class="block__head">
      <span class="block__num">03</span>
      <h2 class="block__title">用到它的技术栈<em>Stacks</em></h2>
      <span class="block__rule"></span>
    </div>
    <div class="fw-chips fw-chips--large">{chips}</div>
  </section>"""


def render_teaser(lang, detail, short):
    slug = lang["slug"]
    href = f"../frameworks/{slug}.html"
    if detail:
        cards = detail["cards"]
        chips = "".join(f'<span class="fw-chip">{e(c["name"])}</span>' for c in cards[:4])
        return f"""<section class="block fw-teaser reveal" id="frameworks">
    <div class="block__head">
      <span class="block__num">06</span>
      <h2 class="block__title">框架与场景<em>Frameworks</em></h2>
      <span class="block__rule"></span>
    </div>
    <div class="fw-teaser__card">
      <div class="fw-teaser__body">
        <p class="fw-teaser__summary">{e(detail["summary"])}</p>
        <div class="fw-chips">{chips}</div>
      </div>
      <a class="fw-teaser__link" href="{href}">查看框架与场景 →</a>
    </div>
  </section>"""

    tools = "".join(f'<span class="fw-chip">{e(t)}</span>' for t in short.get("tools", [])[:4])
    return f"""<section class="block fw-teaser reveal" id="frameworks">
    <div class="block__head">
      <span class="block__num">06</span>
      <h2 class="block__title">框架与场景<em>Frameworks</em></h2>
      <span class="block__rule"></span>
    </div>
    <div class="fw-teaser__card">
      <div class="fw-teaser__body">
        <p class="fw-teaser__summary">{e(short["summary"])}</p>
        <div class="fw-chips">{tools}</div>
      </div>
      <a class="fw-teaser__link" href="{href}">查看生态与场景 →</a>
    </div>
  </section>"""


def render_cards(slug, detail):
    cards = []
    for card in detail["cards"]:
        cid = slugify(card["name"])
        m = fw_meta.META.get((slug, card["name"]), {})
        badges = (
            f'<div class="fw-badges">'
            f'<span class="fw-badge" title="编者判断，非官方评级"><b>学习</b>{e(m.get("learn", "—"))}</span>'
            f'<span class="fw-badge" title="编者判断，非官方评级"><b>生态</b>{e(m.get("eco", "—"))}</span>'
            f'<span class="fw-badge" title="许可以官方文档为准"><b>许可</b><a class="cite" href="#fw-src-{cid}" aria-label="许可来源">{e(m.get("license", "—"))}</a></span>'
            f'</div>'
        )
        fit = "".join(f"<li>{e(x)}</li>" for x in card["fit"])
        avoid = "".join(f"<li>{e(x)}</li>" for x in card["avoid"])
        chain = "".join(
            f'<span class="fw-step">{e(step)}</span>'
            + ("<span class=\"fw-arrow\" aria-hidden=\"true\">→</span>" if i < len(card["chain"]) - 1 else "")
            for i, step in enumerate(card["chain"])
        )
        projects = " · ".join(e(x) for x in card["projects"])
        alts = "；".join(f"{e(name)}（{e(why)}）" for name, why in card["alternatives"])
        cards.append(f"""<article class="fw-card" id="{cid}">
      <header class="fw-card__head">
        <span class="fw-type">{e(card["type"])}</span>
        <h3 class="fw-name">{e(card["name"])}</h3>
        <span class="fw-year">{card["year"]}</span>
      </header>
      <p class="fw-maintainer">{e(card["maintainer"])}</p>
      {badges}
      <p class="fw-tagline">{e(card["tagline"])}</p>
      <div class="fw-cols">
        <div><h4 class="fw-label">适用</h4><ul class="fw-list">{fit}</ul></div>
        <div><h4 class="fw-label">不适用</h4><ul class="fw-list fw-list--avoid">{avoid}</ul></div>
      </div>
      <div class="fw-chain" aria-label="最小产物链">{chain}</div>
      <div class="fw-meta">
        <p><b>代表</b> {projects}</p>
        <p><b>替代</b> {alts}</p>
      </div>
      <p class="fw-division">{e(card["division"])}</p>
      {sources_site.fw_source(slug, card["name"], cid)}
    </article>""")
    return "".join(cards)


def render_page(lang, detail, short, catalog_html, total, batch_label):
    slug = lang["slug"]
    name = lang["name"]
    cards = detail["cards"] if detail else []
    count = len(cards) if detail else 0
    scenarios = detail["scenarios"] if detail else ["无成熟应用框架", "生态 / 工具"]
    tag_html = '<span class="tag tag--level" title="框架卡的学习/生态为编者判断，许可以官方文档为准">编者判断</span>' + "".join(f'<span class="tag">{e(t)}</span>' for t in scenarios)

    if detail:
        picks = "".join(
            f"<tr><td>{e(need)}</td>"
            f"<td><a href=\"#{slugify(pick)}\">{e(pick)}</a></td>"
            f"<td>{e(why)}</td></tr>"
            for need, pick, why in detail["picks"]
        )
        conclusion = "；".join(
            f"{e(need)} → <b>{e(pick)}</b>"
            for need, pick, _why in detail["picks"][:3]
        ) + "。"
        compare_rows = "".join(
            f"<tr><td>{e(c['name'])}</td><td>{e(c['type'])}</td>"
            f"<td>{e(fw_meta.META.get((slug, c['name']), {}).get('learn', '—'))}</td>"
            f"<td>{e(fw_meta.META.get((slug, c['name']), {}).get('eco', '—'))}</td>"
            f"<td>{e(fw_meta.META.get((slug, c['name']), {}).get('license', '—'))}</td>"
            f"<td>{e(c['chain'][0])} → {e(c['chain'][-1])}</td></tr>"
            for c in detail["cards"]
        )
        body = f"""<section class="block reveal" id="picks">
    <div class="block__head">
      <span class="block__num">01</span>
      <h2 class="block__title">选型速查<em>Decision Guide</em></h2>
      <span class="block__rule"></span>
    </div>
    <div class="table-wrap">
      <table class="pick-table">
        <caption>需求 → 推荐 → 理由</caption>
        <thead><tr><th scope="col">需求</th><th scope="col">推荐</th><th scope="col">理由</th></tr></thead>
        <tbody>{picks}</tbody>
      </table>
    </div>
    <p class="table-hint">表格可横向滑动 →</p>
    <p class="pick-conclusion"><b>选型结论</b> {conclusion}</p>
  </section>
  <section class="block reveal" id="cards">
    <div class="block__head">
      <span class="block__num">02</span>
      <h2 class="block__title">框架决策卡<em>{count} cards</em></h2>
      <span class="block__rule"></span>
    </div>
    <div class="fw-grid">{render_cards(slug, detail)}</div>
    <h3 class="fw-compare-title">同语言框架对比</h3>
    <div class="table-wrap">
      <table class="fw-compare">
        <caption>学习曲线 / 生态 / 许可 / 最小产物链</caption>
        <thead><tr><th scope="col">框架</th><th scope="col">类型</th><th scope="col">学习</th><th scope="col">生态</th><th scope="col">许可</th><th scope="col">产物链</th></tr></thead>
        <tbody>{compare_rows}</tbody>
      </table>
    </div>
    <p class="table-hint">表格可横向滑动 →</p>
  </section>"""
        summary = detail["summary"]
        meta_value = f"{count} 个框架"
    else:
        tools = "".join(f'<span class="fw-chip">{e(t)}</span>' for t in short.get("tools", []))
        body = f"""<section class="block reveal" id="tools">
    <div class="block__head">
      <span class="block__num">01</span>
      <h2 class="block__title">生态工具<em>Ecosystem</em></h2>
      <span class="block__rule"></span>
    </div>
    <p class="prose">下列工具与库属于该语言的生态；它们的规模与成熟度通常小于主流框架。</p>
    <div class="fw-chips fw-chips--large">{tools}</div>
  </section>
  <section class="block reveal" id="when">
    <div class="block__head">
      <span class="block__num">02</span>
      <h2 class="block__title">什么时候仍选它<em>When</em></h2>
      <span class="block__rule"></span>
    </div>
    <p class="prose">{e(short["when"])}</p>
  </section>"""
        summary = short["summary"]
        meta_value = "无成熟应用框架"

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{ui.head_snippet()}
<title>{e(name)} · 框架与场景 — 语言的产物链</title>
<meta name="description" content="{e(name)} 的框架与使用场景：{e(summary)}">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body data-page="framework" data-root="../">
<a class="skip-link" href="#main">跳到正文</a>
<div class="progress" aria-hidden="true"><span></span></div>
<button class="menu-toggle" type="button" aria-label="打开目录" aria-expanded="false" aria-controls="catalog"><span></span></button>
<div class="scrim"></div>
{ui.font_ui()}
<button class="cmdk-btn" type="button" data-cmdk aria-label="全站搜索">搜索全站 <kbd>⌘K</kbd></button>
{catalog_html}
<main class="page" id="main">
  <div class="page__inner">
    <nav class="plate-nav" aria-label="框架页导航">
      <a class="plate-nav__link" href="../languages/{slug}.html">← <span>{e(name)} 档案</span></a>
      <span class="plate-nav__counter">FRAMEWORKS · {lang["plate"]:02d} / {total}</span>
      <a class="plate-nav__link" href="../scenarios.html"><span>开发场景</span> →</a>
    </nav>
    <header class="dossier fw-dossier">
      <div class="dossier__eyebrow">
        <span>FRAMEWORKS · PLATE {lang["plate"]:02d} / {total}</span>
        <span class="dot"></span>
        <span class="era">{e(lang["family_label"])}</span>
        <span class="dot"></span>
        <span>{count} 个框架</span>
      </div>
      <h1 class="dossier__name">{e(name)}<span class="cn">框架与场景</span></h1>
      <p class="dossier__tagline">{e(summary)}</p>
      <div class="tags">{tag_html}</div>
      <div class="dossier__meta">
        <div class="meta-item"><span class="meta-label">语言</span><span class="meta-value">{e(name)}</span></div>
        <div class="meta-item"><span class="meta-label">类型</span><span class="meta-value">{e(lang["family_label"])}</span></div>
        <div class="meta-item"><span class="meta-label">框架</span><span class="meta-value">{e(meta_value)}</span></div>
        <div class="meta-item"><span class="meta-label">入口</span><span class="meta-value"><a href="../languages/{slug}.html">语言档案 →</a></span></div>
      </div>
    </header>
    {body}
    {_stacks_section(slug)}
    <footer class="pagefoot">
      <p class="stamp">框架与生态会随时间变化；学习/生态为编者判断，许可与事实以官方文档为准。最后核对 {sources.LAST_VERIFIED}。</p>
      <p>{batch_label} · {e(name)} 框架页</p>
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

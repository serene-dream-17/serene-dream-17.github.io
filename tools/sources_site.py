# -*- coding: utf-8 -*-
"""来源区块：带编号的页级引用。"""

import html
from data import sources


def e(value):
    return html.escape(str(value), quote=True)


def lang_sources(slug):
    item = sources.LANG.get(slug)
    if not item:
        return ""
    label, url = item
    return f"""<section class="sources" id="sources" aria-label="参考来源">
    <h3 class="sources__title">参考来源 <span>References</span></h3>
    <ol class="sources__list">
      <li id="src-1"><a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(label)} ↗</a>
        <span class="sources__kind">官方文档 / 规范</span></li>
      <li id="src-2"><a href="../AUDIT.md">本站审计与方法说明</a>
        <span class="sources__kind">内容口径与已知限制</span></li>
    </ol>
    <p class="sources__note">最后核对 {sources.LAST_VERIFIED}。产物样例为示意内容；年份、许可与生态以来源文档为准。</p>
  </section>"""


def fw_source(slug, name, anchor):
    item = sources.FW.get((slug, name))
    if not item:
        return ""
    label, url = item
    return (
        f'<p class="fw-source" id="fw-src-{e(anchor)}">'
        f'<a href="{e(url)}" target="_blank" rel="noopener noreferrer">来源：{e(label)} ↗</a>'
        f'<span class="fw-source__kind">官方文档</span></p>'
    )


def esc(text):
    return html.escape(str(text), quote=True)

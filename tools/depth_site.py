# -*- coding: utf-8 -*-
"""语言深读区块的 HTML 渲染。"""

import html


def e(value):
    return html.escape(str(value), quote=True)


def render_deep(lang, deep):
    goals = "".join(f"<li>{e(x)}</li>" for x in deep["goals"])
    tradeoffs = "".join(f"<li>{e(x)}</li>" for x in deep["tradeoffs"])
    features = "".join(
        f'<div class="deep-feature"><span class="deep-feature__key">{e(k)}</span>'
        f'<span class="deep-feature__value">{e(v)}</span></div>'
        for k, v in deep["features"].items()
    )
    milestones = []
    for year, label in deep["timeline"]:
        milestones.append(
            f'<span class="deep-milestone"><b>{e(year)}</b><span>{e(label)}</span></span>'
        )
    timeline = '<span class="deep-arrow" aria-hidden="true">→</span>'.join(milestones)
    projects = " · ".join(e(x) for x in deep["projects"])
    compares = "".join(
        f"<tr><td>{e(name)}</td><td>{e(why)}</td></tr>"
        for name, why in deep["compare"]
    )

    return f"""<section class="block deep reveal" id="deep">
    <div class="block__head">
      <span class="block__num">05</span>
      <h2 class="block__title">语言深读<em>Deep Dive</em><span class="block__level" title="深读字段为编者整理，非官方评级">编者整理</span></h2>
      <span class="block__rule"></span>
    </div>

    <div class="deep-grid">
      <div class="deep-col">
        <h3 class="deep-sub">设计目标</h3>
        <ul class="deep-list">{goals}</ul>
      </div>
      <div class="deep-col">
        <h3 class="deep-sub">关键取舍</h3>
        <ul class="deep-list deep-list--tradeoff">{tradeoffs}</ul>
      </div>
    </div>

    <h3 class="deep-sub">语言特性 <a class="cite" href="#src-1" aria-label="来源 1">1</a></h3>
    <div class="deep-features">{features}</div>

    <h3 class="deep-sub">版本里程碑 <a class="cite" href="#src-1" aria-label="来源 1">1</a></h3>
    <div class="deep-timeline">{timeline}</div>

    <div class="deep-eco">
      <div><h3 class="deep-sub">代表项目</h3><p>{projects}</p></div>
      <div><h3 class="deep-sub">包管理 / 生态</h3><p>{e(deep["packages"])}</p></div>
      <div><h3 class="deep-sub">现状 <a class="cite" href="#src-1" aria-label="来源 1">1</a></h3><p>{e(deep["status"])}</p></div>
    </div>

    <h3 class="deep-sub">与邻近语言对比</h3>
    <div class="table-wrap">
      <table class="deep-table">
        <caption>{e(lang["name"])} 与邻近语言的差异</caption>
        <thead><tr><th scope="col">语言</th><th scope="col">主要差异</th></tr></thead>
        <tbody>{compares}</tbody>
      </table>
    </div>
    <p class="table-hint">表格可横向滑动 →</p>
  </section>"""

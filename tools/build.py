# -*- coding: utf-8 -*-
"""
静态站点生成器：tools/data/*.py → langs/*.html + index.html + assets/data.js

用法：
    python tools/build.py
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from registry import (  # noqa: E402
    LANGUAGES, ERAS, ERAS_BY_KEY, BUILT, BUILT_SLUGS, FAMILIES,
)
from data import era_1950, era_1970, era_1980, era_1990, era_2000, era_2010, era_2020, era_markup  # noqa: E402
from data import fw_a, fw_b, fw_c, fw_d, fw_e, fw_meta  # noqa: E402
from data import security, dev_scenarios  # noqa: E402
import fw_site  # noqa: E402
import ui  # noqa: E402
import depth_site  # noqa: E402
import sources_site  # noqa: E402
import src_index  # noqa: E402
import fmt_index  # noqa: E402
import lineage  # noqa: E402
import compare_index  # noqa: E402
import verified_site  # noqa: E402
import security_site  # noqa: E402
import scenario_site  # noqa: E402
from data import verified  # noqa: E402
import formats  # noqa: E402
from data import sources  # noqa: E402
from data import depth_1, depth_2, depth_3  # noqa: E402

DATA = {}
DATA.update(era_1950.LANGS)
DATA.update(era_1970.LANGS)
DATA.update(era_1980.LANGS)
DATA.update(era_1990.LANGS)
DATA.update(era_2000.LANGS)
DATA.update(era_2010.LANGS)
DATA.update(era_2020.LANGS)
DATA.update(era_markup.LANGS)

FRAMEWORKS = {}
for _mod in (fw_a, fw_b, fw_c, fw_d, fw_e):
    FRAMEWORKS.update(_mod.DETAIL)
SHORT = fw_d.SHORT
for _upgraded in list(FRAMEWORKS):
    SHORT.pop(_upgraded, None)
SCENARIOS = fw_d.SCENARIOS
FRAMEWORK_CARDS = sum(len(d["cards"]) for d in FRAMEWORKS.values())
fw_site.ALL_LANGS = LANGUAGES
scenario_site.ALL_LANGS = LANGUAGES

DEEP = {}
for _mod in (depth_1, depth_2, depth_3):
    DEEP.update(_mod.DEEP)

BATCH_DONE = 18
BATCH_LABEL = "第 1–18 批"
BATCH_RANGE = "1950s–2020s"
TOTAL = len(LANGUAGES)
OPEN = len(BUILT)

META = {
    "fortran":  ("John Backus 与 IBM 团队", "IBM，美国"),
    "lisp":     ("John McCarthy", "MIT，美国"),
    "algol60":  ("Peter Naur 等 / IFIP 委员会", "欧洲（苏黎世会议）"),
    "cobol":    ("Grace Hopper 等 / CODASYL", "美国国防部召集"),
    "basic":    ("John Kemeny & Thomas Kurtz", "Dartmouth College，美国"),
    "simula":   ("Ole-Johan Dahl & Kristen Nygaard", "挪威计算中心，挪威"),
    "pli":      ("IBM 委员会", "IBM，美国"),
    "apl":      ("Kenneth Iverson", "IBM，美国"),
    "snobol":   ("Farber / Griswold / Polonsky", "贝尔实验室，美国"),
    "b":        ("Ken Thompson", "贝尔实验室，美国"),
    "c":        ("Dennis Ritchie", "贝尔实验室，美国"),
    "pascal":   ("Niklaus Wirth", "ETH Zürich，瑞士"),
    "smalltalk": ("Alan Kay / Dan Ingalls 等", "Xerox PARC，美国"),
    "prolog":   ("Colmerauer & Roussel", "马赛大学，法国"),
    "ml":       ("Robin Milner 等", "爱丁堡大学，英国"),
    "scheme":   ("Guy Steele & Gerald Sussman", "MIT，美国"),
    "forth":    ("Charles H. Moore", "独立设计，美国"),
    "modula2":  ("Niklaus Wirth", "ETH Zürich，瑞士"),
    "cpp":      ("Bjarne Stroustrup", "贝尔实验室，美国"),
    "objectivec": ("Brad Cox & Tom Love", "Stepstone，美国"),
    "perl":     ("Larry Wall", "美国"),
    "erlang":   ("Joe Armstrong 等", "爱立信，瑞典"),
    "ada":      ("Jean Ichbiah 等", "CII Honeywell Bull，法国"),
    "eiffel":   ("Bertrand Meyer", "法国 / 瑞士"),
    "matlab":   ("Cleve Moler", "MathWorks，美国"),
    "commonlisp": ("ANSI X3J13 委员会", "美国"),
    "tcl":      ("John Ousterhout", "加州大学伯克利，美国"),
    "python":   ("Guido van Rossum", "CWI，荷兰"),
    "java":     ("James Gosling 等", "Sun Microsystems，美国"),
    "javascript": ("Brendan Eich", "Netscape，美国"),
    "php":      ("Rasmus Lerdorf", "个人项目 / Zend，丹麦-加拿大"),
    "ruby":     ("松本行弘（Matz）", "日本"),
    "haskell":  ("Haskell 委员会", "英国（格拉斯哥）"),
    "lua":      ("Roberto Ierusalimschy 等", "PUC-Rio，巴西"),
    "r":        ("Ross Ihaka & Robert Gentleman", "奥克兰大学，新西兰"),
    "delphi":   ("Anders Hejlsberg / Borland", "Borland，美国"),
    "vb":       ("Alan Cooper / Microsoft", "Microsoft，美国"),
    "ocaml":    ("Xavier Leroy 等", "INRIA，法国"),
    "csharp":   ("Anders Hejlsberg / Microsoft", "丹麦 / 美国"),
    "scala":    ("Martin Odersky", "EPFL，瑞士"),
    "fsharp":   ("Don Syme / Microsoft Research", "英国 / 美国"),
    "clojure":  ("Rich Hickey", "美国"),
    "groovy":   ("James Strachan", "Java 社区"),
    "go":       ("Griesemer / Pike / Thompson", "Google，美国"),
    "d":        ("Walter Bright / Digital Mars", "美国"),
    "actionscript": ("Gary Grossman / Macromedia", "美国"),
    "rust":     ("Graydon Hoare / Mozilla", "加拿大 / 美国"),
    "typescript": ("Anders Hejlsberg / Microsoft", "美国"),
    "swift":    ("Chris Lattner / Apple", "美国"),
    "kotlin":   ("JetBrains 团队", "捷克 / 俄罗斯"),
    "elixir":   ("José Valim", "巴西"),
    "julia":    ("Bezanson / Karpinski / Shah / Edelman", "MIT，美国"),
    "dart":     ("Lars Bak 等 / Google", "丹麦 / 美国"),
    "zig":      ("Andrew Kelley", "美国"),
    "nim":      ("Andreas Rumpf", "德国"),
    "crystal":  ("Ary Borenzweig", "阿根廷"),
    "elm":      ("Evan Czaplicki", "美国"),
    "solidity": ("Gavin Wood 等 / Ethereum", "英国 / 瑞士"),
    "mojo":     ("Chris Lattner / Modular", "美国"),
    "gleam":    ("Louis Pilfold", "英国"),
    "carbon":   ("Google Carbon 团队", "美国"),
    "odin":     ("Ginger Bill", "美国"),
    "roc":      ("Richard Feldman 等", "美国"),
    "v":        ("Alexander Medvednikov", "俄罗斯 / 开源社区"),
    "sql":      ("Chamberlin & Boyce / IBM", "美国"),
    "assembly": ("早期计算机程序员", "美国 / 英国"),
    "shell":    ("Stephen Bourne / 贝尔实验室", "英国 / 美国"),
    "verilog":  ("Phil Moorby / Gateway Design", "英国 / 美国"),
    "cuda":     ("NVIDIA", "美国"),
    "glsl":     ("3Dlabs / OpenGL ARB", "美国"),
    "html":     ("Tim Berners-Lee", "CERN，瑞士"),
    "css":      ("Håkon Wium Lie & Bert Bos", "W3C，挪威 / 荷兰"),
    "xml":      ("W3C XML 工作组", "W3C，美国 / 欧洲"),
    "svg":      ("W3C SVG 工作组", "W3C，美国 / 欧洲"),
    "yaml":     ("Clark Evans 等", "美国"),
    "markdown": ("John Gruber", "美国"),
    "sass":     ("Hampton Catlin / Natalie Weizenbaum", "美国"),
    "less":     ("Alexis Sellier", "法国"),
}

PARADIGMS = {
    "fortran":  ["命令式", "科学计算", "数组"],
    "lisp":     ["函数式", "符号计算", "宏"],
    "algol60":  ["命令式", "结构化", "块作用域"],
    "cobol":    ["命令式", "商业数据", "记录"],
    "basic":    ["命令式", "交互式", "教学"],
    "simula":   ["面向对象", "仿真", "协程"],
    "pli":      ["多范式", "商业数据", "异常"],
    "apl":      ["数组", "函数式", "交互式"],
    "snobol":   ["模式匹配", "字符串", "动态类型"],
    "b":        ["命令式", "无类型", "系统编程"],
    "c":        ["命令式", "系统编程", "静态类型"],
    "pascal":   ["命令式", "结构化", "教学"],
    "smalltalk": ["面向对象", "消息传递", "动态类型"],
    "prolog":   ["逻辑", "声明式", "回溯"],
    "ml":       ["函数式", "类型推断", "模式匹配"],
    "scheme":   ["函数式", "尾调用", "续延"],
    "forth":    ["栈式", "元编程", "嵌入式"],
    "modula2":  ["模块化", "系统编程", "强类型"],
    "cpp":       ["面向对象", "泛型", "系统编程"],
    "objectivec": ["面向对象", "消息传递", "Apple 生态"],
    "perl":      ["脚本", "文本处理", "正则"],
    "erlang":    ["并发", "容错", "函数式"],
    "ada":       ["强类型", "并发", "实时系统"],
    "eiffel":    ["面向对象", "契约式设计", "静态类型"],
    "matlab":    ["数组", "数值计算", "交互式"],
    "commonlisp": ["函数式", "宏", "CLOS"],
    "tcl":       ["脚本", "嵌入", "事件驱动"],
    "python":    ["命令式", "动态类型", "科学计算"],
    "java":      ["面向对象", "字节码", "企业应用"],
    "javascript": ["动态类型", "事件驱动", "原型"],
    "php":       ["脚本", "Web", "动态类型"],
    "ruby":      ["面向对象", "动态类型", "元编程"],
    "haskell":   ["纯函数式", "惰性", "类型系统"],
    "lua":       ["脚本", "嵌入", "轻量"],
    "r":         ["统计", "向量化", "交互式"],
    "delphi":    ["面向对象", "快速应用", "Windows"],
    "vb":        ["事件驱动", "快速应用", "COM"],
    "ocaml":     ["函数式", "类型推断", "模块"],
    "csharp":     ["面向对象", "托管运行时", "LINQ"],
    "scala":      ["函数式", "面向对象", "JVM"],
    "fsharp":     ["函数式", ".NET", "类型推断"],
    "clojure":    ["函数式", "Lisp", "持久化数据"],
    "groovy":     ["动态类型", "JVM", "脚本"],
    "go":         ["并发", "静态类型", "云原生"],
    "d":          ["系统编程", "模板", "GC"],
    "actionscript": ["面向对象", "Flash", "AVM2"],
    "rust":       ["系统编程", "所有权", "无 GC"],
    "typescript": ["静态类型", "JavaScript", "编译期"],
    "swift":      ["面向对象", "协议", "ARC"],
    "kotlin":     ["面向对象", "空安全", "JVM"],
    "elixir":     ["函数式", "并发", "BEAM"],
    "julia":      ["多重派发", "科学计算", "JIT"],
    "dart":       ["面向对象", "Flutter", "空安全"],
    "zig":        ["系统编程", "comptime", "无隐藏分配"],
    "nim":        ["系统编程", "宏", "编译到 C"],
    "crystal":    ["静态类型", "Ruby 语法", "LLVM"],
    "elm":        ["函数式", "前端", "无运行时异常"],
    "solidity":   ["智能合约", "EVM", "静态类型"],
    "mojo":       ["Python 语法", "系统编程", "MLIR"],
    "gleam":      ["静态类型", "BEAM", "函数式"],
    "carbon":     ["系统编程", "C++ 互操作", "泛型"],
    "odin":       ["系统编程", "数据导向", "游戏"],
    "roc":        ["函数式", "快速编译", "平台"],
    "v":          ["系统编程", "编译到 C", "简洁"],
    "sql":        ["声明式", "关系模型", "查询"],
    "assembly":   ["低级", "机器相关", "符号"],
    "shell":      ["脚本", "管道", "进程"],
    "verilog":    ["硬件描述", "并发", "仿真"],
    "cuda":       ["GPU", "并行", "SIMT"],
    "glsl":       ["着色器", "GPU", "图形管线"],
    "html":       ["标记", "文档结构", "超文本"],
    "css":        ["样式", "层叠", "声明式"],
    "xml":        ["标记", "数据交换", "可扩展"],
    "svg":        ["矢量图形", "XML", "声明式"],
    "yaml":       ["数据序列化", "配置", "人类可读"],
    "markdown":   ["标记", "纯文本", "文档"],
    "sass":       ["CSS 预处理", "变量", "嵌套"],
    "less":       ["CSS 预处理", "变量", "混入"],
}


# ------------------------------------------------------------------
# 基础工具
# ------------------------------------------------------------------
def e(value):
    return html.escape(str(value), quote=True)


def rich(value):
    """转义后把 `反引号` 片段转成 <code>。"""
    escaped = e(value)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)


def search_blob(lang):
    parts = [
        lang["name"], lang["cn"], lang["year"], lang["desc"],
        lang["family_label"], lang["slug"],
    ]
    parts.extend(PARADIGMS.get(lang["slug"], []))
    return e(" ".join(str(p) for p in parts).lower())


def stage_count(slug):
    return len(DATA[slug]["chain"])


def language_by_slug(slug):
    for lang in LANGUAGES:
        if lang["slug"] == slug:
            return lang
    raise KeyError(slug)


def neighbors(slug):
    i = BUILT_SLUGS.index(slug)
    prev_lang = BUILT[i - 1] if i > 0 else None
    next_lang = BUILT[i + 1] if i + 1 < len(BUILT) else None
    return prev_lang, next_lang


# ------------------------------------------------------------------
# 侧栏目录
# ------------------------------------------------------------------
SEARCH_ICON = (
    '<svg class="search__icon" viewBox="0 0 16 16" fill="none" '
    'stroke="currentColor" stroke-width="1.4" aria-hidden="true">'
    '<circle cx="7" cy="7" r="4.5"></circle>'
    '<path d="M10.5 10.5 14 14"></path></svg>'
)


def render_catalog(active_slug, root):
    groups = []
    for era in ERAS:
        items = [l for l in LANGUAGES if l["era"] == era["key"]]
        open_count = sum(1 for l in items if l["built"])
        lis = []
        for lang in items:
            active = lang["slug"] == active_slug
            status = "is-active" if active else ""
            search = search_blob(lang)
            common = (
                f'data-search="{search}" data-family="{lang["family"]}" '
                f'data-year="{lang["year"]}" data-name="{e(lang["name"])}"'
            )
            num = f'<span class="catalog__num">{lang["plate"]:02d}</span>'
            if lang["built"]:
                aria = ' aria-current="page"' if active else ""
                lis.append(
                    f'<li><a class="catalog__link {status}" href="{root}langs/'
                    f'{lang["slug"]}.html" {common}{aria}>'
                    f'{num}<span class="catalog__name">{e(lang["name"])}</span>'
                    f'<span class="catalog__year">{lang["year"]}</span></a></li>'
                )
            else:
                lis.append(
                    f'<li><span class="catalog__link is-pending" {common}>'
                    f'{num}<span class="catalog__name">{e(lang["name"])}</span>'
                    f'<span class="catalog__pending">待</span></span></li>'
                )
        groups.append(
            f'<section class="catalog__group" data-era="{era["key"]}">'
            f'<div class="catalog__grouphead"><span>{e(era["title"])}'
            f'</span><em>{open_count}/{len(items)}</em></div>'
            f'<ul class="catalog__list">{"".join(lis)}</ul></section>'
        )

    filters = [
        ("all", "全部"),
        ("compiled", "编译"),
        ("interpreted", "解释"),
        ("domain", "领域"),
        ("markup", "标记"),
    ]
    filter_html = "".join(
        f'<button class="filter" type="button" data-filter="{key}" '
        f'aria-pressed="{"true" if key == "all" else "false"}">{label}</button>'
        for key, label in filters
    )

    return f"""<aside class="catalog" id="catalog" aria-label="全站目录">
  <div class="catalog__head">
    <p class="catalog__kicker">Catalogue · 1957 — 2026</p>
    <h2 class="catalog__title">语言产物链<span>Languages &amp; Their Artifacts</span></h2>
    <p class="catalog__meta"><b>{OPEN}</b> / {TOTAL} 已开放 · 第 {BATCH_DONE} 批</p>
  </div>
  <div class="catalog__tools">
    <label class="search" for="catalogSearch">
      {SEARCH_ICON}
      <input id="catalogSearch" type="search" placeholder="搜索语言 / 年代 / 关键词"
             autocomplete="off" spellcheck="false" aria-label="搜索语言">
      <kbd>/</kbd>
    </label>
    <div class="filters" role="group" aria-label="按实现方式筛选">{filter_html}</div>
  </div>
  <div class="catalog__body">
    {"".join(groups)}
    <p class="catalog__empty" data-visible="false">没有匹配的条目。<br>试试「c」「1972」「字节码」。</p>
  </div>
  <div class="catalog__foot">
    {BATCH_LABEL} · {BATCH_RANGE}<br>
    <a href="{root}index.html">← 馆藏总览</a><br>
    <a href="{root}frameworks.html">框架场景矩阵 →</a><br>
    <a href="{root}scenarios.html">开发场景 →</a><br>
    <a href="{root}security.html">安全专题 →</a><br>
    <a href="{root}sources.html">来源索引 →</a><br>
    <a href="{root}formats.html">产物格式索引 →</a><br>
    <a href="{root}lineage.html">语言谱系图 →</a><br>
    <a href="{root}compare.html">对比器 →</a><br>
    <a href="{root}verified.html">实测记录 →</a>
  </div>
</aside>"""


def render_page_nav(lang, prev_lang, next_lang):
    if prev_lang:
        prev_href = f"{prev_lang['slug']}.html"
        prev_text = f'<a class="plate-nav__link" href="{prev_href}">← <span>{e(prev_lang["name"])}</span></a>'
    else:
        prev_href = "../index.html"
        prev_text = f'<a class="plate-nav__link" href="{prev_href}">← <span>馆藏目录</span></a>'

    if next_lang:
        next_href = f"{next_lang['slug']}.html"
        next_text = f'<a class="plate-nav__link" href="{next_href}"><span>{e(next_lang["name"])}</span> →</a>'
    else:
        next_href = "../index.html"
        next_text = f'<a class="plate-nav__link" href="{next_href}"><span>馆藏目录</span> →</a>'

    return (
        f'<nav class="plate-nav" aria-label="翻页">'
        f'{prev_text}'
        f'<span class="plate-nav__counter">PLATE <b>{lang["plate"]}</b> / {TOTAL}</span>'
        f'{next_text}</nav>'
    )


# ------------------------------------------------------------------
# 页面区块
# ------------------------------------------------------------------
def render_dossier(lang, data):
    designer, place = META[lang["slug"]]
    era = ERAS_BY_KEY[lang["era"]]
    tags = PARADIGMS.get(lang["slug"], []) + [lang["family_label"]]
    tag_html = "".join(
        f'<span class="tag{" is-accent" if t == lang["family_label"] else ""}">{e(t)}</span>'
        for t in tags
    )
    cn_html = (
        f'<span class="cn">{e(lang["cn"])}</span>'
        if lang["cn"] != lang["name"] else ""
    )
    if lang["slug"] in verified.VERIFIED:
        level_tag = verified_site.verified_tag(lang["slug"])
    else:
        level_tag = '<span class="tag tag--level" title="产物链样例为文档重构，不是本机实测">文档重构</span>'
    froms = " · ".join(e(x) for x in data["lineage"]["from"])
    tos = " · ".join(e(x) for x in data["lineage"]["to"])

    return f"""<header class="dossier">
    <div class="dossier__eyebrow">
      <span>PLATE {lang["plate"]:02d} / {TOTAL}</span>
      <span class="dot"></span>
      <span class="era">{e(era["title"])} · {e(era["range"])}</span>
      <span class="dot"></span>
      <span>{e(lang["family_label"])}</span>
    </div>
    <h1 class="dossier__name">{e(lang["name"])}{cn_html}</h1>
    <p class="dossier__tagline">{rich(data["tagline"])}</p>
    <div class="dossier__meta">
      <div class="meta-item"><span class="meta-label">设计者</span><span class="meta-value">{e(designer)}</span></div>
      <div class="meta-item"><span class="meta-label">诞生地</span><span class="meta-value">{e(place)}</span></div>
      <div class="meta-item"><span class="meta-label">首次发布</span><span class="meta-value">{lang["year"]}</span></div>
      <div class="meta-item"><span class="meta-label">类型</span><span class="meta-value">{e(lang["family_label"])}</span></div>
    </div>
    <div class="tags">{tag_html}{level_tag}</div>
    <a class="dossier__fwlink" href="{lang["slug"]}-frameworks.html">框架与场景 →</a>
    <div class="lineage">
      <div><div class="lineage__label">源自 / From</div><p class="lineage__list">{froms}</p></div>
      <div><div class="lineage__label">影响 / To</div><p class="lineage__list">{tos}</p></div>
    </div>
  </header>"""


def render_profile(data):
    paras = "".join(f"<p>{rich(p)}</p>" for p in data["intro"])
    return f"""<section class="block reveal" id="profile">
    <div class="block__head">
      <span class="block__num">01</span>
      <h2 class="block__title">语言档案<em>Dossier</em></h2>
      <span class="block__rule"></span>
    </div>
    <div class="prose">{paras}</div>
  </section>"""


def render_chain(data):
    chips = []
    for i, stage in enumerate(data["chain"], start=1):
        chips.append(
            f'<a class="stage-chip" href="#stage-{i}">'
            f'<span class="stage-chip__num">{i:02d}</span>'
            f'<span class="stage-chip__file">{e(stage["file"])}</span>'
            f'<span class="stage-chip__label">{e(stage["label"])}</span></a>'
        )
        if i != len(data["chain"]):
            chips.append('<span class="chain-arrow" aria-hidden="true">→</span>')

    cards = []
    for i, stage in enumerate(data["chain"], start=1):
        code = stage["code"].strip("\n")
        line_count = code.count("\n") + 1
        clamped = line_count > 20
        pre_class = "code is-clamped" if clamped else "code"
        expand = (
            '<button class="code-btn" type="button" data-expand '
            'aria-expanded="false">展开全部</button>'
            if clamped else ""
        )
        format_rows = "".join(
            f'<div class="format__row"><span class="format__key">{e(k)}</span>'
            f'<span class="format__val">{e(v)}</span></div>'
            for k, v in stage["format"]
        )
        cards.append(f"""<article class="stage-card reveal" id="stage-{i}">
      <header class="stage-card__head">
        <span class="stage-card__no">{i:02d}</span>
        <span class="stage-card__file">{e(stage["file"])}</span>
        <span class="stage-card__label">{e(stage["label"])}</span>
        <span class="stage-card__cmd">{e(stage["cmd"])}</span>
      </header>
      <div class="code-wrap">
        <div class="code-bar">
          <span class="code-bar__dots" aria-hidden="true"><i></i><i></i><i></i></span>
          <span class="code-bar__name">{e(stage["file"])}</span>
          <span class="code-bar__note">示意样例</span>
        </div>
        <pre class="{pre_class}" tabindex="0"><code>{e(code)}</code></pre>
        <div class="code-actions">
          <button class="code-btn" type="button" data-copy>复制</button>
          {expand}
          <span class="code-hint">文档重构 · 非实测输出</span>
        </div>
      </div>
      <div class="format">{format_rows}</div>
      <p class="stage-note">{rich(stage["note"])}</p>
    </article>""")

    return f"""<section class="block reveal" id="chain">
    <div class="block__head">
      <span class="block__num">02</span>
      <h2 class="block__title">产物链<em>Artifact Chain</em></h2>
      <span class="block__rule"></span>
    </div>
    <div class="chain-strip" aria-label="产物阶段导航">{"".join(chips)}</div>
    {"".join(cards)}
  </section>"""


def render_tools(data):
    rows = []
    for row in data["tools"]:
        cells = []
        for key in ("era", "editor", "compiler", "build", "pkg", "debug"):
            value = row.get(key, "—")
            cls = ' class="none"' if value == "—" else ""
            cells.append(f"<td{cls}>{e(value)}</td>")
        rows.append(f"<tr>{''.join(cells)}</tr>")

    return f"""<section class="block reveal" id="tools">
    <div class="block__head">
      <span class="block__num">03</span>
      <h2 class="block__title">工具链时间表<em>Toolchain</em></h2>
      <span class="block__rule"></span>
    </div>
    <div class="table-wrap">
      <table class="tools-table">
        <caption>编辑 → 编译 / 解释 → 构建 → 包 → 调试</caption>
        <thead><tr>
          <th scope="col">年代</th><th scope="col">编辑器</th>
          <th scope="col">编译器 / 解释器</th><th scope="col">构建</th>
          <th scope="col">包管理</th><th scope="col">调试</th>
        </tr></thead>
        <tbody>{"".join(rows)}</tbody>
      </table>
    </div>
    <p class="table-hint">表格可横向滑动 →</p>
  </section>"""


def render_hello(data, slug):
    hello = data["hello"]
    rows = "".join(
        f'<div class="footprint__row">'
        f'<span class="footprint__stage">{e(item["stage"])}</span>'
        f'<span class="footprint__track"><span class="footprint__fill" '
        f'data-w="{item["w"]}" style="width:{item["w"]}%"></span></span>'
        f'<span class="footprint__size">{e(item["size"])}</span></div>'
        for item in hello["footprint"]
    )
    why = "".join(f"<li>{item}</li>" for item in hello["why"])
    code = hello["code"].strip("\n")

    return f"""<section class="block reveal" id="hello">
    <div class="block__head">
      <span class="block__num">04</span>
      <h2 class="block__title">Hello World 追踪<em>Trace</em></h2>
      <span class="block__rule"></span>
    </div>
    <div class="hello-grid">
      <div class="hello-source">
        <div class="code-bar">
          <span class="code-bar__dots" aria-hidden="true"><i></i><i></i><i></i></span>
          <span class="code-bar__name">{e(hello["file"])}</span>
          <span class="code-bar__note">SOURCE</span>
        </div>
        <pre class="code" tabindex="0"><code>{e(code)}</code></pre>
        <div class="code-actions">
          <button class="code-btn" type="button" data-copy>复制</button>
          <span class="code-hint">与上方产物链同源</span>
        </div>
      </div>
      <div>
        <p class="footprint__title">体积与形态 · 对数尺度示意</p>
        <div class="footprint">{rows}</div>
        <ol class="why-list">{why}</ol>
      </div>
    </div>
    {verified_site.verified_block(slug)}
  </section>"""


def render_next_card(lang, next_lang):
    if next_lang:
        href = f"{next_lang['slug']}.html"
        label = "下一门 / Next"
        title = f"{next_lang['name']} · {next_lang['year']}"
    else:
        href = "../index.html"
        label = "馆藏 / Index"
        title = "返回总目录"
    return f"""<a class="next-card" href="{href}">
    <span><span class="next-card__label">{label}</span>
      <span class="next-card__title">{e(title)}</span></span>
    <span class="next-card__arrow" aria-hidden="true">→</span>
  </a>"""


# ------------------------------------------------------------------
# 语言页
# ------------------------------------------------------------------
def render_language_page(lang):
    slug = lang["slug"]
    data = DATA[slug]
    prev_lang, next_lang = neighbors(slug)
    fw_teaser = fw_site.render_teaser(lang, FRAMEWORKS.get(slug), SHORT.get(slug))
    deep_html = depth_site.render_deep(lang, DEEP[slug])

    prev_href = f"{prev_lang['slug']}.html" if prev_lang else "../index.html"
    next_href = f"{next_lang['slug']}.html" if next_lang else "../index.html"

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{ui.head_snippet()}
<title>{e(lang["name"])} — 产物链档案 · 语言产物链</title>
<meta name="description" content="{e(lang["name"])}（{lang["year"]}）的产物链档案：从源码、中间表示到最终产物，逐阶段给出文件内容与格式说明。">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body data-page="lang" data-prev="{prev_href}" data-next="{next_href}">
<a class="skip-link" href="#main">跳到正文</a>
<div class="progress" aria-hidden="true"><span></span></div>
<button class="menu-toggle" type="button" aria-label="打开目录" aria-expanded="false" aria-controls="catalog"><span></span></button>
<div class="scrim"></div>
{ui.font_ui()}
<button class="cmdk-btn" type="button" data-cmdk aria-label="全站搜索">搜索全站 <kbd>⌘K</kbd></button>
{render_catalog(slug, "../")}
<main class="page" id="main">
  <div class="page__inner">
    {render_page_nav(lang, prev_lang, next_lang)}
    {render_dossier(lang, data)}
    {render_profile(data)}
    {render_chain(data)}
    {render_tools(data)}
    {render_hello(data, slug)}
    {deep_html}
    {fw_teaser}
    {sources_site.lang_sources(slug)}
    {render_next_card(lang, next_lang)}
    <footer class="pagefoot">
      <p class="stamp">本页所有文件样例为依据公开规范与文档重构的示意内容；具体地址、偏移与字节数为示例值，不代表任何特定编译器版本的实测输出。</p>
      <p>{BATCH_LABEL} · PLATE {lang["plate"]:02d} / {TOTAL}</p>
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


# ------------------------------------------------------------------
# 首页
# ------------------------------------------------------------------
def render_index():
    by_era = {era["key"]: [] for era in ERAS}
    for lang in LANGUAGES:
        by_era[lang["era"]].append(lang)

    sections = []
    for idx, era in enumerate(ERAS, start=1):
        items = by_era[era["key"]]
        open_count = sum(1 for l in items if l["built"])
        cards = []
        for lang in items:
            search = search_blob(lang)
            if lang["built"]:
                cards.append(
                    f'<a class="lang-card is-open" href="langs/{lang["slug"]}.html" '
                    f'data-search="{search}" data-family="{lang["family"]}">'
                    f'<span class="lang-card__top"><span class="lang-card__name">'
                    f'{e(lang["name"])}</span><span class="lang-card__year">{lang["year"]}</span></span>'
                    f'<span class="lang-card__desc">{e(lang["desc"])}</span>'
                    f'<span class="lang-card__status">产物链 · {stage_count(lang["slug"])} 阶段</span></a>'
                )
            else:
                cards.append(
                    f'<div class="lang-card is-pending" data-search="{search}" '
                    f'data-family="{lang["family"]}">'
                    f'<span class="lang-card__top"><span class="lang-card__name">'
                    f'{e(lang["name"])}</span><span class="lang-card__year">{lang["year"]}</span></span>'
                    f'<span class="lang-card__desc">{e(lang["desc"])}</span>'
                    f'<span class="lang-card__status">待开放</span></div>'
                )
        sections.append(f"""<section class="era-section" data-era="{era["key"]}">
      <div class="era-head">
        <span class="era-head__num">{idx:02d}</span>
        <h2 class="era-head__title">{e(era["title"])}</h2>
        <span class="era-head__range">{e(era["range"])} · {e(era["label"])}</span>
        <span class="era-head__count">{open_count} / {len(items)} 已开放</span>
      </div>
      <div class="lang-grid">{"".join(cards)}</div>
    </section>""")

    legend = [
        ("01", "语言档案", "诞生背景、设计目标与谱系。"),
        ("02", "产物链", "每个阶段的文件内容、格式与生成命令。"),
        ("03", "工具链", "编辑器、编译器、构建、包管理与调试器的年代对照。"),
        ("04", "Hello World", "同一段程序在各阶段的体积与存在理由。"),
    ]
    legend_html = "".join(
        f'<div class="legend__item"><span class="legend__num">{n}</span>'
        f'<h3 class="legend__title">{e(t)}</h3><p class="legend__desc">{e(d)}</p></div>'
        for n, t, d in legend
    )

    filters = [
        ("all", "全部"),
        ("compiled", "编译型"),
        ("interpreted", "解释 / 字节码"),
        ("domain", "领域专用"),
        ("markup", "标记 / 配置"),
    ]
    filter_html = "".join(
        f'<button class="filter" type="button" data-filter="{key}" '
        f'aria-pressed="{"true" if key == "all" else "false"}">{label}</button>'
        for key, label in filters
    )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{ui.head_snippet()}
<title>语言产物链 — {TOTAL} 个条目 · {FRAMEWORK_CARDS} 个框架</title>
<meta name="description" content="从穿孔卡到 ELF，从 P-code 到 EVM 字节码：{TOTAL} 个语言与标记条目的产物链、文件格式、工具，以及 {FRAMEWORK_CARDS} 个框架的选型地图。">
<link rel="stylesheet" href="assets/style.css">
</head>
<body data-page="index">
<a class="skip-link" href="#main">跳到正文</a>
<div class="progress" aria-hidden="true"><span></span></div>
<button class="menu-toggle" type="button" aria-label="打开目录" aria-expanded="false" aria-controls="catalog"><span></span></button>
<div class="scrim"></div>
{ui.font_ui()}
<button class="cmdk-btn" type="button" data-cmdk aria-label="全站搜索">搜索全站 <kbd>⌘K</kbd></button>
{render_catalog(None, "")}
<main class="page" id="main">
  <div class="page__inner">
    <header class="hero">
      <p class="hero__kicker">An Archive of Programming Languages · 1950s — 2020s</p>
      <h1 class="hero__title">语言的<br><em>产物链</em></h1>
      <p class="hero__sub">从一张 80 列穿孔卡，到 ELF 的一个段；从 P-code 到 EVM 字节码。七十八门语言与标记，每一种都有一条可以逐阶段打开的产物链——源码、中间表示、目标文件、最终产物，以及它们身边的工具。</p>
      <div class="hero__meta">
        <div class="stat"><span class="stat__num">{TOTAL}</span><span class="stat__label">个条目</span></div>
        <div class="stat"><span class="stat__num">{FRAMEWORK_CARDS}</span><span class="stat__label">张决策卡</span></div>
        <div class="stat"><span class="stat__num">{len(SCENARIOS)}</span><span class="stat__label">个场景</span></div>
        <div class="stat"><span class="stat__num">{OPEN}</span><span class="stat__label">已开放</span></div>
        <div class="stat"><span class="stat__num">{BATCH_DONE}</span><span class="stat__label">当前批次</span></div>
      </div>
    </header>

    <div class="index-tools">
      <label class="index-search" for="indexSearch">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="7" cy="7" r="4.5"></circle><path d="M10.5 10.5 14 14"></path></svg>
        <input id="indexSearch" type="search" placeholder="搜索：语言名、年代、关键词（按 / 聚焦）" autocomplete="off" spellcheck="false" aria-label="搜索语言">
      </label>
      <div class="index-filters" role="group" aria-label="按实现方式筛选">{filter_html}</div>
      <a class="matrix-link" href="frameworks.html">框架场景矩阵 →</a>
      <a class="matrix-link" href="scenarios.html">开发场景 →</a>
      <a class="matrix-link matrix-link--ghost" href="security.html">安全专题</a>
      <a class="matrix-link matrix-link--ghost" href="sources.html">来源索引</a>
      <span class="era-head__count" id="indexCount">{OPEN} / {TOTAL} 门</span>
    </div>

    <section class="block reveal" id="howto">
      <div class="block__head">
        <span class="block__num">00</span>
        <h2 class="block__title">如何阅读<em>How to read</em></h2>
        <span class="block__rule"></span>
      </div>
      <div class="legend">{legend_html}</div>
      <p class="legend-note">每门语言页顶部的「框架与场景」与底部的第 06 板块，可进入该语言的框架决策卡；全站选型见上方「框架场景矩阵」。</p>
    </section>

    {"".join(sections)}

    <p class="index-empty">没有匹配的语言。试试「1972」「字节码」「Lisp」，或切换到「全部」。</p>

    <footer class="pagefoot">
      <p class="stamp">全站样例为依据公开规范与文档重构的示意内容；具体地址、偏移与字节数为示例值。全站 {OPEN} 个条目已全部开放。</p>
      <p>语言产物链档案 · {BATCH_LABEL}</p>
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


def render_404():
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{ui.head_snippet()}
<title>404 — 这一页不在馆藏里</title>
<meta name="description" content="页面不存在。返回目录、框架矩阵、产物格式索引或来源索引继续浏览。">
<link rel="stylesheet" href="assets/style.css">
</head>
<body data-page="notfound">
<a class="skip-link" href="#main">跳到正文</a>
<div class="progress" aria-hidden="true"><span></span></div>
<button class="menu-toggle" type="button" aria-label="打开目录" aria-expanded="false" aria-controls="catalog"><span></span></button>
<div class="scrim"></div>
{ui.font_ui()}
<button class="cmdk-btn" type="button" data-cmdk aria-label="全站搜索">搜索全站 <kbd>⌘K</kbd></button>
{render_catalog(None, "")}
<main class="page" id="main">
  <div class="page__inner">
    <header class="hero">
      <p class="hero__kicker">ERROR 404 · 未找到</p>
      <h1 class="hero__title">这一页<br><em>不在馆藏里</em></h1>
      <p class="hero__sub">地址可能写错了，或者这条展签还没开放。可以从下面几个入口继续。</p>
    </header>
    <section class="block reveal" id="where">
      <div class="block__head">
        <span class="block__num">00</span>
        <h2 class="block__title">继续浏览<em>Where to go</em></h2>
        <span class="block__rule"></span>
      </div>
      <div class="fw-grid">
        <a class="stack-card" href="index.html"><span class="stack-top"><span class="stack-lang">INDEX</span><span class="stack-type">目录</span></span><span class="stack-fw">语言的产物链</span><span class="stack-why">78 个条目，按年代与家族浏览。</span></a>
        <a class="stack-card" href="frameworks.html"><span class="stack-top"><span class="stack-lang">MATRIX</span><span class="stack-type">选型</span></span><span class="stack-fw">框架场景矩阵</span><span class="stack-why">{len(SCENARIOS)} 个场景，{sum(len(sc["entries"]) for sc in SCENARIOS)} 组推荐。</span></a>
        <a class="stack-card" href="scenarios.html"><span class="stack-top"><span class="stack-lang">SCENARIOS</span><span class="stack-type">分类</span></span><span class="stack-fw">开发场景</span><span class="stack-why">{len(dev_scenarios.SCENARIOS)} 个开发场景 × {sum(len(s["architectures"]) for s in dev_scenarios.SCENARIOS)} 个架构组合。</span></a>
        <a class="stack-card" href="security.html"><span class="stack-top"><span class="stack-lang">SECURITY</span><span class="stack-type">专题</span></span><span class="stack-fw">安全专题</span><span class="stack-why">{len(security.TOOLS)} 个工具，从编码到审计。</span></a>
        <a class="stack-card" href="formats.html"><span class="stack-top"><span class="stack-lang">FORMATS</span><span class="stack-type">索引</span></span><span class="stack-fw">产物格式索引</span><span class="stack-why">42 种格式反查语言与阶段。</span></a>
        <a class="stack-card" href="sources.html"><span class="stack-top"><span class="stack-lang">SOURCES</span><span class="stack-type">引用</span></span><span class="stack-fw">来源索引</span><span class="stack-why">220 条官方来源，可搜索。</span></a>
      </div>
    </section>
    <footer class="pagefoot">
      <p class="stamp">如果是从站内链接过来的，说明有一个链接写错了；可以用 ⌘K 搜索或回到目录。</p>
      <p>404 · 语言产物链</p>
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


def inject_meta(path):
    """注入 favicon 与 OG/Twitter 元数据；重复运行不会重复插入。"""
    s = path.read_text(encoding="utf-8")
    if 'property="og:title"' in s:
        return
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    title = m.group(1).strip() if m else "语言的产物链"
    m = re.search(r'<meta name="description" content="([^"]*)"', s)
    desc = m.group(1) if m else "编程语言与框架的产物链档案"
    root = "../" if path.parent.name == "langs" else ""
    tags = f"""<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#f3ede1">
<meta property="og:type" content="website">
<meta property="og:locale" content="zh_CN">
<meta property="og:site_name" content="语言的产物链">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{root}assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{root}assets/og.png">
"""
    s = s.replace("</head>", tags + "</head>", 1)
    path.write_text(s, encoding="utf-8")


# ------------------------------------------------------------------
# 数据与校验
# ------------------------------------------------------------------
ALIASES = {
    "javascript": ["js", "es6", "node"],
    "typescript": ["ts"],
    "python": ["py"],
    "kubernetes": ["k8s"],
    "yaml": ["k8s", "kubectl", "helm", "ci"],
    "html": ["h5", "web"],
    "css": ["scss", "样式"],
    "postgresql": ["pg"],
    "csharp": ["c#", "dotnet", ".net"],
    "cpp": ["c++"],
    "fsharp": ["f#"],
    "objectivec": ["objc", "ios"],
    "swift": ["ios", "macos"],
    "kotlin": ["android"],
    "dart": ["flutter"],
    "rust": ["cargo"],
    "go": ["golang"],
    "ruby": ["rails"],
    "php": ["laravel"],
    "markdown": ["md"],
}


def write_search_js():
    """生成全局搜索索引：语言 / 框架 / 格式 / 场景 / 工具页。"""
    items = []
    fw_names = {}
    for slug, detail in FRAMEWORKS.items():
        for card in detail["cards"]:
            fw_names.setdefault(slug, []).append(card["name"])

    for l in LANGUAGES:
        slug = l["slug"]
        items.append({
            "title": l["name"], "group": l["cn"] or "语言",
            "desc": f"{l['cn']} · {l['year']} · 语言档案与产物链",
            "href": f"langs/{slug}.html", "kind": "语言",
            "keywords": [l["cn"], str(l["year"]), l["desc"], l["family_label"], slug]
                        + ALIASES.get(slug, []),
        })
        detail = FRAMEWORKS.get(slug)
        if detail:
            items.append({
                "title": f"{l['name']} · 框架与场景", "group": "框架",
                "desc": detail["summary"],
                "href": f"langs/{slug}-frameworks.html", "kind": "框架页",
                "keywords": fw_names.get(slug, []) + detail["scenarios"] + [l["name"]],
            })
            for card in detail["cards"]:
                items.append({
                    "title": card["name"], "group": "框架",
                    "desc": f"{card['type']} · {l['name']} · {card['tagline']}",
                    "href": f"langs/{slug}-frameworks.html#{_slugify(card['name'])}",
                    "kind": "决策卡",
                    "keywords": [l["name"], l["cn"], card["type"], card["maintainer"], card["tagline"]],
                })

    fmt_index_data = formats.build(DATA)
    for f in fmt_index_data:
        items.append({
            "title": f["name"], "group": "产物格式",
            "desc": f["desc"] + f"（{len(f['langs'])} 门语言）",
            "href": f"formats.html#{f['key']}", "kind": "格式",
            "keywords": f["langs"] + [f["desc"], "格式", "artifact"],
        })

    for sc in SCENARIOS:
        page = sc.get("page", "frameworks.html")
        items.append({
            "title": sc["title"], "group": "场景",
            "desc": sc["desc"],
            "href": f"{page}#{sc['key']}", "kind": "场景",
            "keywords": [entry[1] for entry in sc["entries"]] + [entry[2] for entry in sc["entries"]],
        })
        for slug, fw, why in sc["entries"]:
            if sc.get("page"):
                tool = next((t for t in security.TOOLS if t["name"] == fw), None)
                href = f"{page}#{tool['slug'] if tool else _slugify(fw)}"
            else:
                href = f"langs/{slug}-frameworks.html"
            items.append({
                "title": f"{sc['title']} · {fw}", "group": "场景",
                "desc": f"{why}",
                "href": href, "kind": "场景推荐",
                "keywords": [sc["title"], fw, slug, why],
            })

    for tool in security.TOOLS:
        items.append({
            "title": tool["name"], "group": "安全",
            "desc": f"{tool['category']} · {tool['lang']} · {tool['summary']}",
            "href": f"security.html#{tool['slug']}", "kind": "安全工具",
            "keywords": [tool["lang"], tool["category"], tool["license"], tool["summary"]]
                        + tool["fit"],
        })

    for sc in dev_scenarios.SCENARIOS:
        items.append({
            "title": f"开发场景 · {sc['title']}", "group": "开发场景",
            "desc": sc["desc"],
            "href": f"scenarios.html#dev-{sc['key']}", "kind": "开发场景",
            "keywords": [sc["title"], sc["en"]]
                        + [a["title"] for a in sc["architectures"]],
        })
        for arch in sc["architectures"]:
            items.append({
                "title": f"{sc['title']} · {arch['title']}", "group": "开发场景",
                "desc": arch["desc"],
                "href": f"scenarios.html#dev-{sc['key']}", "kind": "架构组合",
                "keywords": [sc["title"], arch["title"]]
                            + [entry[1] for entry in arch["entries"]],
            })

    for title, href, desc in (
        ("框架场景矩阵", "frameworks.html", "按场景反查语言与框架"),
        ("开发场景", "scenarios.html", "按开发场景 × 架构模式浏览语言与框架"),
        ("安全专题", "security.html", "应用安全、密码学、供应链与审计"),
        ("来源索引", "sources.html", "220 条官方来源"),
        ("产物格式索引", "formats.html", "按格式反查语言与阶段"),
        ("语言谱系图", "lineage.html", "影响关系与时间轴"),
        ("对比器", "compare.html", "并排对比语言与框架"),
        ("实测记录", "verified.html", "本机真正跑通的 Hello 产物链"),
    ):
        items.append({
            "title": title, "group": "页面", "desc": desc,
            "href": href, "kind": "索引", "keywords": [desc],
        })

    payload = {"items": items}
    text = "window.ARCHIVE_SEARCH = " + json.dumps(payload, ensure_ascii=False) + ";\n"
    (ROOT / "assets" / "search-index.js").write_text(text, encoding="utf-8")
    return len(items)


def _slugify(value):
    return re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-") or "item"


def write_compare_js():
    langs = []
    for l in BUILT:
        deep = DEEP[l["slug"]]
        langs.append({
            "slug": l["slug"], "name": l["name"], "cn": l["cn"],
            "year": l["year"], "family_label": l["family_label"],
            "deep": deep,
        })
    cards = []
    for slug, detail in FRAMEWORKS.items():
        lang = language_by_slug(slug)
        for card in detail["cards"]:
            m = fw_meta.META.get((slug, card["name"]), {})
            cards.append({
                "slug": slug, "lang": lang["name"], "name": card["name"],
                "anchor": _slugify(card["name"]), "year": card["year"],
                "type": card["type"], "tagline": card["tagline"],
                "fit": card["fit"], "avoid": card["avoid"], "chain": card["chain"],
                "projects": card["projects"], "alternatives": card["alternatives"],
                "division": card["division"],
                "learn": m.get("learn", "—"), "eco": m.get("eco", "—"),
                "license": m.get("license", "—"),
            })
    payload = {"languages": langs, "frameworks": cards}
    text = "window.ARCHIVE_COMPARE = " + json.dumps(payload, ensure_ascii=False) + ";\n"
    (ROOT / "assets" / "compare-data.js").write_text(text, encoding="utf-8")
    return len(langs), len(cards)


def write_data_js():
    payload = {
        "total": TOTAL,
        "open": OPEN,
        "batch": BATCH_DONE,
        "frameworks": FRAMEWORK_CARDS,
        "scenarios": len(SCENARIOS),
        "dev_scenarios": len(dev_scenarios.SCENARIOS),
        "security_tools": len(security.TOOLS),
        "languages": [
            {
                "plate": l["plate"],
                "slug": l["slug"],
                "name": l["name"],
                "cn": l["cn"],
                "year": l["year"],
                "era": l["era"],
                "family": l["family"],
                "built": l["built"],
                "desc": l["desc"],
                "stages": stage_count(l["slug"]) if l["built"] else None,
            }
            for l in LANGUAGES
        ],
    }
    text = "window.ARCHIVE = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n"
    (ROOT / "assets" / "data.js").write_text(text, encoding="utf-8")


def validate():
    errors = []

    missing = [l["slug"] for l in BUILT if l["slug"] not in DATA]
    if missing:
        errors.append("built 但缺数据：" + ", ".join(missing))

    extra = [s for s in DATA if s not in BUILT_SLUGS]
    if extra:
        errors.append("有数据但未标记 built：" + ", ".join(extra))

    for slug, data in DATA.items():
        lang = language_by_slug(slug)
        for field in ("tagline", "intro", "lineage", "chain", "tools", "hello"):
            if field not in data:
                errors.append(f"{slug}: 缺少字段 {field}")
        if len(data["chain"]) < 3:
            errors.append(f"{slug}: 产物链少于 3 个阶段")
        for i, stage in enumerate(data["chain"], 1):
            for field in ("label", "file", "cmd", "code", "format", "note"):
                if field not in stage:
                    errors.append(f"{slug} stage {i}: 缺少 {field}")

    if len(LANGUAGES) != 78:
        errors.append(f"条目总数 {len(LANGUAGES)} ≠ 78")

    missing_fw = [
        l["slug"] for l in BUILT
        if l["slug"] not in FRAMEWORKS and l["slug"] not in SHORT
    ]
    if missing_fw:
        errors.append("缺少框架数据：" + ", ".join(missing_fw))

    for slug, detail in FRAMEWORKS.items():
        for field in ("summary", "scenarios", "picks", "cards"):
            if field not in detail:
                errors.append(f"{slug} 框架: 缺少 {field}")
        if not (2 <= len(detail["cards"]) <= 4):
            errors.append(f"{slug} 框架: 卡片数 {len(detail['cards'])} 不在 2–4")
        names = [c["name"] for c in detail["cards"]]
        for need, pick, _why in detail["picks"]:
            if pick not in names:
                errors.append(f"{slug} 框架: 选型推荐 {pick} 无对应卡片")
        for card in detail["cards"]:
            for field in ("name", "year", "type", "maintainer", "tagline",
                          "fit", "avoid", "chain", "projects", "alternatives", "division"):
                if field not in card:
                    errors.append(f"{slug}/{card.get('name', '?')}: 缺少 {field}")
            if (slug, card.get("name")) not in fw_meta.META:
                errors.append(f"{slug}/{card.get('name', '?')}: 缺少框架元信息")

    for slug, short in SHORT.items():
        for field in ("summary", "tools", "when"):
            if field not in short:
                errors.append(f"{slug} 短页: 缺少 {field}")

    missing_deep = [slug for slug in BUILT_SLUGS if slug not in DEEP]
    if missing_deep:
        errors.append("缺少语言深读：" + ", ".join(missing_deep))
    missing_src = [slug for slug in BUILT_SLUGS if slug not in sources.LANG]
    if missing_src:
        errors.append("缺少语言来源：" + ", ".join(missing_src))
    for slug, detail in FRAMEWORKS.items():
        for card in detail["cards"]:
            if (slug, card["name"]) not in sources.FW:
                errors.append(f"缺少框架来源：{slug}/{card['name']}")

    for slug, deep in DEEP.items():
        for field in ("goals", "tradeoffs", "features", "timeline",
                      "projects", "packages", "compare", "status"):
            if field not in deep:
                errors.append(f"{slug} 深读: 缺少 {field}")
        if len(deep.get("features", {})) != 4:
            errors.append(f"{slug} 深读: features 不是 4 项")

    security_names = {t["name"] for t in security.TOOLS}
    for sc in SCENARIOS:
        for slug, fw_name, _why in sc["entries"]:
            if slug not in BUILT_SLUGS:
                errors.append(f"矩阵场景 {sc['key']} 引用未知语言 {slug}")
            elif sc.get("page"):
                if fw_name not in security_names:
                    errors.append(f"矩阵场景 {sc['key']} 引用未知安全工具 {fw_name}")
            elif slug in FRAMEWORKS:
                names = [c["name"] for c in FRAMEWORKS[slug]["cards"]]
                if fw_name not in names:
                    errors.append(f"矩阵场景 {sc['key']} 引用未知框架 {slug}/{fw_name}")

    for sc in dev_scenarios.SCENARIOS:
        if not sc.get("architectures"):
            errors.append(f"开发场景 {sc['key']} 缺少架构模式")
        for arch in sc["architectures"]:
            if not arch.get("entries"):
                errors.append(f"开发场景 {sc['key']}/{arch['key']} 缺少条目")
            for entry in arch["entries"]:
                slug, fw_name = entry[0], entry[1]
                explicit = entry[3] if len(entry) > 3 else ""
                if slug not in BUILT_SLUGS:
                    errors.append(f"开发场景 {sc['key']}/{arch['key']} 引用未知语言 {slug}")
                elif explicit:
                    target, _, frag = explicit.partition("#")
                    if target != "security.html":
                        errors.append(f"开发场景 {sc['key']} 引用未知目标 {explicit}")
                    elif frag not in {t["slug"] for t in security.TOOLS}:
                        errors.append(f"开发场景 {sc['key']} 引用未知安全锚点 {frag}")
                elif slug in FRAMEWORKS:
                    names = [c["name"] for c in FRAMEWORKS[slug]["cards"]]
                    if fw_name not in names:
                        errors.append(
                            f"开发场景 {sc['key']}/{arch['key']} 引用未知框架 {slug}/{fw_name}"
                        )
                elif slug in SHORT:
                    if fw_name not in SHORT[slug]["tools"]:
                        errors.append(
                            f"开发场景 {sc['key']}/{arch['key']} 引用未知短页工具 {slug}/{fw_name}"
                        )

    return errors


def link_check():
    """检查生成页面中的相对链接是否都指向实际文件。"""
    problems = []
    pages = list((ROOT / "langs").glob("*.html")) + [
        ROOT / "index.html", ROOT / "frameworks.html", ROOT / "sources.html",
        ROOT / "formats.html", ROOT / "lineage.html", ROOT / "compare.html",
        ROOT / "verified.html", ROOT / "security.html", ROOT / "scenarios.html",
        ROOT / "404.html",
    ]
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for href in re.findall(r'href="([^"#]+)"', text):
            if href.startswith(("http://", "https://", "mailto:", "data:")):
                continue
            target = (page.parent / href).resolve()
            if not target.exists():
                problems.append(f"{page.relative_to(ROOT)} → {href}")
    return problems


def main():
    errors = validate()
    if errors:
        print("校验失败：")
        for err in errors:
            print("  -", err)
        sys.exit(1)

    (ROOT / "langs").mkdir(exist_ok=True)
    (ROOT / "assets").mkdir(exist_ok=True)

    for lang in BUILT:
        out = ROOT / "langs" / f"{lang['slug']}.html"
        out.write_text(render_language_page(lang), encoding="utf-8")
        fw_out = ROOT / "langs" / f"{lang['slug']}-frameworks.html"
        fw_out.write_text(
            fw_site.render_page(
                lang,
                FRAMEWORKS.get(lang["slug"]),
                SHORT.get(lang["slug"]),
                render_catalog(lang["slug"], "../"),
                TOTAL,
                BATCH_LABEL,
            ),
            encoding="utf-8",
        )

    (ROOT / "index.html").write_text(render_index(), encoding="utf-8")
    lineage_map = {}
    for lang in BUILT:
        lineage_map[lang["slug"]] = {
            "from": DATA[lang["slug"]]["lineage"]["from"],
            "to": DATA[lang["slug"]]["lineage"]["to"],
        }
    (ROOT / "lineage.html").write_text(
        lineage.render_page(
            BUILT, ERAS, lineage_map, render_catalog(None, ""), BATCH_LABEL, BATCH_DONE, TOTAL,
        ),
        encoding="utf-8",
    )
    (ROOT / "verified.html").write_text(
        verified_site.render_verified_page(
            {l["slug"]: l for l in BUILT}, render_catalog(None, ""), BATCH_LABEL, BATCH_DONE,
        ),
        encoding="utf-8",
    )
    (ROOT / "compare.html").write_text(
        compare_index.render_compare(
            render_catalog(None, ""), BATCH_LABEL, BATCH_DONE, len(BUILT), FRAMEWORK_CARDS,
        ),
        encoding="utf-8",
    )
    (ROOT / "formats.html").write_text(
        fmt_index.render_formats(
            DATA, {l["slug"]: l for l in BUILT}, render_catalog(None, ""),
            BATCH_LABEL, BATCH_DONE, len(BUILT),
        ),
        encoding="utf-8",
    )
    (ROOT / "sources.html").write_text(
        src_index.render_sources_index(
            BUILT, render_catalog(None, ""), BATCH_LABEL,
        ),
        encoding="utf-8",
    )
    (ROOT / "404.html").write_text(render_404(), encoding="utf-8")
    (ROOT / "frameworks.html").write_text(
        fw_site.render_matrix(
            FRAMEWORKS,
            SHORT,
            SCENARIOS,
            render_catalog(None, ""),
            TOTAL,
            FRAMEWORK_CARDS,
            BATCH_LABEL,
        ),
        encoding="utf-8",
    )
    (ROOT / "security.html").write_text(
        security_site.render_security(render_catalog(None, ""), BATCH_LABEL),
        encoding="utf-8",
    )
    (ROOT / "scenarios.html").write_text(
        scenario_site.render_scenarios(render_catalog(None, ""), FRAMEWORKS, BATCH_LABEL),
        encoding="utf-8",
    )
    write_data_js()
    cmp_langs, cmp_cards = write_compare_js()
    search_count = write_search_js()

    all_pages = [ROOT / "index.html", ROOT / "frameworks.html",
                 ROOT / "sources.html", ROOT / "formats.html",
                 ROOT / "lineage.html", ROOT / "compare.html",
                 ROOT / "verified.html", ROOT / "security.html",
                 ROOT / "scenarios.html", ROOT / "404.html"]
    all_pages += sorted((ROOT / "langs").glob("*.html"))
    for page in all_pages:
        inject_meta(page)

    problems = link_check()
    print(f"已生成：{len(BUILT)} 个语言页 + {len(BUILT)} 个框架页 + 矩阵 + 来源索引 + 格式索引 + 谱系图 + 首页")
    print(f"产物阶段总数：{sum(stage_count(l['slug']) for l in BUILT)}")
    print(f"框架决策卡：{FRAMEWORK_CARDS} · 场景：{len(SCENARIOS)}")
    print(f"全局搜索索引：{search_count} 条 · 产物格式：{len(formats.build(DATA))} 种")
    print(f"对比数据：{cmp_langs} 语言 · {cmp_cards} 框架")
    print(f"实测记录：{len(verified.VERIFIED)} 门语言")
    if problems:
        print("链接问题：")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("链接检查：通过")


if __name__ == "__main__":
    main()

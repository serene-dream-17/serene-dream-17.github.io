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
from data import dev_scenarios, stacks  # noqa: E402
import fw_site  # noqa: E402
import ui  # noqa: E402
import depth_site  # noqa: E402
import sources_site  # noqa: E402
import src_index  # noqa: E402
import fmt_index  # noqa: E402
import verified_site  # noqa: E402
import scenario_site  # noqa: E402
import stack_site  # noqa: E402
import frameworks_index  # noqa: E402
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
FRAMEWORK_CARDS = sum(len(d["cards"]) for d in FRAMEWORKS.values())
scenario_site.ALL_LANGS = LANGUAGES
stack_site.ALL_LANGS = LANGUAGES
stack_site.FRAMEWORKS = FRAMEWORKS

# 三级目录
LANG_DIR = "languages"
FW_DIR = "frameworks"
STACK_DIR = "stacks"

DEEP = {}
for _mod in (depth_1, depth_2, depth_3):
    DEEP.update(_mod.DEEP)

BATCH_DONE = 23
BATCH_LABEL = "第 1–23 批"
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


def render_catalog(active_slug, root, lang_index=None):
    """侧栏目录。lang_index 用于语言目录自身页面（同目录跳转）。"""
    lang_href = lang_index or f"{root}{LANG_DIR}/index.html"
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
                    f'<li><a class="catalog__link {status}" href="{root}{LANG_DIR}/'
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
  <nav class="catalog__levels" aria-label="层级导航">
    <a href="{lang_href}">编程语言</a>
    <a href="{root}{FW_DIR}/index.html">框架</a>
    <a href="{root}{STACK_DIR}/index.html">技术栈</a>
  </nav>
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
    <a href="{root}index.html">← 首页</a><br>
    <a href="{lang_href}">编程语言 →</a><br>
    <a href="{root}{FW_DIR}/index.html">框架 →</a><br>
    <a href="{root}{STACK_DIR}/index.html">技术栈 →</a><br>
    <a href="{root}scenarios.html">开发场景 →</a><br>
    <a href="{root}{LANG_DIR}/formats.html">产物索引 →</a><br>
    <a href="{root}sources.html">来源索引 →</a><br>
    <a href="{root}verified.html">实测记录 →</a>
  </div>
</aside>"""


def render_page_nav(lang, prev_lang, next_lang):
    if prev_lang:
        prev_href = f"{prev_lang['slug']}.html"
        prev_text = f'<a class="plate-nav__link" href="{prev_href}">← <span>{e(prev_lang["name"])}</span></a>'
    else:
        prev_href = "index.html"
        prev_text = f'<a class="plate-nav__link" href="{prev_href}">← <span>语言总览</span></a>'

    if next_lang:
        next_href = f"{next_lang['slug']}.html"
        next_text = f'<a class="plate-nav__link" href="{next_href}"><span>{e(next_lang["name"])}</span> →</a>'
    else:
        next_href = "index.html"
        next_text = f'<a class="plate-nav__link" href="{next_href}"><span>语言总览</span> →</a>'

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
    <a class="dossier__fwlink" href="../frameworks/{lang["slug"]}.html">框架与场景 →</a>
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
        href = "index.html"
        label = "语言总览 / Index"
        title = "返回语言总览"
    return f"""<a class="next-card" href="{href}">
    <span><span class="next-card__label">{label}</span>
      <span class="next-card__title">{e(title)}</span></span>
    <span class="next-card__arrow" aria-hidden="true">→</span>
  </a>"""


# ------------------------------------------------------------------
# 语言页
# ------------------------------------------------------------------
def stacks_for(slug, name=None):
    """引用某语言（或某框架卡）的技术栈。"""
    hits = []
    for st in stacks.STACKS:
        for layer in st["layers"]:
            for item in layer["items"]:
                if not isinstance(item, tuple) or item[0] != slug:
                    continue
                if name is None or item[1] == name:
                    hits.append(st)
                    break
            else:
                continue
            break
    return hits


def render_stack_links(items, root="../"):
    if not items:
        return ""
    cards = "".join(
        f'<a class="stack-card" href="{root}{STACK_DIR}/{e(st["key"])}.html">'
        f'<span class="stack-top"><span class="stack-lang">{e(next(d["title"] for d in stacks.DOMAINS if d["key"] == st["domain"]))}</span>'
        f'<span class="stack-type">技术栈</span></span>'
        f'<span class="stack-fw">{e(st["title"])}</span>'
        f'<span class="stack-why">{e(st["summary"])}</span></a>'
        for st in items
    )
    return f"""<section class="block reveal" id="stacks">
    <div class="block__head">
      <span class="block__num">07</span>
      <h2 class="block__title">用到它的技术栈<em>Stacks</em></h2>
      <span class="block__rule"></span>
    </div>
    <div class="stack-grid">{cards}</div>
  </section>"""


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
<body data-page="lang" data-root="../" data-prev="{prev_href}" data-next="{next_href}">
<a class="skip-link" href="#main">跳到正文</a>
<div class="progress" aria-hidden="true"><span></span></div>
<button class="menu-toggle" type="button" aria-label="打开目录" aria-expanded="false" aria-controls="catalog"><span></span></button>
<div class="scrim"></div>
{ui.font_ui()}
<button class="cmdk-btn" type="button" data-cmdk aria-label="全站搜索">搜索全站 <kbd>⌘K</kbd></button>
{render_catalog(slug, "../", "index.html")}
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
    {render_stack_links(stacks_for(slug))}
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
PIPELINE = [
    {
        "num": "01", "title": "源码", "en": "Source",
        "desc": "源文件、编码与入口约定。语言在这里只决定了语法与文件后缀，真正的产物链从下一步开始。",
        "formats": [],
        "langs": ["c", "python", "javascript", "java", "rust"],
    },
    {
        "num": "02", "title": "前端分析", "en": "Parse & Check",
        "desc": "词法、语法与语义分析生成抽象语法树；类型检查与宏展开通常也在这一层完成。",
        "formats": [],
        "langs": ["rust", "typescript", "haskell", "swift"],
    },
    {
        "num": "03", "title": "中间表示", "en": "Intermediate",
        "desc": "IR 是优化与跨平台的分界线：LLVM IR、CIL、SIL / MIR、字节码与 WASM 都在这一层。",
        "formats": ["llvm", "cil", "mir", "class", "pyc", "beam", "wasm"],
        "langs": ["rust", "csharp", "swift", "java", "python", "elixir"],
    },
    {
        "num": "04", "title": "目标文件", "en": "Object",
        "desc": "面向具体平台的目标文件：ELF、PE / COFF、.o、a.out，以及 Android 的 DEX。",
        "formats": ["elf", "exe-pe", "aout", "dex"],
        "langs": ["c", "cpp", "zig", "go", "kotlin"],
    },
    {
        "num": "05", "title": "链接与打包", "en": "Link & Package",
        "desc": "链接器与打包器把目标文件组合成可发布单位：可执行、静态库、JAR、APK / IPA、镜像。",
        "formats": ["static", "jar", "apk", "ipa", "image", "langpkg"],
        "langs": ["go", "java", "dart", "swift", "smalltalk"],
    },
    {
        "num": "06", "title": "运行时与加载", "en": "Runtime",
        "desc": "加载器、虚拟机与运行时决定产物如何被执行：JVM、CLR、BEAM、CPython、WASM runtime。",
        "formats": ["wasm"],
        "langs": ["java", "csharp", "erlang", "python", "rust"],
    },
]


def _pipeline_html():
    lang_by_slug = {l["slug"]: l for l in LANGUAGES}
    stages = []
    for stage in PIPELINE:
        fmt = " · ".join(
            f'<a href="formats.html#{key}">{key}</a>' for key in stage["formats"]
        ) or "—"
        langs = " · ".join(
            f'<a href="{slug}.html">{e(lang_by_slug[slug]["name"])}</a>'
            for slug in stage["langs"] if slug in lang_by_slug
        )
        stages.append(f"""<article class="pipe-stage">
        <div class="pipe-stage__head"><span class="pipe-stage__num">{stage["num"]}</span>
          <h3 class="pipe-stage__title">{e(stage["title"])}<em>{e(stage["en"])}</em></h3></div>
        <p class="pipe-stage__desc">{e(stage["desc"])}</p>
        <p class="pipe-stage__links"><b>产物格式</b> {fmt}</p>
        <p class="pipe-stage__links"><b>代表语言</b> {langs}</p>
      </article>""")
    return f"""<section class="block reveal" id="pipeline">
      <div class="block__head">
        <span class="block__num">00</span>
        <h2 class="block__title">编译管线与产物<em>Pipeline</em></h2>
        <span class="block__rule"></span>
      </div>
      <p class="prose">同一段代码在不同语言里会走出不同的路径：有的停在字节码，有的直接生成机器码。下面六段是共同的骨架，每段给出典型产物格式与代表语言。</p>
      <div class="pipeline">{"".join(stages)}</div>
    </section>"""


def render_language_index():
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
                    f'<a class="lang-card is-open" href="{lang["slug"]}.html" '
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
<title>编程语言 — 编译管线与产物链 · {TOTAL} 个条目</title>
<meta name="description" content="从源码到中间表示、目标文件与运行时：{TOTAL} 个语言与标记条目的编译产物链，以及 {FRAMEWORK_CARDS} 个框架的入口。">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body data-page="index" data-root="../">
<a class="skip-link" href="#main">跳到正文</a>
<div class="progress" aria-hidden="true"><span></span></div>
<button class="menu-toggle" type="button" aria-label="打开目录" aria-expanded="false" aria-controls="catalog"><span></span></button>
<div class="scrim"></div>
{ui.font_ui()}
<button class="cmdk-btn" type="button" data-cmdk aria-label="全站搜索">搜索全站 <kbd>⌘K</kbd></button>
{render_catalog(None, "../", "index.html")}
<main class="page" id="main">
  <div class="page__inner">
    <nav class="plate-nav" aria-label="层级导航">
      <a class="plate-nav__link" href="../index.html">← <span>首页</span></a>
      <span class="plate-nav__counter">LANGUAGES · {TOTAL}</span>
      <a class="plate-nav__link" href="../frameworks/index.html"><span>框架总览</span> →</a>
    </nav>
    <header class="hero">
      <p class="hero__kicker">Programming Languages · Compilation Pipeline</p>
      <h1 class="hero__title">语言与<br><em>产物链</em></h1>
      <p class="hero__sub">从一张 80 列穿孔卡，到 ELF 的一个段；从 P-code 到 EVM 字节码。七十八门语言与标记，每一种都有一条可以逐阶段打开的产物链——源码、中间表示、目标文件、最终产物，以及它们身边的工具。</p>
      <div class="hero__meta">
        <div class="stat"><span class="stat__num">{TOTAL}</span><span class="stat__label">个条目</span></div>
        <div class="stat"><span class="stat__num">{FRAMEWORK_CARDS}</span><span class="stat__label">张决策卡</span></div>
        <div class="stat"><span class="stat__num">{len(stacks.STACKS)}</span><span class="stat__label">个技术栈</span></div>
        <div class="stat"><span class="stat__num">{OPEN}</span><span class="stat__label">已开放</span></div>
        <div class="stat"><span class="stat__num">{BATCH_DONE}</span><span class="stat__label">当前批次</span></div>
      </div>
    </header>

    {_pipeline_html()}

    <div class="index-tools">
      <label class="index-search" for="indexSearch">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="7" cy="7" r="4.5"></circle><path d="M10.5 10.5 14 14"></path></svg>
        <input id="indexSearch" type="search" placeholder="搜索：语言名、年代、关键词（按 / 聚焦）" autocomplete="off" spellcheck="false" aria-label="搜索语言">
      </label>
      <div class="index-filters" role="group" aria-label="按实现方式筛选">{filter_html}</div>
      <a class="matrix-link" href="../frameworks/index.html">框架总览 →</a>
      <a class="matrix-link" href="../stacks/index.html">技术栈 →</a>
      <a class="matrix-link matrix-link--ghost" href="../scenarios.html">开发场景</a>
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
<script src="../assets/font.js"></script>
<script src="../assets/data.js"></script>
<script src="../assets/search-index.js"></script>
<script src="../assets/app.js"></script>
<script src="../assets/search.js"></script>
</body>
</html>
"""


def render_home():
    cards = [
        ("LANGUAGES", "编程语言", f"{TOTAL} 个条目", "编译管线、产物链与年代谱系。", f"{LANG_DIR}/index.html"),
        ("FRAMEWORKS", "框架", f"{FRAMEWORK_CARDS} 张决策卡", "按语言与类型浏览，含适用与最小产物链。", f"{FW_DIR}/index.html"),
        ("STACKS", "技术栈", f"{len(stacks.STACKS)} 个组合", "语言 + 框架 + 数据与部署的落地搭配。", f"{STACK_DIR}/index.html"),
    ]
    card_html = "".join(
        f'<a class="home-door" href="{href}"><span class="home-door__kicker">{kicker}</span>'
        f'<span class="home-door__title">{title}</span>'
        f'<span class="home-door__num">{num}</span>'
        f'<span class="home-door__desc">{desc}</span>'
        f'<span class="home-door__arrow" aria-hidden="true">→</span></a>'
        for kicker, title, num, desc, href in cards
    )
    topics = [
        ("SCENARIOS", "开发场景", f"{len(dev_scenarios.SCENARIOS)} 个场景 · {sum(len(s['architectures']) for s in dev_scenarios.SCENARIOS)} 个架构分组", "scenarios.html"),
        ("FORMATS", "产物索引", "42 种格式反查 + 320 个阶段产物总表", f"{LANG_DIR}/formats.html"),
        ("VERIFIED", "实测记录", f"{len(verified.VERIFIED)} 门语言的本机复现", "verified.html"),
        ("SOURCES", "来源索引", "220 条官方来源", "sources.html"),
    ]
    topic_html = "".join(
        f'<a class="topic-link" href="{href}"><span class="topic-link__kicker">{kicker}</span>'
        f'<span class="topic-link__title">{title}</span>'
        f'<span class="topic-link__desc">{desc}</span></a>'
        for kicker, title, desc, href in topics
    )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{ui.head_snippet()}
<title>语言的产物链 — 语言 / 框架 / 技术栈</title>
<meta name="description" content="编程语言、框架与技术栈的三级索引：{TOTAL} 个语言条目、{FRAMEWORK_CARDS} 张框架决策卡、{len(stacks.STACKS)} 个组合栈，以及场景、安全与格式专题。">
<link rel="stylesheet" href="assets/style.css">
</head>
<body data-page="home">
<a class="skip-link" href="#main">跳到正文</a>
<div class="progress" aria-hidden="true"><span></span></div>
<button class="menu-toggle" type="button" aria-label="打开目录" aria-expanded="false" aria-controls="catalog"><span></span></button>
<div class="scrim"></div>
{ui.font_ui()}
<button class="cmdk-btn" type="button" data-cmdk aria-label="全站搜索">搜索全站 <kbd>⌘K</kbd></button>
{render_catalog(None, "")}
<main class="page" id="main">
  <div class="page__inner">
    <header class="hero home-hero">
      <p class="hero__kicker">An Archive of Languages, Frameworks &amp; Stacks</p>
      <h1 class="hero__title">语言、框架与<br><em>技术栈</em></h1>
      <p class="hero__sub">先看语言能做什么，再看框架怎么搭，最后落到一套能开工的组合栈。专题页负责横向问题：场景怎么选、安全怎么做、产物长什么样。</p>
    </header>

    <section class="home-doors" aria-label="三级入口">{card_html}</section>

    <section class="block reveal" id="topics">
      <div class="block__head">
        <span class="block__num">00</span>
        <h2 class="block__title">专题<em>Topics</em></h2>
        <span class="block__rule"></span>
      </div>
      <div class="topic-grid">{topic_html}</div>
    </section>

    <footer class="pagefoot">
      <p class="stamp">全站样例为依据公开规范与文档重构的示意内容；具体地址、偏移与字节数为示例值。</p>
      <p>{BATCH_LABEL} · 首页</p>
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
        <a class="stack-card" href="index.html"><span class="stack-top"><span class="stack-lang">HOME</span><span class="stack-type">入口</span></span><span class="stack-fw">首页</span><span class="stack-why">语言 / 框架 / 技术栈三个入口。</span></a>
        <a class="stack-card" href="{LANG_DIR}/index.html"><span class="stack-top"><span class="stack-lang">LANGUAGES</span><span class="stack-type">一级</span></span><span class="stack-fw">编程语言</span><span class="stack-why">{TOTAL} 个条目，按年代与家族浏览。</span></a>
        <a class="stack-card" href="{FW_DIR}/index.html"><span class="stack-top"><span class="stack-lang">FRAMEWORKS</span><span class="stack-type">二级</span></span><span class="stack-fw">框架总览</span><span class="stack-why">{FRAMEWORK_CARDS} 张决策卡，按语言与类型筛选。</span></a>
        <a class="stack-card" href="{STACK_DIR}/index.html"><span class="stack-top"><span class="stack-lang">STACKS</span><span class="stack-type">三级</span></span><span class="stack-fw">技术栈</span><span class="stack-why">{len(stacks.STACKS)} 个组合栈，按领域浏览。</span></a>
        <a class="stack-card" href="scenarios.html"><span class="stack-top"><span class="stack-lang">SCENARIOS</span><span class="stack-type">专题</span></span><span class="stack-fw">开发场景</span><span class="stack-why">{len(dev_scenarios.SCENARIOS)} 个开发场景 × {sum(len(s["architectures"]) for s in dev_scenarios.SCENARIOS)} 个架构分组。</span></a>
        <a class="stack-card" href="{LANG_DIR}/formats.html"><span class="stack-top"><span class="stack-lang">FORMATS</span><span class="stack-type">专题</span></span><span class="stack-fw">产物索引</span><span class="stack-why">42 种格式 + 320 个阶段产物。</span></a>
        <a class="stack-card" href="sources.html"><span class="stack-top"><span class="stack-lang">SOURCES</span><span class="stack-type">专题</span></span><span class="stack-fw">来源索引</span><span class="stack-why">220 条官方来源，可搜索。</span></a>
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
    root = "" if path.parent == ROOT else "../"
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
            "href": f"{LANG_DIR}/{slug}.html", "kind": "语言",
            "keywords": [l["cn"], str(l["year"]), l["desc"], l["family_label"], slug]
                        + ALIASES.get(slug, []),
        })
        detail = FRAMEWORKS.get(slug)
        if detail:
            items.append({
                "title": f"{l['name']} · 框架与场景", "group": "框架",
                "desc": detail["summary"],
                "href": f"{FW_DIR}/{slug}.html", "kind": "框架页",
                "keywords": fw_names.get(slug, []) + detail["scenarios"] + [l["name"]],
            })
            for card in detail["cards"]:
                items.append({
                    "title": card["name"], "group": "框架",
                    "desc": f"{card['type']} · {l['name']} · {card['tagline']}",
                    "href": f"{FW_DIR}/{slug}.html#{_slugify(card['name'])}",
                    "kind": "决策卡",
                    "keywords": [l["name"], l["cn"], card["type"], card["maintainer"], card["tagline"]],
                })

    fmt_index_data = formats.build(DATA)
    for f in fmt_index_data:
        items.append({
            "title": f["name"], "group": "产物格式",
            "desc": f["desc"] + f"（{len(f['langs'])} 门语言）",
            "href": f"{LANG_DIR}/formats.html#{f['key']}", "kind": "格式",
            "keywords": f["langs"] + [f["desc"], "格式", "artifact"],
        })

    for sc in dev_scenarios.SCENARIOS:
        items.append({
            "title": f"开发场景 · {sc['title']}", "group": "开发场景",
            "desc": sc["desc"],
            "href": f"scenarios.html#dev-{sc['key']}", "kind": "开发场景",
            "keywords": [sc["title"], sc["en"]]
                        + [a["title"] for a in sc["architectures"]]
                        + [dev_scenarios.PATTERN_BY_KEY[a["pattern"]]["title"]
                           for a in sc["architectures"]],
        })
        for arch in sc["architectures"]:
            pattern = dev_scenarios.PATTERN_BY_KEY[arch["pattern"]]
            items.append({
                "title": f"{sc['title']} · {arch['title']}", "group": "开发场景",
                "desc": f"{arch['desc']}（模式：{pattern['title']}）",
                "href": f"scenarios.html#dev-{sc['key']}", "kind": "架构组合",
                "keywords": [sc["title"], arch["title"], pattern["title"]]
                            + [entry[1] for entry in arch["entries"]],
            })

    domain_titles = {d["key"]: d["title"] for d in stacks.DOMAINS}
    for st in stacks.STACKS:
        items.append({
            "title": st["title"], "group": "技术栈",
            "desc": f"{domain_titles.get(st['domain'], '')} · {st['summary']}",
            "href": f"{STACK_DIR}/{st['key']}.html", "kind": "技术栈",
            "keywords": [domain_titles.get(st["domain"], ""), st["summary"]]
                        + st["fit"] + st["avoid"]
                        + [i[1] for l in st["layers"] for i in l["items"] if isinstance(i, tuple)],
        })

    for title, href, desc in (
        ("编程语言", f"{LANG_DIR}/index.html", "编译管线、产物链与语言列表"),
        ("框架总览", f"{FW_DIR}/index.html", "142 张决策卡，按语言与类型筛选"),
        ("技术栈", f"{STACK_DIR}/index.html", "语言 + 框架 + 数据与部署的组合栈"),
        ("开发场景", "scenarios.html", "按开发场景 × 架构模式浏览语言与框架"),
        ("来源索引", "sources.html", "220 条官方来源"),
        ("产物索引", f"{LANG_DIR}/formats.html", "按格式反查语言与阶段，含全部阶段产物"),
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


def write_data_js():
    payload = {
        "total": TOTAL,
        "open": OPEN,
        "batch": BATCH_DONE,
        "frameworks": FRAMEWORK_CARDS,
        "dev_scenarios": len(dev_scenarios.SCENARIOS),
        "stacks": len(stacks.STACKS),
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

    patterns = {p["key"]: p for p in dev_scenarios.PATTERNS}
    if len(dev_scenarios.PATTERNS) != 12:
        errors.append(f"统一架构模式不是 12 种：{len(dev_scenarios.PATTERNS)}")
    used_patterns = set()
    for sc in dev_scenarios.SCENARIOS:
        if not sc.get("architectures"):
            errors.append(f"开发场景 {sc['key']} 缺少架构模式")
        for arch in sc["architectures"]:
            pattern_key = arch.get("pattern", "")
            if pattern_key not in patterns:
                errors.append(f"开发场景 {sc['key']}/{arch['key']} 引用未知模式 {pattern_key}")
            else:
                used_patterns.add(pattern_key)
            if not arch.get("entries"):
                errors.append(f"开发场景 {sc['key']}/{arch['key']} 缺少条目")
            for entry in arch["entries"]:
                slug, fw_name = entry[0], entry[1]
                if slug not in BUILT_SLUGS:
                    errors.append(f"开发场景 {sc['key']}/{arch['key']} 引用未知语言 {slug}")
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

    unused = set(patterns) - used_patterns
    if unused:
        errors.append("统一架构模式未被使用：" + ", ".join(sorted(unused)))

    domain_keys = {d["key"] for d in stacks.DOMAINS}
    stack_keys = {s["key"] for s in stacks.STACKS}
    for st in stacks.STACKS:
        if st["domain"] not in domain_keys:
            errors.append(f"技术栈 {st['key']} 引用未知领域 {st['domain']}")
        for layer in st["layers"]:
            for item in layer["items"]:
                if not isinstance(item, tuple):
                    continue
                slug, name = item
                if slug not in BUILT_SLUGS:
                    errors.append(f"技术栈 {st['key']} 引用未知语言 {slug}")
                    continue
                card_names = [c["name"] for c in FRAMEWORKS.get(slug, {}).get("cards", [])]
                lang_name = language_by_slug(slug)["name"]
                if name not in card_names and name != lang_name:
                    errors.append(f"技术栈 {st['key']} 引用未知组件 {slug}/{name}")
        for alt in st["alternatives"]:
            if alt not in stack_keys:
                errors.append(f"技术栈 {st['key']} 引用未知替代栈 {alt}")

    return errors


def canonical_pages():
    pages = [
        ROOT / "index.html", ROOT / "sources.html", ROOT / "verified.html",
        ROOT / "scenarios.html", ROOT / "404.html",
    ]
    for name in (LANG_DIR, FW_DIR, STACK_DIR):
        pages += sorted((ROOT / name).glob("*.html"))
    return pages


def write_redirect(path, target):
    """旧地址的跳转桩：不带脚本与样式，不进入审计与冒烟扫描。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>页面已迁移</title>
<meta http-equiv="refresh" content="0; url={target}">
<link rel="canonical" href="{target}">
<meta name="robots" content="noindex">
</head>
<body>
<p><a href="{target}">页面已迁移，点击继续 →</a></p>
</body>
</html>
""", encoding="utf-8")


def link_check():
    """检查生成页面中的相对链接是否都指向实际文件。"""
    problems = []
    pages = canonical_pages()
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

    for name in (LANG_DIR, FW_DIR, STACK_DIR, "langs"):
        (ROOT / name).mkdir(exist_ok=True)
    (ROOT / "assets").mkdir(exist_ok=True)

    # 旧的框架页直接删除，不保留跳转（按用户选择）
    for stale in (ROOT / "langs").glob("*-frameworks.html"):
        stale.unlink()

    for lang in BUILT:
        slug = lang["slug"]
        (ROOT / LANG_DIR / f"{slug}.html").write_text(
            render_language_page(lang), encoding="utf-8",
        )
        (ROOT / FW_DIR / f"{slug}.html").write_text(
            fw_site.render_page(
                lang,
                FRAMEWORKS.get(slug),
                SHORT.get(slug),
                render_catalog(slug, "../"),
                TOTAL,
                BATCH_LABEL,
            ),
            encoding="utf-8",
        )
        # 旧语言页保留跳转
        write_redirect(ROOT / "langs" / f"{slug}.html", f"../{LANG_DIR}/{slug}.html")

    (ROOT / LANG_DIR / "index.html").write_text(render_language_index(), encoding="utf-8")
    (ROOT / FW_DIR / "index.html").write_text(
        frameworks_index.render_frameworks_index(
            FRAMEWORKS, LANGUAGES, render_catalog(None, "../"), BATCH_LABEL,
        ),
        encoding="utf-8",
    )
    (ROOT / STACK_DIR / "index.html").write_text(
        stack_site.render_stacks_index(render_catalog(None, "../"), BATCH_LABEL),
        encoding="utf-8",
    )
    for st in stacks.STACKS:
        (ROOT / STACK_DIR / f"{st['key']}.html").write_text(
            stack_site.render_stack(st, render_catalog(None, "../"), BATCH_LABEL),
            encoding="utf-8",
        )

    (ROOT / "index.html").write_text(render_home(), encoding="utf-8")
    (ROOT / "verified.html").write_text(
        verified_site.render_verified_page(
            {l["slug"]: l for l in BUILT}, render_catalog(None, ""), BATCH_LABEL, BATCH_DONE,
        ),
        encoding="utf-8",
    )
    (ROOT / LANG_DIR / "formats.html").write_text(
        fmt_index.render_formats(
            DATA, {l["slug"]: l for l in BUILT}, render_catalog(None, "../", "index.html"),
            BATCH_LABEL, BATCH_DONE, len(BUILT),
        ),
        encoding="utf-8",
    )
    write_redirect(ROOT / "formats.html", f"{LANG_DIR}/formats.html")
    (ROOT / "sources.html").write_text(
        src_index.render_sources_index(
            BUILT, render_catalog(None, ""), BATCH_LABEL,
        ),
        encoding="utf-8",
    )
    (ROOT / "404.html").write_text(render_404(), encoding="utf-8")
    (ROOT / "scenarios.html").write_text(
        scenario_site.render_scenarios(render_catalog(None, ""), FRAMEWORKS, BATCH_LABEL),
        encoding="utf-8",
    )
    write_data_js()
    search_count = write_search_js()

    for page in canonical_pages():
        inject_meta(page)

    problems = link_check()
    print(f"已生成：{len(BUILT)} 个语言页 + {len(BUILT)} 个框架页 + {len(stacks.STACKS)} 个技术栈页 + 索引 + 专题")
    print(f"页面总数：{len(canonical_pages())}（另有 {len(BUILT) + 1} 个旧链接跳转）")
    print(f"产物阶段总数：{sum(stage_count(l['slug']) for l in BUILT)}")
    print(f"框架决策卡：{FRAMEWORK_CARDS} · 开发场景：{len(dev_scenarios.SCENARIOS)}")
    print(f"全局搜索索引：{search_count} 条 · 产物格式：{len(formats.build(DATA))} 种")
    print(f"实测记录：{len(verified.VERIFIED)} 门语言")
    if problems:
        print("链接问题：")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("链接检查：通过")


if __name__ == "__main__":
    main()

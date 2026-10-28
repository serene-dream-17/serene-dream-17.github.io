# -*- coding: utf-8 -*-
"""
全站馆藏登记表：70 门语言。
顺序即展签编号（PLATE 01–70），与需求清单一致。
built=True 表示该语言页已在本批次生成。
"""

ERAS = [
    {"key": "1950s-1960s", "title": "1950s–1960s", "range": "1950–1969", "label": "创世纪"},
    {"key": "1970s", "title": "1970s", "range": "1970–1979", "label": "系统与范式"},
    {"key": "1980s", "title": "1980s", "range": "1980–1989", "label": "个人电脑"},
    {"key": "1990s", "title": "1990s", "range": "1990–1999", "label": "互联网"},
    {"key": "2000s", "title": "2000s", "range": "2000–2009", "label": "托管运行时"},
    {"key": "2010s", "title": "2010s", "range": "2010–2019", "label": "现代工程化"},
    {"key": "2020s", "title": "2020s", "range": "2020–2029", "label": "新一波"},
    {"key": "domain", "title": "领域专用", "range": "1949–2020s", "label": "另一条赛道"},
    {"key": "markup", "title": "标记与配置", "range": "1991–2009", "label": "文档与数据"},
]

FAMILIES = {
    "compiled": "编译型",
    "interpreted": "解释 / 字节码",
    "domain": "领域专用",
    "markup": "标记 / 配置",
}

# slug, name, cn, year, era, family, desc, built
RAW = [
    ("fortran", "FORTRAN", "公式翻译系统", 1957, "1950s-1960s", "compiled",
     "科学计算的起点；固定列卡片与 IBM 704 编译器", True),
    ("lisp", "LISP", "表处理语言", 1958, "1950s-1960s", "interpreted",
     "代码即数据；AI 的第一门母语", True),
    ("algol60", "ALGOL 60", "算法语言", 1960, "1950s-1960s", "compiled",
     "几乎所有现代语法记法的祖先", True),
    ("cobol", "COBOL", "通用商业语言", 1959, "1950s-1960s", "compiled",
     "银行、保险与政府的账本语言", True),
    ("basic", "BASIC", "初学者通用符号指令代码", 1964, "1950s-1960s", "interpreted",
     "把编程带到个人电脑与课堂", True),
    ("simula", "Simula 67", "仿真语言", 1967, "1950s-1960s", "compiled",
     "class 与对象概念的源头", True),
    ("pli", "PL/I", "编程语言一号", 1964, "1950s-1960s", "compiled",
     "大型机上的「万能语言」", True),
    ("apl", "APL", "数组编程语言", 1966, "1950s-1960s", "interpreted",
     "数组与符号的极简记法", True),
    ("snobol", "SNOBOL", "字符串操作语言", 1962, "1950s-1960s", "interpreted",
     "字符串模式匹配的先驱", True),
    ("b", "B", "B 语言", 1969, "1950s-1960s", "compiled",
     "C 的前身，UNIX 的第一种实现语言", True),

    ("c", "C", "C 语言", 1972, "1970s", "compiled",
     "UNIX 内核与系统软件的通用语", True),
    ("pascal", "Pascal", "帕斯卡语言", 1970, "1970s", "compiled",
     "结构化教学与 Turbo 时代", True),
    ("smalltalk", "Smalltalk", "面向对象环境", 1972, "1970s", "interpreted",
     "图形界面、字节码与活的镜像", True),
    ("prolog", "Prolog", "逻辑编程", 1972, "1970s", "interpreted",
     "逻辑即程序，WAM 即产物", True),
    ("ml", "ML", "元语言", 1973, "1970s", "compiled",
     "类型推断与函数式语言的底座", True),
    ("scheme", "Scheme", "Scheme", 1975, "1970s", "interpreted",
     "极简 Lisp，SICP 的课堂语言", True),
    ("forth", "Forth", "Forth", 1970, "1970s", "compiled",
     "线程码、词典与望远镜控制台", True),
    ("modula2", "Modula-2", "模块化语言", 1978, "1970s", "compiled",
     "定义模块与实现模块的分离", True),

    ("cpp", "C++", "C++", 1985, "1980s", "compiled",
     "C 的对象化，性能与复杂度并存", False),
    ("objectivec", "Objective-C", "Objective-C", 1984, "1980s", "compiled",
     "NeXT 与 Apple 生态的底座", False),
    ("perl", "Perl", "实用报表提取语言", 1987, "1980s", "interpreted",
     "CGI 时代的系统胶水", False),
    ("erlang", "Erlang", "Erlang", 1986, "1980s", "interpreted",
     "电信级并发与容错", False),
    ("ada", "Ada", "Ada", 1980, "1980s", "compiled",
     "军工与关键系统的语言", False),
    ("eiffel", "Eiffel", "Eiffel", 1986, "1980s", "compiled",
     "契约式设计", False),
    ("matlab", "MATLAB", "矩阵实验室", 1984, "1980s", "interpreted",
     "工程仿真与矩阵计算", False),
    ("commonlisp", "Common Lisp", "通用 Lisp", 1984, "1980s", "interpreted",
     "标准化的大型 Lisp", False),
    ("tcl", "Tcl", "工具命令语言", 1988, "1980s", "interpreted",
     "嵌入脚本与 EDA 工具", False),

    ("python", "Python", "Python", 1991, "1990s", "interpreted",
     "可读性优先，科学计算的默认语言", False),
    ("java", "Java", "Java", 1995, "1990s", "interpreted",
     "一次编写，到处运行", False),
    ("javascript", "JavaScript", "JavaScript", 1995, "1990s", "interpreted",
     "浏览器里的唯一通用语", False),
    ("php", "PHP", "PHP", 1995, "1990s", "interpreted",
     "动态网站的草根语言", False),
    ("ruby", "Ruby", "Ruby", 1995, "1990s", "interpreted",
     "为开发者快乐而设计", False),
    ("haskell", "Haskell", "Haskell", 1990, "1990s", "compiled",
     "纯函数式与类型系统试验田", False),
    ("lua", "Lua", "Lua", 1993, "1990s", "interpreted",
     "游戏与嵌入式的轻量脚本", False),
    ("r", "R", "R", 1993, "1990s", "interpreted",
     "统计学家的工作台", False),
    ("delphi", "Delphi", "Object Pascal", 1995, "1990s", "compiled",
     "Windows 桌面的快速应用", False),
    ("vb", "Visual Basic", "Visual Basic", 1991, "1990s", "interpreted",
     "让业务人员也能写程序", False),
    ("ocaml", "OCaml", "OCaml", 1996, "1990s", "compiled",
     "类型安全的函数式系统语言", False),

    ("csharp", "C#", "C#", 2000, "2000s", "interpreted",
     ".NET 生态的主力", False),
    ("scala", "Scala", "Scala", 2004, "2000s", "interpreted",
     "JVM 上的函数式与大数据", False),
    ("fsharp", "F#", "F#", 2005, "2000s", "interpreted",
     ".NET 上的函数式", False),
    ("clojure", "Clojure", "Clojure", 2007, "2000s", "interpreted",
     "JVM 上的 Lisp", False),
    ("groovy", "Groovy", "Groovy", 2003, "2000s", "interpreted",
     "构建脚本与 JVM 动态语言", False),
    ("go", "Go", "Go", 2009, "2000s", "compiled",
     "云原生基础设施的语言", False),
    ("d", "D", "D", 2001, "2000s", "compiled",
     "C++ 的现代化尝试", False),
    ("actionscript", "ActionScript", "ActionScript", 1998, "2000s", "interpreted",
     "Flash 时代的前端", False),

    ("rust", "Rust", "Rust", 2010, "2010s", "compiled",
     "无 GC 的内存安全", False),
    ("typescript", "TypeScript", "TypeScript", 2012, "2010s", "interpreted",
     "给 JavaScript 加上类型", False),
    ("swift", "Swift", "Swift", 2014, "2010s", "compiled",
     "Apple 平台的新语言", False),
    ("kotlin", "Kotlin", "Kotlin", 2011, "2010s", "interpreted",
     "Android 的现代选择", False),
    ("elixir", "Elixir", "Elixir", 2011, "2010s", "interpreted",
     "BEAM 上的现代函数式", False),
    ("julia", "Julia", "Julia", 2012, "2010s", "interpreted",
     "科学计算的性能新解", False),
    ("dart", "Dart", "Dart", 2011, "2010s", "interpreted",
     "Flutter 的 UI 语言", False),
    ("zig", "Zig", "Zig", 2016, "2010s", "compiled",
     "C 的克制替代品", False),
    ("nim", "Nim", "Nim", 2008, "2010s", "compiled",
     "Python 式语法的系统语言", False),
    ("crystal", "Crystal", "Crystal", 2014, "2010s", "compiled",
     "Ruby 语法，C 性能", False),
    ("elm", "Elm", "Elm", 2012, "2010s", "compiled",
     "前端的类型化架构", False),
    ("solidity", "Solidity", "Solidity", 2014, "2010s", "domain",
     "以太坊智能合约", False),

    ("mojo", "Mojo", "Mojo", 2023, "2020s", "compiled",
     "AI 时代的 Python 超集", False),
    ("gleam", "Gleam", "Gleam", 2016, "2020s", "interpreted",
     "BEAM 上的类型化语言", False),
    ("carbon", "Carbon", "Carbon", 2022, "2020s", "compiled",
     "Google 的 C++ 后继实验", False),
    ("odin", "Odin", "Odin", 2016, "2020s", "compiled",
     "游戏与图形编程", False),
    ("roc", "Roc", "Roc", 2022, "2020s", "compiled",
     "函数式与快速编译", False),
    ("v", "V", "V", 2019, "2020s", "compiled",
     "极简快速的系统语言", False),

    ("sql", "SQL", "结构化查询语言", 1974, "domain", "domain",
     "关系数据库的通用查询语言", False),
    ("assembly", "Assembly", "汇编语言", 1949, "domain", "domain",
     "机器码之上的第一层", False),
    ("shell", "Shell", "命令解释器", 1971, "domain", "domain",
     "操作系统的胶水", False),
    ("verilog", "Verilog", "Verilog", 1984, "domain", "domain",
     "芯片设计的硬件描述语言", False),
    ("cuda", "CUDA", "CUDA", 2007, "domain", "domain",
     "GPU 并行计算", False),
    ("glsl", "GLSL", "GLSL", 2002, "domain", "domain",
     "着色器与图形管线", False),

    ("html", "HTML", "超文本标记语言", 1991, "markup", "markup",
     "文档结构、DOM 与渲染流水线", True),
    ("css", "CSS", "层叠样式表", 1996, "markup", "markup",
     "层叠、盒模型与布局", True),
    ("xml", "XML", "可扩展标记语言", 1998, "markup", "markup",
     "可扩展标记与数据交换", True),
    ("svg", "SVG", "可缩放矢量图形", 2001, "markup", "markup",
     "矢量图形、XML 与 DOM", True),
    ("yaml", "YAML", "YAML", 2001, "markup", "markup",
     "配置与基础设施清单", True),
    ("markdown", "Markdown", "Markdown", 2004, "markup", "markup",
     "纯文本文档与静态站点", True),
    ("sass", "Sass", "SCSS", 2006, "markup", "markup",
     "CSS 预处理器与设计系统", True),
    ("less", "Less", "Less", 2009, "markup", "markup",
     "CSS 预处理器与遗留项目", True),
]

LANGUAGES = []
for i, (slug, name, cn, year, era, family, desc, built) in enumerate(RAW, start=1):
    LANGUAGES.append({
        "plate": i,
        "slug": slug,
        "name": name,
        "cn": cn,
        "year": year,
        "era": era,
        "family": family,
        "family_label": FAMILIES[family],
        "desc": desc,
        "built": built,
    })

ERAS_BY_KEY = {e["key"]: e for e in ERAS}

# 第 2 批开放的 1980s–1990s 页面
BATCH2 = {
    "cpp", "objectivec", "perl", "erlang", "ada", "eiffel", "matlab",
    "commonlisp", "tcl",
    "python", "java", "javascript", "php", "ruby", "haskell", "lua",
    "r", "delphi", "vb", "ocaml",
}
for _lang in LANGUAGES:
    if _lang["slug"] in BATCH2:
        _lang["built"] = True

# 第 3 批开放的 2000s–2010s 页面
BATCH3 = {
    "csharp", "scala", "fsharp", "clojure", "groovy", "go", "d",
    "actionscript",
    "rust", "typescript", "swift", "kotlin", "elixir", "julia", "dart",
    "zig", "nim", "crystal", "elm", "solidity",
}
for _lang in LANGUAGES:
    if _lang["slug"] in BATCH3:
        _lang["built"] = True

# 第 4 批开放的 2020s + 领域专用页面
BATCH4 = {
    "mojo", "gleam", "carbon", "odin", "roc", "v",
    "sql", "assembly", "shell", "verilog", "cuda", "glsl",
}
for _lang in LANGUAGES:
    if _lang["slug"] in BATCH4:
        _lang["built"] = True

BUILT = [l for l in LANGUAGES if l["built"]]
BUILT_SLUGS = [l["slug"] for l in BUILT]
PENDING = [l for l in LANGUAGES if not l["built"]]

assert len(LANGUAGES) == 78, len(LANGUAGES)
assert len({l["slug"] for l in LANGUAGES}) == 78

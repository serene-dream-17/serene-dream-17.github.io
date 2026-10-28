# -*- coding: utf-8 -*-
"""第 5 批 · 标记与配置：8 个条目的档案与产物链数据。"""

LANGS = {

# ============================================================
"html": {
    "tagline": "用标签描述文档结构，浏览器把它变成 DOM、渲染树与像素。",
    "intro": [
        "HTML 由 Tim Berners-Lee 在 CERN 于 1991 年提出，最初是为了让论文之间可以互相链接。它继承 SGML 的标签语法，但把「文档结构」放到了第一位：标题、段落、列表、链接、图片。",
        "HTML 不是编程语言，它没有变量与控制流；它的「程序」是一棵文档树。浏览器解析标签，建立 DOM；CSS 参与后形成渲染树；最后经过布局与绘制变成屏幕上的像素。",
        "从 HTML 4 到 XHTML 再到 HTML5，语法有过摇摆；今天的 HTML 是 WHATWG 的 Living Standard，由浏览器与社区持续演进。",
    ],
    "lineage": {
        "from": ["SGML", "超文本系统", "CERN 文档需求"],
        "to": ["XHTML", "HTML5", "Web Components", "JSX / 模板语言"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.html",
            "cmd": "$ cat hello.html",
            "code": r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>Hello</title>
</head>
<body>
  <p>Hello, world</p>
</body>
</html>""",
            "format": [
                ("MIME", "text/html"),
                ("编码", "UTF-8（meta charset 声明）"),
                ("结构", "doctype → html → head/body"),
                ("解析", "容错解析器，标签可省略"),
            ],
            "note": "HTML 的解析器非常宽容：未闭合的标签、错误的嵌套都会被修复成一棵合法的树。这也是网页能长期兼容的原因。",
        },
        {
            "label": "DOM 树",
            "file": "DOM",
            "cmd": "document.documentElement",
            "code": r"""Document
└─ html
   ├─ head
   │  ├─ meta
   │  └─ title
   │     └─ "Hello"
   └─ body
      └─ p
         └─ "Hello, world"

; DOM = Document Object Model
; 每个标签是一个 Element 节点
; 文本是 Text 节点""",
            "format": [
                ("节点", "Document / Element / Text"),
                ("接口", "DOM API（querySelector 等）"),
                ("可变", "JS 可以增删改节点"),
                ("事件", "DOM 也是事件目标树"),
            ],
            "note": "DOM 是 HTML 的「运行时表示」。CSS、JavaScript、无障碍树都建立在它之上。",
        },
        {
            "label": "渲染树",
            "file": "render tree",
            "cmd": "DevTools → Elements / Rendering",
            "code": r"""RenderView
└─ RenderBlock html
   └─ RenderBlock body
      └─ RenderBlock p
         └─ RenderText "Hello, world"

; 只包含可见节点
; display:none 的元素不进入渲染树
; 伪元素会生成额外的盒子""",
            "format": [
                ("输入", "DOM + CSSOM"),
                ("节点", "RenderBlock / RenderInline / RenderText"),
                ("过滤", "display:none 不参与"),
                ("伪元素", "::before / ::after 生成盒子"),
            ],
            "note": "渲染树是 DOM 与样式的交集：结构节点 + 计算后的显示属性。它决定了后面布局与绘制的工作量。",
        },
        {
            "label": "布局与绘制",
            "file": "pixels",
            "cmd": "document.querySelector('p').getBoundingClientRect()",
            "code": r"""DOMRect { x: 8, y: 8, width: 784, height: 19, ... }

; 布局：块级盒宽度由包含块决定
; 绘制：文本 run 写入图层
; 合成：图层交给 GPU 合成上屏

; 产物不是文件，而是一帧像素
; DevTools → Layers / Paint flashing 可观察""",
            "format": [
                ("布局", "盒模型：content / padding / border / margin"),
                ("绘制", "文本、背景、边框、阴影"),
                ("合成", "图层 + GPU"),
                ("产物", "屏幕像素 / 无障碍树"),
            ],
            "note": "HTML 的「最终产物」是一帧像素，以及一棵无障碍树。它们都不是可以拷走的文件。",
        },
    ],
    "tools": [
        {"era": "1990s", "editor": "文本编辑器", "compiler": "浏览器解析器", "build": "—", "pkg": "—", "debug": "View Source"},
        {"era": "2000s", "editor": "Dreamweaver / 记事本", "compiler": "浏览器", "build": "—", "pkg": "—", "debug": "Firebug"},
        {"era": "2020s", "editor": "VS Code", "compiler": "浏览器 / 解析器", "build": "Vite / Next.js", "pkg": "npm", "debug": "DevTools / Lighthouse"},
    ],
    "hello": {
        "file": "hello.html",
        "code": r"""<!doctype html>
<html lang="zh-CN">
<head><meta charset="utf-8"><title>Hello</title></head>
<body><p>Hello, world</p></body>
</html>""",
        "footprint": [
            {"stage": "HTML", "size": "≈ 110 B", "w": 5},
            {"stage": "DOM", "size": "≈ 6 个节点", "w": 8},
            {"stage": "渲染树", "size": "≈ 4 个盒子", "w": 10},
            {"stage": "布局", "size": "1 个块级盒", "w": 8},
            {"stage": "像素", "size": "视口大小", "w": 60},
        ],
        "why": [
            "<strong>标签</strong>：用嵌套结构表达文档语义，而不是绘制指令。",
            "<strong>DOM</strong>：把文档变成可查询、可修改、可绑定事件的对象树。",
            "<strong>渲染树</strong>：DOM 与 CSSOM 结合，只保留可见节点。",
            "<strong>布局 / 绘制</strong>：盒模型决定位置，绘制决定像素。",
        ],
    },
},

# ============================================================
"css": {
    "tagline": "把样式从结构里分离出来，用层叠与优先级计算每个元素的样子。",
    "intro": [
        "CSS 由 Håkon Wium Lie 与 Bert Bos 在 1994 年提出，1996 年发布 CSS1。它把「文档结构」与「视觉表现」分开：HTML 负责语义，CSS 负责颜色、字体、间距与布局。",
        "CSS 的核心机制是层叠（cascade）与优先级（specificity）：多个规则可能同时命中一个元素，浏览器按来源、重要性、优先级与顺序决定胜者，再计算最终样式。",
        "从 CSS2 到 CSS3 的模块化，再到 Flexbox、Grid、容器查询与自定义属性，CSS 已经能独立完成复杂布局。Sass、PostCSS、Tailwind 等工具则在其上增加工程能力。",
    ],
    "lineage": {
        "from": ["SGML / HTML 表现需求", "桌面排版"],
        "to": ["CSS3 模块", "Flexbox / Grid", "Sass / PostCSS / Tailwind"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.css",
            "cmd": "$ cat hello.css",
            "code": r"""body::before {
  content: "Hello, world";
  display: block;
  font: 16px/1.5 system-ui;
}""",
            "format": [
                ("扩展名", ".css"),
                ("规则", "选择器 + 声明块"),
                ("层叠", "来源 / 重要性 / 优先级 / 顺序"),
                ("单位", "px / rem / em / % / vw …"),
            ],
            "note": "`::before` 是伪元素：它不在 DOM 里，但会生成一个可样式的盒子。`content` 只在伪元素上生效。",
        },
        {
            "label": "CSSOM",
            "file": "CSSOM",
            "cmd": "document.styleSheets[0].cssRules",
            "code": r"""CSSStyleSheet
└─ CSSStyleRule
   selectorText: "body::before"
   style:
     content: "Hello, world"
     display: block
     font: 16px/1.5 system-ui

; CSSOM = CSS Object Model
; 浏览器把样式表解析成可查询的对象
; JS 可读写样式规则""",
            "format": [
                ("对象", "CSSStyleSheet / CSSStyleRule"),
                ("选择器", "selectorText"),
                ("声明", "CSSStyleDeclaration"),
                ("可变", "JS 可插入/删除规则"),
            ],
            "note": "CSSOM 是 CSS 的运行时表示。`getComputedStyle` 读取的是层叠计算后的结果，而不是单条规则。",
        },
        {
            "label": "计算样式",
            "file": "computed style",
            "cmd": "getComputedStyle(document.body, '::before')",
            "code": r"""content: "Hello, world"
display: block
font-family: system-ui
font-size: 16px
line-height: 24px
color: rgb(0, 0, 0)

; 层叠与继承已解决
; 相对单位已换算
; 最终值参与布局""",
            "format": [
                ("层叠", "来源 / !important / 优先级 / 顺序"),
                ("继承", "字体、颜色等可继承属性"),
                ("计算", "相对单位 → 绝对值"),
                ("使用值", "布局阶段最终采用的值"),
            ],
            "note": "计算样式不是「源码里写的值」：`em` 会按父级字号换算，`%` 会按包含块解析，继承会填充未声明的属性。",
        },
        {
            "label": "布局与绘制",
            "file": "box / pixels",
            "cmd": "DevTools → Computed / Layout",
            "code": r"""::before box
  x: 8   y: 8
  width: 784
  height: 24
  margin: 0
  padding: 0
  border: 0

text run: "Hello, world" at (8, 8)
color: rgb(0, 0, 0)

; 布局：盒模型 + 包含块
; 绘制：文本 run
; 合成：图层""",
            "format": [
                ("盒模型", "content / padding / border / margin"),
                ("布局", "块级 / 行内 / Flex / Grid"),
                ("绘制", "文本、背景、边框"),
                ("产物", "像素"),
            ],
            "note": "CSS 的产物同样是像素。它与 HTML 共享同一条渲染流水线，只是输入是样式而不是结构。",
        },
    ],
    "tools": [
        {"era": "1990s", "editor": "文本编辑器", "compiler": "浏览器", "build": "—", "pkg": "—", "debug": "View Source"},
        {"era": "2000s", "editor": "Dreamweaver", "compiler": "浏览器", "build": "—", "pkg": "—", "debug": "Firebug"},
        {"era": "2020s", "editor": "VS Code", "compiler": "浏览器 / PostCSS", "build": "Vite / Sass / Tailwind", "pkg": "npm", "debug": "DevTools"},
    ],
    "hello": {
        "file": "hello.css",
        "code": r"""body::before {
  content: "Hello, world";
  display: block;
  font: 16px/1.5 system-ui;
}""",
        "footprint": [
            {"stage": "CSS", "size": "≈ 100 B", "w": 5},
            {"stage": "CSSOM", "size": "1 条规则", "w": 6},
            {"stage": "计算样式", "size": "≈ 10 个属性", "w": 8},
            {"stage": "布局", "size": "1 个伪元素盒", "w": 8},
            {"stage": "像素", "size": "视口大小", "w": 60},
        ],
        "why": [
            "<strong>层叠</strong>：多个规则命中同一元素时，用一套确定的规则决出胜者。",
            "<strong>继承</strong>：字体、颜色等属性自动向下传递，减少重复声明。",
            "<strong>盒模型</strong>：内容、内边距、边框、外边距决定元素占位。",
            "<strong>布局系统</strong>：Flexbox / Grid 把二维排版变成可计算的约束。",
        ],
    },
},

# ============================================================
"xml": {
    "tagline": "用可嵌套的标签描述数据，让不同系统交换结构化信息。",
    "intro": [
        "XML 由 W3C 在 1998 年发布，是 SGML 的一个子集。它的目标不是显示，而是描述结构化数据：元素、属性、命名空间、嵌套关系。",
        "XML 有两个层次：格式良好（well-formed）与有效（valid）。前者只要标签正确嵌套即可；后者还需要符合 DTD 或 XML Schema 的定义。",
        "它在 2000 年代主导了企业集成、配置文件与 SOAP；今天仍用于 Office 文档、Android 布局、SVG、构建工具与许多行业标准。",
    ],
    "lineage": {
        "from": ["SGML", "Web 数据交换需求"],
        "to": ["XHTML", "SOAP / WSDL", "SVG", "Office Open XML"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.xml",
            "cmd": "$ cat hello.xml",
            "code": r"""<?xml version="1.0" encoding="UTF-8"?>
<greeting lang="zh">
  <text>Hello, world</text>
</greeting>""",
            "format": [
                ("扩展名", ".xml / .xsd / .xsl"),
                ("MIME", "application/xml"),
                ("结构", "元素 + 属性 + 文本"),
                ("命名空间", "xmlns 区分同名元素"),
            ],
            "note": "XML 的标签名由你定义，所以它既能描述文档，也能描述订单、配置或图形。",
        },
        {
            "label": "DOM 树",
            "file": "DOM",
            "cmd": "$ xmllint --format hello.xml",
            "code": r"""Document
└─ Element greeting
   ├─ Attribute lang="zh"
   └─ Element text
      └─ Text "Hello, world"

; DOM：整棵树读入内存
; SAX：边读边发事件，适合大文件
; 两种解析模型，产物相同""",
            "format": [
                ("DOM", "整树加载，可随机访问"),
                ("SAX", "流式事件，低内存"),
                ("节点", "Element / Attribute / Text"),
                ("顺序", "元素顺序有意义"),
            ],
            "note": "DOM 适合小文件与随机访问；SAX 适合大文件与流式处理。选择解析器会直接影响内存与延迟。",
        },
        {
            "label": "Schema 校验",
            "file": "hello.xsd",
            "cmd": "$ xmllint --schema hello.xsd hello.xml",
            "code": r"""<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="greeting">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="text" type="xs:string"/>
      </xs:sequence>
      <xs:attribute name="lang" type="xs:language"/>
    </xs:complexType>
  </xs:element>
</xs:schema>

; well-formed：语法正确
; valid：符合 XSD
; 校验失败会给出路径与原因""",
            "format": [
                ("XSD", "元素、类型、顺序、基数"),
                ("校验", "结构 + 数据类型"),
                ("DTD", "更老的模式语言"),
                ("错误", "行号 + 路径 + 原因"),
            ],
            "note": "Schema 把「数据长什么样」变成可机器检查的契约。这是 XML 在企业集成里最重要的能力。",
        },
        {
            "label": "应用数据",
            "file": "JSON / HTML",
            "cmd": "$ xsltproc hello.xsl hello.xml",
            "code": r"""<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <p><xsl:value-of select="greeting/text"/></p>
  </xsl:template>
</xsl:stylesheet>

<!-- 输出 -->
<p>Hello, world</p>

; XSLT 把 XML 转成 HTML / 文本
; 应用也可以直接把 DOM 映射成对象""",
            "format": [
                ("XSLT", "XML → HTML / XML / 文本"),
                ("XPath", "在树中选取节点"),
                ("绑定", "DOM → 语言对象"),
                ("用途", "集成、报表、配置"),
            ],
            "note": "XML 本身只是数据；真正让它有用的是 schema、XPath、XSLT 与各语言的绑定层。",
        },
    ],
    "tools": [
        {"era": "1990s", "editor": "文本编辑器", "compiler": "XML 解析器", "build": "make", "pkg": "—", "debug": "xmllint"},
        {"era": "2000s", "editor": "XMLSpy / Eclipse", "compiler": "Xerces / .NET XML", "build": "Ant", "pkg": "—", "debug": "XML 调试器"},
        {"era": "2020s", "editor": "VS Code + XML", "compiler": "libxml2 / lxml", "build": "Maven / Gradle", "pkg": "—", "debug": "xmllint / 日志"},
    ],
    "hello": {
        "file": "hello.xml",
        "code": r"""<?xml version="1.0" encoding="UTF-8"?>
<greeting lang="zh">
  <text>Hello, world</text>
</greeting>""",
        "footprint": [
            {"stage": "XML", "size": "≈ 110 B", "w": 5},
            {"stage": "DOM", "size": "≈ 3 个节点", "w": 6},
            {"stage": "XSD", "size": "≈ 300 B", "w": 12},
            {"stage": "校验", "size": "1 棵树", "w": 8},
            {"stage": "应用数据", "size": "1 个对象", "w": 7},
        ],
        "why": [
            "<strong>自定义标签</strong>：数据结构由 schema 定义，而不是固定语法。",
            "<strong>命名空间</strong>：不同标准可以安全地组合。",
            "<strong>Schema</strong>：结构、类型、顺序、基数都可校验。",
            "<strong>转换</strong>：XSLT / XPath 让同一份数据输出多种格式。",
        ],
    },
},

# ============================================================
"svg": {
    "tagline": "用 XML 描述矢量图形：缩放不失真，还能进 DOM 与 CSS。",
    "intro": [
        "SVG（Scalable Vector Graphics）由 W3C 在 2001 年发布 1.0 标准。它用 XML 描述线段、路径、矩形、文本与渐变，而不是像素。",
        "SVG 是矢量格式：图形在渲染时才栅格化，所以放大不会模糊。它还能嵌入 HTML，成为 DOM 的一部分，接受 CSS 与 JavaScript。",
        "图标、图表、地图、插画与数据可视化大量使用 SVG。它的产物可以是 `.svg` 文件、DOM 节点，或最终的一帧像素。",
    ],
    "lineage": {
        "from": ["XML", "PGML / VML", "矢量图形需求"],
        "to": ["D3 / 图表库", "图标系统", "Web 动画"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.svg",
            "cmd": "$ cat hello.svg",
            "code": r"""<svg xmlns="http://www.w3.org/2000/svg"
     width="320" height="80" viewBox="0 0 320 80">
  <rect width="320" height="80" fill="#f3ede1"/>
  <text x="16" y="48" font-size="24" fill="#1c1a16">
    Hello, world
  </text>
</svg>""",
            "format": [
                ("扩展名", ".svg"),
                ("MIME", "image/svg+xml"),
                ("坐标", "viewBox 定义用户坐标"),
                ("图形", "rect / path / text / circle"),
            ],
            "note": "`viewBox` 是 SVG 的核心：它把用户坐标映射到视口，缩放时几何关系保持不变。",
        },
        {
            "label": "XML DOM",
            "file": "DOM",
            "cmd": "document.querySelector('svg')",
            "code": r"""svg
├─ rect  width=320 height=80 fill=#f3ede1
└─ text  x=16 y=48 font-size=24 fill=#1c1a16
   └─ "Hello, world"

; SVG 元素就是 DOM 元素
; 可以用 CSS 改 fill / stroke
; 可以绑定事件、做动画""",
            "format": [
                ("节点", "svg / rect / text / path"),
                ("样式", "CSS 可作用于 SVG 元素"),
                ("脚本", "可查询、修改、绑定事件"),
                ("无障碍", "可加 title / desc / role"),
            ],
            "note": "内联 SVG 不是图片，而是 DOM。它能继承 CSS 变量、响应父容器，也能被 JavaScript 操作。",
        },
        {
            "label": "场景与几何",
            "file": "scene",
            "cmd": "DevTools → Elements / Layers",
            "code": r"""viewport: 320 × 80
rect:  x=0   y=0   w=320 h=80
text:  baseline=(16,48)
       glyph run "Hello, world"
       font-size=24

; 几何在用户坐标中计算
; 再经 viewBox 变换到视口
; 输出仍是矢量指令""",
            "format": [
                ("坐标", "用户坐标 → 视口坐标"),
                ("几何", "路径、包围盒、变换"),
                ("文本", "字体度量 + 字形"),
                ("动画", "SMIL / CSS / JS"),
            ],
            "note": "SVG 在栅格化之前始终是矢量指令。导出的 PNG 才固定了分辨率。",
        },
        {
            "label": "栅格化",
            "file": "pixels / .png",
            "cmd": "$ rsvg-convert -w 640 hello.svg -o hello.png",
            "code": r"""$ rsvg-convert -w 640 hello.svg -o hello.png
$ file hello.png
hello.png: PNG image data, 640 x 160, 8-bit/color RGBA

; 浏览器：矢量指令 → 图层 → GPU
; 导出：按目标分辨率栅格化
; 同一份 SVG 可输出任意尺寸""",
            "format": [
                ("浏览器", "矢量 → 图层 → GPU"),
                ("导出", "rsvg-convert / Inkscape / sharp"),
                ("格式", "PNG / WebP / PDF"),
                ("分辨率", "栅格化时决定"),
            ],
            "note": "SVG 的最终产物取决于使用方式：浏览器里是 DOM + 像素，导出时是特定分辨率的位图。",
        },
    ],
    "tools": [
        {"era": "2000s", "editor": "Inkscape / Illustrator", "compiler": "浏览器 / librsvg", "build": "—", "pkg": "—", "debug": "浏览器"},
        {"era": "2010s", "editor": "Inkscape / Figma", "compiler": "浏览器", "build": "SVGO", "pkg": "npm", "debug": "DevTools"},
        {"era": "2020s", "editor": "Figma / VS Code", "compiler": "浏览器 / resvg", "build": "SVGO / Vite", "pkg": "npm", "debug": "DevTools"},
    ],
    "hello": {
        "file": "hello.svg",
        "code": r"""<svg xmlns="http://www.w3.org/2000/svg" width="320" height="80" viewBox="0 0 320 80">
  <rect width="320" height="80" fill="#f3ede1"/>
  <text x="16" y="48" font-size="24" fill="#1c1a16">Hello, world</text>
</svg>""",
        "footprint": [
            {"stage": "SVG", "size": "≈ 230 B", "w": 6},
            {"stage": "DOM", "size": "3 个节点", "w": 7},
            {"stage": "场景", "size": "2 个图元", "w": 6},
            {"stage": "PNG 640", "size": "≈ 8 KB", "w": 20},
            {"stage": "像素", "size": "640 × 160", "w": 30},
        ],
        "why": [
            "<strong>矢量</strong>：几何在栅格化前保持精确，任意缩放。",
            "<strong>DOM</strong>：可被 CSS/JS 操作，能做交互与动画。",
            "<strong>viewBox</strong>：把用户坐标与视口解耦，响应式布局的基础。",
            "<strong>文本可访问</strong>：SVG 文本是可选中、可搜索的。",
        ],
    },
},

# ============================================================
"yaml": {
    "tagline": "人类可读的数据序列化格式，成了 Kubernetes、CI 与配置文件的通用语。",
    "intro": [
        "YAML（YAML Ain't Markup Language）由 Clark Evans、Ingy döt Net 与 Oren Ben-Kiki 在 2001 年设计。它用缩进与简洁标量表示嵌套数据，目标是让人读写配置时不必和括号、引号搏斗。",
        "YAML 1.2 是 JSON 的超集：合法 JSON 也是合法 YAML。它支持锚点、别名、多文档、块标量与流式写法，表达力强，但也因此有「隐式类型」与缩进陷阱。",
        "YAML 本身不执行任何东西。它的价值在于被工具消费：Kubernetes 清单、GitHub Actions、Docker Compose、Ansible、OpenAPI 都把它当作配置语言。",
    ],
    "lineage": {
        "from": ["JSON", "配置文件需求", "Perl / Python 数据结构"],
        "to": ["Kubernetes", "GitHub Actions", "Docker Compose", "Ansible"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.yaml",
            "cmd": "$ cat hello.yaml",
            "code": r"""message: Hello, world
service:
  name: hello
  replicas: 1
  ports:
    - 8080""",
            "format": [
                ("扩展名", ".yaml / .yml"),
                ("缩进", "空格，不能用 Tab"),
                ("标量", "字符串 / 数字 / 布尔 / null"),
                ("多文档", "--- 分隔"),
            ],
            "note": "YAML 的缩进是语法。两个空格与四个空格可能表示不同层级；Tab 通常会直接报错。",
        },
        {
            "label": "事件流",
            "file": "events",
            "cmd": "$ yq -P hello.yaml   # 或 YAML 解析器",
            "code": r"""STREAM-START
DOCUMENT-START
MAPPING-START
  KEY "message"  VALUE "Hello, world"
  KEY "service"  VALUE MAPPING-START
    KEY "name"     VALUE "hello"
    KEY "replicas" VALUE 1
    KEY "ports"    VALUE SEQUENCE-START
      VALUE 8080
    SEQUENCE-END
  MAPPING-END
MAPPING-END
DOCUMENT-END
STREAM-END

; 解析器把文本变成事件流
; 事件流再构建成节点树""",
            "format": [
                ("模型", "事件流 → 节点树"),
                ("节点", "Scalar / Mapping / Sequence"),
                ("锚点", "&anchor / *alias"),
                ("标签", "!!str / !!int 显式类型"),
            ],
            "note": "YAML 的解析分为扫描、解析、组合三步。事件流是理解缩进与锚点行为的中间层。",
        },
        {
            "label": "数据对象",
            "file": "JSON",
            "cmd": "$ yq -o=json hello.yaml",
            "code": r"""{
  "message": "Hello, world",
  "service": {
    "name": "hello",
    "replicas": 1,
    "ports": [8080]
  }
}

; YAML → JSON 是最常见的转换
; JSON 是 YAML 1.2 的子集
; 类型由标量与标签决定""",
            "format": [
                ("等价", "YAML 1.2 ⊃ JSON"),
                ("映射", "object / dict"),
                ("序列", "array / list"),
                ("类型", "隐式推断，易踩坑"),
            ],
            "note": "YAML 的隐式类型是常见坑：`country: NO` 在旧解析器里会变成布尔 false，而不是字符串 \"NO\"。必要时加引号。",
        },
        {
            "label": "被工具消费",
            "file": "manifest",
            "cmd": "$ kubectl apply -f hello.yaml",
            "code": r"""apiVersion: v1
kind: Pod
metadata:
  name: hello
spec:
  containers:
    - name: hello
      image: hello:latest
      ports:
        - containerPort: 8080

; YAML 本身不执行
; Kubernetes 定义 schema 与语义
; 同样的文本在 GitHub Actions / Compose 里含义不同""",
            "format": [
                ("消费者", "K8s / Actions / Compose / Ansible"),
                ("Schema", "由消费工具定义"),
                ("校验", "kubeconform / actionlint"),
                ("执行", "工具把对象应用到系统"),
            ],
            "note": "YAML 是「数据」，不是「程序」。同一份 YAML 在不同工具里可能有完全不同的含义，必须看对应 schema。",
        },
    ],
    "tools": [
        {"era": "2000s", "editor": "文本编辑器", "compiler": "YAML 解析器", "build": "—", "pkg": "—", "debug": "yamllint"},
        {"era": "2010s", "editor": "VS Code", "compiler": "PyYAML / libyaml", "build": "Ansible / Compose", "pkg": "—", "debug": "yamllint"},
        {"era": "2020s", "editor": "VS Code + YAML", "compiler": "yq / libyaml", "build": "kubectl / Helm / Actions", "pkg": "Helm", "debug": "kubeconform / actionlint"},
    ],
    "hello": {
        "file": "hello.yaml",
        "code": r"""message: Hello, world
service:
  name: hello
  replicas: 1
  ports:
    - 8080""",
        "footprint": [
            {"stage": "YAML", "size": "≈ 75 B", "w": 5},
            {"stage": "事件流", "size": "≈ 20 个事件", "w": 9},
            {"stage": "对象", "size": "≈ 4 个键", "w": 7},
            {"stage": "JSON", "size": "≈ 100 B", "w": 6},
            {"stage": "应用", "size": "由工具决定", "w": 20},
        ],
        "why": [
            "<strong>可读</strong>：缩进 + 简洁标量，适合人写配置。",
            "<strong>JSON 超集</strong>：能和 JSON 工具链互通。",
            "<strong>锚点 / 别名</strong>：复用重复配置，减少复制粘贴。",
            "<strong>生态</strong>：K8s、CI、Compose 把它变成基础设施的通用语。",
        ],
    },
},

# ============================================================
"markdown": {
    "tagline": "用纯文本写结构，渲染成 HTML；文档与代码终于能放在同一个仓库。",
    "intro": [
        "Markdown 由 John Gruber 在 2004 年发布，Aaron Swartz 参与了早期设计。它用少量符号（#、*、-、[]()）表示标题、强调、列表与链接，目标是「可读的纯文本」。",
        "Markdown 的解析器把文本变成 AST，再渲染成 HTML。CommonMark 在 2014 年统一了语法细节；GitHub Flavored Markdown 增加了表格、任务列表与删除线；MDX 允许在文档里直接写组件。",
        "它成了 README、文档站、博客与 issue 的默认格式。产物可以是 HTML、PDF、幻灯片，或一个静态站点。",
    ],
    "lineage": {
        "from": ["纯文本邮件", "Setext", "Textile"],
        "to": ["CommonMark", "GFM", "MDX", "静态站点生成器"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.md",
            "cmd": "$ cat hello.md",
            "code": r"""# Hello, world

This is **Markdown**.

- plain text
- readable source""",
            "format": [
                ("扩展名", ".md / .markdown / .mdx"),
                ("标题", "# 的个数表示级别"),
                ("强调", "*斜体* / **粗体**"),
                ("链接", "[text](url)"),
            ],
            "note": "Markdown 的设计目标是「不渲染也能读」。源文件本身就是一份可读的纯文本。",
        },
        {
            "label": "AST",
            "file": "AST",
            "cmd": "$ remark hello.md",
            "code": r"""Document
├─ Heading depth=1
│  └─ Text "Hello, world"
├─ Paragraph
│  ├─ Text "This is "
│  ├─ Strong
│  │  └─ Text "Markdown"
│  └─ Text "."
└─ List ordered=false
   ├─ ListItem → Text "plain text"
   └─ ListItem → Text "readable source\"""",
            "format": [
                ("解析", "markdown-it / remark / cmark"),
                ("节点", "Heading / Paragraph / Strong / List"),
                ("标准", "CommonMark"),
                ("扩展", "GFM / MDX / front matter"),
            ],
            "note": "不同解析器的扩展不同：表格、任务列表、脚注、数学公式都不是 CommonMark 核心。",
        },
        {
            "label": "HTML",
            "file": "hello.html",
            "cmd": "$ pandoc hello.md -o hello.html",
            "code": r"""<h1>Hello, world</h1>
<p>This is <strong>Markdown</strong>.</p>
<ul>
<li>plain text</li>
<li>readable source</li>
</ul>

; Markdown → HTML
; 也可以渲染成 PDF / 幻灯片 / Docx""",
            "format": [
                ("输出", "HTML"),
                ("转义", "HTML 特殊字符"),
                ("其它目标", "PDF / Docx / 幻灯片"),
                ("安全", "需要过滤原始 HTML"),
            ],
            "note": "Markdown 允许内嵌原始 HTML，这很灵活，也带来 XSS 风险。渲染用户内容时必须做净化。",
        },
        {
            "label": "渲染页面",
            "file": "site",
            "cmd": "$ npm run build   # VitePress / Astro / Docusaurus",
            "code": r"""$ npm run build
$ ls dist
index.html  assets/  ...

; 静态站点生成器：
;   Markdown → HTML → 主题 → 静态文件
; 产物可直接部署到 CDN
; MDX 还可以在文档里嵌入组件""",
            "format": [
                ("生成器", "VitePress / Astro / Docusaurus"),
                ("主题", "布局、导航、搜索"),
                ("产物", "静态 HTML + 资源"),
                ("部署", "CDN / Pages"),
            ],
            "note": "Markdown 的最终产物通常是一个静态站点。文档与代码在同一个仓库里，构建时一起生成。",
        },
    ],
    "tools": [
        {"era": "2000s", "editor": "文本编辑器", "compiler": "Markdown.pl", "build": "—", "pkg": "—", "debug": "预览"},
        {"era": "2010s", "editor": "VS Code / Typora", "compiler": "markdown-it / Pandoc", "build": "Jekyll / Hugo", "pkg": "npm", "debug": "预览"},
        {"era": "2020s", "editor": "VS Code / Obsidian", "compiler": "remark / MDX", "build": "VitePress / Astro", "pkg": "npm", "debug": "预览 / 构建日志"},
    ],
    "hello": {
        "file": "hello.md",
        "code": r"""# Hello, world

This is **Markdown**.""",
        "footprint": [
            {"stage": "Markdown", "size": "≈ 40 B", "w": 4},
            {"stage": "AST", "size": "≈ 8 个节点", "w": 7},
            {"stage": "HTML", "size": "≈ 70 B", "w": 5},
            {"stage": "页面", "size": "≈ 2 KB", "w": 12},
            {"stage": "站点", "size": "视项目而定", "w": 40},
        ],
        "why": [
            "<strong>纯文本</strong>：可 diff、可合并、可搜索。",
            "<strong>AST</strong>：解析器把文档变成树，便于转换与扩展。",
            "<strong>HTML</strong>：浏览器能直接渲染，也能转 PDF/Docx。",
            "<strong>静态站点</strong>：文档与代码同仓库，构建即发布。",
        ],
    },
},

# ============================================================
"sass": {
    "tagline": "给 CSS 加变量、嵌套、混入与模块，再编译回普通 CSS。",
    "intro": [
        "Sass（Syntactically Awesome Style Sheets）由 Hampton Catlin 在 2006 年创建，Natalie Weizenbaum 后来主导了 SCSS 语法与实现。它是最早流行的 CSS 预处理器之一。",
        "Sass 增加了变量、嵌套、混入（mixin）、函数、模块（@use）与条件/循环。浏览器不认识这些语法，所以必须编译成普通 CSS。",
        "Dart Sass 是今天的官方实现；CSS 自定义属性与原生嵌套减少了部分需求，但 Sass 在大型设计系统里仍然常见。",
    ],
    "lineage": {
        "from": ["CSS", "Ruby（早期实现）", "Haml 社区"],
        "to": ["SCSS", "Dart Sass", "设计系统工具链"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.scss",
            "cmd": "$ cat hello.scss",
            "code": r"""$message: "Hello, world";

.greeting {
  &::before {
    content: $message;
    display: block;
  }
}""",
            "format": [
                ("扩展名", ".scss / .sass"),
                ("变量", "$name"),
                ("嵌套", "& 表示父选择器"),
                ("模块", "@use / @forward"),
            ],
            "note": "SCSS 是 CSS 的超集：合法 CSS 也是合法 SCSS。`.sass` 则是缩进语法，不写大括号与分号。",
        },
        {
            "label": "AST",
            "file": "AST",
            "cmd": "$ sass --dump-ast hello.scss",
            "code": r"""Stylesheet
├─ VariableDeclaration $message = "Hello, world"
└─ StyleRule .greeting
   └─ StyleRule &::before
      ├─ Declaration content: $message
      └─ Declaration display: block

; 变量在编译期解析
; 嵌套在编译期展开
; 混入在编译期复制""",
            "format": [
                ("节点", "Stylesheet / Rule / Declaration"),
                ("变量", "编译期替换"),
                ("嵌套", "展开成后代选择器"),
                ("混入", "复制声明块"),
            ],
            "note": "Sass 的「魔法」都发生在编译期：变量、嵌套、混入、函数最终都会消失，只剩 CSS。",
        },
        {
            "label": "编译 CSS",
            "file": "hello.css",
            "cmd": "$ sass hello.scss hello.css",
            "code": r""".greeting::before {
  content: "Hello, world";
  display: block;
}

/*# sourceMappingURL=hello.css.map */

; 嵌套已展开
; 变量已替换
; 可加 --style=compressed""",
            "format": [
                ("输出", "普通 CSS"),
                ("source map", "指回 .scss 行号"),
                ("压缩", "--style=compressed"),
                ("兼容", "autoprefixer / postcss"),
            ],
            "note": "Sass 的产物是标准 CSS，浏览器不需要知道 Sass 的存在。source map 让调试仍能指回源文件。",
        },
        {
            "label": "CSSOM / 布局",
            "file": "CSSOM",
            "cmd": "DevTools → Styles",
            "code": r"""CSSStyleSheet
└─ CSSStyleRule
   selectorText: ".greeting::before"
   style:
     content: "Hello, world"
     display: block

; 之后与普通 CSS 相同：
;   CSSOM → 计算样式 → 布局 → 绘制""",
            "format": [
                ("输入", "编译后的 CSS"),
                ("后续", "CSSOM → 布局 → 绘制"),
                ("调试", "source map"),
                ("产物", "像素"),
            ],
            "note": "Sass 不改变渲染模型，只改变「写 CSS 的方式」。最终仍然汇入同一条 CSS 流水线。",
        },
    ],
    "tools": [
        {"era": "2000s", "editor": "TextMate", "compiler": "Ruby Sass", "build": "Compass", "pkg": "RubyGems", "debug": "浏览器"},
        {"era": "2010s", "editor": "VS Code / CodeKit", "compiler": "LibSass / node-sass", "build": "Gulp / webpack", "pkg": "npm", "debug": "source map"},
        {"era": "2020s", "editor": "VS Code", "compiler": "Dart Sass", "build": "Vite / PostCSS", "pkg": "npm", "debug": "DevTools"},
    ],
    "hello": {
        "file": "hello.scss",
        "code": r"""$message: "Hello, world";

.greeting::before {
  content: $message;
}""",
        "footprint": [
            {"stage": "SCSS", "size": "≈ 70 B", "w": 4},
            {"stage": "AST", "size": "≈ 5 个节点", "w": 6},
            {"stage": "CSS", "size": "≈ 55 B", "w": 4},
            {"stage": "CSSOM", "size": "1 条规则", "w": 5},
            {"stage": "像素", "size": "视口大小", "w": 55},
        ],
        "why": [
            "<strong>变量</strong>：颜色、字号、间距集中管理。",
            "<strong>嵌套</strong>：让选择器结构与 DOM 结构对应。",
            "<strong>混入 / 函数</strong>：复用声明块与计算。",
            "<strong>模块</strong>：@use 让大型样式表可拆分、可命名空间。",
        ],
    },
},

# ============================================================
"less": {
    "tagline": "更早的 CSS 预处理器之一：变量、混入与嵌套，语法接近原生 CSS。",
    "intro": [
        "Less 由 Alexis Sellier 在 2009 年发布，受 Sass 影响，但语法更接近 CSS。它引入了 `@variable`、混入、嵌套与运算，并能在浏览器或 Node.js 里编译。",
        "Bootstrap 在 2.x/3.x 时代使用 Less，这让它获得了大量用户；4.x 之后 Bootstrap 转向 Sass。今天 Less 主要出现在遗留项目与部分工具链里。",
        "和 Sass 一样，Less 最终编译成普通 CSS；浏览器不需要 Less 运行时（除非用 less.js 在客户端编译，不推荐生产）。",
    ],
    "lineage": {
        "from": ["CSS", "Sass（早期影响）", "Bootstrap 生态"],
        "to": ["CSS 预处理器生态", "遗留前端项目"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.less",
            "cmd": "$ cat hello.less",
            "code": r"""@message: "Hello, world";

.greeting {
  &::before {
    content: @message;
    display: block;
  }
}""",
            "format": [
                ("扩展名", ".less"),
                ("变量", "@name"),
                ("嵌套", "& 父选择器"),
                ("混入", ".mixin() / .mixin;"),
            ],
            "note": "Less 的变量用 `@`，与 Sass 的 `$` 不同。语法整体更接近原生 CSS，迁移成本低。",
        },
        {
            "label": "AST",
            "file": "AST",
            "cmd": "$ lessc --lint hello.less",
            "code": r"""Ruleset .greeting
└─ Ruleset &::before
   ├─ Declaration content: @message
   └─ Declaration display: block
Variable @message = "Hello, world"

; 变量在编译期解析
; 作用域：后定义可覆盖前定义
; 混入在编译期展开""",
            "format": [
                ("节点", "Ruleset / Declaration / Variable"),
                ("作用域", "词法 + 延迟求值"),
                ("混入", "复制规则集"),
                ("导入", "@import"),
            ],
            "note": "Less 的变量是延迟求值的：同一个作用域里后定义的变量可能影响前面的使用。",
        },
        {
            "label": "编译 CSS",
            "file": "hello.css",
            "cmd": "$ lessc hello.less hello.css",
            "code": r""".greeting::before {
  content: "Hello, world";
  display: block;
}

/*# sourceMappingURL=hello.css.map */

; 嵌套已展开
; 变量已替换
; 可加 --clean-css 压缩""",
            "format": [
                ("输出", "普通 CSS"),
                ("source map", "指回 .less"),
                ("压缩", "clean-css"),
                ("兼容", "autoprefixer"),
            ],
            "note": "Less 编译后的 CSS 与手写 CSS 没有区别。它的价值在编写阶段，而不是运行阶段。",
        },
        {
            "label": "CSSOM / 布局",
            "file": "CSSOM",
            "cmd": "DevTools → Styles",
            "code": r"""CSSStyleSheet
└─ CSSStyleRule
   selectorText: ".greeting::before"
   style:
     content: "Hello, world"
     display: block

; 之后与普通 CSS 相同：
;   CSSOM → 计算样式 → 布局 → 绘制""",
            "format": [
                ("输入", "编译后的 CSS"),
                ("后续", "CSSOM → 布局 → 绘制"),
                ("调试", "source map"),
                ("产物", "像素"),
            ],
            "note": "Less 与 Sass 一样，不改变浏览器渲染模型，只改变样式表的组织方式。",
        },
    ],
    "tools": [
        {"era": "2000s", "editor": "文本编辑器", "compiler": "less.js", "build": "—", "pkg": "npm", "debug": "浏览器"},
        {"era": "2010s", "editor": "WebStorm / VS Code", "compiler": "lessc", "build": "Grunt / Gulp / webpack", "pkg": "npm", "debug": "source map"},
        {"era": "2020s", "editor": "VS Code", "compiler": "lessc", "build": "Vite / webpack", "pkg": "npm", "debug": "DevTools"},
    ],
    "hello": {
        "file": "hello.less",
        "code": r"""@message: "Hello, world";

.greeting::before {
  content: @message;
}""",
        "footprint": [
            {"stage": "Less", "size": "≈ 65 B", "w": 4},
            {"stage": "AST", "size": "≈ 4 个节点", "w": 6},
            {"stage": "CSS", "size": "≈ 55 B", "w": 4},
            {"stage": "CSSOM", "size": "1 条规则", "w": 5},
            {"stage": "像素", "size": "视口大小", "w": 55},
        ],
        "why": [
            "<strong>语法接近 CSS</strong>：迁移成本低，学习曲线平缓。",
            "<strong>变量</strong>：集中管理颜色与尺寸。",
            "<strong>混入</strong>：复用声明块。",
            "<strong>浏览器编译</strong>：less.js 可在客户端运行，但生产环境通常预编译。",
        ],
    },
},

}

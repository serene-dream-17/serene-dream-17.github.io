# 由 tools/verify.py 生成；只包含本机真正跑通的条目。

VERIFIED = {
  "c": {
    "tool": "gcc.EXE (GCC) 16.2.0",
    "command": "gcc -O0 hello.c -o hello.exe && hello.exe",
    "output": "Hello, world",
    "artifacts": [
      "hello.exe · 49876 B · 首字节 4d 5a 90 00",
      "hello.o · 866 B · 首字节 64 86 07 00"
    ],
    "note": "本机为 Windows/MinGW，目标格式是 PE/COFF；页面中的 ELF 样例是 Linux 口径。",
    "date": "2026-10-28"
  },
  "cpp": {
    "tool": "g++.EXE (GCC) 16.2.0",
    "command": "g++ -O0 hello.cpp -o hello.exe && hello.exe",
    "output": "Hello, world",
    "artifacts": [
      "hello.exe · 2594870 B · 首字节 4d 5a 90 00"
    ],
    "note": "Windows/MinGW 生成 PE；与页面中的 Linux ELF 阶段对应，但目标格式不同。",
    "date": "2026-10-28"
  },
  "python": {
    "tool": "Python 3.11.9",
    "command": "python hello.py && python -m py_compile hello.py",
    "output": "Hello, world",
    "artifacts": [
      "__pycache__/hello.cpython-311.pyc · 169 B · 魔数 a7 0d 0d 0a"
    ],
    "note": ".pyc 的魔数与解释器版本绑定，跨版本不兼容。",
    "date": "2026-10-28"
  },
  "javascript": {
    "tool": "v24.14.0",
    "command": "node hello.js",
    "output": "Hello, world",
    "artifacts": [
      "源码直接由 V8 解析执行；本机未落盘字节码。"
    ],
    "note": "V8 的字节码是内存中的实现细节，不是可分发文件。",
    "date": "2026-10-28"
  },
  "java": {
    "tool": "javac 21.0.4",
    "command": "javac Hello.java && java Hello",
    "output": "Hello, world",
    "artifacts": [
      "Hello.class · 412 B · 魔数 ca fe ba be"
    ],
    "note": "CAFEBABE 魔数与常量池可在 .class 中直接验证。",
    "date": "2026-10-28"
  },
  "csharp": {
    "tool": "10.0.401",
    "command": "dotnet run hello.cs",
    "output": "Hello, world",
    "artifacts": [
      "文件式程序由 .NET SDK 编译并执行；本机未保留中间程序集。"
    ],
    "note": "页面中的 CIL/程序集阶段由 Roslyn 与 CLR 完成；这里验证的是源码到运行结果。",
    "date": "2026-10-28"
  },
  "shell": {
    "tool": "GNU bash, version 4.4.23(1)-release (x86_64-pc-msys)",
    "command": "bash hello.sh",
    "output": "Hello, world",
    "artifacts": [
      "脚本直接由 shell 解析；无目标文件。"
    ],
    "note": "Shell 没有编译产物；解析、展开与 execve 是可观察的中间层。",
    "date": "2026-10-28"
  },
  "sql": {
    "tool": "sqlite3 3.45.1（Python 3.11.9）",
    "command": "SELECT 'Hello, world';",
    "output": "Hello, world",
    "artifacts": [
      "内存数据库；查询计划与结果集由 SQLite 生成。"
    ],
    "note": "SQL 的产物是结果集与执行计划，不是可执行文件。",
    "date": "2026-10-28"
  },
  "html": {
    "tool": "Chromium 156.0.8078.47",
    "command": "在浏览器中打开 hello.html",
    "output": "Hello, world",
    "artifacts": [
      "DOM 元素 6 个；渲染树/布局/绘制由浏览器完成。"
    ],
    "note": "HTML 的产物是 DOM 与像素，不是文件。",
    "date": "2026-10-28"
  },
  "css": {
    "tool": "Chromium 156.0.8078.47",
    "command": "打开 hello.html，读取 getComputedStyle(.g, '::before')",
    "output": "content: \"Hello, world\" · color: rgb(140, 51, 36)",
    "artifacts": [
      "CSSOM 与计算样式由浏览器生成；没有目标文件。"
    ],
    "note": "CSS 的产物是计算样式与像素。",
    "date": "2026-10-28"
  },
  "fortran": {
    "tool": "GNU Fortran (GCC) 16.2.0",
    "command": "gfortran -O0 hello.f90 -o hello.exe && hello.exe",
    "output": "Hello, world",
    "artifacts": [
      "hello.o · 1455 B · 首字节 64 86 07 00",
      "hello.exe · 674288 B · 首字节 4d 5a 90 00"
    ],
    "note": "Windows/MinGW 生成 PE/COFF；页面中的 ELF 样例是 Linux 口径。",
    "date": "2026-10-28"
  },
  "go": {
    "tool": "go version go1.26.2 windows/amd64",
    "command": "go run hello.go && go build -o hello.exe hello.go",
    "output": "Hello, world",
    "artifacts": [
      "hello.exe · 2458112 B · 首字节 4d 5a 90 00",
      "hello.exe: go1.26.2"
    ],
    "note": "Go 默认静态链接运行时与标准库；Windows 目标为 PE，Linux 目标为 ELF。",
    "date": "2026-10-28"
  },
  "xml": {
    "tool": "lxml 6.1.0",
    "command": "lxml.etree.parse('hello.xml')",
    "output": "Hello, world",
    "artifacts": [
      "根元素 greeting，节点 2 个，序列化长度 56 字符"
    ],
    "note": "XML 的产物是 DOM/元素树与应用数据；这里验证解析与取值。",
    "date": "2026-10-28"
  },
  "yaml": {
    "tool": "PyYAML 6.0.3",
    "command": "yaml.safe_load(hello.yaml)",
    "output": "Hello, world",
    "artifacts": [
      "解析为对象：{\"message\": \"Hello, world\", \"service\": {\"name\": \"hello\", \"replicas\": 1}}"
    ],
    "note": "YAML 本身不执行；产物是被工具消费的数据对象。",
    "date": "2026-10-28"
  },
  "sass": {
    "tool": "1.86.0 compiled with dart2js 3.7.2",
    "command": "sass hello.scss hello.css",
    "output": ".greeting::before {\n  content: \"Hello, world\";\n}\n\n/*# sourceMappingURL=hello.css.map */",
    "artifacts": [
      "hello.css · 88 B",
      "编译结果：.greeting::before {\n  content: \"Hello, world\";\n}\n\n/*# sourceMappingURL=hello.css.map */"
    ],
    "note": "Sass 的产物是普通 CSS；浏览器不需要 Sass 运行时。",
    "date": "2026-10-28"
  },
  "svg": {
    "tool": "Chromium 156.0.8078.47",
    "command": "在浏览器中打开 hello.svg",
    "output": "Hello, world",
    "artifacts": [
      "SVG 子元素 2 个；矢量图元由浏览器栅格化。"
    ],
    "note": "SVG 的产物是 DOM/场景图与像素。",
    "date": "2026-10-28"
  }
}

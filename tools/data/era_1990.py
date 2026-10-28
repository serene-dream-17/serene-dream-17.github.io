# -*- coding: utf-8 -*-
"""第二批 · 1990s：11 门语言的档案与产物链数据。"""

LANGS = {

# ============================================================
"python": {
    "tagline": "可读性优先的脚本语言，最后成了科学计算与 AI 的默认语言。",
    "intro": [
        "Python 由 Guido van Rossum 在 1989 年圣诞节前后开始写，1991 年发布 0.9.0。它的目标不是最快，而是让代码容易读：用缩进表示块、用显式的 import、用一套统一的协议（迭代、上下文管理器）把语言变小。",
        "Python 的产物链分为两条：解释执行时，源码被解析成 AST，再编译成字节码，缓存为 `.pyc`；分发时，`.pyz`（zipapp）或 PyInstaller 把字节码与解释器打包成可执行文件。",
        "`__pycache__` 里的 `.pyc` 是带版本魔数的 marshal 数据，不能跨 Python 版本使用。理解这一点，就能理解为什么容器镜像里总要锁定 Python 小版本。",
    ],
    "lineage": {
        "from": ["ABC", "Modula-3", "C"],
        "to": ["JavaScript（部分）", "Julia", "Mojo", "PyTorch 生态"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.py",
            "cmd": "$ cat hello.py",
            "code": r"""def hello():
    print("Hello, world")

hello()""",
            "format": [
                ("扩展名", ".py / .pyw"),
                ("编码", "默认 UTF-8"),
                ("块", "缩进，不用大括号"),
                ("执行", "自上而下，函数定义也是语句"),
            ],
            "note": "Python 没有单独的声明区：`def` 是运行时执行的语句，模块被导入时才创建函数对象。",
        },
        {
            "label": "AST",
            "file": "ast",
            "cmd": "$ python -c \"import ast; print(ast.dump(ast.parse(open('hello.py').read()), indent=2))\"",
            "code": r"""Module(
  body=[
    FunctionDef(
      name='hello',
      args=arguments(...),
      body=[
        Expr(
          value=Call(
            func=Name(id='print', ctx=Load()),
            args=[Constant(value='Hello, world')],
            keywords=[]))]),
    Expr(
      value=Call(
        func=Name(id='hello', ctx=Load()),
        args=[], keywords=[]))])""",
            "format": [
                ("AST", "抽象语法树，标准库 ast 可读"),
                ("节点", "Module / FunctionDef / Call / Constant"),
                ("用途", "静态分析、改写、代码生成"),
                ("编译", "AST → 字节码，发生在导入时"),
            ],
            "note": "Python 的 AST 是公开、稳定的接口。linter、格式化工具、代码改写工具都在这一层工作。",
        },
        {
            "label": "字节码",
            "file": "__pycache__/hello.cpython-311.pyc",
            "cmd": "$ python -m py_compile hello.py && xxd -l 16 __pycache__/hello.cpython-311.pyc",
            "code": r"""$ xxd -l 16 __pycache__/hello.cpython-311.pyc
00000000: a70d 0d0a 0000 0000 6812 6a66 1a00 0000  ........h.jf....

; 头部：magic(4) + flags(4) + mtime(4) + source_size(4)
; 之后是 marshal 序列化的 code object

$ python -m dis hello.py
  1           0 RESUME                   0
  2           2 LOAD_GLOBAL              1 (NULL + print)
             12 LOAD_CONST               1 ('Hello, world')
             14 CALL                     1
             22 POP_TOP
             24 RETURN_VALUE""",
            "format": [
                ("魔数", "每个 Python 版本不同（示例 3.11）"),
                ("头", "flags / mtime / 源文件大小"),
                ("主体", "marshal 编码的 code object"),
                ("缓存", "__pycache__/*.cpython-311.pyc"),
            ],
            "note": "`.pyc` 不是可移植字节码：魔数、字节码指令、marshal 格式都可能随版本变化。删掉它，Python 会重新生成。",
        },
        {
            "label": "打包",
            "file": "hello.pyz / hello",
            "cmd": "$ python -m zipapp app -o hello.pyz -p \"/usr/bin/env python3\"",
            "code": r"""$ python -m zipapp app -o hello.pyz -p "/usr/bin/env python3"
$ unzip -l hello.pyz
  __main__.py
$ ./hello.pyz
Hello, world

; 另一条路：PyInstaller
$ pyinstaller --onefile hello.py
$ file dist/hello
dist/hello: ELF 64-bit LSB executable, x86-64 ...

; PyInstaller 把解释器 + 字节码 + 库塞进一个自解压程序""",
            "format": [
                (".pyz", "zip 归档 + __main__.py，需要 Python"),
                ("PyInstaller", "引导程序 + 打包的运行时"),
                ("体积", "单文件通常 6–15 MB"),
                ("解包", "运行时释放到临时目录（_MEIPASS）"),
            ],
            "note": "zipapp 只是换了容器，仍需目标机有 Python；PyInstaller 才把解释器一起带上。",
        },
    ],
    "tools": [
        {"era": "1990s", "editor": "Emacs / IDLE", "compiler": "CPython 解释器", "build": "make", "pkg": "distutils", "debug": "pdb"},
        {"era": "2000s", "editor": "vim / Eclipse PyDev", "compiler": "CPython 2.x", "build": "setuptools", "pkg": "pip", "debug": "pdb"},
        {"era": "2010s", "editor": "PyCharm / VS Code", "compiler": "CPython 3.x", "build": "setuptools / poetry", "pkg": "pip / conda", "debug": "pdb / ipdb"},
        {"era": "2020s", "editor": "VS Code + Pylance", "compiler": "CPython 3.12 / PyPy", "build": "uv / poetry / hatch", "pkg": "pip / uv / conda", "debug": "debugpy"},
    ],
    "hello": {
        "file": "hello.py",
        "code": r"""print("Hello, world")""",
        "footprint": [
            {"stage": "源码", "size": "≈ 22 B", "w": 4},
            {"stage": "AST", "size": "≈ 500 B", "w": 10},
            {"stage": ".pyc", "size": "≈ 300 B", "w": 9},
            {"stage": ".pyz", "size": "≈ 1 KB", "w": 12},
            {"stage": "PyInstaller", "size": "≈ 8 MB", "w": 80},
            {"stage": "+ 解释器", "size": "≈ 30 MB", "w": 100},
        ],
        "why": [
            "<strong>AST</strong>：公开的语法树，工具链在这一层做分析、改写与生成。",
            "<strong>字节码</strong>：导入时编译，缓存到 __pycache__，下次跳过解析。",
            "<strong>版本魔数</strong>：.pyc 绑定解释器版本，跨版本必须重新编译。",
            "<strong>打包</strong>：zipapp 只换容器；PyInstaller 连解释器一起带走。",
        ],
    },
},

# ============================================================
"java": {
    "tagline": "一次编写，到处运行：源码先编译成字节码，再由虚拟机执行。",
    "intro": [
        "Java 由 James Gosling 等人在 Sun 于 1991 年开始设计，1995 年公开发布。它把 C++ 的语法简化，去掉指针与多重继承，留下类、接口、异常与垃圾回收，目标是把「平台差异」关进虚拟机里。",
        "Java 的产物链是教科书式的两段式：`javac` 把源码编译成 `.class`（CAFEBABE 开头，含常量池与栈式字节码），`.jar` 只是 zip 容器，运行时由 JVM 加载、验证、解释，再由 JIT 编译热点。",
        "Android 走了另一条支线：`.class` 先合并成 `.dex`，由 ART 执行。同一个 Java 源码，可以落到两种完全不同的运行时格式。",
    ],
    "lineage": {
        "from": ["C++", "Smalltalk（GC/VM）", "Ada（部分）"],
        "to": ["C#", "Kotlin", "Scala", "Android 生态"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "Hello.java",
            "cmd": "$ cat Hello.java",
            "code": r"""public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, world");
    }
}""",
            "format": [
                ("扩展名", ".java"),
                ("结构", "一个文件一个 public 类"),
                ("入口", "public static void main(String[])"),
                ("编译", "javac 生成 .class"),
            ],
            "note": "Java 的类名必须与文件名一致（public 类）。源文件是编译单元，.class 是加载单元。",
        },
        {
            "label": "字节码",
            "file": "Hello.class",
            "cmd": "$ javac Hello.java && javap -c -v Hello",
            "code": r"""$ xxd -l 8 Hello.class
00000000: cafe babe 0000 0037                       .......7

$ javap -c -v Hello | head -30
Classfile Hello.class
  magic: CAFEBABE
  minor: 0
  major: 55
Constant pool:
  #1 = Methodref  #2.#3   // java/lang/Object."<init>":()V
  #7 = String     #8      // Hello, world
  #9 = Fieldref   #10.#12 // java/lang/System.out
...
public static void main(java.lang.String[]);
  Code:
     0: getstatic     #9  // Field System.out
     3: ldc           #7  // String Hello, world
     5: invokevirtual #15 // Method PrintStream.println
     8: return""",
            "format": [
                ("魔数", "CAFEBABE"),
                ("版本", "major 55 = Java 11"),
                ("常量池", "符号、字符串、类引用"),
                ("字节码", "栈式指令，如 getstatic / ldc"),
            ],
            "note": "`.class` 里的方法体不是机器码，而是栈式字节码。JVM 负责验证类型安全，再决定解释还是 JIT。",
        },
        {
            "label": "JAR",
            "file": "hello.jar",
            "cmd": "$ jar --create --file hello.jar --main-class Hello Hello.class",
            "code": r"""$ jar --create --file hello.jar --main-class Hello Hello.class
$ unzip -l hello.jar
  META-INF/MANIFEST.MF
  Hello.class

$ unzip -p hello.jar META-INF/MANIFEST.MF
Manifest-Version: 1.0
Main-Class: Hello

$ java -jar hello.jar
Hello, world""",
            "format": [
                ("容器", "zip"),
                ("清单", "META-INF/MANIFEST.MF"),
                ("Main-Class", "指定入口类"),
                ("依赖", "可用 Class-Path 或外部构建工具"),
            ],
            "note": "JAR 没有新格式，就是 zip + 清单。构建工具（Maven/Gradle）负责把依赖与清单拼进去。",
        },
        {
            "label": "DEX（Android）",
            "file": "classes.dex",
            "cmd": "$ d8 --output dex hello.jar",
            "code": r"""$ d8 --output dex hello.jar
$ xxd -l 8 classes.dex
00000000: 6465 780a 3033 3500                    dex\n035.

; dex = Dalvik Executable
; 寄存器式字节码（不是 JVM 的栈式）
; 多个 .class 合并、去重、重排
; ART 在安装时 AOT 编译，运行时 JIT""",
            "format": [
                ("魔数", "dex\\n035\\0"),
                ("字节码", "寄存器式，Dalvik/ART"),
                ("来源", ".class → d8 → .dex"),
                ("执行", "ART：AOT + JIT"),
            ],
            "note": "Android 不运行 JVM 字节码。d8 把栈式 .class 转成寄存器式 .dex，这是同一门语言在另一条运行时上的产物。",
        },
    ],
    "tools": [
        {"era": "1990s", "editor": "vi / Emacs", "compiler": "javac", "build": "make", "pkg": "—", "debug": "jdb"},
        {"era": "2000s", "editor": "Eclipse / IntelliJ", "compiler": "javac", "build": "Ant / Maven", "pkg": "Maven Central", "debug": "jdb / IDE"},
        {"era": "2010s", "editor": "IntelliJ IDEA", "compiler": "javac", "build": "Gradle / Maven", "pkg": "Maven Central", "debug": "IDE 调试器"},
        {"era": "2020s", "editor": "IntelliJ / VS Code", "compiler": "javac / ecj", "build": "Gradle / Maven", "pkg": "Maven Central", "debug": "JDWP"},
    ],
    "hello": {
        "file": "Hello.java",
        "code": r"""public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, world");
    }
}""",
        "footprint": [
            {"stage": "源码", "size": "≈ 120 B", "w": 5},
            {"stage": ".class", "size": "≈ 420 B", "w": 10},
            {"stage": ".jar", "size": "≈ 1.5 KB", "w": 14},
            {"stage": ".dex", "size": "≈ 1.1 KB", "w": 13},
            {"stage": "+ JVM/ART", "size": "≈ 40–200 MB", "w": 100},
        ],
        "why": [
            "<strong>CAFEBABE</strong>：类文件有固定魔数与版本，JVM 在加载时检查。",
            "<strong>常量池</strong>：符号引用集中存放，链接时才解析成内存地址。",
            "<strong>JAR</strong>：zip + 清单，把多个 .class 与资源装成一个分发单位。",
            "<strong>DEX</strong>：Android 把栈式字节码转成寄存器式，适配 ART。",
        ],
    },
},

# ============================================================
"javascript": {
    "tagline": "十天写出来的浏览器脚本，最后统治了前端与服务端。",
    "intro": [
        "JavaScript 由 Brendan Eich 在 Netscape 于 1995 年用十天左右设计完成，最初叫 Mocha，后改名 LiveScript，最终借 Java 的势头叫 JavaScript。它的语法借了 Java，函数式能力借了 Scheme，原型继承借了 Self。",
        "JS 没有标准的字节码文件。引擎（V8、SpiderMonkey、JavaScriptCore）各自把源码解析成 AST，再编译成内部字节码，热点函数由 JIT 编译成机器码；V8 还能把启动状态保存成 snapshot。",
        "真正跨引擎的标准只有语法与语义（ECMAScript），以及 AST 的事实标准 ESTree。至于字节码长什么样，取决于你跑在哪个引擎、哪个版本。",
    ],
    "lineage": {
        "from": ["Java（语法）", "Scheme（函数）", "Self（原型）"],
        "to": ["TypeScript", "Node.js 生态", "WebAssembly（互补）"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.js",
            "cmd": "$ cat hello.js",
            "code": r"""function hello() {
  console.log("Hello, world");
}

hello();""",
            "format": [
                ("扩展名", ".js / .mjs / .cjs"),
                ("类型", "动态、弱类型"),
                ("函数", "一等对象，可闭包"),
                ("标准", "ECMAScript（每年更新）"),
            ],
            "note": "JS 的源码没有类型标注；变量、函数、对象都可以在运行时改变形状。引擎会为这些变化做隐藏类与内联缓存。",
        },
        {
            "label": "AST",
            "file": "ESTree",
            "cmd": "$ node --print-ast hello.js   # 或 acorn / babel",
            "code": r"""Program
  body:
    FunctionDeclaration
      id: Identifier "hello"
      body: BlockStatement
        ExpressionStatement
          CallExpression
            callee: MemberExpression
              object: Identifier "console"
              property: Identifier "log"
            arguments: [ Literal "Hello, world" ]
    ExpressionStatement
      CallExpression
        callee: Identifier "hello"
        arguments: []""",
            "format": [
                ("标准", "ESTree（事实标准）"),
                ("节点", "Program / FunctionDeclaration / CallExpression"),
                ("用途", "Babel、ESLint、打包器、压缩器"),
                ("解析器", "Acorn、Babel、SWC、oxc"),
            ],
            "note": "前端工具链几乎都从 AST 开始：转译、lint、tree-shaking、压缩，都是对 AST 的变换。",
        },
        {
            "label": "字节码",
            "file": "V8 Ignition",
            "cmd": "$ node --print-bytecode --print-bytecode-filter=hello hello.js",
            "code": r"""[generated bytecode for function: hello]
Parameter count 1
Frame size 24
   0 E> 0x... @    0 : 13 00             LdaConstant [0]
   2 E> 0x... @    2 : 19 01             Star1
   4 E> 0x... @    4 : 2d 03 00 00       LdaNamedProperty a0, [3]
   ...
   ...                               CallProperty
   ...                               LdaUndefined
   ...                               Return

; V8 的字节码不落盘，只在内存中
; 指令名与编码随 V8 版本变化""",
            "format": [
                ("引擎", "V8 Ignition（解释器）"),
                ("形态", "寄存器/累加器式字节码"),
                ("存储", "内存，不生成标准文件"),
                ("热点", "TurboFan 编译为机器码"),
            ],
            "note": "同一段 JS 在 SpiderMonkey 或 JavaScriptCore 里的字节码完全不同。它不是规范的一部分。",
        },
        {
            "label": "JIT 与快照",
            "file": "snapshot / 机器码",
            "cmd": "$ node --trace-opt hello.js",
            "code": r"""$ node --trace-opt hello.js
[marking 0x... <JSFunction hello (sfi = 0x...)> for optimization]
[compiling method 0x... <JSFunction hello> using TurboFan]

; 启动快照
$ node --build-snapshot hello.js
$ node --snapshot-blob snapshot.blob

; 快照 = 堆 + 已编译代码的序列化
; 与 V8 版本、平台强绑定""",
            "format": [
                ("JIT", "TurboFan / Maglev / Sparkplug"),
                ("优化", "类型反馈、内联缓存、去优化"),
                ("快照", "V8 startup snapshot"),
                ("绑定", "版本与平台强相关"),
            ],
            "note": "JS 的性能来自运行时反馈：先解释，收集类型信息，再编译。去优化（deopt）是这套机制的代价。",
        },
    ],
    "tools": [
        {"era": "1990s", "editor": "文本编辑器", "compiler": "浏览器解释器", "build": "—", "pkg": "—", "debug": "alert / Firebug 前身"},
        {"era": "2000s", "editor": "Dreamweaver / 记事本", "compiler": "各浏览器引擎", "build": "—", "pkg": "—", "debug": "Firebug / 开发者工具"},
        {"era": "2010s", "editor": "VS Code / WebStorm", "compiler": "V8 / JSC", "build": "webpack / gulp", "pkg": "npm", "debug": "Chrome DevTools"},
        {"era": "2020s", "editor": "VS Code + TypeScript", "compiler": "V8 / JSC / SpiderMonkey", "build": "Vite / esbuild / Turbopack", "pkg": "npm / pnpm", "debug": "DevTools / node --inspect"},
    ],
    "hello": {
        "file": "hello.js",
        "code": r"""console.log("Hello, world");""",
        "footprint": [
            {"stage": "源码", "size": "≈ 28 B", "w": 4},
            {"stage": "AST", "size": "≈ 1.5 KB", "w": 14},
            {"stage": "字节码", "size": "≈ 400 B", "w": 10},
            {"stage": "机器码", "size": "≈ 1 KB", "w": 12},
            {"stage": "快照", "size": "≈ 30 MB", "w": 90},
        ],
        "why": [
            "<strong>AST</strong>：跨引擎的事实标准，支撑 Babel/ESLint/打包器。",
            "<strong>字节码</strong>：引擎内部格式，不落盘、不跨引擎。",
            "<strong>JIT</strong>：用运行时类型反馈换性能，热点函数才编译。",
            "<strong>快照</strong>：把堆与已编译代码序列化，缩短启动时间。",
        ],
    },
},

# ============================================================
"php": {
    "tagline": "为个人主页写的小工具，最后跑起了大半个早期 Web。",
    "intro": [
        "PHP 由 Rasmus Lerdorf 在 1994–1995 年用 C 写成，最初是一组统计访问量的 CGI 脚本（Personal Home Page Tools），后来重写成 PHP/FI，再经过 Zeev Suraski 与 Andi Gutmans 的重构，成为 PHP 3/4/5/7/8。",
        "PHP 是请求驱动的：每个请求重新执行脚本，编译成 opcode 数组后交给 Zend 虚拟机。opcache 把 opcode 缓存在共享内存里，避免每次重新编译；但 PHP 没有标准的可分发字节码文件。",
        "分发层面，PHAR 把脚本与资源打成一个归档，Composer 管依赖。需要独立二进制时，可以用 FrankenPHP、RoadRunner 或静态编译的 PHP。",
    ],
    "lineage": {
        "from": ["C", "Perl（字符串/正则）", "CGI"],
        "to": ["Hack", "Laravel 生态", "WordPress 生态"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.php",
            "cmd": "$ cat hello.php",
            "code": r"""<?php
declare(strict_types=1);

echo "Hello, world\n";""",
            "format": [
                ("扩展名", ".php"),
                ("标签", "<?php … ?>"),
                ("类型", "动态，可选 strict_types"),
                ("执行", "每次请求重新执行"),
            ],
            "note": "PHP 文件可以混合 HTML 与代码；`<?php` 之外的内容会原样输出。现代 PHP 通常只写代码，不写结束标签。",
        },
        {
            "label": "词法记号",
            "file": "tokens",
            "cmd": "$ php -r 'print_r(token_get_all(file_get_contents(\"hello.php\")));'",
            "code": r"""Array
(
    [0] => Array ( [0] => 387  [1] => "<?php\n"  [2] => 1 )
    [1] => Array ( [0] => 391  [1] => "declare"  [2] => 2 )
    ...
    [n] => Array ( [0] => 328  [1] => "echo"     [2] => 4 )
    [n] => Array ( [0] => 262  [1] => " "        [2] => 4 )
    [n] => Array ( [0] => 269  [1] => "\"Hello, world\\n\"" [2] => 4 )
    [n] => ";"
)

; token 编号随 PHP 版本变化，此处为示意""",
            "format": [
                ("接口", "token_get_all()"),
                ("记号", "T_OPEN_TAG / T_ECHO / T_CONSTANT_ENCAPSED_STRING"),
                ("用途", "语法高亮、静态分析、代码转换"),
                ("下一层", "AST（php-parser）→ opcode"),
            ],
            "note": "PHP 的词法层是公开的；AST 层由 nikic/php-parser 等库提供，不是引擎的稳定接口。",
        },
        {
            "label": "opcode",
            "file": "opcache",
            "cmd": "$ php -d opcache.opt_debug_level=0x10000 hello.php",
            "code": r"""$ php -d opcache.opt_debug_level=0x10000 hello.php
$_main:
     ; (lines=3, args=0, vars=0, tmps=0)
     ; (after optimizer)
     ECHO string("Hello, world\n")
     RETURN int(1)

; opcode 数组在内存中
; opcache 把它缓存到共享内存
; 默认不生成可分发文件""",
            "format": [
                ("引擎", "Zend VM"),
                ("opcode", "ECHO / RETURN / INIT_FCALL …"),
                ("缓存", "opcache 共享内存"),
                ("文件", "无标准字节码文件"),
            ],
            "note": "PHP 的「编译」发生在每个请求开始时；opcache 让第二次请求跳过解析与编译，但 opcode 不会被写成 .class 那样的文件。",
        },
        {
            "label": "PHAR",
            "file": "hello.phar",
            "cmd": "$ php -d phar.readonly=0 build.php && php hello.phar",
            "code": r"""$ php -d phar.readonly=0 build.php
$ file hello.phar
hello.phar: PHP Phar archive

$ php hello.phar
Hello, world

; PHAR 结构：
;   stub（PHP 代码，以 __HALT_COMPILER(); 结束）
;   manifest（序列化的文件表、元数据）
;   文件内容（可压缩）
; 需要 phar 扩展；生产环境常禁用 phar.readonly=0""",
            "format": [
                ("容器", "stub + manifest + 文件"),
                ("stub", "以 __HALT_COMPILER(); 结束"),
                ("清单", "序列化的路径、大小、校验和"),
                ("运行", "php hello.phar，需要 phar 扩展"),
            ],
            "note": "PHAR 是 PHP 自己的归档格式：它不是字节码，而是把源码与资源装进一个可执行归档。",
        },
    ],
    "tools": [
        {"era": "1990s", "editor": "文本编辑器", "compiler": "PHP/FI 解释器", "build": "—", "pkg": "—", "debug": "echo / error_log"},
        {"era": "2000s", "editor": "Eclipse PDT / Zend Studio", "compiler": "Zend Engine 2", "build": "Phing", "pkg": "PEAR", "debug": "Xdebug"},
        {"era": "2010s", "editor": "PhpStorm", "compiler": "PHP 7", "build": "Composer scripts", "pkg": "Composer", "debug": "Xdebug"},
        {"era": "2020s", "editor": "VS Code + Intelephense", "compiler": "PHP 8.x", "build": "Composer / Make", "pkg": "Composer", "debug": "Xdebug / phpdbg"},
    ],
    "hello": {
        "file": "hello.php",
        "code": r"""<?php
echo "Hello, world\n";""",
        "footprint": [
            {"stage": "源码", "size": "≈ 34 B", "w": 4},
            {"stage": "tokens", "size": "≈ 300 B", "w": 8},
            {"stage": "opcode", "size": "≈ 200 B", "w": 7},
            {"stage": "PHAR", "size": "≈ 2 KB", "w": 14},
            {"stage": "+ PHP 运行时", "size": "≈ 40 MB", "w": 90},
        ],
        "why": [
            "<strong>请求模型</strong>：每个请求从零开始，状态不跨请求保留。",
            "<strong>opcache</strong>：把 opcode 缓存在共享内存，避免重复编译。",
            "<strong>无字节码文件</strong>：opcode 不是公开的可分发格式。",
            "<strong>PHAR</strong>：用归档封装源码与资源，方便分发。",
        ],
    },
},

# ============================================================
"ruby": {
    "tagline": "为开发者快乐而设计：一切皆对象，语法尽量像自然语言。",
    "intro": [
        "Ruby 由松本行弘（Matz）在 1993 年开始设计，1995 年发布。他把 Smalltalk 的对象模型、Perl 的实用主义与 Lisp 的元编程揉在一起，目标很明确：让写程序的人高兴。",
        "Ruby 1.9 之后使用 YARV 虚拟机，源码先编译成字节码再执行；`RubyVM::InstructionSequence` 可以查看反汇编，也可以把字节码序列化成二进制。但 Ruby 官方不保证字节码跨版本兼容，因此它很少作为分发格式。",
        "Rails 在 2004 年之后把 Ruby 推向 Web 开发主流。Ruby 的产物链也体现了它的哲学：开发者体验优先，底层格式可以变。",
    ],
    "lineage": {
        "from": ["Smalltalk", "Perl", "Lisp", "Python（部分）"],
        "to": ["Elixir（语法）", "Crystal（语法）", "Rails 生态"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.rb",
            "cmd": "$ cat hello.rb",
            "code": r"""def hello
  puts "Hello, world"
end

hello""",
            "format": [
                ("扩展名", ".rb / .rake / Gemfile"),
                ("对象", "一切皆对象，包括数字与 nil"),
                ("块", "do…end 或 {…}"),
                ("元编程", "方法可动态定义、可打开类"),
            ],
            "note": "Ruby 的 `puts` 不是关键字，而是 Kernel 模块的私有方法；`hello` 调用时连括号都可以省略。",
        },
        {
            "label": "AST",
            "file": "Ripper sexp",
            "cmd": "$ ruby -rripper -e 'pp Ripper.sexp(File.read(\"hello.rb\"))'",
            "code": r"""[:program,
 [[:def,
   [:@ident, "hello", [1, 4]],
   [:params, nil, nil, nil, nil, nil, nil, nil],
   [:bodystmt,
    [[:command,
      [:@ident, "puts", [2, 2]],
      [:args_add_block,
       [[:string_literal,
         [:string_content,
          [:@tstring_content, "Hello, world", [2, 8]]]]],
       false]]],
    nil, nil, nil]],
  [:command,
   [:@ident, "hello", [5, 0]],
   [:args_add_block, [], false]]]]""",
            "format": [
                ("工具", "Ripper（标准库）"),
                ("形式", "S 表达式数组"),
                ("用途", "语法分析、代码转换、工具链"),
                ("下一层", "YARV 字节码"),
            ],
            "note": "Ripper 把源码解析成嵌套数组，每个节点带类型与源码位置。RuboCop 等工具就工作在这一层。",
        },
        {
            "label": "YARV 字节码",
            "file": "iseq",
            "cmd": "$ ruby --dump=insns hello.rb",
            "code": r"""== disasm: #<ISeq:<main>@hello.rb:1 (1,0)-(5,5)>
0000 definemethod                       :hello, hello
0003 putself
0004 opt_send_without_block           <calldata!mid:hello, argc:0>
0006 leave

== disasm: #<ISeq:hello@hello.rb:1 (1,0)-(3,3)>
0000 putself
0001 putstring                        "Hello, world"
0003 send                             <calldata!mid:puts, argc:1>, nil
0007 leave""",
            "format": [
                ("虚拟机", "YARV（Ruby 1.9+）"),
                ("指令", "putself / putstring / send / leave"),
                ("存储", "内存中的 ISeq 对象"),
                ("查看", "RubyVM::InstructionSequence.disasm"),
            ],
            "note": "YARV 是栈式虚拟机。`send` 在运行时查找方法，这保留了 Ruby 的动态派发能力。",
        },
        {
            "label": "二进制 ISeq",
            "file": "hello.rbc",
            "cmd": "$ ruby -e 'File.binwrite(\"hello.rbc\", RubyVM::InstructionSequence.compile_file(\"hello.rb\").to_binary)'",
            "code": r"""$ xxd -l 16 hello.rbc
00000000: 5941 5242 3033 3000 ...              YARB030.

; YARB + 版本号 + 序列化的 ISeq
; 官方不保证跨 Ruby 版本兼容
; 可用 ruby-packer / rubyc 打包成独立程序
$ rubyc hello.rb -o hello
$ ./hello
Hello, world""",
            "format": [
                ("魔数", "YARB + 版本"),
                ("内容", "序列化的指令序列"),
                ("兼容", "不保证跨版本"),
                ("打包", "ruby-packer / rubyc 内嵌解释器"),
            ],
            "note": "Ruby 可以把字节码写入文件，但这不是官方分发格式；升级 Ruby 后通常要重新编译。",
        },
    ],
    "tools": [
        {"era": "1990s", "editor": "vi / Emacs", "compiler": "ruby 解释器", "build": "Rake", "pkg": "RubyGems（后）", "debug": "ruby -d"},
        {"era": "2000s", "editor": "TextMate / RadRails", "compiler": "MRI 1.8", "build": "Rake", "pkg": "RubyGems", "debug": "ruby-debug"},
        {"era": "2010s", "editor": "RubyMine / VS Code", "compiler": "MRI 2.x / YARV", "build": "Rake / Bundler", "pkg": "RubyGems / Bundler", "debug": "byebug / pry"},
        {"era": "2020s", "editor": "VS Code + Ruby LSP", "compiler": "MRI 3.x / YJIT", "build": "Rake / Bundler", "pkg": "RubyGems", "debug": "debug.gem"},
    ],
    "hello": {
        "file": "hello.rb",
        "code": r"""puts "Hello, world"
# 输出：Hello, world""",
        "footprint": [
            {"stage": "源码", "size": "≈ 24 B", "w": 4},
            {"stage": "Ripper AST", "size": "≈ 600 B", "w": 12},
            {"stage": "YARV ISeq", "size": "≈ 250 B", "w": 8},
            {"stage": ".rbc", "size": "≈ 1 KB", "w": 14},
            {"stage": "打包 exe", "size": "≈ 8 MB", "w": 80},
        ],
        "why": [
            "<strong>YARV</strong>：源码编译成栈式字节码，保留动态派发。",
            "<strong>ISeq</strong>：字节码、常量、行号、异常表一起构成可执行单元。",
            "<strong>不落盘</strong>：默认只在内存中，二进制格式不保证跨版本。",
            "<strong>打包</strong>：ruby-packer 把解释器与代码一起带上。",
        ],
    },
},

# ============================================================
"haskell": {
    "tagline": "纯函数式、惰性求值、类型系统，把「副作用」关进 IO。",
    "intro": [
        "Haskell 在 1987 年的 FPCA 会议上被提出，1990 年发布 Haskell 1.0 报告，目标是统一当时各自为政的惰性函数式语言。它的两个标志是纯函数与惰性求值：默认没有副作用，表达式按需计算。",
        "GHC 的产物链很长：源码先被去糖成 Core，再做严格性分析、优化、转换成 STG，最后生成 Cmm 与机器码。Core 与 STG 是学习「函数式程序如何变成机器码」的最好样本。",
        "Haskell 程序通常静态链接 GHC 运行时，体积以 MB 计。运行时负责 thunk、垃圾回收、异常与绿色线程（green threads）。",
    ],
    "lineage": {
        "from": ["Miranda", "ML", "λ 演算"],
        "to": ["GHC 生态", "Elm（部分）", "Rust（trait 思想）"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.hs",
            "cmd": "$ cat hello.hs",
            "code": r"""main :: IO ()
main = putStrLn "Hello, world"

-- 纯函数与 IO 分开
-- putStrLn :: String -> IO ()""",
            "format": [
                ("扩展名", ".hs / .lhs"),
                ("类型", "静态、推断、多态"),
                ("求值", "默认惰性"),
                ("入口", "main :: IO ()"),
            ],
            "note": "Haskell 的 `main` 是一个 IO 动作，不是一组语句。程序的执行顺序由 IO 的绑定关系决定，而不是书写顺序。",
        },
        {
            "label": "Core",
            "file": "hello.core",
            "cmd": "$ ghc -ddump-simpl hello.hs",
            "code": r"""; GHC Core（示意）
Main.main1 :: State# RealWorld -> (# State# RealWorld, () #)
Main.main1 =
  \s -> case putStrLn "Hello, world" s of
          (# s', _ #) -> (# s', () #)

; Core 是 GHC 的核心中间语言
; 类型、模式匹配、let、case 都显式化
; 之后做严格性分析与内联""",
            "format": [
                ("中间语言", "Core"),
                ("特征", "显式类型、显式 case、无语法糖"),
                ("状态", "State# 把世界状态串起来"),
                ("优化", "内联、严格性、融合"),
            ],
            "note": "惰性 language 的 Core 里，函数调用默认是 thunk；严格性分析会决定哪些参数可以立即求值。",
        },
        {
            "label": "STG",
            "file": "hello.stg",
            "cmd": "$ ghc -ddump-stg-final hello.hs",
            "code": r"""; STG（示意）
main = \u ->
  let { sat = putStrLn "Hello, world" }
  in case sat of { _ -> () }

; STG = Spineless Tagless G-machine
; 函数、thunk、更新、进入（enter）都显式
; 惰性求值的执行模型在这里定型""",
            "format": [
                ("中间语言", "STG"),
                ("模型", "thunk + 进入 + 更新"),
                ("惰性", "参数是闭包，需要时才求值"),
                ("后续", "Cmm → 汇编 → 目标"),
            ],
            "note": "STG 是 Haskell 惰性求值的核心：变量不是值，而是待进入的闭包；求值后会回写（update）以免重复计算。",
        },
        {
            "label": "Cmm 与可执行",
            "file": "hello",
            "cmd": "$ ghc -O2 hello.hs -o hello",
            "code": r"""; Cmm（示意）
Main_main1()
    ...
    call base_GHCziIOziHandleziText_putStrLn_info
    ...

$ ghc -O2 hello.hs -o hello
$ ./hello
Hello, world

$ file hello
hello: ELF 64-bit LSB executable, x86-64 ...

; 静态链接 GHC RTS：
;   GC、thunk、异常、调度、时钟""",
            "format": [
                ("Cmm", "GHC 的低级中间语言"),
                ("后端", "汇编 / 目标文件"),
                ("运行时", "GHC RTS，静态链接"),
                ("体积", "hello 通常 1–2 MB"),
            ],
            "note": "GHC 默认静态链接运行时，所以一个 hello 也有 MB 级体积。运行时负责 GC、线程调度与 thunk 管理。",
        },
    ],
    "tools": [
        {"era": "1990s", "editor": "Emacs", "compiler": "GHC / Hugs", "build": "make", "pkg": "—", "debug": "Hugs 调试"},
        {"era": "2000s", "editor": "Emacs / Leksah", "compiler": "GHC", "build": "Cabal", "pkg": "Cabal", "debug": "ghci"},
        {"era": "2010s", "editor": "Emacs / VS Code", "compiler": "GHC", "build": "Cabal / Stack", "pkg": "Hackage / Stackage", "debug": "ghci / GHCi debugger"},
        {"era": "2020s", "editor": "VS Code + HLS", "compiler": "GHC 9.x", "build": "Cabal / Stack", "pkg": "Hackage", "debug": "ghci / HLS"},
    ],
    "hello": {
        "file": "hello.hs",
        "code": r"""main :: IO ()
main = putStrLn "Hello, world"
-- 输出：Hello, world""",
        "footprint": [
            {"stage": "源码", "size": "≈ 48 B", "w": 4},
            {"stage": "Core", "size": "≈ 1 KB", "w": 14},
            {"stage": "STG", "size": "≈ 800 B", "w": 12},
            {"stage": "Cmm", "size": "≈ 1.2 KB", "w": 15},
            {"stage": "可执行", "size": "≈ 1.4 MB", "w": 80},
            {"stage": "+ RTS", "size": "≈ 2 MB", "w": 90},
        ],
        "why": [
            "<strong>Core</strong>：去糖后的函数式核心，类型与 case 显式。",
            "<strong>STG</strong>：把惰性求值变成可执行的 thunk/enter/update 模型。",
            "<strong>Cmm</strong>：接近机器的低级 IR，负责调用约定与栈。",
            "<strong>RTS</strong>：GC、绿色线程、异常、时钟都在运行时里。",
        ],
    },
},

# ============================================================
"lua": {
    "tagline": "为嵌入而生的轻量脚本：一个栈、一张表、一个虚拟机。",
    "intro": [
        "Lua 由 Roberto Ierusalimschy、Luiz Henrique de Figueiredo 与 Waldemar Celes 在巴西 PUC-Rio 开发，1993 年发布。它从诞生起就有一个明确约束：要能嵌进 C 程序，体积小、依赖少、可移植。",
        "Lua 的核心抽象只有表（table）与函数；对象、模块、命名空间都用表模拟。它的编译器一次扫描就生成字节码，`luac` 可以把字节码写成 `.luac` 文件，但官方不保证跨版本兼容。",
        "游戏行业是它最大的用户：魔兽世界、Roblox、Redis、Nginx（OpenResty）都把 Lua 当作嵌入脚本层。产物链因此常常是「`.luac` + C 宿主程序」。",
    ],
    "lineage": {
        "from": ["C", "Scheme（部分）", "自身体积约束"],
        "to": ["Roblox Luau", "OpenResty", "游戏脚本生态"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.lua",
            "cmd": "$ cat hello.lua",
            "code": r"""print("Hello, world")""",
            "format": [
                ("扩展名", ".lua"),
                ("类型", "动态，唯一容器是 table"),
                ("索引", "从 1 开始"),
                ("执行", "编译成字节码后由 VM 执行"),
            ],
            "note": "`print` 不是关键字，而是全局表 `_ENV` 里的一个函数；Lua 5.2 之后全局变量就是 `_ENV` 的字段。",
        },
        {
            "label": "字节码清单",
            "file": "luac -l -l",
            "cmd": "$ luac -l -l hello.lua",
            "code": r"""$ luac -l -l hello.lua

main <hello.lua:0,0> (4 instructions at 0x...)
0+ params, 2 slots, 1 upvalue, 0 locals, 1 constant, 0 functions
    1   [1] GETTABUP   0 0 0   ; _ENV "print"
    2   [1] LOADK      1 0     ; "Hello, world"
    3   [1] CALL       0 2 1
    4   [1] RETURN     0 1

constants (1) for 0x...:
    0   "Hello, world"
""",
            "format": [
                ("指令", "寄存器式字节码"),
                ("常量表", "字符串、数字、函数原型"),
                ("原型", "每个函数一个 Proto"),
                ("查看", "luac -l -l"),
            ],
            "note": "Lua 的字节码是寄存器式，不是 JVM 的栈式。每条指令带 A/B/C 操作数字段，紧凑且解码快。",
        },
        {
            "label": ".luac 文件",
            "file": "hello.luac",
            "cmd": "$ luac -o hello.luac hello.lua && xxd -l 24 hello.luac",
            "code": r"""$ xxd -l 24 hello.luac
00000000: 1b4c 7561 5400 1993 0d0a 1a0a 0408 0408  .LuaT...........
00000010: 0800 0000 0000 0000 0000 0000 0000 0000  ................

; 1b 4c 75 61  = "\x1bLua"
; 54           = 版本 5.4
; 00           = 格式
; 19 93 0d 0a 1a 0a = LUAC_DATA
; 之后是头部尺寸与函数原型""",
            "format": [
                ("魔数", "\\x1bLua + 版本"),
                ("格式", "头部 + 原型 + 常量 + 调试信息"),
                ("兼容", "跨版本不保证"),
                ("生成", "luac -o"),
            ],
            "note": "`.luac` 不是独立的可执行文件，它需要 Lua 虚拟机加载。游戏与嵌入式通常把字节码直接嵌进宿主程序。",
        },
        {
            "label": "嵌入可执行",
            "file": "hello",
            "cmd": "$ srlua hello.lua hello && ./hello",
            "code": r"""$ srlua hello.lua hello
$ file hello
hello: ELF 64-bit LSB executable, x86-64 ...

$ ./hello
Hello, world

; 结构：Lua 解释器 + 脚本字节码
; 游戏引擎：宿主 C/C++ 程序 dlopen 或静态链接 liblua
; Roblox / OpenResty 都是这种模式""",
            "format": [
                ("打包", "srlua / luastatic"),
                ("内容", "解释器 + 字节码"),
                ("嵌入", "C API：luaL_loadbuffer / lua_pcall"),
                ("体积", "通常 200–400 KB"),
            ],
            "note": "Lua 的典型产物不是独立程序，而是「宿主程序 + liblua + 脚本」的组合。灵活之处在于脚本可以随时替换。",
        },
    ],
    "tools": [
        {"era": "1990s", "editor": "vi", "compiler": "lua 解释器", "build": "make", "pkg": "—", "debug": "print 调试"},
        {"era": "2000s", "editor": "SciTE", "compiler": "lua 5.1", "build": "make", "pkg": "LuaRocks", "debug": "调试库"},
        {"era": "2010s", "editor": "ZeroBrane Studio", "compiler": "LuaJIT / lua 5.3", "build": "make", "pkg": "LuaRocks", "debug": "ZeroBrane 调试器"},
        {"era": "2020s", "editor": "VS Code + Lua", "compiler": "Lua 5.4 / LuaJIT", "build": "make / luarocks", "pkg": "LuaRocks", "debug": "debugger.lua"},
    ],
    "hello": {
        "file": "hello.lua",
        "code": r"""print("Hello, world")""",
        "footprint": [
            {"stage": "源码", "size": "≈ 22 B", "w": 4},
            {"stage": "指令", "size": "≈ 80 B", "w": 6},
            {"stage": ".luac", "size": "≈ 300 B", "w": 9},
            {"stage": "嵌入 exe", "size": "≈ 280 KB", "w": 45},
            {"stage": "+ liblua", "size": "≈ 400 KB", "w": 55},
        ],
        "why": [
            "<strong>寄存器字节码</strong>：指令紧凑，适合嵌入与快速加载。",
            "<strong>Proto</strong>：每个函数一个原型，包含指令、常量、调试信息。",
            "<strong>.luac</strong>：可加载的字节码，不是独立程序。",
            "<strong>嵌入</strong>：宿主程序通过 C API 加载脚本，替换脚本不需重编译宿主。",
        ],
    },
},

# ============================================================
"r": {
    "tagline": "统计学家的工作台：向量、数据框与一张张图。",
    "intro": [
        "R 由 Ross Ihaka 与 Robert Gentleman 在奥克兰大学开发，1993 年发布，后来由 R Core Team 维护。它是 S 语言的开源实现，目标是把统计计算、数据整理与绘图放在同一个交互环境里。",
        "R 的核心是向量化：`x + 1` 对整个向量生效，循环通常交给底层 C/Fortran。函数是一等对象，环境（environment）构成词法作用域；`data.frame` 是表格数据的基本结构。",
        "R 的产物链偏交互：源码被解析成表达式树，解释执行；3.4 之后有 JIT，3.5 之后有字节码编译器。分发时通常打包成 `.tar.gz` 源码包或 `.rds` 序列化对象。",
    ],
    "lineage": {
        "from": ["S", "Scheme（作用域）", "Fortran（数值库）"],
        "to": ["tidyverse 生态", "Julia（部分）", "Python（statsmodels）"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.R",
            "cmd": "$ cat hello.R",
            "code": r"""hello <- function() {
  cat("Hello, world\n")
}

hello()""",
            "format": [
                ("扩展名", ".R / .r"),
                ("赋值", "<- 或 ="),
                ("向量", "默认向量化"),
                ("函数", "一等对象，闭包捕获环境"),
            ],
            "note": "R 的 `<-` 是赋值，`=` 也能赋值但优先级不同。函数调用 `hello()` 会创建一个新环境，而不是新栈帧。",
        },
        {
            "label": "表达式树",
            "file": "parse tree",
            "cmd": "> parse(text = 'cat(\"Hello, world\\\\n\")')",
            "code": r"""> parse(text = 'cat("Hello, world\n")')
expression(cat("Hello, world\n"))

> as.list(parse(text = 'cat("Hello, world\n")')[[1]])
[[1]]
cat

[[2]]
Hello, world

; 代码在 R 里也是对象
; 可以打印、修改、求值（eval）""",
            "format": [
                ("解析", "parse() 返回 expression"),
                ("节点", "call / symbol / constant"),
                ("元编程", "代码即数据，可 eval"),
                ("环境", "词法作用域，函数携带环境"),
            ],
            "note": "R 的表达式树是公开的：`substitute`、`quote`、`eval` 都在这一层工作。这既是元编程能力，也是调试复杂性的来源。",
        },
        {
            "label": "字节码",
            "file": "bc",
            "cmd": "> compiler::disassemble(function() cat(\"Hello, world\\n\"))",
            "code": r"""> library(compiler)
> f <- function() cat("Hello, world\n")
> disassemble(f)
list(cat("Hello, world\n"))

; 3.5+ 默认对包函数做字节码编译
; 字节码是 R 对象，不落盘
; JIT 在 3.4+ 对热点循环生效""",
            "format": [
                ("编译器", "compiler 包（3.5+ 默认）"),
                ("字节码", "bc 对象，内存中"),
                ("JIT", "3.4+，热点循环"),
                ("查看", "disassemble / cmpfun"),
            ],
            "note": "R 的字节码不是可分发文件：它是运行时的对象。包安装时可能缓存字节码，但跨版本不保证。",
        },
        {
            "label": "序列化与包",
            "file": "hello.rds / hello.tar.gz",
            "cmd": "$ Rscript -e 'saveRDS(hello, \"hello.rds\")'",
            "code": r"""$ xxd -l 8 hello.rds
00000000: 5244 5833 0a00 0000 ...              RDX3....

; RDX3 = RDS 版本 3
; 内容：序列化的 R 对象（函数、数据框、环境）
; 跨 R 版本通常可读，但新特性可能不兼容

$ R CMD build hellopkg
$ ls hellopkg_0.1.0.tar.gz
; 包结构：DESCRIPTION / NAMESPACE / R/ / src/ / man/""",
            "format": [
                ("RDS", "单对象序列化，RDX3 头"),
                ("RData", "工作区多对象"),
                ("包", ".tar.gz + DESCRIPTION/NAMESPACE"),
                ("分发", "CRAN / Bioconductor"),
            ],
            "note": "R 的分发单位是包（源码 tar.gz 或二进制），而不是可执行文件。`.rds` 用于数据与模型对象。",
        },
    ],
    "tools": [
        {"era": "1990s", "editor": "R 控制台", "compiler": "R 解释器", "build": "R CMD build", "pkg": "CRAN", "debug": "browser()"},
        {"era": "2000s", "editor": "Emacs + ESS", "compiler": "R 2.x", "build": "R CMD build", "pkg": "CRAN", "debug": "debug()"},
        {"era": "2010s", "editor": "RStudio", "compiler": "R 3.x + JIT", "build": "devtools", "pkg": "CRAN / Bioconductor", "debug": "RStudio 调试器"},
        {"era": "2020s", "editor": "RStudio / VS Code", "compiler": "R 4.x", "build": "pak / devtools", "pkg": "CRAN / Bioconductor", "debug": "debugger"},
    ],
    "hello": {
        "file": "hello.R",
        "code": r"""cat("Hello, world\n")""",
        "footprint": [
            {"stage": "源码", "size": "≈ 26 B", "w": 4},
            {"stage": "表达式树", "size": "≈ 150 B", "w": 7},
            {"stage": "字节码", "size": "≈ 200 B", "w": 8},
            {"stage": "RDS", "size": "≈ 180 B", "w": 8},
            {"stage": "+ R 运行时", "size": "≈ 80 MB", "w": 90},
        ],
        "why": [
            "<strong>表达式树</strong>：代码是对象，支持 quote/eval 与统计建模 DSL。",
            "<strong>环境</strong>：词法作用域与闭包，函数携带定义环境。",
            "<strong>字节码</strong>：3.5+ 默认编译包函数，减少解释开销。",
            "<strong>RDS/包</strong>：分发的是数据对象与源码包，不是可执行文件。",
        ],
    },
},

# ============================================================
"delphi": {
    "tagline": "Object Pascal 的快速应用开发：拖控件、按 F9、生成原生 Windows 程序。",
    "intro": [
        "Delphi 由 Borland 在 1995 年发布，核心是 Object Pascal 编译器与 VCL 组件库。它把可视化设计器、编译器、调试器塞进一个 IDE，用「拖控件 + 写事件」的方式快速构建 Windows 应用。",
        "Delphi 的编译器极快：一次扫描生成原生代码，单元编译成 `.dcu`（Delphi Compiled Unit），其中包含符号表、类型信息与目标代码；最终链接成 PE 可执行文件。",
        "它长期是 Windows 桌面与企业内部系统的主力之一。2000 年代后，Delphi 也支持跨平台（FireMonkey），但经典产物链仍是 `.dpr → .dcu → .exe`。",
    ],
    "lineage": {
        "from": ["Pascal", "Turbo Pascal", "Object Pascal"],
        "to": ["C# / .NET（Anders Hejlsberg）", "Free Pascal / Lazarus"],
    },
    "chain": [
        {
            "label": "项目源码",
            "file": "Hello.dpr",
            "cmd": "$ cat Hello.dpr",
            "code": r"""program Hello;

{$APPTYPE CONSOLE}

uses
  System.SysUtils;

begin
  Writeln('Hello, world');
end.""",
            "format": [
                ("扩展名", ".dpr（项目）/ .pas（单元）"),
                ("指令", "{$APPTYPE CONSOLE} 指定子系统"),
                ("uses", "显式依赖单元"),
                ("编译", "dcc32 / dcc64"),
            ],
            "note": "`.dpr` 是项目入口；真正的代码通常在 `.pas` 单元里。`uses` 决定编译顺序与符号可见性。",
        },
        {
            "label": "单元与窗体",
            "file": "HelloUnit.pas / HelloForm.dfm",
            "cmd": "$ cat HelloUnit.pas",
            "code": r"""unit HelloUnit;

interface

procedure SayHello;

implementation

uses
  System.SysUtils;

procedure SayHello;
begin
  Writeln('Hello, world');
end;

end.

// HelloForm.dfm（窗体资源，文本形式）
object Form1: TForm1
  Caption = 'Hello'
end""",
            "format": [
                ("单元", ".pas，interface + implementation"),
                ("窗体", ".dfm 文本资源 / .res 二进制"),
                ("单元", ".dcu 编译产物"),
                ("链接", "项目把单元与资源合成 .exe"),
            ],
            "note": "VCL 窗体在设计器里是对象树，保存为 `.dfm`；编译时被转换成资源，链接进 PE。",
        },
        {
            "label": "DCU",
            "file": "HelloUnit.dcu",
            "cmd": "$ dcc32 Hello.dpr && ls -l *.dcu",
            "code": r"""$ dcc32 Hello.dpr
$ ls -l HelloUnit.dcu
-rw-r--r-- 1 user user 4.2K ... HelloUnit.dcu

$ file HelloUnit.dcu
HelloUnit.dcu: data

; DCU = Delphi Compiled Unit
; 包含：目标代码、符号表、类型信息、内联信息
; 格式私有，随 Delphi 版本变化
; 分发 .dcu 等于分发编译后的单元""",
            "format": [
                ("格式", "私有二进制"),
                ("内容", "代码 + 符号 + 类型 + 内联"),
                ("兼容", "与编译器版本绑定"),
                ("用途", "增量编译 / 闭源单元分发"),
            ],
            "note": "Delphi 的 `.dcu` 类似 Java 的 `.class` + 符号表：客户可以编译依赖它的单元，但看不到源码。",
        },
        {
            "label": "可执行",
            "file": "Hello.exe",
            "cmd": "$ file Hello.exe && objdump -p Hello.exe | grep 'DLL Name'",
            "code": r"""$ file Hello.exe
Hello.exe: PE32+ executable (console) x86-64

$ objdump -p Hello.exe | grep 'DLL Name'
  DLL Name: KERNEL32.dll
  DLL Name: USER32.dll
  DLL Name: ADVAPI32.dll

; 可选运行时包（.bpl）
; VCL 可静态链接或动态加载
; 资源段包含图标、版本信息、窗体""",
            "format": [
                ("格式", "PE32 / PE32+"),
                ("依赖", "Win32 API + 可选 BPL"),
                ("资源", "图标、版本、窗体"),
                ("部署", "拷贝 exe（+ bpl/dll）即可"),
            ],
            "note": "经典 Delphi 程序的部署非常简单：一个 exe 加必要的 DLL/BPL。没有虚拟机，也没有外部运行时。",
        },
    ],
    "tools": [
        {"era": "1990s", "editor": "Delphi IDE", "compiler": "dcc32", "build": "IDE / make", "pkg": "VCL / 组件", "debug": "IDE 调试器"},
        {"era": "2000s", "editor": "Delphi IDE", "compiler": "dcc32", "build": "IDE / MSBuild", "pkg": "GetIt", "debug": "IDE 调试器"},
        {"era": "2010s", "editor": "Delphi XE IDE", "compiler": "dcc32/dcc64", "build": "MSBuild", "pkg": "GetIt", "debug": "IDE 调试器"},
        {"era": "2020s", "editor": "Delphi / VS Code + Lazarus", "compiler": "dcc / fpc", "build": "MSBuild / lazbuild", "pkg": "GetIt / OPM", "debug": "IDE / gdb"},
    ],
    "hello": {
        "file": "Hello.dpr",
        "code": r"""program Hello;
{$APPTYPE CONSOLE}
begin
  Writeln('Hello, world');
end.""",
        "footprint": [
            {"stage": ".dpr", "size": "≈ 100 B", "w": 4},
            {"stage": ".pas/.dfm", "size": "≈ 300 B", "w": 8},
            {"stage": ".dcu", "size": "≈ 4 KB", "w": 16},
            {"stage": ".exe", "size": "≈ 400 KB", "w": 50},
            {"stage": "+ VCL", "size": "≈ 1.5 MB", "w": 75},
        ],
        "why": [
            "<strong>单遍编译</strong>：Object Pascal 设计上就能快速编译，IDE 体验是核心卖点。",
            "<strong>DCU</strong>：编译单元 + 符号表，支持增量编译与闭源分发。",
            "<strong>DFM</strong>：窗体是对象树，保存为资源，链接进 exe。",
            "<strong>原生 PE</strong>：没有虚拟机，部署就是拷贝文件。",
        ],
    },
},

# ============================================================
"vb": {
    "tagline": "让业务人员也能拖控件写程序：事件驱动与 COM 的普及者。",
    "intro": [
        "Visual Basic 1.0 于 1991 年发布，Alan Cooper 的界面设计工具与 Microsoft 的 Basic 编译器结合，形成了「拖控件 + 写事件」的开发方式。它让大量非专业程序员第一次能做出 Windows 应用。",
        "VB 3/4/5/6 是经典版本：项目是 `.vbp`，窗体是 `.frm` + `.frx`（二进制资源），编译产物是 `.exe` 或 `.dll`。默认编译成 p-code，由 `MSVBVM60.DLL` 解释；也可以选择原生代码。",
        "VB 6 的组件生态（OCX、ActiveX、COM）在 1990 年代末统治了企业内网。2002 年的 VB.NET 是另一门语言，产物链转向 .NET IL。",
    ],
    "lineage": {
        "from": ["BASIC", "QuickBASIC", "COM / ActiveX"],
        "to": ["VB.NET", "VBA", "低代码平台"],
    },
    "chain": [
        {
            "label": "项目文件",
            "file": "Hello.vbp",
            "cmd": "$ cat Hello.vbp",
            "code": r"""Type=Exe
Form=Form1.frm
Reference=*\G{00020430-0000-0000-C000-000000000046}#2.0#0#C:\Windows\System32\stdole2.tlb#OLE Automation
Object={831FDD16-0C5C-11D2-A9FC-0000F8754DA1}#2.0#0; MSCOMCTL.OCX
Startup="Form1"
Command32=""
Name="Hello"
HelpContextID="0""",
            "format": [
                ("扩展名", ".vbp"),
                ("内容", "窗体、引用、组件、启动对象"),
                ("控件", "OCX 以 GUID 引用"),
                ("入口", "Startup 指定启动窗体"),
            ],
            "note": "VB 项目文件是纯文本清单：引用了哪些 COM 组件、哪个窗体先启动、编译成 exe 还是 dll。",
        },
        {
            "label": "窗体与资源",
            "file": "Form1.frm / Form1.frx",
            "cmd": "$ cat Form1.frm",
            "code": r"""VERSION 5.00
Begin VB.Form Form1
   Caption         =   "Hello"
   ClientHeight    =   3090
   ClientWidth     =   4680
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False

Private Sub Form_Load()
    MsgBox "Hello, world"
End Sub""",
            "format": [
                ("窗体", ".frm，文本 + 控件属性"),
                ("资源", ".frx，二进制（图片、图标）"),
                ("事件", "Form_Load 等由运行时回调"),
                ("设计器", "属性窗口直接改 .frm"),
            ],
            "note": "`.frm` 上半部分是设计器生成的控件树，下半部分是你写的事件过程。`.frx` 保存二进制资源。",
        },
        {
            "label": "编译产物",
            "file": "Hello.exe",
            "cmd": "$ dumpbin /imports Hello.exe | findstr /i msvbvm",
            "code": r"""$ dumpbin /imports Hello.exe | findstr /i msvbvm
    MSVBVM60.DLL
    ...

$ file Hello.exe
Hello.exe: PE32 executable (GUI) Intel 80386, for MS Windows

; 默认：p-code（由 MSVBVM60 解释）
; 可选：原生代码（Project Properties → Compile）
; p-code 更小，原生代码更快""",
            "format": [
                ("格式", "PE32"),
                ("p-code", "默认，解释执行"),
                ("原生", "可切换到本机代码"),
                ("依赖", "MSVBVM60.DLL（VB6 运行时）"),
            ],
            "note": "VB6 的 p-code 存在 exe 里，由 `MSVBVM60.DLL` 解释。选择「Compile to Native Code」才会生成 x86 机器码。",
        },
        {
            "label": "运行时",
            "file": "MSVBVM60.DLL",
            "cmd": "C:\\Windows\\System32\\MSVBVM60.DLL",
            "code": r"""C:\Windows\System32\MSVBVM60.DLL

; VB6 运行时提供：
;   - p-code 解释器
;   - 窗体与控件实现
;   - 字符串/变体/错误处理
;   - COM 绑定
; 安装程序通常需要附带并注册该 DLL
; 现代 Windows 仍保留兼容""",
            "format": [
                ("运行时", "MSVBVM60.DLL"),
                ("作用", "解释 p-code、窗体、COM"),
                ("部署", "安装程序附带并注册"),
                ("兼容", "Windows 保留兼容层"),
            ],
            "note": "VB6 程序不是自包含的：没有 `MSVBVM60.DLL` 就起不来。这也是「拷贝 exe 就能跑」并不总成立的原因。",
        },
    ],
    "tools": [
        {"era": "1990s", "editor": "Visual Basic IDE", "compiler": "VB 3–6 编译器", "build": "IDE 编译", "pkg": "OCX / COM", "debug": "IDE 调试器"},
        {"era": "2000s", "editor": "VB6 IDE", "compiler": "VB6", "build": "Package & Deployment", "pkg": "COM / OCX", "debug": "IDE 调试器"},
        {"era": "2010s", "editor": "VB6（遗留）/ VB.NET", "compiler": "VB6 / Roslyn", "build": "MSBuild", "pkg": "NuGet", "debug": "VS 调试器"},
        {"era": "2020s", "editor": "VS 2022（VB.NET）", "compiler": "Roslyn", "build": "MSBuild", "pkg": "NuGet", "debug": "VS 调试器"},
    ],
    "hello": {
        "file": "Form1.frm",
        "code": r"""VERSION 5.00
Begin VB.Form Form1
   Caption = "Hello"
End
Private Sub Form_Load()
    MsgBox "Hello, world"
End Sub""",
        "footprint": [
            {"stage": ".vbp", "size": "≈ 400 B", "w": 5},
            {"stage": ".frm/.frx", "size": "≈ 2 KB", "w": 10},
            {"stage": ".exe", "size": "≈ 30 KB", "w": 22},
            {"stage": "p-code", "size": "≈ 8 KB", "w": 14},
            {"stage": "+ MSVBVM60", "size": "≈ 1.4 MB", "w": 80},
        ],
        "why": [
            "<strong>事件驱动</strong>：代码由用户操作触发，而不是从 main 顺序执行。",
            "<strong>.frm/.frx</strong>：界面是资源，设计器与代码分离。",
            "<strong>p-code</strong>：默认编译为紧凑字节码，由运行时解释。",
            "<strong>COM</strong>：控件与组件通过 COM 接口组合，部署需要注册 DLL/OCX。",
        ],
    },
},

# ============================================================
"ocaml": {
    "tagline": "ML 的工业实现：类型推断、模块系统、两个后端（字节码与原生）。",
    "intro": [
        "OCaml 由 Xavier Leroy 等人在 INRIA 于 1996 年发布，继承 Caml Light 与 Standard ML 的传统。它保留了 ML 的类型推断与模式匹配，加入模块系统与对象层，并提供字节码与原生两条编译路径。",
        "OCaml 的产物链很适合对照：`ocamlc` 生成 `.cmo`（字节码目标）与 `.cma`（库），由 `ocamlrun` 执行；`ocamlopt` 生成 `.cmx` 与原生 `.o`，链接成普通 ELF。同一份源码，两种完全不同的产物。",
        "它的类型系统在编译期完成，运行时不需要类型检查；垃圾回收、异常、闭包都由运行时处理。OCaml 在编译器、金融、自动化证明与 Jane Street 的交易系统里长期使用。",
    ],
    "lineage": {
        "from": ["Caml Light", "Standard ML", "λ 演算"],
        "to": ["ReasonML / ReScript", "F#（部分）", "Rust（部分）"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.ml",
            "cmd": "$ cat hello.ml",
            "code": r"""let () = print_endline "Hello, world"
(* 输出：Hello, world *)""",
            "format": [
                ("扩展名", ".ml / .mli"),
                ("类型", "静态、推断、参数多态"),
                ("模块", "module / functor"),
                ("入口", "顶层 let () 在启动时执行"),
            ],
            "note": "OCaml 没有特殊的 main 函数：模块顶层的 `let () = ...` 在程序启动时按顺序执行。",
        },
        {
            "label": "Lambda",
            "file": "lambda",
            "cmd": "$ ocamlc -dlambda -c hello.ml",
            "code": r"""(let
  (() = (apply (field 21 (global Stdlib!))
               "Hello, world"))
  0)

; 类型已擦除，模式匹配已展开
; Lambda 是 OCaml 的核心中间语言
; 之后做闭包转换 / 寄存器分配""",
            "format": [
                ("中间语言", "Lambda"),
                ("类型", "已擦除，运行时无类型标记"),
                ("模式", "已编译为分支与投影"),
                ("后续", "字节码或原生代码"),
            ],
            "note": "OCaml 的类型在编译后完全消失：运行时没有类型信息，也没有泛型实例化。这是它与 Java/C# 的重要区别。",
        },
        {
            "label": "字节码",
            "file": "hello.cmo",
            "cmd": "$ ocamlc -c hello.ml && head -c 12 hello.cmo",
            "code": r"""$ head -c 12 hello.cmo
Caml1999X030

$ ocamlc -o hello.byte hello.cmo
$ ./hello.byte
Hello, world

; .cmo = 编译单元（字节码 + 元数据）
; .cma = 库（多个 .cmo）
; ocamlrun 执行字节码""",
            "format": [
                ("魔数", "Caml1999X0xx（版本相关）"),
                ("单元", ".cmo / .cma"),
                ("执行", "ocamlrun 字节码虚拟机"),
                ("优点", "编译快、可移植"),
            ],
            "note": "OCaml 字节码是官方支持的产物，不是内部缓存。它可以在不同架构上由 `ocamlrun` 执行，前提是版本匹配。",
        },
        {
            "label": "原生可执行",
            "file": "hello",
            "cmd": "$ ocamlopt -o hello hello.ml && file hello",
            "code": r"""$ ocamlopt -c hello.ml
$ ls hello.cmx hello.o
hello.cmx  hello.o

$ ocamlopt -o hello hello.cmx
$ file hello
hello: ELF 64-bit LSB pie executable, x86-64 ...

$ ./hello
Hello, world

; .cmx = 跨模块优化信息
; .o   = 原生目标文件
; 运行时：GC、异常、闭包""",
            "format": [
                ("原生单元", ".cmx + .o"),
                ("优化", "跨模块内联（.cmx 提供信息）"),
                ("运行时", "GC、异常、闭包"),
                ("产物", "普通 ELF / Mach-O / PE"),
            ],
            "note": "`.cmx` 不只是目标文件：它保存了跨模块优化所需的类型与近似代码信息，让 `ocamlopt` 能跨单元内联。",
        },
    ],
    "tools": [
        {"era": "1990s", "editor": "Emacs", "compiler": "ocamlc / ocamlopt", "build": "make", "pkg": "—", "debug": "ocamldebug"},
        {"era": "2000s", "editor": "Emacs + Tuareg", "compiler": "ocamlc / ocamlopt", "build": "ocamlbuild", "pkg": "Findlib", "debug": "ocamldebug"},
        {"era": "2010s", "editor": "VS Code + Merlin", "compiler": "ocamlopt", "build": "dune", "pkg": "opam", "debug": "ocamldebug / gdb"},
        {"era": "2020s", "editor": "VS Code + OCaml Platform", "compiler": "ocamlopt 5.x", "build": "dune", "pkg": "opam", "debug": "ocamldebug / gdb"},
    ],
    "hello": {
        "file": "hello.ml",
        "code": r"""let () = print_endline "Hello, world"
(* 输出：Hello, world *)""",
        "footprint": [
            {"stage": "源码", "size": "≈ 38 B", "w": 4},
            {"stage": "Lambda", "size": "≈ 90 B", "w": 6},
            {"stage": ".cmo", "size": "≈ 600 B", "w": 12},
            {"stage": ".cmx/.o", "size": "≈ 4 KB", "w": 18},
            {"stage": "原生 ELF", "size": "≈ 350 KB", "w": 55},
        ],
        "why": [
            "<strong>类型擦除</strong>：编译后没有类型信息，运行时零开销。",
            "<strong>Lambda</strong>：去糖后的核心语言，闭包与模式匹配已显式。",
            "<strong>双后端</strong>：字节码可移植，原生代码追求性能。",
            "<strong>.cmx</strong>：跨模块优化信息，让内联跨越编译单元。",
        ],
    },
},

}

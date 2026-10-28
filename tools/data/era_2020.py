# -*- coding: utf-8 -*-
"""第四批 · 2020s + 领域专用：12 门语言的档案与产物链数据。"""

LANGS = {

# ============================================================
"mojo": {
    "tagline": "Python 的语法，系统级的性能：用 MLIR 把 AI 基础设施重新编译一遍。",
    "intro": [
        "Mojo 由 Chris Lattner 在 Modular 主导，2023 年公开。它想解决 AI 基础设施里的一个矛盾：Python 生态好用，但性能与部署依赖大量 C/C++/CUDA 扩展。Mojo 选择兼容 Python 语法，同时提供强类型、所有权与编译期元编程。",
        "Mojo 的编译器基于 MLIR：源码先降到 Mojo 自己的 MLIR 方言，再做优化与降级，最后生成 LLVM IR 与机器码。它没有 Python 解释器，也没有 GIL。",
        "Mojo 仍处于早期，工具链与标准库在快速变化。这一页的产物链展示的是它的结构，而不是某个稳定版本的实测输出。",
    ],
    "lineage": {
        "from": ["Python（语法）", "Swift / Rust（类型与所有权）", "MLIR / LLVM"],
        "to": ["AI 算子", "异构计算", "Python 超集生态"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.mojo",
            "cmd": "$ cat hello.mojo",
            "code": r"""fn main():
    print("Hello, world")""",
            "format": [
                ("扩展名", ".mojo / .🔥"),
                ("语法", "Python 风格缩进"),
                ("fn", "强类型函数；def 更动态"),
                ("内存", "所有权与借用"),
            ],
            "note": "`fn` 是强类型函数，`def` 更接近 Python 的动态语义。Mojo 同时提供两套函数形态，便于渐进迁移。",
        },
        {
            "label": "MLIR",
            "file": "hello.mlir",
            "cmd": "$ mojo build --emit=mlir hello.mojo",
            "code": r"""module {
  func.func @main() {
    %0 = "kgen.string"() {value = "Hello, world"} : () -> !kgen.string
    %1 = "kgen.print"(%0) : (!kgen.string) -> !kgen.none
    return
  }
}

; Mojo 方言建立在 MLIR 之上
; 之后逐层降级到 LLVM 方言
; 具体方言与指令随版本变化""",
            "format": [
                ("中间表示", "MLIR（Mojo 方言）"),
                ("优势", "多层 IR、可复用优化"),
                ("降级", "Mojo → LLVM 方言"),
                ("稳定", "方言仍在演进"),
            ],
            "note": "MLIR 允许 Mojo 在多个抽象层做优化，而不必一次性降到 LLVM。这也是它能同时服务 Python 语义与 GPU 代码的原因。",
        },
        {
            "label": "LLVM IR",
            "file": "hello.ll",
            "cmd": "$ mojo build --emit=llvm hello.mojo",
            "code": r"""define void @main() {
  %1 = call ptr @_EN4mojo...
  call void @_EN4mojo...print(ptr %1)
  ret void
}

; MLIR 降级后的 LLVM IR
; 字符串常量、运行时调用已具体化
; 交给 LLVM 优化与代码生成""",
            "format": [
                ("中间表示", "LLVM IR"),
                ("降级", "MLIR → LLVM"),
                ("优化", "LLVM 管线"),
                ("平台", "x86-64 / ARM / GPU"),
            ],
            "note": "到 LLVM IR 这一层，Mojo 已经和 C/C++/Rust/Swift 共享同一条后端流水线。",
        },
        {
            "label": "可执行",
            "file": "hello",
            "cmd": "$ mojo build hello.mojo -o hello && ./hello",
            "code": r"""$ ./hello
Hello, world

$ file hello
hello: ELF 64-bit LSB pie executable, x86-64 ...

; 原生代码，无 Python 解释器
; 仍可调用 Python 生态（通过互操作层）
; 也可生成 GPU kernel""",
            "format": [
                ("格式", "ELF / Mach-O / PE"),
                ("运行时", "Mojo 运行时（无 GIL）"),
                ("互操作", "可调用 Python / C"),
                ("GPU", "可生成 kernel"),
            ],
            "note": "Mojo 的目标不是「更快的 Python 脚本」，而是让 Python 语法进入系统与 GPU 的编译世界。产物因此是原生二进制。",
        },
    ],
    "tools": [
        {"era": "2020s", "editor": "VS Code + Mojo", "compiler": "mojo", "build": "mojo build", "pkg": "magic / pixi", "debug": "gdb / lldb"},
    ],
    "hello": {
        "file": "hello.mojo",
        "code": r"""fn main():
    print("Hello, world")""",
        "footprint": [
            {"stage": "源码", "size": "≈ 40 B", "w": 4},
            {"stage": "MLIR", "size": "≈ 300 B", "w": 10},
            {"stage": "LLVM IR", "size": "≈ 1 KB", "w": 14},
            {"stage": "hello.o", "size": "≈ 3 KB", "w": 18},
            {"stage": "可执行", "size": "≈ 500 KB", "w": 55},
        ],
        "why": [
            "<strong>MLIR</strong>：多层 IR 让 Python 语义与系统优化可以共存。",
            "<strong>fn/def</strong>：同一门语言里同时提供强类型与动态风格。",
            "<strong>无 GIL</strong>：原生线程与所有权模型，适合 AI 基础设施。",
            "<strong>Python 互操作</strong>：复用生态，而不是从零重建。",
        ],
    },
},

# ============================================================
"gleam": {
    "tagline": "BEAM 上的类型化语言：没有 null，没有异常，编译到 Erlang 或 JavaScript。",
    "intro": [
        "Gleam 由 Louis Pilfold 在 2016 年开始，2020 年代逐渐成熟。它运行在 Erlang 的 BEAM 上，也可以编译到 JavaScript；语法接近 Rust/ML，但保留 Erlang 的进程与容错模型。",
        "Gleam 的类型系统在编译期检查，没有 null、没有异常、没有隐式转换。它编译成 Erlang 源码（再交给 Erlang 编译器）或 JavaScript，因此产物仍是 `.beam` 或 `.mjs`。",
        "它与 Elixir/Erlang 可以互相调用：Gleam 模块在 BEAM 上就是普通模块，可以加入同一个 release。",
    ],
    "lineage": {
        "from": ["Erlang / BEAM", "Rust（类型系统）", "Elm（无异常）"],
        "to": ["BEAM 生态", "JavaScript 后端", "全栈 Gleam"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.gleam",
            "cmd": "$ cat hello.gleam",
            "code": r"""import gleam/io

pub fn main() {
  io.println("Hello, world")
}""",
            "format": [
                ("扩展名", ".gleam"),
                ("类型", "静态、推断"),
                ("无 null", "用 Option 表示缺失"),
                ("无异常", "用 Result 表示失败"),
            ],
            "note": "Gleam 没有 `null`，也没有异常。可能失败的操作返回 `Result`，可能缺失的值用 `Option`。",
        },
        {
            "label": "生成的 Erlang",
            "file": "hello.erl",
            "cmd": "$ gleam build",
            "code": r"""-module(hello).
-export([main/0]).

main() ->
    gleam_stdlib:println(<<"Hello, world">>).

; Gleam → Erlang 源码
; 再交给 erlc 生成 .beam
; 也可 --target javascript → .mjs""",
            "format": [
                ("后端", "Erlang / JavaScript"),
                ("中间", "Erlang 抽象语法"),
                ("构建", "gleam build"),
                ("互操作", "与 Erlang/Elixir 互相调用"),
            ],
            "note": "Gleam 不直接生成 BEAM 字节码，而是生成 Erlang 源码，再复用 Erlang 编译器。这降低了后端维护成本。",
        },
        {
            "label": "BEAM",
            "file": "hello.beam",
            "cmd": "$ ls build/dev/erlang/hello/_gleam_artefacts/",
            "code": r"""$ ls build/dev/erlang/hello/_gleam_artefacts/
hello.beam

$ xxd -l 16 hello.beam
00000000: 464f 5231 0000 01f4 4245 414d 0000 01c8  FOR1....BEAM....

; 与 Erlang/Elixir 相同的 FOR1 容器
; 模块名 hello
; 可热加载到运行中的 BEAM""",
            "format": [
                ("容器", "FOR1 / BEAM"),
                ("模块", "hello"),
                ("热加载", "BEAM 支持"),
                ("来源", "Erlang 编译器"),
            ],
            "note": "在 BEAM 眼里，Gleam 模块与 Erlang 模块没有区别。类型信息在编译后消失。",
        },
        {
            "label": "发布",
            "file": "erlang-shipment",
            "cmd": "$ gleam export erlang-shipment",
            "code": r"""$ gleam export erlang-shipment
$ ls build/erlang-shipment
entrypoint.sh  erts-15.0/  lib/

$ ./entrypoint.sh run
Hello, world

; shipment = ERTS + 所有 .beam + 启动脚本
; 目标机无需安装 Erlang
; 也可用 mix release 与 Elixir 一起打包""",
            "format": [
                ("打包", "gleam export erlang-shipment"),
                ("内容", "ERTS + .beam + 脚本"),
                ("部署", "拷贝目录"),
                ("混合", "可与 Elixir release 合并"),
            ],
            "note": "Gleam 的部署单位与 Erlang/Elixir 相同：一个带运行时与模块的 release 目录。",
        },
    ],
    "tools": [
        {"era": "2020s", "editor": "VS Code + Gleam", "compiler": "gleam", "build": "gleam build", "pkg": "gleam deps", "debug": "Erlang observer"},
    ],
    "hello": {
        "file": "hello.gleam",
        "code": r"""import gleam/io

pub fn main() {
  io.println("Hello, world")
}""",
        "footprint": [
            {"stage": "源码", "size": "≈ 70 B", "w": 4},
            {"stage": "Erlang", "size": "≈ 120 B", "w": 7},
            {"stage": ".beam", "size": "≈ 1.3 KB", "w": 16},
            {"stage": "shipment", "size": "≈ 25 MB", "w": 75},
            {"stage": "+ ERTS", "size": "≈ 40 MB", "w": 95},
        ],
        "why": [
            "<strong>生成 Erlang</strong>：复用成熟的 Erlang 编译器与 BEAM 生态。",
            "<strong>Result/Option</strong>：用类型取代 null 与异常。",
            "<strong>双后端</strong>：同一份代码可编译到 BEAM 或 JavaScript。",
            "<strong>shipment</strong>：与 Erlang/Elixir 共用 release 部署模型。",
        ],
    },
},

# ============================================================
"carbon": {
    "tagline": "Google 的 C++ 后继实验：保留 C++ 互操作，重做泛型与语法。",
    "intro": [
        "Carbon 是 Google 在 2022 年公开的实验性语言，目标是成为 C++ 的继任者，而不是立刻取代它。它强调与现有 C++ 代码的双向互操作，同时重做泛型、安全性与语法。",
        "Carbon 使用 LLVM 后端，中间有一层 Carbon 自己的语义 IR。工具链仍在早期：没有稳定的标准库与完整的生产级实现，很多细节会变化。",
        "这一页的产物链展示的是设计结构：源码 → Carbon IR → LLVM IR → 目标文件 → 可执行。样例用于说明层次，不代表某个发布版本的真实输出。",
    ],
    "lineage": {
        "from": ["C++", "Rust（部分安全性）", "Swift（泛型）", "LLVM"],
        "to": ["C++ 互操作", "实验性系统语言"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.carbon",
            "cmd": "$ cat hello.carbon",
            "code": r"""package Hello api;

fn Main() -> i32 {
  Core.Print("Hello, world\n");
  return 0;
}

// 语法与标准库仍在演进
// 样例用于展示结构""",
            "format": [
                ("扩展名", ".carbon"),
                ("包", "package … api"),
                ("入口", "fn Main() -> i32"),
                ("互操作", "可直接调用 C++"),
            ],
            "note": "Carbon 的 `Main` 返回 i32，和 C/C++ 的入口约定一致。它与 C++ 的互操作是设计核心，而不是事后补丁。",
        },
        {
            "label": "Carbon IR",
            "file": "hello.carbonir",
            "cmd": "$ carbon compile --dump-ir hello.carbon",
            "code": r"""fn @Main() -> i32 {
  %str = string.constant("Hello, world\n")
  %0 = call @Core.Print(%str)
  return i32 0
}

; Carbon 语义 IR（结构示意）
; 类型、泛型、生命周期在这一层检查
; 之后降级到 LLVM""",
            "format": [
                ("中间表示", "Carbon Semantics IR"),
                ("检查", "类型、泛型、生命周期"),
                ("输出", "文本 IR（实验性）"),
                ("稳定", "格式未固定"),
            ],
            "note": "Carbon 的 IR 尚未稳定，工具链可能改变文本格式。这里展示的是结构，而不是可依赖的接口。",
        },
        {
            "label": "LLVM IR",
            "file": "hello.ll",
            "cmd": "$ carbon compile --emit-llvm hello.carbon",
            "code": r"""define i32 @Main() {
entry:
  %0 = call i32 @Core_Print(ptr @.str)
  ret i32 0
}

; Carbon IR → LLVM IR
; 泛型已单态化
; 复用 LLVM 优化与后端""",
            "format": [
                ("中间表示", "LLVM IR"),
                ("泛型", "单态化"),
                ("后端", "LLVM"),
                ("互操作", "C++ ABI"),
            ],
            "note": "Carbon 的泛型在编译期单态化，这一点与 Rust 类似，而不是 Java 的擦除。",
        },
        {
            "label": "可执行",
            "file": "hello",
            "cmd": "$ carbon build hello.carbon -o hello && ./hello",
            "code": r"""$ ./hello
Hello, world

$ file hello
hello: ELF 64-bit LSB pie executable, x86-64 ...

; 原生代码，无虚拟机
; 可与 C++ 目标文件链接
; 工具链仍在早期""",
            "format": [
                ("格式", "ELF / Mach-O / PE"),
                ("运行时", "接近 C++"),
                ("链接", "可与 C++ 互操作"),
                ("状态", "实验性"),
            ],
            "note": "Carbon 的产物形态接近 C++：原生对象文件与可执行文件，没有 GC 或虚拟机。",
        },
    ],
    "tools": [
        {"era": "2020s", "editor": "VS Code", "compiler": "carbon", "build": "bazel / carbon", "pkg": "—", "debug": "lldb / gdb"},
    ],
    "hello": {
        "file": "hello.carbon",
        "code": r"""package Hello api;

fn Main() -> i32 {
  Core.Print("Hello, world\n");
  return 0;
}""",
        "footprint": [
            {"stage": "源码", "size": "≈ 100 B", "w": 4},
            {"stage": "Carbon IR", "size": "≈ 250 B", "w": 9},
            {"stage": "LLVM IR", "size": "≈ 600 B", "w": 12},
            {"stage": "hello.o", "size": "≈ 2 KB", "w": 16},
            {"stage": "可执行", "size": "≈ 20 KB", "w": 30},
        ],
        "why": [
            "<strong>语义 IR</strong>：在降级到 LLVM 前完成类型与泛型检查。",
            "<strong>单态化</strong>：泛型在编译期展开，没有运行时类型擦除。",
            "<strong>C++ 互操作</strong>：直接复用 C++ 的类型与 ABI，而不是通过 C 边界。",
            "<strong>实验性</strong>：工具链与标准库仍在变化，产物格式不保证稳定。",
        ],
    },
},

# ============================================================
"odin": {
    "tagline": "为游戏与图形编程设计的系统语言：数据导向、无隐藏分配、显式控制。",
    "intro": [
        "Odin 由 Ginger Bill 在 2016 年发布，目标是做一门适合游戏、图形与工具开发的系统语言。它强调数据导向设计、显式内存管理、编译期元编程，以及「没有隐藏行为」。",
        "Odin 默认不强制 GC（可选 `core:mem` 的跟踪分配器），没有继承、没有异常、没有运算符重载。它使用 LLVM 后端，也支持 C 与汇编互操作。",
        "Odin 的产物链很短：源码 → LLVM IR → 目标文件 → 可执行。标准库以源码形式随编译器分发，按需编译进程序。",
    ],
    "lineage": {
        "from": ["C", "Jai（设计理念）", "Go（部分语法）", "LLVM"],
        "to": ["游戏引擎", "图形工具", "原生应用"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.odin",
            "cmd": "$ cat hello.odin",
            "code": r"""package main

import "core:fmt"

main :: proc() {
    fmt.println("Hello, world")
}""",
            "format": [
                ("扩展名", ".odin"),
                ("包", "package main"),
                ("过程", "proc，显式参数"),
                ("内存", "显式分配器 / 可选 GC"),
            ],
            "note": "Odin 的过程用 `proc` 声明，调用约定与内存行为都显式。没有隐式构造函数或析构函数。",
        },
        {
            "label": "LLVM IR",
            "file": "hello.ll",
            "cmd": "$ odin build . -build-mode:llvm-ir -out:hello.ll",
            "code": r"""define internal void @main.main() {
  ...
  call void @fmt.println(...)
  ret void
}

; Odin 直接生成 LLVM IR
; 没有独立的字节码格式
; 标准库按需编译""",
            "format": [
                ("中间表示", "LLVM IR"),
                ("后端", "LLVM"),
                ("标准库", "源码，按需编译"),
                ("输出", "-build-mode:llvm-ir"),
            ],
            "note": "Odin 不经过 C：它直接生成 LLVM IR，再交给 LLVM 优化与代码生成。",
        },
        {
            "label": "目标文件",
            "file": "hello.o",
            "cmd": "$ odin build . -build-mode:obj",
            "code": r"""$ odin build . -build-mode:obj
$ file hello.o
hello.o: ELF 64-bit LSB relocatable, x86-64

$ nm hello.o | grep main
... T main.main
... U fmt.println

; 平台目标文件
; 可与 C 目标文件链接
; 默认不链接 GC""",
            "format": [
                ("格式", "ELF / COFF / Mach-O"),
                ("符号", "包名.过程名"),
                ("互操作", "C ABI / 汇编"),
                ("GC", "默认不启用"),
            ],
            "note": "Odin 的目标文件可以直接与 C 代码链接，适合嵌入现有引擎或工具链。",
        },
        {
            "label": "可执行",
            "file": "hello",
            "cmd": "$ odin build . -out:hello && ./hello",
            "code": r"""$ ./hello
Hello, world

$ file hello
hello: ELF 64-bit LSB executable, x86-64 ...

$ ls -lh hello
-rwxr-xr-x 1 user user 420K ... hello

; 静态链接 Odin 运行时
; 无 VM、无强制 GC
; 启动即执行""",
            "format": [
                ("格式", "原生可执行"),
                ("运行时", "Odin runtime（小）"),
                ("GC", "可选"),
                ("体积", "hello ≈ 420 KB"),
            ],
            "note": "Odin 的运行时很小：默认没有 GC 线程与虚拟机，适合对启动时间与内存布局敏感的场景。",
        },
    ],
    "tools": [
        {"era": "2020s", "editor": "VS Code + Odin", "compiler": "odin", "build": "odin build", "pkg": "ols / vendor", "debug": "gdb / lldb"},
    ],
    "hello": {
        "file": "hello.odin",
        "code": r"""package main

import "core:fmt"

main :: proc() {
    fmt.println("Hello, world")
}""",
        "footprint": [
            {"stage": "源码", "size": "≈ 80 B", "w": 4},
            {"stage": "LLVM IR", "size": "≈ 1.5 KB", "w": 12},
            {"stage": "hello.o", "size": "≈ 10 KB", "w": 18},
            {"stage": "可执行", "size": "≈ 420 KB", "w": 50},
            {"stage": "+ runtime", "size": "≈ 420 KB", "w": 50},
        ],
        "why": [
            "<strong>直接 LLVM</strong>：没有 C 中间层，编译路径短。",
            "<strong>显式内存</strong>：分配器由调用方提供，行为可预测。",
            "<strong>数据导向</strong>：语言特性服务于缓存友好与批量处理。",
            "<strong>小运行时</strong>：默认无 GC/VM，适合游戏与图形。",
        ],
    },
},

# ============================================================
"roc": {
    "tagline": "函数式语言，主打快速编译与「平台」抽象。",
    "intro": [
        "Roc 由 Richard Feldman 等人在 2022 年公开，是一门函数式语言，目标是让函数式编程在真实应用里更实用：编译快、错误信息好、与平台（platform）解耦。",
        "Roc 的「平台」把副作用与运行时交给宿主：语言只描述纯计算与任务，平台负责 I/O、并发与部署。同一份应用可以跑在 CLI、Web 服务器或 Wasm 上。",
        "Roc 的编译器有自己的 canonical IR 与 mono IR，最后生成 LLVM IR 或 Wasm。工具链仍在快速迭代，IR 不是稳定接口。",
    ],
    "lineage": {
        "from": ["Elm", "Haskell", "Rust（工具链体验）"],
        "to": ["函数式应用", "Wasm 平台", "快速编译语言"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.roc",
            "cmd": "$ cat hello.roc",
            "code": r"""app "hello"
    packages { pf: "https://github.com/roc-lang/basic-cli/releases/download/..." }
    imports [pf.Stdout]
    provides [main] to pf

main =
    Stdout.line "Hello, world"
# 输出：Hello, world""",
            "format": [
                ("扩展名", ".roc"),
                ("app", "声明平台与依赖"),
                ("provides", "向平台提供 main"),
                ("纯函数", "副作用由平台执行"),
            ],
            "note": "Roc 的应用必须声明平台（platform）。语言本身不直接做 I/O，而是返回平台能执行的任务。",
        },
        {
            "label": "Canonical / Mono IR",
            "file": "IR",
            "cmd": "$ roc check hello.roc",
            "code": r"""; Roc 编译器的中间表示（结构示意）
main : Task {} [Stdout]*
main =
    Stdout.line "Hello, world"

; canonicalize：去糖、解析名字
; type check：统一类型
; monomorphize：单态化
; 之后生成 LLVM IR / Wasm""",
            "format": [
                ("前端", "canonicalize + 类型检查"),
                ("单态化", "mono IR"),
                ("后端", "LLVM / Wasm"),
                ("稳定", "IR 非公开接口"),
            ],
            "note": "Roc 不把 IR 当作公开产物。这里展示的是编译阶段，而不是可依赖的文件格式。",
        },
        {
            "label": "LLVM IR",
            "file": "hello.ll",
            "cmd": "$ roc build hello.roc",
            "code": r"""define void @main() {
  ...
  call void @roc__mainForHost_1_exposed(...)
  ret void
}

; mono IR → LLVM IR
; 平台接口由 host 提供
; 之后交给 LLVM""",
            "format": [
                ("中间表示", "LLVM IR"),
                ("平台", "host 接口"),
                ("后端", "LLVM"),
                ("备选", "Wasm"),
            ],
            "note": "Roc 的「平台」在代码生成阶段表现为 host 接口：应用代码调用平台提供的函数，而不是直接系统调用。",
        },
        {
            "label": "可执行",
            "file": "hello",
            "cmd": "$ ./hello",
            "code": r"""$ ./hello
Hello, world

$ file hello
hello: ELF 64-bit LSB pie executable, x86-64 ...

; 原生二进制 + basic-cli 平台
; 也可编译到 Wasm
; 编译速度是设计目标之一""",
            "format": [
                ("格式", "ELF / Wasm"),
                ("平台", "basic-cli / web / wasm"),
                ("运行时", "由平台决定"),
                ("编译", "强调速度"),
            ],
            "note": "Roc 的产物取决于平台：同一份应用在 CLI 上是原生二进制，在 Web 上可能是 Wasm 模块。",
        },
    ],
    "tools": [
        {"era": "2020s", "editor": "VS Code + Roc", "compiler": "roc", "build": "roc build", "pkg": "roc 包", "debug": "roc repl"},
    ],
    "hello": {
        "file": "hello.roc",
        "code": r"""app "hello"
    packages { pf: "https://github.com/roc-lang/basic-cli/releases/download/..." }
    imports [pf.Stdout]
    provides [main] to pf

main =
    Stdout.line "Hello, world"
# 输出：Hello, world""",
        "footprint": [
            {"stage": "源码", "size": "≈ 230 B", "w": 6},
            {"stage": "IR", "size": "≈ 300 B", "w": 9},
            {"stage": "LLVM IR", "size": "≈ 1 KB", "w": 13},
            {"stage": "可执行", "size": "≈ 1.5 MB", "w": 65},
            {"stage": "+ 平台", "size": "≈ 2 MB", "w": 75},
        ],
        "why": [
            "<strong>平台抽象</strong>：语言只描述任务，I/O 交给宿主平台。",
            "<strong>单态化</strong>：类型在编译期具体化，运行时无类型擦除。",
            "<strong>快速编译</strong>：工具链体验是设计目标，不只是运行性能。",
            "<strong>Wasm 后端</strong>：同一份应用可以换平台部署。",
        ],
    },
},

# ============================================================
"v": {
    "tagline": "语法极简、编译极快、编译到 C 的系统语言。",
    "intro": [
        "V 由 Alexander Medvednikov 在 2019 年发布，目标是做一门小而快、语法简洁、无 GC（默认 autofree）的系统语言。它能编译到 C，也能编译到 JavaScript 或原生后端。",
        "V 的默认路径是生成 C：编译器把 V 源码翻译成 C，再调用系统 C 编译器。这与 Nim 类似，让 V 能复用成熟的 C 工具链与平台支持。",
        "V 仍处于早期，语言语义、标准库与「无 GC」的实现方式都有争议与变化。这一页展示的是它的产物结构，而不是对稳定性的承诺。",
    ],
    "lineage": {
        "from": ["Go（语法）", "Rust（内存安全目标）", "C"],
        "to": ["V 生态", "跨平台 CLI"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.v",
            "cmd": "$ cat hello.v",
            "code": r"""fn main() {
    println('Hello, world')
}""",
            "format": [
                ("扩展名", ".v"),
                ("字符串", "单引号"),
                ("函数", "fn main()"),
                ("内存", "autofree / 手动"),
            ],
            "note": "V 的字符串默认用单引号，`println` 是内置函数。语法刻意保持小。",
        },
        {
            "label": "生成的 C",
            "file": "hello.c",
            "cmd": "$ v -o hello.c hello.v",
            "code": r"""// Generated by V (示意)
VV_LOCAL_SYMBOL void main__main(void) {
    println(_SLIT("Hello, world"));
}

; V → C → 系统 C 编译器
; 运行时与标准库以 C 形式生成
; 也可输出 JS""",
            "format": [
                ("中间产物", "C 源码"),
                ("命令", "v -o hello.c"),
                ("后端", "C / JS / 原生"),
                ("编译", "tcc / gcc / clang"),
            ],
            "note": "V 的默认后端是 C 生成器。它把 V 的运行时、字符串与标准库一起翻译成 C。",
        },
        {
            "label": "目标文件",
            "file": "hello.o",
            "cmd": "$ cc -c hello.c -o hello.o",
            "code": r"""$ file hello.o
hello.o: ELF 64-bit LSB relocatable, x86-64

$ nm hello.o | grep main
... T main__main

; 由 C 编译器生成
; 可与其他 C 目标文件链接
; 运行时已包含在生成代码里""",
            "format": [
                ("格式", "平台对象文件"),
                ("生成", "C 编译器"),
                ("符号", "main__main"),
                ("互操作", "C ABI"),
            ],
            "note": "因为中间是 C，V 程序可以链接 C 库，也可以被 C 项目调用。",
        },
        {
            "label": "可执行",
            "file": "hello",
            "cmd": "$ v -o hello hello.v && ./hello",
            "code": r"""$ ./hello
Hello, world

$ file hello
hello: ELF 64-bit LSB pie executable, x86-64 ...

$ ls -lh hello
-rwxr-xr-x 1 user user 1.2M ... hello

; 编译速度是卖点
; 默认静态链接 V 运行时
; 语义与工具链仍在演进""",
            "format": [
                ("格式", "ELF / PE / Mach-O"),
                ("运行时", "V runtime（生成 C）"),
                ("体积", "hello ≈ 1.2 MB"),
                ("状态", "语言仍在早期"),
            ],
            "note": "V 的卖点是编译速度与简单语法；代价是生态与语义稳定性仍在建设中。",
        },
    ],
    "tools": [
        {"era": "2010s", "editor": "VS Code", "compiler": "v", "build": "v", "pkg": "vpm", "debug": "gdb"},
        {"era": "2020s", "editor": "VS Code + V", "compiler": "v", "build": "v", "pkg": "vpm", "debug": "gdb / lldb"},
    ],
    "hello": {
        "file": "hello.v",
        "code": r"""fn main() {
    println('Hello, world')
}""",
        "footprint": [
            {"stage": "源码", "size": "≈ 45 B", "w": 4},
            {"stage": "生成的 C", "size": "≈ 30 KB", "w": 25},
            {"stage": "hello.o", "size": "≈ 8 KB", "w": 16},
            {"stage": "可执行", "size": "≈ 1.2 MB", "w": 65},
            {"stage": "+ libc", "size": "≈ 2 MB", "w": 75},
        ],
        "why": [
            "<strong>C 后端</strong>：复用系统 C 编译器与 ABI。",
            "<strong>极小语法</strong>：语言表面小，上手成本低。",
            "<strong>快速编译</strong>：工具链速度是核心卖点。",
            "<strong>autofree</strong>：尝试在无 GC 的前提下自动管理内存。",
        ],
    },
},

# ============================================================
"sql": {
    "tagline": "声明式查询语言：你描述「要什么」，数据库决定「怎么取」。",
    "intro": [
        "SQL 由 Donald Chamberlin 与 Raymond Boyce 在 IBM 于 1970 年代设计，基于 Codd 的关系模型。1974 年的 SEQUEL 是它的前身，后来成为关系数据库的通用语言。",
        "SQL 是声明式的：你写的是结果集的条件，而不是执行步骤。数据库把 SQL 解析成语法树，再做逻辑/物理计划与优化，最后交给执行器。执行计划才是它的「编译产物」。",
        "不同数据库的计划格式不同，也没有可移植的字节码。理解执行计划，是理解 SQL 性能的核心。",
    ],
    "lineage": {
        "from": ["关系代数", "Codd 关系模型", "SEQUEL"],
        "to": ["PostgreSQL / MySQL / SQLite", "数据仓库", "查询优化器"],
    },
    "chain": [
        {
            "label": "查询",
            "file": "query.sql",
            "cmd": "$ cat query.sql",
            "code": r"""SELECT 'Hello, world' AS greeting;""",
            "format": [
                ("扩展名", ".sql"),
                ("类型", "声明式"),
                ("标准", "SQL-92 / SQL:2016 …"),
                ("方言", "PostgreSQL / MySQL / SQLite"),
            ],
            "note": "SQL 没有「主函数」。一条语句就是一个查询，结果是一个关系（表）。",
        },
        {
            "label": "语法树",
            "file": "parse tree",
            "cmd": "$ pg_query -j query.sql",
            "code": r"""{
  "version": 170000,
  "stmts": [{
    "stmt": {
      "SelectStmt": {
        "targetList": [{
          "ResTarget": {
            "name": "greeting",
            "val": { "A_Const": { "sval": "Hello, world" } }
          }
        }]
      }
    }
  }]
}

; PostgreSQL 的解析树（libpg_query，结构示意）
; 之后进入分析、重写、计划""",
            "format": [
                ("工具", "libpg_query / 数据库前端"),
                ("内容", "SelectStmt / ResTarget / A_Const"),
                ("下一步", "语义分析 + 重写"),
                ("稳定", "随数据库版本变化"),
            ],
            "note": "语法树只描述「写了什么」，还没有表、类型与权限信息。语义分析之后才变成可执行的计划。",
        },
        {
            "label": "执行计划",
            "file": "EXPLAIN",
            "cmd": "EXPLAIN (VERBOSE, COSTS OFF) SELECT 'Hello, world' AS greeting;",
            "code": r"""Result
  Output: 'Hello, world'::text

; 没有表，所以计划只有一个 Result 节点
; 有表时会看到 Seq Scan / Index Scan / Hash Join
; 计划 = 数据库的「编译产物」""",
            "format": [
                ("产物", "执行计划"),
                ("节点", "Result / Scan / Join / Aggregate"),
                ("优化", "基于代价（CBO）"),
                ("查看", "EXPLAIN / EXPLAIN ANALYZE"),
            ],
            "note": "执行计划是数据库内部的数据结构，`EXPLAIN` 只是它的文本表示。它不是可移植字节码，换数据库就会变。",
        },
        {
            "label": "结果集",
            "file": "result",
            "cmd": "$ psql -c \"SELECT 'Hello, world' AS greeting;\"",
            "code": r"""   greeting
---------------
 Hello, world
(1 row)

; 结果是一个关系（表）
; 列名、类型、行数由查询决定
; 客户端按协议解码""",
            "format": [
                ("形态", "关系 / 结果集"),
                ("协议", "PostgreSQL wire protocol"),
                ("类型", "列类型由查询与 schema 决定"),
                ("输出", "表格 / JSON / 游标"),
            ],
            "note": "SQL 的最终产物不是文件，而是结果集。数据库可能返回行、游标或流式结果。",
        },
    ],
    "tools": [
        {"era": "1970s", "editor": "终端", "compiler": "SEQUEL / System R", "build": "—", "pkg": "—", "debug": "EXPLAIN 前身"},
        {"era": "1990s", "editor": "psql / SQL*Plus", "compiler": "查询优化器", "build": "—", "pkg": "—", "debug": "EXPLAIN"},
        {"era": "2000s", "editor": "pgAdmin / TOAD", "compiler": "优化器", "build": "迁移脚本", "pkg": "—", "debug": "EXPLAIN ANALYZE"},
        {"era": "2020s", "editor": "DataGrip / VS Code", "compiler": "优化器", "build": "dbt / migration", "pkg": "—", "debug": "EXPLAIN ANALYZE / pg_stat"},
    ],
    "hello": {
        "file": "query.sql",
        "code": r"""SELECT 'Hello, world' AS greeting;""",
        "footprint": [
            {"stage": "SQL", "size": "≈ 38 B", "w": 4},
            {"stage": "语法树", "size": "≈ 500 B", "w": 12},
            {"stage": "计划", "size": "≈ 100 B", "w": 6},
            {"stage": "结果", "size": "1 行", "w": 5},
            {"stage": "+ 优化器", "size": "≈ 数十 MB", "w": 90},
        ],
        "why": [
            "<strong>声明式</strong>：只描述结果，不描述执行步骤。",
            "<strong>优化器</strong>：根据统计信息选择扫描、连接与聚合方式。",
            "<strong>计划</strong>：数据库的编译产物，随版本与数据分布变化。",
            "<strong>结果集</strong>：最终交付的是关系，不是文件。",
        ],
    },
},

# ============================================================
"assembly": {
    "tagline": "机器码的符号形式：每条指令对应一个操作，地址由汇编器填上。",
    "intro": [
        "汇编语言是机器指令的符号表示。1949 年前后，随着存储程序计算机普及，程序员开始用助记符代替二进制码，再由汇编器翻译成机器码。",
        "汇编与高级语言的关键区别是「几乎一一对应」：一条指令通常对应一条机器指令，寄存器、栈、系统调用都直接暴露。没有优化器，也没有运行时（除非你链接一个）。",
        "这一页用 x86-64 Linux 的 `_start` 程序展示完整链路：源码 → 汇编清单 → 目标文件 → 链接 → 反汇编。它也是理解 ELF 与调用约定的最小样本。",
    ],
    "lineage": {
        "from": ["机器码", "助记符", "早期汇编器"],
        "to": ["C 编译器后端", "反汇编 / 逆向", "引导程序"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.s",
            "cmd": "$ cat hello.s",
            "code": r"""    .section .rodata
msg:
    .ascii "Hello, world\n"
    .set len, . - msg

    .text
    .globl _start
_start:
    mov $1, %rax        # write
    mov $1, %rdi        # stdout
    lea msg(%rip), %rsi
    mov $len, %rdx
    syscall

    mov $60, %rax       # exit
    xor %rdi, %rdi
    syscall""",
            "format": [
                ("扩展名", ".s / .S（含预处理）"),
                ("语法", "GNU as（AT&T）"),
                ("入口", "_start，直接与内核对话"),
                ("依赖", "无 libc"),
            ],
            "note": "这段程序不链接 libc：它用 `syscall` 直接调用 write 与 exit。`_start` 是内核跳进来的第一个用户态地址。",
        },
        {
            "label": "汇编清单",
            "file": "hello.lst",
            "cmd": "$ as -alh hello.s -o hello.o",
            "code": r"""   1 0000 48C7C001000000      mov $1, %rax
   2 0007 48C7C701000000      mov $1, %rdi
   3 000e 488D3500000000      lea msg(%rip), %rsi
   4 0015 48C7C20C000000      mov $len, %rdx
   5 001c 0F05                syscall
...
; 地址 + 机器码 + 源码
; 标签与重定位由汇编器解析""",
            "format": [
                ("清单", "地址 / 机器码 / 源码"),
                ("机器码", "x86-64 指令字节"),
                ("重定位", "lea 的位移留待链接"),
                ("生成", "as -alh"),
            ],
            "note": "清单是汇编器给你的「逐行对照表」。`lea msg(%rip)` 的位移在目标文件里仍是 0，链接时才填。",
        },
        {
            "label": "目标文件",
            "file": "hello.o",
            "cmd": "$ readelf -h hello.o && nm hello.o",
            "code": r"""$ readelf -h hello.o | grep -E 'Type|Entry'
  Type:    REL (Relocatable file)
  Entry:   0x0

$ nm hello.o
0000000000000000 T _start
0000000000000000 r msg

$ readelf -S hello.o | grep -E 'text|rodata|rela'
  [ 1] .text
  [ 3] .rodata
  [ 5] .rela.text""",
            "format": [
                ("格式", "ELF64 · ET_REL"),
                ("段", ".text / .rodata / .rela.text"),
                ("符号", "_start 已定义，msg 只读"),
                ("入口", "目标文件没有入口地址"),
            ],
            "note": "目标文件里所有地址都是相对的，入口点也还是 0。链接器才决定程序装到哪个虚拟地址。",
        },
        {
            "label": "可执行",
            "file": "hello",
            "cmd": "$ ld -o hello hello.o && file hello",
            "code": r"""$ ld -o hello hello.o
$ file hello
hello: ELF 64-bit LSB executable, x86-64, statically linked

$ readelf -h hello | grep Entry
  Entry point address: 0x401000

$ ./hello
Hello, world""",
            "format": [
                ("链接", "ld，无 libc"),
                ("类型", "ET_EXEC / ET_DYN"),
                ("入口", "0x401000（示例）"),
                ("大小", "≈ 4 KB"),
            ],
            "note": "这是最小可执行文件之一：没有解释器、没有动态库，内核加载后直接跳到 `_start`。",
        },
        {
            "label": "反汇编",
            "file": "objdump",
            "cmd": "$ objdump -d hello",
            "code": r"""0000000000401000 <_start>:
  401000: 48 c7 c0 01 00 00 00  mov    $0x1,%rax
  401007: 48 c7 c7 01 00 00 00  mov    $0x1,%rdi
  40100e: 48 8d 35 f3 0f 00 00  lea    0xff3(%rip),%rsi
  401015: 48 c7 c2 0c 00 00 00  mov    $0xc,%rdx
  40101c: 0f 05                 syscall
  ...

; 机器码 → 汇编
; 地址已被链接器填好
; 反汇编是逆向工程的第一步""",
            "format": [
                ("工具", "objdump / llvm-objdump"),
                ("输入", "可执行文件"),
                ("输出", "地址 + 字节 + 助记符"),
                ("用途", "调试、逆向、验证"),
            ],
            "note": "反汇编展示的是最终机器码。与源码对照，可以看到链接器填上的地址与位移。",
        },
    ],
    "tools": [
        {"era": "1950s", "editor": "纸带 / 卡片", "compiler": "汇编器", "build": "装入器", "pkg": "—", "debug": "转储"},
        {"era": "1970s", "editor": "ed", "compiler": "as", "build": "make", "pkg": "—", "debug": "adb"},
        {"era": "2000s", "editor": "vim / Emacs", "compiler": "as / nasm", "build": "make", "pkg": "—", "debug": "gdb"},
        {"era": "2020s", "editor": "VS Code", "compiler": "as / nasm / llvm-mc", "build": "make / CMake", "pkg": "—", "debug": "gdb / lldb"},
    ],
    "hello": {
        "file": "hello.s",
        "code": r"""    .section .rodata
msg:
    .ascii "Hello, world\n"
    .set len, . - msg

    .text
    .globl _start
_start:
    mov $1, %rax
    mov $1, %rdi
    lea msg(%rip), %rsi
    mov $len, %rdx
    syscall

    mov $60, %rax
    xor %rdi, %rdi
    syscall""",
        "footprint": [
            {"stage": "源码", "size": "≈ 220 B", "w": 5},
            {"stage": "清单", "size": "≈ 400 B", "w": 8},
            {"stage": "hello.o", "size": "≈ 1.2 KB", "w": 14},
            {"stage": "可执行", "size": "≈ 4.5 KB", "w": 22},
            {"stage": "反汇编", "size": "≈ 300 B", "w": 6},
        ],
        "why": [
            "<strong>符号化</strong>：用助记符与标签代替裸机器码，地址交给汇编器。",
            "<strong>重定位</strong>：目标文件保留符号与重定位，链接器填最终地址。",
            "<strong>无运行时</strong>：直接 syscall，没有 libc 与启动代码。",
            "<strong>可逆</strong>：反汇编能把机器码还原成接近源码的形态。",
        ],
    },
},

# ============================================================
"shell": {
    "tagline": "操作系统的胶水：把命令、管道与文件描述符组合成程序。",
    "intro": [
        "Shell 是命令解释器，也是 Unix 的编程语言。1971 年 Stephen Bourne 在贝尔实验室写出 `sh`，此后 bash、zsh、fish 等方言延续了「命令 + 管道 + 重定向」的模型。",
        "Shell 没有目标文件，也没有字节码。它的「编译」发生在每次执行：解析脚本、展开变量与命令替换、fork/exec 进程、连接管道。可观察的中间产物是 pretty-print 的脚本、执行 trace 与 execve 调用。",
        "Shell 的强项不是数据结构，而是组合：`|` 连接进程，`>` 重定向文件描述符，`$()` 把命令输出变成字符串。理解这些机制，就理解了 Unix 的进程模型。",
    ],
    "lineage": {
        "from": ["Multics shell", "Unix 进程模型", "Bourne shell"],
        "to": ["bash / zsh / fish", "CI 脚本", "DevOps 工具链"],
    },
    "chain": [
        {
            "label": "脚本",
            "file": "hello.sh",
            "cmd": "$ cat hello.sh",
            "code": r"""#!/bin/sh
name="world"
printf 'Hello, %s\n' "$name"
# 输出：Hello, world""",
            "format": [
                ("扩展名", ".sh / .bash / .zsh"),
                ("shebang", "#!/bin/sh 指定解释器"),
                ("变量", "赋值无空格，引用加 $"),
                ("退出码", "$? 表示上一条命令状态"),
            ],
            "note": "shebang 让内核用指定解释器执行脚本，而不是把它当二进制。`$name` 在双引号内展开。",
        },
        {
            "label": "规范化脚本",
            "file": "pretty-print",
            "cmd": "$ bash --pretty-print hello.sh",
            "code": r"""#!/bin/sh
name=world
printf 'Hello, %s\n' "$name"

; bash 把脚本重新打印成规范形式
; 注释、空行与格式被重排
; 语法结构保持不变""",
            "format": [
                ("工具", "bash --pretty-print"),
                ("作用", "展示解析后的脚本结构"),
                ("保留", "命令、引用、重定向"),
                ("丢失", "注释与原始空白"),
            ],
            "note": "pretty-print 不是字节码，但它展示了 shell 解析后的结构。脚本在执行时仍然要重新解析。",
        },
        {
            "label": "执行 trace",
            "file": "xtrace",
            "cmd": "$ bash -x hello.sh",
            "code": r"""+ name=world
+ printf 'Hello, %s\n' world
Hello, world

; + 开头是 xtrace
; 变量已经展开
; 引号已被解析""",
            "format": [
                ("选项", "bash -x"),
                ("内容", "展开后的命令"),
                ("变量", "已替换为值"),
                ("参数", "已分词"),
            ],
            "note": "trace 展示的是「实际要执行的命令」，比源码更接近进程看到的 argv。",
        },
        {
            "label": "进程与系统调用",
            "file": "execve",
            "cmd": "$ strace -f -e execve sh hello.sh",
            "code": r"""execve("/bin/sh", ["sh", "hello.sh"], 0x... /* 环境 */) = 0
...
execve("/usr/bin/printf", ["printf", "Hello, %s\n", "world"], ...) = 0
Hello, world
+++ exited with 0 +++

; shell 本身是一个进程
; 每条外部命令 fork + exec
; 内建命令不创建新进程""",
            "format": [
                ("系统调用", "execve"),
                ("参数", "argv 数组"),
                ("进程", "fork + exec（外部命令）"),
                ("管道", "pipe + dup2"),
            ],
            "note": "Shell 的执行模型是进程组合：脚本本身不编译成机器码，而是不断解析、展开并创建子进程。",
        },
    ],
    "tools": [
        {"era": "1970s", "editor": "ed", "compiler": "sh", "build": "make", "pkg": "—", "debug": "sh -x"},
        {"era": "1980s", "editor": "vi", "compiler": "sh / csh", "build": "make", "pkg": "—", "debug": "sh -x"},
        {"era": "1990s", "editor": "vim / Emacs", "compiler": "bash / ksh", "build": "make / autoconf", "pkg": "—", "debug": "bash -x / set -x"},
        {"era": "2020s", "editor": "VS Code + ShellCheck", "compiler": "bash / zsh / dash", "build": "make / CI", "pkg": "—", "debug": "bash -x / strace"},
    ],
    "hello": {
        "file": "hello.sh",
        "code": r"""#!/bin/sh
printf 'Hello, world\n'""",
        "footprint": [
            {"stage": "脚本", "size": "≈ 36 B", "w": 4},
            {"stage": "规范化", "size": "≈ 36 B", "w": 4},
            {"stage": "trace", "size": "≈ 40 B", "w": 5},
            {"stage": "execve", "size": "1 次", "w": 6},
            {"stage": "+ shell", "size": "≈ 1 MB", "w": 70},
        ],
        "why": [
            "<strong>无编译产物</strong>：每次执行都重新解析与展开。",
            "<strong>进程组合</strong>：管道与重定向连接的是文件描述符，不是函数调用。",
            "<strong>字符串模型</strong>：变量与命令输出都是字符串，简单但不适合复杂数据。",
            "<strong>可观察</strong>：trace 与 execve 让执行过程可审计。",
        ],
    },
},

# ============================================================
"verilog": {
    "tagline": "描述硬件的语言：代码在并行，时间由时钟推进。",
    "intro": [
        "Verilog 由 Phil Moorby 在 Gateway Design 于 1984 年推出，用于数字电路仿真。它后来成为 IEEE 标准（Verilog-95/2001/2005，以及 SystemVerilog）。",
        "Verilog 不是「按顺序执行的程序」：`always` 块、赋值与连线描述的是并行硬件。它既可以被仿真器执行（生成波形），也可以被综合工具转换成门级网表，最终变成 FPGA 或 ASIC 的配置。",
        "「Hello world」在硬件里通常是一个闪烁的 LED：用计数器分频时钟。它的产物链从 RTL 源码到波形、网表，再到比特流。",
    ],
    "lineage": {
        "from": ["C（语法）", "硬件描述需求", "EDA 工具"],
        "to": ["SystemVerilog", "VHDL（竞争）", "HLS"],
    },
    "chain": [
        {
            "label": "RTL 源码",
            "file": "hello.v",
            "cmd": "$ cat hello.v",
            "code": r"""module hello(
    input  wire clk,
    output reg  led
);
    reg [23:0] count = 0;

    always @(posedge clk) begin
        count <= count + 1;
        led   <= count[23];
    end
endmodule""",
            "format": [
                ("扩展名", ".v / .sv"),
                ("模块", "module … endmodule"),
                ("并行", "always / assign 同时存在"),
                ("时序", "posedge clk 触发"),
            ],
            "note": "`always @(posedge clk)` 描述的是时钟边沿触发的寄存器，不是循环。`<=` 是非阻塞赋值，对应硬件寄存器更新。",
        },
        {
            "label": "仿真波形",
            "file": "hello.vcd",
            "cmd": "$ iverilog -o hello.vvp hello_tb.v hello.v && vvp hello.vvp",
            "code": r"""$ iverilog -o hello.vvp hello_tb.v hello.v
$ vvp hello.vvp
VCD info: dumpfile hello.vcd opened for output.

$ head -12 hello.vcd
$date
  2026-10-27 10:00:00
$end
$version
  Icarus Verilog
$end
$timescale
  1ns
$end
$scope module hello_tb $end""",
            "format": [
                ("格式", "VCD（值变化转储）"),
                ("工具", "Icarus Verilog / Verilator"),
                ("内容", "时间 + 信号 + 值"),
                ("用途", "调试、验证、波形查看"),
            ],
            "note": "仿真器的产物是波形，不是可执行文件。VCD 记录每个信号随时间的变化，GTKWave 等工具可以打开它。",
        },
        {
            "label": "门级网表",
            "file": "hello_netlist.v",
            "cmd": "$ yosys -p \"read_verilog hello.v; synth -top hello; write_verilog hello_netlist.v\"",
            "code": r"""$ yosys -p "read_verilog hello.v; synth -top hello; write_verilog hello_netlist.v"

// 综合后的网表（片段，示意）
module hello(clk, led);
  wire [23:0] count;
  ...
  LUT4 #(.INIT(16'h...)) ...
  DFF #(.WIDTH(1)) ...
endmodule

; RTL → 门级网表
; 触发器、查找表、连线
; 工艺库相关""",
            "format": [
                ("工具", "Yosys / 商业综合工具"),
                ("产物", "门级网表"),
                ("元件", "LUT / DFF / 连线"),
                ("绑定", "工艺库 / FPGA 原语"),
            ],
            "note": "综合把行为级描述变成门级连接。同一个 RTL 在不同 FPGA/工艺上会得到不同网表。",
        },
        {
            "label": "比特流",
            "file": "hello.bin",
            "cmd": "$ nextpnr-ice40 --hx8k --json hello.json --pcf hello.pcf --asc hello.asc && icepack hello.asc hello.bin",
            "code": r"""$ nextpnr-ice40 --hx8k --json hello.json \
      --pcf hello.pcf --asc hello.asc
$ icepack hello.asc hello.bin
$ ls -l hello.bin
-rw-r--r-- 1 user user 32K ... hello.bin

; 比特流 = 配置 FPGA 的位模式
; 与芯片型号强绑定
; 下载到板子后，硬件才开始工作""",
            "format": [
                ("格式", "FPGA 比特流（厂商相关）"),
                ("工具", "nextpnr / icepack / 厂商工具"),
                ("绑定", "芯片型号与封装"),
                ("部署", "JTAG / Flash 配置"),
            ],
            "note": "比特流不是机器码，而是 FPGA 内部连线与查找表的配置位。换一块芯片，比特流就不能用。",
        },
    ],
    "tools": [
        {"era": "1980s", "editor": "文本编辑器", "compiler": "Verilog-XL", "build": "make", "pkg": "—", "debug": "波形查看器"},
        {"era": "1990s", "editor": "Emacs", "compiler": "Synopsys VCS", "build": "Makefile", "pkg": "—", "debug": "DVE"},
        {"era": "2000s", "editor": "Eclipse / vim", "compiler": "ModelSim", "build": "Makefile", "pkg": "—", "debug": "ModelSim"},
        {"era": "2020s", "editor": "VS Code + Verilog", "compiler": "Verilator / Icarus / Yosys", "build": "make / FuseSoC", "pkg": "FuseSoC", "debug": "GTKWave / Surfer"},
    ],
    "hello": {
        "file": "hello.v",
        "code": r"""module hello(
    input  wire clk,
    output reg  led
);
    reg [23:0] count = 0;
    always @(posedge clk) begin
        count <= count + 1;
        led   <= count[23];
    end
endmodule""",
        "footprint": [
            {"stage": "RTL", "size": "≈ 200 B", "w": 5},
            {"stage": "VCD", "size": "≈ 1 MB", "w": 55},
            {"stage": "网表", "size": "≈ 4 KB", "w": 12},
            {"stage": "比特流", "size": "≈ 32 KB", "w": 25},
            {"stage": "+ 工具链", "size": "≈ 100 MB", "w": 90},
        ],
        "why": [
            "<strong>并行语义</strong>：always 块与连续赋值描述同时存在的硬件。",
            "<strong>仿真</strong>：VCD 波形是验证电路行为的主要产物。",
            "<strong>综合</strong>：RTL 被映射成 LUT、触发器与连线。",
            "<strong>比特流</strong>：配置位与芯片型号绑定，是硬件的「可执行文件」。",
        ],
    },
},

# ============================================================
"cuda": {
    "tagline": "在 GPU 上写并行程序：一个 kernel，成千上万个线程。",
    "intro": [
        "CUDA 由 NVIDIA 在 2007 年推出，把 GPU 变成通用并行计算平台。它在 C/C++ 上加了 `__global__`、`__device__`、`<<<grid, block>>>` 等扩展，让程序员直接描述线程层级。",
        "CUDA 的产物链分成主机与设备两部分：`.cu` 先被拆成主机 C++ 与设备代码；设备代码编译成 PTX（虚拟 ISA），再编译成 SASS（具体 GPU 的机器码），打包成 cubin/fatbin 嵌进宿主可执行文件。",
        "PTX 是可移植的中间层，SASS 不是。驱动可以在加载时把 PTX JIT 编译成目标 GPU 的 SASS；预编译的 SASS 只对特定架构有效。",
    ],
    "lineage": {
        "from": ["C / C++", "SIMT 并行模型", "GPU 图形管线"],
        "to": ["深度学习框架", "CUDA 库生态", "HIP / SYCL（竞争）"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.cu",
            "cmd": "$ cat hello.cu",
            "code": r"""#include <cstdio>

__global__ void hello() {
    printf("Hello from block %d, thread %d\n",
           blockIdx.x, threadIdx.x);
}

int main() {
    hello<<<1, 4>>>();
    cudaDeviceSynchronize();
}""",
            "format": [
                ("扩展名", ".cu / .cuh"),
                ("kernel", "__global__ 函数"),
                ("启动", "<<<grid, block>>>"),
                ("线程", "blockIdx / threadIdx"),
            ],
            "note": "`<<<1, 4>>>` 启动 1 个 block、4 个 thread。GPU 上的 printf 由设备运行时缓冲，最后拷回主机。",
        },
        {
            "label": "PTX",
            "file": "hello.ptx",
            "cmd": "$ nvcc -ptx hello.cu -o hello.ptx",
            "code": r"""//
// Generated by NVIDIA NVVM Compiler
//
.version 8.0
.target sm_80
.address_size 64

.visible .entry _Z5hellov()
{
    .reg .b32 %r<4>;
    ...
    call.uni _Z6printfPKcz, (...);
    ret;
}

; PTX = 虚拟 ISA
; 与具体 GPU 架构解耦
; 驱动可在加载时 JIT""",
            "format": [
                ("中间表示", "PTX（虚拟 ISA）"),
                ("目标", "sm_80 等虚拟架构"),
                ("可移植", "由驱动 JIT 到具体 GPU"),
                ("查看", "nvcc -ptx / cuobjdump -ptx"),
            ],
            "note": "PTX 是 CUDA 的「字节码」：它不直接运行，而是由驱动编译成目标 GPU 的 SASS。",
        },
        {
            "label": "SASS",
            "file": "hello.sass",
            "cmd": "$ cuobjdump -sass hello",
            "code": r"""Function : _Z5hellov
        /*0000*/  MOV R1, c[0x0][0x28] ;
        /*0010*/  MOV R2, c[0x0][0x218] ;
        ...
        /*00a0*/  CALL.ABS.NOINC 0x0 ;
        /*00b0*/  EXIT ;

; SASS = 具体 GPU 的机器码
; 与架构绑定（sm_80 / sm_90 …）
; 不可跨架构移植""",
            "format": [
                ("机器码", "SASS"),
                ("绑定", "GPU 架构（sm_xx）"),
                ("查看", "cuobjdump -sass"),
                ("执行", "GPU 流式多处理器"),
            ],
            "note": "SASS 是真正的 GPU 指令。不同架构的指令集不同，所以预编译的 SASS 不能跨代使用。",
        },
        {
            "label": "fatbin / 可执行",
            "file": "hello",
            "cmd": "$ nvcc -o hello hello.cu && file hello",
            "code": r"""$ nvcc -o hello hello.cu
$ file hello
hello: ELF 64-bit LSB pie executable, x86-64 ...

$ cuobjdump -elf hello | head
Fatbin elf code:
================
arch = sm_80
...

; 宿主 ELF 里嵌入 cubin / fatbin
; 主机代码 + 设备代码在同一个文件
; 运行时由 CUDA driver 加载""",
            "format": [
                ("宿主", "ELF 可执行"),
                ("设备", "cubin / fatbin"),
                ("嵌入", "宿主文件内"),
                ("加载", "CUDA driver"),
            ],
            "note": "CUDA 程序是一个宿主 ELF，里面嵌着设备代码。运行时驱动把设备代码加载到 GPU。",
        },
    ],
    "tools": [
        {"era": "2000s", "editor": "vim / Visual Studio", "compiler": "nvcc", "build": "make", "pkg": "—", "debug": "cuda-gdb"},
        {"era": "2010s", "editor": "Nsight / VS Code", "compiler": "nvcc / clang", "build": "CMake", "pkg": "—", "debug": "cuda-gdb / Nsight"},
        {"era": "2020s", "editor": "VS Code + Nsight", "compiler": "nvcc / nvc++", "build": "CMake", "pkg": "conda / pip", "debug": "cuda-gdb / compute-sanitizer"},
    ],
    "hello": {
        "file": "hello.cu",
        "code": r"""#include <cstdio>

__global__ void hello() {
    printf("Hello from block %d, thread %d\n",
           blockIdx.x, threadIdx.x);
}

int main() {
    hello<<<1, 4>>>();
    cudaDeviceSynchronize();
}""",
        "footprint": [
            {"stage": ".cu", "size": "≈ 220 B", "w": 5},
            {"stage": "PTX", "size": "≈ 2 KB", "w": 12},
            {"stage": "SASS", "size": "≈ 1.5 KB", "w": 10},
            {"stage": "cubin", "size": "≈ 8 KB", "w": 16},
            {"stage": "宿主 ELF", "size": "≈ 60 KB", "w": 45},
            {"stage": "+ driver", "size": "≈ 数百 MB", "w": 95},
        ],
        "why": [
            "<strong>PTX</strong>：虚拟 ISA，让同一份代码适配不同 GPU 架构。",
            "<strong>SASS</strong>：具体架构的机器码，性能最好但不可移植。",
            "<strong>fatbin</strong>：把多个架构的 cubin 嵌进宿主文件。",
            "<strong>SIMT</strong>：一个 kernel 由大量线程并行执行，硬件负责调度。",
        ],
    },
},

# ============================================================
"glsl": {
    "tagline": "运行在 GPU 上的着色器语言：每个像素一小段并行程序。",
    "intro": [
        "GLSL 是 OpenGL 的着色器语言，2002 年随 OpenGL 2.0 标准化。它描述顶点、片元、几何等 GPU 管线阶段，由驱动编译并在 GPU 上并行执行。",
        "GLSL 源码先被编译器（如 glslang）解析成 AST 与中间表示，再生成 SPIR-V（标准可移植 IR）。驱动把 SPIR-V 编译成具体 GPU 的机器码，在绘制时执行。",
        "片元着色器的「Hello world」是给像素写颜色：`fragColor = vec4(1.0, 0.5, 0.2, 1.0)`。它没有 printf，输出直接进入帧缓冲。",
    ],
    "lineage": {
        "from": ["C（语法）", "图形管线", "OpenGL ARB"],
        "to": ["SPIR-V", "Vulkan / WebGPU", "计算着色器"],
    },
    "chain": [
        {
            "label": "源着色器",
            "file": "hello.frag",
            "cmd": "$ cat hello.frag",
            "code": r"""#version 450

layout(location = 0) out vec4 fragColor;

void main() {
    fragColor = vec4(1.0, 0.5, 0.2, 1.0);
}""",
            "format": [
                ("扩展名", ".vert / .frag / .comp"),
                ("入口", "void main()"),
                ("输出", "out 变量 → 帧缓冲"),
                ("版本", "#version 450"),
            ],
            "note": "片元着色器每个像素执行一次。`fragColor` 是输出，写入当前 framebuffer 的对应位置。",
        },
        {
            "label": "AST / 中间树",
            "file": "glslang -i",
            "cmd": "$ glslangValidator -i hello.frag",
            "code": r"""hello.frag
Shader version: 450
0:? Sequence
0:5  Function Definition: main( (void)
0:6    Sequence
0:7      move second child to first child
0:7        'fragColor' (layout( location=0) out 4-component vector of float)
0:7        Constant:
0:7          1.000000
0:7          0.500000
0:7          0.200000
0:7          1.000000""",
            "format": [
                ("工具", "glslangValidator -i"),
                ("内容", "语法树 + 类型"),
                ("用途", "调试、验证"),
                ("下一步", "SPIR-V"),
            ],
            "note": "glslang 的 `-i` 打印中间树，能看清类型、布局与常量。它是驱动编译前的可读形态。",
        },
        {
            "label": "SPIR-V",
            "file": "hello.spv",
            "cmd": "$ glslangValidator -V -o hello.spv hello.frag && xxd -l 20 hello.spv",
            "code": r"""$ xxd -l 20 hello.spv
00000000: 0302 2307 0005 0000 0000 0000 0b00 0000  ..#.............
00000010: 0000 0000

; 03 02 23 07 = SPIR-V magic（0x07230203，小端）
; 00 05 00 00 = 版本 1.5
; 之后：generator / bound / schema
; 模块由指令流组成（OpCapability / OpEntryPoint …）""",
            "format": [
                ("魔数", "0x07230203"),
                ("格式", "32 位字指令流"),
                ("作用", "可移植的 GPU 中间表示"),
                ("生成", "glslangValidator -V"),
            ],
            "note": "SPIR-V 是 Vulkan/OpenGL 的可移植 IR。它不是机器码，驱动仍需把它编译成具体 GPU 的指令。",
        },
        {
            "label": "驱动与输出",
            "file": "spirv-dis / pixel",
            "cmd": "$ spirv-dis hello.spv",
            "code": r"""$ spirv-dis hello.spv | head
; SPIR-V
; Version: 1.5
OpCapability Shader
OpMemoryModel Logical GLSL450
OpEntryPoint Fragment %main "main"
OpExecutionMode %main OriginUpperLeft
...
%main = OpFunction %void None %3
...
OpStore %fragColor %color

; 驱动把 SPIR-V 编译成 GPU ISA
; 片元写入帧缓冲，得到最终像素
; 没有可执行文件，只有管线状态""",
            "format": [
                ("查看", "spirv-dis"),
                ("消费", "GPU 驱动"),
                ("输出", "帧缓冲像素"),
                ("部署", "随应用打包 .spv"),
            ],
            "note": "GLSL 的最终产物不是一个可执行文件，而是驱动内部的 GPU 程序与一帧像素。SPIR-V 是可分发的那一层。",
        },
    ],
    "tools": [
        {"era": "2000s", "editor": "文本编辑器", "compiler": "GLSL 驱动编译器", "build": "—", "pkg": "—", "debug": "RenderDoc 前身"},
        {"era": "2010s", "editor": "VS Code / RenderDoc", "compiler": "glslang / 驱动", "build": "CMake", "pkg": "—", "debug": "RenderDoc"},
        {"era": "2020s", "editor": "VS Code + glslang", "compiler": "glslang / DXC / 驱动", "build": "CMake / shaderc", "pkg": "vcpkg", "debug": "RenderDoc / Nsight"},
    ],
    "hello": {
        "file": "hello.frag",
        "code": r"""#version 450
layout(location = 0) out vec4 fragColor;
void main() {
    fragColor = vec4(1.0, 0.5, 0.2, 1.0);
}""",
        "footprint": [
            {"stage": ".frag", "size": "≈ 120 B", "w": 5},
            {"stage": "AST", "size": "≈ 500 B", "w": 10},
            {"stage": ".spv", "size": "≈ 600 B", "w": 12},
            {"stage": "GPU ISA", "size": "≈ 1 KB", "w": 14},
            {"stage": "+ driver", "size": "≈ 数百 MB", "w": 95},
        ],
        "why": [
            "<strong>并行执行</strong>：每个像素/顶点独立运行同一段着色器。",
            "<strong>SPIR-V</strong>：可移植的中间表示，跨驱动与 API。",
            "<strong>驱动编译</strong>：最终机器码由驱动按 GPU 架构生成。",
            "<strong>无文件产物</strong>：输出是像素与管线状态，不是可执行文件。",
        ],
    },
},

}

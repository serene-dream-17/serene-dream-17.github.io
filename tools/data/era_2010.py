# -*- coding: utf-8 -*-
"""第三批 · 2010s：12 门语言的档案与产物链数据。"""

LANGS = {

# ============================================================
"rust": {
    "tagline": "没有 GC 的内存安全：所有权、借用与生命周期，在编译期解决。",
    "intro": [
        "Rust 由 Graydon Hoare 在 Mozilla 开始设计，2010 年首次公开，2015 年发布 1.0。它要解决系统编程里的老问题：内存安全与并发安全，但不引入垃圾回收。",
        "Rust 用所有权（ownership）、借用（borrowing）与生命周期（lifetime）在编译期证明内存安全；运行时只需要处理栈、panic 与少量运行时库。错误在编译期出现，而不是在生产环境。",
        "它的产物链与 C/C++ 类似，但中间层不同：HIR → MIR → LLVM IR → 目标文件 → ELF。MIR 是借用检查与优化的核心，也是理解 Rust 语义的好入口。",
    ],
    "lineage": {
        "from": ["C++", "ML", "Haskell", "Cyclone"],
        "to": ["Linux 内核模块", "wasm", "Firefox Servo", "现代系统语言"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.rs",
            "cmd": "$ cat hello.rs",
            "code": r"""fn main() {
    println!("Hello, world");
}""",
            "format": [
                ("扩展名", ".rs"),
                ("宏", "println! 是宏，不是函数"),
                ("内存", "无 GC，所有权管理"),
                ("入口", "fn main()"),
            ],
            "note": "`println!` 末尾的 `!` 表示宏。它在编译期展开成格式化与 I/O 调用，参数类型在编译期检查。",
        },
        {
            "label": "MIR",
            "file": "hello.mir",
            "cmd": "$ rustc --emit=mir hello.rs",
            "code": r"""fn main() -> () {
    let mut _0: ();
    let _1: ();
    let _2: &str;

    _2 = const "Hello, world\n";
    _1 = std::io::_print(move _2) -> [return: bb1, unwind: bb2];
    _0 = const ();
    return;
}

; MIR = Mid-level IR
; 借用检查与部分优化在这一层
; 控制流图 + 基本块""",
            "format": [
                ("中间表示", "MIR"),
                ("形态", "控制流图 + 基本块"),
                ("用途", "借用检查、优化"),
                ("查看", "--emit=mir"),
            ],
            "note": "MIR 是 Rust 借用检查的舞台：所有权、借用、生命周期都在这一层被验证。",
        },
        {
            "label": "LLVM IR",
            "file": "hello.ll",
            "cmd": "$ rustc --emit=llvm-ir hello.rs",
            "code": r"""define void @main() unnamed_addr #0 {
start:
  %0 = call i32 (ptr, ...) @_ZN3std2io5stdio6_print...
  ret void
}

; MIR → LLVM IR
; 泛型已单态化，宏已展开
; 之后交给 LLVM 优化与代码生成""",
            "format": [
                ("中间表示", "LLVM IR"),
                ("单态化", "泛型实例已展开"),
                ("优化", "LLVM 管线"),
                ("后端", "LLVM → 目标机器码"),
            ],
            "note": "Rust 的泛型在编译期单态化：每个具体类型组合都会生成一份代码，这与 Java 的擦除相反。",
        },
        {
            "label": "目标文件",
            "file": "hello.o",
            "cmd": "$ rustc --emit=obj hello.rs && nm -C hello.o | grep main",
            "code": r"""$ nm -C hello.o | grep main
0000000000000000 T main

$ readelf -S hello.o | grep -E 'text|eh_frame|gcc_except'
  [ 1] .text
  [ 5] .eh_frame
  [ 6] .gcc_except_table

; panic=unwind 需要展开表
; 目标文件是标准 ELF
; 符号已单态化 + 修饰""",
            "format": [
                ("格式", "ELF / COFF / Mach-O"),
                ("符号", "Rust 修饰 + 单态化"),
                ("展开表", ".eh_frame / .gcc_except_table"),
                ("panic", "unwind 或 abort"),
            ],
            "note": "Rust 默认 panic=unwind，所以目标文件里有异常展开表。改成 panic=abort 可以显著缩小体积。",
        },
        {
            "label": "可执行",
            "file": "hello",
            "cmd": "$ rustc -O hello.rs -o hello && file hello && ldd hello",
            "code": r"""$ file hello
hello: ELF 64-bit LSB pie executable, x86-64, dynamically linked

$ ldd hello
  libgcc_s.so.1
  libc.so.6

$ ls -lh hello
-rwxr-xr-x 1 user user 3.8M ... hello

; 无 GC / 无虚拟机
; 默认链接 libc
; strip / panic=abort 可显著缩小""",
            "format": [
                ("格式", "ELF / PE / Mach-O"),
                ("运行时", "无 GC，无 VM"),
                ("依赖", "libc / libgcc_s"),
                ("体积", "默认约 3–4 MB（含调试）"),
            ],
            "note": "Rust 的「零成本抽象」最终体现在产物上：没有解释器、没有 GC、没有运行时调度器，只有机器码与少量运行时支持。",
        },
    ],
    "tools": [
        {"era": "2010s", "editor": "vim / VS Code", "compiler": "rustc", "build": "cargo", "pkg": "crates.io", "debug": "gdb / lldb"},
        {"era": "2020s", "editor": "VS Code + rust-analyzer", "compiler": "rustc", "build": "cargo", "pkg": "crates.io", "debug": "rust-gdb / lldb"},
    ],
    "hello": {
        "file": "hello.rs",
        "code": r"""fn main() {
    println!("Hello, world");
}""",
        "footprint": [
            {"stage": "源码", "size": "≈ 50 B", "w": 4},
            {"stage": "MIR", "size": "≈ 300 B", "w": 9},
            {"stage": "LLVM IR", "size": "≈ 1.2 KB", "w": 13},
            {"stage": "hello.o", "size": "≈ 4 KB", "w": 16},
            {"stage": "ELF", "size": "≈ 3.8 MB", "w": 80},
        ],
        "why": [
            "<strong>MIR</strong>：借用检查与优化的核心中间表示。",
            "<strong>单态化</strong>：泛型在编译期展开，没有运行时类型擦除。",
            "<strong>panic 展开表</strong>：unwind 语义需要 .eh_frame 与异常表。",
            "<strong>无运行时</strong>：没有 GC 与 VM，最终产物接近 C/C++。",
        ],
    },
},

# ============================================================
"typescript": {
    "tagline": "给 JavaScript 加上类型，然后在编译时把类型全部擦掉。",
    "intro": [
        "TypeScript 由 Anders Hejlsberg 在 Microsoft 主导，2012 年发布。它是 JavaScript 的超集：任何合法 JS 都是合法 TS，额外提供静态类型、接口、泛型与更早的错误检查。",
        "TypeScript 的「编译」主要是类型检查与语法降级：类型在运行时不存在，`tsc` 把它们擦除，输出仍然是 JavaScript。因此它的产物链没有字节码，只有 AST、JS、声明文件与打包结果。",
        "类型只在开发期存在，运行时无法依赖它做检查（除非用 zod 之类的库）。这一取舍让 TS 能无缝接入 JS 生态，也决定了它的产物形态。",
    ],
    "lineage": {
        "from": ["JavaScript", "C#（类型系统经验）", "Java"],
        "to": ["现代前端工程", "Deno / Bun 生态", "类型化 JS 工具链"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.ts",
            "cmd": "$ cat hello.ts",
            "code": r"""function hello(name: string): void {
  console.log(`Hello, ${name}`);
}

hello("world");""",
            "format": [
                ("扩展名", ".ts / .tsx / .mts"),
                ("类型", "静态，仅编译期"),
                ("目标", "ES3 — ESNext"),
                ("配置", "tsconfig.json"),
            ],
            "note": "类型标注只是编译期信息；`tsc` 输出时会把它们删掉，不会改变运行时行为。",
        },
        {
            "label": "AST",
            "file": "AST",
            "cmd": "$ node -e \"const ts=require('typescript'); ...\"",
            "code": r"""SourceFile hello.ts
  FunctionDeclaration hello
    parameters:
      Parameter name: string
    body:
      ExpressionStatement
        CallExpression console.log
          TemplateExpression `Hello, ${name}`
  ExpressionStatement
    CallExpression hello("world")

; TypeScript Compiler API 暴露完整 AST
; 类型检查器在 AST 上做符号解析与推断""",
            "format": [
                ("AST", "TypeScript AST"),
                ("接口", "typescript 包 / Compiler API"),
                ("类型检查", "绑定符号 + 推断 + 检查"),
                ("用途", "IDE、lint、代码生成"),
            ],
            "note": "TS 的 AST 是公开 API，语言服务、ESLint、Babel 插件都依赖它。类型信息附着在 AST 节点上。",
        },
        {
            "label": "JavaScript",
            "file": "hello.js",
            "cmd": "$ tsc hello.ts --target es2017",
            "code": r""""use strict";
function hello(name) {
    console.log(`Hello, ${name}`);
}
hello("world");
//# sourceMappingURL=hello.js.map

; 类型标注消失
; 模板字符串按 target 决定是否降级
; sourcemap 指回 .ts""",
            "format": [
                ("输出", "JavaScript"),
                ("类型", "全部擦除"),
                ("降级", "按 target 转换语法"),
                ("sourcemap", "映射回 .ts 行号"),
            ],
            "note": "TS 不生成运行时代码来检查类型，只做语法降级。类型错误在构建期由 tsc / IDE 报告。",
        },
        {
            "label": "声明与打包",
            "file": "hello.d.ts + bundle.js",
            "cmd": "$ tsc --declaration && esbuild hello.ts --bundle --minify",
            "code": r"""$ cat hello.d.ts
declare function hello(name: string): void;

$ esbuild hello.ts --bundle --minify --outfile=hello.min.js
$ ls -lh hello.min.js
-rw-r--r-- 1 user user 180 B ... hello.min.js

; .d.ts 是给消费者看的类型声明
; 打包器只做转译与压缩，不做类型检查""",
            "format": [
                (".d.ts", "类型声明，供其他项目使用"),
                ("打包", "esbuild / Vite / webpack"),
                ("类型检查", "与打包分离"),
                ("产物", "JS + 声明 + sourcemap"),
            ],
            "note": "现代工具链把「转译」与「类型检查」分开：esbuild/swc 快速转译，tsc 负责完整类型检查。",
        },
    ],
    "tools": [
        {"era": "2010s", "editor": "VS Code / WebStorm", "compiler": "tsc", "build": "gulp / webpack", "pkg": "npm", "debug": "Chrome DevTools"},
        {"era": "2020s", "editor": "VS Code", "compiler": "tsc / swc / esbuild", "build": "Vite / Next.js", "pkg": "npm / pnpm / bun", "debug": "DevTools"},
    ],
    "hello": {
        "file": "hello.ts",
        "code": r"""function hello(name: string): void {
  console.log(`Hello, ${name}`);
}
hello("world");""",
        "footprint": [
            {"stage": "hello.ts", "size": "≈ 90 B", "w": 4},
            {"stage": "AST", "size": "≈ 1.2 KB", "w": 14},
            {"stage": "hello.js", "size": "≈ 110 B", "w": 5},
            {"stage": ".d.ts", "size": "≈ 45 B", "w": 3},
            {"stage": "bundle", "size": "≈ 180 B", "w": 6},
        ],
        "why": [
            "<strong>类型擦除</strong>：类型只在编译期存在，运行时没有额外开销。",
            "<strong>AST</strong>：类型检查器与语言服务都在这棵树上工作。",
            "<strong>JS 输出</strong>：保持与浏览器/Node 兼容，不引入新运行时。",
            "<strong>.d.ts</strong>：把类型信息留给消费者，而不是运行环境。",
        ],
    },
},

# ============================================================
"swift": {
    "tagline": "Apple 的现代语言：LLVM、可选类型、协议与 ARC。",
    "intro": [
        "Swift 由 Chris Lattner 在 Apple 主导，2014 年发布。它继承了 Objective-C 的 Cocoa 生态，但语法更现代：类型推断、可选类型（Optional）、值类型、协议扩展、泛型。",
        "Swift 的产物链与 Rust 类似：源码 → SIL（Swift Intermediate Language）→ LLVM IR → 目标文件 → 可执行。SIL 负责泛型特化、ARC 优化与协议 witness 的生成。",
        "Swift 运行时提供 ARC、反射、协议一致性表与动态派发。在 Apple 平台上运行时随系统提供；在 Linux 上需要一起链接。",
    ],
    "lineage": {
        "from": ["Objective-C", "Rust（语法/安全）", "Haskell（部分）", "LLVM"],
        "to": ["SwiftUI 生态", "Server-side Swift", "Swift for TensorFlow（历史）"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.swift",
            "cmd": "$ cat hello.swift",
            "code": r"""print("Hello, world")

// print 是标准库函数
// 字符串是值类型""",
            "format": [
                ("扩展名", ".swift"),
                ("类型", "静态、推断"),
                ("内存", "ARC（引用计数）"),
                ("入口", "顶层代码或 @main"),
            ],
            "note": "Swift 的顶层代码会被包进隐式的 main。值类型（struct/enum）与引用类型（class）的语义不同。",
        },
        {
            "label": "SIL",
            "file": "hello.sil",
            "cmd": "$ swiftc -emit-sil hello.swift",
            "code": r"""sil @main : $@convention(c) (Int32, UnsafeMutablePointer<...>) -> Int32 {
bb0(%0 : $Int32, %1 : $...):
  %2 = function_ref @$s... : $@convention(thin) () -> ()
  %3 = apply %2() : $@convention(thin) () -> ()
  ...
  return %...
}

; SIL = Swift Intermediate Language
; 泛型特化、ARC 优化、协议 witness 在这一层
; 之后交给 LLVM""",
            "format": [
                ("中间语言", "SIL"),
                ("阶段", "raw → canonical → optimized"),
                ("职责", "ARC、泛型特化、协议"),
                ("查看", "swiftc -emit-sil"),
            ],
            "note": "SIL 是 Swift 编译器的核心中间层：它保留 Swift 语义（ARC、协议、泛型），又足够接近 LLVM。",
        },
        {
            "label": "LLVM IR",
            "file": "hello.ll",
            "cmd": "$ swiftc -emit-ir hello.swift",
            "code": r"""define i32 @main(i32 %0, ptr %1) #0 {
entry:
  %2 = call ptr @swift_allocObject(...)
  ...
  call void @print(...)
  ret i32 0
}

; ARC 调用已展开为 retain/release
; 协议 witness 已生成
; LLVM 负责优化与代码生成""",
            "format": [
                ("中间表示", "LLVM IR"),
                ("ARC", "retain/release 已显式"),
                ("泛型", "特化或 witness table"),
                ("后端", "LLVM"),
            ],
            "note": "Swift 的 ARC 在 SIL/LLVM 层被展开成 retain/release 调用；优化器会尝试消除多余的引用计数操作。",
        },
        {
            "label": "目标文件",
            "file": "hello.o",
            "cmd": "$ swiftc -emit-object hello.swift",
            "code": r"""$ file hello.o
hello.o: Mach-O 64-bit object arm64

$ nm hello.o | grep main
... T _main

; Apple 平台：Mach-O
; Linux：ELF
; 含 Swift 运行时引用与元数据""",
            "format": [
                ("格式", "Mach-O / ELF / COFF"),
                ("符号", "_main"),
                ("元数据", "类型、协议、反射"),
                ("运行时", "Swift runtime 引用"),
            ],
            "note": "Swift 目标文件里有大量类型元数据，用于反射、动态派发与协议一致性。",
        },
        {
            "label": "可执行",
            "file": "hello",
            "cmd": "$ swiftc hello.swift -o hello && ./hello",
            "code": r"""$ ./hello
Hello, world

$ file hello
hello: Mach-O 64-bit executable arm64

$ otool -L hello
  /usr/lib/swift/libswiftCore.dylib
  /usr/lib/libSystem.B.dylib

; Apple 平台：Swift 运行时随系统
; Linux：libswiftCore 需一起链接
; ARC 在运行时管理引用计数""",
            "format": [
                ("格式", "Mach-O / ELF"),
                ("运行时", "Swift runtime"),
                ("内存", "ARC"),
                ("部署", "Apple 平台自带运行时"),
            ],
            "note": "在 Apple 平台上 Swift 运行时属于系统；在 Linux/Windows 上则要随程序分发，体积会更大。",
        },
    ],
    "tools": [
        {"era": "2010s", "editor": "Xcode", "compiler": "swiftc", "build": "Xcode / SwiftPM", "pkg": "CocoaPods / Carthage", "debug": "lldb"},
        {"era": "2020s", "editor": "Xcode / VS Code", "compiler": "swiftc", "build": "SwiftPM / Xcode", "pkg": "SwiftPM", "debug": "lldb"},
    ],
    "hello": {
        "file": "hello.swift",
        "code": r"""print("Hello, world")""",
        "footprint": [
            {"stage": "源码", "size": "≈ 24 B", "w": 4},
            {"stage": "SIL", "size": "≈ 600 B", "w": 12},
            {"stage": "LLVM IR", "size": "≈ 1.5 KB", "w": 16},
            {"stage": "hello.o", "size": "≈ 4 KB", "w": 18},
            {"stage": "可执行", "size": "≈ 50 KB", "w": 35},
            {"stage": "+ Swift runtime", "size": "≈ 7 MB", "w": 85},
        ],
        "why": [
            "<strong>SIL</strong>：保留 Swift 语义的中间语言，负责 ARC 与泛型特化。",
            "<strong>LLVM IR</strong>：retain/release 与 witness table 已展开。",
            "<strong>元数据</strong>：反射、协议与动态派发依赖目标文件里的类型信息。",
            "<strong>运行时</strong>：Apple 平台随系统，其他平台需要分发。",
        ],
    },
},

# ============================================================
"kotlin": {
    "tagline": "JetBrains 的 JVM 语言：空安全、扩展函数与协程，Android 的首选。",
    "intro": [
        "Kotlin 由 JetBrains 在 2011 年发布，2016 年发布 1.0，2017 年成为 Android 官方支持语言。它在 JVM 上与 Java 完全互操作，但语法更简洁，并在类型系统里区分可空与非空。",
        "Kotlin 编译成 JVM 字节码，类名与文件名有关（`Hello.kt` → `HelloKt.class`）。编译器把 Kotlin 特有的信息（空安全、默认参数、扩展函数）编码进 `@Metadata` 注解，供 Kotlin 编译器读取。",
        "Kotlin 还能编译到 JavaScript、Native 与 Wasm。Android 上则走 `.class → d8 → .dex` 的路线，与 Java 相同。",
    ],
    "lineage": {
        "from": ["Java", "Scala", "C#", "Groovy（部分）"],
        "to": ["Android 生态", "Kotlin Multiplatform", "Compose"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "Hello.kt",
            "cmd": "$ cat Hello.kt",
            "code": r"""fun main() {
    println("Hello, world")
}""",
            "format": [
                ("扩展名", ".kt / .kts"),
                ("空安全", "String 与 String? 不同"),
                ("顶层函数", "无需类"),
                ("入口", "fun main()"),
            ],
            "note": "Kotlin 允许顶层函数。`Hello.kt` 里的 main 会被编译进 `HelloKt` 类，作为静态方法。",
        },
        {
            "label": "字节码",
            "file": "HelloKt.class",
            "cmd": "$ kotlinc Hello.kt && javap -c HelloKt",
            "code": r"""$ ls HelloKt.class
HelloKt.class

$ javap -c HelloKt
public final class HelloKt {
  public static final void main();
    Code:
       0: ldc           #...  // String Hello, world
       2: invokevirtual #...  // println
       5: return
}

; @Metadata 注解携带 Kotlin 类型信息
; 空安全在字节码里变成 Intrinsics 检查或注解""",
            "format": [
                ("产物", "JVM .class"),
                ("类名", "文件名 + Kt"),
                ("元数据", "@Metadata 注解"),
                ("空安全", "编译期检查 + 运行时断言"),
            ],
            "note": "Kotlin 的 `.class` 与 Java 完全兼容；`@Metadata` 让 Kotlin 编译器知道可空性、默认参数与扩展函数。",
        },
        {
            "label": "JAR",
            "file": "hello.jar",
            "cmd": "$ kotlinc Hello.kt -include-runtime -d hello.jar && java -jar hello.jar",
            "code": r"""$ java -jar hello.jar
Hello, world

$ unzip -l hello.jar | head
  META-INF/MANIFEST.MF
  HelloKt.class
  kotlin/...
  kotlin-stdlib...

; -include-runtime 把 kotlin-stdlib 打进去
; 否则运行时需要单独提供""",
            "format": [
                ("容器", "JAR"),
                ("依赖", "kotlin-stdlib"),
                ("入口", "Main-Class: HelloKt"),
                ("互操作", "可被 Java 调用"),
            ],
            "note": "Kotlin 标准库是运行时依赖。`-include-runtime` 生成可独立运行的 jar，但体积会变大。",
        },
        {
            "label": "DEX（Android）",
            "file": "classes.dex",
            "cmd": "$ d8 --output dex hello.jar",
            "code": r"""$ d8 --output dex hello.jar
$ xxd -l 8 classes.dex
00000000: 6465 780a 3033 3500                    dex\n035.

; Android 不跑 JVM 字节码
; .class → d8 → .dex（寄存器式）
; ART 在安装时 AOT，运行时 JIT
; Kotlin 与 Java 共用这条链""",
            "format": [
                ("转换", ".class → .dex"),
                ("字节码", "寄存器式（ART）"),
                ("工具", "d8 / R8"),
                ("执行", "ART：AOT + JIT"),
            ],
            "note": "Kotlin 在 Android 上的产物与 Java 相同：dex。`@Metadata` 在运行时对 ART 不可见，只服务 Kotlin 编译期。",
        },
    ],
    "tools": [
        {"era": "2010s", "editor": "IntelliJ IDEA / Android Studio", "compiler": "kotlinc", "build": "Gradle", "pkg": "Maven Central", "debug": "IDE 调试器"},
        {"era": "2020s", "editor": "Android Studio / VS Code", "compiler": "kotlinc", "build": "Gradle", "pkg": "Maven Central", "debug": "IDE / lldb"},
    ],
    "hello": {
        "file": "Hello.kt",
        "code": r"""fun main() {
    println("Hello, world")
}""",
        "footprint": [
            {"stage": "源码", "size": "≈ 45 B", "w": 4},
            {"stage": ".class", "size": "≈ 1.1 KB", "w": 14},
            {"stage": "jar", "size": "≈ 1.4 KB", "w": 16},
            {"stage": ".dex", "size": "≈ 900 B", "w": 12},
            {"stage": "+ kotlin-stdlib", "size": "≈ 1.7 MB", "w": 75},
        ],
        "why": [
            "<strong>顶层函数</strong>：编译进文件对应的 `*Kt` 类，作为静态方法。",
            "<strong>@Metadata</strong>：把 Kotlin 语义（可空性、默认参数）留给编译器。",
            "<strong>stdlib</strong>：标准库是运行时依赖，影响分发体积。",
            "<strong>dex</strong>：Android 复用 Java 的工具链，只换最后一步。",
        ],
    },
},

# ============================================================
"elixir": {
    "tagline": "BEAM 上的现代函数式：Ruby 式语法、Actor 并发、Phoenix 实时应用。",
    "intro": [
        "Elixir 由 José Valim 在 2011 年发布，运行在 Erlang 的 BEAM 虚拟机上。它借了 Ruby 的语法与开发者体验，同时保留 Erlang 的进程模型、监督树与容错。",
        "Elixir 的编译产物是 `.beam`：模块名 `Elixir.Hello`，内容是 BEAM 字节码、原子表、字符串表与调试信息。编译由 Erlang 的编译器完成，Elixir 宏在编译期展开。",
        "Phoenix 框架把 Elixir 带到 Web 实时应用；Mix 与 releases 把项目、依赖与运行时打包成可部署产物。",
    ],
    "lineage": {
        "from": ["Erlang", "Ruby（语法）", "Clojure（部分）"],
        "to": ["Phoenix 生态", "LiveView", "Gleam（互操作）"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.ex",
            "cmd": "$ cat hello.ex",
            "code": r"""defmodule Hello do
  def world do
    IO.puts("Hello, world")
  end
end

Hello.world()""",
            "format": [
                ("扩展名", ".ex / .exs"),
                ("模块", "defmodule"),
                ("函数", "def / defp"),
                ("编译", "elixirc / mix compile"),
            ],
            "note": "`.ex` 是编译文件，`.exs` 是脚本。模块名会变成 `Elixir.Hello`，在 BEAM 里是普通原子。",
        },
        {
            "label": "展开后的 AST",
            "file": "quoted",
            "cmd": "iex> quote do: IO.puts(\"Hello, world\")",
            "code": r"""iex> quote do: IO.puts("Hello, world")
{{:., [], [{:__aliases__, [alias: false], [:IO]}, :puts]}, [],
 ["Hello, world"]}

; Elixir 代码先被解析成 quoted 表达式
; 宏在编译期展开这些表达式
; 最终交给 Erlang 编译器""",
            "format": [
                ("AST", "quoted expression（三元组）"),
                ("宏", "编译期展开"),
                ("目标", "Erlang abstract format"),
                ("产物", ".beam"),
            ],
            "note": "Elixir 的宏不是文本替换：它接收 quoted 表达式，返回新表达式，再交给 Erlang 编译器。",
        },
        {
            "label": "BEAM",
            "file": "Elixir.Hello.beam",
            "cmd": "$ elixirc hello.ex && ls Elixir.Hello.beam",
            "code": r"""$ xxd -l 32 Elixir.Hello.beam
00000000: 464f 5231 0000 02a4 4245 414d 0000 026c  FOR1....BEAM...l
00000010: 436f 6465 0000 01d8 4174 6f6d 0000 0054  Code....Atom...T

; 同一个 .beam 容器格式：
;   FOR1 / BEAM / Code / Atom / StrT / Attr
; 模块名：Elixir.Hello（原子）
; 字节码由 Erlang 编译器生成""",
            "format": [
                ("容器", "FOR1（同 Erlang）"),
                ("模块", "Elixir.Hello"),
                ("字节码", "BEAM 指令"),
                ("元数据", "Atom / StrT / Attr"),
            ],
            "note": "Elixir 没有自己的字节码：它复用 Erlang 的编译器与 BEAM 文件格式。",
        },
        {
            "label": "Release",
            "file": "hello.tar.gz",
            "cmd": "$ mix release && ls _build/prod/rel/hello",
            "code": r"""$ mix release
$ ls _build/prod/rel/hello
bin/  erts-15.0/  lib/  releases/

$ ./bin/hello start
Hello, world

; release = ERTS + 应用 + 依赖 + 启动脚本
; 目标机不需要安装 Elixir / Erlang
; 热升级由 release_handler 支持""",
            "format": [
                ("打包", "mix release"),
                ("内容", "ERTS + .beam + 配置 + 脚本"),
                ("体积", "通常 20–60 MB"),
                ("部署", "拷贝目录即可"),
            ],
            "note": "Elixir 的部署单位是 release 目录，而不是单个二进制。虚拟机和所有模块一起打包。",
        },
    ],
    "tools": [
        {"era": "2010s", "editor": "Emacs / VS Code", "compiler": "elixirc", "build": "mix", "pkg": "Hex", "debug": "IEx / observer"},
        {"era": "2020s", "editor": "VS Code + ElixirLS", "compiler": "elixirc", "build": "mix", "pkg": "Hex", "debug": "IEx / observer"},
    ],
    "hello": {
        "file": "hello.ex",
        "code": r"""IO.puts("Hello, world")""",
        "footprint": [
            {"stage": "源码", "size": "≈ 24 B", "w": 4},
            {"stage": "quoted", "size": "≈ 120 B", "w": 7},
            {"stage": ".beam", "size": "≈ 1.4 KB", "w": 16},
            {"stage": "release", "size": "≈ 25 MB", "w": 75},
            {"stage": "+ ERTS", "size": "≈ 40 MB", "w": 90},
        ],
        "why": [
            "<strong>quoted AST</strong>：宏在编译期改写表达式，是 Elixir DSL 的基础。",
            "<strong>BEAM 容器</strong>：与 Erlang 共用 FOR1 块格式与字节码。",
            "<strong>release</strong>：把运行时与所有模块打包，目标机无需安装环境。",
            "<strong>热升级</strong>：BEAM 允许替换模块，release_handler 负责版本切换。",
        ],
    },
},

# ============================================================
"julia": {
    "tagline": "为科学计算设计的语言：多重派发、JIT、接近 C 的速度。",
    "intro": [
        "Julia 由 Jeff Bezanson、Stefan Karpinski、Viral Shah 与 Alan Edelman 在 MIT 开发，2012 年发布。它想同时要 Python 的易用、R 的统计表达力与 C/Fortran 的性能。",
        "Julia 的核心是多重派发：函数由参数类型组合决定具体方法，JIT 为每组具体类型生成特化代码。它的编译链是 lowered AST → typed IR → LLVM IR → 机器码。",
        "Julia 没有标准的可分发字节码。预编译缓存（`.ji`）、系统镜像（sysimage）与 PackageCompiler 生成的 `.so` 是常见的产物形态。",
    ],
    "lineage": {
        "from": ["MATLAB", "Lisp", "Python", "Fortran"],
        "to": ["SciML 生态", "Flux.jl", "科学计算语言"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.jl",
            "cmd": "$ cat hello.jl",
            "code": r"""greet(name) = println("Hello, ", name)

greet("world")""",
            "format": [
                ("扩展名", ".jl"),
                ("派发", "多重派发"),
                ("类型", "动态 + 可选类型标注"),
                ("执行", "JIT"),
            ],
            "note": "`greet` 没有类型标注。第一次用某个参数类型调用时，Julia 会为该组合生成特化代码。",
        },
        {
            "label": "Lowered AST",
            "file": "@code_lowered",
            "cmd": "julia> @code_lowered greet(\"world\")",
            "code": r"""CodeInfo(
1 ─ %1 = Main.println("Hello, ", name)
└──      return %1
)

; 语法糖已去掉
; 仍是未定型的 IR
; 类型未知，方法未特化""",
            "format": [
                ("中间表示", "lowered CodeInfo"),
                ("类型", "未知"),
                ("查看", "@code_lowered"),
                ("下一层", "类型推断"),
            ],
            "note": "Lowered AST 是 Julia 去糖后的形式：宏已展开，控制流已显式，但还没有类型信息。",
        },
        {
            "label": "Typed IR",
            "file": "@code_typed",
            "cmd": "julia> @code_typed greet(\"world\")",
            "code": r"""CodeInfo(
1 ─ %1 = Base.println("Hello, ", name)::Nothing
└──      return %1
) => Nothing

; 类型推断完成
; 每个值都有具体类型
; 方法特化由参数类型决定""",
            "format": [
                ("中间表示", "typed CodeInfo"),
                ("类型", "具体化"),
                ("派发", "已选定方法"),
                ("查看", "@code_typed"),
            ],
            "note": "类型推断是 Julia 性能的关键：推断出具体类型后，才能生成无装箱的机器码。",
        },
        {
            "label": "LLVM IR",
            "file": "@code_llvm",
            "cmd": "julia> @code_llvm greet(\"world\")",
            "code": r"""define void @julia_greet_1234(ptr %0, ptr %1) #0 {
top:
  %2 = call ptr @jl_apply_generic(...)
  ...
  ret void
}

; typed IR → LLVM IR
; 未特化的动态调用仍走 jl_apply_generic
; 热点路径会被内联与特化""",
            "format": [
                ("中间表示", "LLVM IR"),
                ("特化", "按参数类型生成"),
                ("动态回退", "jl_apply_generic"),
                ("查看", "@code_llvm"),
            ],
            "note": "`@code_llvm` 展示的是某个具体类型组合生成的 LLVM IR；换一种参数类型，代码可能完全不同。",
        },
        {
            "label": "原生代码 / 镜像",
            "file": "@code_native",
            "cmd": "julia> @code_native greet(\"world\")",
            "code": r"""julia> @code_native greet("world")
  .text
  ...
  movq  %rdi, %rax
  callq jl_apply_generic
  retq

; JIT：进程内生成机器码
; 预编译：.ji 缓存
; 部署：PackageCompiler 生成 sysimage .so 或独立 app""",
            "format": [
                ("JIT", "进程内生成机器码"),
                ("缓存", ".ji 预编译文件"),
                ("镜像", "sysimage（.so）"),
                ("部署", "PackageCompiler"),
            ],
            "note": "Julia 的产物通常是「运行时 + 缓存/镜像」，而不是单个可执行文件。PackageCompiler 可以生成独立应用。",
        },
    ],
    "tools": [
        {"era": "2010s", "editor": "Juno / VS Code", "compiler": "Julia JIT", "build": "Pkg", "pkg": "Pkg / General", "debug": "Debugger.jl"},
        {"era": "2020s", "editor": "VS Code + Julia", "compiler": "Julia JIT", "build": "Pkg / PackageCompiler", "pkg": "Pkg", "debug": "Debugger.jl"},
    ],
    "hello": {
        "file": "hello.jl",
        "code": r"""println("Hello, world")""",
        "footprint": [
            {"stage": "源码", "size": "≈ 24 B", "w": 4},
            {"stage": "lowered", "size": "≈ 150 B", "w": 8},
            {"stage": "typed", "size": "≈ 180 B", "w": 9},
            {"stage": "LLVM IR", "size": "≈ 1 KB", "w": 14},
            {"stage": "机器码", "size": "≈ 200 B", "w": 6},
            {"stage": "+ sysimage", "size": "≈ 200 MB", "w": 100},
        ],
        "why": [
            "<strong>多重派发</strong>：方法由参数类型组合决定，JIT 为每种组合特化。",
            "<strong>Typed IR</strong>：类型推断完成后，才能生成无装箱代码。",
            "<strong>LLVM</strong>：Julia 自己不写后端，直接复用 LLVM。",
            "<strong>sysimage</strong>：把常用代码预编译进镜像，缩短启动时间。",
        ],
    },
},

# ============================================================
"dart": {
    "tagline": "Google 的 UI 语言：JIT 开发、AOT 发布，Flutter 的底座。",
    "intro": [
        "Dart 由 Lars Bak 等人在 Google 设计，2011 年发布。它最初想替代 JavaScript，后来转向「客户端 UI 语言」，并在 2017 年成为 Flutter 的编程语言。",
        "Dart 的产物链有两条：开发时用 JIT（热重载），发布时用 AOT。两者都经过 Kernel AST（`.dill`）这一层；AOT 把 Kernel 编译成机器码，连同精简后的运行时打进可执行文件或 Flutter 的 `libapp.so`。",
        "空安全（sound null safety）在编译期检查，运行时不需要额外判空。这让 Dart 在 UI 场景里既快又相对安全。",
    ],
    "lineage": {
        "from": ["Java", "JavaScript", "C#（部分）", "Flutter"],
        "to": ["Flutter 生态", "Web / Wasm 后端"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.dart",
            "cmd": "$ cat hello.dart",
            "code": r"""void main() {
  print('Hello, world');
}""",
            "format": [
                ("扩展名", ".dart"),
                ("类型", "静态，空安全"),
                ("入口", "void main()"),
                ("运行", "JIT（开发）/ AOT（发布）"),
            ],
            "note": "Dart 的 `main` 可以没有返回值，也可以是 `Future<void>`（异步）。空安全在编译期检查。",
        },
        {
            "label": "Kernel",
            "file": "hello.dill",
            "cmd": "$ dart compile kernel hello.dart",
            "code": r"""$ dart compile kernel hello.dart
$ ls -lh hello.dill
-rw-r--r-- 1 user user 12K ... hello.dill

$ file hello.dill
hello.dill: data

; Kernel = Dart 的二进制 AST / IR
; 前端（解析、类型检查）产物
; JIT 与 AOT 都从 Kernel 开始""",
            "format": [
                ("格式", "Kernel binary（.dill）"),
                ("内容", "AST + 类型 + 常量"),
                ("作用", "前端与后端的分界"),
                ("稳定", "不保证跨 SDK 版本"),
            ],
            "note": "`.dill` 是 Dart 前端的产物，也是 JIT/AOT 的共同输入。它不是公开稳定的分发格式。",
        },
        {
            "label": "AOT 可执行",
            "file": "hello",
            "cmd": "$ dart compile exe hello.dart -o hello",
            "code": r"""$ dart compile exe hello.dart -o hello
$ ./hello
Hello, world

$ file hello
hello: ELF 64-bit LSB executable, x86-64 ...

$ ls -lh hello
-rwxr-xr-x 1 user user 5.2M ... hello

; AOT：Kernel → 机器码
; 运行时被裁剪后嵌入
; 无 JIT，启动快""",
            "format": [
                ("命令", "dart compile exe"),
                ("产物", "原生 ELF / PE / Mach-O"),
                ("运行时", "裁剪后的 Dart runtime"),
                ("体积", "hello ≈ 5 MB"),
            ],
            "note": "AOT 产物自带精简运行时，不需要目标机安装 Dart。适合命令行工具与服务端部署。",
        },
        {
            "label": "Flutter 应用",
            "file": "libapp.so / app.apk",
            "cmd": "$ flutter build apk --release",
            "code": r"""$ flutter build apk --release
$ unzip -l build/app/outputs/flutter-apk/app-release.apk | grep libapp
  lib/arm64-v8a/libapp.so
  lib/armeabi-v7a/libapp.so

; Flutter：Dart AOT → libapp.so
; 加上 Flutter engine（Skia/Impeller）
; 资源、字体、图标打进 APK/AAB""",
            "format": [
                ("产物", "libapp.so + 资源"),
                ("引擎", "Flutter Engine（Skia/Impeller）"),
                ("容器", "APK / AAB / IPA"),
                ("平台", "Android / iOS / 桌面 / Web"),
            ],
            "note": "Flutter 应用不是单个 Dart 二进制：Dart AOT 代码是 `libapp.so`，渲染与平台集成由 Flutter Engine 提供。",
        },
    ],
    "tools": [
        {"era": "2010s", "editor": "Dart Editor / IntelliJ", "compiler": "dart2js / dart", "build": "pub", "pkg": "pub.dev", "debug": "Observatory"},
        {"era": "2020s", "editor": "VS Code / Android Studio", "compiler": "dart compile / flutter", "build": "flutter build", "pkg": "pub.dev", "debug": "DevTools"},
    ],
    "hello": {
        "file": "hello.dart",
        "code": r"""void main() {
  print('Hello, world');
}""",
        "footprint": [
            {"stage": "源码", "size": "≈ 40 B", "w": 4},
            {"stage": "Kernel .dill", "size": "≈ 12 KB", "w": 18},
            {"stage": "AOT exe", "size": "≈ 5.2 MB", "w": 70},
            {"stage": "Flutter libapp", "size": "≈ 8 MB", "w": 80},
            {"stage": "+ Engine", "size": "≈ 20 MB", "w": 100},
        ],
        "why": [
            "<strong>Kernel</strong>：前端产出的二进制 AST，JIT 与 AOT 的共同入口。",
            "<strong>AOT</strong>：发布时编译成机器码，避免 JIT 的启动与预热。",
            "<strong>运行时</strong>：AOT 产物仍带裁剪后的 Dart runtime（GC、类型、异常）。",
            "<strong>Flutter</strong>：Dart 代码与引擎分离，`libapp.so` 只是应用层。",
        ],
    },
},

# ============================================================
"zig": {
    "tagline": "C 的克制替代品：comptime、无隐藏分配、交叉编译像本地编译。",
    "intro": [
        "Zig 由 Andrew Kelley 在 2016 年发布。它想成为 C 的替代品：没有隐式控制流、没有隐藏内存分配、没有预处理器；用 `comptime` 在编译期执行代码，用显式分配器管理内存。",
        "Zig 自带 LLVM 后端，也自带 C/C++ 编译器（`zig cc`）。`zig build-exe` 可以直接交叉编译到其他平台，不需要为目标平台安装工具链。",
        "它的产物链很短：源码 → LLVM IR（或自研后端）→ 目标文件 → 静态 ELF。标准库被编译进程序，默认不依赖 libc。",
    ],
    "lineage": {
        "from": ["C", "C++", "Rust（部分反思）", "LLVM"],
        "to": ["Bun 运行时", "嵌入式", "交叉编译工具链"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.zig",
            "cmd": "$ cat hello.zig",
            "code": r"""const std = @import("std");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    try stdout.print("Hello, world\n", .{});
}""",
            "format": [
                ("扩展名", ".zig"),
                ("comptime", "编译期执行代码"),
                ("错误", "!void 表示可能失败"),
                ("内存", "显式分配器"),
            ],
            "note": "Zig 没有隐式分配：需要内存的地方必须传入 allocator。`try` 把错误向上传播，而不是抛异常。",
        },
        {
            "label": "LLVM IR",
            "file": "hello.ll",
            "cmd": "$ zig build-exe hello.zig -femit-llvm-ir=hello.ll",
            "code": r"""define i32 @main() #0 {
Entry:
  ...
  call void @std.io.getStdOut...
  ...
  ret i32 0
}

; comptime 已在编译期求值
; 之后交给 LLVM 优化
; 也可以使用 Zig 自研后端""",
            "format": [
                ("中间表示", "LLVM IR"),
                ("comptime", "编译期求值完毕"),
                ("后端", "LLVM / 自研"),
                ("输出", "-femit-llvm-ir"),
            ],
            "note": "Zig 的 `comptime` 不是宏系统：它真的在编译期执行 Zig 代码，生成类型与常量。",
        },
        {
            "label": "目标文件",
            "file": "hello.o",
            "cmd": "$ zig build-obj hello.zig && file hello.o",
            "code": r"""$ zig build-obj hello.zig
$ file hello.o
hello.o: ELF 64-bit LSB relocatable, x86-64

$ nm hello.o | grep main
... T main

; 标准库代码已编译进目标文件
; 默认不依赖 libc
; 交叉编译：-target aarch64-linux-gnu""",
            "format": [
                ("格式", "ELF / COFF / Mach-O"),
                ("符号", "main"),
                ("libc", "默认不链接"),
                ("交叉编译", "-target"),
            ],
            "note": "Zig 默认把标准库与启动代码编译进目标文件，所以一个 hello 可以完全静态、无 libc。",
        },
        {
            "label": "可执行",
            "file": "hello",
            "cmd": "$ zig build-exe hello.zig && ./hello && ldd hello",
            "code": r"""$ ./hello
Hello, world

$ file hello
hello: ELF 64-bit LSB executable, x86-64, statically linked

$ ldd hello
        not a dynamic executable

$ ls -lh hello
-rwxr-xr-x 1 user user 1.1M ... hello

; 静态链接，无 libc（除非显式链接）
; 启动代码、std、panic 处理都在里面
; 可直接交叉编译到其他平台""",
            "format": [
                ("格式", "ELF / PE / Mach-O"),
                ("链接", "静态，默认无 libc"),
                ("运行时", "极小（panic、栈检查）"),
                ("交叉编译", "单命令完成"),
            ],
            "note": "Zig 的部署模型接近 Go：静态二进制、无外部依赖；但运行时更小，且不强制 GC。",
        },
    ],
    "tools": [
        {"era": "2010s", "editor": "VS Code", "compiler": "zig", "build": "zig build", "pkg": "zig fetch", "debug": "gdb / lldb"},
        {"era": "2020s", "editor": "VS Code + ZLS", "compiler": "zig", "build": "zig build", "pkg": "zig fetch", "debug": "gdb / lldb"},
    ],
    "hello": {
        "file": "hello.zig",
        "code": r"""const std = @import("std");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    try stdout.print("Hello, world\n", .{});
}""",
        "footprint": [
            {"stage": "源码", "size": "≈ 130 B", "w": 5},
            {"stage": "LLVM IR", "size": "≈ 2 KB", "w": 12},
            {"stage": "hello.o", "size": "≈ 8 KB", "w": 18},
            {"stage": "静态 ELF", "size": "≈ 1.1 MB", "w": 65},
            {"stage": "+ std", "size": "≈ 1.1 MB", "w": 65},
        ],
        "why": [
            "<strong>comptime</strong>：在编译期执行代码，替代宏与模板。",
            "<strong>显式分配</strong>：没有隐藏分配，内存行为可预测。",
            "<strong>自带工具链</strong>：`zig cc` 与交叉编译不依赖系统工具链。",
            "<strong>静态链接</strong>：默认无 libc，部署只需一个文件。",
        ],
    },
},

# ============================================================
"nim": {
    "tagline": "Python 式语法的系统语言：编译到 C，再交给 C 编译器。",
    "intro": [
        "Nim 由 Andreas Rumpf 在 2008 年发布。它想结合 Python 的可读性与 C 的性能：缩进语法、静态类型、泛型、宏与编译期执行。",
        "Nim 的主要后端是 C（也支持 C++ 与 JavaScript）。编译器把 Nim 源码翻译成 C，再调用系统 C 编译器生成目标文件。因此产物链中间会出现一层可读的 C 代码，这是它最鲜明的特征。",
        "Nim 有垃圾回收（可选 ARC/ORC 或 Boehm），也可以 `--mm:arc` / `--mm:none` 调整内存模型。部署时通常静态链接运行时，得到较小的原生二进制。",
    ],
    "lineage": {
        "from": ["Python（语法）", "Ada（类型）", "Lisp（宏）", "C"],
        "to": ["系统工具", "游戏脚本", "嵌入式"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.nim",
            "cmd": "$ cat hello.nim",
            "code": r"""echo "Hello, world"
# 输出：Hello, world""",
            "format": [
                ("扩展名", ".nim"),
                ("缩进", "Python 风格"),
                ("类型", "静态、推断"),
                ("编译期", "宏与 `when`"),
            ],
            "note": "`echo` 是标准库模板，不是关键字。Nim 的宏在编译期执行，可以生成任意代码。",
        },
        {
            "label": "生成的 C",
            "file": "@mhello.nim.c",
            "cmd": "$ nim c --nimcache:build hello.nim",
            "code": r"""/* Generated by Nim Compiler (示意) */
N_LIB_PRIVATE N_NIMCALL(void, NimMain)(void) {
    ...
    echoBinSafe(TM__abc, 1);
    ...
}

; Nim → C → 系统 C 编译器
; 名字修饰、运行时调用都在 C 里
; 可读性较差，但可调试""",
            "format": [
                ("中间产物", "生成的 C 代码"),
                ("位置", "nimcache / --nimcache"),
                ("后端", "C / C++ / JS"),
                ("编译", "gcc / clang / vcc"),
            ],
            "note": "Nim 没有自己的机器码后端（默认）：它生成 C，再让成熟的 C 编译器做优化与代码生成。",
        },
        {
            "label": "目标文件",
            "file": "hello.o",
            "cmd": "$ gcc -c build/@mhello.nim.c -o hello.o",
            "code": r"""$ file hello.o
hello.o: ELF 64-bit LSB relocatable, x86-64

$ nm hello.o | grep -E 'NimMain|echo'
... T NimMain
... T echoBinSafe

; 由 C 编译器生成
; 含 Nim 运行时（GC、字符串、异常）
; 可与其他 C 目标文件链接""",
            "format": [
                ("格式", "平台对象文件"),
                ("生成", "C 编译器"),
                ("运行时", "Nim runtime"),
                ("互操作", "可链接 C/C++"),
            ],
            "note": "因为中间是 C，Nim 可以很自然地调用 C 库，也可以被 C 项目链接。",
        },
        {
            "label": "可执行",
            "file": "hello",
            "cmd": "$ nim c -d:release hello.nim && ./hello",
            "code": r"""$ nim c -d:release hello.nim
$ ./hello
Hello, world

$ file hello
hello: ELF 64-bit LSB executable, x86-64 ...

$ ldd hello
  libc.so.6

; 默认静态链接 Nim 运行时
; 可选 --mm:arc / --mm:none / -d:useMalloc
; 体积：hello ≈ 100–300 KB""",
            "format": [
                ("格式", "ELF / PE / Mach-O"),
                ("运行时", "Nim runtime + GC"),
                ("内存", "ARC / ORC / refc / none"),
                ("体积", "较小，接近 C"),
            ],
            "note": "Nim 的运行时与 GC 策略是可选的。`--mm:none` 可以完全去掉 GC，接近 C 的模型。",
        },
    ],
    "tools": [
        {"era": "2010s", "editor": "VS Code / Nim IDE", "compiler": "nim", "build": "nimble", "pkg": "nimble", "debug": "gdb"},
        {"era": "2020s", "editor": "VS Code + nimlangserver", "compiler": "nim", "build": "nimble", "pkg": "nimble", "debug": "gdb / lldb"},
    ],
    "hello": {
        "file": "hello.nim",
        "code": r"""echo "Hello, world"
# 输出：Hello, world""",
        "footprint": [
            {"stage": "源码", "size": "≈ 22 B", "w": 4},
            {"stage": "生成的 C", "size": "≈ 200 KB", "w": 55},
            {"stage": "hello.o", "size": "≈ 40 KB", "w": 25},
            {"stage": "可执行", "size": "≈ 150 KB", "w": 40},
            {"stage": "+ libc", "size": "≈ 2 MB", "w": 80},
        ],
        "why": [
            "<strong>C 后端</strong>：复用成熟 C 编译器，兼容 C ABI 与库。",
            "<strong>宏</strong>：编译期代码生成，能构造 DSL 与优化。",
            "<strong>可选 GC</strong>：ARC/ORC/none，按场景选择内存模型。",
            "<strong>静态运行时</strong>：默认把 Nim 运行时链接进可执行文件。",
        ],
    },
},

# ============================================================
"crystal": {
    "tagline": "Ruby 的语法，C 的性能：全程序类型推断 + LLVM。",
    "intro": [
        "Crystal 由 Ary Borenzweig 在 2014 年发布，目标是「像 Ruby 一样好写，像 C 一样快」。它保留了 Ruby 的语法与对象模型，但在编译期做全程序类型推断，并直接生成 LLVM IR。",
        "Crystal 没有虚拟机：编译器把整个程序（包括标准库）一起分析、特化、生成机器码。因此编译较慢，但产物是原生可执行文件，启动快、运行时小。",
        "它使用 Boehm GC 管理内存，也可以在某些场景关闭。Crystal 的宏在编译期展开，语法上接近 Ruby 的元编程。",
    ],
    "lineage": {
        "from": ["Ruby（语法）", "C（性能目标）", "LLVM"],
        "to": ["原生 CLI 工具", "Web 服务（Kemal）", "系统脚本"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.cr",
            "cmd": "$ cat hello.cr",
            "code": r"""puts "Hello, world"
# 输出：Hello, world""",
            "format": [
                ("扩展名", ".cr"),
                ("语法", "Ruby 风格"),
                ("类型", "静态，全程序推断"),
                ("编译", "crystal build"),
            ],
            "note": "Crystal 的源码看起来像 Ruby，但类型在编译期确定；`puts` 是顶层方法。",
        },
        {
            "label": "LLVM IR",
            "file": "hello.ll",
            "cmd": "$ crystal build --emit llvm-ir hello.cr",
            "code": r"""define i32 @main(i32 %0, ptr %1) #0 {
entry:
  ...
  call void @puts(ptr @str)
  ret i32 0
}

; 全程序类型推断完成
; 泛型/方法已特化
; 交给 LLVM 优化""",
            "format": [
                ("中间表示", "LLVM IR"),
                ("推断", "全程序、单态化"),
                ("输出", "--emit llvm-ir"),
                ("后端", "LLVM"),
            ],
            "note": "Crystal 没有字节码：类型推断后直接生成 LLVM IR，再编译成机器码。",
        },
        {
            "label": "目标文件",
            "file": "hello.o",
            "cmd": "$ crystal build --emit obj hello.cr",
            "code": r"""$ file hello.o
hello.o: ELF 64-bit LSB relocatable, x86-64

$ nm hello.o | grep -E 'main|puts'
... T main
... U puts
... U GC_malloc

; 依赖 libgc（Boehm GC）
; 标准库已编译进目标文件
; 可执行由链接器生成""",
            "format": [
                ("格式", "ELF / Mach-O / COFF"),
                ("GC", "Boehm（libgc）"),
                ("标准库", "静态编译"),
                ("链接", "系统链接器"),
            ],
            "note": "Crystal 的运行时依赖包括 libgc、libevent、libpcre 等；部署时通常静态或随包提供。",
        },
        {
            "label": "可执行",
            "file": "hello",
            "cmd": "$ crystal build hello.cr -o hello && ./hello",
            "code": r"""$ ./hello
Hello, world

$ file hello
hello: ELF 64-bit LSB pie executable, x86-64 ...

$ ldd hello
  libgc.so.1
  libevent-2.1.so.7
  libc.so.6

; 原生代码，无 VM
; 启动快，运行时小
; 编译时间较长（全程序分析）""",
            "format": [
                ("格式", "原生可执行"),
                ("运行时", "Boehm GC + libevent"),
                ("启动", "无 VM，直接执行"),
                ("代价", "编译慢、产物依赖库"),
            ],
            "note": "Crystal 的取舍很明确：用编译时间换运行时性能与开发体验。",
        },
    ],
    "tools": [
        {"era": "2010s", "editor": "VS Code / Atom", "compiler": "crystal", "build": "shards", "pkg": "shards", "debug": "gdb / lldb"},
        {"era": "2020s", "editor": "VS Code + Crystal", "compiler": "crystal", "build": "shards", "pkg": "shards", "debug": "gdb / lldb"},
    ],
    "hello": {
        "file": "hello.cr",
        "code": r"""puts "Hello, world"
# 输出：Hello, world""",
        "footprint": [
            {"stage": "源码", "size": "≈ 22 B", "w": 4},
            {"stage": "LLVM IR", "size": "≈ 1 KB", "w": 12},
            {"stage": "hello.o", "size": "≈ 8 KB", "w": 18},
            {"stage": "可执行", "size": "≈ 400 KB", "w": 45},
            {"stage": "+ libgc", "size": "≈ 1 MB", "w": 60},
        ],
        "why": [
            "<strong>全程序推断</strong>：没有运行时类型检查，泛型在编译期特化。",
            "<strong>LLVM</strong>：直接生成 IR，复用成熟优化器与后端。",
            "<strong>无 VM</strong>：启动快，运行时行为可预测。",
            "<strong>Boehm GC</strong>：自动内存管理，但保留了原生代码的执行模型。",
        ],
    },
},

# ============================================================
"elm": {
    "tagline": "前端的类型化架构：没有运行时异常，编译器替你抓错。",
    "intro": [
        "Elm 由 Evan Czaplicki 在 2012 年发布，是一门编译到 JavaScript 的函数式前端语言。它的卖点是「没有运行时异常」：类型错误、空值、副作用都在编译期处理。",
        "Elm 的架构（Model–View–Update）影响了 Redux。它不暴露中间表示：编译器把源码检查、优化后直接生成 JavaScript；再进一步可以生成一个自带运行时的 HTML 文件。",
        "Elm 的产物链很短：`.elm → JavaScript → 优化后的 JS/HTML`。没有字节码，也没有运行时类型检查。",
    ],
    "lineage": {
        "from": ["Haskell", "ML", "OCaml", "React/Redux（反向影响）"],
        "to": ["Redux 架构", "类型化前端", "Elm 生态"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "Hello.elm",
            "cmd": "$ cat Hello.elm",
            "code": r"""module Hello exposing (main)

import Html exposing (text)

main =
    text "Hello, world"
-- 输出：Hello, world""",
            "format": [
                ("扩展名", ".elm"),
                ("模块", "module … exposing"),
                ("不可变", "所有值不可变"),
                ("副作用", "通过 Cmd/Sub 描述"),
            ],
            "note": "Elm 的 `main` 是一个 HTML 值，不是一组 DOM 操作。渲染由运行时根据值完成。",
        },
        {
            "label": "类型检查",
            "file": "compiler",
            "cmd": "$ elm make Hello.elm --output=hello.js",
            "code": r"""$ elm make Hello.elm --output=hello.js
Success! Compiled 1 module.

; 编译期检查：
;   - 类型推断与统一
;   - 穷尽性（case 必须覆盖所有构造器）
;   - 无 null / 无异常
; 通过后才生成 JS""",
            "format": [
                ("检查", "类型推断 + 穷尽性"),
                ("保证", "无 null / 无运行时异常"),
                ("输出", "JavaScript"),
                ("中间表示", "不对外暴露"),
            ],
            "note": "Elm 不提供公开的 IR 或字节码。编译器内部做完检查与优化后，直接输出 JS。",
        },
        {
            "label": "生成的 JavaScript",
            "file": "hello.js",
            "cmd": "$ head -20 hello.js",
            "code": r"""(function(scope){
'use strict';

function F(arity, fun, wrapper) { ... }
function _Platform_export(exports) { ... }

var author$project$Hello$main =
    $elm$html$Html$text('Hello, world');

_Platform_export({'Hello':{'init':...}});
}(this));

; 运行时被内联进输出
; 模块名被编码成变量名
; 没有类型信息""",
            "format": [
                ("输出", "JavaScript"),
                ("运行时", "Elm runtime 内联"),
                ("模块", "编码成变量名"),
                ("类型", "已擦除"),
            ],
            "note": "Elm 的 JS 输出包含一个小型运行时（虚拟 DOM、调度、平台适配），不是裸函数。",
        },
        {
            "label": "优化与部署",
            "file": "main.js / index.html",
            "cmd": "$ elm make Hello.elm --optimize --output=main.js",
            "code": r"""$ elm make Hello.elm --optimize --output=main.js
$ ls -lh main.js
-rw-r--r-- 1 user user 28K ... main.js

$ elm make Hello.elm --output=index.html
$ ls
index.html  ; 自带运行时的单文件页面

; --optimize：死代码消除、压缩
; 输出可直接放进静态站点
; 无需 Node，无需构建服务器""",
            "format": [
                ("优化", "--optimize"),
                ("产物", "JS / 单文件 HTML"),
                ("部署", "静态文件"),
                ("体积", "hello ≈ 20–30 KB"),
            ],
            "note": "Elm 的部署极其简单：一个 JS 或一个 HTML 文件。代价是必须接受它的架构与生态。",
        },
    ],
    "tools": [
        {"era": "2010s", "editor": "Atom / VS Code", "compiler": "elm make", "build": "elm make", "pkg": "elm install", "debug": "Elm 调试器"},
        {"era": "2020s", "editor": "VS Code + Elm", "compiler": "elm make", "build": "elm make", "pkg": "elm install", "debug": "Elm 调试器"},
    ],
    "hello": {
        "file": "Hello.elm",
        "code": r"""module Hello exposing (main)
import Html exposing (text)
main = text "Hello, world"
-- 输出：Hello, world""",
        "footprint": [
            {"stage": "源码", "size": "≈ 80 B", "w": 4},
            {"stage": "检查", "size": "—", "w": 6},
            {"stage": "hello.js", "size": "≈ 30 KB", "w": 55},
            {"stage": "main.js", "size": "≈ 28 KB", "w": 52},
            {"stage": "index.html", "size": "≈ 30 KB", "w": 56},
        ],
        "why": [
            "<strong>类型检查</strong>：编译期消灭空值与未覆盖分支。",
            "<strong>无 IR</strong>：编译器不暴露中间表示，直接产 JS。",
            "<strong>内联运行时</strong>：输出自带虚拟 DOM 与平台适配。",
            "<strong>单文件部署</strong>：静态 HTML/JS，无需服务端。",
        ],
    },
},

# ============================================================
"solidity": {
    "tagline": "写给以太坊虚拟机的语言：合约、ABI 与不可更改的字节码。",
    "intro": [
        "Solidity 由 Gavin Wood、Christian Reitwiessner 等人在 2014 年设计，运行在以太坊虚拟机（EVM）上。它的语法接近 JavaScript，但语义围绕账户、存储、gas 与消息调用。",
        "Solidity 的产物不是普通可执行文件，而是 EVM 字节码 + ABI JSON。部署时把「部署字节码」发给链，链上保存的是「运行时字节码」；ABI 描述如何编码函数调用与返回值。",
        "编译器中间会经过 Yul（一种低级 IR）与优化器。理解 Yul 与字节码，才能理解 gas 成本、存储布局与合约升级的限制。",
    ],
    "lineage": {
        "from": ["JavaScript（语法）", "EVM", "Vyper（竞争）", "Yul"],
        "to": ["DeFi / NFT 生态", "Layer 2", "形式化验证工具"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "Hello.sol",
            "cmd": "$ cat Hello.sol",
            "code": r"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Hello {
    function greet() public pure returns (string memory) {
        return "Hello, world";
    }
}""",
            "format": [
                ("扩展名", ".sol"),
                ("合约", "contract + 函数"),
                ("可见性", "public / pure"),
                ("存储", "storage / memory / calldata"),
            ],
            "note": "`pure` 表示函数不读也不写链上状态；`returns (string memory)` 表示返回值放在内存。",
        },
        {
            "label": "AST",
            "file": "Hello.ast.json",
            "cmd": "$ solc --ast-compact-json Hello.sol",
            "code": r"""{
  "nodeType": "ContractDefinition",
  "name": "Hello",
  "nodes": [
    {
      "nodeType": "FunctionDefinition",
      "name": "greet",
      "stateMutability": "pure",
      "returnParameters": { ... }
    }
  ]
}

; 编译器前端暴露完整 AST
; 工具链（slither / 形式化验证）在这一层工作""",
            "format": [
                ("格式", "JSON AST"),
                ("节点", "ContractDefinition / FunctionDefinition"),
                ("用途", "静态分析、审计、代码生成"),
                ("查看", "--ast-compact-json"),
            ],
            "note": "Solidity 的 AST 是公开 JSON，安全审计工具（Slither 等）大量依赖它。",
        },
        {
            "label": "Yul IR",
            "file": "Hello.yul",
            "cmd": "$ solc --ir Hello.sol",
            "code": r"""object "Hello" {
  code {
    datacopy(0, dataoffset("runtime"), datasize("runtime"))
    return(0, datasize("runtime"))
  }
  object "runtime" {
    code {
      mstore(0x00, 0x20)
      mstore(0x20, 0x0c)
      mstore(0x40, 0x48656c6c6f2c20776f726c6400000000000000000000000000000000)
      return(0x00, 0x60)
    }
  }
}

; Yul = 低级 IR（可读汇编）
; 部署代码与运行时对象分开
; 优化器在 Yul 上工作""",
            "format": [
                ("中间表示", "Yul"),
                ("对象", "部署代码 + runtime 对象"),
                ("优化", "Yul 优化器"),
                ("查看", "--ir"),
            ],
            "note": "Yul 是 EVM 的可读汇编：它暴露栈、内存、存储与 ABI 编码，是理解 gas 的关键层。",
        },
        {
            "label": "字节码与 ABI",
            "file": "Hello.bin / Hello.abi",
            "cmd": "$ solc --bin --abi Hello.sol",
            "code": r"""$ solc --bin --abi Hello.sol
======= Hello.sol:Hello =======
Binary:
6080604052348015600f57600080fd5b506...

Contract JSON ABI:
[{"inputs":[],"name":"greet","outputs":
  [{"internalType":"string","name":"","type":"string"}],
  "stateMutability":"pure","type":"function"}]

; Binary = 部署字节码（creation code）
; 其中包含 runtime 字节码
; ABI = 调用编码说明，不是代码""",
            "format": [
                ("字节码", "EVM 十六进制"),
                ("部署码", "creation code + runtime"),
                ("ABI", "JSON，描述函数与事件"),
                ("执行", "EVM 栈式虚拟机"),
            ],
            "note": "部署到链上后，真正长期保存的是 runtime 字节码；creation code 只在部署时执行一次。ABI 帮助外部程序编码调用。",
        },
    ],
    "tools": [
        {"era": "2010s", "editor": "Remix / VS Code", "compiler": "solc", "build": "Truffle / Hardhat", "pkg": "npm", "debug": "Remix / Tenderly"},
        {"era": "2020s", "editor": "VS Code + Solidity", "compiler": "solc / foundry", "build": "Foundry / Hardhat", "pkg": "npm / forge", "debug": "Foundry / Tenderly"},
    ],
    "hello": {
        "file": "Hello.sol",
        "code": r"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
contract Hello {
    function greet() public pure returns (string memory) {
        return "Hello, world";
    }
}""",
        "footprint": [
            {"stage": "源码", "size": "≈ 150 B", "w": 5},
            {"stage": "AST", "size": "≈ 2 KB", "w": 14},
            {"stage": "Yul", "size": "≈ 1 KB", "w": 10},
            {"stage": "字节码", "size": "≈ 300 B", "w": 7},
            {"stage": "部署交易", "size": "≈ 500 B", "w": 9},
        ],
        "why": [
            "<strong>EVM 字节码</strong>：不是本机代码，由链上虚拟机执行。",
            "<strong>Yul</strong>：可读的低级 IR，暴露栈、内存与 ABI 编码。",
            "<strong>creation/runtime</strong>：部署码只执行一次，runtime 永久保存在链上。",
            "<strong>ABI</strong>：外部调用者按 ABI 编码参数，字节码本身不描述接口。",
        ],
    },
},

}

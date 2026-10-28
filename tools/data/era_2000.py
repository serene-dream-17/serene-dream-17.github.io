# -*- coding: utf-8 -*-
"""第三批 · 2000s：8 门语言的档案与产物链数据。"""

LANGS = {

# ============================================================
"csharp": {
    "tagline": "Anders Hejlsberg 在 .NET 上的答案：CIL、值类型、LINQ 与 async。",
    "intro": [
        "C# 由 Anders Hejlsberg 主导，2000 年随 .NET 平台发布。它借了 C++ 的语法与 Java 的托管运行时，但补上了值类型、属性、委托、LINQ、async/await 等特性。",
        "C# 的产物链是 CLR 的：源码先编译成 CIL（Common Intermediate Language），装进 PE 格式的程序集（.dll/.exe），附带元数据表。运行时由 CLR 加载、JIT 编译；也可以预编译成 R2R 或 NativeAOT 原生程序。",
        "程序集不是普通的 PE：它在 PE 头里嵌了一个 CLR 头，指向元数据（BSJB 签名）与 IL 代码。理解这一层，就能理解 .NET 的反射、泛型与跨语言互操作。",
    ],
    "lineage": {
        "from": ["C++", "Java", "Delphi（Anders 的前作）"],
        "to": ["F#", "Kotlin（部分）", "Unity 生态"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "Hello.cs",
            "cmd": "$ cat Hello.cs",
            "code": r"""using System;

class Hello {
    static void Main() {
        Console.WriteLine("Hello, world");
    }
}""",
            "format": [
                ("扩展名", ".cs"),
                ("编译", "csc / dotnet build"),
                ("入口", "static Main"),
                ("目标", "CIL + 元数据"),
            ],
            "note": "C# 源码最终不会变成机器码，而是变成 CIL。JIT 在运行时才把 CIL 编译成本机指令。",
        },
        {
            "label": "CIL",
            "file": "Hello.il",
            "cmd": "$ ildasm Hello.dll /out:Hello.il",
            "code": r""".method private hidebysig static void Main() cil managed
{
  .entrypoint
  .maxstack 8
  IL_0000: ldstr "Hello, world"
  IL_0005: call void [System.Console]System.Console::WriteLine(string)
  IL_000a: ret
}

; CIL 是栈式中间语言
; ldstr 把字符串压栈，call 调用 Console.WriteLine
; 方法体带签名与异常表""",
            "format": [
                ("形态", "栈式中间语言"),
                ("指令", "ldstr / call / ret"),
                ("元数据", "类型、方法、字段、引用"),
                ("验证", "CLR 在 JIT 前做类型安全验证"),
            ],
            "note": "CIL 是 .NET 多语言的共同目标：C#、F#、VB 都编译到它，因此可以互相调用。",
        },
        {
            "label": "程序集",
            "file": "Hello.dll",
            "cmd": "$ file Hello.dll && xxd -l 128 Hello.dll",
            "code": r"""$ file Hello.dll
Hello.dll: PE32 executable (console) Intel 80386 Mono/.Net assembly

$ xxd -l 96 Hello.dll
00000000: 4d5a 9000 0300 0000 0400 0000 ffff 0000  MZ..............
...
00000080: 5045 0000 4c01 ...                    PE..L...

; PE 头之后是 CLR 头：
;   cb / MajorRuntimeVersion / MetaData RVA
; 元数据签名：42 53 4a 42 = "BSJB"
; 表：#~（压缩表）/ #Strings / #US / #GUID / #Blob""",
            "format": [
                ("容器", "PE32 / PE32+"),
                ("CLR 头", "指向元数据与 IL"),
                ("元数据签名", "BSJB"),
                ("元数据表", "#~ / #Strings / #US / #GUID / #Blob"),
            ],
            "note": "程序集 = PE 容器 + CIL + 元数据 + 清单。反射之所以能工作，是因为元数据表完整描述了类型与成员。",
        },
        {
            "label": "运行 / AOT",
            "file": "Hello.dll → hello",
            "cmd": "$ dotnet Hello.dll  /  dotnet publish -p:PublishAot=true",
            "code": r"""$ dotnet Hello.dll
Hello, world

; 默认：CLR 加载 → JIT 编译 Main → 执行
; 可选：ReadyToRun（R2R）预编译
$ dotnet publish -c Release -r linux-x64 -p:PublishAot=true
$ file bin/Release/net8.0/linux-x64/publish/Hello
Hello: ELF 64-bit LSB pie executable, x86-64 ...

; NativeAOT：CIL 在发布时编译成本机代码
; 运行时仍然存在（GC、异常、反射子集）""",
            "format": [
                ("默认", "CLR + JIT"),
                ("R2R", "程序集内预编译本机代码"),
                ("NativeAOT", "发布时生成原生 ELF"),
                ("运行时", "GC、异常、元数据"),
            ],
            "note": "NativeAOT 让 .NET 程序脱离 CLR 启动，代价是反射与动态加载受限。这是一条从托管到原生的连续光谱。",
        },
    ],
    "tools": [
        {"era": "2000s", "editor": "Visual Studio .NET", "compiler": "csc", "build": "MSBuild", "pkg": "NuGet（后）", "debug": "VS 调试器"},
        {"era": "2010s", "editor": "Visual Studio / VS Code", "compiler": "Roslyn", "build": "MSBuild / dotnet CLI", "pkg": "NuGet", "debug": "VS / vsdbg"},
        {"era": "2020s", "editor": "VS Code + C# Dev Kit", "compiler": "Roslyn", "build": "dotnet CLI", "pkg": "NuGet", "debug": "vsdbg"},
    ],
    "hello": {
        "file": "Hello.cs",
        "code": r"""using System;

class Hello {
    static void Main() => Console.WriteLine("Hello, world");
}""",
        "footprint": [
            {"stage": "源码", "size": "≈ 90 B", "w": 4},
            {"stage": "CIL", "size": "≈ 200 B", "w": 8},
            {"stage": "Hello.dll", "size": "≈ 4 KB", "w": 14},
            {"stage": "NativeAOT", "size": "≈ 1.7 MB", "w": 70},
            {"stage": "+ CLR", "size": "≈ 70 MB", "w": 100},
        ],
        "why": [
            "<strong>CIL</strong>：多语言共享的栈式中间语言，JIT 的输入。",
            "<strong>元数据</strong>：类型与成员的结构化描述，支撑反射与跨语言调用。",
            "<strong>程序集</strong>：部署与版本的单位，PE 只是外壳。",
            "<strong>NativeAOT</strong>：在发布时把 CIL 编译成本机码，换取启动速度与独立部署。",
        ],
    },
},

# ============================================================
"scala": {
    "tagline": "JVM 上的函数式与面向对象：类型系统很强，语法很克制。",
    "intro": [
        "Scala 由 Martin Odersky 在 EPFL 设计，2004 年发布。它把函数式编程（不可变数据、模式匹配、高阶函数）与面向对象（类、trait、子类型）放在同一门语言里，运行在 JVM 上。",
        "Scala 的编译器 scalac 会做大量类型检查与去糖，最终生成 JVM 字节码。一个 `object Hello` 会变成 `Hello$.class` 与 `Hello.class` 两个类；伴生对象、闭包、模式匹配都会展开成 JVM 能理解的形态。",
        "Scala 3 重新设计了类型系统与语法（enum、given、extension），但产物仍然是 `.class`。Spark 与大数据生态让 Scala 在 2010 年代获得了大量用户。",
    ],
    "lineage": {
        "from": ["Java", "ML", "Haskell", "Pizza"],
        "to": ["Kotlin（部分）", "Spark 生态", "ZIO / Cats 生态"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "Hello.scala",
            "cmd": "$ cat Hello.scala",
            "code": r"""object Hello extends App {
  println("Hello, world")
}""",
            "format": [
                ("扩展名", ".scala / .sc"),
                ("object", "单例对象，编译成两个类"),
                ("App", "提供 main 的 trait"),
                ("类型", "静态、推断、代数数据类型"),
            ],
            "note": "`object` 是 Scala 的单例。它会被编译成 `Hello$`（实例）与 `Hello`（静态转发）两个 JVM 类。",
        },
        {
            "label": "去糖 / 擦除",
            "file": "typer",
            "cmd": "$ scalac -Xprint:erasure Hello.scala",
            "code": r"""package <empty> {
  object Hello extends Object with App {
    def <init>(): Hello.type = {
      Hello.super.<init>();
      ()
    };
    ...
    def main(args: Array[String]): Unit = Hello.this.println("Hello, world")
  }
}

; 类型参数被擦除
; for / 模式匹配 / 闭包 已展开
; 伴生对象已拆成两个类""",
            "format": [
                ("阶段", "typer → erasure"),
                ("擦除", "泛型类型参数被移除"),
                ("去糖", "for / match / 闭包展开"),
                ("输出", "更接近 JVM 的核心语言"),
            ],
            "note": "JVM 的泛型是类型擦除的，Scala 必须在编译期把类型信息擦掉，再通过签名与反射补偿。",
        },
        {
            "label": "字节码",
            "file": "Hello$.class",
            "cmd": "$ scalac Hello.scala && javap -c Hello$",
            "code": r"""$ ls Hello*.class
Hello$.class  Hello.class

$ javap -c Hello$
public final class Hello$ {
  public static final Hello$ MODULE$;
  public void main(java.lang.String[]);
    Code:
       0: getstatic     #...  // Field MODULE$
       3: ldc           #...  // String Hello, world
       5: invokevirtual #...  // Method println
       8: return
}""",
            "format": [
                ("产物", ".class（JVM 字节码）"),
                ("伴生", "Hello$ + Hello"),
                ("签名", "ScalaSignature 注解携带类型信息"),
                ("互操作", "可从 Java 调用"),
            ],
            "note": "Scala 的 `.class` 与 Java 的完全同构；额外信息放在 `ScalaSignature` 注解里，供 Scala 编译器读取。",
        },
        {
            "label": "JAR",
            "file": "hello.jar",
            "cmd": "$ scala-cli package . --assembly -o hello.jar",
            "code": r"""$ java -jar hello.jar
Hello, world

$ unzip -l hello.jar | head
  META-INF/MANIFEST.MF
  Hello$.class
  Hello.class
  scala/...
  scala-library.jar（assembly 时展开）

; 普通 jar 依赖外部 scala-library
; assembly / uberjar 把标准库打进来""",
            "format": [
                ("容器", "JAR（zip）"),
                ("依赖", "scala-library"),
                ("assembly", "把依赖展开进同一个 jar"),
                ("运行", "java -jar / scala"),
            ],
            "note": "Scala 的部署单位仍然是 JVM 的 jar。区别只在依赖：标准库与运行时库需要一起带上。",
        },
    ],
    "tools": [
        {"era": "2000s", "editor": "Eclipse / IDEA", "compiler": "scalac", "build": "Ant / Maven", "pkg": "Maven Central", "debug": "JDB / IDE"},
        {"era": "2010s", "editor": "IntelliJ IDEA", "compiler": "scalac", "build": "sbt", "pkg": "Maven Central", "debug": "IDE 调试器"},
        {"era": "2020s", "editor": "VS Code + Metals", "compiler": "dotty / scalac", "build": "sbt / mill / scala-cli", "pkg": "Maven Central", "debug": "Metals / IDEA"},
    ],
    "hello": {
        "file": "Hello.scala",
        "code": r"""object Hello extends App {
  println("Hello, world")
}""",
        "footprint": [
            {"stage": "源码", "size": "≈ 55 B", "w": 4},
            {"stage": "去糖", "size": "≈ 300 B", "w": 10},
            {"stage": ".class", "size": "≈ 1.2 KB", "w": 16},
            {"stage": "jar", "size": "≈ 2 KB", "w": 18},
            {"stage": "+ scala-library", "size": "≈ 6 MB", "w": 90},
        ],
        "why": [
            "<strong>擦除</strong>：JVM 泛型不保留类型参数，Scala 在编译期擦除并补签名。",
            "<strong>伴生对象</strong>：object 编译成两个类，静态与实例入口分开。",
            "<strong>trait</strong>：默认实现与线性化在编译期展开成方法。",
            "<strong>jar</strong>：复用 JVM 生态的部署格式，依赖单独管理。",
        ],
    },
},

# ============================================================
"fsharp": {
    "tagline": "ML 的血统跑在 .NET 上：类型推断、不可变数据、管道与异步。",
    "intro": [
        "F# 由 Don Syme 在 Microsoft Research 主导，2005 年发布。它把 ML 的函数式核心（类型推断、模式匹配、代数数据类型）带到 .NET，同时保留与 C#、VB 的互操作。",
        "F# 编译到 CIL，但生成的 IL 比 C# 复杂：闭包变成类，模式匹配变成分支与类型测试，`printfn` 走 FSharp.Core 的格式化类型。程序集里因此会引用 FSharp.Core。",
        "它的特色还包括度量单位、类型提供器、计算表达式与异步工作流。Fable 还能把 F# 编译成 JavaScript，形成另一条后端。",
    ],
    "lineage": {
        "from": ["ML", "OCaml", "Haskell（部分）", ".NET"],
        "to": ["Fable（JS）", "Azure 工具链", "金融量化"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "Hello.fs",
            "cmd": "$ cat Hello.fs",
            "code": r"""[<EntryPoint>]
let main _ =
    printfn "Hello, world"
    0""",
            "format": [
                ("扩展名", ".fs / .fsx"),
                ("入口", "[<EntryPoint>] 标记"),
                ("缩进", "空白敏感"),
                ("类型", "推断，默认不可变"),
            ],
            "note": "F# 的 `main` 必须返回 int（退出码）。`printfn` 不是简单函数，而是一个带格式串的类型提供机制。",
        },
        {
            "label": "CIL",
            "file": "Hello.il",
            "cmd": "$ ildasm Hello.dll /out:Hello.il",
            "code": r""".method public static int32 main(string[] argv) cil managed
{
  .entrypoint
  .maxstack 8
  IL_0000: ldstr "Hello, world"
  IL_0005: call void [FSharp.Core]Microsoft.FSharp.Core.Printf::
             printfn@11<string>(class ...)
  IL_000a: ldc.i4.0
  IL_000b: ret
}

; 模式匹配、闭包、管道在 IL 里展开
; FSharp.Core 提供 printfn / 列表 / 异步""",
            "format": [
                ("目标", "CIL"),
                ("格式化", "printfn 走 FSharp.Core 的类型化格式"),
                ("闭包", "编译成类"),
                ("依赖", "FSharp.Core"),
            ],
            "note": "F# 的 `printfn` 在编译期被解析成泛型调用，格式串错误能在编译期发现，而不是运行时。",
        },
        {
            "label": "程序集",
            "file": "Hello.dll",
            "cmd": "$ dotnet build && file bin/Debug/net8.0/Hello.dll",
            "code": r"""$ file bin/Debug/net8.0/Hello.dll
Hello.dll: PE32 executable (console) Intel 80386 Mono/.Net assembly

$ monodis --assemblyref Hello.dll
AssemblyRef Table
1: FSharp.Core
2: System.Runtime
3: System.Console

; 程序集 = PE + CIL + 元数据
; F# 特有信息放在 FSharpSignature / FSharpOptimization 资源里""",
            "format": [
                ("容器", "PE 程序集"),
                ("引用", "FSharp.Core / System.Runtime"),
                ("资源", "F# 签名与优化信息"),
                ("运行", "dotnet Hello.dll"),
            ],
            "note": "F# 程序集里额外嵌入了签名资源，供 F# 编译器做跨程序集的类型检查与优化。",
        },
        {
            "label": "另一后端：Fable",
            "file": "Hello.js",
            "cmd": "$ dotnet fable . --outDir out",
            "code": r"""$ dotnet fable . --outDir out
$ cat out/Hello.js
export function main(argv) {
  console.log("Hello, world");
  return 0;
}

; Fable：F# → JavaScript
; 类型被擦除，函数式结构映射到 JS
; 用于前端 / Node.js""",
            "format": [
                ("后端", "Fable"),
                ("目标", "JavaScript"),
                ("用途", "前端 / Node.js"),
                ("代价", "运行时语义与 .NET 不完全相同"),
            ],
            "note": "F# 不只属于 .NET：Fable 把它编译成 JS，说明语言的核心可以脱离 CLR 存在。",
        },
    ],
    "tools": [
        {"era": "2000s", "editor": "Visual Studio", "compiler": "fsc", "build": "MSBuild", "pkg": "NuGet", "debug": "VS 调试器"},
        {"era": "2010s", "editor": "VS Code + Ionide", "compiler": "fsc", "build": "FAKE / dotnet", "pkg": "NuGet", "debug": "Ionide"},
        {"era": "2020s", "editor": "VS Code + Ionide / Rider", "compiler": "fsc", "build": "dotnet / FAKE", "pkg": "NuGet", "debug": "Ionide / Rider"},
    ],
    "hello": {
        "file": "Hello.fs",
        "code": r"""printfn "Hello, world"
// 输出：Hello, world""",
        "footprint": [
            {"stage": "源码", "size": "≈ 26 B", "w": 4},
            {"stage": "CIL", "size": "≈ 180 B", "w": 8},
            {"stage": "Hello.dll", "size": "≈ 4.5 KB", "w": 15},
            {"stage": "Fable JS", "size": "≈ 120 B", "w": 6},
            {"stage": "+ FSharp.Core", "size": "≈ 1.5 MB", "w": 70},
        ],
        "why": [
            "<strong>EntryPoint</strong>：F# 用特性标记入口，main 返回退出码。",
            "<strong>printfn</strong>：格式串在编译期解析成类型化调用。",
            "<strong>FSharp.Core</strong>：列表、选项、异步、格式化都在这个运行时库里。",
            "<strong>Fable</strong>：同一门语言可以编译到 JS，产物完全换一套。",
        ],
    },
},

# ============================================================
"clojure": {
    "tagline": "JVM 上的 Lisp：不可变数据、STM、REPL 驱动开发。",
    "intro": [
        "Clojure 由 Rich Hickey 在 2007 年发布。它把 Lisp 的宏与代码即数据带到 JVM，同时强调不可变数据与函数式编程；并发用 STM、agent 与 core.async。",
        "Clojure 默认在运行时把表单编译成 JVM 字节码，不生成中间文件；需要 AOT 时用 `:gen-class` 与 `compile` 提前生成 `.class`。分发通常是 uberjar：把 Clojure 运行时、依赖与你自己的类打成一个 jar。",
        "它的 REPL 文化很强：编辑器连接运行中的 JVM，边写边求值。产物链因此常常是「源码 → 内存中的字节码 → jar」，而不是一条离线编译流水线。",
    ],
    "lineage": {
        "from": ["Lisp", "Scheme", "Java", "ML（部分）"],
        "to": ["ClojureScript", "Datomic", "Babashka"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.clj",
            "cmd": "$ cat hello.clj",
            "code": r"""(ns hello
  (:gen-class))

(defn -main [& args]
  (println "Hello, world"))""",
            "format": [
                ("扩展名", ".clj / .cljs / .cljc"),
                ("ns", "命名空间 + gen-class"),
                ("函数", "defn，参数用向量"),
                ("数据", "列表 / 向量 / map / set"),
            ],
            "note": "`:gen-class` 让 Clojure 生成一个带 main 的 Java 类，才能用 `java -cp` 启动。",
        },
        {
            "label": "读取器表单",
            "file": "forms",
            "cmd": "user=> (read-string \"(println \\\"Hello, world\\\")\")",
            "code": r"""user=> (read-string "(println \"Hello, world\")")
(println "Hello, world")

user=> (class *1)
clojure.lang.PersistentList

; 源码先被读取成数据结构
; 宏在编译期对这些结构做变换
; 之后才生成字节码""",
            "format": [
                ("读取", "reader 把文本变成 list/vector/map"),
                ("宏", "编译期对表单做变换"),
                ("求值", "编译成 JVM 字节码后执行"),
                ("代码即数据", "可生成、拼接、序列化"),
            ],
            "note": "Clojure 的「语法树」就是 Lisp 的数据结构。宏不是文本替换，而是接收这些结构并返回新结构。",
        },
        {
            "label": "AOT 字节码",
            "file": "hello__init.class",
            "cmd": "$ clojure -M -e \"(compile 'hello)\"",
            "code": r"""$ clojure -M -e "(compile 'hello)"
$ ls classes/hello
hello__init.class
hello$fn__123.class
hello$main.class

$ javap -c classes/hello/hello__init
public class hello.hello__init {
  public static void load() { ... }
  ...
}

; 默认：运行时编译，不落盘
; AOT：compile 生成 .class
; 类名带命名空间与哈希""",
            "format": [
                ("默认", "运行时编译为字节码"),
                ("AOT", "compile 生成 .class"),
                ("类名", "命名空间 + 函数名 + 哈希"),
                ("JVM", "与 Java 类完全同构"),
            ],
            "note": "Clojure 没有自己的字节码格式：它就是 JVM 字节码。AOT 只是把运行时要做的事提前到构建阶段。",
        },
        {
            "label": "Uberjar",
            "file": "hello-standalone.jar",
            "cmd": "$ lein uberjar && java -jar target/uberjar/hello-standalone.jar",
            "code": r"""$ java -jar target/uberjar/hello-standalone.jar
Hello, world

$ unzip -l target/uberjar/hello-standalone.jar | head
  META-INF/MANIFEST.MF
  clojure/core.class
  clojure/core$...class
  hello/hello__init.class
  hello/hello$main.class

; uberjar = 你的代码 + Clojure + 依赖
; 启动 JVM，加载 hello 命名空间，调用 -main""",
            "format": [
                ("容器", "JAR"),
                ("内容", "代码 + Clojure 运行时 + 依赖"),
                ("入口", "Main-Class / -main"),
                ("启动", "JVM 加载命名空间"),
            ],
            "note": "uberjar 的启动仍然需要 JVM 与 Clojure 运行时；Babashka 与 GraalVM native-image 是后来的另一条路。",
        },
    ],
    "tools": [
        {"era": "2000s", "editor": "Emacs + SLIME", "compiler": "Clojure 编译器（JVM）", "build": "Ant / Leiningen", "pkg": "Clojars", "debug": "REPL"},
        {"era": "2010s", "editor": "Emacs + CIDER", "compiler": "Clojure", "build": "Leiningen", "pkg": "Clojars", "debug": "CIDER"},
        {"era": "2020s", "editor": "VS Code + Calva", "compiler": "Clojure", "build": "deps.edn / tools.build", "pkg": "Clojars / Maven", "debug": "Calva"},
    ],
    "hello": {
        "file": "hello.clj",
        "code": r"""(println "Hello, world")""",
        "footprint": [
            {"stage": "源码", "size": "≈ 24 B", "w": 4},
            {"stage": "表单", "size": "≈ 40 B", "w": 5},
            {"stage": ".class", "size": "≈ 1 KB", "w": 12},
            {"stage": "uberjar", "size": "≈ 4 MB", "w": 55},
            {"stage": "+ JVM", "size": "≈ 200 MB", "w": 100},
        ],
        "why": [
            "<strong>代码即数据</strong>：读取器产出的结构直接进入宏与编译器。",
            "<strong>JVM 字节码</strong>：没有独立字节码格式，复用 JVM 的工具与生态。",
            "<strong>AOT 可选</strong>：默认运行时编译，需要时提前生成 .class。",
            "<strong>uberjar</strong>：把运行时与依赖打进同一个 jar，简化部署。",
        ],
    },
},

# ============================================================
"groovy": {
    "tagline": "JVM 上的动态脚本：Java 语法减掉仪式感，加上闭包与 DSL。",
    "intro": [
        "Groovy 由 James Strachan 在 2003 年创建，目标是给 Java 平台加一门动态、简洁的脚本语言。它可以与 Java 无缝互操作，语法上省掉分号、getter/setter 与类型声明。",
        "Groovy 在 2.0 之后大量使用 `invokedynamic` 与 call site 缓存，把动态调用做得更接近静态语言性能。Groovy 代码编译成标准的 JVM `.class`，因此可以被打进 jar 或在 Java 项目中直接使用。",
        "它最持久的影响可能在构建工具：Gradle 的构建脚本就是 Groovy DSL。Jenkins Pipeline 也大量使用 Groovy。",
    ],
    "lineage": {
        "from": ["Java", "Ruby", "Python", "Smalltalk（部分）"],
        "to": ["Gradle DSL", "Jenkins Pipeline", "Kotlin DSL（竞争）"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.groovy",
            "cmd": "$ cat hello.groovy",
            "code": r"""println "Hello, world"

// 省掉分号、类型与 main
// 顶层语句自动包进 run()""",
            "format": [
                ("扩展名", ".groovy / .gradle"),
                ("类型", "动态，可选静态编译"),
                ("顶层语句", "自动变成 run()"),
                ("互操作", "直接调用 Java 类"),
            ],
            "note": "Groovy 脚本没有显式 main：顶层语句被编译器包进一个脚本类的 run() 方法。",
        },
        {
            "label": "AST",
            "file": "AST",
            "cmd": "$ groovy -e 'new AstBuilder().buildFromString(...)'",
            "code": r"""MethodCallExpression
  method: println
  arguments:
    ConstantExpression "Hello, world"

; Groovy 的 AST 转换阶段：
;   parsing → conversion → semantic analysis → canonicalization
; 大量 DSL 通过 AST 变换实现""",
            "format": [
                ("AST", "Groovy AST（可变换）"),
                ("阶段", "解析 → 转换 → 语义分析"),
                ("DSL", "AST 变换是 Groovy DSL 的基础"),
                ("注解", "@CompileStatic / @TypeChecked"),
            ],
            "note": "Groovy 的编译器允许在 AST 阶段插入变换；Gradle 的 DSL 与 Spock 的断言都靠这一层。",
        },
        {
            "label": "字节码",
            "file": "Hello.class",
            "cmd": "$ groovyc hello.groovy && javap -c Hello",
            "code": r"""$ javap -c Hello
public class Hello extends groovy.lang.Script {
  public java.lang.Object run();
    Code:
       0: aload_0
       1: invokedynamic #...  // call site
       6: ...
  public static void main(java.lang.String[]);
    ...
}

; 动态调用经 invokedynamic + call site 缓存
; 类仍然是标准 JVM 字节码""",
            "format": [
                ("产物", "JVM .class"),
                ("调用", "invokedynamic + call site"),
                ("基类", "groovy.lang.Script"),
                ("静态编译", "@CompileStatic 可去掉动态派发"),
            ],
            "note": "Groovy 的动态性由 call site 实现：第一次调用慢，之后缓存方法句柄。`@CompileStatic` 则走静态绑定。",
        },
        {
            "label": "JAR / 运行时",
            "file": "hello.jar",
            "cmd": "$ groovyc hello.groovy && jar cf hello.jar Hello.class",
            "code": r"""$ java -cp hello.jar:$GROOVY_HOME/lib/groovy.jar Hello
Hello, world

$ unzip -l hello.jar
  Hello.class

; 需要 groovy 运行时（groovy.jar）
; Gradle 把它作为构建脚本的运行时
; 也可用 groovy-all 打包""",
            "format": [
                ("容器", "JAR"),
                ("依赖", "groovy.jar"),
                ("运行", "java -cp …"),
                ("构建工具", "Gradle / Jenkins 内嵌"),
            ],
            "note": "Groovy 的部署单位仍是 jar + 运行时。它在构建工具里更多是「被嵌入的脚本引擎」，而不是独立应用。",
        },
    ],
    "tools": [
        {"era": "2000s", "editor": "Eclipse / IDEA", "compiler": "groovyc", "build": "Ant / Gant", "pkg": "Groovy Grape", "debug": "IDE"},
        {"era": "2010s", "editor": "IntelliJ IDEA", "compiler": "groovyc", "build": "Gradle", "pkg": "Maven / Grape", "debug": "IDE"},
        {"era": "2020s", "editor": "IntelliJ / VS Code", "compiler": "groovyc", "build": "Gradle", "pkg": "Maven Central", "debug": "IDE"},
    ],
    "hello": {
        "file": "hello.groovy",
        "code": r"""println "Hello, world"
// 输出：Hello, world""",
        "footprint": [
            {"stage": "源码", "size": "≈ 22 B", "w": 4},
            {"stage": "AST", "size": "≈ 400 B", "w": 10},
            {"stage": ".class", "size": "≈ 3 KB", "w": 16},
            {"stage": "jar", "size": "≈ 2 KB", "w": 14},
            {"stage": "+ groovy", "size": "≈ 7 MB", "w": 80},
        ],
        "why": [
            "<strong>脚本类</strong>：顶层语句被包进 run()，没有显式 main。",
            "<strong>AST 变换</strong>：DSL 与注解在编译期改写语法树。",
            "<strong>invokedynamic</strong>：动态派发用 call site 缓存，兼顾灵活与性能。",
            "<strong>JVM jar</strong>：产物与 Java 生态一致，运行时库单独依赖。",
        ],
    },
},

# ============================================================
"go": {
    "tagline": "为工程化并发与云原生基础设施设计：简单语法、静态二进制、自带运行时。",
    "intro": [
        "Go 由 Robert Griesemer、Rob Pike 与 Ken Thompson 在 Google 设计，2009 年开源。它刻意保持语法小：没有继承、没有异常、没有模板；用 goroutine 与 channel 表达并发，用接口做抽象。",
        "Go 的产物链有自己的规则：编译器生成 Go 目标文件（自定义格式），链接器负责把它们拼成静态 ELF。运行时（调度器、GC、栈管理）被静态链接进每个二进制，因此 hello 也有 MB 级体积，且不依赖 libc。",
        "`go build` 的缓存、`go tool nm`、`go version -m` 都是这条链的观察窗口。理解它，就能理解为什么 Go 的部署常常只是「拷贝一个文件」。",
    ],
    "lineage": {
        "from": ["C", "Pascal / Modula（语法）", "CSP（并发）", "Newsqueak"],
        "to": ["云原生工具链", "TinyGo", "Zig（部分反思）"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.go",
            "cmd": "$ cat hello.go",
            "code": r"""package main

import "fmt"

func main() {
    fmt.Println("Hello, world")
}""",
            "format": [
                ("扩展名", ".go"),
                ("包", "package main + func main"),
                ("导入", "显式 import，不允许未使用"),
                ("格式", "gofmt 强制统一"),
            ],
            "note": "Go 的包与入口都是显式的。`fmt.Println` 来自标准库，最终会被链接进二进制。",
        },
        {
            "label": "SSA",
            "file": "ssa.html / SSA",
            "cmd": "$ GOSSAFUNC=main go build hello.go",
            "code": r"""b1:
  v1 = InitMem <mem>
  v2 = SP <uintptr>
  v3 = SB <uintptr>
  v4 = LocalAddr <*string> ...
  v6 = StaticCall <mem> {fmt.Println} ...
  v7 = Exit <mem> v6
  Ret v7

; Go 编译器的 SSA 中间表示
; GOSSAFUNC 生成 ssa.html，展示各优化阶段""",
            "format": [
                ("中间表示", "SSA"),
                ("阶段", "lower → opt → regalloc"),
                ("查看", "GOSSAFUNC=name go build"),
                ("产物", "ssa.html（可视化）"),
            ],
            "note": "Go 的 SSA 不是可加载产物，而是编译器的内部表示。`ssa.html` 把各阶段并排展示，是学习 Go 后端的好材料。",
        },
        {
            "label": "汇编",
            "file": "hello.s",
            "cmd": "$ go tool compile -S hello.go",
            "code": r"""TEXT main.main(SB) /home/user/hello.go
  ...
  LEAQ go:string."Hello, world"(SB), AX
  MOVQ AX, (SP)
  CALL fmt.Println(SB)
  RET

; Go 汇编是 Plan 9 语法
; go:string."Hello, world" 是只读字符串符号
; 调用 fmt.Println 由链接器解析""",
            "format": [
                ("语法", "Plan 9 汇编"),
                ("字符串", "go:string.\"...\" 符号"),
                ("调用", "CALL fmt.Println(SB)"),
                ("查看", "go tool compile -S / go tool objdump"),
            ],
            "note": "Go 汇编不是 GNU as：寄存器名、操作数顺序、符号命名都不同。它主要供编译器与运行时使用。",
        },
        {
            "label": "目标文件",
            "file": "hello.o",
            "cmd": "$ go tool compile -p main -importcfg importcfg -o hello.o hello.go",
            "code": r"""$ head -c 48 hello.o
go object linux amd64 go1.22.0 X:regabi

$ go tool nm hello.o | grep main
  ... T main.main
  ... T main.init
  ... U fmt.Println

; Go 目标文件是自定义格式（含导出数据）
; 不是 ELF / COFF
; 链接器读取后生成最终可执行文件""",
            "format": [
                ("格式", "Go object（自定义）"),
                ("魔数", "go object <os> <arch> <version>"),
                ("符号", "main.main / fmt.Println"),
                ("链接", "go tool link"),
            ],
            "note": "Go 编译器需要 importcfg 指向依赖包的导出数据；`go build` 在内部生成它。目标文件不是 ELF，而是带类型与导出信息的自定义容器。",
        },
        {
            "label": "静态 ELF",
            "file": "hello",
            "cmd": "$ go build -o hello && file hello && ldd hello",
            "code": r"""$ file hello
hello: ELF 64-bit LSB executable, x86-64, statically linked

$ ldd hello
        not a dynamic executable

$ ls -lh hello
-rwxr-xr-x 1 user user 2.1M ... hello

$ go version -m hello
hello: go1.22.0
  path  hello
  mod   hello (devel)

; 运行时（调度器、GC、栈）静态链接
; 默认不依赖 libc""",
            "format": [
                ("格式", "ELF 可执行"),
                ("链接", "静态，默认无 libc"),
                ("运行时", "调度器 / GC / 栈管理"),
                ("体积", "hello ≈ 2 MB"),
            ],
            "note": "Go 的静态二进制是它云原生流行的原因之一：没有动态库版本问题，拷贝即可运行。",
        },
    ],
    "tools": [
        {"era": "2000s", "editor": "vim / Emacs", "compiler": "gc", "build": "go build", "pkg": "go get", "debug": "gdb"},
        {"era": "2010s", "editor": "VS Code + Go", "compiler": "gc", "build": "go build", "pkg": "go modules", "debug": "delve"},
        {"era": "2020s", "editor": "VS Code + gopls", "compiler": "gc", "build": "go build", "pkg": "go modules", "debug": "delve"},
    ],
    "hello": {
        "file": "hello.go",
        "code": r"""package main

import "fmt"

func main() {
    fmt.Println("Hello, world")
}""",
        "footprint": [
            {"stage": "源码", "size": "≈ 80 B", "w": 4},
            {"stage": "SSA", "size": "≈ 2 KB", "w": 10},
            {"stage": "汇编", "size": "≈ 1.5 KB", "w": 9},
            {"stage": "hello.o", "size": "≈ 20 KB", "w": 20},
            {"stage": "静态 ELF", "size": "≈ 2.1 MB", "w": 90},
        ],
        "why": [
            "<strong>SSA</strong>：编译器内部表示，负责优化与寄存器分配。",
            "<strong>Go object</strong>：自定义目标格式，携带类型与导出信息。",
            "<strong>静态链接</strong>：运行时与标准库都进二进制，部署无依赖。",
            "<strong>自带运行时</strong>：goroutine 调度、GC、栈增长都由它提供。",
        ],
    },
},

# ============================================================
"d": {
    "tagline": "Walter Bright 的 C++ 改良方案：GC、模板、range 与 -betterC。",
    "intro": [
        "D 由 Walter Bright 在 2001 年发布，后来与 Andrei Alexandrescu 合作设计。它想保留 C++ 的性能与系统能力，同时去掉头文件、宏与部分复杂度，加入垃圾回收、模块、模板与 range。",
        "D 的编译器（dmd）直接生成目标文件，没有暴露的文本 IR。它用 `.di` 接口文件替代头文件：`dmd -H` 从实现生成声明，客户模块只依赖 `.di`。",
        "D 提供 `-betterC` 模式，可以关掉运行时与 GC，接近 C 的部署模型；但默认模式会链接 druntime 与 Phobos，提供 GC、数组、字符串与并行运行时。",
    ],
    "lineage": {
        "from": ["C++", "Java", "C#", "Python（range 影响）"],
        "to": ["Rust（部分）", "Go（部分）", "range 概念影响 C++20"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "hello.d",
            "cmd": "$ cat hello.d",
            "code": r"""import std.stdio;

void main() {
    writeln("Hello, world");
}""",
            "format": [
                ("扩展名", ".d"),
                ("模块", "module 声明可选"),
                ("导入", "import std.stdio"),
                ("入口", "void main()"),
            ],
            "note": "D 没有头文件：模块与导入是语言级的，编译器直接读取 `.d` 或预编译的 `.di`。",
        },
        {
            "label": "接口文件",
            "file": "hello.di",
            "cmd": "$ dmd -H hello.d",
            "code": r"""// 由 dmd -H 生成（示意）
module hello;

void main();

; .di 只含声明，不含实现
; 客户模块依赖 .di 做类型检查
; 对应 C 的头文件 / Modula-2 的 .def""",
            "format": [
                ("扩展名", ".di"),
                ("生成", "dmd -H"),
                ("内容", "声明，无实现"),
                ("作用", "独立编译与接口分发"),
            ],
            "note": "`.di` 是 D 对头文件的替代：它由编译器从源码生成，避免手写声明与实现不一致。",
        },
        {
            "label": "目标文件",
            "file": "hello.o",
            "cmd": "$ dmd -c hello.d && nm hello.o | grep -E 'main|writeln'",
            "code": r"""$ nm hello.o | grep -E 'main|writeln'
... T _Dmain
... U _D3std5stdio__T7writeln...
... U gc_malloc
... U _d_run_main

; D 的符号修饰包含模块与模板实例
; 目标文件是平台 ELF/COFF
; 默认会引用 druntime（GC、异常）""",
            "format": [
                ("格式", "ELF / COFF 目标"),
                ("符号", "模块 + 模板实例修饰"),
                ("运行时", "druntime（GC、异常）"),
                ("模板", "实例化在编译期完成"),
            ],
            "note": "D 的模板在编译期实例化，符号里会带上完整实例参数。目标文件里能看到大量展开后的模板代码。",
        },
        {
            "label": "可执行",
            "file": "hello",
            "cmd": "$ dmd hello.d && ./hello",
            "code": r"""$ ./hello
Hello, world

$ file hello
hello: ELF 64-bit LSB pie executable, x86-64 ...

$ ldd hello
  libc.so.6
  libgcc_s.so.1
  libphobos2.so.0

; 默认链接 druntime + Phobos
; -betterC 可去掉运行时与 GC
; 体积：hello ≈ 1.5 MB（动态）""",
            "format": [
                ("格式", "ELF / PE / Mach-O"),
                ("运行时", "druntime + Phobos"),
                ("GC", "默认启用"),
                ("-betterC", "关闭运行时，接近 C"),
            ],
            "note": "D 的默认部署模型比 C 重：GC、异常、模块注册都需要运行时。`-betterC` 则把它拉回 C 的世界。",
        },
    ],
    "tools": [
        {"era": "2000s", "editor": "vim / Emacs", "compiler": "dmd", "build": "make", "pkg": "—", "debug": "gdb"},
        {"era": "2010s", "editor": "VisualD / VS Code", "compiler": "dmd / ldc / gdc", "build": "dub", "pkg": "dub", "debug": "gdb / lldb"},
        {"era": "2020s", "editor": "VS Code + serve-d", "compiler": "dmd / ldc / gdc", "build": "dub", "pkg": "dub", "debug": "gdb / lldb"},
    ],
    "hello": {
        "file": "hello.d",
        "code": r"""import std.stdio;
void main() {
    writeln("Hello, world");
}""",
        "footprint": [
            {"stage": "源码", "size": "≈ 70 B", "w": 4},
            {"stage": ".di", "size": "≈ 50 B", "w": 3},
            {"stage": ".o", "size": "≈ 4 KB", "w": 14},
            {"stage": "可执行", "size": "≈ 1.5 MB", "w": 60},
            {"stage": "+ Phobos", "size": "≈ 4 MB", "w": 80},
        ],
        "why": [
            "<strong>.di</strong>：编译器生成的接口文件，替代手写头文件。",
            "<strong>模板实例化</strong>：模板在编译期展开，符号携带完整实例信息。",
            "<strong>druntime</strong>：GC、异常、模块注册都由运行时提供。",
            "<strong>-betterC</strong>：关掉运行时，回到 C 式部署。",
        ],
    },
},

# ============================================================
"actionscript": {
    "tagline": "Flash 时代的 ActionScript 3：AVM2、SWF 与浏览器里的富应用。",
    "intro": [
        "ActionScript 最初是 Flash 里的简单脚本语言，2006 年的 ActionScript 3 彻底转向 ECMAScript 标准，加入类、包、强类型与 AVM2 虚拟机。它支撑了 Flash 游戏、广告与富媒体应用的一个时代。",
        "AS3 源码编译成 ABC（ActionScript Byte Code），作为 DoABC 标签嵌进 SWF 文件。SWF 是容器：头部、舞台参数、标签流，其中既有矢量图形，也有字节码。",
        "Flash Player 在 2020 年底停止支持，但 AIR 仍然在桌面与移动端使用。AS3 的产物链是理解「字节码 + 媒体容器」的一个好样本。",
    ],
    "lineage": {
        "from": ["ECMAScript", "Java（类/包）", "Flash"],
        "to": ["Haxe（部分）", "HTML5 迁移", "AIR 桌面应用"],
    },
    "chain": [
        {
            "label": "源码",
            "file": "Hello.as",
            "cmd": "$ cat Hello.as",
            "code": r"""package {
    import flash.display.Sprite;
    import flash.text.TextField;

    public class Hello extends Sprite {
        public function Hello() {
            var tf:TextField = new TextField();
            tf.text = "Hello, world";
            addChild(tf);
        }
    }
}""",
            "format": [
                ("扩展名", ".as"),
                ("结构", "package / class / 构造函数"),
                ("类型", "可选强类型"),
                ("运行", "Flash Player / AIR 的 AVM2"),
            ],
            "note": "AS3 的类在构造时创建显示对象。`TextField` 是矢量文本组件，不是 DOM 元素。",
        },
        {
            "label": "ABC 字节码",
            "file": "Hello.abc",
            "cmd": "$ swfdump -D hello.swf",
            "code": r"""// ABC 反汇编（示意）
class Hello extends flash.display.Sprite
  cinit:
    getlocal_0
    pushstring "Hello, world"
    constructprop flash.text.TextField
    ...
    callpropvoid addChild
    returnvoid

; ABC = ActionScript Byte Code
; 运行在 AVM2 上
; 常量池、方法体、类定义""",
            "format": [
                ("字节码", "ABC（AVM2）"),
                ("栈式", "操作数栈 + 作用域链"),
                ("常量池", "字符串、数字、类引用"),
                ("查看", "swfdump -D / abcdump"),
            ],
            "note": "ABC 是 SWF 里的一个标签内容，不是独立文件。它包含常量池、方法体、类与脚本初始化。",
        },
        {
            "label": "SWF",
            "file": "hello.swf",
            "cmd": "$ mxmlc -output hello.swf Hello.as && xxd -l 32 hello.swf",
            "code": r"""$ xxd -l 32 hello.swf
00000000: 4657 530a 2c01 0000 7800 05...  FWS.,...x...

; 46 57 53 = "FWS"（未压缩）
; 0a       = SWF 版本 10
; 2c 01 00 00 = 文件长度
; 之后：舞台矩形、帧率、帧数、标签流
; DoABC 标签里是 ABC 字节码
; CWS = zlib 压缩，ZWS = LZMA 压缩""",
            "format": [
                ("魔数", "FWS / CWS / ZWS"),
                ("版本", "SWF 版本号"),
                ("标签", "DoABC / DefineShape / ShowFrame …"),
                ("压缩", "FWS 无 / CWS zlib / ZWS LZMA"),
            ],
            "note": "SWF 是标签流容器：矢量图形、位图、音频、字体、字节码都在同一个文件里。",
        },
        {
            "label": "AIR 包",
            "file": "hello.air",
            "cmd": "$ adt -package -storetype pkcs12 hello.air application.xml hello.swf",
            "code": r"""$ adt -package -storetype pkcs12 hello.air application.xml hello.swf
$ unzip -l hello.air
  application.xml
  hello.swf
  META-INF/AIR/application.xml
  META-INF/AIR/publisherid

; AIR = zip + 应用描述 + SWF/资源
; 由 AIR 运行时装在桌面/移动端
; 仍是 AVM2 执行 ABC""",
            "format": [
                ("容器", "zip"),
                ("描述", "application.xml"),
                ("内容", "SWF + 资源"),
                ("运行时", "AIR Runtime"),
            ],
            "note": "AIR 把 SWF 包成桌面应用：同一个 ABC 字节码，换一个运行时与安装格式。",
        },
    ],
    "tools": [
        {"era": "2000s", "editor": "Flash IDE", "compiler": "mxmlc / asc", "build": "Ant / Flash IDE", "pkg": "SWC", "debug": "Flash 调试器"},
        {"era": "2010s", "editor": "Flash Builder / IntelliJ", "compiler": "mxmlc / asc2", "build": "Ant / Maven", "pkg": "SWC / ANE", "debug": "Flash Builder"},
        {"era": "2020s", "editor": "VS Code + AS3", "compiler": "Apache Royale / asc", "build": "Ant", "pkg": "SWC", "debug": "AIR 调试器"},
    ],
    "hello": {
        "file": "Hello.as",
        "code": r"""package {
    import flash.display.Sprite;
    import flash.text.TextField;
    public class Hello extends Sprite {
        public function Hello() {
            var tf:TextField = new TextField();
            tf.text = "Hello, world";
            addChild(tf);
        }
    }
}""",
        "footprint": [
            {"stage": "源码", "size": "≈ 280 B", "w": 6},
            {"stage": "ABC", "size": "≈ 600 B", "w": 12},
            {"stage": "SWF", "size": "≈ 1.2 KB", "w": 16},
            {"stage": "AIR", "size": "≈ 18 KB", "w": 30},
            {"stage": "+ AVM2", "size": "≈ 10 MB", "w": 85},
        ],
        "why": [
            "<strong>ABC</strong>：AVM2 的栈式字节码，和 JVM 思路相近但指令集不同。",
            "<strong>SWF 标签流</strong>：字节码与图形、音频、字体共用一个容器。",
            "<strong>压缩变体</strong>：FWS/CWS/ZWS 三种头部，决定文件如何加载。",
            "<strong>AIR</strong>：同一份 ABC 换个运行时与打包格式，变成桌面应用。",
        ],
    },
},

}

# -*- coding: utf-8 -*-
"""产物格式索引：格式 → 产生它的语言与阶段。

匹配方式：
1. file_match：阶段文件名包含任一关键字（精确，召回低）；
2. langs：人工指定的代表语言，取该语言的最后阶段（策展）。
两者合并去重；每个语言最多保留 2 个阶段。
"""

GROUPS = [
    ("exec", "可执行与目标文件", "链接器、载入器与系统最终处理的二进制。"),
    ("bytecode", "字节码与中间表示", "虚拟机或编译器后端消费的中间形态。"),
    ("package", "打包与分发", "面向部署的归档、镜像与安装包。"),
    ("data", "数据、文档与配置", "供浏览器、工具或人消费的格式。"),
    ("gpu", "图形、GPU 与硬件", "图形管线、并行计算与芯片配置。"),
]

# (key, 名称, 说明, 分组, 文件名关键字, 策展语言)
SPECS = [
    # 可执行与目标
    ("elf", "ELF", "Linux / Unix 的可执行、共享库与目标文件", "exec",
     ["elf", ".o", "hello.o", "hello_netlist.v", "a.out"], []),
    ("aout", "a.out", "早期 UNIX 的可执行格式", "exec", ["a.out"], ["b"]),
    ("dex", "DEX", "Android 的寄存器式字节码容器", "exec", [".dex"], ["java", "kotlin", "dart"]),
    ("msi", "MSI / ClickOnce", "Windows 安装与部署包", "exec", [], ["vb", "csharp"]),
    ("exe-pe", "PE / .exe", "Windows 可执行与对象文件", "exec",
     [".exe", "hello.exe", "pe32"], ["c", "cpp", "rust", "go", "zig", "d"]),
    # 打包
    ("apk", "APK / AAB", "Android 应用包", "package", ["apk"], ["dart", "kotlin"]),
    ("ipa", "IPA", "iOS 应用包", "package", [], ["swift", "objectivec"]),
    ("appbundle", "App Bundle", "macOS 应用目录结构", "package", [], ["swift", "objectivec"]),
    ("static", "静态可执行", "自包含、无动态库依赖的二进制", "package",
     ["statically linked", "static"], ["go", "zig", "rust"]),
    ("image", "镜像 / 堆快照", "Smalltalk、Lisp、Forth 保存的运行时状态", "package",
     [], ["smalltalk", "lisp", "commonlisp", "forth", "scheme", "apl"]),
    ("release", "Release / shipment", "BEAM 运行时 + 模块的部署目录", "package",
     ["release", "shipment", "erlang-shipment"], ["erlang", "elixir", "gleam"]),
    ("phar", "PHAR", "PHP 的归档格式", "package", ["phar"], ["php"]),
    ("langpkg", "语言包管理器产物", "gem / crate / hex / cpan / composer 的分发单位", "package",
     [], ["ruby", "rust", "elixir", "perl", "php", "haskell"]),
    # 字节码与 IR
    ("class", ".class", "JVM 类文件，含常量池与栈式字节码", "bytecode",
     [".class", "hello.class", "hellokt.class", "hello$.class"], ["java", "kotlin", "scala", "clojure", "groovy"]),
    ("jar", "JAR / WAR", "Java 归档：zip 容器 + 清单", "bytecode",
     ["jar", "war", "ear", "uberjar"], []),
    ("cil", "CIL / 程序集", ".NET 中间语言与 PE 程序集", "bytecode",
     [".dll", "hello.il", "程序集"], ["csharp", "fsharp", "vb"]),
    ("beam", "BEAM", "Erlang / Elixir / Gleam 模块字节码", "bytecode",
     [".beam", "beam", "for1"], ["erlang", "elixir", "gleam"]),
    ("pyc", ".pyc", "Python 字节码缓存（带版本魔数）", "bytecode", ["pyc", "__pycache__"], ["python"]),
    ("pyz", ".pyz / 打包二进制", "Python zipapp 与 PyInstaller 产物", "package", ["pyz", "pyinstaller"], ["python"]),
    ("luac", ".luac", "Lua 预编译字节码", "bytecode", ["luac"], ["lua"]),
    ("yarv", "YARV ISeq", "Ruby 1.9+ 的字节码指令序列", "bytecode", [".rbc", "iseq"], ["ruby"]),
    ("opcode", "opcode / optree", "解释器内部指令（PHP、Perl、Tcl、APL 等）", "bytecode",
     ["opcode", "optree", "token"], ["php", "perl", "tcl", "apl"]),
    ("wasm", "WebAssembly", "可移植的栈式字节码，面向 Web 与非 Web 宿主", "bytecode",
     ["wasm"], ["rust", "cpp", "c", "zig", "go", "roc", "assembly"]),
    ("llvm", "LLVM IR", "编译器后端的中间表示（.ll / 位码）", "bytecode",
     [".ll", "llvm"], ["swift", "rust", "zig", "nim", "crystal", "julia", "carbon", "mojo", "odin", "clang"]),
    ("mir", "MIR / SIL / Core / STG", "语言专属的中高层中间表示", "bytecode",
     [".mir", ".sil", ".core", "core.ml", "stg", "lambda"], ["rust", "swift", "haskell", "ml", "ocaml", "erlang", "gleam"]),
    ("wam", "WAM", "Prolog 的抽象机指令", "bytecode", ["wam"], ["prolog"]),
    ("evm", "EVM 字节码 / ABI", "以太坊虚拟机字节码与调用 ABI", "bytecode",
     [".abi", ".yul"], ["solidity"]),
    ("spirv", "SPIR-V", "GPU 着色器的可移植中间表示", "bytecode", [".spv"], ["glsl"]),
    ("assembly", "汇编文本", "面向具体 ISA 的符号化指令", "bytecode",
     [".s", ".lst", "hello.sass"], []),
    # 数据与文档
    ("html", "HTML / DOM", "浏览器文档树", "data", [".html"], ["html", "javascript", "typescript", "markdown"]),
    ("css", "CSS / CSSOM", "样式表与计算样式", "data", [".css"], ["css", "sass", "less"]),
    ("json", "JSON", "通用数据交换与配置", "data", [".json"], ["sql", "typescript", "xml", "solidity", "clojure"]),
    ("yaml", "YAML", "配置与基础设施清单", "data", [".yaml", ".yml"], ["yaml"]),
    ("xml", "XML / XSD / XSLT", "结构化数据、模式与转换", "data", [".xml", ".xsd", ".xsl", ".xslt"], ["xml"]),
    ("svg", "SVG", "矢量图形（XML）", "data", [".svg"], ["svg"]),
    ("md", "Markdown / MDX", "文档与静态站点源", "data", [".md", ".mdx", ".rmd"], ["markdown"]),
    ("vcd", "VCD", "硬件仿真的值变化转储", "data", [".vcd"], ["verilog"]),
    # GPU / 硬件
    ("ptx", "PTX", "CUDA 的虚拟指令集", "data", [".ptx"], ["cuda"]),
    ("cubin", "cubin / fatbin", "CUDA 设备代码容器", "gpu", ["cubin", "fatbin"], ["cuda"]),
    ("sassgpu", "SASS（GPU 机器码）", "NVIDIA GPU 的具体指令集", "gpu", [".sass"], ["cuda"]),
    ("netlist", "门级网表", "综合后的电路连接", "gpu", ["netlist"], ["verilog"]),
    ("bitstream", "比特流", "FPGA 配置位流", "gpu", [], ["verilog"]),
]

# 去重（同名 key 保留第一个）
_seen = set()
_clean = []
for spec in SPECS:
    if spec[0] in _seen:
        continue
    _seen.add(spec[0])
    _clean.append(spec)
SPECS = _clean


def _file_hit(filename, key):
    f = filename.lower()
    key = key.lower()
    if key.startswith("."):
        return f.endswith(key)
    return key in f


def build(data):
    results = []
    for key, name, desc, group, file_keys, curated in SPECS:
        hits = []
        seen = set()
        for slug, lang in data.items():
            for i, stage in enumerate(lang["chain"], start=1):
                f = stage["file"].lower()
                if any(_file_hit(f, k) for k in file_keys):
                    if (slug, i) not in seen:
                        seen.add((slug, i))
                        hits.append((slug, i, stage["label"], stage["file"]))
        for slug in curated:
            if slug not in data:
                continue
            if any(h[0] == slug for h in hits):
                continue
            # 策展项不猜具体阶段：链接到语言页本身
            seen.add((slug, 0))
            hits.append((slug, 0, "语言档案", ""))
        if not hits:
            continue
        # 每个语言最多 2 个阶段
        per = {}
        final = []
        for h in sorted(hits, key=lambda x: (x[0], x[1])):
            n = per.get(h[0], 0)
            if n < 2:
                per[h[0]] = n + 1
                final.append(h)
        results.append({
            "key": key, "name": name, "desc": desc, "group": group,
            "langs": sorted({h[0] for h in final}),
            "hits": final,
        })
    return results

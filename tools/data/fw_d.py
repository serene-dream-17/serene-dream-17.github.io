# -*- coding: utf-8 -*-
"""框架层 · 科学/企业 + 38 门短页 + 场景矩阵数据。"""

DETAIL = {

# ============================================================
"fortran": {
    "summary": "Fortran 没有 Web 框架；它的「框架层」是数值库、并行通信与科学数据格式。",
    "scenarios": ["数值计算", "HPC", "科学数据"],
    "picks": [
        ("线性代数", "LAPACK / BLAS", "稠密矩阵的标准实现"),
        ("分布式并行", "MPI", "多进程、多节点通信"),
        ("科学数据", "NetCDF", "自描述数组文件"),
    ],
    "cards": [
        {
            "name": "LAPACK / BLAS", "year": 1992, "type": "数值库",
            "maintainer": "Netlib / 社区",
            "tagline": "线性代数与基础向量运算的标准库，Fortran 科学计算的底座。",
            "fit": ["稠密矩阵求解", "特征值/SVD", "HPC 数值内核"],
            "avoid": ["非数值业务", "需要动态数据结构"],
            "chain": ["Fortran 调用", "链接 BLAS/LAPACK", "库", "可执行/库"],
            "projects": ["MATLAB/NumPy 底层", "科学软件"],
            "alternatives": [("BLIS", "更现代的 BLAS"), ("Eigen", "C++ 头文件库")],
            "division": "BLAS 管基础运算；LAPACK 管矩阵分解；Eigen 偏 C++ 模板。",
        },
        {
            "name": "MPI", "year": 1994, "type": "并行通信",
            "maintainer": "MPI Forum",
            "tagline": "分布式内存并行的消息传递标准，多进程/多节点科学计算的基础。",
            "fit": ["HPC 集群", "多节点并行", "大规模数值模拟"],
            "avoid": ["单机小脚本", "共享内存小任务"],
            "chain": ["Fortran/C 源码", "mpif90", "MPI 库", "mpirun"],
            "projects": ["气象/流体模拟", "超级计算机应用"],
            "alternatives": [("OpenMP", "共享内存"), ("Coarray Fortran", "语言内并行")],
            "division": "MPI 跨节点；OpenMP 单节点多线程；Coarray 是 Fortran 内建。",
        },
        {
            "name": "NetCDF", "year": 1989, "type": "科学数据格式",
            "maintainer": "Unidata / UCAR",
            "tagline": "自描述的数组文件格式与库，气象、海洋与地球科学常用。",
            "fit": ["多维科学数据", "跨平台交换", "气候/海洋模型"],
            "avoid": ["事务型业务数据", "简单键值配置"],
            "chain": ["Fortran/C 调用", "NetCDF 库", ".nc 文件", "分析/可视化"],
            "projects": ["气候数据", "卫星产品"],
            "alternatives": [("HDF5", "更通用的层次格式"), ("Zarr", "云原生数组")],
            "division": "NetCDF 偏地球科学；HDF5 更通用；Zarr 适合云存储。",
        },
    ],
},

# ============================================================
"cobol": {
    "summary": "COBOL 的框架层是大型机事务与数据平台；开源侧以 GnuCOBOL 为入口。",
    "scenarios": ["大型机事务", "批处理", "遗留系统"],
    "picks": [
        ("在线事务", "CICS", "TP monitor、终端会话"),
        ("层次数据库/事务", "IMS", "大型机数据与事务"),
        ("开源编译器", "GnuCOBOL", "迁移/学习/测试"),
    ],
    "cards": [
        {
            "name": "CICS", "year": 1969, "type": "事务处理",
            "maintainer": "IBM",
            "tagline": "大型机在线事务处理监控器，管理终端会话、事务与资源。",
            "fit": ["银行/保险在线交易", "高吞吐事务", "z/OS 环境"],
            "avoid": ["新 Web 项目", "非大型机部署"],
            "chain": ["COBOL 程序", "CICS 编译", "load module", "CICS 区域"],
            "projects": ["银行核心", "保险理赔"],
            "alternatives": [("IMS TM", "IBM 另一套事务"), ("微服务", "新架构")],
            "division": "CICS 偏在线事务；IMS 偏层次数据+事务；微服务是新系统路线。",
        },
        {
            "name": "IMS", "year": 1966, "type": "层次数据库 / 事务",
            "maintainer": "IBM",
            "tagline": "IBM 的层次数据库与事务管理器，仍运行大量核心业务。",
            "fit": ["大型机核心数据", "层次结构数据", "高可靠事务"],
            "avoid": ["新项目（关系/云数据库更合适）", "非 IBM 平台"],
            "chain": ["DL/I 调用", "COBOL/PL/I", "IMS 数据库", "批处理/在线"],
            "projects": ["航空订票", "银行核心"],
            "alternatives": [("Db2", "关系数据库"), ("CICS + VSAM", "文件型事务")],
            "division": "IMS 层次库；Db2 关系库；CICS 常与 VSAM/Db2 组合。",
        },
        {
            "name": "GnuCOBOL", "year": 2002, "type": "编译器 / 运行时",
            "maintainer": "GnuCOBOL 社区",
            "tagline": "开源的 COBOL 编译器，先把 COBOL 翻译成 C，再生成原生程序。",
            "fit": ["COBOL 学习/测试", "迁移评估", "Linux 上的批处理"],
            "avoid": ["需要 IBM 大型机专有特性", "直接替换 CICS/IMS"],
            "chain": [".cob", "cobc -C", "C", "原生可执行"],
            "projects": ["迁移项目", "教学"],
            "alternatives": [("IBM Enterprise COBOL", "大型机生产"), ("Micro Focus", "商业实现")],
            "division": "GnuCOBOL 开源可移植；IBM/Micro Focus 提供大型机与企业支持。",
        },
    ],
},

}

SHORT = {
    "lisp": {
        "summary": "Common Lisp 没有 Web 应用框架的标准答案；生态以实现、库与交互式开发为中心。",
        "tools": ["SBCL", "Quicklisp", "ASDF", "Hunchentoot"],
        "when": "需要符号计算、DSL、交互式开发或 AI 研究时仍值得选。",
    },
    "algol60": {
        "summary": "ALGOL 60 没有现代应用框架；它主要作为语言史与编译技术的研究对象。",
        "tools": ["GNU MARST", "历史编译器", "BNF 工具"],
        "when": "教学、语言史研究，或需要理解块结构/按名调用的原始语义时。",
    },
    "basic": {
        "summary": "BASIC 没有统一的现代框架；生态分散在 FreeBASIC、QB64 与各类嵌入式方言。",
        "tools": ["FreeBASIC", "QB64", "Gambas"],
        "when": "教学、复古计算、快速小工具，或维护旧 BASIC 项目。",
    },
    "simula": {
        "summary": "Simula 没有活跃的应用框架；GNU Cim 是少数仍在维护的实现。",
        "tools": ["GNU Cim", "历史 Simula 编译器"],
        "when": "研究面向对象与仿真语言的源头，或维护历史代码。",
    },
    "pli": {
        "summary": "PL/I 的生态集中在 IBM 大型机与企业遗留系统，没有现代 Web 框架。",
        "tools": ["IBM Enterprise PL/I", "Iron Spring PL/I"],
        "when": "维护大型机业务系统，或迁移 PL/I 代码。",
    },
    "apl": {
        "summary": "APL 的「框架」是工作区与数组库；Dyalog 提供最完整的商业生态。",
        "tools": ["Dyalog APL", "GNU APL", "APL 工作区"],
        "when": "数组/金融/统计原型，或维护 APL 工作区。",
    },
    "snobol": {
        "summary": "SNOBOL 没有现代框架；CSNOBOL4 等实现主要用于语言研究与文本处理。",
        "tools": ["CSNOBOL4", "SNOBOL4", "历史实现"],
        "when": "模式匹配语言研究、遗留文本处理脚本。",
    },
    "b": {
        "summary": "B 没有活跃的框架或工具链；它主要是 C 与 UNIX 历史的一部分。",
        "tools": ["历史 PDP-7 工具链", "模拟器"],
        "when": "语言史、UNIX 早期实现研究。",
    },
    "pascal": {
        "summary": "Pascal 的现代生态集中在 Free Pascal/Lazarus 与 Delphi；没有 Web 主流框架。",
        "tools": ["Free Pascal", "Lazarus", "Delphi"],
        "when": "桌面工具、教学、维护 Turbo Pascal/Delphi 项目。",
    },
    "smalltalk": {
        "summary": "Smalltalk 的「框架」就是镜像与环境；Pharo/Squeak 提供活跃生态，Seaside 是 Web 框架。",
        "tools": ["Pharo", "Squeak", "Seaside", "GNU Smalltalk"],
        "when": "需要活的编程环境、对象系统研究，或维护 Smalltalk 应用。",
    },
    "prolog": {
        "summary": "Prolog 没有通用 Web 框架；SWI-Prolog 提供 HTTP 库与推理生态。",
        "tools": ["SWI-Prolog", "SICStus", "GNU Prolog"],
        "when": "规则推理、知识图谱、约束求解、逻辑编程教学。",
    },
    "ml": {
        "summary": "ML 没有统一的应用框架；SML/NJ、MLton 与 MLKit 是主要实现。",
        "tools": ["SML/NJ", "MLton", "MLKit"],
        "when": "编译器/语言研究、函数式教学、形式化工具。",
    },
    "scheme": {
        "summary": "Scheme 的生态以实现与库为主；Racket 提供最完整的语言工具链。",
        "tools": ["Chez Scheme", "Racket", "CHICKEN", "Guile"],
        "when": "语言实验、教学、脚本扩展、符号计算。",
    },
    "forth": {
        "summary": "Forth 没有应用框架；生态是各家实现与硬件/固件工具。",
        "tools": ["gforth", "SwiftForth", "Mecrisp"],
        "when": "嵌入式固件、极简运行时、交互式硬件控制。",
    },
    "modula2": {
        "summary": "Modula-2 没有现代应用框架；GNU Modula-2 是主要活跃实现。",
        "tools": ["GNU Modula-2（gm2）", "ADW"],
        "when": "教学、系统编程史、维护旧 Modula-2 代码。",
    },
    "ada": {
        "summary": "Ada 的生态以 GNAT、SPARK 与 Alire 为主；没有 Web 主流框架。",
        "tools": ["GNAT", "SPARK", "Alire"],
        "when": "高可靠/实时/军工系统、形式化验证、嵌入式。",
    },
    "eiffel": {
        "summary": "Eiffel 的框架层是 EiffelStudio 的库与契约工具；生态较小。",
        "tools": ["EiffelStudio", "LibertyEiffel", "EiffelStore"],
        "when": "教学契约式设计、维护 Eiffel 项目。",
    },
    "commonlisp": {
        "summary": "Common Lisp 有 Web 库（Hunchentoot 等），但没有单一主流框架。",
        "tools": ["SBCL", "CCL", "Quicklisp", "ASDF", "Hunchentoot"],
        "when": "符号计算、DSL、交互式开发、AI 研究。",
    },
    "tcl": {
        "summary": "Tcl 的框架层是 Tk、Expect 与 Tcllib；应用框架生态较小。",
        "tools": ["tclsh", "Tk", "Expect", "Tcllib"],
        "when": "EDA 脚本、网络设备自动化、GUI 小工具。",
    },
    "haskell": {
        "summary": "Haskell 有 Yesod/Servant 等 Web 框架，但生态规模小于主流语言。",
        "tools": ["GHC", "Cabal", "Stack", "Haskell Language Server"],
        "when": "类型系统研究、编译器、金融/形式化工具。",
    },
    "ocaml": {
        "summary": "OCaml 有 Dream、Lwt 等 Web 库；生态以编译器与金融工具为主。",
        "tools": ["ocamlopt", "dune", "opam", "Merlin"],
        "when": "编译器、金融风控、形式化验证、高性能 CLI。",
    },
    "groovy": {
        "summary": "Groovy 的框架层与 JVM 生态重叠：Grails 是 Web 框架，Gradle 是构建 DSL。",
        "tools": ["Gradle", "Grails", "Spock", "Jenkins"],
        "when": "Gradle 构建脚本、Jenkins Pipeline、遗留 JVM 脚本。",
    },
    "d": {
        "summary": "D 有 vibe.d 等 Web 框架，但生态规模有限。",
        "tools": ["DMD", "LDC", "dub", "vibe.d"],
        "when": "系统工具、需要 C++ 替代且接受较小生态。",
    },
    "actionscript": {
        "summary": "ActionScript 的生态随 Flash 退场；Apache Royale 与 AIR 仍在维护。",
        "tools": ["Apache Royale", "AIR SDK", "Starling"],
        "when": "维护 Flash/AIR 遗留应用，或迁移到 HTML5。",
    },
    "zig": {
        "summary": "Zig 还没有成熟的通用应用框架；生态以标准库、构建系统与 C 互操作为主。",
        "tools": ["zig build", "ZLS", "zig cc"],
        "when": "系统工具、交叉编译、需要 C 替代且能接受早期生态。",
    },
    "nim": {
        "summary": "Nim 有 Jester、Karax 等 Web 框架，但生态规模有限。",
        "tools": ["Nim", "nimble", "Jester", "Karax"],
        "when": "需要 Python 式语法 + C 性能，且接受较小生态。",
    },
    "crystal": {
        "summary": "Crystal 有 Lucky、Kemal 等 Web 框架，但生态仍在成长。",
        "tools": ["crystal", "shards", "Lucky", "Kemal"],
        "when": "Ruby 风格 + 原生性能，且接受较小生态。",
    },
    "elm": {
        "summary": "Elm 的框架层就是语言本身：Elm Architecture 与 elm-ui 等库。",
        "tools": ["elm make", "elm-test", "elm-ui"],
        "when": "类型安全前端、无运行时异常、愿意接受纯 Elm 生态。",
    },
    "mojo": {
        "summary": "Mojo 生态仍在早期，没有成熟的第三方应用框架。",
        "tools": ["Mojo SDK", "magic", "pixi"],
        "when": "AI 算子、Python 语法 + 系统性能的实验项目。",
    },
    "gleam": {
        "summary": "Gleam 有 Wisp、Mist 等 Web 库，但生态较新。",
        "tools": ["gleam", "Hex", "Wisp", "Mist"],
        "when": "BEAM 上的类型化服务、希望避开 null/异常。",
    },
    "carbon": {
        "summary": "Carbon 仍是实验性语言，没有可用的应用框架。",
        "tools": ["Carbon 工具链（实验）"],
        "when": "关注 C++ 后继语言与互操作设计，不建议生产使用。",
    },
    "odin": {
        "summary": "Odin 没有通用应用框架；生态以 core/vendor 库为主。",
        "tools": ["odin", "ols", "vendor 库"],
        "when": "游戏/图形工具、数据导向系统编程。",
    },
    "roc": {
        "summary": "Roc 通过「平台」提供运行时能力，没有传统应用框架。",
        "tools": ["roc", "basic-cli 平台"],
        "when": "函数式应用、Wasm/CLI 实验，接受早期工具链。",
    },
    "v": {
        "summary": "V 有 vweb 等内置 Web 模块，但生态与语义仍在演进。",
        "tools": ["v", "vpm", "vweb"],
        "when": "小型 CLI/服务、关注快速编译，接受早期生态。",
    },
    "assembly": {
        "summary": "汇编没有应用框架；它的生态是汇编器、链接器、调试器与反汇编器。",
        "tools": ["GNU as", "NASM", "ld", "objdump", "gdb"],
        "when": "引导程序、驱动、逆向、性能关键内核、理解机器码。",
    },
    "verilog": {
        "summary": "Verilog 的「框架」是验证方法学与 EDA 工具链：UVM、cocotb、Yosys。",
        "tools": ["Yosys", "Verilator", "Icarus Verilog", "UVM", "cocotb"],
        "when": "芯片/FPGA 设计、仿真验证、硬件原型。",
    },
    "cuda": {
        "summary": "CUDA 的框架层是 GPU 库与推理引擎：cuDNN、TensorRT、Thrust、CUB。",
        "tools": ["nvcc", "cuobjdump", "Nsight", "cuDNN", "TensorRT"],
        "when": "GPU 并行计算、深度学习训练/推理、科学加速。",
    },
    "glsl": {
        "summary": "GLSL 没有应用框架；生态是着色器编译、SPIR-V 与图形调试工具。",
        "tools": ["glslang", "SPIRV-Tools", "RenderDoc", "shaderc"],
        "when": "OpenGL/Vulkan/WebGPU 着色器、图形与计算管线。",
    },
}

SCENARIOS = [
    {
        "key": "web-backend", "title": "Web 后端", "range": "API / 服务端",
        "desc": "先看团队与交付速度，再看启动时间、类型安全与招聘市场。",
        "entries": [
            ("python", "Django", "全栈约定、后台与 ORM 一体"),
            ("java", "Spring Boot", "企业生态与招聘面最大"),
            ("go", "Gin", "静态二进制、部署简单"),
            ("javascript", "Express", "Node 生态、上手快"),
            ("typescript", "NestJS", "结构化、DI、适合大团队"),
            ("php", "Laravel", "交付快、生态完整"),
            ("ruby", "Rails", "约定优于配置、迭代快"),
            ("csharp", "ASP.NET Core", ".NET 企业栈、跨平台"),
            ("elixir", "Phoenix", "实时与高并发"),
            ("rust", "Axum", "类型安全与性能、生态较新"),
        ],
    },
    {
        "key": "web-frontend", "title": "Web 前端", "range": "UI / 交互",
        "desc": "生态、团队经验与首屏体积是主要权衡；内容站另看 SSR/静态生成。",
        "entries": [
            ("javascript", "React", "生态最大、组件化"),
            ("javascript", "Vue", "渐进式、模板直观"),
            ("typescript", "Angular", "大型团队、DI 与约定"),
            ("typescript", "Next.js", "全栈 React、SSR/SSG"),
            ("html", "Tailwind CSS", "原子化样式、设计系统"),
            ("css", "Bootstrap", "现成组件与栅格"),
            ("clojure", "Re-frame", "ClojureScript、事件驱动"),
        ],
    },
    {
        "key": "mobile", "title": "移动", "range": "iOS / Android / 跨平台",
        "desc": "原生能力、跨平台复用与 UI 一致性三者不可兼得。",
        "entries": [
            ("swift", "SwiftUI", "Apple 平台声明式 UI"),
            ("kotlin", "Jetpack Compose", "Android 官方声明式 UI"),
            ("dart", "Flutter", "一套代码跨移动/桌面/Web"),
            ("java", "Android SDK", "Android 原生 API 与 Jetpack"),
            ("objectivec", "Cocoa / Cocoa Touch", "维护旧 iOS/macOS 项目"),
        ],
    },
    {
        "key": "desktop", "title": "桌面", "range": "Windows / macOS / Linux",
        "desc": "原生控件、跨平台与 Web 技术栈之间选择。",
        "entries": [
            ("cpp", "Qt", "跨平台原生控件与工具链"),
            ("csharp", "WPF", "Windows 企业桌面"),
            ("rust", "Tauri", "Web 前端 + Rust 后端、体积小"),
            ("delphi", "VCL", "Windows 快速桌面"),
            ("vb", "WinForms", "内部工具、快速交付"),
            ("swift", "SwiftUI", "macOS 声明式 UI"),
            ("c", "GTK", "Linux 原生桌面"),
        ],
    },
    {
        "key": "data-ai", "title": "数据 / AI", "range": "分析 / 训练 / 服务",
        "desc": "训练、分析与服务是三套不同工具链，不要用一个框架硬套。",
        "entries": [
            ("python", "PyTorch", "训练与研究的主流"),
            ("python", "FastAPI", "模型服务与 API"),
            ("r", "tidyverse", "数据整理与可视化"),
            ("r", "Shiny", "数据应用与仪表盘"),
            ("julia", "Flux", "Julia 科学机器学习"),
            ("scala", "Apache Spark", "大规模数据处理"),
            ("sql", "dbt", "数仓转换与测试"),
        ],
    },
    {
        "key": "game", "title": "游戏", "range": "引擎 / 脚本",
        "desc": "3D 渲染、跨平台与迭代速度决定引擎；脚本层常与引擎绑定。",
        "entries": [
            ("cpp", "Unreal Engine", "高端 3D 与完整工具链"),
            ("csharp", "Unity", "跨平台与快速迭代"),
            ("rust", "Bevy", "ECS、代码驱动"),
            ("lua", "LÖVE", "轻量 2D"),
            ("lua", "Roblox", "平台化 UGC"),
        ],
    },
    {
        "key": "embedded", "title": "嵌入式 / 系统", "range": "RTOS / 原生",
        "desc": "资源、实时性与工具链成熟度优先；生态通常比语言特性更重要。",
        "entries": [
            ("c", "FreeRTOS", "MCU 实时调度"),
            ("cpp", "Qt", "嵌入式 GUI"),
            ("rust", "Tauri", "桌面端系统集成"),
            ("fortran", "MPI", "HPC 多节点"),
        ],
    },
    {
        "key": "enterprise", "title": "企业 / 分布式", "range": "事务 / 微服务 / 容错",
        "desc": "事务、集成与运维能力优先；不要只看语言语法。",
        "entries": [
            ("java", "Spring Boot", "企业后端与微服务"),
            ("java", "Quarkus", "云原生、快启动"),
            ("csharp", "ASP.NET Core", ".NET 企业栈"),
            ("erlang", "OTP", "容错与热升级"),
            ("elixir", "Phoenix", "实时 Web 与分布式"),
            ("scala", "Akka", "Actor 与集群"),
            ("go", "controller-runtime", "Kubernetes 控制面"),
        ],
    },
    {
        "key": "hardware-gpu", "title": "硬件 / GPU", "range": "芯片 / 并行",
        "desc": "仿真、综合、GPU 编程各有独立的产物链，不能套用软件框架思维。",
        "entries": [
            ("verilog", "UVM", "芯片验证方法学"),
            ("verilog", "Yosys", "开源综合"),
            ("cuda", "cuDNN", "深度学习 GPU 库"),
            ("cuda", "TensorRT", "推理优化"),
            ("glsl", "SPIRV-Tools", "着色器中间表示"),
        ],
    },
    {
        "key": "science", "title": "科学计算", "range": "数值 / 仿真 / 数据",
        "desc": "数值库、并行通信与数据格式往往比「框架」更重要。",
        "entries": [
            ("fortran", "LAPACK / BLAS", "线性代数底座"),
            ("fortran", "NetCDF", "科学数据格式"),
            ("matlab", "Simulink", "系统仿真"),
            ("julia", "DifferentialEquations.jl", "微分方程"),
            ("r", "RMarkdown", "可重复报告"),
            ("python", "PyTorch", "科学机器学习"),
        ],
    },
    {
        "key": "docs-config", "title": "文档 / 配置", "range": "站点 / 基础设施",
        "desc": "文档、样式与配置工具的关键是「人可读」与「工具可消费」。",
        "entries": [
            ("html", "Web Components", "原生跨框架组件"),
            ("css", "Tailwind CSS", "设计系统与样式"),
            ("markdown", "MDX", "组件化文档"),
            ("svg", "D3", "数据可视化"),
            ("yaml", "Kubernetes", "容器编排清单"),
            ("xml", "XSLT / XPath", "文档转换"),
            ("sass", "Dart Sass", "样式工程化"),
            ("less", "Less.js", "遗留样式编译"),
        ],
    },
]

# ------------------------------------------------------------------
# 矩阵补齐：把剩余卡片分配到场景；跨语言工具单独成组
# ------------------------------------------------------------------
_EXTRA = {
    "web-backend": [
        ("clojure", "Ring + Compojure", "中间件模型、极简路由"),
        ("go", "Echo", "轻量 API、文档友好"),
        ("java", "Jakarta EE", "企业规范、应用服务器"),
        ("julia", "Genie", "Julia 全栈 Web"),
        ("kotlin", "Ktor", "协程、Kotlin 原生"),
        ("perl", "Mojolicious", "现代 Perl Web、异步"),
        ("perl", "Catalyst", "传统 MVC、插件多"),
        ("perl", "Dancer", "轻量路由、类似 Sinatra"),
        ("php", "Symfony", "组件化、企业长期维护"),
        ("php", "WordPress", "CMS 与内容站"),
        ("python", "Flask", "微框架、自由组合"),
        ("ruby", "Sinatra", "极简 Ruby Web"),
        ("ruby", "Hanami", "模块化、清晰边界"),
        ("rust", "Actix Web", "高吞吐、成熟中间件"),
        ("scala", "Play", "异步全栈、Scala Web"),
        ("swift", "Vapor", "Swift 服务端"),
        ("fsharp", "Giraffe", "函数式 HTTP 组合"),
        ("fsharp", "Saturn", "F# MVC 全栈"),
        ("erlang", "Cowboy", "Erlang HTTP / WebSocket"),
        ("lua", "OpenResty", "Nginx + Lua 网关"),
        ("typescript", "tRPC", "端到端类型安全 API"),
    ],
    "web-frontend": [
        ("csharp", "Blazor", "C# 写 Web UI"),
        ("elixir", "LiveView", "服务端实时 UI"),
        ("fsharp", "Bolero", "F# + Blazor WASM"),
        ("javascript", "Next.js", "React 全栈 / SSR"),
        ("html", "Bootstrap", "组件与栅格"),
        ("css", "Bulma", "纯 CSS 框架"),
    ],
    "mobile": [
        ("swift", "UIKit", "成熟 iOS 控件与兼容性"),
    ],
    "desktop": [
        ("delphi", "FireMonkey", "跨平台 GUI"),
        ("delphi", "Lazarus LCL", "开源跨平台 GUI"),
        ("vb", "WPF（VB.NET）", "XAML 企业桌面"),
        ("vb", "VBA", "Office 自动化"),
        ("matlab", "App Designer", "工程工具界面"),
    ],
    "game": [
        ("c", "SDL2", "窗口、输入、音频与帧循环"),
    ],
    "data-ai": [
        ("clojure", "Datomic", "不可变数据库与时间旅行"),
        ("elixir", "Ecto", "Elixir 数据层"),
        ("sql", "Prisma", "TypeScript ORM"),
        ("sql", "SQLAlchemy", "Python ORM 与 SQL 工具"),
    ],
    "enterprise": [
        ("cobol", "CICS", "大型机在线事务"),
        ("cobol", "IMS", "层次数据库与事务"),
        ("cobol", "GnuCOBOL", "开源 COBOL 编译器"),
        ("kotlin", "Spring Boot", "Kotlin 企业后端"),
    ],
    "docs-config": [
        ("markdown", "CommonMark", "统一 Markdown 解析"),
        ("markdown", "Pandoc", "多格式文档转换"),
        ("sass", "Compass", "历史 Sass 工具集"),
        ("sass", "PostCSS", "CSS 后处理"),
        ("less", "PostCSS", "Less 之后的兼容处理"),
        ("svg", "SVGO", "SVG 压缩与清理"),
        ("svg", "Snap.svg", "SVG 动画与操作"),
        ("xml", "DOM / SAX", "树模型 / 流模型"),
        ("xml", "XSD", "XML 结构与类型校验"),
        ("yaml", "Docker Compose", "本地多容器编排"),
        ("yaml", "GitHub Actions", "仓库 CI/CD 工作流"),
    ],
    "tools": [
        ("cpp", "Boost", "准标准库、基础设施"),
        ("cpp", "POCO", "C++ 网络与服务端基础"),
        ("dart", "shelf", "Dart HTTP 中间件"),
        ("go", "gRPC-Go", "Protobuf RPC"),
        ("objectivec", "AFNetworking", "Objective-C 网络库"),
        ("shell", "bats", "Shell 脚本测试"),
        ("shell", "Ansible", "配置管理与自动化"),
        ("matlab", "MATLAB Compiler", "打包依赖 MCR 的应用"),
    ],
    "blockchain": [
        ("solidity", "OpenZeppelin", "审计过的合约库"),
        ("solidity", "Hardhat", "JS/TS 合约开发环境"),
        ("solidity", "Foundry", "Solidity 原生测试与部署"),
    ],
}

for _sc in SCENARIOS:
    _sc["entries"].extend(_EXTRA.get(_sc["key"], []))

SCENARIOS.extend([
    {
        "key": "tools", "title": "工具与生态", "range": "库 / RPC / 测试 / 自动化",
        "desc": "跨语言的通用库、RPC、测试与自动化工具；它们不是应用框架，但常与框架一起出现。",
        "entries": _EXTRA["tools"],
    },
    {
        "key": "blockchain", "title": "区块链 / 合约", "range": "EVM / 合约工具",
        "desc": "Solidity 合约库、开发环境与测试工具；与 Web 框架的选型逻辑不同，安全与审计优先。",
        "entries": _EXTRA["blockchain"],
    },
])

# 短页升级后的补充条目
_EXTRA2 = {
    "web-backend": [
        ("groovy", "Grails", "约定式全栈、GORM"),
        ("d", "vibe.d", "D 的异步 Web"),
        ("nim", "Jester", "Nim 轻量 Web"),
        ("crystal", "Lucky", "类型安全全栈"),
        ("crystal", "Kemal", "极简 API"),
        ("haskell", "Yesod", "类型安全全栈"),
        ("haskell", "Servant", "类型即 API 契约"),
        ("haskell", "Scotty", "Haskell 微框架"),
        ("ocaml", "Dream", "OCaml 现代 Web"),
        ("commonlisp", "Hunchentoot", "Lisp HTTP 服务器"),
        ("commonlisp", "Caveman2", "Lisp Web 应用骨架"),
        ("smalltalk", "Seaside", "组件与会话"),
    ],
    "web-frontend": [
        ("nim", "Karax", "Nim 写 SPA"),
    ],
    "tools": [
        ("groovy", "Spock", "JVM 行为测试"),
        ("groovy", "Gradle", "构建 DSL 与缓存"),
        ("d", "DUB", "D 包管理与构建"),
        ("nim", "Nimble", "Nim 包管理"),
        ("ocaml", "MirageOS", "unikernel 构建"),
        ("smalltalk", "Glamorous Toolkit", "可编程开发环境"),
    ],
}
for _sc in SCENARIOS:
    _sc["entries"].extend(_EXTRA2.get(_sc["key"], []))

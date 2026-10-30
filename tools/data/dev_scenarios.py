# -*- coding: utf-8 -*-
"""开发场景 → 架构模式 → 语言 / 框架。

条目为策展推荐；架构模式是选型视角，不是框架的官方分类。
安全场景的条目指向 security.html 的对应工具锚点。
"""

# 12 种统一架构模式：场景里的分组保留各自的焦点，但都归入这 12 种视角，
# 这样「架构筛选」在跨场景时才有可比性。
PATTERNS = [
    {"key": "layered", "title": "分层 / MVC", "desc": "请求 → 控制器 → 服务 → 数据层；约定清晰，适合大多数业务系统。"},
    {"key": "microservices", "title": "微服务 / 服务化", "desc": "按业务边界拆服务或模块，独立部署与团队自治优先，代价是运维与一致性。"},
    {"key": "event-driven", "title": "事件驱动 / Actor", "desc": "通过消息与事件解耦，或用 Actor 封装状态；适合实时、长流程与高并发。"},
    {"key": "component", "title": "组件化 / 响应式 UI", "desc": "以组件树组织界面，状态与副作用显式管理；声明式 UI 也归入这一类。"},
    {"key": "ssr", "title": "同构渲染 / SSR", "desc": "服务端渲染首屏，客户端接管交互；内容站与 SEO 敏感场景优先。"},
    {"key": "gateway", "title": "网关 / BFF", "desc": "统一入口、协议转换与接口聚合；让客户端只面对一个边界。"},
    {"key": "native", "title": "原生 / 平台绑定", "desc": "直接使用平台 API、控件或系统库；兼容性与系统能力最完整。"},
    {"key": "cross-platform", "title": "跨平台 / Web 外壳", "desc": "一套代码覆盖多平台，或以内嵌 Web 运行时承载界面；复用优先。"},
    {"key": "plugin", "title": "微内核 / 插件化", "desc": "核心保持小，能力通过插件或脚本扩展；适合编辑器、IDE 与平台型工具。"},
    {"key": "ecs", "title": "ECS / 数据导向", "desc": "按组件与系统组织数据，缓存友好；适合大量实体、数组式计算与数据并行。"},
    {"key": "pipeline", "title": "管线 / 批流", "desc": "分阶段转换与批流处理，强调可重跑、可测试与可观测。"},
    {"key": "control-plane", "title": "控制面 / 编排", "desc": "声明期望状态，由控制器收敛；适合基础设施、部署与升级流程。"},
]

PATTERN_BY_KEY = {p["key"]: p for p in PATTERNS}


SCENARIOS = [
    {
        "key": "backend", "title": "后端开发", "en": "Backend",
        "desc": "先确定团队规模、交付节奏与集成边界，再在分层、微服务与事件驱动之间选择。",
        "architectures": [
            {
                "key": "layered", "pattern": "layered",
                "title": "分层 / MVC", "desc": "请求 → 控制器 → 服务 → 数据层；约定清晰，适合大多数业务系统。",
                "entries": [
                    ("python", "Django", "全栈约定、ORM 与后台一体"),
                    ("java", "Spring Boot", "企业生态与招聘面最大"),
                    ("csharp", "ASP.NET Core", ".NET 企业栈、跨平台"),
                    ("ruby", "Rails", "约定优于配置、迭代快"),
                ],
            },
            {
                "key": "microservices", "pattern": "microservices",
                "title": "微服务", "desc": "按业务边界拆服务；独立部署与团队自治优先，代价是运维与一致性。",
                "entries": [
                    ("go", "Gin", "静态二进制、部署简单"),
                    ("typescript", "NestJS", "结构化、DI、适合大团队"),
                    ("java", "Quarkus", "云原生、快启动"),
                    ("kotlin", "Spring Boot", "Kotlin 企业后端"),
                ],
            },
            {
                "key": "event-driven", "pattern": "event-driven",
                "title": "事件驱动", "desc": "通过消息与事件解耦；适合实时、长流程与高并发场景。",
                "entries": [
                    ("elixir", "Phoenix", "实时与高并发"),
                    ("erlang", "OTP", "容错与热升级"),
                    ("scala", "Akka", "Actor 与集群"),
                    ("rust", "Axum", "类型安全与性能、生态较新"),
                ],
            },
        ],
    },
    {
        "key": "frontend", "title": "前端开发", "en": "Frontend",
        "desc": "组件化是默认起点；是否上 SSR、BFF 取决于首屏、SEO 与前后端协作方式。",
        "architectures": [
            {
                "key": "component", "pattern": "component",
                "title": "组件化 / 响应式", "desc": "以组件树组织 UI，状态与副作用显式管理；适合大多数交互应用。",
                "entries": [
                    ("javascript", "React", "生态最大、组件化"),
                    ("javascript", "Vue", "渐进式、模板直观"),
                    ("typescript", "Angular", "大型团队、DI 与约定"),
                    ("html", "Web Components", "原生跨框架组件"),
                ],
            },
            {
                "key": "ssr", "pattern": "ssr",
                "title": "SSR / 同构", "desc": "服务端渲染首屏，客户端接管交互；内容站与 SEO 敏感场景优先。",
                "entries": [
                    ("typescript", "Next.js", "全栈 React、SSR/SSG"),
                    ("javascript", "Next.js", "React 全栈 / SSR"),
                    ("csharp", "Blazor", "C# 写 Web UI"),
                    ("elixir", "LiveView", "服务端实时 UI"),
                ],
            },
            {
                "key": "bff", "pattern": "gateway",
                "title": "BFF / 全栈", "desc": "前后端共享类型与部署单元，减少接口往返；适合内部系统与单体团队。",
                "entries": [
                    ("typescript", "tRPC", "端到端类型安全 API"),
                    ("javascript", "Express", "Node 生态、上手快"),
                    ("fsharp", "Giraffe", "函数式 HTTP 组合"),
                    ("clojure", "Ring + Compojure", "中间件模型、极简路由"),
                ],
            },
        ],
    },
    {
        "key": "mobile", "title": "移动开发", "en": "Mobile",
        "desc": "原生能力、跨平台复用与 UI 一致性不可兼得；先确定平台优先级。",
        "architectures": [
            {
                "key": "declarative", "pattern": "component",
                "title": "声明式 UI", "desc": "用状态描述界面，框架负责差量更新；新项目的主流选择。",
                "entries": [
                    ("swift", "SwiftUI", "Apple 平台声明式 UI"),
                    ("kotlin", "Jetpack Compose", "Android 官方声明式 UI"),
                    ("dart", "Flutter", "一套代码跨移动/桌面/Web"),
                ],
            },
            {
                "key": "native", "pattern": "native",
                "title": "原生控件", "desc": "直接使用平台 API 与控件；兼容性与系统能力最完整。",
                "entries": [
                    ("swift", "UIKit", "成熟 iOS 控件与兼容性"),
                    ("java", "Android SDK", "Android 原生 API 与 Jetpack"),
                    ("objectivec", "Cocoa / Cocoa Touch", "维护旧 iOS/macOS 项目"),
                ],
            },
            {
                "key": "service", "pattern": "microservices",
                "title": "服务端配套", "desc": "为移动端提供 API、推送与同步；常与客户端同栈或同团队维护。",
                "entries": [
                    ("swift", "Vapor", "Swift 服务端"),
                    ("kotlin", "Ktor", "协程、Kotlin 原生"),
                    ("dart", "shelf", "Dart HTTP 中间件"),
                ],
            },
        ],
    },
    {
        "key": "desktop", "title": "桌面开发", "en": "Desktop",
        "desc": "原生控件、跨平台框架与 Web 外壳三条路线；看发布渠道与系统集成深度。",
        "architectures": [
            {
                "key": "native", "pattern": "native",
                "title": "原生控件", "desc": "使用平台原生控件与系统集成；体验最好，跨平台成本最高。",
                "entries": [
                    ("cpp", "Qt", "跨平台原生控件与工具链"),
                    ("csharp", "WPF", "Windows 企业桌面"),
                    ("c", "GTK", "Linux 原生桌面"),
                    ("delphi", "VCL", "Windows 快速桌面"),
                ],
            },
            {
                "key": "cross-platform", "pattern": "cross-platform",
                "title": "跨平台 GUI", "desc": "一套代码覆盖多平台；适合工具类与内部应用。",
                "entries": [
                    ("cpp", "Qt", "跨平台原生控件与工具链"),
                    ("delphi", "FireMonkey", "跨平台 GUI"),
                    ("delphi", "Lazarus LCL", "开源跨平台 GUI"),
                ],
            },
            {
                "key": "plugin", "pattern": "plugin",
                "title": "微内核 / 插件化", "desc": "核心保持小，能力通过插件扩展；适合编辑器、IDE 与平台型工具。",
                "entries": [
                    ("cpp", "Qt", "插件机制与跨平台"),
                    ("smalltalk", "Glamorous Toolkit", "可编程开发环境"),
                    ("rust", "Tauri", "Web 前端 + Rust 后端、体积小"),
                ],
            },
        ],
    },
    {
        "key": "game", "title": "游戏开发", "en": "Game",
        "desc": "引擎决定美术与工具链，脚本层决定迭代速度；先看团队与目标平台。",
        "architectures": [
            {
                "key": "engine", "pattern": "ecs",
                "title": "引擎驱动", "desc": "使用成熟引擎的渲染、物理与编辑器；把精力放在玩法与内容。",
                "entries": [
                    ("cpp", "Unreal Engine", "高端 3D 与完整工具链"),
                    ("csharp", "Unity", "跨平台与快速迭代"),
                    ("rust", "Bevy", "ECS、代码驱动"),
                ],
            },
            {
                "key": "ecs", "pattern": "ecs",
                "title": "ECS / 数据导向", "desc": "按组件与系统组织数据，缓存友好；适合大量实体与规则化玩法。",
                "entries": [
                    ("rust", "Bevy", "ECS、代码驱动"),
                    ("c", "SDL2", "窗口、输入、音频与帧循环"),
                    ("cpp", "Unreal Engine", "高端 3D 与完整工具链"),
                ],
            },
            {
                "key": "scripting", "pattern": "plugin",
                "title": "脚本层", "desc": "用脚本描述关卡、UI 与玩法；引擎宿主提供运行时与热更新。",
                "entries": [
                    ("lua", "LÖVE", "轻量 2D"),
                    ("lua", "Roblox", "平台化 UGC"),
                    ("c", "SDL2", "窗口、输入、音频与帧循环"),
                ],
            },
        ],
    },
    {
        "key": "data-ai", "title": "数据 / AI", "en": "Data & AI",
        "desc": "批处理、模型服务与实验是三套工具链；不要用一个框架硬套全流程。",
        "architectures": [
            {
                "key": "batch", "pattern": "pipeline",
                "title": "批处理 / 数仓", "desc": "按批次转换与建模，强调可重跑、可测试与血缘。",
                "entries": [
                    ("scala", "Apache Spark", "大规模数据处理"),
                    ("sql", "dbt", "数仓转换与测试"),
                    ("sql", "SQLAlchemy", "Python ORM 与 SQL 工具"),
                ],
            },
            {
                "key": "serving", "pattern": "microservices",
                "title": "模型服务", "desc": "把模型封装成 API，关注延迟、并发与版本回滚。",
                "entries": [
                    ("python", "FastAPI", "模型服务与 API"),
                    ("python", "Flask", "微框架、自由组合"),
                    ("julia", "Genie", "Julia 全栈 Web"),
                ],
            },
            {
                "key": "experiment", "pattern": "pipeline",
                "title": "实验 / 分析", "desc": "交互式探索与可重复分析；优先看库生态与可视化能力。",
                "entries": [
                    ("python", "PyTorch", "训练与研究的主流"),
                    ("julia", "Flux", "Julia 科学机器学习"),
                    ("r", "tidyverse", "数据整理与可视化"),
                ],
            },
        ],
    },
    {
        "key": "embedded", "title": "嵌入式 / IoT", "en": "Embedded & IoT",
        "desc": "资源、实时性与工具链成熟度优先；生态通常比语言特性更重要。",
        "architectures": [
            {
                "key": "rtos", "pattern": "native",
                "title": "RTOS / 实时调度", "desc": "任务、优先级与中断延迟是核心约束；不要套用通用服务端架构。",
                "entries": [
                    ("c", "FreeRTOS", "MCU 实时调度"),
                    ("ocaml", "MirageOS", "unikernel 构建"),
                    ("cpp", "Qt", "嵌入式 GUI"),
                ],
            },
            {
                "key": "gateway", "pattern": "gateway",
                "title": "网关 / 协议接入", "desc": "设备协议转换、消息路由与边缘缓存；强调稳定与可观测。",
                "entries": [
                    ("lua", "OpenResty", "Nginx + Lua 网关"),
                    ("go", "gRPC-Go", "Protobuf RPC"),
                    ("erlang", "Cowboy", "Erlang HTTP / WebSocket"),
                ],
            },
            {
                "key": "device-ui", "pattern": "component",
                "title": "设备 UI", "desc": "本地界面与远程控制并存；看屏幕资源与渲染能力。",
                "entries": [
                    ("cpp", "Qt", "嵌入式 GUI"),
                    ("c", "GTK", "Linux 原生桌面"),
                    ("c", "FreeRTOS", "MCU 实时调度"),
                ],
            },
        ],
    },
    {
        "key": "systems", "title": "系统与基础设施", "en": "Systems & Infra",
        "desc": "控制面、自动化与网关是三类不同工作；优先看可运维性与故障恢复。",
        "architectures": [
            {
                "key": "control-plane", "pattern": "control-plane",
                "title": "控制面 / 编排", "desc": "声明期望状态，由控制器收敛；Kubernetes 生态的默认模型。",
                "entries": [
                    ("go", "controller-runtime", "Kubernetes 控制面"),
                    ("yaml", "Kubernetes", "容器编排清单"),
                    ("go", "gRPC-Go", "Protobuf RPC"),
                ],
            },
            {
                "key": "automation", "pattern": "control-plane",
                "title": "自动化 / IaC", "desc": "用声明式配置描述基础设施与流程；可审计、可回滚优先。",
                "entries": [
                    ("shell", "Ansible", "配置管理与自动化"),
                    ("yaml", "GitHub Actions", "仓库 CI/CD 工作流"),
                    ("yaml", "Docker Compose", "本地多容器编排"),
                ],
            },
            {
                "key": "gateway", "pattern": "gateway",
                "title": "网关 / 可观测", "desc": "统一入口、限流与日志；强调低延迟与配置热更新。",
                "entries": [
                    ("lua", "OpenResty", "Nginx + Lua 网关"),
                    ("go", "Echo", "轻量 API、文档友好"),
                    ("go", "gRPC-Go", "Protobuf RPC"),
                ],
            },
        ],
    },
    {
        "key": "security", "title": "安全", "en": "Security",
        "desc": "安全贯穿应用、密码学与供应链；工具选型优先看默认安全、维护状态与合规要求。",
        "architectures": [
            {
                "key": "appsec", "pattern": "layered",
                "title": "应用安全", "desc": "认证授权、安全响应头与静态检查是应用层的第一道基线。",
                "entries": [
                    ("java", "Spring Security", "Spring 应用的认证与授权基线", "security.html#spring-security"),
                    ("javascript", "Helmet", "Node 服务安全响应头基线", "security.html#helmet"),
                    ("python", "Bandit", "Python 项目静态安全检查", "security.html#bandit"),
                ],
            },
            {
                "key": "crypto", "pattern": "native",
                "title": "密码学 / TLS", "desc": "选成熟库与安全默认值；不要自己发明密码学协议。",
                "entries": [
                    ("c", "OpenSSL", "TLS 与密码学基础库、生态最广", "security.html#openssl"),
                    ("c", "libsodium", "易用、默认安全的现代密码学库", "security.html#libsodium"),
                    ("rust", "rustls", "内存安全的 TLS 实现", "security.html#rustls"),
                    ("c", "GnuTLS", "LGPL 许可的 TLS / DTLS 实现", "security.html#gnutls"),
                    ("go", "age", "现代文件加密工具与格式", "security.html#age"),
                ],
            },
            {
                "key": "audit", "pattern": "pipeline",
                "title": "审计 / 供应链", "desc": "静态与动态扫描、镜像与依赖、策略与暴露面，构成持续审计链。",
                "entries": [
                    ("python", "Semgrep", "多语言静态审计、规则可读", "security.html#semgrep"),
                    ("go", "Trivy", "镜像、依赖与 IaC 漏洞扫描", "security.html#trivy"),
                    ("go", "Open Policy Agent", "策略即代码、统一授权", "security.html#opa"),
                    ("java", "OWASP ZAP", "Web 动态扫描与渗透辅助", "security.html#owasp-zap"),
                    ("java", "Keycloak", "自托管 IAM、OIDC / SAML 单点登录", "security.html#keycloak"),
                    ("go", "Nuclei", "模板化暴露面与漏洞扫描", "security.html#nuclei"),
                    ("python", "Slither", "Solidity 合约静态分析与审计辅助", "security.html#slither"),
                ],
            },
        ],
    },
    {
        "key": "blockchain", "title": "区块链 / 合约", "en": "Blockchain",
        "desc": "合约不可轻易修改；开发、测试与部署都要把审计与升级路径纳入设计。",
        "architectures": [
            {
                "key": "contract", "pattern": "native",
                "title": "合约开发", "desc": "用标准库与成熟模式实现代币、权限与升级；优先复用审计过的代码。",
                "entries": [
                    ("solidity", "OpenZeppelin", "审计过的合约库"),
                    ("solidity", "Foundry", "Solidity 原生测试与部署"),
                    ("solidity", "Hardhat", "JS/TS 合约开发环境"),
                ],
            },
            {
                "key": "testing", "pattern": "pipeline",
                "title": "测试与审计", "desc": "单元测试、模糊测试与静态分析组合使用；主网前必须独立审计。",
                "entries": [
                    ("solidity", "Foundry", "Solidity 原生测试与部署"),
                    ("solidity", "Hardhat", "JS/TS 合约开发环境"),
                    ("solidity", "OpenZeppelin", "审计过的合约库"),
                ],
            },
            {
                "key": "deploy", "pattern": "control-plane",
                "title": "部署与升级", "desc": "脚本化部署、验证源码与升级权限；把密钥与多签流程写进运维手册。",
                "entries": [
                    ("solidity", "Hardhat", "JS/TS 合约开发环境"),
                    ("solidity", "Foundry", "Solidity 原生测试与部署"),
                    ("solidity", "OpenZeppelin", "审计过的合约库"),
                ],
            },
        ],
    },
    {
        "key": "science", "title": "科学计算", "en": "Scientific Computing",
        "desc": "数值库、并行通信与数据格式往往比「框架」更重要；先确定精度与规模。",
        "architectures": [
            {
                "key": "numerical", "pattern": "ecs",
                "title": "数值内核", "desc": "线性代数、微分方程与并行通信；性能与数值稳定性优先。",
                "entries": [
                    ("fortran", "LAPACK / BLAS", "线性代数底座"),
                    ("fortran", "MPI", "HPC 多节点"),
                    ("julia", "DifferentialEquations.jl", "微分方程"),
                ],
            },
            {
                "key": "simulation", "pattern": "pipeline",
                "title": "仿真 / 数据", "desc": "系统仿真与科学数据格式；关注可复现与跨平台交换。",
                "entries": [
                    ("matlab", "Simulink", "系统仿真"),
                    ("fortran", "NetCDF", "科学数据格式"),
                    ("fortran", "MPI", "HPC 多节点"),
                ],
            },
            {
                "key": "reporting", "pattern": "pipeline",
                "title": "可重复报告", "desc": "代码、数据与图表同源；报告可重跑，结论可追溯。",
                "entries": [
                    ("r", "RMarkdown", "可重复报告"),
                    ("r", "Shiny", "数据应用与仪表盘"),
                    ("r", "tidyverse", "数据整理与可视化"),
                ],
            },
        ],
    },
    {
        "key": "hardware", "title": "硬件 / GPU", "en": "Hardware & GPU",
        "desc": "仿真、综合、GPU 编程各有独立的产物链，不能套用软件框架思维。",
        "architectures": [
            {
                "key": "rtl", "pattern": "pipeline",
                "title": "芯片 / RTL", "desc": "硬件描述、验证方法学与综合工具链；正确性验证占大头。",
                "entries": [
                    ("verilog", "UVM", "芯片验证方法学"),
                    ("verilog", "Yosys", "开源综合"),
                ],
            },
            {
                "key": "gpu", "pattern": "ecs",
                "title": "GPU 并行", "desc": "核函数、库与推理引擎；看显存、算力与目标硬件。",
                "entries": [
                    ("cuda", "cuDNN", "深度学习 GPU 库"),
                    ("cuda", "TensorRT", "推理优化"),
                ],
            },
            {
                "key": "shader", "pattern": "pipeline",
                "title": "图形 / 着色器", "desc": "着色器编译、中间表示与调试；跨 API 时优先 SPIR-V。",
                "entries": [
                    ("glsl", "SPIRV-Tools", "着色器中间表示"),
                    ("cuda", "TensorRT", "推理优化"),
                    ("cuda", "cuDNN", "深度学习 GPU 库"),
                ],
            },
        ],
    },
]
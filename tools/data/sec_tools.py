# -*- coding: utf-8 -*-
"""安全工具：渗透、网络、逆向、漏洞挖掘、移动固件与应急情报。

仅用于自有资产或取得书面授权的安全测试；条目是策展索引，许可与用法以官方文档为准。
"""

CATEGORIES = [
    {"key": "pentest", "title": "渗透测试", "desc": "侦察、验证与权限路径分析；范围与授权先于工具。"},
    {"key": "network", "title": "网络与流量", "desc": "抓包、协议构造、检测与无线审计。"},
    {"key": "reversing", "title": "逆向与二进制", "desc": "反汇编、调试与动态插桩。"},
    {"key": "vuln", "title": "漏洞挖掘", "desc": "覆盖率引导的模糊测试与崩溃分析。"},
    {"key": "mobile", "title": "移动与固件", "desc": "App 静态/动态分析与固件解包。"},
    {"key": "forensics", "title": "应急与情报", "desc": "内存取证、威胁情报与 IOC 管理。"},
]

TOOLS = [
    {
        "name": "Metasploit Framework", "slug": "metasploit", "cat": "pentest",
        "license": "BSD-3-Clause",
        "summary": "模块化的漏洞验证与利用框架，覆盖侦察、利用与后渗透模块。",
        "fit": ["授权渗透测试的漏洞验证", "红队演练中的稳定模块", "教学与靶场"],
        "avoid": ["未授权目标", "需要隐蔽对抗的实战"],
        "source": ("Metasploit 文档", "https://docs.metasploit.com/"),
    },
    {
        "name": "Burp Suite", "slug": "burp-suite", "cat": "pentest",
        "license": "商业（Community 免费 / Pro 订阅）",
        "summary": "Web 安全测试的集成平台：代理拦截、重放、扫描与扩展生态。",
        "fit": ["Web / API 手工测试", "授权扫描与复测", "团队协作与报告"],
        "avoid": ["只做自动化扫描的流水线", "无授权的目标"],
        "source": ("PortSwigger 文档", "https://portswigger.net/burp/documentation"),
    },
    {
        "name": "Nmap", "slug": "nmap", "cat": "pentest",
        "license": "NPSL",
        "summary": "端口与服务发现的事实标准，NSE 脚本可扩展资产与漏洞检查。",
        "fit": ["资产与暴露面盘点", "服务指纹识别", "授权扫描"],
        "avoid": ["未授权网段", "大规模高频扫描"],
        "source": ("Nmap 文档", "https://nmap.org/book/"),
    },
    {
        "name": "sqlmap", "slug": "sqlmap", "cat": "pentest",
        "license": "GPL-2.0",
        "summary": "自动化的 SQL 注入检测与利用工具，支持多种数据库与注入点。",
        "fit": ["授权测试中的注入验证", "参数点快速排查", "修复后复测"],
        "avoid": ["未授权扫描", "生产库上的高风险利用"],
        "source": ("sqlmap 文档", "https://github.com/sqlmapproject/sqlmap/wiki"),
    },
    {
        "name": "BloodHound", "slug": "bloodhound", "cat": "pentest",
        "license": "Apache-2.0",
        "summary": "用图数据库还原 Active Directory 的攻击路径，定位提权与横向风险。",
        "fit": ["AD 权限关系梳理", "红蓝共用的攻击面视图", "权限整改验证"],
        "avoid": ["非 AD 环境", "未授权采集"],
        "source": ("BloodHound 文档", "https://bloodhound.readthedocs.io/"),
    },
    {
        "name": "hashcat", "slug": "hashcat", "cat": "pentest",
        "license": "MIT",
        "summary": "GPU 加速的口令恢复工具，用于验证口令策略强度与离线破解风险。",
        "fit": ["授权评估口令策略", "离线哈希强度验证", "训练与靶场"],
        "avoid": ["在线撞库", "未授权哈希"],
        "source": ("hashcat 文档", "https://hashcat.net/wiki/"),
    },
    {
        "name": "Nuclei", "slug": "nuclei", "cat": "pentest",
        "license": "MIT",
        "summary": "基于 YAML 模板的漏洞与暴露面扫描器，模板可审计、可定制。",
        "fit": ["授权渗透测试", "资产暴露面检查", "自定义检测模板"],
        "avoid": ["未授权扫描", "需要深度利用链编排"],
        "source": ("Nuclei 文档", "https://docs.projectdiscovery.io/tools/nuclei/overview"),
    },
    {
        "name": "Wireshark", "slug": "wireshark", "cat": "network",
        "license": "GPL-2.0",
        "summary": "最常用的协议分析器，逐包解码并支持过滤、跟踪流与导出。",
        "fit": ["故障与安全事件排查", "协议学习", "取证中的流量证据"],
        "avoid": ["大规模长期采集", "加密载荷内容分析"],
        "source": ("Wireshark 文档", "https://www.wireshark.org/docs/"),
    },
    {
        "name": "Scapy", "slug": "scapy", "cat": "network",
        "license": "GPL-2.0",
        "summary": "Python 报文构造与收发库，适合自定义协议探测与测试脚本。",
        "fit": ["协议探测与测试", "自定义包构造", "安全自动化脚本"],
        "avoid": ["高性能转发", "生产流量镜像"],
        "source": ("Scapy 文档", "https://scapy.readthedocs.io/"),
    },
    {
        "name": "Suricata", "slug": "suricata", "cat": "network",
        "license": "GPL-2.0",
        "summary": "多线程的入侵检测与防御引擎，支持规则、协议解析与流日志。",
        "fit": ["边界与内网检测", "规则化告警", "与日志平台联动"],
        "avoid": ["只做离线协议分析", "没有规则维护能力的团队"],
        "source": ("Suricata 文档", "https://docs.suricata.io/"),
    },
    {
        "name": "Aircrack-ng", "slug": "aircrack-ng", "cat": "network",
        "license": "GPL-2.0",
        "summary": "无线网络审计工具集，覆盖抓包、握手捕获与口令强度验证。",
        "fit": ["自有无线网络的授权评估", "WPA 口令强度验证", "无线覆盖排查"],
        "avoid": ["非自有或未授权网络", "生产无线环境的干扰性测试"],
        "source": ("Aircrack-ng 文档", "https://www.aircrack-ng.org/doku.php"),
    },
    {
        "name": "Ghidra", "slug": "ghidra", "cat": "reversing",
        "license": "Apache-2.0",
        "summary": "开源逆向平台，提供反汇编、反编译、脚本扩展与协作分析。",
        "fit": ["二进制与固件分析", "恶意样本研判", "无预算团队的逆向基线"],
        "avoid": ["需要商业级调试集成", "超大工程的首选性能"],
        "source": ("Ghidra 仓库与文档", "https://github.com/NationalSecurityAgency/ghidra"),
    },
    {
        "name": "IDA Pro", "slug": "ida-pro", "cat": "reversing",
        "license": "商业",
        "summary": "商业逆向工程的事实标准，反编译、调试与插件生态成熟。",
        "fit": ["深度逆向与漏洞分析", "恶意样本长期研究", "团队协作"],
        "avoid": ["预算受限", "仅需快速字符串与结构概览"],
        "source": ("IDA 文档", "https://docs.hex-rays.com/"),
    },
    {
        "name": "Frida", "slug": "frida", "cat": "reversing",
        "license": "wxWindows",
        "summary": "跨平台动态插桩框架，可在运行中 Hook 函数、读写内存与跟踪调用。",
        "fit": ["移动与桌面 App 的动态分析", "自研程序的可观测性", "授权测试"],
        "avoid": ["未授权第三方 App", "强反调试环境下的稳定使用"],
        "source": ("Frida 文档", "https://frida.re/docs/"),
    },
    {
        "name": "AFL++", "slug": "aflplusplus", "cat": "vuln",
        "license": "AGPL-3.0（运行库 Apache-2.0）",
        "summary": "覆盖率引导的模糊测试器，配合消毒器可高效发现内存与解析类缺陷。",
        "fit": ["解析器与文件格式", "C/C++ 库与协议实现", "CI 中的定向 Fuzz"],
        "avoid": ["无源码且无插桩条件的闭源目标", "需要快速出结果的场景"],
        "source": ("AFL++ 文档", "https://aflplus.plus/docs/"),
    },
    {
        "name": "libFuzzer", "slug": "libfuzzer", "cat": "vuln",
        "license": "Apache-2.0（LLVM 例外）",
        "summary": "LLVM 生态的进程内覆盖率引导 Fuzzer，写一个入口函数即可接入。",
        "fit": ["C/C++ 库函数级 Fuzz", "与 sanitizer 组合", "回归测试"],
        "avoid": ["需要跨进程隔离的复杂目标", "无 LLVM 工具链的环境"],
        "source": ("libFuzzer 文档", "https://llvm.org/docs/LibFuzzer.html"),
    },
    {
        "name": "MobSF", "slug": "mobsf", "cat": "mobile",
        "license": "GPL-3.0",
        "summary": "移动应用安全测试平台，集成静态分析、动态分析与报告。",
        "fit": ["Android / iOS App 授权评估", "上线前安全基线", "报告输出"],
        "avoid": ["未授权 App", "需要深度定制逆向的场景"],
        "source": ("MobSF 文档", "https://mobsf.github.io/docs/"),
    },
    {
        "name": "binwalk", "slug": "binwalk", "cat": "mobile",
        "license": "MIT",
        "summary": "固件与二进制镜像的签名识别与文件系统提取工具。",
        "fit": ["IoT 固件解包", "镜像结构识别", "取证辅助"],
        "avoid": ["加密固件（需先处理密钥）", "大型镜像的完整还原"],
        "source": ("binwalk 文档", "https://github.com/ReFirmLabs/binwalk"),
    },
    {
        "name": "Volatility", "slug": "volatility", "cat": "forensics",
        "license": "Volatility Software License 1.0",
        "summary": "内存镜像分析框架，提取进程、网络连接、注入代码与凭据痕迹。",
        "fit": ["事件响应中的内存取证", "恶意软件驻留分析", "取证报告"],
        "avoid": ["无镜像的纯主机排查", "不支持的符号表版本"],
        "source": ("Volatility 文档", "https://volatility3.readthedocs.io/"),
    },
    {
        "name": "MISP", "slug": "misp", "cat": "forensics",
        "license": "AGPL-3.0",
        "summary": "开源威胁情报平台，用于 IOC、事件与关联信息的共享和交换。",
        "fit": ["团队 / 行业情报共享", "IOC 管理与分发", "事件关联"],
        "avoid": ["单人一次性查询", "需要商业情报源覆盖"],
        "source": ("MISP 文档", "https://www.misp-project.org/documentation/"),
    },
]

CAT_BY_KEY = {c["key"]: c for c in CATEGORIES}
BY_CAT = {}
for _t in TOOLS:
    BY_CAT.setdefault(_t["cat"], []).append(_t)
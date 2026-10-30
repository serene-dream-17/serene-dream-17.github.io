# -*- coding: utf-8 -*-
"""归档：第 23 批删除的开发场景「安全」分组。"""

    {
        "key": "security", "title": "安全", "en": "Security",
        "desc": "安全贯穿应用、密码学、攻防与供应链；工具选型优先看默认安全、授权边界与合规要求。",
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
                "key": "offense", "pattern": "pipeline",
                "title": "攻防与渗透", "desc": "侦察、验证、逆向与漏洞挖掘；只在自有资产或书面授权范围内使用。",
                "entries": [
                    ("ruby", "Metasploit Framework", "授权渗透的漏洞验证框架", "security.html#metasploit"),
                    ("java", "Burp Suite", "Web / API 渗透测试工作台", "security.html#burp-suite"),
                    ("java", "Ghidra", "二进制与固件反编译", "security.html#ghidra"),
                    ("c", "AFL++", "覆盖率引导的漏洞挖掘", "security.html#aflplusplus"),
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

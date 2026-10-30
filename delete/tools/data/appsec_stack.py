# -*- coding: utf-8 -*-
"""归档：第 24 批删除的应用安全基线栈（原 stacks.py）。"""

    {
        "key": "appsec-baseline",
        "title": "应用安全基线",
        "domain": "security",
        "summary": "在业务栈上补齐认证、授权、HTTP 安全头与依赖审计，形成可重复的安全基线。",
        "layers": [
            {"role": "语言", "items": [("java", "Java")]},
            {"role": "框架", "items": [("java", "Spring Boot")]},
            {"role": "认证", "items": ["Spring Security", "Keycloak"]},
            {"role": "策略", "items": ["Open Policy Agent"]},
        ],
        "fit": ["企业业务系统", "统一登录与授权", "合规与审计"],
        "avoid": ["极小内部工具", "没有身份治理需求"],
        "layout": ["security/ 配置", "auth/ 认证", "policies/ 策略", "ci/ 扫描流水线"],
        "alternatives": ["spring-enterprise"],
        "scenarios": ["security"],
        "source": ("OWASP ASVS", "https://owasp.org/www-project-application-security-verification-standard/"),
    },

    # ---------------- 区块链 ----------------

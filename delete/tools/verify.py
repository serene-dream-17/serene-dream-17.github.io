# -*- coding: utf-8 -*-
"""本机实测：对可用工具链运行 Hello 产物链，写入 data/verified.py。

用法：python tools/verify.py

原则：只记录本机真正跑通的项；失败/未安装的语言不写入。
Windows 上 gcc 生成 PE/COFF，不会伪装成 ELF。
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))


def run(cmd, cwd, timeout=120):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       timeout=timeout, shell=False)
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


def first_bytes(path, n=4):
    try:
        with open(path, "rb") as f:
            return f.read(n).hex(" ")
    except OSError:
        return ""


def version(*cmd):
    try:
        rc, out, err = run(list(cmd), ROOT)
        text = (out or err).splitlines()[0] if (out or err) else ""
        return text.strip()
    except Exception:
        return ""


def verify_c(work):
    gcc = shutil.which("gcc") or "gcc"
    src = Path(work) / "hello.c"
    src.write_text('#include <stdio.h>\nint main(void){printf("Hello, world\\n");return 0;}\n', encoding="utf-8")
    rc, out, err = run([gcc, "-O0", "hello.c", "-o", "hello.exe"], work)
    if rc != 0:
        raise RuntimeError(err[:200])
    rc2, run_out, run_err = run([str(Path(work) / "hello.exe")], work)
    if rc2 != 0 or "Hello, world" not in run_out:
        raise RuntimeError(run_err[:200] or "no output")
    rc3, _, _ = run([gcc, "-c", "hello.c", "-o", "hello.o"], work)
    obj = Path(work) / "hello.o"
    exe = Path(work) / "hello.exe"
    return {
        "tool": version(gcc, "--version"),
        "command": "gcc -O0 hello.c -o hello.exe && hello.exe",
        "output": run_out,
        "artifacts": [
            f"hello.exe · {exe.stat().st_size} B · 首字节 {first_bytes(exe)}",
            f"hello.o · {obj.stat().st_size} B · 首字节 {first_bytes(obj)}" if rc3 == 0 else "hello.o 未生成",
        ],
        "note": "本机为 Windows/MinGW，目标格式是 PE/COFF；页面中的 ELF 样例是 Linux 口径。",
    }


def verify_cpp(work):
    gpp = shutil.which("g++") or "g++"
    src = Path(work) / "hello.cpp"
    src.write_text('#include <iostream>\nint main(){std::cout << "Hello, world\\n";}\n', encoding="utf-8")
    rc, out, err = run([gpp, "-O0", "hello.cpp", "-o", "hello.exe"], work)
    if rc != 0:
        raise RuntimeError(err[:200])
    rc2, run_out, run_err = run([str(Path(work) / "hello.exe")], work)
    if rc2 != 0 or "Hello, world" not in run_out:
        raise RuntimeError(run_err[:200] or "no output")
    exe = Path(work) / "hello.exe"
    return {
        "tool": version(gpp, "--version"),
        "command": "g++ -O0 hello.cpp -o hello.exe && hello.exe",
        "output": run_out,
        "artifacts": [f"hello.exe · {exe.stat().st_size} B · 首字节 {first_bytes(exe)}"],
        "note": "Windows/MinGW 生成 PE；与页面中的 Linux ELF 阶段对应，但目标格式不同。",
    }


def verify_python(work):
    src = Path(work) / "hello.py"
    src.write_text('print("Hello, world")\n', encoding="utf-8")
    rc, out, err = run([sys.executable, "hello.py"], work)
    if rc != 0:
        raise RuntimeError(err[:200])
    rc2, _, _ = run([sys.executable, "-m", "py_compile", "hello.py"], work)
    pyc = next(Path(work).glob("__pycache__/*.pyc"), None)
    return {
        "tool": version(sys.executable, "--version"),
        "command": "python hello.py && python -m py_compile hello.py",
        "output": out,
        "artifacts": [
            f"__pycache__/{pyc.name} · {pyc.stat().st_size} B · 魔数 {first_bytes(pyc, 4)}"
            if pyc else "未生成 .pyc",
        ],
        "note": ".pyc 的魔数与解释器版本绑定，跨版本不兼容。",
    }


def verify_javascript(work):
    src = Path(work) / "hello.js"
    src.write_text('console.log("Hello, world");\n', encoding="utf-8")
    rc, out, err = run(["node", "hello.js"], work)
    if rc != 0:
        raise RuntimeError(err[:200])
    return {
        "tool": version("node", "--version"),
        "command": "node hello.js",
        "output": out,
        "artifacts": ["源码直接由 V8 解析执行；本机未落盘字节码。"],
        "note": "V8 的字节码是内存中的实现细节，不是可分发文件。",
    }


def verify_java(work):
    src = Path(work) / "Hello.java"
    src.write_text('public class Hello { public static void main(String[] a){ System.out.println("Hello, world"); } }\n', encoding="utf-8")
    rc, out, err = run(["javac", "Hello.java"], work)
    if rc != 0:
        raise RuntimeError(err[:200])
    rc2, run_out, run_err = run(["java", "Hello"], work)
    if rc2 != 0:
        raise RuntimeError(run_err[:200])
    cls = Path(work) / "Hello.class"
    return {
        "tool": version("javac", "-version"),
        "command": "javac Hello.java && java Hello",
        "output": run_out,
        "artifacts": [f"Hello.class · {cls.stat().st_size} B · 魔数 {first_bytes(cls, 4)}"],
        "note": "CAFEBABE 魔数与常量池可在 .class 中直接验证。",
    }


def verify_csharp(work):
    src = Path(work) / "hello.cs"
    src.write_text('Console.WriteLine("Hello, world");\n', encoding="utf-8")
    rc, out, err = run(["dotnet", "run", "hello.cs"], work, timeout=180)
    if rc != 0 or "Hello, world" not in out:
        raise RuntimeError((err or out)[:200])
    return {
        "tool": version("dotnet", "--version"),
        "command": "dotnet run hello.cs",
        "output": "Hello, world",
        "artifacts": ["文件式程序由 .NET SDK 编译并执行；本机未保留中间程序集。"],
        "note": "页面中的 CIL/程序集阶段由 Roslyn 与 CLR 完成；这里验证的是源码到运行结果。",
    }


def verify_shell(work):
    src = Path(work) / "hello.sh"
    src.write_text('#!/bin/sh\nprintf "Hello, world\\n"\n', encoding="utf-8")
    bash = shutil.which("bash") or "bash"
    rc, out, err = run([bash, "hello.sh"], work)
    if rc != 0:
        raise RuntimeError(err[:200])
    return {
        "tool": version(bash, "--version"),
        "command": "bash hello.sh",
        "output": out,
        "artifacts": ["脚本直接由 shell 解析；无目标文件。"],
        "note": "Shell 没有编译产物；解析、展开与 execve 是可观察的中间层。",
    }


def verify_sql(work):
    import sqlite3
    con = sqlite3.connect(":memory:")
    out = con.execute("select 'Hello, world'").fetchone()[0]
    con.close()
    return {
        "tool": f"sqlite3 {sqlite3.sqlite_version}（Python {sys.version.split()[0]}）",
        "command": "SELECT 'Hello, world';",
        "output": out,
        "artifacts": ["内存数据库；查询计划与结果集由 SQLite 生成。"],
        "note": "SQL 的产物是结果集与执行计划，不是可执行文件。",
    }


def verify_html(work):
    from playwright.sync_api import sync_playwright
    src = Path(work) / "hello.html"
    src.write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>Hello</title></head><body><p>Hello, world</p></body></html>', encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        pg = b.new_page()
        pg.goto(src.as_uri())
        text = pg.inner_text("body")
        nodes = pg.evaluate("document.querySelectorAll('*').length")
        ver = b.version
        b.close()
    return {
        "tool": f"Chromium {ver}",
        "command": "在浏览器中打开 hello.html",
        "output": text,
        "artifacts": [f"DOM 元素 {nodes} 个；渲染树/布局/绘制由浏览器完成。"],
        "note": "HTML 的产物是 DOM 与像素，不是文件。",
    }


def verify_css(work):
    from playwright.sync_api import sync_playwright
    html = Path(work) / "hello.html"
    css = Path(work) / "hello.css"
    html.write_text('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><link rel="stylesheet" href="hello.css"><title>Hello</title></head><body><p class="g">Hello</p></body></html>', encoding="utf-8")
    css.write_text('.g::before { content: "Hello, world"; color: rgb(140, 51, 36); }\n', encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        pg = b.new_page()
        pg.goto(html.as_uri())
        content = pg.eval_on_selector(".g", "e => getComputedStyle(e, '::before').content")
        color = pg.eval_on_selector(".g", "e => getComputedStyle(e, '::before').color")
        ver = b.version
        b.close()
    return {
        "tool": f"Chromium {ver}",
        "command": "打开 hello.html，读取 getComputedStyle(.g, '::before')",
        "output": f"content: {content} · color: {color}",
        "artifacts": ["CSSOM 与计算样式由浏览器生成；没有目标文件。"],
        "note": "CSS 的产物是计算样式与像素。",
    }



def verify_fortran(work):
    gfortran = shutil.which("gfortran") or "gfortran"
    src = Path(work) / "hello.f90"
    src.write_text('program hello\n  implicit none\n  write (*, "(A)") "Hello, world"\nend program hello\n', encoding="utf-8")
    rc, out, err = run([gfortran, "-O0", "hello.f90", "-o", "hello.exe"], work)
    if rc != 0:
        raise RuntimeError(err[:200])
    rc2, run_out, run_err = run([str(Path(work) / "hello.exe")], work)
    if rc2 != 0 or "Hello, world" not in run_out:
        raise RuntimeError(run_err[:200] or "no output")
    rc3, _, _ = run([gfortran, "-c", "hello.f90", "-o", "hello.o"], work)
    obj = Path(work) / "hello.o"
    exe = Path(work) / "hello.exe"
    return {
        "tool": version(gfortran, "--version"),
        "command": "gfortran -O0 hello.f90 -o hello.exe && hello.exe",
        "output": run_out,
        "artifacts": [
            f"hello.o · {obj.stat().st_size} B · 首字节 {first_bytes(obj)}" if rc3 == 0 else "hello.o 未生成",
            f"hello.exe · {exe.stat().st_size} B · 首字节 {first_bytes(exe)}",
        ],
        "note": "Windows/MinGW 生成 PE/COFF；页面中的 ELF 样例是 Linux 口径。",
    }


def verify_go(work):
    src = Path(work) / "hello.go"
    src.write_text('package main\nimport "fmt"\nfunc main() { fmt.Println("Hello, world") }\n', encoding="utf-8")
    rc, out, err = run(["go", "run", "hello.go"], work, timeout=180)
    if rc != 0 or "Hello, world" not in out:
        raise RuntimeError((err or out)[:200])
    rc2, _, _ = run(["go", "build", "-o", "hello.exe", "hello.go"], work, timeout=180)
    exe = Path(work) / "hello.exe"
    mod = ""
    if exe.exists():
        _, mout, _ = run(["go", "version", "-m", "hello.exe"], work)
        mod = mout.splitlines()[0] if mout else ""
    return {
        "tool": version("go", "version"),
        "command": "go run hello.go && go build -o hello.exe hello.go",
        "output": out,
        "artifacts": [
            f"hello.exe · {exe.stat().st_size} B · 首字节 {first_bytes(exe)}" if exe.exists() else "hello.exe 未生成",
            mod or "go version -m 未读取",
        ],
        "note": "Go 默认静态链接运行时与标准库；Windows 目标为 PE，Linux 目标为 ELF。",
    }


def verify_xml(work):
    from lxml import etree
    src = Path(work) / "hello.xml"
    src.write_text('<?xml version="1.0" encoding="UTF-8"?>\n<greeting lang="zh"><text>Hello, world</text></greeting>\n', encoding="utf-8")
    tree = etree.parse(str(src))
    root = tree.getroot()
    text = root.findtext("text")
    nodes = sum(1 for _ in root.iter())
    serialized = etree.tostring(root, encoding="unicode")
    return {
        "tool": f"lxml {etree.LXML_VERSION[0]}.{etree.LXML_VERSION[1]}.{etree.LXML_VERSION[2]}",
        "command": "lxml.etree.parse('hello.xml')",
        "output": text,
        "artifacts": [f"根元素 {root.tag}，节点 {nodes} 个，序列化长度 {len(serialized)} 字符"],
        "note": "XML 的产物是 DOM/元素树与应用数据；这里验证解析与取值。",
    }


def verify_yaml(work):
    import yaml
    src = Path(work) / "hello.yaml"
    src.write_text("message: Hello, world\nservice:\n  name: hello\n  replicas: 1\n", encoding="utf-8")
    data = yaml.safe_load(src.read_text(encoding="utf-8"))
    import json
    return {
        "tool": f"PyYAML {yaml.__version__}",
        "command": "yaml.safe_load(hello.yaml)",
        "output": data["message"],
        "artifacts": [f"解析为对象：{json.dumps(data, ensure_ascii=False)}"],
        "note": "YAML 本身不执行；产物是被工具消费的数据对象。",
    }


def verify_sass(work):
    sass = shutil.which("sass") or "sass"
    src = Path(work) / "hello.scss"
    src.write_text('$message: "Hello, world";\n.greeting::before { content: $message; }\n', encoding="utf-8")
    rc, out, err = run([sass, "hello.scss", "hello.css"], work, timeout=120)
    if rc != 0:
        raise RuntimeError(err[:200])
    css = Path(work) / "hello.css"
    body = css.read_text(encoding="utf-8").strip()
    return {
        "tool": version(sass, "--version"),
        "command": "sass hello.scss hello.css",
        "output": body,
        "artifacts": [f"hello.css · {css.stat().st_size} B", f"编译结果：{body}"],
        "note": "Sass 的产物是普通 CSS；浏览器不需要 Sass 运行时。",
    }


def verify_svg(work):
    from playwright.sync_api import sync_playwright
    src = Path(work) / "hello.svg"
    src.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="320" height="80" viewBox="0 0 320 80"><rect width="320" height="80" fill="#f3ede1"/><text x="16" y="48" font-size="24" fill="#1c1a16">Hello, world</text></svg>', encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        pg = b.new_page()
        pg.goto(src.as_uri())
        shapes = pg.evaluate("document.querySelectorAll('svg *').length")
        text = pg.evaluate("document.querySelector('svg').textContent.trim()")
        ver = b.version
        b.close()
    return {
        "tool": f"Chromium {ver}",
        "command": "在浏览器中打开 hello.svg",
        "output": text,
        "artifacts": [f"SVG 子元素 {shapes} 个；矢量图元由浏览器栅格化。"],
        "note": "SVG 的产物是 DOM/场景图与像素。",
    }

CHECKS = {
    "c": verify_c,
    "cpp": verify_cpp,
    "python": verify_python,
    "javascript": verify_javascript,
    "java": verify_java,
    "csharp": verify_csharp,
    "shell": verify_shell,
    "sql": verify_sql,
    "html": verify_html,
    "css": verify_css,
    "fortran": verify_fortran,
    "go": verify_go,
    "xml": verify_xml,
    "yaml": verify_yaml,
    "sass": verify_sass,
    "svg": verify_svg,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("langs", nargs="*", help="只验证指定语言；省略则全部")
    parser.add_argument("--merge", action="store_true", help="与已有 verified.py 合并，不覆盖其它项")
    args = parser.parse_args()

    results = {}
    out = ROOT / "tools" / "data" / "verified.py"
    if args.merge and out.exists():
        ns = {}
        exec(out.read_text(encoding="utf-8"), ns)
        results.update(ns.get("VERIFIED", {}))

    only = args.langs or list(CHECKS)
    for slug in only:
        fn = CHECKS.get(slug)
        if not fn:
            print("skip unknown", slug)
            continue
        work = tempfile.mkdtemp(prefix=f"verify_{slug}_")
        try:
            info = fn(work)
            info["date"] = "2026-10-28"
            results[slug] = info
            print("OK", slug, "·", info["tool"], "·", info["output"][:40])
        except Exception as e:
            print("FAIL", slug, type(e).__name__, str(e)[:120])
        finally:
            shutil.rmtree(work, ignore_errors=True)

    out = ROOT / "tools" / "data" / "verified.py"
    body = "# 由 tools/verify.py 生成；只包含本机真正跑通的条目。\n\nVERIFIED = " + \
        json.dumps(results, ensure_ascii=False, indent=2) + "\n"
    out.write_text(body, encoding="utf-8")
    print("wrote", out, "items", len(results))


if __name__ == "__main__":
    main()

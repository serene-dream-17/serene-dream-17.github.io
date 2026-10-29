# -*- coding: utf-8 -*-
"""全站冒烟测试：结构、交互、移动端、打印。

用法：
    python tests/smoke.py
    python tests/smoke.py --quick     # 跳过 163 页全量扫描

依赖：playwright（已安装），Chrome。可用 CHROME_PATH 指定浏览器。
"""

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHROME = os.environ.get(
    "CHROME_PATH", r"C:\Program Files\Google\Chrome\Application\chrome.exe"
)

PASS = []
FAIL = []


def check(name, fn):
    try:
        fn()
        PASS.append(name)
        print("PASS", name)
    except Exception as e:
        FAIL.append((name, str(e)))
        print("FAIL", name, "·", str(e)[:200])


def assert_(cond, msg):
    if not cond:
        raise AssertionError(msg)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="跳过全量页面扫描")
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        print("需要 playwright：pip install playwright")
        return 2

    if not Path(CHROME).exists():
        print("找不到 Chrome：", CHROME)
        return 2

    pages = [ROOT / "index.html", ROOT / "frameworks.html",
             ROOT / "sources.html", ROOT / "formats.html",
             ROOT / "lineage.html", ROOT / "compare.html", ROOT / "verified.html",
             ROOT / "security.html", ROOT / "scenarios.html",
             ROOT / "404.html"]
    pages += sorted((ROOT / "langs").glob("*.html"))

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME)
        ctx = browser.new_context(viewport={"width": 1440, "height": 1000})
        page = ctx.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append("pageerror: " + str(e)))
        page.on("console", lambda m: errors.append("console: " + m.text)
                if m.type == "error" else None)

        if not args.quick:
            check("页面扫描（%d 页）" % len(pages), lambda: sweep(page, pages, errors))
        check("首页搜索与 URL", lambda: index_test(page))
        check("矩阵筛选与 URL", lambda: matrix_test(page))
        check("开发场景筛选与 URL", lambda: scenarios_test(page))
        check("安全工具筛选与 URL", lambda: security_test(page))
        check("来源搜索", lambda: sources_test(page))
        check("格式搜索", lambda: formats_test(page))
        check("对比器预设与恢复", lambda: compare_test(page))
        check("谱系筛选与悬停", lambda: lineage_test(page))
        check("实测覆盖表", lambda: verified_test(page))
        check("字体控制器持久化", lambda: font_test(page))
        check("命令面板键盘", lambda: cmdk_test(page))
        check("打印样式", lambda: print_test(page))

        mobile = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
        m = mobile.new_page()
        check("移动端无溢出与搜索入口", lambda: mobile_test(m))
        check("移动端抽屉焦点", lambda: drawer_test(m))

        browser.close()

    print()
    print("通过 %d · 失败 %d" % (len(PASS), len(FAIL)))
    if FAIL:
        for name, err in FAIL:
            print(" -", name, ":", err)
        return 1
    return 0


def sweep(page, pages, errors):
    for path in pages:
        rel = path.relative_to(ROOT).as_posix()
        errors.clear()
        page.goto(path.as_uri())
        page.wait_for_timeout(18)
        assert_(not errors, f"{rel} 有 JS 错误：{errors[:2]}")

        h1 = page.eval_on_selector_all("h1", "els => els.length")
        assert_(h1 == 1, f"{rel} h1={h1}")

        over = page.evaluate(
            "document.documentElement.scrollWidth - document.documentElement.clientWidth"
        )
        assert_(over <= 0, f"{rel} 横向溢出 {over}px")

        if "data-cmdk" not in page.content():
            raise AssertionError(f"{rel} 缺少全站搜索按钮")

        if path.parent.name == "langs" and not path.stem.endswith("-frameworks"):
            assert_(page.locator(".deep-feature").count() == 4, f"{rel} 深读特性不足")
            assert_(page.locator(".tag--verified").count()
                    + page.locator(".tag--level").count() >= 1,
                    f"{rel} 缺少内容等级")
            assert_(page.locator(".sources").count() == 1, f"{rel} 缺少参考来源")
        elif path.parent.name == "langs" and path.stem.endswith("-frameworks"):
            cards = page.locator(".fw-card").count()
            if cards:
                assert_(page.locator(".fw-source").count() == cards,
                        f"{rel} 来源数与卡片数不一致")
                assert_(page.locator(".fw-badge").count() == cards * 3,
                        f"{rel} 徽章数异常")
            assert_(page.locator(".tag--level").count() >= 1,
                    f"{rel} 缺少编者判断标签")


def index_test(page):
    page.goto((ROOT / "index.html").as_uri())
    page.wait_for_timeout(120)
    page.fill("#indexSearch", "rust")
    page.wait_for_timeout(120)
    assert_("q=rust" in page.url, "搜索未写入 URL")
    assert_(page.locator(".lang-card:not([hidden])").count() >= 1, "未搜到 Rust")
    page.click('.index-filters .filter[data-filter="interpreted"]')
    page.wait_for_timeout(120)
    assert_("f=interpreted" in page.url, "筛选未写入 URL")
    page.click('.index-filters .filter[data-filter="all"]')
    page.fill("#indexSearch", "")
    page.wait_for_timeout(100)


def matrix_test(page):
    page.goto((ROOT / "frameworks.html").as_uri())
    page.wait_for_timeout(120)
    page.fill("#matrixSearch", "rust")
    page.select_option("#matrixScenario", "game")
    page.wait_for_timeout(150)
    assert_("q=rust" in page.url and "s=game" in page.url, "矩阵 URL 状态缺失")
    shown = page.locator(".stack-card:not([hidden])").count()
    assert_(shown >= 1, "矩阵未显示结果")
    page.fill("#matrixSearch", "")
    page.select_option("#matrixScenario", "security")
    page.wait_for_timeout(120)
    sec_cards = page.locator('#security .stack-card:not([hidden])').count()
    assert_(sec_cards >= 10, f"安全场景条目不足 {sec_cards}")
    href = page.get_attribute('#security .stack-card', "href")
    assert_(href.startswith("security.html#"), f"安全场景链接异常 {href}")


def scenarios_test(page):
    page.goto((ROOT / "scenarios.html").as_uri())
    page.wait_for_timeout(150)
    assert_(page.locator(".dev-section").count() == 12, "开发场景不是 12 个")
    assert_(page.locator(".dev-card").count() >= 100, "开发场景推荐组不足")
    page.fill("#devSearch", "微服务")
    page.select_option("#devScenario", "backend")
    page.wait_for_timeout(150)
    assert_("q=" in page.url and "s=backend" in page.url, "开发场景 URL 状态缺失")
    assert_(page.locator(".dev-card:not([hidden])").count() >= 1, "开发场景未显示结果")
    page.fill("#devSearch", "")
    page.wait_for_timeout(120)
    page.select_option("#devArch", "event-driven")
    page.wait_for_timeout(150)
    assert_("a=event-driven" in page.url, "架构筛选未写入 URL")
    assert_(page.locator(".dev-card:not([hidden])").count() >= 1, "架构筛选结果为空")


def security_test(page):
    page.goto((ROOT / "security.html").as_uri())
    page.wait_for_timeout(150)
    assert_(page.locator(".sec-tool").count() == 12, "安全工具不是 12 个")
    page.fill("#secSearch", "tls")
    page.wait_for_timeout(150)
    assert_("q=tls" in page.url, "安全搜索未写入 URL")
    assert_(page.locator(".sec-tool:not([hidden])").count() >= 1, "安全搜索无结果")
    page.fill("#secSearch", "")
    page.select_option("#secCategory", "供应链 / 镜像扫描")
    page.wait_for_timeout(150)
    assert_("c=" in page.url, "安全类别未写入 URL")
    assert_(page.locator(".sec-tool:not([hidden])").count() == 1, "安全类别过滤异常")


def sources_test(page):
    page.goto((ROOT / "sources.html").as_uri())
    page.wait_for_timeout(120)
    assert_(page.locator(".src-list li").count() == 220, "来源数不是 220")
    page.fill("#srcSearch", "django")
    page.wait_for_timeout(120)
    assert_("1 / 220" in page.inner_text("#srcCount"), "来源搜索计数异常")


def formats_test(page):
    page.goto((ROOT / "formats.html").as_uri())
    page.wait_for_timeout(120)
    total = page.locator(".fmt-card").count()
    assert_(total >= 40, f"格式数异常 {total}")
    page.fill("#fmtSearch", "elf")
    page.wait_for_timeout(120)
    assert_(page.locator(".fmt-card:not([hidden])").count() == 1, "ELF 过滤异常")
    assert_("q=elf" in page.url, "格式搜索未写入 URL")


def compare_test(page):
    page.goto((ROOT / "compare.html").as_uri())
    page.wait_for_timeout(180)
    page.click('[data-preset="mobile"]')
    page.wait_for_timeout(180)
    assert_(page.input_value("#cmp1") == "swift|SwiftUI", "移动预设未生效")
    assert_("m=framework" in page.url, "对比模式未写入 URL")
    url = page.url
    page.goto(url)
    page.wait_for_timeout(180)
    assert_(page.input_value("#cmp1") == "swift|SwiftUI", "刷新后预设未恢复")
    page.click('[data-preset="science"]')
    page.wait_for_timeout(150)
    assert_(page.input_value("#cmp1") == "fortran", "科学计算预设未生效")


def lineage_test(page):
    page.goto((ROOT / "lineage.html").as_uri())
    page.wait_for_timeout(220)
    assert_(page.locator(".lineage-node").count() == 78, "谱系节点不是 78")
    page.click('[data-lineage-filter="markup"]')
    page.wait_for_timeout(150)
    assert_("f=markup" in page.url, "谱系筛选未写入 URL")
    page.click('[data-lineage-filter="all"]')
    page.hover('.lineage-node[data-slug="c"] .lineage-hit')
    page.wait_for_timeout(120)
    assert_(page.is_visible("#lineageTip"), "悬停提示未出现")


def verified_test(page):
    page.goto((ROOT / "verified.html").as_uri())
    page.wait_for_timeout(150)
    assert_(page.locator(".verify-card").count() >= 16, "实测卡片不足")
    assert_(page.locator(".coverage-table tbody tr").count() == 78, "覆盖表不是 78 行")
    legend = page.inner_text(".cov-legend")
    for word in ("已实测", "已装未测", "未安装", "仅文档"):
        assert_(word in legend, f"图例缺少 {word}")


def font_test(page):
    page.goto((ROOT / "langs" / "python.html").as_uri())
    page.wait_for_timeout(120)
    page.click(".font-toggle")
    page.click('[data-font="serif"]')
    page.click('[data-size="l"]')
    page.click('[data-line="loose"]')
    assert_(page.evaluate("document.documentElement.dataset.font") == "serif", "字体未切换")
    page.reload()
    page.wait_for_timeout(150)
    assert_(page.evaluate("document.documentElement.dataset.size") == "l", "字号未持久化")
    page.click(".font-toggle")
    page.click("[data-font-reset]")
    assert_(page.evaluate("document.documentElement.dataset.font") == "sans", "重置失败")


def cmdk_test(page):
    page.goto((ROOT / "index.html").as_uri())
    page.wait_for_timeout(120)
    page.keyboard.press("Control+k")
    page.wait_for_timeout(120)
    assert_(page.is_visible("#cmdk"), "命令面板未打开")
    assert_(page.evaluate("document.activeElement.id") == "cmdkInput", "输入框未聚焦")
    page.fill("#cmdkInput", "django")
    page.wait_for_timeout(120)
    page.keyboard.press("Enter")
    page.wait_for_timeout(350)
    assert_("python-frameworks.html#django" in page.url, "回车跳转异常")
    page.goto((ROOT / "index.html").as_uri())
    page.keyboard.press("Control+k")
    page.wait_for_timeout(100)
    page.keyboard.press("Escape")
    page.wait_for_timeout(100)
    assert_("cmdk-btn" in page.evaluate("document.activeElement.className"), "焦点未回到按钮")


def print_test(page):
    page.goto((ROOT / "compare.html").as_uri())
    page.wait_for_timeout(120)
    page.emulate_media(media="print")
    assert_(page.eval_on_selector(".catalog", "e=>getComputedStyle(e).display") == "none",
            "打印未隐藏侧栏")
    assert_(page.eval_on_selector(".cmp-table", "e=>getComputedStyle(e).minWidth") == "0px",
            "打印对比表仍被撑宽")
    page.goto((ROOT / "lineage.html").as_uri())
    page.wait_for_timeout(120)
    page.emulate_media(media="print")
    assert_(page.eval_on_selector(".lineage-wrap", "e=>getComputedStyle(e).display") == "none",
            "打印未隐藏谱系图")
    page.emulate_media(media="screen")


def mobile_test(m):
    m.goto((ROOT / "index.html").as_uri())
    m.wait_for_timeout(150)
    over = m.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    assert_(over <= 0, f"移动端横向溢出 {over}px")
    assert_(m.is_visible(".cmdk-btn"), "移动端缺少搜索按钮")
    m.click(".cmdk-btn")
    m.wait_for_timeout(120)
    assert_(m.is_visible("#cmdk"), "移动端命令面板未打开")
    m.keyboard.press("Escape")
    m.goto((ROOT / "404.html").as_uri())
    m.wait_for_timeout(80)
    over = m.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    assert_(over <= 0, f"404 移动端横向溢出 {over}px")


def drawer_test(m):
    m.goto((ROOT / "index.html").as_uri())
    m.wait_for_timeout(120)
    m.click(".menu-toggle")
    m.wait_for_timeout(180)
    assert_(m.evaluate("document.body.classList.contains('menu-open')"), "抽屉未打开")
    assert_(m.evaluate("document.activeElement.id") == "catalogSearch", "抽屉未聚焦搜索")
    m.keyboard.press("Escape")
    m.wait_for_timeout(100)
    assert_("menu-toggle" in m.evaluate("document.activeElement.className"), "抽屉焦点未恢复")


if __name__ == "__main__":
    sys.exit(main())
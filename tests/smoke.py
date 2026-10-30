# -*- coding: utf-8 -*-
"""全站冒烟测试：结构、交互、移动端、打印。

用法：
    python tests/smoke.py
    python tests/smoke.py --quick     # 跳过 221 页全量扫描

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

    pages = [ROOT / "index.html", ROOT / "sources.html",
             ROOT / "scenarios.html", ROOT / "404.html"]
    for name in ("languages", "frameworks", "stacks"):
        pages += sorted((ROOT / name).glob("*.html"))

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
        check("首页三级入口", lambda: home_test(page))
        check("语言总览搜索与 URL", lambda: index_test(page))
        check("框架总览筛选与 URL", lambda: frameworks_index_test(page))
        check("技术栈总览与详情", lambda: stacks_test(page))
        check("旧链接跳转", lambda: redirect_test(page))
        check("开发场景筛选与 URL", lambda: scenarios_test(page))
        check("来源搜索", lambda: sources_test(page))
        check("产物索引与阶段总表", lambda: formats_test(page))
        check("安全工具筛选与 URL", lambda: sectools_test(page))
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

        if path.parent.name == "languages" and path.name not in ("index.html", "formats.html"):
            assert_(page.locator(".deep-feature").count() == 4, f"{rel} 深读特性不足")
            assert_(page.locator(".tag--verified").count()
                    + page.locator(".tag--level").count() >= 1,
                    f"{rel} 缺少内容等级")
            assert_(page.locator(".sources").count() == 1, f"{rel} 缺少参考来源")
        elif (path.parent.name == "frameworks"
              and path.name not in ("index.html", "security.html")):
            cards = page.locator(".fw-card").count()
            if cards:
                assert_(page.locator(".fw-source").count() == cards,
                        f"{rel} 来源数与卡片数不一致")
                assert_(page.locator(".fw-badge").count() == cards * 3,
                        f"{rel} 徽章数异常")
            assert_(page.locator(".tag--level").count() >= 1,
                    f"{rel} 缺少编者判断标签")


def home_test(page):
    page.goto((ROOT / "index.html").as_uri())
    page.wait_for_timeout(120)
    assert_(page.locator(".home-door").count() == 3, "首页不是三个入口")
    hrefs = page.eval_on_selector_all(
        ".home-door", "els => els.map(e => e.getAttribute('href'))"
    )
    for target in ("languages/index.html", "frameworks/index.html", "stacks/index.html"):
        assert_(target in hrefs, f"首页缺少入口 {target}")
    assert_(page.locator(".topic-link").count() == 3, "首页专题入口不是 3 个")
    assert_(page.is_visible(".cmdk-btn"), "首页缺少搜索按钮")


def frameworks_index_test(page):
    page.goto((ROOT / "frameworks" / "index.html").as_uri())
    page.wait_for_timeout(150)
    assert_(page.locator(".fw-index-card").count() == 142, "框架总览不是 142 张卡")
    page.select_option("#fwIndexLang", "python")
    page.wait_for_timeout(150)
    shown = page.locator(".fw-index-card:not([hidden])").count()
    assert_(shown == 4, f"Python 框架卡应为 4 张，实际 {shown}")
    assert_("l=python" in page.url, "框架语言筛选未写入 URL")
    page.select_option("#fwIndexLang", "all")
    page.fill("#fwIndexSearch", "游戏")
    page.wait_for_timeout(150)
    assert_(page.locator(".fw-index-card:not([hidden])").count() >= 2, "框架搜索无结果")


def stacks_test(page):
    page.goto((ROOT / "stacks" / "index.html").as_uri())
    page.wait_for_timeout(150)
    assert_(page.locator(".stack-entry").count() == 56, "技术栈不是 56 个")
    page.select_option("#stackDomain", "mobile")
    page.wait_for_timeout(150)
    assert_(page.locator(".stack-entry:not([hidden])").count() == 4, "移动领域栈不是 4 个")
    assert_("d=mobile" in page.url, "技术栈领域筛选未写入 URL")
    page.goto((ROOT / "stacks" / "flutter-cross.html").as_uri())
    page.wait_for_timeout(150)
    assert_("Flutter" in page.inner_text("h1"), "栈详情标题异常")
    rows = page.locator(".stack-table tbody tr").count()
    assert_(rows == 4, f"栈构成表应为 4 层，实际 {rows}")
    assert_(page.locator('a[href="../frameworks/dart.html#flutter"]').count() == 1,
            "栈页缺少框架链接")
    assert_(page.locator(".depth-block").count() == 8, "栈页深度段不是 8 个")


def sectools_test(page):
    page.goto((ROOT / "frameworks" / "security.html").as_uri())
    page.wait_for_timeout(150)
    assert_(page.locator(".sec-tool-card").count() == 20, "安全工具不是 20 个")
    assert_(page.locator(".sec-auth-note").count() == 1, "缺少授权提示")
    page.select_option("#secToolCat", "pentest")
    page.wait_for_timeout(150)
    assert_(page.locator(".sec-tool-card:not([hidden])").count() == 7,
            "渗透测试工具不是 7 个")
    assert_("c=pentest" in page.url, "安全类别未写入 URL")
    page.select_option("#secToolCat", "all")
    page.fill("#secToolSearch", "burp")
    page.wait_for_timeout(150)
    assert_(page.locator(".sec-tool-card:not([hidden])").count() == 1, "Burp 搜索异常")


def redirect_test(page):
    page.goto((ROOT / "langs" / "python.html").as_uri())
    page.wait_for_timeout(400)
    assert_("languages/python.html" in page.url, f"旧语言页未跳转：{page.url}")
    page.goto((ROOT / "formats.html").as_uri())
    page.wait_for_timeout(400)
    assert_("languages/formats.html" in page.url, f"旧产物索引未跳转：{page.url}")


def index_test(page):
    page.goto((ROOT / "languages" / "index.html").as_uri())
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


def scenarios_test(page):
    page.goto((ROOT / "scenarios.html").as_uri())
    page.wait_for_timeout(150)
    assert_(page.locator(".dev-section").count() == 11, "开发场景不是 11 个")
    assert_(page.locator(".dev-card").count() >= 100, "开发场景推荐组不足")
    patterns = page.locator("#devArch option").count()
    assert_(patterns == 13, f"统一模式选项不是 12 + 全部（{patterns}）")
    assert_(page.locator(".dev-legend__item").count() == 12, "架构模式图例不是 12 项")
    assert_(page.locator(".dev-arch__pattern").count() == 33, "架构分组模式徽标不是 33 个")
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
    page.select_option("#devScenario", "all")
    page.wait_for_timeout(120)
    page.select_option("#devArch", "pipeline")
    page.wait_for_timeout(150)
    shown = page.locator(".dev-card:not([hidden])").count()
    assert_(shown == 20, f"管线 / 批流模式应为 20 组，实际 {shown}")
    assert_("a=pipeline" in page.url, "模式筛选未写入 URL")
    page.reload()
    page.wait_for_timeout(180)
    assert_(page.input_value("#devArch") == "pipeline", "模式筛选刷新后未恢复")
    assert_(page.locator(".dev-card:not([hidden])").count() == 20, "刷新后模式筛选结果不一致")

    page.select_option("#devScenario", "embedded")
    page.select_option("#devArch", "native")
    page.wait_for_timeout(180)
    assert_("s=embedded" in page.url and "a=native" in page.url, "场景 + 模式 URL 状态缺失")
    assert_(page.locator(".dev-card:not([hidden])").count() == 3,
            "嵌入式场景 + 原生模式应为 3 组")
    assert_(page.locator("#dev-embedded .dev-arch:not([hidden])").count() == 1,
            "嵌入式场景 + 原生模式应只剩 1 个分组")


def sources_test(page):
    page.goto((ROOT / "sources.html").as_uri())
    page.wait_for_timeout(120)
    assert_(page.locator(".src-list li").count() == 220, "来源数不是 220")
    page.fill("#srcSearch", "django")
    page.wait_for_timeout(120)
    assert_("1 / 220" in page.inner_text("#srcCount"), "来源搜索计数异常")


def formats_test(page):
    page.goto((ROOT / "languages" / "formats.html").as_uri())
    page.wait_for_timeout(150)
    total = page.locator(".fmt-card").count()
    assert_(total >= 40, f"格式数异常 {total}")
    assert_(page.locator(".stage-details").count() == 78, "阶段总表不是 78 组")
    assert_(page.locator("#unclassified").count() == 1, "缺少未归类阶段")
    page.fill("#fmtSearch", "elf")
    page.wait_for_timeout(120)
    assert_(page.locator(".fmt-card:not([hidden])").count() == 1, "ELF 过滤异常")
    assert_("q=elf" in page.url, "格式搜索未写入 URL")


def font_test(page):
    page.goto((ROOT / "languages" / "python.html").as_uri())
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
    assert_("frameworks/python.html#django" in page.url, "回车跳转异常")
    page.goto((ROOT / "index.html").as_uri())
    page.wait_for_timeout(120)
    page.keyboard.press("Control+k")
    page.wait_for_timeout(120)
    page.goto((ROOT / "index.html").as_uri())
    page.wait_for_timeout(120)
    page.keyboard.press("Control+k")
    page.wait_for_timeout(120)
    page.fill("#cmdkInput", "管线")
    page.wait_for_timeout(120)
    assert_(page.locator("#cmdkInput").count() == 1, "命令面板输入框丢失")
    assert_(page.locator(".cmdk__item").count() >= 1, "模式关键词未命中任何索引")
    page.keyboard.press("Escape")
    page.wait_for_timeout(100)
    page.goto((ROOT / "languages" / "python.html").as_uri())
    page.wait_for_timeout(120)
    page.keyboard.press("Control+k")
    page.wait_for_timeout(120)
    page.fill("#cmdkInput", "django")
    page.wait_for_timeout(120)
    page.keyboard.press("Enter")
    page.wait_for_timeout(350)
    assert_("frameworks/python.html#django" in page.url, "语言页 ⌘K 跳转路径错误")
    page.goto((ROOT / "index.html").as_uri())
    page.keyboard.press("Control+k")
    page.wait_for_timeout(100)
    page.keyboard.press("Escape")
    page.wait_for_timeout(100)
    assert_("cmdk-btn" in page.evaluate("document.activeElement.className"), "焦点未回到按钮")


def print_test(page):
    page.goto((ROOT / "scenarios.html").as_uri())
    page.wait_for_timeout(120)
    page.emulate_media(media="print")
    assert_(page.eval_on_selector(".catalog", "e=>getComputedStyle(e).display") == "none",
            "打印未隐藏侧栏")
    page.goto((ROOT / "stacks" / "flutter-cross.html").as_uri())
    page.wait_for_timeout(120)
    page.emulate_media(media="print")
    assert_(page.eval_on_selector(".catalog", "e=>getComputedStyle(e).display") == "none",
            "栈页打印未隐藏侧栏")
    assert_(page.eval_on_selector(".table-hint", "e=>getComputedStyle(e).display") == "none",
            "打印未隐藏表格提示")
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
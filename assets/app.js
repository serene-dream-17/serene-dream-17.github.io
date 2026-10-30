/* ============================================================
   编程语言产物链档案 — 交互
   纯原生 JS，无外部依赖，file:// 可直接运行
   ============================================================ */
(function () {
  "use strict";

  /* 只有在脚本真正运行后才启用进场动画的初始隐藏态；
     脚本缺失时内容保持可见。 */
  document.documentElement.classList.add("js");

  var body = document.body;
  var page = body.dataset.page || "lang";
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------- 侧栏抽屉 ---------------- */
  var menuToggle = document.querySelector(".menu-toggle");
  var scrim = document.querySelector(".scrim");
  var catalog = document.querySelector(".catalog");
  var lastMenuFocus = null;

  function focusables(root) {
    return Array.prototype.slice.call(
      root.querySelectorAll('a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])')
    ).filter(function (el) { return el.getClientRects().length > 0; });
  }

  function trapTab(list, e) {
    if (!list.length) return;
    var first = list[0];
    var last = list[list.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }

  function openMenu() {
    lastMenuFocus = document.activeElement;
    body.classList.add("menu-open");
    if (menuToggle) menuToggle.setAttribute("aria-expanded", "true");
    var target = document.getElementById("catalogSearch");
    if (target) setTimeout(function () { target.focus(); }, 60);
  }
  function closeMenu() {
    var wasOpen = body.classList.contains("menu-open");
    body.classList.remove("menu-open");
    if (menuToggle) menuToggle.setAttribute("aria-expanded", "false");
    if (wasOpen && menuToggle) menuToggle.focus();
  }

  if (menuToggle) {
    menuToggle.addEventListener("click", function () {
      if (body.classList.contains("menu-open")) closeMenu();
      else openMenu();
    });
  }
  if (scrim) scrim.addEventListener("click", closeMenu);
  window.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeMenu();
    if (e.key === "Tab" && body.classList.contains("menu-open") && catalog) {
      var list = [];
      if (menuToggle) list.push(menuToggle);
      list = list.concat(focusables(catalog));
      trapTab(list, e);
    }
  });

  /* 桌面端不保留抽屉状态 */
  var desktop = window.matchMedia("(min-width: 1081px)");
  if (desktop.matches) closeMenu();
  if (desktop.addEventListener) {
    desktop.addEventListener("change", function (e) {
      if (e.matches) closeMenu();
    });
  }

  /* 当前条目不在目录视野内时，才滚到中间 */
  var activeLink = document.querySelector(".catalog__link.is-active");
  if (activeLink && catalog) {
    var catBody = catalog.querySelector(".catalog__body");
    if (catBody) {
      var linkRect = activeLink.getBoundingClientRect();
      var bodyRect = catBody.getBoundingClientRect();
      var outside = linkRect.top < bodyRect.top || linkRect.bottom > bodyRect.bottom;
      if (outside) {
        catBody.scrollTop +=
          linkRect.top - bodyRect.top - (bodyRect.height - linkRect.height) / 2;
      }
    }
  }

  /* ---------------- 目录搜索 + 筛选 ---------------- */
  var searchInput = document.getElementById("catalogSearch");
  var catalogBody = document.querySelector(".catalog__body");
  var emptyMsg = document.querySelector(".catalog__empty");
  var filters = Array.prototype.slice.call(document.querySelectorAll(".filter"));
  var activeFilter = "all";

  function normalize(s) {
    return (s || "").toLowerCase().replace(/\s+/g, " ");
  }

  function applyCatalogFilter() {
    if (!catalogBody || !searchInput) return;
    var q = normalize(searchInput.value.trim());
    var links = catalogBody.querySelectorAll(".catalog__link");
    var shown = 0;

    links.forEach(function (link) {
      var hay = normalize(link.dataset.search || link.textContent);
      var fam = link.dataset.family || "";
      var okQ = !q || hay.indexOf(q) !== -1;
      var okF = activeFilter === "all" || fam === activeFilter;
      var show = okQ && okF;
      link.hidden = !show;
      if (show) shown++;
    });

    catalogBody.querySelectorAll(".catalog__group").forEach(function (group) {
      var any = group.querySelector(".catalog__link:not([hidden])");
      group.hidden = !any;
    });

    if (emptyMsg) emptyMsg.dataset.visible = shown === 0 ? "true" : "false";
    if (catalog) catalog.classList.toggle("is-searching", !!q || activeFilter !== "all");
  }

  if (searchInput) {
    var t;
    searchInput.addEventListener("input", function () {
      clearTimeout(t);
      t = setTimeout(applyCatalogFilter, 70);
    });
  }

  filters.forEach(function (btn) {
    btn.addEventListener("click", function () {
      activeFilter = btn.dataset.filter || "all";
      /* 侧栏与首页各有一组筛选按钮，保持两组状态同步 */
      filters.forEach(function (b) {
        b.setAttribute(
          "aria-pressed",
          b.dataset.filter === activeFilter ? "true" : "false"
        );
      });
      applyCatalogFilter();
      if (page === "index") applyIndexFilter();
    });
  });

  /* ---------------- 首页搜索 + 筛选 ---------------- */
  var indexSearch = document.getElementById("indexSearch");
  var indexEmpty = document.querySelector(".index-empty");
  var indexCount = document.getElementById("indexCount");

  function applyIndexFilter() {
    if (!indexSearch) return;
    var q = normalize(indexSearch.value.trim());
    var cards = document.querySelectorAll(".lang-card");
    var shown = 0;

    cards.forEach(function (card) {
      var hay = normalize(card.dataset.search || card.textContent);
      var fam = card.dataset.family || "";
      var okQ = !q || hay.indexOf(q) !== -1;
      var okF = activeFilter === "all" || fam === activeFilter;
      var show = okQ && okF;
      card.hidden = !show;
      if (show) shown++;
    });

    document.querySelectorAll(".era-section").forEach(function (sec) {
      var any = sec.querySelector(".lang-card:not([hidden])");
      sec.hidden = !any;
    });

    if (indexEmpty) indexEmpty.classList.toggle("is-visible", shown === 0);
    if (indexCount) {
      var totalCards = document.querySelectorAll(".lang-card").length;
      indexCount.textContent = shown === totalCards
        ? totalCards + " 门"
        : shown + " / " + totalCards + " 门";
    }
  }

  if (indexSearch) {
    var ti;
    indexSearch.addEventListener("input", function () {
      clearTimeout(ti);
      ti = setTimeout(applyIndexFilter, 70);
    });
    applyIndexFilter();
  }

  /* ---------------- 开发场景 ---------------- */
  var devSearch = document.getElementById("devSearch");
  var devScenario = document.getElementById("devScenario");
  var devArch = document.getElementById("devArch");
  var devCount = document.getElementById("devCount");
  var devEmpty = document.getElementById("devEmpty");

  function applyDevFilter() {
    if (!devSearch) return;
    var q = normalize(devSearch.value.trim());
    var sc = devScenario ? devScenario.value : "all";
    var ar = devArch ? devArch.value : "all";
    var cards = document.querySelectorAll(".dev-card");
    var total = cards.length;
    var shown = 0;

    cards.forEach(function (card) {
      var hay = normalize(card.dataset.search || card.textContent);
      var okQ = !q || hay.indexOf(q) !== -1;
      var okS = sc === "all" || card.dataset.scenario === sc;
      var okA = ar === "all" || card.dataset.arch === ar;
      var show = okQ && okS && okA;
      card.hidden = !show;
      if (show) shown++;
    });

    document.querySelectorAll(".dev-arch").forEach(function (arch) {
      var any = arch.querySelector(".dev-card:not([hidden])");
      arch.hidden = !any;
    });
    document.querySelectorAll(".dev-section").forEach(function (sec) {
      var any = sec.querySelector(".dev-card:not([hidden])");
      sec.hidden = !any;
    });

    if (devCount) {
      devCount.textContent = shown === total
        ? total + " 组"
        : shown + " / " + total + " 组";
    }
    if (devEmpty) devEmpty.classList.toggle("is-visible", shown === 0);
  }

  if (devSearch) {
    var td;
    devSearch.addEventListener("input", function () {
      clearTimeout(td);
      td = setTimeout(applyDevFilter, 70);
    });
    if (devScenario) devScenario.addEventListener("change", applyDevFilter);
    if (devArch) devArch.addEventListener("change", applyDevFilter);
    applyDevFilter();
  }

  /* ---------------- 框架总览 ---------------- */
  var fwIndexSearch = document.getElementById("fwIndexSearch");
  var fwIndexLang = document.getElementById("fwIndexLang");
  var fwIndexType = document.getElementById("fwIndexType");
  var fwIndexCount = document.getElementById("fwIndexCount");
  var fwIndexEmpty = document.getElementById("fwIndexEmpty");

  function applyFwIndexFilter() {
    if (!fwIndexSearch) return;
    var q = normalize(fwIndexSearch.value.trim());
    var lg = fwIndexLang ? fwIndexLang.value : "all";
    var ty = fwIndexType ? fwIndexType.value : "all";
    var cards = document.querySelectorAll(".fw-index-card");
    var total = cards.length;
    var shown = 0;
    cards.forEach(function (card) {
      var hay = normalize(card.dataset.search || card.textContent);
      var show = (!q || hay.indexOf(q) !== -1)
        && (lg === "all" || card.dataset.lang === lg)
        && (ty === "all" || card.dataset.type === ty);
      card.hidden = !show;
      if (show) shown++;
    });
    if (fwIndexCount) {
      fwIndexCount.textContent = shown === total ? total + " 张" : shown + " / " + total + " 张";
    }
    if (fwIndexEmpty) fwIndexEmpty.classList.toggle("is-visible", shown === 0);
  }

  if (fwIndexSearch) {
    var tf;
    fwIndexSearch.addEventListener("input", function () {
      clearTimeout(tf);
      tf = setTimeout(applyFwIndexFilter, 70);
    });
    if (fwIndexLang) fwIndexLang.addEventListener("change", applyFwIndexFilter);
    if (fwIndexType) fwIndexType.addEventListener("change", applyFwIndexFilter);
    applyFwIndexFilter();
  }

  /* ---------------- 技术栈总览 ---------------- */
  var stackSearch = document.getElementById("stackSearch");
  var stackDomain = document.getElementById("stackDomain");
  var stackCount = document.getElementById("stackCount");
  var stackEmpty = document.getElementById("stackEmpty");

  function applyStackFilter() {
    if (!stackSearch) return;
    var q = normalize(stackSearch.value.trim());
    var dom = stackDomain ? stackDomain.value : "all";
    var cards = document.querySelectorAll(".stack-entry");
    var total = cards.length;
    var shown = 0;
    cards.forEach(function (card) {
      var hay = normalize(card.dataset.search || card.textContent);
      var show = (!q || hay.indexOf(q) !== -1)
        && (dom === "all" || card.dataset.domain === dom);
      card.hidden = !show;
      if (show) shown++;
    });
    document.querySelectorAll(".matrix-section").forEach(function (sec) {
      sec.hidden = !sec.querySelector(".stack-entry:not([hidden])");
    });
    if (stackCount) {
      stackCount.textContent = shown === total ? total + " 个栈" : shown + " / " + total + " 个栈";
    }
    if (stackEmpty) stackEmpty.classList.toggle("is-visible", shown === 0);
  }

  if (stackSearch) {
    var tk;
    stackSearch.addEventListener("input", function () {
      clearTimeout(tk);
      tk = setTimeout(applyStackFilter, 70);
    });
    if (stackDomain) stackDomain.addEventListener("change", applyStackFilter);
    applyStackFilter();
  }

  /* ---------------- 安全工具 ---------------- */
  var secToolSearch = document.getElementById("secToolSearch");
  var secToolCat = document.getElementById("secToolCat");
  var secToolCount = document.getElementById("secToolCount");
  var secToolEmpty = document.getElementById("secToolEmpty");

  function applySecToolFilter() {
    if (!secToolSearch) return;
    var q = normalize(secToolSearch.value.trim());
    var cat = secToolCat ? secToolCat.value : "all";
    var cards = document.querySelectorAll(".sec-tool-card");
    var total = cards.length;
    var shown = 0;
    cards.forEach(function (card) {
      var hay = normalize(card.dataset.search || card.textContent);
      var show = (!q || hay.indexOf(q) !== -1)
        && (cat === "all" || card.dataset.cat === cat);
      card.hidden = !show;
      if (show) shown++;
    });
    document.querySelectorAll(".matrix-section").forEach(function (sec) {
      sec.hidden = !sec.querySelector(".sec-tool-card:not([hidden])");
    });
    if (secToolCount) {
      secToolCount.textContent = shown === total ? total + " 个工具" : shown + " / " + total + " 个工具";
    }
    if (secToolEmpty) secToolEmpty.classList.toggle("is-visible", shown === 0);
  }

  if (secToolSearch) {
    var tst;
    secToolSearch.addEventListener("input", function () {
      clearTimeout(tst);
      tst = setTimeout(applySecToolFilter, 70);
    });
    if (secToolCat) secToolCat.addEventListener("change", applySecToolFilter);
    applySecToolFilter();
  }

  /* ---------------- 来源索引 ---------------- */
  var srcSearch = document.getElementById("srcSearch");
  var srcCount = document.getElementById("srcCount");
  var srcEmpty = document.getElementById("srcEmpty");

  function applySourceFilter() {
    if (!srcSearch) return;
    var q = normalize(srcSearch.value.trim());
    var li = document.querySelectorAll(".src-list li");
    var total = li.length;
    var shown = 0;

    li.forEach(function (item) {
      var hay = normalize(item.dataset.search || item.textContent);
      var ok = !q || hay.indexOf(q) !== -1;
      item.hidden = !ok;
      if (ok) shown++;
    });

    document.querySelectorAll(".src-group").forEach(function (group) {
      var any = group.querySelector(".src-list li:not([hidden])");
      group.hidden = !any;
    });

    if (srcCount) {
      srcCount.textContent = shown === total ? total + " 条" : shown + " / " + total + " 条";
    }
    if (srcEmpty) srcEmpty.classList.toggle("is-visible", shown === 0);
  }

  if (srcSearch) {
    var ts;
    srcSearch.addEventListener("input", function () {
      clearTimeout(ts);
      ts = setTimeout(applySourceFilter, 60);
    });
    applySourceFilter();
  }


  /* ---------------- 格式索引 ---------------- */
  var fmtSearch = document.getElementById("fmtSearch");
  var fmtCount = document.getElementById("fmtCount");
  var fmtEmpty = document.getElementById("fmtEmpty");

  function applyFormatFilter() {
    if (!fmtSearch) return;
    var q = normalize(fmtSearch.value.trim());
    var cards = document.querySelectorAll(".fmt-card");
    var total = cards.length;
    var shown = 0;

    cards.forEach(function (card) {
      var hay = normalize(card.dataset.search || card.textContent);
      var ok = !q || hay.indexOf(q) !== -1;
      card.hidden = !ok;
      if (ok) shown++;
    });
    document.querySelectorAll(".fmt-section").forEach(function (sec) {
      var any = sec.querySelector(".fmt-card:not([hidden])");
      sec.hidden = !any;
    });
    if (fmtCount) {
      fmtCount.textContent = shown === total ? total + " 种" : shown + " / " + total + " 种";
    }
    if (fmtEmpty) fmtEmpty.classList.toggle("is-visible", shown === 0);
  }

  if (fmtSearch) {
    var tf;
    fmtSearch.addEventListener("input", function () {
      clearTimeout(tf);
      tf = setTimeout(applyFormatFilter, 60);
    });
    applyFormatFilter();
  }

  /* ---------------- URL 状态 ---------------- */
  var restoring = false;
  var params = new URLSearchParams(window.location.search);

  function syncParam(key, value, push) {
    if (restoring) return;
    var p = new URLSearchParams(window.location.search);
    if (value) p.set(key, value);
    else p.delete(key);
    var qs = p.toString();
    var url = window.location.pathname + (qs ? "?" + qs : "") + window.location.hash;
    if (push) history.pushState(null, "", url);
    else history.replaceState(null, "", url);
  }

  function setSearchValue(el, key, value) {
    if (!el || !value) return;
    el.value = value;
    syncParam(key, value, false);
    el.dispatchEvent(new Event("input"));
  }

  function clickFilter(key, value) {
    var btn = document.querySelector('[data-filter="' + value + '"]');
    if (btn) btn.click();
  }

  if (page === "index") {
    setSearchValue(indexSearch, "q", params.get("q"));
    if (params.get("f")) clickFilter("f", params.get("f"));
    if (indexSearch) {
      indexSearch.addEventListener("input", function () {
        syncParam("q", indexSearch.value.trim(), false);
      });
    }
    document.querySelectorAll(".index-filters .filter").forEach(function (b) {
      b.addEventListener("click", function () { syncParam("f", b.dataset.filter, true); });
    });
  } else if (page === "lang" || page === "framework") {
    setSearchValue(searchInput, "q", params.get("q"));
    if (params.get("f")) clickFilter("f", params.get("f"));
    if (searchInput) {
      searchInput.addEventListener("input", function () {
        syncParam("q", searchInput.value.trim(), false);
      });
    }
    document.querySelectorAll(".catalog__tools .filter").forEach(function (b) {
      b.addEventListener("click", function () { syncParam("f", b.dataset.filter, true); });
    });
  } else if (page === "scenarios") {
    setSearchValue(devSearch, "q", params.get("q"));
    if (params.get("s") && devScenario) {
      devScenario.value = params.get("s");
      devScenario.dispatchEvent(new Event("change"));
    }
    if (params.get("a") && devArch) {
      devArch.value = params.get("a");
      devArch.dispatchEvent(new Event("change"));
    }
    if (devSearch) {
      devSearch.addEventListener("input", function () {
        syncParam("q", devSearch.value.trim(), false);
      });
    }
    if (devScenario) {
      devScenario.addEventListener("change", function () { syncParam("s", devScenario.value, true); });
    }
    if (devArch) {
      devArch.addEventListener("change", function () { syncParam("a", devArch.value, true); });
    }
  } else if (page === "frameworks") {
    setSearchValue(fwIndexSearch, "q", params.get("q"));
    if (params.get("l") && fwIndexLang) {
      fwIndexLang.value = params.get("l");
      fwIndexLang.dispatchEvent(new Event("change"));
    }
    if (params.get("t") && fwIndexType) {
      fwIndexType.value = params.get("t");
      fwIndexType.dispatchEvent(new Event("change"));
    }
    if (fwIndexSearch) {
      fwIndexSearch.addEventListener("input", function () {
        syncParam("q", fwIndexSearch.value.trim(), false);
      });
    }
    if (fwIndexLang) {
      fwIndexLang.addEventListener("change", function () { syncParam("l", fwIndexLang.value, true); });
    }
    if (fwIndexType) {
      fwIndexType.addEventListener("change", function () { syncParam("t", fwIndexType.value, true); });
    }
  } else if (page === "stacks") {
    setSearchValue(stackSearch, "q", params.get("q"));
    if (params.get("d") && stackDomain) {
      stackDomain.value = params.get("d");
      stackDomain.dispatchEvent(new Event("change"));
    }
    if (stackSearch) {
      stackSearch.addEventListener("input", function () {
        syncParam("q", stackSearch.value.trim(), false);
      });
    }
    if (stackDomain) {
      stackDomain.addEventListener("change", function () { syncParam("d", stackDomain.value, true); });
    }
  } else if (page === "sectools") {
    setSearchValue(secToolSearch, "q", params.get("q"));
    if (params.get("c") && secToolCat) {
      secToolCat.value = params.get("c");
      secToolCat.dispatchEvent(new Event("change"));
    }
    if (secToolSearch) {
      secToolSearch.addEventListener("input", function () {
        syncParam("q", secToolSearch.value.trim(), false);
      });
    }
    if (secToolCat) {
      secToolCat.addEventListener("change", function () { syncParam("c", secToolCat.value, true); });
    }
  } else if (page === "sources") {
    setSearchValue(srcSearch, "q", params.get("q"));
    if (srcSearch) {
      srcSearch.addEventListener("input", function () {
        syncParam("q", srcSearch.value.trim(), false);
      });
    }
  } else if (page === "formats") {
    setSearchValue(fmtSearch, "q", params.get("q"));
    if (fmtSearch) {
      fmtSearch.addEventListener("input", function () {
        syncParam("q", fmtSearch.value.trim(), false);
      });
    }
  }

  window.addEventListener("popstate", function () {
    window.location.reload();
  });

  /* ---------------- 键盘 ---------------- */
  window.addEventListener("keydown", function (e) {
    var tag = (e.target.tagName || "").toLowerCase();
    var typing = tag === "input" || tag === "textarea" || tag === "select" ||
                 e.target.isContentEditable;

    if (e.key === "/" && !typing) {
      e.preventDefault();
      var focusTarget;
      if (page === "index") {
        focusTarget = document.getElementById("indexSearch") ||
                      document.getElementById("catalogSearch");
      } else if (page === "scenarios") {
        focusTarget = document.getElementById("devSearch") ||
                      document.getElementById("catalogSearch");
      } else if (page === "sectools") {
        focusTarget = document.getElementById("secToolSearch") ||
                      document.getElementById("catalogSearch");
      } else if (page === "sources") {
        focusTarget = document.getElementById("srcSearch") ||
                      document.getElementById("catalogSearch");
      } else if (page === "formats") {
        focusTarget = document.getElementById("fmtSearch") ||
                      document.getElementById("catalogSearch");
      } else {
        focusTarget = document.getElementById("catalogSearch") ||
                      document.getElementById("indexSearch");
      }
      if (focusTarget) focusTarget.focus();
      return;
    }

    if (e.key === "Escape" && typing) {
      e.target.value = "";
      e.target.dispatchEvent(new Event("input"));
      e.target.blur();
      return;
    }

    if (typing) return;

    if (e.key === "ArrowLeft" && body.dataset.prev) {
      window.location.href = body.dataset.prev;
    } else if (e.key === "ArrowRight" && body.dataset.next) {
      window.location.href = body.dataset.next;
    }
  });

  /* ---------------- 代码：复制 / 展开 ---------------- */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "fixed";
      ta.style.top = "-1000px";
      document.body.appendChild(ta);
      ta.select();
      try {
        document.execCommand("copy");
        resolve();
      } catch (err) {
        reject(err);
      } finally {
        document.body.removeChild(ta);
      }
    });
  }

  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var wrap = btn.closest(".code-wrap");
      var codeEl = wrap ? wrap.querySelector("code") : null;
      if (!codeEl) return;
      copyText(codeEl.textContent).then(function () {
        var old = btn.textContent;
        btn.textContent = "已复制";
        btn.dataset.copied = "true";
        setTimeout(function () {
          btn.textContent = old;
          btn.dataset.copied = "false";
        }, 1600);
      }).catch(function () {
        btn.textContent = "复制失败";
        setTimeout(function () { btn.textContent = "复制"; }, 1600);
      });
    });
  });

  document.querySelectorAll("[data-expand]").forEach(function (btn) {
    var wrap = btn.closest(".code-wrap");
    var pre = wrap ? wrap.querySelector(".code") : null;
    if (!pre) return;

    btn.addEventListener("click", function () {
      var clamped = pre.classList.toggle("is-clamped");
      btn.textContent = clamped ? "展开全部" : "收起";
      btn.setAttribute("aria-expanded", clamped ? "false" : "true");
    });
  });

  /* 动态计数对读屏可播报 */
  ["indexCount", "srcCount", "fmtCount", "fwIndexCount", "stackCount"].forEach(function (id) {
    var el = document.getElementById(id);
    if (el) {
      el.setAttribute("aria-live", "polite");
      el.setAttribute("role", "status");
    }
  });

  /* ---------------- 阅读进度 + 移动端菜单收起 ---------------- */
  var progressBar = document.querySelector(".progress span");
  var lastScrollY = window.scrollY;
  function updateProgress() {
    var y = window.scrollY;
    if (progressBar) {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      var p = h > 0 ? Math.min(1, Math.max(0, y / h)) : 0;
      progressBar.style.width = (p * 100).toFixed(2) + "%";
    }
    if (menuToggle) {
      if (body.classList.contains("menu-open")) {
        menuToggle.classList.remove("is-hidden");
      } else if (y > lastScrollY + 6 && y > 180) {
        menuToggle.classList.add("is-hidden");
      } else if (y < lastScrollY - 6 || y < 120) {
        menuToggle.classList.remove("is-hidden");
      }
    }
    lastScrollY = y;
  }
  window.addEventListener("scroll", updateProgress, { passive: true });
  window.addEventListener("resize", updateProgress);
  updateProgress();

  /* ---------------- 进场动画 ---------------- */
  var reveals = document.querySelectorAll(".reveal");
  if (!reduceMotion && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* 体积条：进入视野后再增长 */
  var fills = document.querySelectorAll(".footprint__fill");
  function growFill(el) {
    var target = el.dataset.w;
    if (target == null) return;
    el.style.width = "0%";
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        el.style.width = target + "%";
      });
    });
  }
  if (!reduceMotion && "IntersectionObserver" in window) {
    var io2 = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          growFill(entry.target);
          io2.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });
    fills.forEach(function (el) { io2.observe(el); });
  }

  /* ---------------- 阶段条平滑定位 ---------------- */
  document.querySelectorAll(".stage-chip").forEach(function (chip) {
    chip.addEventListener("click", function (e) {
      var id = chip.getAttribute("href");
      if (!id || id.charAt(0) !== "#") return;
      var target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({
        behavior: reduceMotion ? "auto" : "smooth",
        block: "start"
      });
      target.classList.remove("is-flash");
      void target.offsetWidth;
      target.classList.add("is-flash");
      history.replaceState(null, "", id);
    });
  });

  /* ---------------- 引用目标高亮 ---------------- */
  function flashCiteTarget() {
    var id = "";
    try { id = decodeURIComponent(window.location.hash.slice(1)); } catch (e) { return; }
    if (!id) return;
    var el = document.getElementById(id);
    if (!el) return;
    var box = el.closest("li") || el.closest(".fw-source") || el;
    box.classList.remove("is-target");
    void box.offsetWidth;
    box.classList.add("is-target");
    setTimeout(function () { box.classList.remove("is-target"); }, 1900);
  }

  document.querySelectorAll(".cite").forEach(function (a) {
    a.addEventListener("click", function () { setTimeout(flashCiteTarget, 80); });
  });
  window.addEventListener("hashchange", flashCiteTarget);
  if (window.location.hash) setTimeout(flashCiteTarget, 80);

  /* 页面就绪 */
  requestAnimationFrame(function () {
    body.classList.add("is-ready");
  });
})();

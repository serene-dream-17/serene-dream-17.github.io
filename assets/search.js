/* ============================================================
   ⌘K 全局搜索
   数据：window.ARCHIVE_SEARCH（由 build.py 生成）
   ============================================================ */
(function () {
  "use strict";

  var data = window.ARCHIVE_SEARCH;
  if (!data || !data.items || !data.items.length) return;

  var root = document.body.dataset.root || "";
  var items = data.items;
  var open = false;
  var active = 0;
  var results = [];
  var box, input, list, empty;
  var lastFocus = null;

  function normalize(s) {
    return (s || "").toLowerCase().replace(/\s+/g, " ").trim();
  }

  items.forEach(function (it) {
    it._hay = normalize(
      [it.title, it.group, it.desc, (it.keywords || []).join(" "), it.kind].join(" ")
    );
    it._kw = (it.keywords || []).map(normalize);
  });

  function build() {
    var wrap = document.createElement("div");
    wrap.className = "cmdk";
    wrap.id = "cmdk";
    wrap.setAttribute("role", "dialog");
    wrap.setAttribute("aria-modal", "true");
    wrap.setAttribute("aria-label", "全站搜索");
    wrap.innerHTML =
      '<div class="cmdk__box">' +
      '<div class="cmdk__head">' +
      '<svg width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">' +
      '<circle cx="7" cy="7" r="4.5"></circle><path d="M10.5 10.5 14 14"></path></svg>' +
      '<input id="cmdkInput" type="search" placeholder="搜索语言、框架、格式、场景（⌘K）" autocomplete="off" spellcheck="false" aria-label="全站搜索">' +
      '<span class="cmdk__esc">Esc</span>' +
      "</div>" +
      '<ul class="cmdk__list" id="cmdkList" role="listbox"></ul>' +
      '<p class="cmdk__empty" id="cmdkEmpty" hidden>没有匹配项。试试「rust」「elf」「游戏」。</p>' +
      '<div class="cmdk__foot"><span><kbd>↑</kbd><kbd>↓</kbd> 选择</span><span><kbd>Enter</kbd> 打开</span><span><kbd>Esc</kbd> 关闭</span></div>' +
      "</div>";
    document.body.appendChild(wrap);

    box = wrap;
    input = wrap.querySelector("#cmdkInput");
    list = wrap.querySelector("#cmdkList");
    empty = wrap.querySelector("#cmdkEmpty");

    wrap.addEventListener("click", function (e) {
      if (e.target === wrap) close();
    });
    input.addEventListener("input", render);
    input.addEventListener("keydown", onKey);
  }

  function isWordStart(hay, idx) {
    return idx === 0 || /[\s\-_/·、，,.()\[\]]/.test(hay.charAt(idx - 1));
  }

  function startsWord(text, q) {
    var i = text.indexOf(q);
    while (i !== -1) {
      if (i > 0 && /[\s\-_/·]/.test(text.charAt(i - 1))) return true;
      i = text.indexOf(q, i + 1);
    }
    return false;
  }

  function score(it, q) {
    if (!q) return 1;
    var hay = it._hay;
    var idx = hay.indexOf(q);
    if (idx === -1) return 0;

    var title = normalize(it.title);
    if (title === q) return 120;
    if (it._kw && it._kw.indexOf(q) !== -1) return 110;
    if (title.indexOf(q) === 0) return 100;
    if (startsWord(title, q)) return 95;
    if (title.indexOf(q) !== -1) return 45;
    if (isWordStart(hay, idx)) return 45;
    if (normalize(it.group).indexOf(q) !== -1) return 30;
    return 8;
  }

  function render() {
    var q = normalize(input.value);
    results = items
      .map(function (it) { return { it: it, s: score(it, q) }; })
      .filter(function (r) {
        if (!q) return true;
        return q.length >= 3 ? r.s >= 30 : r.s > 0;
      })
      .sort(function (a, b) {
        if (b.s !== a.s) return b.s - a.s;
        return a.it.title.length - b.it.title.length;
      })
      .map(function (r) { return r.it; });

    active = 0;
    list.innerHTML = "";
    if (!results.length) {
      empty.hidden = false;
      return;
    }
    empty.hidden = true;

    var order = [];
    var buckets = {};
    results.forEach(function (it) {
      if (!buckets[it.group]) {
        buckets[it.group] = [];
        order.push(it.group);
      }
      buckets[it.group].push(it);
    });
    var flat = [];
    order.forEach(function (g) {
      flat = flat.concat(buckets[g]);
    });
    results = flat.slice(0, 40);

    var lastGroup = null;
    results.forEach(function (it, i) {
      if (it.group !== lastGroup) {
        lastGroup = it.group;
        var g = document.createElement("li");
        g.className = "cmdk__group";
        g.textContent = it.group;
        list.appendChild(g);
      }
      var li = document.createElement("li");
      li.setAttribute("role", "option");
      li.id = "cmdk-opt-" + i;
      li.setAttribute("aria-selected", i === 0 ? "true" : "false");
      li.innerHTML =
        '<a class="cmdk__item" href="' + root + it.href + '">' +
        "<b>" + escapeHtml(it.title) + "</b>" +
        "<span>" + escapeHtml(it.desc) + "</span>" +
        "<em>" + escapeHtml(it.kind) + "</em></a>";
      li.addEventListener("mousemove", function () { setActive(i); });
      li.addEventListener("click", function (e) {
        if (e.target.closest("a")) return;
        window.location.href = root + it.href;
      });
      list.appendChild(li);
    });
    setActive(0);
  }

  function escapeHtml(s) {
    var d = document.createElement("div");
    d.textContent = s == null ? "" : String(s);
    return d.innerHTML;
  }

  function setActive(i) {
    var opts = list.querySelectorAll('[role="option"]');
    if (!opts.length) return;
    active = Math.max(0, Math.min(i, opts.length - 1));
    opts.forEach(function (o, n) {
      o.setAttribute("aria-selected", n === active ? "true" : "false");
    });
    var cur = opts[active];
    if (cur) {
      cur.scrollIntoView({ block: "nearest" });
      input.setAttribute("aria-activedescendant", cur.id);
    }
  }

  function onKey(e) {
    if (e.key === "Tab") {
      var list = Array.prototype.slice.call(
        box.querySelectorAll('a[href], button:not([disabled]), input')
      ).filter(function (el) { return el.getClientRects().length > 0; });
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
      return;
    }
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActive(active + 1);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActive(active - 1);
    } else if (e.key === "Enter") {
      e.preventDefault();
      var it = results[active];
      if (it) window.location.href = root + it.href;
    } else if (e.key === "Escape") {
      e.preventDefault();
      close();
    }
  }

  function show() {
    if (!box) build();
    lastFocus = document.activeElement;
    open = true;
    box.classList.add("is-open");
    document.body.classList.add("cmdk-open");
    input.value = "";
    render();
    input.focus();
  }

  function close() {
    if (!box) return;
    open = false;
    box.classList.remove("is-open");
    document.body.classList.remove("cmdk-open");
    if (lastFocus && lastFocus !== document.body && lastFocus.focus) {
      lastFocus.focus();
    } else {
      var trigger = document.querySelector(".cmdk-btn");
      if (trigger) trigger.focus();
    }
  }

  document.addEventListener("keydown", function (e) {
    var tag = (e.target.tagName || "").toLowerCase();
    var typing = tag === "input" || tag === "textarea" || tag === "select";
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      if (open) close();
      else show();
      return;
    }
    if (!typing && e.key === "Escape" && open) close();
  });

  document.querySelectorAll("[data-cmdk]").forEach(function (btn) {
    btn.addEventListener("click", show);
  });
})();

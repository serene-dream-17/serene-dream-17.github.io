/* ============================================================
   阅读设置：字体 / 字号 / 行距
   ============================================================ */
(function () {
  "use strict";

  var KEY = "archive-reading";
  var root = document.documentElement;
  var panel = document.getElementById("fontPanel");
  var toggle = document.querySelector(".font-toggle");
  if (!panel || !toggle) return;

  var defaults = { font: "sans", size: "m", line: "normal" };
  var current = Object.assign({}, defaults);
  var lastFocus = null;

  try {
    current = Object.assign(current, JSON.parse(localStorage.getItem(KEY) || "{}"));
  } catch (e) {}

  function apply() {
    root.dataset.font = current.font;
    root.dataset.size = current.size;
    root.dataset.line = current.line;

    panel.querySelectorAll("[data-font]").forEach(function (btn) {
      btn.setAttribute("aria-pressed", btn.dataset.font === current.font ? "true" : "false");
    });
    panel.querySelectorAll("[data-size]").forEach(function (btn) {
      btn.setAttribute("aria-pressed", btn.dataset.size === current.size ? "true" : "false");
    });
    panel.querySelectorAll("[data-line]").forEach(function (btn) {
      btn.setAttribute("aria-pressed", btn.dataset.line === current.line ? "true" : "false");
    });
  }

  function save() {
    try {
      localStorage.setItem(KEY, JSON.stringify(current));
    } catch (e) {}
  }

  function open() {
    lastFocus = document.activeElement;
    panel.hidden = false;
    toggle.setAttribute("aria-expanded", "true");
    var first = panel.querySelector("[data-font]") || panel.querySelector("button");
    if (first) first.focus();
  }

  function close() {
    var wasOpen = !panel.hidden;
    panel.hidden = true;
    toggle.setAttribute("aria-expanded", "false");
    if (wasOpen && lastFocus && lastFocus.focus) lastFocus.focus();
    else if (wasOpen) toggle.focus();
  }

  toggle.addEventListener("click", function () {
    if (panel.hidden) open();
    else close();
  });

  panel.querySelectorAll("[data-font]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      current.font = btn.dataset.font;
      apply(); save();
    });
  });

  panel.querySelectorAll("[data-size]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      current.size = btn.dataset.size;
      apply(); save();
    });
  });

  panel.querySelectorAll("[data-line]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      current.line = btn.dataset.line;
      apply(); save();
    });
  });

  var closeBtn = panel.querySelector("[data-font-close]");
  if (closeBtn) closeBtn.addEventListener("click", close);

  var reset = panel.querySelector("[data-font-reset]");
  if (reset) {
    reset.addEventListener("click", function () {
      current = Object.assign({}, defaults);
      apply(); save();
    });
  }

  document.addEventListener("click", function (e) {
    if (panel.hidden) return;
    if (panel.contains(e.target) || toggle.contains(e.target)) return;
    close();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !panel.hidden) {
      close();
      return;
    }
    if (e.key === "Tab" && !panel.hidden) {
      var list = Array.prototype.slice.call(
        panel.querySelectorAll('a[href], button:not([disabled]), input, select, textarea')
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
    }
  });

  apply();
})();

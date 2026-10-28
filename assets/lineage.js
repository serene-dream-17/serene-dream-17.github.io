/* ============================================================
   语言谱系图交互：筛选 / 悬停 / 点击
   ============================================================ */
(function () {
  "use strict";

  var svg = document.querySelector(".lineage-graph");
  if (!svg) return;
  var tip = document.getElementById("lineageTip");
  var wrap = document.querySelector(".lineage-wrap");
  var count = document.getElementById("lineageCount");
  var nodes = Array.prototype.slice.call(svg.querySelectorAll(".lineage-node"));
  var edges = Array.prototype.slice.call(svg.querySelectorAll(".lineage-edge"));
  var activeFilter = new URLSearchParams(window.location.search).get("f") || "all";

  function syncURL(push) {
    var p = new URLSearchParams(window.location.search);
    if (activeFilter && activeFilter !== "all") p.set("f", activeFilter);
    else p.delete("f");
    var qs = p.toString();
    var url = window.location.pathname + (qs ? "?" + qs : "") + window.location.hash;
    if (push) history.pushState(null, "", url);
    else history.replaceState(null, "", url);
  }

  var labels = {};
  var names = {};
  nodes.forEach(function (n) { names[n.dataset.slug] = n.dataset.name || n.dataset.slug; });
  try {
    var raw = document.getElementById("lineageEdges");
    if (raw) {
      JSON.parse(raw.textContent).forEach(function (e) {
        labels[e.from + ">" + e.to] = e.label;
      });
    }
  } catch (e) {}

  function applyFilter() {
    var shown = 0;
    nodes.forEach(function (n) {
      var ok = activeFilter === "all" || n.dataset.family === activeFilter;
      n.classList.toggle("is-dim", !ok);
      if (ok) shown++;
    });
    edges.forEach(function (edge) {
      var a = edge.dataset.from;
      var b = edge.dataset.to;
      var na = nodeBySlug(a);
      var nb = nodeBySlug(b);
      var ok = (!na || !nb) ? false :
        (activeFilter === "all" || (na.dataset.family === activeFilter && nb.dataset.family === activeFilter));
      edge.classList.toggle("is-dim", !ok);
    });
    if (count) {
      count.textContent = activeFilter === "all"
        ? nodes.length + " 个节点 · " + edges.length + " 条边"
        : shown + " 个节点 · " + edges.filter(function (e) { return !e.classList.contains("is-dim"); }).length + " 条边";
    }
  }

  function nodeBySlug(slug) {
    for (var i = 0; i < nodes.length; i++) {
      if (nodes[i].dataset.slug === slug) return nodes[i];
    }
    return null;
  }

  function hot(slug) {
    edges.forEach(function (edge) {
      edge.classList.toggle("is-hot",
        edge.dataset.from === slug || edge.dataset.to === slug);
    });
  }

  function clearHot() {
    edges.forEach(function (edge) { edge.classList.remove("is-hot"); });
  }

  function showTip(node, event) {
    if (!tip) return;
    var slug = node.dataset.slug;
    var name = node.getAttribute("aria-label") || slug;
    var incoming = [];
    var outgoing = [];
    edges.forEach(function (e) {
      if (e.dataset.to === slug) incoming.push(names[e.dataset.from] || e.dataset.from);
      if (e.dataset.from === slug) outgoing.push(names[e.dataset.to] || e.dataset.to);
    });
    tip.innerHTML =
      "<b>" + escapeHtml(name) + "</b><br>" +
      (incoming.length ? "源自：" + escapeHtml(incoming.slice(0, 4).join("、")) + "<br>" : "") +
      (outgoing.length ? "影响：" + escapeHtml(outgoing.slice(0, 4).join("、")) : "点击进入档案");
    tip.hidden = false;
    var rect = wrap.getBoundingClientRect();
    var x = event.clientX - rect.left + 14;
    var y = event.clientY - rect.top + 14;
    tip.style.left = Math.min(x, wrap.clientWidth - 290) + "px";
    tip.style.top = y + "px";
  }

  function escapeHtml(s) {
    var d = document.createElement("div");
    d.textContent = s == null ? "" : String(s);
    return d.innerHTML;
  }

  nodes.forEach(function (node) {
    node.addEventListener("mouseenter", function (e) { hot(node.dataset.slug); showTip(node, e); });
    node.addEventListener("mousemove", function (e) { showTip(node, e); });
    node.addEventListener("mouseleave", function () { clearHot(); if (tip) tip.hidden = true; });
    node.addEventListener("focus", function () {
      hot(node.dataset.slug);
      if (tip) {
        tip.textContent = node.getAttribute("aria-label") || "";
        tip.hidden = false;
      }
    });
    node.addEventListener("blur", function () { clearHot(); if (tip) tip.hidden = true; });
    node.addEventListener("click", function () {
      window.location.href = "langs/" + node.dataset.slug + ".html";
    });
    node.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        window.location.href = "langs/" + node.dataset.slug + ".html";
      }
    });
  });

  document.querySelectorAll("[data-lineage-filter]").forEach(function (btn) {
    if (btn.dataset.lineageFilter === activeFilter) {
      document.querySelectorAll("[data-lineage-filter]").forEach(function (b) {
        b.setAttribute("aria-pressed", b === btn ? "true" : "false");
      });
    }
    btn.addEventListener("click", function () {
      activeFilter = btn.dataset.lineageFilter;
      document.querySelectorAll("[data-lineage-filter]").forEach(function (b) {
        b.setAttribute("aria-pressed", b === btn ? "true" : "false");
      });
      applyFilter();
      syncURL(true);
    });
  });

  applyFilter();
  window.addEventListener("popstate", function () { window.location.reload(); });
})();

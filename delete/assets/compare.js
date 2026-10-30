/* ============================================================
   跨语言 / 跨框架对比器
   数据：window.ARCHIVE_COMPARE（build.py 生成）
   ============================================================ */
(function () {
  "use strict";

  var data = window.ARCHIVE_COMPARE;
  if (!data) return;

  var mode = "language";
  var selects = [
    document.getElementById("cmp1"),
    document.getElementById("cmp2"),
    document.getElementById("cmp3")
  ];
  var tableWrap = document.getElementById("cmpTableWrap");
  var count = document.getElementById("cmpCount");
  if (!selects[0] || !tableWrap) return;

  var presets = {
    web: { mode: "framework", values: ["python|Django", "ruby|Rails", "java|Spring Boot"] },
    frontend: { mode: "framework", values: ["javascript|React", "javascript|Vue", "typescript|Angular"] },
    mobile: { mode: "framework", values: ["swift|SwiftUI", "kotlin|Jetpack Compose", "dart|Flutter"] },
    data: { mode: "framework", values: ["python|PyTorch", "scala|Apache Spark", "julia|Flux"] },
    systems: { mode: "language", values: ["c", "rust", "go"] },
    science: { mode: "language", values: ["fortran", "julia", "r"] }
  };

  var langDefaults = ["python", "go", "rust"];
  var fwDefaults = [
    ["python", "Django"],
    ["ruby", "Rails"],
    ["java", "Spring Boot"]
  ];

  function e(s) {
    var d = document.createElement("div");
    d.textContent = s == null ? "" : String(s);
    return d.innerHTML;
  }

  function options() {
    if (mode === "language") {
      return data.languages.slice().sort(function (a, b) {
        return a.year - b.year;
      }).map(function (l) {
        return { value: l.slug, label: l.name + " · " + l.year };
      });
    }
    return data.frameworks.slice().sort(function (a, b) {
      if (a.lang === b.lang) return a.name.localeCompare(b.name);
      return a.lang.localeCompare(b.lang);
    }).map(function (f) {
      return { value: f.slug + "|" + f.name, label: f.lang + " · " + f.name };
    });
  }

  function populateSelects() {
    var opts = options();
    selects.forEach(function (sel, i) {
      sel.innerHTML = '<option value="">— 不选 —</option>' + opts.map(function (o) {
        return '<option value="' + e(o.value) + '">' + e(o.label) + "</option>";
      }).join("");
    });
    if (mode === "language") {
      selects.forEach(function (sel, i) { sel.value = langDefaults[i] || ""; });
    } else {
      selects.forEach(function (sel, i) {
        var d = fwDefaults[i];
        sel.value = d ? d[0] + "|" + d[1] : "";
      });
    }
  }

  function selected() {
    return selects.map(function (s) { return s.value; }).filter(Boolean).map(function (v) {
      if (mode === "language") return data.languages.find(function (l) { return l.slug === v; });
      var parts = v.split("|");
      return data.frameworks.find(function (f) { return f.slug === parts[0] && f.name === parts[1]; });
    }).filter(Boolean);
  }

  function row(label, values) {
    return "<tr><th scope=\"row\">" + e(label) + "</th>" + values.map(function (v) {
      return "<td>" + (v == null || v === "" ? "<span class=\"cmp-none\">—</span>" : v) + "</td>";
    }).join("") + "</tr>";
  }

  function renderLanguage(items) {
    var titles = items.map(function (l) {
      return '<a href="languages/' + l.slug + '.html">' + e(l.name) + "</a>";
    });
    var head = "<thead><tr><th scope=\"col\">属性</th>" + titles.map(function (t) {
      return "<th scope=\"col\">" + t + "</th>";
    }).join("") + "</tr></thead>";

    var featureKeys = ["类型", "内存", "并发", "元编程"];
    var rows = [
      row("年份", items.map(function (l) { return l.year; })),
      row("家族", items.map(function (l) { return e(l.family_label); })),
      row("中文名", items.map(function (l) { return e(l.cn); })),
    ];
    featureKeys.forEach(function (key) {
      rows.push(row(key, items.map(function (l) {
        return e((l.deep.features || {})[key] || "");
      })));
    });
    rows.push(row("设计目标", items.map(function (l) {
      return (l.deep.goals || []).map(e).join("；");
    })));
    rows.push(row("关键取舍", items.map(function (l) {
      return (l.deep.tradeoffs || []).map(e).join("；");
    })));
    rows.push(row("版本里程碑", items.map(function (l) {
      return (l.deep.timeline || []).map(function (t) {
        return e(t[0]) + " " + e(t[1]);
      }).join(" → ");
    })));
    rows.push(row("代表项目", items.map(function (l) {
      return (l.deep.projects || []).map(e).join(" · ");
    })));
    rows.push(row("包管理", items.map(function (l) { return e(l.deep.packages); })));
    rows.push(row("现状", items.map(function (l) { return e(l.deep.status); })));
    return head + "<tbody>" + rows.join("") + "</tbody>";
  }

  function renderFramework(items) {
    var titles = items.map(function (f) {
      return '<a href="frameworks/' + f.slug + '.html#' + f.anchor + '">' +
        e(f.name) + "</a>";
    });
    var head = "<thead><tr><th scope=\"col\">属性</th>" + titles.map(function (t) {
      return "<th scope=\"col\">" + t + "</th>";
    }).join("") + "</tr></thead>";

    var rows = [
      row("语言", items.map(function (f) {
        return '<a href="languages/' + f.slug + '.html">' + e(f.lang) + "</a>";
      })),
      row("类型", items.map(function (f) { return e(f.type); })),
      row("年份", items.map(function (f) { return f.year; })),
      row("学习曲线", items.map(function (f) { return e(f.learn); })),
      row("生态", items.map(function (f) { return e(f.eco); })),
      row("许可证", items.map(function (f) { return e(f.license); })),
      row("定位", items.map(function (f) { return e(f.tagline); })),
      row("适用", items.map(function (f) {
        return "<ul class=\"cmp-list\">" + f.fit.map(function (x) { return "<li>" + e(x) + "</li>"; }).join("") + "</ul>";
      })),
      row("不适用", items.map(function (f) {
        return "<ul class=\"cmp-list\">" + f.avoid.map(function (x) { return "<li>" + e(x) + "</li>"; }).join("") + "</ul>";
      })),
      row("最小产物链", items.map(function (f) {
        return f.chain.map(e).join(" → ");
      })),
      row("代表", items.map(function (f) { return f.projects.map(e).join(" · "); })),
      row("替代", items.map(function (f) {
        return f.alternatives.map(function (a) { return e(a[0]) + "（" + e(a[1]) + "）"; }).join("；");
      })),
      row("同语言分工", items.map(function (f) { return e(f.division); })),
    ];
    return head + "<tbody>" + rows.join("") + "</tbody>";
  }

  function syncURL(push) {
    var p = new URLSearchParams(window.location.search);
    p.set("m", mode);
    var vals = selects.map(function (s) { return s.value; });
    ["a", "b", "c"].forEach(function (k, i) {
      if (vals[i]) p.set(k, vals[i]);
      else p.delete(k);
    });
    var qs = p.toString();
    var url = window.location.pathname + (qs ? "?" + qs : "") + window.location.hash;
    if (push) history.pushState(null, "", url);
    else history.replaceState(null, "", url);
  }

  function restore() {
    var p = new URLSearchParams(window.location.search);
    var m = p.get("m");
    if (m === "framework" || m === "language") {
      mode = m;
      document.querySelectorAll("[data-cmp-mode]").forEach(function (b) {
        b.setAttribute("aria-pressed", b.dataset.cmpMode === mode ? "true" : "false");
      });
    }
    populateSelects();
    ["a", "b", "c"].forEach(function (k, i) {
      var v = p.get(k);
      if (v) selects[i].value = v;
    });
    render();
    syncURL(false);
  }

  function render() {
    var items = selected();
    if (count) count.textContent = items.length + " 项对比";
    if (!items.length) {
      tableWrap.innerHTML = '<p class="cmp-empty">选择至少一项开始对比。</p>';
      return;
    }
    var html = mode === "language" ? renderLanguage(items) : renderFramework(items);
    tableWrap.innerHTML = '<table class="cmp-table">' + html + "</table>";
  }

  document.querySelectorAll("[data-preset]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var preset = presets[btn.dataset.preset];
      if (!preset) return;
      mode = preset.mode;
      document.querySelectorAll("[data-cmp-mode]").forEach(function (b) {
        b.setAttribute("aria-pressed", b.dataset.cmpMode === mode ? "true" : "false");
      });
      document.querySelectorAll("[data-preset]").forEach(function (b) {
        b.setAttribute("aria-pressed", b === btn ? "true" : "false");
      });
      populateSelects();
      selects.forEach(function (sel, i) {
        sel.value = preset.values[i] || "";
      });
      render();
      syncURL(true);
    });
  });

  document.querySelectorAll("[data-cmp-mode]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      mode = btn.dataset.cmpMode;
      document.querySelectorAll("[data-cmp-mode]").forEach(function (b) {
        b.setAttribute("aria-pressed", b === btn ? "true" : "false");
      });
      document.querySelectorAll("[data-preset]").forEach(function (b) {
        b.setAttribute("aria-pressed", "false");
      });
      populateSelects();
      render();
      syncURL(true);
    });
  });

  selects.forEach(function (sel) {
    sel.addEventListener("change", function () { render(); syncURL(true); });
  });

  restore();
  window.addEventListener("popstate", function () { restore(); render(); });
})();

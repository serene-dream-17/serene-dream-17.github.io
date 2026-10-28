# -*- coding: utf-8 -*-
"""全站共用的小型 UI：阅读设置（字体控制器）。"""


def head_snippet():
    """在 CSS 之前应用本地保存的阅读设置，避免闪烁。"""
    return """<script>
try {
  var r = JSON.parse(localStorage.getItem("archive-reading") || "{}");
  var h = document.documentElement;
  if (r.font) h.dataset.font = r.font;
  if (r.size) h.dataset.size = r.size;
  if (r.line) h.dataset.line = r.line;
} catch (e) {}
</script>"""


def font_ui():
    return """<button class="font-toggle" type="button" aria-label="阅读设置" aria-expanded="false" aria-controls="fontPanel">Aa</button>
<div class="font-panel" id="fontPanel" hidden>
  <div class="font-panel__head">
    <strong>阅读设置</strong>
    <button class="font-panel__close" type="button" data-font-close aria-label="关闭">×</button>
  </div>
  <div class="font-panel__group">
    <span class="font-panel__label">字体</span>
    <div class="font-panel__opts">
      <button type="button" data-font="sans" aria-pressed="true">思源黑体</button>
      <button type="button" data-font="serif" aria-pressed="false">思源宋体</button>
      <button type="button" data-font="system" aria-pressed="false">系统字体</button>
    </div>
  </div>
  <div class="font-panel__group">
    <span class="font-panel__label">字号</span>
    <div class="font-panel__opts">
      <button type="button" data-size="s" aria-pressed="false">小</button>
      <button type="button" data-size="m" aria-pressed="true">标准</button>
      <button type="button" data-size="l" aria-pressed="false">大</button>
      <button type="button" data-size="xl" aria-pressed="false">特大</button>
    </div>
  </div>
  <div class="font-panel__group">
    <span class="font-panel__label">行距</span>
    <div class="font-panel__opts">
      <button type="button" data-line="tight" aria-pressed="false">紧凑</button>
      <button type="button" data-line="normal" aria-pressed="true">标准</button>
      <button type="button" data-line="loose" aria-pressed="false">宽松</button>
    </div>
  </div>
  <button class="font-panel__reset" type="button" data-font-reset>恢复默认</button>
</div>"""

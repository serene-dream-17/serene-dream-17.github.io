# delete — 已下线内容暂存区

这里保存已从站点下线、但可能需要恢复或追溯的页面与源码。

构建、审计与冒烟测试都不会扫描本目录。

## 当前内容

| 路径 | 来源 | 原因 |
|---|---|---|
| `security.html` | 第 23 批 | 安全专题整条线下线 |
| `tools/security_site.py`、`tools/data/security.py` | 第 23 批 | 安全页渲染器与工具数据 |
| `tools/data/security_scene.py` | 第 23 批 | 开发场景「安全」分组（4 组 / 19 条） |
| `matrix.html` | 第 23 批 | 选型地图与「技术栈」重复 |
| `tools/data/matrix_scenarios.py` | 第 23 批 | 矩阵场景数据（原 `fw_d.py` 的 `SCENARIOS` / `_EXTRA` / `_EXTRA2`） |
| `frameworks.html` | 第 23 批 | 旧矩阵跳转桩（目标已下线） |
| `lineage.html`、`tools/lineage.py`、`assets/lineage.js` | 第 23 批 | 语言谱系图下线 |
| `compare.html`、`tools/compare_index.py`、`assets/compare.js`、`assets/compare-data.js` | 第 23 批 | 对比器下线 |
| `laravel-stack.html` | 第 23 批 | 第 22 批删栈后遗留的旧生成页 |
| `view-source_https___serene-dream-17.github.io.html` | 第 23 批 | 早期网页快照，无站内入链 |

## 恢复方式

1. 把需要的文件移回原路径；
2. 在 `tools/build.py` 重新接回对应的渲染器与数据；
3. 运行 `python tools/build.py`、`python tools/audit.py`、`python tests/smoke.py`。

注意：这些页面生成时依赖的导航与搜索结果已在第 23 批移除，直接移回不会自动出现在站内入口。
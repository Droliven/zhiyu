# Quarto 最小示例

一份 Markdown 出三种产物：网页、PDF、PPTX。

## 用法

```bash
cd docs/talks/2026-11-18_quarto-demo
quarto render                    # 全部格式
quarto render slides.qmd --to pdf
quarto preview                   # 本地预览，改文件即时刷新
```

## 文件

| 文件 | 作用 |
|---|---|
| `slides.qmd` | 幻灯片，`revealjs` 出网页、`pptx` 出 PowerPoint |
| `report.qmd` | 报告页，`html` 出网页、`pdf` 出 LaTeX 排版 |
| `assets/` | 本地图片。视频不要放这里，用外链 |
| `_quarto.yml` | 项目配置，列出要渲染的源文件 |

渲染产物写在源文件旁（`slides.html`、`slides.pptx`、`report.html`、`report.pdf`），提交后 GitHub Pages 会直接发布。HTML 用 `embed-resources: true`，单文件自包含，不生成 `_files/` 目录。

## 与 Slidev 的分工

- `slides.qmd`：报告类幻灯片，要 PDF 或 PPTX 交付时用这个。
- `reports/robodojo-slidev`：现场演示、需要代码交互和动画时用 Slidev。

## 环境

Quarto 1.11.9 装在 `~/.local/quarto`，`~/.local/bin/quarto` 是指向它的软链接（该目录已在 `PATH` 中）。PDF 走系统 TeX Live，`/Library/TeX/texbin`。

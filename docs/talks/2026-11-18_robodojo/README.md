# RoboDojo 汇报（2026-11-18）

Slidev 汇报稿源文件与构建说明。正文阅读版见 [汇报正文.md](汇报正文.md)，站点入口在知域“专题报告”列表。

## 目录内容

| 文件 | 用途 |
| --- | --- |
| `slides.md` | 22 页幻灯片源稿（含演讲者备注） |
| `style.css` | 版式与配色，不依赖外部字体文件 |
| `public/media/` | 6 个实际引用的素材：`vpp.png`、`plug-approach.jpg`、`plug-align.jpg`、`plug-seated.jpg`、`alignment.webm`、`alignment.webp` |
| `汇报正文.md` | 知域报告阅读视图使用的 Markdown 正文 |

## 重新构建

在装有 Slidev 依赖的目录执行（`reports/robodojo-slidev` 已包含 `node_modules`）：

```bash
npx slidev build docs/talks/2026-11-18_robodojo/slides.md \
  --base /zhiyu/slides/robodojo-2026-11/ \
  --out slides/robodojo-2026-11
```

要点：

- `--base` 必须带仓库前缀 `/zhiyu/`，否则 GitHub Pages 项目站点下资源路径会 404。
- 产物落在 `slides/robodojo-2026-11/`，需要提交；不要放 `dist/`，该目录被 `.gitignore` 忽略。
- 本地预览用 `npx slidev docs/talks/2026-11-18_robodojo/slides.md`，无需设置 base。
- 修改 `slides.md` 或 `style.css` 后必须重新构建并提交产物，站点展示的是构建结果。

## 已知边界

- 幻灯片是单页应用，翻页使用 history 路由（`/slides/robodojo-2026-11/3`）。直接访问单页链接会触发 `404.html`，回退到放映首页而不是对应页码。
- 版式使用系统字体（Inter、PingFang SC），不同设备字形略有差异；未打包字体文件以控制体积。
- 当前构建产物约 2.6 MB，其中视频与图片 1.4 MB，JS 与 CSS gzip 后约 290 KB。

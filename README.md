# 知域

知域是一个可独立部署到 GitHub Pages 的纯静态研究知识库。当前数据由 7 份 Markdown 论文报告合并生成，包含 43 篇去重后的论文与完整专题报告阅读视图。

本项目按独立 Git 仓库设计。下文所有路径和命令都相对于仓库根目录，不依赖其他项目或外部 `sys_docs`。

## 本地预览

网站通过 `fetch()` 读取 JSON 和 Markdown，请用本地 HTTP 服务预览：

```bash
# 替换为你在本机克隆知域仓库的实际路径
cd /path/to/zhiyu
test -f index.html && test -d scripts && echo "已进入知域仓库根目录"
python3 -m http.server 8080
```

打开 `http://localhost:8080/`。

## 增量导入

把新的 AI 论文报告复制进文献库并重建数据：

```bash
python3 scripts/ingest_reports.py --copy /absolute/path/to/new_report.md
python3 scripts/enrich_arxiv.py
python3 scripts/validate_data.py
```

导入器会扫描 `content/reports/*.md`，并按以下优先级合并重复论文：

1. arXiv ID；
2. DOI；
3. 规范化标题（忽略大小写、标点和空格）。

已存在的评论、删除标记和人工字段不会被导入器覆盖。新报告必须遵循 [CONTRIBUTING.md](CONTRIBUTING.md) 中的检索、证据和标题层级规则，并在每篇论文段落中保留 Insight、Pipeline、实验、开放情况与局限等小节。

## 团队贡献

用户先 `cd` 到包含 `index.html`、`data/`、`content/` 和 `scripts/` 的知域仓库根目录，在终端同步主分支并创建工作分支，再把站内 README 提供的提示词交给 AI。AI 负责检索、编辑、重建数据和运行校验，但停在未提交状态。用户检查 `git diff` 后，亲自选择文件、创建 commit、push 分支并发起 Pull Request。

不要让 AI 自动执行 `git add`、`git commit` 或 `git push`，也不要使用 `git add .` 将未审阅的工作区内容一起提交。

## 评论与软删除

网站中的评论和“隐藏”操作先保存在浏览器 `localStorage`。在“数据维护”页点击“导出本地修改”，会得到 `paper_overrides.json`。用它替换 `data/paper_overrides.json` 并提交后，修改会随网站永久发布。

覆盖文件格式：

```json
{
  "arxiv-2602-11389": {
    "deleted": true,
    "comments": "值得复现 object masking 消融。"
  }
}
```

## 数据文件

- `data/papers.json`：合并后的论文记录；稳定 ID 优先使用 `arxiv-YYMM-NNNNN`。
- `data/reports.json`：专题报告索引及其关联论文 ID。
- `data/paper_overrides.json`：人工评论、隐藏标记及字段修订。
- `content/reports/`：可直接阅读的原始 Markdown 报告。
- `content/images/`：经过筛选的本地配图。目前 4 张图合计约 476 KB。

论文原图默认使用原论文 HTML 或项目页的远程地址，并在详情页懒加载，不占用仓库空间。新增本地图片前运行：

```bash
python3 scripts/check_asset_budget.py
```

单张图片默认不应超过 500 KB，本地图像总量默认不应超过 25 MB。建议最长边不超过 1600 px，并优先保存为 WebP；任何配图都必须保留论文名、图号和来源链接。

## GitHub Pages

独立仓库的 Pages workflow 会校验数据并将仓库根目录 `.` 作为 Pages artifact 发布。第一次运行 workflow 前，仓库管理员必须完成一次启用：

1. 打开 GitHub 仓库的 **Settings → Pages**。
2. 在 **Build and deployment** 下，将 **Source** 设为 **GitHub Actions**。
3. 回到 **Actions → Deploy Zhiyu**，点击 **Re-run all jobs**，或在 workflow 页面手动运行。

如果 `actions/configure-pages` 报 `Get Pages site failed` 和 `404 Not Found`，说明 GitHub 尚未为该仓库创建 Pages site，通常就是上面的 Source 尚未设置。Node 20 deprecation 信息只是 GitHub Runner 将旧 Action 自动运行在 Node 24 上的迁移提示，不是本次部署失败原因；不要设置 `ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION=true` 回退到 Node 20。

不建议直接给 `configure-pages` 添加 `enablement: true`：该选项不能使用默认 `GITHUB_TOKEN` 自动启用站点，需要额外的 Personal Access Token 或 GitHub App 管理权限。团队仓库采用一次性 UI 启用更简单，也更安全。

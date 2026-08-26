#!/usr/bin/env python3
"""Validate generated paper-library JSON and duplicate identities."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    papers = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
    reports = json.loads((ROOT / "data" / "reports.json").read_text(encoding="utf-8"))
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    index_html = (ROOT / "index.html").read_text(encoding="utf-8")
    required = {
        "id",
        "title",
        "year",
        "publication",
        "links",
        "tags",
        "summary",
        "pipeline",
        "code_data_status",
        "limitations",
    }
    errors: list[str] = []
    for index, paper in enumerate(papers):
        missing = sorted(required - paper.keys())
        if missing:
            errors.append(f"paper[{index}] missing {', '.join(missing)}")
        paper_url = paper.get("links", {}).get("paper") or paper.get("links", {}).get("publication")
        if not paper_url:
            errors.append(f"{paper.get('id')}: no paper/publication URL")
        if paper.get("arxiv_id") and not re.fullmatch(r"\d{4}\.\d{4,5}", paper["arxiv_id"]):
            errors.append(f"{paper.get('id')}: invalid arXiv id")

    for field in ("id", "arxiv_id"):
        values = [paper.get(field) for paper in papers if paper.get(field)]
        duplicates = [value for value, count in Counter(values).items() if count > 1]
        if duplicates:
            errors.append(f"duplicate {field}: {duplicates}")

    report_ids = {report["id"] for report in reports}
    paper_ids = {paper["id"] for paper in papers}
    for paper in papers:
        unknown = set(paper.get("source_reports", [])) - report_ids
        if unknown:
            errors.append(f"{paper['id']}: unknown reports {sorted(unknown)}")
        figure = paper.get("figure")
        if figure and not figure.get("url", "").startswith("http"):
            figure_path = ROOT / figure["url"]
            if not figure_path.exists():
                errors.append(f"{paper['id']}: missing local figure {figure['url']}")
        elif figure:
            url = figure.get("url", "")
            if url.startswith("http") and not re.search(
                r"\.(?:png|jpe?g|gif|webp|svg)(?:\?|#|$)", url, flags=re.I
            ):
                errors.append(f"{paper['id']}: figure.url is not a direct image file: {url}")
        for tag in paper.get("tags", []):
            if any(bracket in tag for bracket in "[]【】"):
                errors.append(f"{paper['id']}: malformed tag contains brackets: {tag}")

    for report in reports:
        report_path = ROOT / report["path"]
        if not report_path.exists():
            errors.append(f"{report['id']}: missing report {report['path']}")
        for tag in report.get("tags", []):
            if any(bracket in tag for bracket in "[]【】"):
                errors.append(f"{report['id']}: malformed tag contains brackets: {tag}")
        unknown_papers = set(report.get("paper_ids", [])) - paper_ids
        if unknown_papers:
            errors.append(f"{report['id']}: unknown papers {sorted(unknown_papers)}")

    readme_modes = (
        "方式一：直接检索论文",
        "方式二：整理指定列表",
        "方式三：专题检索综述",
        "方式四：固定周期周报",
    )
    for mode in readme_modes:
        if mode not in readme:
            errors.append(f"README missing AI mode: {mode}")
    for prompt_id in ("prompt-search", "prompt-list", "prompt-survey", "prompt-weekly"):
        if f'id="{prompt_id}"' not in index_html:
            errors.append(f"web README missing prompt module: {prompt_id}")
    shared_prompts = (
        "方式一：让 AI 直接检索论文",
        "方式二：提供论文列表，让 AI 细化整理",
        "方式三：专题检索与综述报告",
    )
    for title in shared_prompts:
        pattern = rf"<summary><strong>{re.escape(title)}</strong></summary>[\s\S]*?```text\s*\n([\s\S]*?)\n```"
        match = re.search(pattern, readme)
        if not match or len(match.group(1).strip()) < 500:
            errors.append(f"README shared prompt missing or incomplete: {title}")
        if f'data-readme-prompt="{title}"' not in index_html:
            errors.append(f"web README is not linked to shared prompt: {title}")
    if "**报告标签**：[" in index_html:
        errors.append("web README prompt uses bracketed report tags")
    weekly_prompt = re.search(
        r"<summary><strong>方式四：每周论文自动抓取</strong></summary>[\s\S]*?```text\s*\n([\s\S]*?)\n```",
        readme,
    )
    if not weekly_prompt:
        errors.append("README weekly prompt cannot be extracted by the web module")
    elif not all(
        marker in weekly_prompt.group(1)
        for marker in ("# 角色与唯一交付物", "# 无新增结果")
    ):
        errors.append("README weekly prompt is incomplete")
    ordered_sections = (
        "## 网页功能与数据边界",
        "## 团队贡献",
        "## AI 更新模式",
        "<summary><strong>方式一：让 AI 直接检索论文</strong></summary>",
        "<summary><strong>方式二：提供论文列表，让 AI 细化整理</strong></summary>",
        "<summary><strong>方式三：专题检索与综述报告</strong></summary>",
        "<summary><strong>方式四：每周论文自动抓取</strong></summary>",
        "## 增量导入",
        "## 本地预览",
        "## 审阅并提交 Pull Request",
        "## 评论与软删除",
    )
    positions = [readme.find(section) for section in ordered_sections]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        errors.append("README workflow sections are out of order")

    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated {len(papers)} papers and {len(reports)} reports.")


if __name__ == "__main__":
    main()

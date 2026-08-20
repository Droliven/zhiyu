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
    required = {"id", "title", "year", "publication", "links", "tags", "summary", "pipeline"}
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

    for report in reports:
        report_path = ROOT / report["path"]
        if not report_path.exists():
            errors.append(f"{report['id']}: missing report {report['path']}")
        unknown_papers = set(report.get("paper_ids", [])) - paper_ids
        if unknown_papers:
            errors.append(f"{report['id']}: unknown papers {sorted(unknown_papers)}")

    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated {len(papers)} papers and {len(reports)} reports.")


if __name__ == "__main__":
    main()

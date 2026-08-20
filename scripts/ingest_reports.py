#!/usr/bin/env python3
"""Build the static paper library data from Markdown reading reports."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "content" / "reports"
DATA_DIR = ROOT / "data"
PAPERS_PATH = DATA_DIR / "papers.json"
REPORTS_PATH = DATA_DIR / "reports.json"

PROFILES = {
    "world_model_causality_counterfactual_survey_2026-08-20.md": {
        "level": 2,
        "tags": ["因果世界模型", "反事实推理", "对象中心"],
    },
    "causal_world_models_2026_survey.md": {
        "level": 2,
        "tags": ["因果世界模型", "反事实推理"],
    },
    "causal_world_models_2026_survey.original.md": {
        "level": 1,
        "tags": ["因果世界模型", "反事实推理"],
    },
    "wam_paper_reading_summary.md": {
        "level": 2,
        "tags": ["World Action Model", "机器人学习", "预测表征"],
    },
    "paper_reading_summary.md": {
        "level": 2,
        "tags": ["交互世界模型", "HOI"],
    },
    "hoi_world_model_3d4d_report.md": {
        "level": 1,
        "tags": ["HOI", "3D/4D", "第一视角"],
    },
    "geometric_consistency_video_generation_report.md": {
        "level": 1,
        "tags": ["几何一致性", "视频生成", "3D/4D"],
    },
}

SKIP_TITLE_PARTS = (
    "快速定位",
    "总体结论",
    "先给结论",
    "分类脉络",
    "分类梳理",
    "横向",
    "建议的研究",
    "推荐阅读",
    "补充推荐",
    "额外推荐",
    "关键数据集",
    "研究脉络",
    "总结",
    "最终结论",
    "一句话",
    "最适合你",
    "给 hand-object",
    "对“2D",
    "对 3D/4D",
    "最新值得跟踪",
    "奠基性工作",
)

FORMAL_HOSTS = (
    "openreview.net",
    "proceedings.",
    "openaccess.thecvf.com",
    "ojs.aaai.org",
    "papers.neurips.cc",
    "deepmind.google",
    "dl.acm.org",
    "ieeexplore.ieee.org",
)


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def normalized_title(title: str) -> str:
    title = title.replace("—", ":").replace("–", ":")
    return re.sub(r"[^a-z0-9]+", "", title.casefold())


def plain_text(markdown: str) -> str:
    text = re.sub(r"```.*?```", " ", markdown, flags=re.S)
    text = re.sub(r"!\[([^]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[#>*_`|\\]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def first_paragraph(markdown: str, limit: int = 420) -> str:
    paragraphs = [plain_text(part) for part in re.split(r"\n\s*\n", markdown)]
    text = next((part for part in paragraphs if len(part) > 20), "")
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def field_value(section: str, labels: tuple[str, ...]) -> str:
    label_pattern = "|".join(re.escape(label) for label in labels)
    pattern = re.compile(
        rf"(?mi)^\s*(?:-\s*)?\*\*(?:{label_pattern})(?:[：:])?\*\*\s*[：:]?\s*(.+?)\s*$"
    )
    match = pattern.search(section)
    return plain_text(match.group(1)) if match else ""


def major_marker(line: str) -> str | None:
    value = re.sub(r"^#{1,5}\s+", "", line.strip())
    value = value.strip("* ")
    lowered = value.casefold()
    if "核心概括" in value or lowered == "insight" or lowered.startswith("insight "):
        return "insight"
    if lowered.startswith("pipeline") or value.startswith("流程"):
        return "pipeline"
    if value.startswith("实验") or "实验与证据" in value or lowered.startswith("experiments"):
        return "experiments"
    if "开放情况与局限" in value:
        return "open_and_limits"
    if "代码与数据" in value or "代码/数据" in value:
        return "code_data"
    if value.startswith("局限") or "失败案例" in value:
        return "limitations"
    if value.startswith("主张、证据"):
        return "evidence"
    return None


def extract_segments(section: str) -> dict[str, str]:
    lines = section.splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        marker = major_marker(line)
        if marker:
            starts.append((index, marker))

    segments: dict[str, str] = {}
    for position, (start, marker) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        body = "\n".join(lines[start + 1 : end]).strip()
        if body:
            segments[marker] = body

    if "open_and_limits" in segments:
        segments.setdefault("code_data", segments["open_and_limits"])
        segments.setdefault("limitations", segments["open_and_limits"])
    return segments


def extract_pipeline(markdown: str) -> dict[str, str]:
    fields: dict[str, str] = {"input": "", "process": "", "output": "", "details": markdown}
    label_map = {
        "input": ("输入", "Input"),
        "process": ("过程", "处理", "主要处理流程", "Process"),
        "output": ("输出", "Output", "推理期输出"),
    }
    for key, labels in label_map.items():
        for label in labels:
            match = re.search(
                rf"(?mi)^\s*(?:-\s*|\d+\.\s*)?\*\*{re.escape(label)}\*\*[：:]?\s*(.+)$",
                markdown,
            )
            if match:
                fields[key] = plain_text(match.group(1))
                break

    table_rows = []
    for line in markdown.splitlines():
        if line.strip().startswith("|") and "---" not in line:
            cells = [plain_text(cell) for cell in line.strip().strip("|").split("|")]
            if cells and not any(label in cells[0] for label in ("环节", "输入")):
                table_rows.append(cells)
    if table_rows:
        if not fields["input"]:
            fields["input"] = "；".join(row[1] for row in table_rows if len(row) > 1)
        if not fields["process"]:
            fields["process"] = "；".join(row[2] for row in table_rows if len(row) > 2)
        if not fields["output"]:
            fields["output"] = "；".join(row[-1] for row in table_rows if len(row) > 2)

    bullets = [plain_text(line) for line in markdown.splitlines() if re.match(r"^\s*-\s+", line)]
    if not fields["input"] and bullets:
        fields["input"] = bullets[0]
    if not fields["process"] and len(bullets) > 1:
        fields["process"] = "；".join(bullets[1:-1] or bullets[1:2])
    if not fields["output"] and len(bullets) > 2:
        fields["output"] = bullets[-1]
    return fields


def classify_links(section: str, arxiv_id: str) -> dict[str, str]:
    links: dict[str, str] = {}
    for label, url in re.findall(r"\[([^]]+)\]\((https?://[^)]+)\)", section):
        lower_label = label.casefold()
        lower_url = url.casefold()
        if "arxiv.org/abs/" in lower_url:
            links.setdefault("paper", url)
        elif any(host in lower_url for host in FORMAL_HOSTS):
            links.setdefault("publication", url)
        elif "github.com" in lower_url or "code" in lower_label or "代码" in label:
            links.setdefault("code", url)
            if "data" in lower_label or "数据" in label:
                links.setdefault("data", url)
        elif "/datasets/" in lower_url or "dataset" in lower_label or "数据" in label:
            links.setdefault("data", url)
        elif "huggingface.co" in lower_url or "model" in lower_label or "权重" in label:
            links.setdefault("model", url)
        elif "project" in lower_label or "项目" in label or "github.io" in lower_url:
            links.setdefault("project", url)

    if arxiv_id:
        links.setdefault("paper", f"https://arxiv.org/abs/{arxiv_id}")
        links.setdefault("alphaxiv", f"https://alphaxiv.org/abs/{arxiv_id}")
    return links


def infer_tags(title: str, section: str, base_tags: list[str]) -> list[str]:
    haystack = f"{title}\n{section}".casefold()
    tags = set(base_tags)
    keyword_tags = {
        "causal": "因果推理",
        "counterfactual": "反事实推理",
        "hand-object": "HOI",
        "hand object": "HOI",
        "egocentric": "第一视角",
        "world action": "World Action Model",
        "4d": "3D/4D",
        "3d": "3D/4D",
        "geometry": "几何一致性",
        "geometric": "几何一致性",
        "video generation": "视频生成",
        "video diffusion": "视频生成",
        "robot": "机器人学习",
        "vision-language-action": "VLA",
        "vla": "VLA",
        "reconstruction": "重建",
        "point map": "重建",
        "affordance": "可供性",
        "motion generation": "动作生成",
    }
    for keyword, tag in keyword_tags.items():
        if keyword in haystack:
            tags.add(tag)
    return sorted(tags, key=str.casefold)


def extract_figure(section: str, title: str) -> dict[str, str] | None:
    image = re.search(r"!\[([^]]*)\]\(([^)]+)\)", section)
    if not image:
        return None
    alt, url = image.groups()
    if url.startswith("causal_world_models_assets/") or url.startswith("../images/"):
        url = "content/images/" + Path(url).name
    label = field_value(section, ("代表图",))
    source_match = re.search(r"来源[：:]\s*\[([^]]+)\]\((https?://[^)]+)\)", section)
    source_url = source_match.group(2) if source_match else ""
    if not source_url and url.startswith("http"):
        source_url = url
    return {
        "url": url,
        "alt": alt or f"{title} representative figure",
        "label": label or alt,
        "paper_title": title,
        "source_url": source_url,
    }


def split_paper_sections(text: str, level: int) -> list[tuple[str, str]]:
    marker = re.compile(rf"(?m)^{'#' * level}\s+(\d+)[\.:]?\s+(.+?)\s*$")
    matches = list(marker.finditer(text))
    sections = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((match.group(2).strip(), text[match.end() : end].strip()))
    return sections


def make_id(title: str, arxiv_id: str, doi: str = "") -> str:
    if arxiv_id:
        return "arxiv-" + arxiv_id.replace(".", "-")
    if doi:
        return "doi-" + re.sub(r"[^a-z0-9]+", "-", doi.casefold()).strip("-")
    digest = hashlib.sha1(normalized_title(title).encode("utf-8")).hexdigest()[:10]
    return f"paper-{digest}"


def parse_paper(title: str, section: str, profile: dict[str, Any], report_id: str) -> dict[str, Any] | None:
    if any(part.casefold() in title.casefold() for part in SKIP_TITLE_PARTS):
        return None
    if not re.search(r"arxiv\.org/abs/|openreview\.net|proceedings\.|openaccess\.thecvf|ojs\.aaai", section):
        return None

    arxiv_match = re.search(r"arxiv\.org/(?:abs|html)/(\d{4}\.\d{4,5})", section)
    arxiv_id = arxiv_match.group(1) if arxiv_match else ""
    doi_match = re.search(r"doi\.org/([^\s)]+)", section)
    doi = doi_match.group(1) if doi_match else ""
    publication = field_value(section, ("年份与发表", "发表情况", "发表", "年份"))
    year_match = re.search(r"20\d{2}", publication)
    if not year_match and arxiv_id:
        year = 2000 + int(arxiv_id[:2])
    else:
        year = int(year_match.group()) if year_match else None

    segments = extract_segments(section)
    insight = segments.get("insight", "")
    pipeline_markdown = segments.get("pipeline", "")
    links = classify_links(section, arxiv_id)
    authors = field_value(section, ("作者", "Authors"))
    code_data = segments.get("code_data", "")
    if not code_data:
        status_parts = []
        if links.get("code"):
            status_parts.append("代码链接已记录")
        if links.get("data"):
            status_parts.append("数据链接已记录")
        if links.get("model"):
            status_parts.append("模型/权重链接已记录")
        code_data = "；".join(status_parts)

    record = {
        "id": make_id(title, arxiv_id, doi),
        "title": title,
        "authors": [part.strip() for part in re.split(r"[,，]", authors) if part.strip()],
        "year": year,
        "publication": publication or (f"arXiv {year}" if year else "待核验"),
        "arxiv_id": arxiv_id,
        "doi": doi,
        "links": links,
        "tags": infer_tags(title, section, profile["tags"]),
        "figure": extract_figure(section, title),
        "summary": first_paragraph(insight or section),
        "insight": insight,
        "pipeline": extract_pipeline(pipeline_markdown),
        "experiments": segments.get("experiments", ""),
        "evidence_notes": segments.get("evidence", ""),
        "code_data_status": code_data,
        "limitations": segments.get("limitations", ""),
        "comments": "",
        "source_reports": [report_id],
        "deleted": False,
        "updated_at": str(date.today()),
    }
    return record


def identity_keys(record: dict[str, Any]) -> list[str]:
    keys = ["title:" + normalized_title(record.get("title", ""))]
    if record.get("arxiv_id"):
        keys.append("arxiv:" + record["arxiv_id"])
    if record.get("doi"):
        keys.append("doi:" + record["doi"].casefold())
    return keys


def prefer_text(old: str, new: str) -> str:
    if not old:
        return new
    if not new:
        return old
    return new if len(new) > len(old) * 1.2 else old


def merge_records(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    merged = dict(old)
    for key in ("summary", "insight", "experiments", "evidence_notes", "code_data_status", "limitations"):
        merged[key] = prefer_text(old.get(key, ""), new.get(key, ""))
    for key in ("authors", "year", "publication", "arxiv_id", "doi"):
        if not merged.get(key) and new.get(key):
            merged[key] = new[key]
    if len(new.get("authors", [])) > len(merged.get("authors", [])):
        merged["authors"] = new["authors"]
    merged["links"] = {**new.get("links", {}), **old.get("links", {})}
    merged["tags"] = sorted(set(old.get("tags", [])) | set(new.get("tags", [])), key=str.casefold)
    merged["source_reports"] = sorted(set(old.get("source_reports", [])) | set(new.get("source_reports", [])))
    old_pipeline = old.get("pipeline", {})
    new_pipeline = new.get("pipeline", {})
    merged["pipeline"] = {
        key: prefer_text(old_pipeline.get(key, ""), new_pipeline.get(key, ""))
        for key in ("input", "process", "output", "details")
    }
    old_figure = old.get("figure")
    new_figure = new.get("figure")
    if not old_figure or (new_figure and not new_figure["url"].startswith("http")):
        merged["figure"] = new_figure
    for key in ("comments", "deleted"):
        if key in old:
            merged[key] = old[key]
    if merged != old:
        merged["updated_at"] = str(date.today())
    return merged


def report_summary(text: str) -> str:
    body = re.sub(r"(?m)^#.+$", "", text, count=1)
    candidates = re.findall(r"(?s)(?:^|\n)>(.+?)(?=\n\n|\n---|$)", body)
    if candidates:
        return first_paragraph(candidates[0], 360)
    return first_paragraph(body, 360)


def report_profile(path: Path, text: str) -> dict[str, Any]:
    profile = dict(PROFILES.get(path.name, {"level": 2, "tags": []}))
    tag_match = re.search(
        r"(?mi)^\s*(?:-\s*)?\*\*报告标签\*\*[：:]\s*(.+?)\s*$", text[:2000]
    )
    if tag_match:
        declared = [
            item.strip()
            for item in re.split(r"[,，、;；]", tag_match.group(1))
            if item.strip()
        ]
        profile["tags"] = sorted(set(profile.get("tags", [])) | set(declared), key=str.casefold)
    if not profile.get("tags"):
        profile["tags"] = ["未分类"]
    return profile


def build() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    existing = read_json(PAPERS_PATH, [])
    papers = list(existing)
    key_to_index: dict[str, int] = {}
    for index, paper in enumerate(papers):
        for key in identity_keys(paper):
            key_to_index[key] = index

    reports: list[dict[str, Any]] = []
    for path in sorted(REPORT_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        profile = report_profile(path, text)
        title_match = re.search(r"(?m)^#\s+(.+)$", text)
        report_title = title_match.group(1).strip() if title_match else path.stem
        report_id = "report-" + hashlib.sha1(path.name.encode("utf-8")).hexdigest()[:10]
        report_paper_ids: list[str] = []

        for paper_title, section in split_paper_sections(text, profile["level"]):
            candidate = parse_paper(paper_title, section, profile, report_id)
            if not candidate:
                continue
            matches = [key_to_index[key] for key in identity_keys(candidate) if key in key_to_index]
            if matches:
                index = matches[0]
                papers[index] = merge_records(papers[index], candidate)
            else:
                index = len(papers)
                papers.append(candidate)
            for key in identity_keys(papers[index]):
                key_to_index[key] = index
            report_paper_ids.append(papers[index]["id"])

        date_match = re.search(r"20\d{2}-\d{2}-\d{2}", text[:1000])
        reports.append(
            {
                "id": report_id,
                "title": report_title,
                "date": date_match.group() if date_match else str(date.today()),
                "tags": profile["tags"],
                "summary": report_summary(text),
                "paper_ids": sorted(set(report_paper_ids)),
                "path": f"content/reports/{path.name}",
                "source_file": path.name,
            }
        )

    papers.sort(key=lambda item: (-(item.get("year") or 0), item["title"].casefold()))
    reports.sort(key=lambda item: (item["date"], item["title"]), reverse=True)
    return papers, reports


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="*", type=Path, help="Markdown reports to add")
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy source reports into content/reports before rebuilding",
    )
    args = parser.parse_args()

    if args.sources and not args.copy:
        parser.error("use --copy when passing external source reports")
    for source in args.sources:
        if source.suffix.casefold() != ".md":
            parser.error(f"not a Markdown file: {source}")
        shutil.copy2(source, REPORT_DIR / source.name)

    papers, reports = build()
    write_json(PAPERS_PATH, papers)
    write_json(REPORTS_PATH, reports)
    print(f"Built {len(papers)} papers from {len(reports)} reports.")


if __name__ == "__main__":
    main()

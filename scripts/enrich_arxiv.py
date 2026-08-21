#!/usr/bin/env python3
"""Fill missing paper metadata from the official arXiv API."""

from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS_PATH = ROOT / "data" / "papers.json"
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"


def chunks(items: list[str], size: int) -> list[list[str]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def fetch(ids: list[str]) -> dict[str, dict[str, object]]:
    metadata: dict[str, dict[str, object]] = {}
    for batch in chunks(ids, 35):
        query = urllib.parse.urlencode({"id_list": ",".join(batch), "max_results": len(batch)})
        request = urllib.request.Request(
            "https://export.arxiv.org/api/query?" + query,
            headers={"User-Agent": "paper-library-builder/1.0 (metadata enrichment)"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            root = ET.fromstring(response.read())
        for entry in root.findall(f"{ATOM}entry"):
            id_text = entry.findtext(f"{ATOM}id", default="")
            paper_id = id_text.rsplit("/", 1)[-1].split("v", 1)[0]
            authors = [
                author.findtext(f"{ATOM}name", default="").strip()
                for author in entry.findall(f"{ATOM}author")
            ]
            category = entry.find(f"{ARXIV}primary_category")
            metadata[paper_id] = {
                "title": " ".join(entry.findtext(f"{ATOM}title", default="").split()),
                "authors": [author for author in authors if author],
                "published": entry.findtext(f"{ATOM}published", default=""),
                "revised_at": entry.findtext(f"{ATOM}updated", default=""),
                "primary_category": category.attrib.get("term", "") if category is not None else "",
                "doi": entry.findtext(f"{ARXIV}doi", default=""),
                "journal_ref": entry.findtext(f"{ARXIV}journal_ref", default=""),
            }
        if len(ids) > len(batch):
            time.sleep(3)
    return metadata


def main() -> None:
    papers = json.loads(PAPERS_PATH.read_text(encoding="utf-8"))
    ids = sorted({paper["arxiv_id"] for paper in papers if paper.get("arxiv_id")})
    metadata = fetch(ids)
    changed = 0
    for paper in papers:
        item = metadata.get(paper.get("arxiv_id", ""))
        if not item:
            continue
        before = json.dumps(paper, ensure_ascii=False, sort_keys=True)
        incoming_title = str(item["title"] or "").strip()
        current_title = str(paper.get("title") or "").strip()
        if incoming_title and not current_title:
            paper["title"] = incoming_title
        if not paper.get("authors") or len(item["authors"]) > len(paper.get("authors") or []):
            paper["authors"] = item["authors"]
        paper["arxiv"] = {
            "published": item["published"],
            "revised_at": item["revised_at"],
            "primary_category": item["primary_category"],
        }
        if not paper.get("doi") and item["doi"]:
            paper["doi"] = item["doi"]
        journal_ref = str(item["journal_ref"] or "").strip()
        if journal_ref and paper.get("publication", "").startswith("arXiv"):
            paper["publication"] = journal_ref
        if json.dumps(paper, ensure_ascii=False, sort_keys=True) != before:
            changed += 1
    PAPERS_PATH.write_text(
        json.dumps(papers, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Enriched {changed}/{len(papers)} records from arXiv.")


if __name__ == "__main__":
    main()

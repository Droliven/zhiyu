#!/usr/bin/env python3
"""Maintain data/xhs_candidates.json: frequent paper-library authors to look
up on Xiaohongshu.

    python3 scripts/xhs/candidates.py refresh [--min-papers 3]   # recount from data/papers.json
    python3 scripts/xhs/candidates.py list [--status pending]     # print the table
    python3 scripts/xhs/candidates.py set "Shanghang Zhang" --status found --user-id <24hex> [--note ...]

``refresh`` recomputes paper counts and sample titles but never overwrites the
hand-maintained fields (cn_name, affiliation, status, user_id, note). Authors
that drop below the threshold are kept if they already have manual data.
Status values: pending / found / added / not_found / skipped.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.xhs.common import dump_json, load_json, load_watchlist  # noqa: E402

PAPERS_PATH = ROOT / "data" / "papers.json"
CANDIDATES_PATH = ROOT / "data" / "xhs_candidates.json"
MANUAL_FIELDS = ("cn_name", "affiliation", "affiliation_source", "status", "user_id", "note")
STATUSES = ("pending", "found", "added", "not_found", "skipped")


def normalize_author(name: str) -> str:
    name = re.sub(r"\s+", " ", name).strip().strip(",;")
    return re.sub(r"[\d*†‡]+$", "", name).strip()


def count_authors() -> dict[str, dict]:
    papers = load_json(PAPERS_PATH, [])
    stats: dict[str, dict] = defaultdict(lambda: {"papers": 0, "titles": [], "paper_ids": []})
    for paper in papers:
        seen = set()
        for author in paper.get("authors") or []:
            name = normalize_author(author)
            if len(name) < 3 or name in seen:
                continue
            seen.add(name)
            entry = stats[name]
            entry["papers"] += 1
            entry["paper_ids"].append(paper["id"])
            if len(entry["titles"]) < 4:
                entry["titles"].append(paper["title"])
    return stats


def load_candidates() -> dict:
    return load_json(CANDIDATES_PATH, {"version": 1, "min_papers": 3, "updated_at": None, "candidates": []})


def cmd_refresh(args: argparse.Namespace) -> None:
    data = load_candidates()
    existing = {item["author"]: item for item in data["candidates"]}
    stats = count_authors()
    watchlist_ids = {c["user_id"] for c in load_watchlist().get("creators", [])}
    merged = []
    for author, stat in stats.items():
        old = existing.get(author)
        has_manual = bool(old and any(old.get(field) for field in ("cn_name", "affiliation", "user_id")))
        if stat["papers"] < args.min_papers and not has_manual:
            continue
        item = {
            "author": author,
            "papers": stat["papers"],
            "titles": stat["titles"],
            "paper_ids": stat["paper_ids"],
            "cn_name": "",
            "affiliation": "",
            "affiliation_source": "",
            "status": "pending",
            "user_id": "",
            "note": "",
        }
        if old:
            for field in MANUAL_FIELDS:
                if old.get(field):
                    item[field] = old[field]
        if item["user_id"] and item["user_id"] in watchlist_ids:
            item["status"] = "added"
        merged.append(item)
    merged.sort(key=lambda item: (-item["papers"], item["author"]))
    data.update({"min_papers": args.min_papers, "candidates": merged})
    from scripts.xhs.common import now_iso

    data["updated_at"] = now_iso()
    dump_json(CANDIDATES_PATH, data)
    print(f"{len(merged)} candidates (>= {args.min_papers} papers) written to {CANDIDATES_PATH.relative_to(ROOT)}")


def cmd_list(args: argparse.Namespace) -> None:
    data = load_candidates()
    rows = [c for c in data["candidates"] if not args.status or c["status"] == args.status]
    print(f"{'篇':>2}  {'作者':<22} {'中文名':<8} {'状态':<10} 单位")
    for item in rows:
        print(f"{item['papers']:>2}  {item['author']:<22} {item.get('cn_name') or '':<8} {item['status']:<10} {item.get('affiliation') or ''}")


def cmd_set(args: argparse.Namespace) -> None:
    data = load_candidates()
    for item in data["candidates"]:
        if item["author"] == args.author:
            if args.status:
                if args.status not in STATUSES:
                    raise SystemExit(f"status must be one of {STATUSES}")
                item["status"] = args.status
            if args.user_id:
                item["user_id"] = args.user_id
            if args.cn_name:
                item["cn_name"] = args.cn_name
            if args.affiliation:
                item["affiliation"] = args.affiliation
                item["affiliation_source"] = args.affiliation_source or "manual"
            if args.note:
                item["note"] = args.note
            dump_json(CANDIDATES_PATH, data)
            print(f"updated {args.author}")
            return
    raise SystemExit(f"no candidate named {args.author!r}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    refresh = sub.add_parser("refresh")
    refresh.add_argument("--min-papers", type=int, default=3)
    lst = sub.add_parser("list")
    lst.add_argument("--status", default="")
    setter = sub.add_parser("set")
    setter.add_argument("author")
    setter.add_argument("--status", default="")
    setter.add_argument("--user-id", default="")
    setter.add_argument("--cn-name", default="")
    setter.add_argument("--affiliation", default="")
    setter.add_argument("--affiliation-source", default="")
    setter.add_argument("--note", default="")
    args = parser.parse_args()
    {"refresh": cmd_refresh, "list": cmd_list, "set": cmd_set}[args.command](args)


if __name__ == "__main__":
    main()

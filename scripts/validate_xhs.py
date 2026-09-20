#!/usr/bin/env python3
"""Validate the Xiaohongshu watchlist and captured note feed."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.xhs.common import (  # noqa: E402
    FEED_DIR,
    INDEX_PATH,
    NOTE_FIELDS,
    NOTE_ID_RE,
    USER_ID_RE,
    WATCHLIST_PATH,
    load_json,
    month_of,
)

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:[+-]\d{2}:\d{2}|Z)$")


def validate_watchlist(errors: list[str]) -> dict:
    watchlist = load_json(WATCHLIST_PATH, None)
    if watchlist is None:
        errors.append(f"missing {WATCHLIST_PATH.relative_to(ROOT)}")
        return {"topics": [], "creators": []}
    topics = watchlist.get("topics", [])
    creators = watchlist.get("creators", [])
    topic_ids = [topic.get("id") for topic in topics]
    for index, topic in enumerate(topics):
        if not topic.get("id") or not SLUG_RE.match(topic["id"]):
            errors.append(f"topic[{index}]: id must be a lowercase slug, got {topic.get('id')!r}")
        if not topic.get("name"):
            errors.append(f"topic[{index}] ({topic.get('id')}): missing name")
        if not isinstance(topic.get("keywords", []), list):
            errors.append(f"topic {topic.get('id')}: keywords must be a list")
    for dup, count in Counter(topic_ids).items():
        if count > 1:
            errors.append(f"duplicate topic id: {dup}")
    known_topics = set(topic_ids)
    user_ids = []
    for index, creator in enumerate(creators):
        user_id = creator.get("user_id", "")
        if not USER_ID_RE.match(str(user_id)):
            errors.append(f"creator[{index}]: user_id must be 24 hex chars, got {user_id!r}")
        user_ids.append(user_id)
        for topic in creator.get("topics", []):
            if topic not in known_topics:
                errors.append(f"creator {user_id}: unknown topic {topic!r}")
        if "enabled" in creator and not isinstance(creator["enabled"], bool):
            errors.append(f"creator {user_id}: enabled must be boolean")
    for dup, count in Counter(user_ids).items():
        if count > 1:
            errors.append(f"duplicate creator user_id: {dup}")
    return watchlist


def validate_feed(errors: list[str]) -> tuple[int, int]:
    if not INDEX_PATH.exists():
        return 0, 0
    index = load_json(INDEX_PATH, {})
    months = index.get("months", [])
    seen_ids: Counter[str] = Counter()
    total = 0
    listed_paths = set()
    for entry in months:
        path = ROOT / entry.get("path", "")
        listed_paths.add(path.name)
        if not path.exists():
            errors.append(f"index lists missing file {entry.get('path')}")
            continue
        notes = load_json(path, [])
        if len(notes) != entry.get("count"):
            errors.append(f"{path.name}: index count {entry.get('count')} != actual {len(notes)}")
        previous_key = None
        for note in notes:
            total += 1
            note_id = note.get("note_id", "")
            seen_ids[note_id] += 1
            missing = sorted(set(NOTE_FIELDS) - note.keys())
            if missing:
                errors.append(f"{path.name} {note_id}: missing fields {missing}")
                continue
            if not NOTE_ID_RE.match(note_id):
                errors.append(f"{path.name}: invalid note_id {note_id!r}")
            if not note["url"].startswith("https://www.xiaohongshu.com/explore/"):
                errors.append(f"{note_id}: unexpected url {note['url']}")
            if note.get("xsec_token") and "xsec_token=" not in note["url"]:
                errors.append(f"{note_id}: url is missing xsec_token query")
            for field in ("captured_at", "published_at", "updated_at"):
                value = note.get(field)
                if value and not ISO_RE.match(value):
                    errors.append(f"{note_id}: {field} is not ISO-8601: {value}")
            if not note.get("captured_at"):
                errors.append(f"{note_id}: captured_at is required")
            if note.get("creator_id") and not USER_ID_RE.match(note["creator_id"]):
                errors.append(f"{note_id}: invalid creator_id {note['creator_id']}")
            bucket = month_of(note.get("published_at"), note.get("captured_at", ""))
            if bucket != entry.get("month"):
                errors.append(f"{note_id}: belongs to {bucket} but stored in {entry.get('month')}")
            if not isinstance(note.get("stats"), dict):
                errors.append(f"{note_id}: stats must be an object")
            key = (note.get("published_at") or note.get("captured_at"), note_id)
            if previous_key is not None and key > previous_key:
                errors.append(f"{path.name}: notes are not sorted newest-first around {note_id}")
            previous_key = key
    for note_id, count in seen_ids.items():
        if count > 1:
            errors.append(f"duplicate note_id across feed files: {note_id}")
    for orphan in FEED_DIR.glob("notes-*.json"):
        if orphan.name not in listed_paths:
            errors.append(f"feed file not listed in index: {orphan.name}")
    if index.get("total") not in (None, total):
        errors.append(f"index total {index.get('total')} != actual {total}")
    digest = index.get("digest")
    if digest is not None:
        validate_digest(digest, set(seen_ids), errors, label="index.digest")
    archive_path = FEED_DIR / "digests.json"
    if archive_path.exists():
        archive = load_json(archive_path, [])
        if not isinstance(archive, list):
            errors.append("digests.json must be a list")
        else:
            dates = [entry.get("date") for entry in archive]
            for dup, count in Counter(dates).items():
                if count > 1:
                    errors.append(f"digests.json has duplicate date {dup}")
            for entry in archive:
                # Archived digests may legitimately point at notes purged later.
                validate_digest(entry, None, errors, label=f"digests.json[{entry.get('date')}]")
    return len(months), total


def validate_digest(digest: dict, note_ids: set[str] | None, errors: list[str], label: str) -> None:
    for field in ("date", "generated_at", "window_hours", "note_count", "backend", "headline", "sections"):
        if field not in digest:
            errors.append(f"{label}: missing {field}")
    if not isinstance(digest.get("sections"), list):
        errors.append(f"{label}: sections must be a list")
        return
    for section in digest["sections"]:
        if not section.get("topic"):
            errors.append(f"{label}: section without topic")
        for item in section.get("highlights", []):
            if note_ids is not None and item.get("note_id") not in note_ids:
                errors.append(f"{label}: highlight references unknown note {item.get('note_id')}")


def main() -> None:
    errors: list[str] = []
    watchlist = validate_watchlist(errors)
    months, notes = validate_feed(errors)
    if errors:
        raise SystemExit("\n".join(errors))
    print(
        f"Validated xhs watchlist ({len(watchlist['topics'])} topics, {len(watchlist['creators'])} creators) "
        f"and feed ({notes} notes in {months} month files)."
    )


if __name__ == "__main__":
    main()

"""Shared data model helpers for the Xiaohongshu (小红书) watch feed.

Everything in this module is pure Python with no browser dependency so it can
be unit-tested and reused by the validator. Storage layout:

    data/xhs_watchlist.json        human-maintained topics + creators
    data/xhs/index.json            manifest: months, discovered creators, last run
    data/xhs/notes-YYYY-MM.json    notes bucketed by publish month (newest first)
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
WATCHLIST_PATH = ROOT / "data" / "xhs_watchlist.json"
FEED_DIR = ROOT / "data" / "xhs"
INDEX_PATH = FEED_DIR / "index.json"

CST = timezone(timedelta(hours=8))
# Only metadata + link are stored; body text is capped so monthly files stay
# small on GitHub Pages. The original note is always one click away.
DESC_MAX_CHARS = 800
USER_ID_RE = re.compile(r"^[0-9a-f]{24}$")
NOTE_ID_RE = re.compile(r"^[0-9a-f]{24}$")
PROFILE_URL_RE = re.compile(r"xiaohongshu\.com/user/profile/([0-9a-f]{24})")
NOTE_URL_RE = re.compile(r"xiaohongshu\.com/(?:explore|discovery/item)/([0-9a-f]{24})")

NOTE_FIELDS = (
    "note_id",
    "xsec_token",
    "url",
    "type",
    "title",
    "desc",
    "creator_id",
    "creator_name",
    "topics",
    "tags",
    "published_at",
    "captured_at",
    "updated_at",
    "stats",
    "cover",
    "image_count",
    "ip_location",
)


# ---------------------------------------------------------------------------
# JSON helpers
# ---------------------------------------------------------------------------


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def now_iso() -> str:
    return datetime.now(CST).replace(microsecond=0).isoformat()


def ms_to_iso(value: Any) -> str | None:
    """Convert a millisecond (or second) epoch to ISO-8601 in UTC+8."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if number <= 0:
        return None
    if number > 1e11:  # milliseconds
        number /= 1000
    return datetime.fromtimestamp(number, CST).replace(microsecond=0).isoformat()


def note_id_time(note_id: str) -> str | None:
    """Xiaohongshu note ids embed the creation time: the first 8 hex chars are
    a unix timestamp in seconds (verified against ``note.time`` from detail
    pages). This gives every list-only note a usable publish time."""
    if not isinstance(note_id, str) or not NOTE_ID_RE.match(note_id):
        return None
    seconds = int(note_id[:8], 16)
    if not 1_262_304_000 <= seconds <= 4_102_444_800:  # 2010 .. 2100 sanity window
        return None
    return datetime.fromtimestamp(seconds, CST).isoformat()


def month_of(iso: str | None, fallback: str) -> str:
    source = iso or fallback
    return source[:7]


# ---------------------------------------------------------------------------
# Watchlist
# ---------------------------------------------------------------------------


def load_watchlist(path: Path = WATCHLIST_PATH) -> dict:
    data = load_json(path, {"version": 1, "topics": [], "creators": []})
    data.setdefault("topics", [])
    data.setdefault("creators", [])
    return data


def save_watchlist(data: dict, path: Path = WATCHLIST_PATH) -> None:
    dump_json(path, data)


def enabled_creators(watchlist: dict) -> list[dict]:
    return [item for item in watchlist.get("creators", []) if item.get("enabled", True)]


def parse_user_id(value: str) -> str | None:
    value = value.strip()
    if USER_ID_RE.match(value):
        return value
    match = PROFILE_URL_RE.search(value)
    return match.group(1) if match else None


def parse_note_id(value: str) -> str | None:
    value = value.strip()
    if NOTE_ID_RE.match(value):
        return value
    match = NOTE_URL_RE.search(value)
    return match.group(1) if match else None


def profile_url(user_id: str) -> str:
    return f"https://www.xiaohongshu.com/user/profile/{user_id}"


def note_url(note_id: str, xsec_token: str | None, source: str = "pc_user") -> str:
    url = f"https://www.xiaohongshu.com/explore/{note_id}"
    if xsec_token:
        url += f"?xsec_token={xsec_token}&xsec_source={source}"
    return url


# ---------------------------------------------------------------------------
# Raw payload normalisation
# ---------------------------------------------------------------------------


def unwrap(value: Any) -> Any:
    """Strip Vue ref wrappers (``{_value, _rawValue}``) that leak into
    ``window.__INITIAL_STATE__``."""
    if isinstance(value, dict):
        for key in ("_rawValue", "_value"):
            if key in value:
                return unwrap(value[key])
    return value


def pick(mapping: Any, *keys: str, default: Any = None) -> Any:
    """Return the first present key, accepting snake_case and camelCase."""
    mapping = unwrap(mapping)
    if not isinstance(mapping, dict):
        return default
    for key in keys:
        if key in mapping and mapping[key] not in (None, ""):
            return unwrap(mapping[key])
        camel = re.sub(r"_([a-z])", lambda m: m.group(1).upper(), key)
        if camel in mapping and mapping[camel] not in (None, ""):
            return unwrap(mapping[camel])
    return default


def to_int(value: Any) -> int:
    """Interaction counts arrive as ``"1.2万"``, ``"1,234"`` or ints."""
    if isinstance(value, (int, float)):
        return int(value)
    if not isinstance(value, str):
        return 0
    text = value.strip().replace(",", "")
    if not text:
        return 0
    multiplier = 1
    if text.endswith("万"):
        multiplier, text = 10_000, text[:-1]
    elif text.endswith("w") or text.endswith("W"):
        multiplier, text = 10_000, text[:-1]
    elif text.endswith("亿"):
        multiplier, text = 100_000_000, text[:-1]
    try:
        return int(float(text) * multiplier)
    except ValueError:
        return 0


SIGNED_IMAGE_RE = re.compile(
    r"^https?://sns-webpic(?:-qc)?\.xhscdn\.com/\d{10,16}/[0-9a-f]{32}/(?P<path>[^!?#]+)(?:![^?#]*)?"
)
IMAGE_TRANSFORM = "imageView2/2/w/480/format/webp"


def durable_image_url(url: str) -> str:
    """Rewrite a time-limited ``sns-webpic`` URL into the stable
    ``sns-img-qc.xhscdn.com/<file>`` form (served as webp, https).

    The signed form embeds a timestamp and expires within hours; the stable
    form only requires the page to send no Referer (handled in the frontend
    with ``referrerpolicy="no-referrer"``).
    """
    if not url:
        return ""
    match = SIGNED_IMAGE_RE.match(url)
    if match:
        return f"https://sns-img-qc.xhscdn.com/{match.group('path')}?{IMAGE_TRANSFORM}"
    if url.startswith("http://"):
        url = "https://" + url[len("http://"):]
    return url


def image_url(image: Any) -> str:
    """Best public URL for a cover/image object; prefers the default scene."""
    image = unwrap(image)
    if not isinstance(image, dict):
        return ""
    direct = pick(image, "url_default", "url_pre", "url", default="")
    if direct:
        return durable_image_url(str(direct))
    infos = pick(image, "info_list", default=[]) or []
    by_scene = {}
    for info in infos:
        scene = pick(info, "image_scene", default="")
        url = pick(info, "url", default="")
        if url:
            by_scene[scene] = url
    for scene in ("WB_DFT", "WB_PRV"):
        if scene in by_scene:
            return durable_image_url(str(by_scene[scene]))
    return durable_image_url(str(next(iter(by_scene.values()), "")))


def clip_text(text: str, limit: int = DESC_MAX_CHARS) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def normalize_list_note(raw: Any) -> dict | None:
    """Normalise one entry from a creator's note list.

    Accepts both the ``user_posted`` API shape (``note_id``, ``display_title``)
    and the ``__INITIAL_STATE__`` shape (``{id, xsecToken, noteCard: {...}}``).
    """
    raw = unwrap(raw)
    if not isinstance(raw, dict):
        return None
    card = pick(raw, "note_card", default=raw)
    note_id = pick(card, "note_id", "id") or pick(raw, "note_id", "id")
    if not isinstance(note_id, str) or not NOTE_ID_RE.match(note_id):
        return None
    xsec_token = pick(card, "xsec_token") or pick(raw, "xsec_token")
    user = pick(card, "user", default={})
    interact = pick(card, "interact_info", default={})
    return {
        "note_id": note_id,
        "xsec_token": xsec_token if isinstance(xsec_token, str) else None,
        "type": pick(card, "type", default="normal"),
        "title": str(pick(card, "display_title", "title", default="")).strip(),
        "creator_id": pick(user, "user_id", "userid"),
        "creator_name": pick(user, "nickname", "nick_name", default=""),
        "cover": image_url(pick(card, "cover", default={})),
        "published_at": note_id_time(note_id),
        "published_source": "note_id",
        "stats": {"liked": to_int(pick(interact, "liked_count", default=0))},
    }


def normalize_detail_note(raw: Any) -> dict | None:
    """Normalise a note detail payload (``noteDetailMap[id].note`` or the
    ``feed`` API ``items[0].note_card``)."""
    raw = unwrap(raw)
    if not isinstance(raw, dict):
        return None
    card = pick(raw, "note_card", "note", default=raw)
    note_id = pick(card, "note_id", "id") or pick(raw, "note_id", "id")
    if not isinstance(note_id, str) or not NOTE_ID_RE.match(note_id):
        return None
    user = pick(card, "user", default={})
    interact = pick(card, "interact_info", default={})
    tags = [pick(tag, "name") for tag in (pick(card, "tag_list", default=[]) or [])]
    images = pick(card, "image_list", default=[]) or []
    cover = image_url(images[0]) if images else ""
    return {
        "note_id": note_id,
        "xsec_token": pick(card, "xsec_token") or pick(raw, "xsec_token"),
        "type": pick(card, "type", default="normal"),
        "title": str(pick(card, "title", "display_title", default="")).strip(),
        "desc": clip_text(str(pick(card, "desc", default="")).strip()),
        "creator_id": pick(user, "user_id", "userid"),
        "creator_name": pick(user, "nickname", "nick_name", default=""),
        "published_at": ms_to_iso(pick(card, "time")) or note_id_time(note_id),
        "published_source": "detail" if pick(card, "time") else "note_id",
        "updated_at": ms_to_iso(pick(card, "last_update_time")),
        "tags": [tag for tag in tags if isinstance(tag, str) and tag],
        "cover": cover,
        "image_count": len(images),
        "ip_location": pick(card, "ip_location", default=""),
        "stats": {
            "liked": to_int(pick(interact, "liked_count", default=0)),
            "collected": to_int(pick(interact, "collected_count", default=0)),
            "comments": to_int(pick(interact, "comment_count", default=0)),
            "shares": to_int(pick(interact, "share_count", default=0)),
        },
    }


def classify_url(url: str) -> str:
    """Classify a landing URL as ``ok``, ``unavailable`` (this note only) or
    ``risk`` (account/session level: stop the run)."""
    if "website-login/error" in url or "/login" in url.split("?")[0]:
        return "risk"
    match = re.search(r"error_code=(\d+)", url)
    if match and match.group(1) in {"300011", "300012", "300013", "300015"}:
        return "risk"
    if "/404" in url or match:
        return "unavailable"
    return "ok"


def is_risk_control_url(url: str) -> bool:
    return classify_url(url) == "risk"


# ---------------------------------------------------------------------------
# Store (index + monthly buckets)
# ---------------------------------------------------------------------------


class NoteStore:
    """In-memory view of ``data/xhs`` with helpers for incremental merge."""

    def __init__(self, feed_dir: Path = FEED_DIR):
        self.feed_dir = feed_dir
        self.index_path = feed_dir / "index.json"
        self.index: dict = load_json(
            self.index_path,
            {"version": 1, "updated_at": None, "months": [], "creators": {}, "last_run": None},
        )
        self.index.setdefault("months", [])
        self.index.setdefault("creators", {})
        self.notes: dict[str, dict] = {}
        self.dirty_months: set[str] = set()
        for entry in self.index["months"]:
            for note in load_json(feed_dir / Path(entry["path"]).name, []):
                self.notes[note["note_id"]] = note

    # -- queries ----------------------------------------------------------

    def has(self, note_id: str) -> bool:
        return note_id in self.notes

    def get(self, note_id: str) -> dict | None:
        return self.notes.get(note_id)

    def creator_notes(self, creator_id: str) -> list[dict]:
        return [note for note in self.notes.values() if note.get("creator_id") == creator_id]

    # -- mutations --------------------------------------------------------

    def upsert(self, incoming: dict, creator: dict | None = None, captured_at: str | None = None) -> str:
        """Merge ``incoming`` (normalised list/detail dict) into the store.

        Returns ``"new"``, ``"updated"`` or ``"unchanged"``.
        """
        captured_at = captured_at or now_iso()
        note_id = incoming["note_id"]
        existing = self.notes.get(note_id)
        record = dict(existing) if existing else {
            "note_id": note_id,
            "xsec_token": None,
            "url": "",
            "type": "normal",
            "title": "",
            "desc": "",
            "creator_id": None,
            "creator_name": "",
            "topics": [],
            "tags": [],
            "published_at": None,
            "published_source": None,
            "captured_at": captured_at,
            "updated_at": None,
            "stats": {},
            "cover": "",
            "image_count": 0,
            "ip_location": "",
        }
        before = json.dumps(record, sort_keys=True, ensure_ascii=False)
        old_month = month_of(record.get("published_at"), record["captured_at"]) if existing else None

        for key in ("xsec_token", "type", "title", "desc", "creator_id", "creator_name",
                    "updated_at", "cover", "ip_location", "detail_failed_at"):
            value = incoming.get(key)
            if value not in (None, ""):
                record[key] = value
        # Publish time: a detail-page timestamp always wins over the note-id estimate.
        incoming_time = incoming.get("published_at")
        incoming_source = incoming.get("published_source") or ("detail" if incoming_time else None)
        if incoming_time and (record.get("published_source") != "detail" or incoming_source == "detail"):
            record["published_at"] = incoming_time
            record["published_source"] = incoming_source
        if incoming.get("tags"):
            record["tags"] = list(dict.fromkeys(incoming["tags"]))
        if incoming.get("image_count"):
            record["image_count"] = incoming["image_count"]
        stats = dict(record.get("stats") or {})
        for key, value in (incoming.get("stats") or {}).items():
            if isinstance(value, int) and (value > 0 or key not in stats):
                stats[key] = value
        record["stats"] = stats
        if creator:
            if not record.get("creator_id"):
                record["creator_id"] = creator.get("user_id")
            if creator.get("name") and not record.get("creator_name"):
                record["creator_name"] = creator["name"]
            record["topics"] = list(dict.fromkeys([*(record.get("topics") or []), *(creator.get("topics") or [])]))
        if record.get("xsec_token"):
            record["url"] = note_url(note_id, record["xsec_token"])
        elif not record.get("url"):
            record["url"] = note_url(note_id, None)

        after = json.dumps(record, sort_keys=True, ensure_ascii=False)
        if existing and before == after:
            return "unchanged"
        record["stats_updated_at"] = captured_at
        self.notes[note_id] = record
        new_month = month_of(record.get("published_at"), record["captured_at"])
        self.dirty_months.add(new_month)
        if old_month and old_month != new_month:
            self.dirty_months.add(old_month)
        return "updated" if existing else "new"

    def remove_creator(self, user_id: str) -> int:
        """Drop every note of ``user_id`` and forget the creator. Returns count."""
        doomed = [note_id for note_id, note in self.notes.items() if note.get("creator_id") == user_id]
        for note_id in doomed:
            note = self.notes.pop(note_id)
            self.dirty_months.add(month_of(note.get("published_at"), note["captured_at"]))
        self.index["creators"].pop(user_id, None)
        gone = set(doomed)
        digest = self.index.get("digest")
        if isinstance(digest, dict):
            for section in digest.get("sections") or []:
                section["highlights"] = [h for h in section.get("highlights") or [] if h.get("note_id") not in gone]
        return len(doomed)

    def remember_creator(self, user_id: str, name: str = "", avatar: str = "") -> None:
        entry = self.index["creators"].setdefault(user_id, {})
        if name:
            entry["name"] = name
        if avatar:
            entry["avatar"] = avatar
        entry["last_seen"] = now_iso()

    # -- persistence ------------------------------------------------------

    def months(self) -> dict[str, list[dict]]:
        buckets: dict[str, list[dict]] = {}
        for note in self.notes.values():
            buckets.setdefault(month_of(note.get("published_at"), note["captured_at"]), []).append(note)
        for bucket in buckets.values():
            bucket.sort(key=lambda n: (n.get("published_at") or n["captured_at"], n["note_id"]), reverse=True)
        return dict(sorted(buckets.items(), reverse=True))

    def save(self, last_run: dict | None = None) -> None:
        buckets = self.months()
        self.feed_dir.mkdir(parents=True, exist_ok=True)
        month_entries = []
        for month, notes in buckets.items():
            path = self.feed_dir / f"notes-{month}.json"
            if month in self.dirty_months or not path.exists():
                dump_json(path, notes)
            try:
                relative = str(path.relative_to(ROOT))
            except ValueError:  # store outside the repo (tests)
                relative = f"data/xhs/{path.name}"
            month_entries.append({"month": month, "path": relative, "count": len(notes)})
        for stale in self.feed_dir.glob("notes-*.json"):
            if stale.stem.removeprefix("notes-") not in buckets:
                stale.unlink()
        counts: dict[str, int] = {}
        for note in self.notes.values():
            if note.get("creator_id"):
                counts[note["creator_id"]] = counts.get(note["creator_id"], 0) + 1
        for user_id, entry in self.index["creators"].items():
            entry["note_count"] = counts.get(user_id, 0)
        self.index["months"] = month_entries
        self.index["total"] = len(self.notes)
        self.index["updated_at"] = now_iso()
        if last_run is not None:
            self.index["last_run"] = last_run
        dump_json(self.index_path, self.index)
        self.dirty_months.clear()


def iter_store_notes(feed_dir: Path = FEED_DIR) -> Iterable[dict]:
    index = load_json(feed_dir / "index.json", {"months": []})
    for entry in index.get("months", []):
        yield from load_json(feed_dir / Path(entry["path"]).name, [])

#!/usr/bin/env python3
"""Generate the "今日摘要" digest for the Xiaohongshu watch feed.

Runs after ``fetch.py``: picks notes published in the last window, groups
them by topic, asks an LLM for a short per-topic synthesis, validates the
answer against the store and writes it to ``data/xhs/index.json["digest"]``
(plus an archive in ``data/xhs/digests.json``). Purely local; no browsing.

Backends (``--backend``):
  auto      openai if XHS_LLM_API_KEY is set, else codex if the CLI exists, else heuristic
  openai    any OpenAI-compatible chat API (XHS_LLM_API_KEY, XHS_LLM_BASE_URL, XHS_LLM_MODEL)
  codex     the local ``codex exec`` CLI (uses its own login; no API key needed)
  heuristic no model: top notes per topic by engagement, no prose

The heuristic result is also the fallback whenever a model call fails, so the
frontend digest block is never empty after a successful fetch.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.xhs.common import (  # noqa: E402
    CST,
    FEED_DIR,
    NoteStore,
    dump_json,
    load_json,
    load_watchlist,
    now_iso,
)

DIGESTS_PATH = FEED_DIR / "digests.json"
MAX_ARCHIVE = 60
DESC_IN_PROMPT = 280
MAX_NOTES_IN_PROMPT = 120

DIGEST_SCHEMA = {
    "type": "object",
    "properties": {
        "headline": {"type": "string", "description": "一句话总览今天的动向（≤60 字）"},
        "sections": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "topic id，必须来自给定列表"},
                    "summary": {"type": "string", "description": "该方向 2–4 句综述，点出趋势和值得跟进的点"},
                    "highlights": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "note_id": {"type": "string"},
                                "why": {"type": "string", "description": "为什么值得看，≤40 字"},
                            },
                            "required": ["note_id", "why"],
                            "additionalProperties": False,
                        },
                    },
                },
                "required": ["topic", "summary", "highlights"],
                "additionalProperties": False,
            },
        },
        "chatter": {
            "type": "string",
            "description": "圈内吐槽、观点争论、招聘/活动等非论文类但有信息量的动态，1–3 句；没有则为空字符串",
        },
    },
    "required": ["headline", "sections", "chatter"],
    "additionalProperties": False,
}


def log(message: str) -> None:
    print(f"[digest] {message}", flush=True)


# ---------------------------------------------------------------------------
# Note selection
# ---------------------------------------------------------------------------


def engagement(note: dict) -> int:
    stats = note.get("stats") or {}
    return (
        int(stats.get("liked") or 0)
        + 2 * int(stats.get("collected") or 0)
        + 3 * int(stats.get("comments") or 0)
        + 2 * int(stats.get("shares") or 0)
    )


def note_time(note: dict) -> str:
    return note.get("published_at") or note.get("captured_at") or ""


def select_window(notes: list[dict], hours: int, now: datetime | None = None, minimum: int = 8) -> tuple[list[dict], int]:
    """Notes published within ``hours``; widen (48h, 72h, 7d) when too few."""
    now = now or datetime.now(CST)
    for window in sorted({hours, 48, 72, 168}):
        if window < hours:
            continue
        cutoff = (now - timedelta(hours=window)).isoformat()
        picked = [note for note in notes if note_time(note) >= cutoff]
        if len(picked) >= minimum or window == 168:
            picked.sort(key=lambda n: (note_time(n), n["note_id"]), reverse=True)
            return picked, window
    return [], hours


def group_by_topic(notes: list[dict], topics: list[dict]) -> dict[str, list[dict]]:
    order = [topic["id"] for topic in topics if topic.get("enabled", True)]
    groups: dict[str, list[dict]] = {topic_id: [] for topic_id in order}
    groups["_other"] = []
    for note in notes:
        assigned = [topic for topic in (note.get("topics") or []) if topic in groups]
        if not assigned:
            groups["_other"].append(note)
        for topic in assigned:
            groups[topic].append(note)
    return {key: value for key, value in groups.items() if value}


# ---------------------------------------------------------------------------
# Heuristic digest (no model)
# ---------------------------------------------------------------------------


def heuristic_digest(notes: list[dict], topics: list[dict], per_topic: int = 3) -> dict:
    names = {topic["id"]: topic["name"] for topic in topics}
    groups = group_by_topic(notes, topics)
    sections = []
    for topic_id, items in groups.items():
        ranked = sorted(items, key=engagement, reverse=True)[:per_topic]
        creators = sorted({item.get("creator_name") or "" for item in items} - {""})
        sections.append({
            "topic": topic_id,
            "summary": f"{names.get(topic_id, '其他')}方向 {len(items)} 条更新，来自 {len(creators)} 位博主"
                       f"（{'、'.join(creators[:4])}{'…' if len(creators) > 4 else ''}）。按互动量列出代表笔记。",
            "highlights": [
                {"note_id": item["note_id"], "why": f"互动 {engagement(item)} · {item.get('creator_name') or ''}"}
                for item in ranked
            ],
        })
    hot = max(notes, key=engagement) if notes else None
    headline = (
        f"{len(notes)} 条新动态，覆盖 {len([s for s in sections if s['topic'] != '_other'])} 个方向"
        + (f"；最热：{hot.get('title') or hot['note_id']}" if hot else "")
    )
    return {"headline": headline, "sections": sections, "chatter": ""}


# ---------------------------------------------------------------------------
# Prompt + model backends
# ---------------------------------------------------------------------------


def build_prompt(notes: list[dict], topics: list[dict], window_hours: int) -> str:
    names = {topic["id"]: topic["name"] for topic in topics}
    groups = group_by_topic(notes[:MAX_NOTES_IN_PROMPT], topics)
    lines = [
        "你是一位跟踪 AI 科研圈动向的研究助理。下面是过去 %d 小时内关注博主在小红书发布的笔记，已按方向分组。" % window_hours,
        "请生成一份中文“今日摘要”，只依据给定内容，不要编造论文名、机构或结论；不确定就不写。",
        "要求：",
        "1. headline：一句话总览（≤60 字），点出今天最重要的 1–2 个信号。",
        "2. sections：每个有内容的方向一段 2–4 句综述，指出趋势、共同主题或值得跟进的工作；highlights 选 2–4 条最值得看的笔记，给出 note_id 和 ≤40 字理由。热度（互动量）是参考，不是唯一标准，学术价值和信息量优先。",
        "3. chatter：圈内吐槽、观点争论、招聘、活动、会议截稿等非论文类但有信息量的内容，1–3 句；没有则为空字符串。",
        "4. topic 字段只能使用给定的 topic id。note_id 必须原样来自下面的列表。",
        "5. 严格按 JSON schema 输出，不要输出 JSON 以外的任何内容，不要调用任何工具。",
        "",
        "topic id 对照：" + "，".join(f"{tid}={name}" for tid, name in names.items()) + "，_other=未分组",
        "",
    ]
    for topic_id, items in groups.items():
        lines.append(f"## {topic_id}（{names.get(topic_id, '未分组')}，{len(items)} 条）")
        for note in items:
            stats = note.get("stats") or {}
            meta = f"赞{stats.get('liked', 0)}"
            if stats.get("collected") is not None:
                meta += f" 藏{stats.get('collected', 0)} 评{stats.get('comments', 0)}"
            desc = (note.get("desc") or "").replace("\n", " ").strip()
            if len(desc) > DESC_IN_PROMPT:
                desc = desc[: DESC_IN_PROMPT - 1] + "…"
            tags = " ".join(f"#{tag}" for tag in (note.get("tags") or [])[:5])
            lines.append(
                f"- note_id={note['note_id']} | {note_time(note)[:16]} | {note.get('creator_name') or ''} | {meta}"
                f"\n  标题：{note.get('title') or '（无标题）'}"
                + (f"\n  正文：{desc}" if desc else "")
                + (f"\n  话题：{tags}" if tags else "")
            )
        lines.append("")
    return "\n".join(lines)


def call_openai(prompt: str, model: str, timeout: int) -> dict:
    api_key = os.environ.get("XHS_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("未设置 XHS_LLM_API_KEY / OPENAI_API_KEY")
    base_url = (os.environ.get("XHS_LLM_BASE_URL") or os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
    body = {
        "model": model,
        "temperature": 0.3,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": "你只输出符合给定 JSON schema 的 JSON 对象。schema：" + json.dumps(DIGEST_SCHEMA, ensure_ascii=False)},
            {"role": "user", "content": prompt},
        ],
    }
    request = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"HTTP {error.code}: {error.read().decode('utf-8', 'replace')[:300]}") from error
    content = payload["choices"][0]["message"]["content"]
    return parse_json_text(content)


def call_codex(prompt: str, model: str | None, timeout: int) -> dict:
    codex = shutil.which("codex")
    if not codex:
        raise RuntimeError("找不到 codex CLI")
    with tempfile.TemporaryDirectory(prefix="zhiyu-digest-") as tmp:
        tmp_path = Path(tmp)
        schema_path = tmp_path / "schema.json"
        output_path = tmp_path / "out.txt"
        schema_path.write_text(json.dumps(DIGEST_SCHEMA, ensure_ascii=False), encoding="utf-8")
        command = [
            codex, "exec", "--ephemeral", "--skip-git-repo-check", "-s", "read-only", "--color", "never",
            "-C", tmp, "--output-schema", str(schema_path), "-o", str(output_path),
        ]
        if model:
            command += ["-m", model]
        command.append("-")
        result = subprocess.run(command, input=prompt, text=True, capture_output=True, timeout=timeout)
        if not output_path.exists():
            tail = (result.stderr or result.stdout or "").strip().splitlines()[-3:]
            raise RuntimeError("codex exec 未产生输出：" + " / ".join(tail))
        return parse_json_text(output_path.read_text(encoding="utf-8"))


def parse_json_text(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text[text.find("{"):]
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < 0:
        raise RuntimeError(f"模型输出不是 JSON：{text[:120]}")
    return json.loads(text[start : end + 1])


# ---------------------------------------------------------------------------
# Validation + persistence
# ---------------------------------------------------------------------------


def sanitize_digest(raw: dict, notes: list[dict], topics: list[dict]) -> dict:
    """Keep only well-formed sections that reference real notes/topics."""
    known_notes = {note["note_id"] for note in notes}
    known_topics = {topic["id"] for topic in topics} | {"_other"}
    sections = []
    for section in raw.get("sections") or []:
        if not isinstance(section, dict) or section.get("topic") not in known_topics:
            continue
        highlights = []
        for item in section.get("highlights") or []:
            if isinstance(item, dict) and item.get("note_id") in known_notes:
                highlights.append({"note_id": item["note_id"], "why": str(item.get("why") or "").strip()[:80]})
        summary = str(section.get("summary") or "").strip()
        if not summary and not highlights:
            continue
        sections.append({"topic": section["topic"], "summary": summary, "highlights": highlights[:6]})
    return {
        "headline": str(raw.get("headline") or "").strip()[:120],
        "sections": sections,
        "chatter": str(raw.get("chatter") or "").strip()[:600],
    }


def write_digest(store: NoteStore, digest: dict) -> None:
    store.index["digest"] = digest
    store.save()
    archive = load_json(DIGESTS_PATH, [])
    archive = [entry for entry in archive if entry.get("date") != digest["date"]]
    archive.insert(0, digest)
    dump_json(DIGESTS_PATH, archive[:MAX_ARCHIVE])


def generate(args: argparse.Namespace) -> dict:
    store = NoteStore()
    watchlist = load_watchlist()
    topics = [topic for topic in watchlist.get("topics", []) if topic.get("enabled", True)]
    notes, window = select_window(list(store.notes.values()), args.hours)
    if not notes:
        log("窗口内没有笔记，跳过摘要")
        return {}
    log(f"窗口 {window} 小时，{len(notes)} 条笔记")

    backend = args.backend
    if backend == "auto":
        if os.environ.get("XHS_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY"):
            backend = "openai"
        elif shutil.which("codex"):
            backend = "codex"
        else:
            backend = "heuristic"
    model = args.model or os.environ.get("XHS_LLM_MODEL") or ("gpt-4o-mini" if backend == "openai" else None)

    content = None
    used = backend
    error = ""
    if backend in ("openai", "codex"):
        prompt = build_prompt(notes, topics, window)
        if args.dump_prompt:
            Path(args.dump_prompt).write_text(prompt, encoding="utf-8")
            log(f"prompt 已写入 {args.dump_prompt}")
        try:
            raw = call_openai(prompt, model, args.timeout) if backend == "openai" else call_codex(prompt, model, args.timeout)
            content = sanitize_digest(raw, notes, topics)
            if not content["sections"] and not content["headline"]:
                raise RuntimeError("模型输出为空或全部被过滤")
        except Exception as exc:  # noqa: BLE001
            error = str(exc)[:300]
            log(f"{backend} 失败，退回启发式摘要：{error}")
            content = None
    if content is None:
        content = heuristic_digest(notes, topics)
        used = "heuristic"

    digest = {
        "date": datetime.now(CST).date().isoformat(),
        "generated_at": now_iso(),
        "window_hours": window,
        "note_count": len(notes),
        "backend": used,
        "model": model if used != "heuristic" else None,
        "error": error or None,
        **content,
    }
    write_digest(store, digest)
    log(f"已写入摘要（{used}）：{digest['headline'][:60]}")
    return digest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--hours", type=int, default=24, help="摘要窗口（小时），笔记太少时自动放宽到 48/72/168")
    parser.add_argument("--backend", choices=("auto", "openai", "codex", "heuristic"), default="auto")
    parser.add_argument("--model", default="", help="模型名；openai 默认 gpt-4o-mini，codex 默认沿用其配置")
    parser.add_argument("--timeout", type=int, default=300, help="模型调用超时（秒）")
    parser.add_argument("--dump-prompt", default="", help="把发送给模型的 prompt 另存到此文件")
    args = parser.parse_args()
    generate(args)


if __name__ == "__main__":
    main()

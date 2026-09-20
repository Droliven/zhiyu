#!/usr/bin/env python3
"""Manage data/xhs_watchlist.json from the command line.

    python3 scripts/xhs/watchlist.py list
    python3 scripts/xhs/watchlist.py add-creator <profile-url-or-user_id> --topics world-model,embodied --name 某某 --note "为什么关注"
    python3 scripts/xhs/watchlist.py disable-creator <user_id>      # 暂停抓取，保留历史
    python3 scripts/xhs/watchlist.py enable-creator <user_id>
    python3 scripts/xhs/watchlist.py remove-creator <user_id>       # 从清单删除（已抓取的笔记保留）
    python3 scripts/xhs/watchlist.py add-topic <id> --name 名称 [--keywords a,b] [--description ...]

Editing the JSON by hand is equally fine; this CLI only guards the format.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.xhs.common import (  # noqa: E402
    NoteStore,
    load_watchlist,
    parse_user_id,
    profile_url,
    save_watchlist,
)


def split_csv(value: str | None) -> list[str]:
    return [item.strip() for item in (value or "").split(",") if item.strip()]


def cmd_list(watchlist: dict, _: argparse.Namespace) -> None:
    print(f"topics ({len(watchlist['topics'])}):")
    for topic in watchlist["topics"]:
        flag = "" if topic.get("enabled", True) else "  [disabled]"
        print(f"  {topic['id']:<16} {topic.get('name', '')}{flag}")
    print(f"creators ({len(watchlist['creators'])}):")
    for creator in watchlist["creators"]:
        flag = "" if creator.get("enabled", True) else "  [disabled]"
        topics = ",".join(creator.get("topics", []))
        print(f"  {creator['user_id']}  {creator.get('name') or '(名称待抓取)':<20} {topics}{flag}")


def cmd_add_creator(watchlist: dict, args: argparse.Namespace) -> None:
    user_id = parse_user_id(args.target)
    if not user_id:
        raise SystemExit(f"无法识别 user_id：{args.target}（需要 24 位十六进制 ID 或主页 URL）")
    known_topics = {topic["id"] for topic in watchlist["topics"]}
    topics = split_csv(args.topics)
    unknown = [topic for topic in topics if topic not in known_topics]
    if unknown:
        raise SystemExit(f"未知 topic：{unknown}。先用 add-topic 添加，或从 {sorted(known_topics)} 中选择。")
    for creator in watchlist["creators"]:
        if creator["user_id"] == user_id:
            creator["topics"] = sorted(set(creator.get("topics", [])) | set(topics))
            if args.name:
                creator["name"] = args.name
            if args.note:
                creator["note"] = args.note
            creator["enabled"] = True
            print(f"已更新 {user_id}")
            return
    watchlist["creators"].append({
        "user_id": user_id,
        "name": args.name or "",
        "profile_url": profile_url(user_id),
        "topics": topics,
        "note": args.note or "",
        "added": date.today().isoformat(),
        "enabled": True,
    })
    print(f"已添加 {user_id}")


def set_creator_enabled(watchlist: dict, user_id: str, enabled: bool) -> None:
    user_id = parse_user_id(user_id) or user_id
    for creator in watchlist["creators"]:
        if creator["user_id"] == user_id:
            creator["enabled"] = enabled
            print(f"{user_id} enabled={enabled}")
            return
    raise SystemExit(f"清单中没有 {user_id}")


def cmd_remove_creator(watchlist: dict, args: argparse.Namespace) -> None:
    user_id = parse_user_id(args.target) or args.target
    before = len(watchlist["creators"])
    watchlist["creators"] = [c for c in watchlist["creators"] if c["user_id"] != user_id]
    if len(watchlist["creators"]) == before and not args.purge_notes:
        raise SystemExit(f"清单中没有 {user_id}")
    if args.purge_notes:
        store = NoteStore()
        removed = store.remove_creator(user_id)
        store.save()
        print(f"已删除 {user_id}，并从 data/xhs 清除 {removed} 条笔记")
    else:
        print(f"已删除 {user_id}（历史笔记保留在 data/xhs 中；加 --purge-notes 可一并清除）")


def cmd_add_topic(watchlist: dict, args: argparse.Namespace) -> None:
    for topic in watchlist["topics"]:
        if topic["id"] == args.topic_id:
            raise SystemExit(f"topic 已存在：{args.topic_id}")
    watchlist["topics"].append({
        "id": args.topic_id,
        "name": args.name,
        "keywords": split_csv(args.keywords),
        "description": args.description or "",
        "enabled": True,
    })
    print(f"已添加 topic {args.topic_id}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    add = sub.add_parser("add-creator")
    add.add_argument("target", help="主页 URL 或 24 位 user_id")
    add.add_argument("--topics", default="")
    add.add_argument("--name", default="")
    add.add_argument("--note", default="")
    for name in ("disable-creator", "enable-creator"):
        sub.add_parser(name).add_argument("target")
    remove = sub.add_parser("remove-creator")
    remove.add_argument("target")
    remove.add_argument("--purge-notes", action="store_true", help="同时从 data/xhs 删除该博主的全部笔记")
    topic = sub.add_parser("add-topic")
    topic.add_argument("topic_id")
    topic.add_argument("--name", required=True)
    topic.add_argument("--keywords", default="")
    topic.add_argument("--description", default="")
    args = parser.parse_args()

    watchlist = load_watchlist()
    if args.command == "list":
        cmd_list(watchlist, args)
        return
    if args.command == "add-creator":
        cmd_add_creator(watchlist, args)
    elif args.command == "disable-creator":
        set_creator_enabled(watchlist, args.target, False)
    elif args.command == "enable-creator":
        set_creator_enabled(watchlist, args.target, True)
    elif args.command == "remove-creator":
        cmd_remove_creator(watchlist, args)
    elif args.command == "add-topic":
        cmd_add_topic(watchlist, args)
    save_watchlist(watchlist)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Incrementally capture new notes from watched Xiaohongshu creators.

Design (see README "小红书动向"):

* A dedicated Chrome profile (``~/.zhiyu/xhs-chrome-profile``) is launched with
  remote debugging enabled, or reused if it is already running. Login state
  lives in that profile, so scanning the QR code is needed only when it expires.
* Playwright attaches over CDP and simply *browses*: creator profile pages and
  note pages are opened like a human would, and data is read from
  ``window.__INITIAL_STATE__`` plus the XHR responses the page itself issued.
  No request signing is re-implemented, so signature changes do not break us.
* New notes are merged into ``data/xhs/notes-YYYY-MM.json``; existing notes
  only get their like counts refreshed from the list page.

Usage:
    python3 scripts/xhs/fetch.py                 # normal incremental run
    python3 scripts/xhs/fetch.py --creators <id>  # limit to some creators
    python3 scripts/xhs/fetch.py --check-login    # only verify login state
    python3 scripts/xhs/fetch.py --dump-state     # save raw page state for debugging
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import random
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.xhs.common import (  # noqa: E402
    NoteStore,
    classify_url,
    enabled_creators,
    load_watchlist,
    normalize_detail_note,
    normalize_list_note,
    note_url,
    now_iso,
    pick,
    profile_url,
    unwrap,
)

STATE_DIR = Path(os.environ.get("XHS_STATE_DIR", Path.home() / ".zhiyu" / "xhs"))
DEFAULT_PROFILE_DIR = Path(os.environ.get("XHS_PROFILE_DIR", Path.home() / ".zhiyu" / "xhs-chrome-profile"))
DEFAULT_PORT = int(os.environ.get("XHS_CDP_PORT", "9222"))
EXPLORE_URL = "https://www.xiaohongshu.com/explore"
RISK_MARKERS = ("安全限制", "Account abnormal", "300011", "300012", "300013", "访问频次异常")
CHROME_CANDIDATES = (
    os.environ.get("XHS_CHROME", ""),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
)


class RunAborted(Exception):
    """Raised when the platform pushes back (risk control) and we must stop."""


def log(message: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def notify(title: str, message: str) -> None:
    if platform.system() != "Darwin":
        return
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script], check=False, capture_output=True)


def human_pause(low: float, high: float) -> None:
    time.sleep(random.uniform(low, high))


# ---------------------------------------------------------------------------
# Browser lifecycle
# ---------------------------------------------------------------------------


def cdp_alive(port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1.5) as response:
            return response.status == 200
    except (urllib.error.URLError, OSError):
        return False


def find_chrome() -> str:
    for candidate in CHROME_CANDIDATES:
        if candidate and Path(candidate).exists():
            return candidate
    raise SystemExit("找不到 Chrome。请安装 Google Chrome，或通过环境变量 XHS_CHROME 指定可执行文件路径。")


def ensure_browser(port: int, profile_dir: Path) -> bool:
    """Return True if we launched Chrome ourselves (and therefore own it)."""
    if cdp_alive(port):
        log(f"复用已在 127.0.0.1:{port} 监听的 Chrome")
        return False
    profile_dir.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    chrome = find_chrome()
    log_file = open(STATE_DIR / "chrome.log", "ab")
    subprocess.Popen(
        [
            chrome,
            f"--remote-debugging-port={port}",
            f"--user-data-dir={profile_dir}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-session-crashed-bubble",
            "--window-size=1280,900",
            "about:blank",
        ],
        stdout=log_file,
        stderr=log_file,
        start_new_session=True,
    )
    log(f"已启动专用 Chrome（profile: {profile_dir}）")
    for _ in range(60):
        if cdp_alive(port):
            return True
        time.sleep(0.5)
    raise SystemExit("Chrome 启动后 30 秒内没有开放调试端口，请查看 ~/.zhiyu/xhs/chrome.log")


def close_browser(context, page) -> None:
    """Quit Chrome gracefully so cookies are flushed to the profile."""
    try:
        session = context.new_cdp_session(page)
        session.send("Browser.close")
    except Exception as error:  # noqa: BLE001 - best effort
        log(f"关闭浏览器失败（可手动关闭）：{error}")


# ---------------------------------------------------------------------------
# Page helpers
# ---------------------------------------------------------------------------


class Capture:
    """Collects XHR responses issued by the page during one navigation."""

    WATCHED = ("/api/sns/web/v1/user_posted", "/api/sns/web/v1/feed", "/api/sns/web/v2/user/otherinfo")

    def __init__(self, page):
        self.responses = []
        page.on("response", self._on_response)

    def _on_response(self, response) -> None:
        if any(marker in response.url for marker in self.WATCHED):
            self.responses.append(response)

    def drain(self) -> list[dict]:
        payloads = []
        for response in self.responses:
            try:
                body = response.json()
            except Exception:  # noqa: BLE001
                continue
            payloads.append({"url": response.url, "body": body})
        self.responses = []
        return payloads


# After hydration ``window.__INITIAL_STATE__`` holds live Vue refs/reactive
# proxies with circular internals, so a naive JSON.stringify throws. This
# serializer unwraps refs (``.value``) and skips reactivity bookkeeping keys.
PLAIN_STATE_JS = """
(keys) => {
  const SKIP = new Set(['dep', 'deps', 'sub', 'subs', 'effect', 'computed', 'scheduler',
    '__v_skip', '__v_isRef', '__v_isShallow', '__v_raw', '__v_isReactive', '__v_isReadonly']);
  const seen = new WeakSet();
  const plain = (value, depth) => {
    if (value === null || value === undefined) return null;
    if (typeof value !== 'object') return typeof value === 'function' ? undefined : value;
    if (depth > 14) return undefined;
    if (value.__v_isRef) return plain(value.value, depth + 1);
    if (seen.has(value)) return undefined;
    seen.add(value);
    if (Array.isArray(value)) return value.map((item) => plain(item, depth + 1));
    if (value instanceof Map) { const out = {}; for (const [k, v] of value) out[k] = plain(v, depth + 1); return out; }
    if (value instanceof Set) return [...value].map((item) => plain(item, depth + 1));
    const out = {};
    for (const key of Object.keys(value)) {
      if (SKIP.has(key)) continue;
      const result = plain(value[key], depth + 1);
      if (result !== undefined) out[key] = result;
    }
    return out;
  };
  const state = window.__INITIAL_STATE__;
  if (!state) return JSON.stringify({ missing: true });
  const picked = {};
  for (const key of keys) picked[key] = plain(state[key], 0);
  return JSON.stringify(picked);
}
"""


def page_state(page, keys: tuple[str, ...]) -> dict:
    try:
        return json.loads(page.evaluate(PLAIN_STATE_JS, list(keys)) or "{}")
    except Exception as error:  # noqa: BLE001
        return {"error": str(error)}


class NoteUnavailable(Exception):
    """The note itself cannot be viewed (deleted, private, missing token)."""


def check_page(page) -> None:
    """Raise ``RunAborted`` on account-level pushback, ``NoteUnavailable`` when
    only this page is blocked, otherwise return."""
    url = page.url
    verdict = classify_url(url)
    if verdict == "risk":
        raise RunAborted(f"页面被重定向到 {url}，疑似触发风控或需要重新登录")
    try:
        text = page.evaluate("() => document.body ? document.body.innerText.slice(0, 4000) : ''")
    except Exception:  # noqa: BLE001
        text = ""
    if any(marker in text for marker in RISK_MARKERS):
        raise RunAborted("页面出现『安全限制/访问频次异常』提示，已停止本次抓取。请等待数小时再试，并降低频率。")
    if verdict == "unavailable":
        raise NoteUnavailable(f"页面不可访问：{url}")
    # A silently revoked session keeps rendering pages as a tourist; stop
    # instead of capturing partial data and prompting even more pushback.
    if login_state(page).get("logged_in") is False:
        raise RunAborted("登录态在抓取过程中失效（被登出），已停止。重新运行并扫码即可继续。")


def dump_debug(name: str, payload: object) -> None:
    debug_dir = STATE_DIR / "debug"
    debug_dir.mkdir(parents=True, exist_ok=True)
    path = debug_dir / f"{time.strftime('%Y%m%d-%H%M%S')}-{name}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    log(f"已保存调试信息 {path}")


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------


def login_state(page) -> dict:
    """Return ``{"logged_in": bool | None, "nickname": str, "signal": str}``."""
    # ``user.loggedIn`` is a Vue ref after hydration (read ``.value``); before
    # hydration it is a plain boolean. DOM checks are the fallback.
    script = """
    () => {
      const out = { logged_in: null, nickname: "", signal: "" };
      const unref = (v) => (v && typeof v === 'object' && '__v_isRef' in v) ? v.value : v;
      const state = window.__INITIAL_STATE__;
      const user = state && state.user;
      const flag = user ? unref(user.loggedIn) : undefined;
      if (typeof flag === 'boolean') {
        out.logged_in = flag;
        out.signal = "initialState";
        try { out.nickname = (unref(user.userInfo) || {}).nickname || ""; } catch (error) {}
        return out;
      }
      if (document.querySelector('.login-container, .login-modal, .reds-login')) {
        out.logged_in = false; out.signal = "loginModal"; return out;
      }
      if (document.querySelector('.side-bar .user, a[href^="/user/profile/"] img')) {
        out.logged_in = true; out.signal = "sidebarUser"; return out;
      }
      return out;
    }
    """
    try:
        return page.evaluate(script) or {"logged_in": None, "nickname": "", "signal": "evaluate-failed"}
    except Exception as error:  # noqa: BLE001
        return {"logged_in": None, "nickname": "", "signal": f"error:{error}"}


def ensure_login(page, timeout: int) -> dict:
    page.goto(EXPLORE_URL, wait_until="domcontentloaded", timeout=45_000)
    human_pause(1.5, 3)
    state = login_state(page)
    if state["logged_in"]:
        log(f"登录态有效（{state['nickname'] or '已登录'}，信号 {state['signal']}）")
        return state
    log(f"未检测到登录态（信号 {state['signal']}），请在弹出的 Chrome 窗口中扫码登录…")
    notify("知域 · 小红书动向", "需要扫码登录小红书，请切换到 Chrome 窗口")
    page.bring_to_front()
    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(3)
        state = login_state(page)
        if state["logged_in"]:
            log(f"登录成功（{state['nickname'] or '已登录'}）")
            human_pause(2, 4)
            return state
    raise SystemExit(f"等待扫码超过 {timeout} 秒，已退出。重新运行即可继续。")


# ---------------------------------------------------------------------------
# Crawling
# ---------------------------------------------------------------------------


def flatten_notes(value) -> list:
    value = unwrap(value)
    if isinstance(value, dict):
        value = list(value.values())
    if not isinstance(value, list):
        return []
    flat: list = []
    for item in value:
        item = unwrap(item)
        if isinstance(item, list):
            flat.extend(unwrap(sub) for sub in item)
        else:
            flat.append(item)
    return flat


def fetch_creator_list(page, capture: Capture, creator: dict, dump: bool) -> tuple[list[dict], dict]:
    """Open a creator profile and return (normalised list notes, creator info)."""
    user_id = creator["user_id"]
    page.goto(profile_url(user_id), wait_until="domcontentloaded", timeout=45_000)
    human_pause(2.5, 4.5)
    check_page(page)
    state = page_state(page, ("user",))
    payloads = capture.drain()
    if dump:
        dump_debug(f"profile-{user_id}", {"state": state, "responses": payloads})

    raw_notes: list = []
    user_state = state.get("user") if isinstance(state, dict) else None
    if isinstance(user_state, dict):
        raw_notes.extend(flatten_notes(user_state.get("notes")))
    info: dict = {}
    page_data = unwrap(pick(user_state, "user_page_data", default={})) if isinstance(user_state, dict) else {}
    basic = pick(page_data, "basic_info", default={}) or {}
    if basic:
        info = {
            "name": pick(basic, "nickname", "nick_name", default="") or "",
            "avatar": pick(basic, "imageb", "images", "image", default="") or "",
        }
    for payload in payloads:
        body = payload["body"]
        data = body.get("data") if isinstance(body, dict) else None
        if "user_posted" in payload["url"] and isinstance(data, dict):
            raw_notes.extend(data.get("notes") or [])
        if "otherinfo" in payload["url"] and isinstance(data, dict):
            basic = data.get("basic_info") or {}
            info.setdefault("name", basic.get("nickname", ""))
            info.setdefault("avatar", basic.get("imageb") or basic.get("images", ""))

    notes: dict[str, dict] = {}
    for raw in raw_notes:
        normalized = normalize_list_note(raw)
        if normalized and (normalized.get("creator_id") in (None, "", user_id)):
            normalized["creator_id"] = user_id
            notes.setdefault(normalized["note_id"], normalized)
    if not notes and not raw_notes:
        # Nothing parsed: keep evidence so the selectors can be fixed quickly.
        dump_debug(f"profile-empty-{user_id}", {"url": page.url, "state": state, "responses": payloads})
    return list(notes.values()), info


def fetch_note_detail(page, capture: Capture, note: dict, dump: bool) -> dict | None:
    url = note_url(note["note_id"], note.get("xsec_token"))
    page.goto(url, wait_until="domcontentloaded", timeout=45_000)
    human_pause(2.5, 5)
    check_page(page)
    state = page_state(page, ("note",))
    payloads = capture.drain()
    if dump:
        dump_debug(f"note-{note['note_id']}", {"state": state, "responses": payloads})

    candidates: list = []
    note_state = state.get("note") if isinstance(state, dict) else None
    if isinstance(note_state, dict):
        detail_map = unwrap(pick(note_state, "note_detail_map", default={})) or {}
        entry = unwrap(detail_map.get(note["note_id"])) if isinstance(detail_map, dict) else None
        if isinstance(entry, dict):
            candidates.append(pick(entry, "note", default=entry))
    for payload in payloads:
        if "/feed" not in payload["url"]:
            continue
        data = payload["body"].get("data") if isinstance(payload["body"], dict) else None
        for item in (data or {}).get("items", []) if isinstance(data, dict) else []:
            if not isinstance(item, dict):
                continue
            card = pick(item, "note_card", default={})
            card_id = card.get("note_id") if isinstance(card, dict) else None
            if item.get("id") == note["note_id"] or card_id == note["note_id"]:
                candidates.append(item)
    for candidate in candidates:
        normalized = normalize_detail_note(candidate)
        if normalized and normalized["note_id"] == note["note_id"]:
            if not normalized.get("xsec_token"):
                normalized["xsec_token"] = note.get("xsec_token")
            return normalized
    dump_debug(f"note-empty-{note['note_id']}", {"url": page.url, "state": state, "responses": payloads})
    return None


def run(args: argparse.Namespace) -> int:
    from playwright.sync_api import sync_playwright

    watchlist = load_watchlist()
    creators = enabled_creators(watchlist)
    if args.creators:
        wanted = set(args.creators.split(","))
        creators = [c for c in creators if c["user_id"] in wanted]
    if not creators and not args.check_login:
        log("watchlist 中没有启用的博主。用 scripts/xhs/watchlist.py add-creator 添加后再运行。")
        return 0

    store = NoteStore()
    started = now_iso()
    summary = {
        "started_at": started,
        "finished_at": None,
        "status": "ok",
        "message": "",
        "creators_total": len(creators),
        "creators_ok": 0,
        "creators_failed": [],
        "new_notes": 0,
        "updated_notes": 0,
        "detail_fetched": 0,
        "detail_failed": 0,
        "new_note_ids": [],
    }

    launched = ensure_browser(args.port, args.profile_dir)
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(f"http://127.0.0.1:{args.port}")
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.new_page()
        capture = Capture(page)
        try:
            ensure_login(page, args.login_timeout)
            if args.check_login:
                return 0

            pending_details: list[tuple[dict, dict]] = []
            consecutive_failures = 0
            for position, creator in enumerate(creators, start=1):
                label = creator.get("name") or creator["user_id"]
                log(f"[{position}/{len(creators)}] 博主 {label}")
                try:
                    notes, info = fetch_creator_list(page, capture, creator, args.dump_state)
                    consecutive_failures = 0
                except RunAborted:
                    raise
                except Exception as error:  # noqa: BLE001
                    consecutive_failures += 1
                    summary["creators_failed"].append({"user_id": creator["user_id"], "error": str(error)[:200]})
                    log(f"  失败：{error}")
                    if consecutive_failures >= 3:
                        raise RunAborted("连续 3 个博主页面失败，可能是网络或风控问题，已停止。")
                    human_pause(args.min_delay, args.max_delay)
                    continue
                summary["creators_ok"] += 1
                store.remember_creator(creator["user_id"], info.get("name") or creator.get("name", ""), info.get("avatar", ""))
                first_run = not store.creator_notes(creator["user_id"])
                new_here = 0
                fresh: list[dict] = []
                for note in notes:
                    if not note.get("creator_name") and info.get("name"):
                        note["creator_name"] = info["name"]
                    was_known = store.has(note["note_id"])
                    outcome = store.upsert(note, creator=creator)
                    if not was_known:
                        new_here += 1
                        summary["new_notes"] += 1
                        summary["new_note_ids"].append(note["note_id"])
                        fresh.append(note)
                    elif outcome == "updated":
                        summary["updated_notes"] += 1
                fresh.sort(key=lambda n: n.get("published_at") or "", reverse=True)
                if first_run and len(fresh) > args.first_run_limit:
                    # Backfill: store the whole first page as metadata, but only
                    # open the newest few notes so a new creator does not cost
                    # dozens of page views in one run.
                    fresh = fresh[: args.first_run_limit]
                pending_details.extend((note, creator) for note in fresh)
                log(f"  列表 {len(notes)} 条，新增 {new_here} 条" + ("（首次收录，只取最新几条详情）" if first_run else ""))
                human_pause(args.min_delay, args.max_delay)

            pending_details.sort(key=lambda item: item[0].get("published_at") or "", reverse=True)
            detail_targets = pending_details[: args.max_detail]
            skipped = len(pending_details) - len(detail_targets)
            budget = args.max_detail - len(detail_targets)
            if budget > 0 and args.backfill > 0:
                # Use leftover budget to gradually complete older notes that only
                # have list-level metadata (no body text / exact time yet).
                creators_by_id = {c["user_id"]: c for c in creators}
                pending_ids = {note["note_id"] for note, _ in detail_targets}
                backlog = [
                    note for note in store.notes.values()
                    if note["note_id"] not in pending_ids
                    and note.get("creator_id") in creators_by_id
                    and note.get("published_source") != "detail"
                    and not note.get("detail_failed_at")
                ]
                backlog.sort(key=lambda n: n.get("published_at") or "", reverse=True)
                for note in backlog[: min(budget, args.backfill)]:
                    detail_targets.append((note, creators_by_id[note["creator_id"]]))
                    summary["backfilled"] = summary.get("backfilled", 0) + 1
            if detail_targets:
                log(f"抓取 {len(detail_targets)} 条笔记详情" + (f"（本次跳过 {skipped} 条新笔记，下次继续）" if skipped else ""))
                for position, (note, creator) in enumerate(detail_targets, start=1):
                    log(f"  [{position}/{len(detail_targets)}] {note.get('title') or note['note_id']}")
                    try:
                        detail = fetch_note_detail(page, capture, note, args.dump_state)
                    except RunAborted:
                        raise
                    except NoteUnavailable as error:
                        detail = None
                        log(f"    跳过：{error}")
                    except Exception as error:  # noqa: BLE001
                        detail = None
                        log(f"    失败：{error}")
                    if detail:
                        store.upsert(detail, creator=creator)
                        summary["detail_fetched"] += 1
                    else:
                        summary["detail_failed"] += 1
                        store.upsert({"note_id": note["note_id"], "detail_failed_at": now_iso()}, creator=creator)
                    human_pause(args.min_delay, args.max_delay)
        except RunAborted as error:
            summary["status"] = "aborted"
            summary["message"] = str(error)
            log(f"中止：{error}")
            notify("知域 · 小红书动向", f"抓取中止：{str(error)[:80]}")
        finally:
            summary["finished_at"] = now_iso()
            if not args.check_login:
                store.save(last_run=summary)
                STATE_DIR.mkdir(parents=True, exist_ok=True)
                (STATE_DIR / "last_run.json").write_text(
                    json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
                )
            if launched and not args.keep_browser:
                close_browser(context, page)
            else:
                try:
                    page.close()
                except Exception:  # noqa: BLE001
                    pass

    log(
        f"完成：博主 {summary['creators_ok']}/{summary['creators_total']}，新增 {summary['new_notes']} 条，"
        f"更新 {summary['updated_notes']} 条，详情 {summary['detail_fetched']} 成功 / {summary['detail_failed']} 失败，"
        f"状态 {summary['status']}"
    )
    return 0 if summary["status"] == "ok" else 2


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--profile-dir", type=Path, default=DEFAULT_PROFILE_DIR, help="专用 Chrome profile 目录")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Chrome 远程调试端口")
    parser.add_argument("--creators", default="", help="只抓取这些 user_id（逗号分隔）")
    parser.add_argument("--max-detail", type=int, default=60, help="单次最多抓取多少条新笔记详情")
    parser.add_argument("--first-run-limit", type=int, default=8, help="首次收录的博主，只抓最新多少条详情")
    parser.add_argument("--backfill", type=int, default=20, help="用剩余额度补抓多少条只有列表信息的旧笔记（0 关闭）")
    parser.add_argument("--min-delay", type=float, default=3.0)
    parser.add_argument("--max-delay", type=float, default=8.0)
    parser.add_argument("--login-timeout", type=int, default=300, help="等待扫码的秒数")
    parser.add_argument("--keep-browser", action="store_true", help="结束后不关闭我们启动的 Chrome")
    parser.add_argument("--check-login", action="store_true", help="只检查/完成登录，不抓取")
    parser.add_argument("--dump-state", action="store_true", help="把每页的原始状态保存到 ~/.zhiyu/xhs/debug")
    args = parser.parse_args()
    if args.min_delay > args.max_delay:
        parser.error("--min-delay 不能大于 --max-delay")
    raise SystemExit(run(args))


if __name__ == "__main__":
    main()

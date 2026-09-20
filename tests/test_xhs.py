import json
import tempfile
import unittest
from pathlib import Path

from scripts.xhs.common import (
    NoteStore,
    classify_url,
    clip_text,
    durable_image_url,
    image_url,
    month_of,
    ms_to_iso,
    note_id_time,
    normalize_detail_note,
    normalize_list_note,
    note_url,
    parse_note_id,
    parse_user_id,
    to_int,
    unwrap,
)

USER = "5f1a2b3c4d5e6f7a8b9c0d1e"
NOTE_A = "66a1b2c3d4e5f60718293a4b"
NOTE_B = "66a1b2c3d4e5f60718293a4c"


def initial_state_note(note_id: str, title: str, liked: str = "1.2万") -> dict:
    """Shape observed in window.__INITIAL_STATE__.user.notes (camelCase + refs)."""
    return {
        "id": note_id,
        "xsecToken": "ABC123",
        "noteCard": {
            "type": "normal",
            "displayTitle": title,
            "user": {"userId": USER, "nickName": "研究员小红"},
            "interactInfo": {"liked": False, "likedCount": liked},
            "cover": {"urlDefault": "https://sns-img.example/cover.jpg"},
            "noteId": note_id,
        },
    }


def api_note(note_id: str, title: str) -> dict:
    """Shape returned by /api/sns/web/v1/user_posted (snake_case)."""
    return {
        "note_id": note_id,
        "xsec_token": "API456",
        "type": "video",
        "display_title": title,
        "user": {"user_id": USER, "nickname": "研究员小红"},
        "interact_info": {"liked_count": "321"},
        "cover": {"url_default": "https://sns-img.example/cover2.jpg"},
    }


class HelpersTest(unittest.TestCase):
    def test_unwrap_strips_vue_refs(self) -> None:
        wrapped = {"__v_isRef": True, "_rawValue": [[1, 2]], "_value": [[1, 2]]}
        self.assertEqual(unwrap(wrapped), [[1, 2]])
        self.assertEqual(unwrap({"plain": 1}), {"plain": 1})

    def test_to_int_handles_chinese_units(self) -> None:
        self.assertEqual(to_int("1.2万"), 12000)
        self.assertEqual(to_int("1,234"), 1234)
        self.assertEqual(to_int(42), 42)
        self.assertEqual(to_int(""), 0)
        self.assertEqual(to_int("赞"), 0)

    def test_ms_to_iso_accepts_ms_and_seconds(self) -> None:
        self.assertEqual(ms_to_iso(1_758_300_000_000), "2025-09-20T00:40:00+08:00")
        self.assertEqual(ms_to_iso(1_758_300_000), ms_to_iso(1_758_300_000_000))
        self.assertIsNone(ms_to_iso(None))
        self.assertIsNone(ms_to_iso(0))

    def test_parse_ids_from_urls(self) -> None:
        self.assertEqual(parse_user_id(f"https://www.xiaohongshu.com/user/profile/{USER}?tab=note"), USER)
        self.assertEqual(parse_user_id(USER), USER)
        self.assertIsNone(parse_user_id("https://www.xiaohongshu.com/explore"))
        self.assertEqual(parse_note_id(f"https://www.xiaohongshu.com/explore/{NOTE_A}?xsec_token=x"), NOTE_A)

    def test_note_url_keeps_xsec_token(self) -> None:
        self.assertIn("xsec_token=tok", note_url(NOTE_A, "tok"))
        self.assertEqual(note_url(NOTE_A, None), f"https://www.xiaohongshu.com/explore/{NOTE_A}")

    def test_durable_image_url_rewrites_signed_cdn_links(self) -> None:
        signed = "http://sns-webpic-qc.xhscdn.com/202609201545/0a83bf6ddbc4e47ab68e91f5a342cf66/spectrum/1040g34o3255qs04lk8304abq90eu1tvrk5u07q8!nc_n_webp_mw_1"
        self.assertEqual(
            durable_image_url(signed),
            "https://sns-img-qc.xhscdn.com/spectrum/1040g34o3255qs04lk8304abq90eu1tvrk5u07q8?imageView2/2/w/480/format/webp",
        )
        plain = "http://sns-webpic-qc.xhscdn.com/202609201545/81f2f6d6609f9cd61ab6faa17cb278d6/1040g2sg322lqsd8qg0704abq90eu1tvrlpl1uv8!nc_n_webp_mw_1"
        self.assertTrue(durable_image_url(plain).startswith("https://sns-img-qc.xhscdn.com/1040g2sg322lqsd8qg0704abq90eu1tvrlpl1uv8?"))
        self.assertEqual(durable_image_url("http://sns-avatar-qc.xhscdn.com/avatar/x"), "https://sns-avatar-qc.xhscdn.com/avatar/x")
        self.assertEqual(durable_image_url(""), "")

    def test_image_url_falls_back_to_info_list(self) -> None:
        cover = {"url": "", "infoList": [
            {"imageScene": "WB_PRV", "url": "http://sns-webpic-qc.xhscdn.com/202609201541/5c89576cf47224b6eaccf92b58a1e766/abc!nc_n_webp_prv_1"},
            {"imageScene": "WB_DFT", "url": "http://sns-webpic-qc.xhscdn.com/202609201541/3754aaaaaaaaaaaaaaaaaaaaaaaaaaaa/abc!nc_n_webp_mw_1"},
        ]}
        self.assertEqual(image_url(cover), "https://sns-img-qc.xhscdn.com/abc?imageView2/2/w/480/format/webp")

    def test_classify_url(self) -> None:
        self.assertEqual(classify_url("https://www.xiaohongshu.com/explore/abc?xsec_token=x"), "ok")
        self.assertEqual(classify_url("https://www.xiaohongshu.com/404?source=/404/sec_x&error_code=300031&error_msg=x"), "unavailable")
        self.assertEqual(classify_url("https://www.xiaohongshu.com/404?error_code=300011"), "risk")
        self.assertEqual(classify_url("https://www.xiaohongshu.com/website-login/error?x=1"), "risk")

    def test_note_id_time_matches_detail_timestamp(self) -> None:
        # Verified live: note 6aab956f… was published 2026-09-17T15:23:27+08:00.
        self.assertEqual(note_id_time("6aab956f000000002600b333"), "2026-09-17T15:23:27+08:00")
        self.assertEqual(note_id_time("65f7cbcb000000001203c048"), "2024-03-18T13:06:19+08:00")
        self.assertIsNone(note_id_time("not-a-note-id"))
        self.assertIsNone(note_id_time("00000000000000000000abcd"))

    def test_clip_text_caps_long_bodies(self) -> None:
        self.assertEqual(clip_text("短文"), "短文")
        clipped = clip_text("字" * 2000)
        self.assertEqual(len(clipped), 800)
        self.assertTrue(clipped.endswith("…"))
        self.assertEqual(clip_text("a\n\n\n\n\nb"), "a\n\nb")

    def test_month_of_prefers_published(self) -> None:
        self.assertEqual(month_of("2026-08-31T23:00:00+08:00", "2026-09-01T00:00:00+08:00"), "2026-08")
        self.assertEqual(month_of(None, "2026-09-01T00:00:00+08:00"), "2026-09")


class NormalizeTest(unittest.TestCase):
    def test_list_note_from_initial_state(self) -> None:
        note = normalize_list_note(initial_state_note(NOTE_A, "世界模型新进展"))
        self.assertEqual(note["note_id"], NOTE_A)
        self.assertEqual(note["xsec_token"], "ABC123")
        self.assertEqual(note["title"], "世界模型新进展")
        self.assertEqual(note["creator_id"], USER)
        self.assertEqual(note["creator_name"], "研究员小红")
        self.assertEqual(note["stats"]["liked"], 12000)
        self.assertEqual(note["cover"], "https://sns-img.example/cover.jpg")

    def test_list_note_from_api_payload(self) -> None:
        note = normalize_list_note(api_note(NOTE_B, "VLA 综述"))
        self.assertEqual(note["type"], "video")
        self.assertEqual(note["xsec_token"], "API456")
        self.assertEqual(note["stats"]["liked"], 321)

    def test_list_note_rejects_garbage(self) -> None:
        self.assertIsNone(normalize_list_note({"id": "not-a-note"}))
        self.assertIsNone(normalize_list_note("string"))

    def test_detail_note_from_initial_state(self) -> None:
        raw = {
            "note": {
                "noteId": NOTE_A,
                "type": "normal",
                "title": "标题",
                "desc": "正文 #世界模型[话题]#",
                "time": 1_758_240_000_000,
                "lastUpdateTime": 1_758_250_000_000,
                "ipLocation": "北京",
                "user": {"userId": USER, "nickname": "研究员小红"},
                "interactInfo": {"likedCount": "10", "collectedCount": "5", "commentCount": "2", "shareCount": "1"},
                "tagList": [{"id": "1", "name": "世界模型", "type": "topic"}],
                "imageList": [{"urlDefault": "https://sns-img.example/1.jpg"}, {"urlDefault": "https://sns-img.example/2.jpg"}],
            }
        }
        note = normalize_detail_note(raw)
        self.assertEqual(note["note_id"], NOTE_A)
        self.assertEqual(note["desc"], "正文 #世界模型[话题]#")
        self.assertEqual(note["published_at"], "2025-09-19T08:00:00+08:00")
        self.assertEqual(note["updated_at"], ms_to_iso(1_758_250_000_000))
        self.assertEqual(note["tags"], ["世界模型"])
        self.assertEqual(note["image_count"], 2)
        self.assertEqual(note["stats"], {"liked": 10, "collected": 5, "comments": 2, "shares": 1})
        self.assertEqual(note["ip_location"], "北京")


class NoteStoreTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.feed_dir = Path(self.tmp.name) / "xhs"
        self.creator = {"user_id": USER, "name": "研究员小红", "topics": ["world-model"]}

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_upsert_new_then_detail_moves_month_bucket(self) -> None:
        store = NoteStore(self.feed_dir)
        captured = "2026-09-20T10:00:00+08:00"
        outcome = store.upsert(normalize_list_note(initial_state_note(NOTE_A, "t")), creator=self.creator, captured_at=captured)
        self.assertEqual(outcome, "new")
        self.assertEqual(store.get(NOTE_A)["topics"], ["world-model"])
        self.assertIn("xsec_token=ABC123", store.get(NOTE_A)["url"])
        # List-only notes already get an estimated publish time from the note id.
        self.assertEqual(store.get(NOTE_A)["published_source"], "note_id")
        self.assertEqual(list(store.months()), ["2024-07"])

        detail = normalize_detail_note({"note": {"noteId": NOTE_A, "title": "t", "desc": "d", "time": 1_704_067_200_000,
                                                 "user": {"userId": USER}, "interactInfo": {"likedCount": "3"}}})
        self.assertEqual(store.upsert(detail, creator=self.creator, captured_at=captured), "updated")
        self.assertEqual(store.get(NOTE_A)["published_source"], "detail")
        self.assertEqual(store.get(NOTE_A)["published_at"][:7], "2024-01")
        self.assertEqual(list(store.months()), ["2024-01"])
        self.assertEqual(store.dirty_months, {"2024-07", "2024-01"})

        # A later list refresh (note-id estimate) must not overwrite the exact detail time.
        store.upsert(normalize_list_note(initial_state_note(NOTE_A, "t", liked="99")), creator=self.creator)
        self.assertEqual(store.get(NOTE_A)["published_at"][:7], "2024-01")
        self.assertEqual(store.get(NOTE_A)["stats"]["liked"], 99)

    def test_upsert_unchanged_is_idempotent(self) -> None:
        store = NoteStore(self.feed_dir)
        note = normalize_list_note(api_note(NOTE_B, "x"))
        store.upsert(note, creator=self.creator, captured_at="2026-09-20T10:00:00+08:00")
        self.assertEqual(store.upsert(note, creator=self.creator, captured_at="2026-09-21T10:00:00+08:00"), "unchanged")

    def test_zero_stats_do_not_clobber_known_counts(self) -> None:
        store = NoteStore(self.feed_dir)
        store.upsert(normalize_list_note(api_note(NOTE_B, "x")), creator=self.creator)
        store.upsert({"note_id": NOTE_B, "stats": {"liked": 0}}, creator=self.creator)
        self.assertEqual(store.get(NOTE_B)["stats"]["liked"], 321)

    def test_save_and_reload_roundtrip(self) -> None:
        store = NoteStore(self.feed_dir)
        store.upsert(normalize_list_note(initial_state_note(NOTE_A, "a")), creator=self.creator, captured_at="2026-09-20T10:00:00+08:00")
        store.upsert(normalize_list_note(api_note(NOTE_B, "b")), creator=self.creator, captured_at="2026-08-02T10:00:00+08:00")
        store.remember_creator(USER, "研究员小红")
        store.save(last_run={"status": "ok"})

        index = json.loads((self.feed_dir / "index.json").read_text(encoding="utf-8"))
        self.assertEqual([m["month"] for m in index["months"]], ["2024-07"])
        self.assertEqual(index["total"], 2)
        self.assertEqual(index["creators"][USER]["note_count"], 2)
        self.assertEqual(index["last_run"], {"status": "ok"})
        self.assertTrue((self.feed_dir / "notes-2024-07.json").exists())

        reloaded = NoteStore(self.feed_dir)
        self.assertTrue(reloaded.has(NOTE_A))
        self.assertTrue(reloaded.has(NOTE_B))
        self.assertEqual(reloaded.dirty_months, set())

    def test_remove_creator_purges_notes_and_files(self) -> None:
        store = NoteStore(self.feed_dir)
        other = {"user_id": "5f1a2b3c4d5e6f7a8b9c0d1f", "name": "别人", "topics": []}
        store.upsert(normalize_list_note(initial_state_note(NOTE_A, "a")), creator=self.creator)
        note_b = normalize_list_note(api_note(NOTE_B, "b"))
        note_b["creator_id"] = other["user_id"]
        store.upsert(note_b, creator=other)
        store.remember_creator(USER, "研究员小红")
        store.save()
        self.assertEqual(store.remove_creator(USER), 1)
        store.save()
        reloaded = NoteStore(self.feed_dir)
        self.assertFalse(reloaded.has(NOTE_A))
        self.assertTrue(reloaded.has(NOTE_B))
        self.assertNotIn(USER, reloaded.index["creators"])
        self.assertEqual(reloaded.index["total"], 1)

    def test_save_removes_emptied_month_files(self) -> None:
        store = NoteStore(self.feed_dir)
        store.upsert(normalize_list_note(initial_state_note(NOTE_A, "a")), creator=self.creator, captured_at="2026-09-20T10:00:00+08:00")
        store.save()
        self.assertTrue((self.feed_dir / "notes-2024-07.json").exists())
        store.upsert({"note_id": NOTE_A, "published_at": "2024-01-05T00:00:00+08:00", "published_source": "detail"}, creator=self.creator)
        store.save()
        self.assertFalse((self.feed_dir / "notes-2024-07.json").exists())
        self.assertTrue((self.feed_dir / "notes-2024-01.json").exists())


if __name__ == "__main__":
    unittest.main()

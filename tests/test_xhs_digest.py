import unittest
from datetime import datetime, timedelta

from scripts.xhs.common import CST
from scripts.xhs.digest import (
    build_prompt,
    engagement,
    group_by_topic,
    heuristic_digest,
    parse_json_text,
    sanitize_digest,
    select_window,
)

TOPICS = [
    {"id": "world-model", "name": "世界模型", "enabled": True},
    {"id": "embodied", "name": "具身智能", "enabled": True},
    {"id": "paused", "name": "暂停", "enabled": False},
]
NOW = datetime(2026, 9, 20, 16, 0, tzinfo=CST)


def note(note_id: str, hours_ago: float, topics: list[str], liked: int = 0, comments: int = 0, title: str = "t") -> dict:
    return {
        "note_id": note_id,
        "title": title,
        "desc": "正文 " * 10,
        "creator_name": "博主" + note_id[-1],
        "topics": topics,
        "tags": ["世界模型"],
        "published_at": (NOW - timedelta(hours=hours_ago)).isoformat(),
        "captured_at": NOW.isoformat(),
        "url": f"https://www.xiaohongshu.com/explore/{note_id}?xsec_token=x",
        "stats": {"liked": liked, "comments": comments},
    }


NOTES = [
    note("a" * 24, 2, ["world-model"], liked=10),
    note("b" * 24, 5, ["embodied", "world-model"], liked=1, comments=20, title="hot"),
    note("c" * 24, 30, ["embodied"], liked=50),
    note("d" * 24, 100, [], liked=3),
    note("e" * 24, 400, ["embodied"], liked=999),
]


class SelectionTest(unittest.TestCase):
    def test_engagement_weights(self) -> None:
        self.assertEqual(engagement({"stats": {"liked": 1, "collected": 1, "comments": 1, "shares": 1}}), 8)
        self.assertEqual(engagement({}), 0)

    def test_select_window_widens_when_sparse(self) -> None:
        picked, window = select_window(NOTES, 24, now=NOW, minimum=1)
        self.assertEqual(window, 24)
        self.assertEqual([n["note_id"][0] for n in picked], ["a", "b"])
        picked, window = select_window(NOTES, 24, now=NOW, minimum=3)
        self.assertEqual(window, 48)
        self.assertEqual(len(picked), 3)
        picked, window = select_window(NOTES, 24, now=NOW, minimum=10)
        self.assertEqual(window, 168)
        self.assertEqual(len(picked), 4)  # the 400h-old note stays out

    def test_group_by_topic_respects_enabled_and_other(self) -> None:
        groups = group_by_topic(NOTES, TOPICS)
        self.assertEqual([n["note_id"][0] for n in groups["world-model"]], ["a", "b"])
        self.assertEqual([n["note_id"][0] for n in groups["embodied"]], ["b", "c", "e"])
        self.assertEqual([n["note_id"][0] for n in groups["_other"]], ["d"])
        self.assertNotIn("paused", groups)


class DigestTest(unittest.TestCase):
    def test_heuristic_digest_ranks_by_engagement(self) -> None:
        digest = heuristic_digest(NOTES[:3], TOPICS, per_topic=2)
        embodied = next(s for s in digest["sections"] if s["topic"] == "embodied")
        self.assertEqual([h["note_id"][0] for h in embodied["highlights"]], ["b", "c"])
        self.assertIn("hot", digest["headline"])
        self.assertEqual(digest["chatter"], "")

    def test_build_prompt_lists_every_note_once_per_topic(self) -> None:
        prompt = build_prompt(NOTES[:3], TOPICS, 24)
        self.assertIn("## world-model", prompt)
        self.assertIn("## embodied", prompt)
        self.assertEqual(prompt.count("note_id=" + "b" * 24), 2)
        self.assertIn("过去 24 小时", prompt)

    def test_parse_json_text_tolerates_fences(self) -> None:
        self.assertEqual(parse_json_text('```json\n{"a": 1}\n```'), {"a": 1})
        self.assertEqual(parse_json_text('前言 {"a": [1, 2]} 后记'), {"a": [1, 2]})
        with self.assertRaises(RuntimeError):
            parse_json_text("no json here")

    def test_sanitize_drops_unknown_notes_and_topics(self) -> None:
        raw = {
            "headline": "h",
            "sections": [
                {"topic": "world-model", "summary": "s", "highlights": [
                    {"note_id": "a" * 24, "why": "good"},
                    {"note_id": "z" * 24, "why": "hallucinated"},
                ]},
                {"topic": "made-up", "summary": "x", "highlights": []},
                {"topic": "embodied", "summary": "", "highlights": []},
            ],
            "chatter": None,
        }
        clean = sanitize_digest(raw, NOTES, TOPICS)
        self.assertEqual(len(clean["sections"]), 1)
        self.assertEqual([h["note_id"] for h in clean["sections"][0]["highlights"]], ["a" * 24])
        self.assertEqual(clean["chatter"], "")


if __name__ == "__main__":
    unittest.main()

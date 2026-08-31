import unittest

from scripts.ingest_reports import merge_records, normalize_tag


def record(figure_url: str, links: dict[str, str]) -> dict:
    return {
        "authors": [],
        "links": links,
        "tags": [],
        "figure": {
            "url": figure_url,
            "alt": "figure",
            "label": "figure",
            "source_url": figure_url,
        },
        "pipeline": {key: "" for key in ("input", "process", "output", "details")},
        "source_reports": ["report-test"],
    }


class MergeRecordsTest(unittest.TestCase):
    def test_changed_report_replaces_equal_quality_figure(self) -> None:
        old = record("https://example.com/broken.png", {})
        new = record("https://example.com/replacement.png", {})

        merged = merge_records(old, new, allow_text_replace=True)

        self.assertEqual(merged["figure"]["url"], new["figure"]["url"])

    def test_image_url_is_not_preserved_as_model_link(self) -> None:
        old = record(
            "https://example.com/broken.png",
            {"model": "https://example.com/broken.png"},
        )
        new = record("https://example.com/replacement.png", {})

        merged = merge_records(old, new, allow_text_replace=True)

        self.assertNotIn("model", merged["links"])


class NormalizeTagTest(unittest.TestCase):
    def test_video_generation_uses_existing_library_casing(self) -> None:
        self.assertEqual(normalize_tag("Video Generation"), "video generation")


if __name__ == "__main__":
    unittest.main()

import unittest

from scripts.ingest_reports import merge_records, normalize_tag, parse_paper


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


class ParsePaperTest(unittest.TestCase):
    def test_official_research_article_is_an_ingestable_primary_source(self) -> None:
        section = """
**作者：** Skild AI
**年份与发表：** 2026，官方研究长文；无 arXiv、DOI 或 PDF
**可靠入口：** [官方研究长文](https://skild.ai/blogs/s1)
**类别标签：** Embodied ICL, Robot Manipulation

### 核心内容与 Insight
S1 使用单段视频示范作为提示，在不更新模型参数的情况下执行任务。

### Pipeline
- **输入：** 视频示范和当前机器人观测。
- **过程：** 预训练策略从上下文中推断任务意图。
- **输出：** 机器人动作。

### 实验与证据
官方页面报告内部评测结果，但未公开完整协议。

### 代码与数据
未公开。

### 局限、失败案例与开放问题
来源不是同行评审论文，结果尚无外部复现。
"""

        parsed = parse_paper(
            "Introducing S1: In-Context Learning for Robotics",
            section,
            {"level": 2, "tags": []},
            "report-icl",
        )

        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["links"]["paper"], "https://skild.ai/blogs/s1")
        self.assertEqual(parsed["arxiv_id"], "")
        self.assertEqual(parsed["doi"], "")

    def test_official_web_technical_report_is_a_primary_paper_source(self) -> None:
        section = """
**作者：** Dyna Robotics
**年份与发表：** 2026，官方网页版 technical report；无 arXiv、DOI 或 PDF
**可靠入口：** [官方技术报告](https://www.dyna.co/dyna-2)
**类别标签：** World Action Model, scaling law

### 当前挑战
机器人预训练缺少可扩展的人类操作数据。

### 研究动机
研究人类视频规模能否迁移到机器人预测与控制。

### 技术方案
- **输入：** 第一视角人类视频、动作伪标签和语言指令。
- **过程：** 联合训练未来视频与动作的流匹配模型。
- **输出：** 未来动作块或未来视频。

### 实验结果
在嵌套数据规模上评估离线预测和真机后训练。

### 总结讨论
结果支持所测设置中的数据扩展趋势。

### 代码与数据
未公开。

### 局限、失败案例与开放问题
- 只有机构发布的网页版技术报告，不能解释成 causal、counterfactual、4D 或 geometry 工作。
"""

        parsed = parse_paper(
            "Dyna-2: A 1-Million-Hour Scaling Law for World-Action Models",
            section,
            {"level": 2, "tags": []},
            "report-dyna-2",
        )

        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["links"]["paper"], "https://www.dyna.co/dyna-2")
        self.assertEqual(parsed["arxiv_id"], "")
        self.assertEqual(parsed["doi"], "")
        self.assertEqual(parsed["tags"], ["scaling law", "World Action Model"])


if __name__ == "__main__":
    unittest.main()

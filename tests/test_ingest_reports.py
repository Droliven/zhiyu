import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from scripts import ingest_reports

from scripts.ingest_reports import classify_links, extract_figure, merge_records, normalize_tag, parse_paper


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
    def test_unchanged_report_preserves_reviewed_tags(self) -> None:
        old = record("", {})
        old["tags"] = ["World Action Model"]
        old["evidence_notes"] = ""
        new = record("", {})
        new["tags"] = ["tactile"]
        new["evidence_notes"] = "Old source evidence, not a new audit"
        merged = merge_records(old, new, allow_text_replace=False)
        self.assertEqual(merged["tags"], ["World Action Model"])
        self.assertEqual(merged["evidence_notes"], "")

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
    def test_semantic_aliases_preserve_causal_boundary(self) -> None:
        self.assertEqual(normalize_tag("Agent Memory"), "长时记忆")
        self.assertEqual(normalize_tag("Causal History"), "长时记忆")
        self.assertEqual(normalize_tag("Causal Modeling"), "因果与反事实")
        self.assertEqual(normalize_tag("Counterfactual Reasoning"), "因果与反事实")
        self.assertEqual(normalize_tag("周报"), "")

    def test_video_generation_uses_existing_library_casing(self) -> None:
        self.assertEqual(normalize_tag("Video Generation"), "视频生成")


class ParsePaperTest(unittest.TestCase):
    def test_embedded_figure_keeps_paper_source_link(self) -> None:
        figure = extract_figure(
            "![Figure 1](../images/paper.webp)\n来源：[论文图注](https://arxiv.org/html/2609.11308v1#S1.F1)",
            "2AM", "2609.11308",
        )
        self.assertEqual(figure["url"], "content/images/paper.webp")
        self.assertEqual(figure["source_url"], "https://arxiv.org/html/2609.11308v1#S1.F1")

    def test_arxiv_card_keeps_its_own_tags_and_evidence(self) -> None:
        parsed = parse_paper(
            "Memory Study",
            """- **论文**：[arXiv](https://arxiv.org/abs/2609.11308)
- **类别标签**：Memory, Robot Manipulation
- **证据等级**：正文表 3 已核验
- **首次提交**：2026-09-10T09:35:56Z
- **最近修订**：2026-09-10T09:35:56Z
- **arXiv 主分类**：cs.RO
""",
            {"level": 2, "tags": ["HOI", "tactile"]},
            "report-memory",
        )
        self.assertEqual(parsed["tags"], ["Memory", "机器人学习"])
        self.assertEqual(parsed["evidence_notes"], "正文表 3 已核验")
        self.assertEqual(parsed["arxiv"]["published"], "2026-09-10T09:35:56Z")

    def test_figure_caption_does_not_create_a_model_download(self) -> None:
        links = classify_links(
            """[World Model overview](https://arxiv.org/html/2609.11308#S2.F1)
[Model architecture](https://example.com/model.png)
[模型](https://huggingface.co/example/weights)
""", "2609.11308"
        )
        self.assertEqual(links["model"], "https://huggingface.co/example/weights")

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
        self.assertEqual(parsed["tags"], ["World Action Model", "预训练与扩展律"])




class StandalonePaperTest(unittest.TestCase):
    def test_standalone_source_deduplicates_without_creating_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            reports_dir = root / 'content/reports'
            papers_dir = root / 'content/papers'
            reports_dir.mkdir(parents=True)
            papers_dir.mkdir()
            section = '''- **论文**：[arXiv](https://arxiv.org/abs/2609.24981)
- **类别标签**：3D/4D

## 研究动机
独立的详细论文叙事。

## 技术方案
- **输入**：图像。
- **过程**：几何编码。
- **输出**：状态。

## 实验结果
已核验的实验结果。
'''
            (papers_dir / '2609.24981.md').write_text('# GAE\n\n' + section)
            old = parse_paper('GAE', section, {'tags': []}, 'historic-report')
            old['source_reports'] = []
            old['comments'] = 'reviewed comment'
            old['insight'] = '历史审阅内容。' * 30
            papers_path = root / 'papers.json'
            papers_path.write_text(json.dumps([old]))
            with patch.multiple(ingest_reports, ROOT=root, REPORT_DIR=reports_dir,
                                PAPER_DIR=papers_dir, PAPERS_PATH=papers_path,
                                REPORTS_PATH=root / 'reports.json', DISPLAY_ONLY_REPORTS=[],
                                TOPIC_CATALOG_PATH=root / 'catalog.json'):
                papers, reports = ingest_reports.build()
                self.assertEqual(len(papers), 1)
                self.assertEqual(reports, [])
                self.assertEqual(papers[0]['source_reports'], [])
                self.assertEqual(papers[0]['source_papers'], ['content/papers/2609.24981.md'])
                self.assertEqual(papers[0]['comments'], old['comments'])
                self.assertEqual(papers[0]['insight'], old['insight'])
                papers_path.write_text(json.dumps(papers))
                self.assertEqual(ingest_reports.build(), (papers, reports))
                # The same source also works when rebuilding a new collection.
                papers_path.write_text('[]')
                fresh, reports = ingest_reports.build()
                self.assertEqual(len(fresh), 1)
                self.assertEqual(reports, [])
                self.assertEqual(fresh[0]['pipeline']['input'], '图像。')


if __name__ == "__main__":
    unittest.main()

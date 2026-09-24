"""A report-library reorganization must not rewrite its protected source or papers."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import ingest_reports


class TopicCatalogTest(unittest.TestCase):
    def test_curated_reports_preserve_protected_entry_and_archive_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'topic.md'
            source.write_text('# Synthesis\n[Paper](https://arxiv.org/abs/2609.24981)\n')
            protected = {'id': 'protected', 'title': 'Reviewed title', 'path': 'talk.md',
                         'paper_ids': ['original-association'], 'tags': ['Reviewed tag']}
            legacy = {'id': 'legacy', 'path': 'legacy.md', 'paper_ids': ['p1']}
            previous = [protected, legacy]
            papers = [{'id': 'p1', 'arxiv_id': '2609.24981',
                       'links': {'paper': 'https://arxiv.org/abs/2609.24981'},
                       'source_reports': ['legacy'], 'comments': 'Reviewed comment'}]
            original = copy.deepcopy(papers)
            reports_path = root / 'reports.json'
            reports_path.write_text(json.dumps(previous))
            catalog_path = root / 'catalog.json'
            catalog_path.write_text(json.dumps({
                'protected_report_ids': ['protected'], 'archived_report_ids': ['legacy'],
                'topics': [{'id': 'topic-one', 'title': 'Synthesis', 'path': 'topic.md',
                            'date': '2026-09-24', 'tags': ['3D/4D']}],
            }))
            with patch.multiple(ingest_reports, ROOT=root, REPORTS_PATH=reports_path,
                                TOPIC_CATALOG_PATH=catalog_path):
                # Even a normal importer refresh must preserve the reviewed entry exactly.
                incoming = [{**protected, 'paper_ids': ['new-auto-association']}, legacy]
                result = ingest_reports.curate_report_catalog(incoming, papers)
                self.assertEqual(result[0], protected)
                self.assertEqual(result[1]['paper_ids'], ['p1'])
                self.assertEqual(result[1]['kind'], 'synthesis')
                self.assertTrue(result[2]['archived'])
                self.assertEqual(result[2]['id'], 'legacy')
                self.assertEqual(papers, original)
                reports_path.write_text(json.dumps(result))
                self.assertEqual(ingest_reports.curate_report_catalog(result, papers), result)

    def test_uncatalogued_citation_is_not_silently_imported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'topic.md').write_text('[Missing](https://arxiv.org/abs/2609.99999)')
            (root / 'catalog.json').write_text(json.dumps({
                'topics': [{'id': 'topic', 'path': 'topic.md'}],
            }))
            with patch.multiple(ingest_reports, ROOT=root, REPORTS_PATH=root / 'reports.json',
                                TOPIC_CATALOG_PATH=root / 'catalog.json'):
                with self.assertRaisesRegex(ValueError, 'uncatalogued'):
                    ingest_reports.curate_report_catalog([], [])

    def test_venue_card_with_arxiv_link_is_an_existing_citation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'topic.md').write_text('[OpenHOI](https://arxiv.org/abs/2505.18947)')
            (root / 'catalog.json').write_text(json.dumps({
                'topics': [{'id': 'topic', 'path': 'topic.md'}],
            }))
            papers = [{'id': 'venue-card', 'arxiv_id': None,
                       'links': {'paper': 'https://arxiv.org/abs/2505.18947'}}]
            with patch.multiple(ingest_reports, ROOT=root, REPORTS_PATH=root / 'reports.json',
                                TOPIC_CATALOG_PATH=root / 'catalog.json'):
                result = ingest_reports.curate_report_catalog([], papers)
                self.assertEqual(result[0]['paper_ids'], ['venue-card'])


if __name__ == '__main__':
    unittest.main()

import importlib.util
import io
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "pattern_scan.py"
SPEC = importlib.util.spec_from_file_location("pattern_scan", MODULE_PATH)
pattern_scan = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pattern_scan)


class _FakeStdin:
    def __init__(self, data, encoding=None):
        self.buffer = io.BytesIO(data)
        self.encoding = encoding


class PatternScanTests(unittest.TestCase):
    def test_chinese_high_risk_patterns_are_detected(self):
        text = (
            "基于社会建构主义理论，本文旨在探讨该问题的重要意义。"
            "首先，研究具有理论价值；其次，具有实践价值；最后，具有广阔前景。"
            "上述结果表明该发现具有重要意义。"
        )

        report = pattern_scan.build_report(text)
        labels = {hit["label"] for hit in report["hits"]}

        self.assertEqual(report["language"], "zh")
        self.assertIn("theory-led opening", labels)
        self.assertIn("template goal statement", labels)
        self.assertIn("list symmetry", labels)
        self.assertIn("paragraph-final meta commentary", labels)

    def test_english_high_risk_patterns_are_detected(self):
        text = (
            "This study aims to examine a critical issue, highlighting its broader landscape. "
            "Studies have shown that the method plays a pivotal role in future research."
        )

        report = pattern_scan.build_report(text)
        labels = {hit["label"] for hit in report["hits"]}

        self.assertEqual(report["language"], "en")
        self.assertIn("aim boilerplate", labels)
        self.assertIn("significance inflation", labels)
        self.assertIn("vague attribution", labels)
        self.assertIn("participle padding", labels)

    def test_sentence_split_does_not_split_decimal_points(self):
        text = "第一句话使用英文句号. 第二句话包含 3.14 这个数值. 第三句话使用中文句号。"

        self.assertEqual(
            pattern_scan.split_sentences(text),
            [
                "第一句话使用英文句号",
                "第二句话包含 3.14 这个数值",
                "第三句话使用中文句号",
            ],
        )

    def test_stdin_reader_accepts_utf8_bytes(self):
        original_stdin = sys.stdin
        try:
            text = "基于理论，本文旨在讨论。"
            sys.stdin = _FakeStdin(text.encode("utf-8"), encoding="cp936")

            self.assertEqual(pattern_scan.read_stdin_text(), text)
        finally:
            sys.stdin = original_stdin


if __name__ == "__main__":
    unittest.main()

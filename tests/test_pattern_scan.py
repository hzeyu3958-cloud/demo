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


def _labels(text: str) -> list[str]:
    report = pattern_scan.build_report(text)
    return [hit["label"] for hit in report["hits"]]


# ---------------------------------------------------------------------------
# Per-pattern detection. One test per pattern in ZH_PATTERNS / EN_PATTERNS so
# a regex regression is caught immediately.
# ---------------------------------------------------------------------------


class TestChinesePatterns(unittest.TestCase):
    def test_theory_led_opening(self):
        self.assertIn("theory-led opening", _labels("基于社会建构主义理论，本文探讨该问题。"))

    def test_template_goal_statement(self):
        self.assertIn("template goal statement", _labels("本文旨在探讨该问题。"))

    def test_importance_inflation(self):
        self.assertIn("importance inflation", _labels("这一问题至关重要，不可忽视。"))

    def test_vague_attribution(self):
        self.assertIn("vague attribution", _labels("有研究表明这一现象非常普遍。"))

    def test_list_symmetry(self):
        text = "本文首先介绍背景，其次梳理文献，最后总结方法。"
        self.assertIn("list symmetry", _labels(text))

    def test_data_boilerplate(self):
        self.assertIn("data boilerplate", _labels("从图中可以看出，呈现上升趋势。"))

    def test_empty_ending(self):
        self.assertIn("empty ending", _labels("综上所述，该方法具有重要意义。"))

    def test_connector_overuse(self):
        self.assertIn("connector overuse", _labels("值得注意的是，需要指出的是，趋势明显。"))

    def test_paired_contrast(self):
        self.assertIn("paired contrast", _labels("这不是技术问题，而是制度问题。"))

    def test_abstract_noun_chain(self):
        text = "传导机制的动态监测体系为创新路径提供了支撑框架。"
        self.assertIn("abstract noun chain", _labels(text))

    def test_paragraph_final_meta_commentary(self):
        self.assertIn("paragraph-final meta commentary", _labels("上述结果表明这一结论具有重要意义。"))

    def test_fixed_term_subject(self):
        self.assertIn("fixed term subject", _labels("逆向技术溢出转化为企业创新能力。"))

    def test_parallel_exposition(self):
        text = "从产业基础看，从人力资本看，从投资动机看，结论成立。"
        self.assertIn("parallel exposition", _labels(text))

    def test_casual_drift(self):
        self.assertIn("casual drift", _labels("说白了，这就是个绕不开的坎。"))


class TestEnglishPatterns(unittest.TestCase):
    def test_aim_boilerplate(self):
        self.assertIn("aim boilerplate", _labels("This study aims to examine the data."))

    def test_significance_inflation(self):
        self.assertIn("significance inflation", _labels("This is a critical and pivotal issue."))

    def test_vague_attribution(self):
        self.assertIn("vague attribution", _labels("Studies have shown that this approach works."))

    def test_participle_padding(self):
        text = "The trend is clear, highlighting the underlying mechanism."
        self.assertIn("participle padding", _labels(text))

    def test_rule_of_three(self):
        text = "First we examine the trend; second we test the mechanism; finally we discuss implications."
        self.assertIn("rule of three", _labels(text))

    def test_copula_avoidance(self):
        self.assertIn("copula avoidance", _labels("The framework serves as a guide for the analysis."))

    def test_contrast_theatrics(self):
        self.assertIn("contrast theatrics", _labels("It is not just an issue but a structural problem."))

    def test_generic_conclusion(self):
        self.assertIn("generic conclusion", _labels("Future research should explore this avenue further."))

    def test_scaffolding_phrase(self):
        text = "It is important to note that the data is clear and unambiguous."
        self.assertIn("scaffolding phrase", _labels(text))

    def test_elegant_variation(self):
        text = "The participants completed the survey, and the respondents reported similar views."
        self.assertIn("elegant variation", _labels(text))


# ---------------------------------------------------------------------------
# Negative cases: natural academic prose should not trip most patterns.
# ---------------------------------------------------------------------------


class TestNegativeCases(unittest.TestCase):
    def test_chinese_natural_text_clean(self):
        text = (
            "我们考察了 2018 年至 2022 年间长三角制造业 327 家上市公司的对外直接投资记录。"
            "样本按行业和所有制分组，对投资规模、东道国选择与技术转让路径分别进行了统计。"
            "结果显示，投资规模在 2020 年后明显回落，但专利引用数并未同步下降。"
        )
        labels = set(_labels(text))
        for forbidden in [
            "theory-led opening",
            "template goal statement",
            "importance inflation",
            "list symmetry",
            "data boilerplate",
            "empty ending",
            "paired contrast",
            "casual drift",
        ]:
            self.assertNotIn(forbidden, labels, f"False positive: {forbidden} in {labels}")

    def test_english_natural_text_clean(self):
        text = (
            "We examined FDI records of 327 manufacturing firms in the Yangtze River Delta between 2018 and 2022. "
            "The sample was grouped by industry and ownership. "
            "Investment scale declined after 2020, but patent citations did not move in parallel."
        )
        labels = set(_labels(text))
        for forbidden in [
            "aim boilerplate",
            "significance inflation",
            "participle padding",
            "rule of three",
            "copula avoidance",
            "contrast theatrics",
            "generic conclusion",
            "scaffolding phrase",
            "elegant variation",
        ]:
            self.assertNotIn(forbidden, labels, f"False positive: {forbidden} in {labels}")


# ---------------------------------------------------------------------------
# Sentence splitting must respect common English abbreviations.
# ---------------------------------------------------------------------------


class TestSentenceSplitting(unittest.TestCase):
    def test_decimal_points_preserved(self):
        text = "第一句话使用英文句号. 第二句话包含 3.14 这个数值. 第三句话使用中文句号。"
        self.assertEqual(
            pattern_scan.split_sentences(text),
            [
                "第一句话使用英文句号",
                "第二句话包含 3.14 这个数值",
                "第三句话使用中文句号",
            ],
        )

    def test_et_al_not_split(self):
        text = "Smith et al. (2020) found that growth accelerates."
        self.assertEqual(
            pattern_scan.split_sentences(text),
            ["Smith et al. (2020) found that growth accelerates"],
        )

    def test_ie_eg_not_split(self):
        text = "Use the linear model, i.e. the baseline, or use the alternative, e.g. a neural net."
        sents = pattern_scan.split_sentences(text)
        self.assertEqual(len(sents), 1, f"Expected 1 sentence, got: {sents}")

    def test_fig_not_split(self):
        text = "As shown in Fig. 3, the trend reverses. The data confirms this."
        self.assertEqual(
            pattern_scan.split_sentences(text),
            ["As shown in Fig. 3, the trend reverses", "The data confirms this"],
        )

    def test_multiple_abbreviations_in_one_sentence(self):
        text = "See Smith et al. (2020, Fig. 2) and Jones et al. (2021, Eq. 5) for details."
        sents = pattern_scan.split_sentences(text)
        self.assertEqual(len(sents), 1, f"Expected 1 sentence, got: {sents}")


# ---------------------------------------------------------------------------
# Rhythm detection: CV-based, threshold configurable.
# ---------------------------------------------------------------------------


class TestRhythmDetection(unittest.TestCase):
    def test_uniform_rhythm_detected(self):
        text = "\n\n".join(["The data shows a clear upward trend in this case."] * 6)
        report = pattern_scan.build_report(text)
        self.assertIsNotNone(report["rhythm"])
        self.assertEqual(report["rhythm"]["label"], "uniform sentence rhythm")

    def test_varied_rhythm_not_flagged(self):
        text = "Short. " + " ".join(
            [
                "This is a much longer sentence with many more words than the previous one to vary the cadence.",
            ]
            * 3
        ) + " Done."
        report = pattern_scan.build_report(text)
        self.assertIsNone(report["rhythm"])

    def test_rhythm_threshold_configurable(self):
        # Uniform text trips a strict threshold.
        text = "\n\n".join(["The data shows a clear upward trend in this case."] * 6)
        report_strict = pattern_scan.build_report(text, rhythm_threshold=0.10)
        self.assertIsNotNone(report_strict["rhythm"])
        # Even mildly varied text trips a very loose threshold.
        text_mild = "A. " + " ".join(["Medium length sentence here."] * 5) + " B."
        report_loose = pattern_scan.build_report(text_mild, rhythm_threshold=0.99)
        self.assertIsNotNone(report_loose["rhythm"])
        # Default threshold leaves clearly varied text alone.
        report_default = pattern_scan.build_report(text_mild)
        self.assertIsNone(report_default["rhythm"])


# ---------------------------------------------------------------------------
# Language detection and mixed-language paragraph handling.
# ---------------------------------------------------------------------------


class TestLanguageDetection(unittest.TestCase):
    def test_pure_chinese(self):
        self.assertEqual(pattern_scan.detect_language("基于理论，本文讨论。"), "zh")

    def test_pure_english(self):
        self.assertEqual(pattern_scan.detect_language("This study aims to examine the data."), "en")

    def test_mixed(self):
        text = "基于 theory，本文 aims 探讨 this issue thoroughly."
        self.assertEqual(pattern_scan.detect_language(text), "mixed")

    def test_empty_string_is_english(self):
        self.assertEqual(pattern_scan.detect_language(""), "en")


class TestMixedParagraphHits(unittest.TestCase):
    def test_mixed_paragraph_emits_language_tag(self):
        text = "基于 theory，本文 aims 探讨 this issue thoroughly."
        report = pattern_scan.build_report(text)
        self.assertTrue(all("language" in hit for hit in report["hits"]))


# ---------------------------------------------------------------------------
# Paragraph-level checks: em-dash staging.
# ---------------------------------------------------------------------------


class TestParagraphChecks(unittest.TestCase):
    def test_em_dash_staging_detected(self):
        text = "First claim — supported by A. Second claim — backed by B. Third claim — confirmed by C."
        self.assertIn("em-dash staging", _labels(text))

    def test_em_dash_below_threshold(self):
        text = "Only one em-dash here — nothing else fancy."
        self.assertNotIn("em-dash staging", _labels(text))


# ---------------------------------------------------------------------------
# Citation / numeric diff against an original.
# ---------------------------------------------------------------------------


class TestCitationDiff(unittest.TestCase):
    def test_missing_citation_detected(self):
        original = "Previous work (Smith, 2019) and (Jones, 2020) support this claim."
        rewritten = "Previous work supports this claim."
        report = pattern_scan.build_report(rewritten, original_text=original)
        labels = [hit["label"] for hit in report["hits"]]
        self.assertIn("citation markers lost", labels)

    def test_missing_number_detected(self):
        original = "The rate reached 42.5% in 2020 with p < 0.01."
        rewritten = "The rate increased significantly."
        report = pattern_scan.build_report(rewritten, original_text=original)
        labels = [hit["label"] for hit in report["hits"]]
        self.assertIn("numeric content lost", labels)

    def test_bracket_style_citation_detected(self):
        original = "As shown in earlier work [12, 15] and [3], the effect persists."
        rewritten = "As shown in earlier work, the effect persists."
        report = pattern_scan.build_report(rewritten, original_text=original)
        labels = [hit["label"] for hit in report["hits"]]
        self.assertIn("citation markers lost", labels)

    def test_citations_preserved_no_diff_hit(self):
        original = "As shown in (Smith, 2019) with p < 0.05 and 42.5%."
        rewritten = "As shown in (Smith, 2019) with p < 0.05 and 42.5%."
        report = pattern_scan.build_report(rewritten, original_text=original)
        labels = [hit["label"] for hit in report["hits"]]
        self.assertNotIn("citation markers lost", labels)
        self.assertNotIn("numeric content lost", labels)


# ---------------------------------------------------------------------------
# Suggestions: the JSON path attaches a suggestion for every known label.
# ---------------------------------------------------------------------------


class TestSuggestions(unittest.TestCase):
    def test_suggestion_present_for_known_label(self):
        text = "本文旨在探讨该问题。"
        report = pattern_scan.build_report(text)
        enriched = pattern_scan._attach_suggestions(report)
        target = [h for h in enriched["hits"] if h["label"] == "template goal statement"]
        self.assertEqual(len(target), 1)
        self.assertTrue(target[0]["suggestion"], "Suggestion should be non-empty for known label")
        self.assertIn("考察", target[0]["suggestion"])

    def test_suggestion_empty_for_unknown_label(self):
        report = {
            "language": "en",
            "paragraphs": 1,
            "hits": [
                {"severity": "low", "label": "no-such-label", "match": "x", "language": "en"}
            ],
            "paragraph_reports": [],
            "rhythm": None,
        }
        enriched = pattern_scan._attach_suggestions(report)
        self.assertEqual(enriched["hits"][0]["suggestion"], "")

    def test_rhythm_suggestion_attached(self):
        text = "\n\n".join(["The data shows a clear upward trend in this case."] * 6)
        report = pattern_scan.build_report(text)
        self.assertIsNotNone(report["rhythm"])
        enriched = pattern_scan._attach_suggestions(report)
        self.assertTrue(enriched["rhythm"]["suggestion"])


# ---------------------------------------------------------------------------
# stdin reading across encodings.
# ---------------------------------------------------------------------------


class TestStdinReading(unittest.TestCase):
    def test_utf8_bytes(self):
        original = sys.stdin
        try:
            text = "基于理论，本文旨在讨论。"
            sys.stdin = _FakeStdin(text.encode("utf-8"), encoding="cp936")
            self.assertEqual(pattern_scan.read_stdin_text(), text)
        finally:
            sys.stdin = original

    def test_utf8_bom_bytes(self):
        original = sys.stdin
        try:
            text = "Hello world."
            sys.stdin = _FakeStdin(b"\xef\xbb\xbfHello world.", encoding="cp936")
            self.assertEqual(pattern_scan.read_stdin_text(), text)
        finally:
            sys.stdin = original

    def test_gb18030_bytes(self):
        original = sys.stdin
        try:
            text = "基于理论"
            sys.stdin = _FakeStdin(text.encode("gb18030"), encoding="cp936")
            self.assertEqual(pattern_scan.read_stdin_text(), text)
        finally:
            sys.stdin = original


# ---------------------------------------------------------------------------
# Backwards-compat smoke tests (originally shipped).
# ---------------------------------------------------------------------------


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

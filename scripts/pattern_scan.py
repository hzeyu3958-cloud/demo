#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path


# Each pattern is (severity, label, regex). Severity is "high" or "medium".
# Labels are stable identifiers; suggestions and tests are keyed off them.
ZH_PATTERNS = [
    ("high", "theory-led opening", r"^(基于|依据|根据|在.{0,12}理论框架下|从.{0,12}视角出发)"),
    ("high", "template goal statement", r"(本文|本研究|本论文).{0,10}(旨在|致力于|试图)"),
    ("high", "importance inflation", r"(至关重要|不可忽视|深远影响|广阔前景|重要意义)"),
    ("high", "vague attribution", r"(有研究表明|学界普遍认为|众所周知|相关研究指出)"),
    ("medium", "list symmetry", r"(首先.{0,40}其次.{0,40}(最后|再次))|(理论上.{0,20}实践上.{0,20}方法上)"),
    ("medium", "data boilerplate", r"(从图中可以看出|从表中可以看出|数据显示|分析结果表明|实验结果表明)"),
    ("medium", "empty ending", r"(综上所述|由此可见|有待进一步研究|具有重要意义)"),
    ("medium", "connector overuse", r"(值得注意的是|需要指出的是|与此同时|具体而言|具体来说)"),
    ("medium", "paired contrast", r"(不是.{0,24}而是.{0,24}|即使.{0,24}也.{0,24})"),
    ("medium", "abstract noun chain", r"([\u4e00-\u9fff]{2,}(机制|体系|路径|框架|模式|维度|结构)[的之]?){2,}"),
    ("medium", "paragraph-final meta commentary", r"(上述|这一|该)(结果|结论|发现|分析).{0,16}(表明|说明|揭示|印证|提供)"),
    ("medium", "fixed term subject", r"^(逆向技术溢出|中介效应|固定效应|互补效应|调节效应|稳健性检验).{0,18}(表明|说明|体现|转化|影响)"),
    ("medium", "parallel exposition", r"(从.{1,12}(看|来看).{0,36}){2,}|(一方面.{0,50}另一方面.{0,50}(同时|此外)?)"),
    ("medium", "casual drift", r"(说白了|其实就是|很明显|绕不开的坎|说实话|不得不说是|蛮有意思的)"),
]

EN_PATTERNS = [
    ("high", "aim boilerplate", r"\b(this (study|paper|article) (aims|seeks) to|the purpose of this study is to)\b"),
    ("high", "significance inflation", r"\b(critical|vital|pivotal|profound implications?|broader landscape)\b"),
    ("high", "vague attribution", r"\b(studies have shown|experts believe|it is widely accepted|research indicates)\b"),
    ("medium", "participle padding", r",\s*(highlighting|underscoring|reflecting|contributing to|demonstrating)\b"),
    ("medium", "rule of three", r"\b(first(ly)?).{0,80}\b(second(ly)?).{0,80}\b(third(ly)?|finally)\b"),
    ("medium", "copula avoidance", r"\b(serves as|functions as|acts as|plays a (critical|vital|key|pivotal)?\s*role in)\b"),
    ("medium", "contrast theatrics", r"\b(not only .{0,60} but also|it is not .{0,40} but .{0,40})\b"),
    ("medium", "generic conclusion", r"\b(future research should explore|important implications?|opens new avenues|highlights the importance of)\b"),
    ("medium", "scaffolding phrase", r"\b(it is important to note that|in the context of)\b"),
    ("medium", "elegant variation", r"\b(participants|subjects|respondents|individuals)\b.{0,80}\b(participants|subjects|respondents|individuals)\b"),
]

# Paragraph-level checks. Each entry has a detect(text) -> Optional[dict].
PARAGRAPH_CHECKS = [
    {
        "label": "em-dash staging",
        "severity": "medium",
        "detect": lambda text: (
            {"detail": f"{text.count(chr(0x2014))} em-dashes in one paragraph"}
            if text.count(chr(0x2014)) >= 3
            else None
        ),
    },
    {
        "label": "citation markers lost",
        "severity": "high",
        "detect": lambda text: None,  # populated only when comparing before/after
    },
]

# Repair suggestions keyed by pattern label. Keep concise and actionable.
# Source of truth: references/chinese-academic.md and references/english-academic.md.
SUGGESTIONS: dict[str, str] = {
    # Chinese
    "theory-led opening": "Lead with the phenomenon, dataset, or problem first. Move the theory into the middle of the sentence only if it still matters.",
    "template goal statement": "State the actual task directly. Replace '本文旨在' with '本文考察' or '本研究聚焦于'.",
    "importance inflation": "Replace with concrete scope, mechanism, or observed effect. If the adjective adds nothing, cut it.",
    "vague attribution": "Cite the source if one is already available. Otherwise turn the claim into the paper's own judgment or remove it.",
    "list symmetry": "Break the symmetry. Keep two points if only two matter. Give the strongest point more space.",
    "data boilerplate": "Mention the concrete trend or comparison. Use '图X显示' or '三组数据的差异主要体现在……'.",
    "empty ending": "End with a specific implication, limit, or unresolved point already grounded in the text. Cut '综上所述' / '由此可见'.",
    "connector overuse": "Delete many of them. Let paragraph adjacency or sentence order do the transition work.",
    "paired contrast": "Say the point directly. Reduce '不是...而是...' staging unless the sentence genuinely needs contrast.",
    "abstract noun chain": "Convert stacked nouns to actor-action-object relations. Keep technical terms if they are field terms, but say who does what to whom.",
    "paragraph-final meta commentary": "End with the concrete difference, boundary, or unresolved point supported by the paragraph. Delete final summary sentences that only restate.",
    "fixed term subject": "Move the term into topic, object, or condition position when meaning permits. Keep the term itself stable.",
    "parallel exposition": "Give the strongest point more space. Merge or shorten weaker points. End on a specific analytical observation.",
    "casual drift": "Academic register has slipped into spoken prose. Replace with restrained connectors such as '因此', '鉴于', or '这意味着'.",
    # English
    "aim boilerplate": "State the action directly. Keep one aim statement only if the genre truly needs it; do not repeat it across sections.",
    "significance inflation": "Replace with scope, mechanism, or observed effect. If the adjective adds nothing, cut it.",
    "vague attribution": "Cite specifically if a source is already present. Otherwise own the sentence or remove it.",
    "participle padding": "Split the clause into a real sentence. Keep only the part that adds actual content.",
    "rule of three": "Use two points when two are enough. Give uneven emphasis so the prose does not sound machine-balanced.",
    "copula avoidance": "Use 'is', 'has', or 'does' when that is all the sentence means.",
    "contrast theatrics": "Say the point directly. Reduce 'not only ... but also' or em-dash staging unless contrast is real.",
    "generic conclusion": "Name the actual limit, next test, or practical implication already supported by the text.",
    "scaffolding phrase": "Delete 'It is important to note that'. Drop 'In the context of' unless the context is genuinely needed.",
    "elegant variation": "Keep one stable term when precision matters. Renaming the same concept every paragraph is a detector signal.",
    # Paragraph-level
    "em-dash staging": "Three or more em-dashes in one paragraph reads as staged. Cut some or replace with commas or full stops.",
    "citation markers lost": "A citation marker present in the original text is missing from this paragraph. Restore it.",
    # Rhythm
    "uniform sentence rhythm": "Every sentence is medium length and the paragraph closes with the same kind of summary. Vary cadence; insert one short sentence when it sharpens the point.",
}


# Common English abbreviations that end with a period. Each entry includes
# its trailing period so the protection pass replaces the whole token — body
# AND trailing period — with one sentinel. This keeps abbreviations whose
# bodies themselves contain periods (e.g. ``i.e.``) intact through sentence
# splitting.
ABBREVIATIONS = [
    "et al.", "i.e.", "e.g.", "cf.", "vs.", "viz.",
    "Fig.", "Eq.", "Ref.", "Sec.", "Ch.", "Vol.", "No.", "pp.",
    "Mr.", "Mrs.", "Ms.", "Dr.", "Prof.", "St.",
    "approx.", "etc.", "ca.", "esp.", "incl.", "max.", "min.",
    "Jan.", "Feb.", "Mar.", "Apr.", "Jun.", "Jul.", "Aug.",
    "Sep.", "Oct.", "Nov.", "Dec.",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan academic prose for common Chinese and English AI-writing patterns."
    )
    parser.add_argument("path", nargs="?", help="Path to a UTF-8 text file")
    parser.add_argument("--stdin", action="store_true", help="Read text from standard input")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of plain text")
    parser.add_argument(
        "--suggest",
        action="store_true",
        help="Include a repair suggestion for each hit (also implied by --json).",
    )
    parser.add_argument(
        "--rhythm-threshold",
        type=float,
        default=0.22,
        help="Coefficient of variation below which sentence rhythm is flagged as uniform (default 0.22).",
    )
    parser.add_argument(
        "--compare",
        metavar="ORIGINAL_FILE",
        help="Compare against an original text file. Citation markers and numbers present in the original but missing from the rewritten text are flagged.",
    )
    return parser.parse_args()


def read_text(args: argparse.Namespace) -> str:
    if args.stdin:
        return read_stdin_text()
    if not args.path:
        raise SystemExit("Provide a file path or use --stdin.")
    return Path(args.path).read_text(encoding="utf-8-sig")


def read_stdin_text() -> str:
    if not hasattr(sys.stdin, "buffer"):
        return sys.stdin.read()

    data = sys.stdin.buffer.read()
    if not data:
        return ""

    encodings = ["utf-8-sig", "utf-8"]
    if sys.stdin.encoding:
        encodings.append(sys.stdin.encoding)
    encodings.extend(["gb18030", "utf-16", "utf-16-le"])

    seen = set()
    for encoding in encodings:
        normalized = encoding.lower().replace("_", "-")
        if normalized in seen:
            continue
        seen.add(normalized)
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue

    return data.decode("utf-8", errors="replace")


def detect_language(text: str) -> str:
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    latin_words = len(re.findall(r"[A-Za-z]+", text))
    if cjk and latin_words:
        return "mixed"
    if cjk:
        return "zh"
    return "en"


def split_paragraphs(text: str) -> list[str]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        return []
    return [chunk.strip() for chunk in re.split(r"\n\s*\n+", normalized) if chunk.strip()]


def token_length(sentence: str) -> int:
    tokens = re.findall(r"[A-Za-z0-9_]+|[\u4e00-\u9fff]", sentence)
    return len(tokens)


def _protect_abbreviations(text: str) -> tuple[str, dict[str, str]]:
    """Replace abbreviation tokens with unique sentinels so the split regex won't cut inside them.

    Returns the protected text and a token -> original mapping. Both the internal
    and trailing periods of abbreviations such as ``i.e.`` and ``e.g.`` are
    protected in one pass.
    """
    mapping: dict[str, str] = {}
    out = text
    for i, abbr in enumerate(ABBREVIATIONS):
        token = f"\x01{i:02d}\x01"
        # (?<!\w) and (?!\w) ensure we match the abbreviation as a whole token.
        # This protects abbreviations whose bodies contain periods (e.g. i.e.).
        pattern = re.compile(rf"(?<!\w){re.escape(abbr)}(?!\w)")
        new_out, count = pattern.subn(token, out)
        if count > 0:
            mapping[token] = abbr
            out = new_out
    return out, mapping


def _restore_abbreviations(text: str, mapping: dict[str, str]) -> str:
    out = text
    # Order: longest token first so we never partially restore. With our fixed
    # 4-char token format this is harmless but kept for safety.
    for token in sorted(mapping.keys(), key=len, reverse=True):
        out = out.replace(token, mapping[token])
    return out


def split_sentences(text: str) -> list[str]:
    protected, mapping = _protect_abbreviations(text)
    parts = re.split(r"[。！？!?]+|(?<!\d)\.(?!\d)\s*", protected)
    parts = [_restore_abbreviations(part, mapping).strip() for part in parts]
    return [part for part in parts if token_length(part) > 0]


def sentence_lengths(text: str) -> list[int]:
    return [token_length(part) for part in split_sentences(text)]


def _match_patterns(text: str, patterns: list[tuple[str, str, str]], language: str) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for severity, label, pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if not match:
            continue
        excerpt = match.group(0).strip()
        excerpt = re.sub(r"\s+", " ", excerpt)
        hits.append(
            {
                "severity": severity,
                "label": label,
                "match": excerpt[:80],
                "language": language,
            }
        )
    return hits


def _run_paragraph_checks(text: str) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for check in PARAGRAPH_CHECKS:
        # Skip checks that need external input (e.g. citation diff).
        result = check["detect"](text)
        if not result:
            continue
        hits.append(
            {
                "severity": check["severity"],
                "label": check["label"],
                "match": result.get("detail", ""),
                "language": "",
            }
        )
    return hits


def scan_paragraph(text: str) -> tuple[str, list[dict[str, str]]]:
    language = detect_language(text)
    hits: list[dict[str, str]] = []

    if language in {"zh", "mixed"}:
        hits.extend(_match_patterns(text, ZH_PATTERNS, language="zh"))
    if language in {"en", "mixed"}:
        hits.extend(_match_patterns(text, EN_PATTERNS, language="en"))
    hits.extend(_run_paragraph_checks(text))

    return language, hits


# Patterns that detect "the same idea rewritten many times" — count based, so
# they are easier to evaluate at the report level than per hit.
_CITATION_RE = re.compile(r"\[(?:\d+[\d,\s\-]*)\]|\(\s*[A-Za-z][A-Za-z\s\-]+\s*,?\s*\d{4}\s*\)")
_NUMBER_RE = re.compile(r"p\s*[<>=]\s*0\.\d+|\d+(?:\.\d+)?%|\d{4}|R\s*²\s*=\s*0?\.\d+")


def _diff_citation_markers(original: str, rewritten: str) -> list[dict[str, str]]:
    """Find citation markers and key numbers present in original but missing from rewritten."""
    orig_cites = set(_CITATION_RE.findall(original))
    new_cites = set(_CITATION_RE.findall(rewritten))
    missing_cites = sorted(orig_cites - new_cites)

    orig_numbers = set(_NUMBER_RE.findall(original))
    new_numbers = set(_NUMBER_RE.findall(rewritten))
    missing_numbers = sorted(orig_numbers - new_numbers)

    hits: list[dict[str, str]] = []
    for cite in missing_cites:
        hits.append(
            {
                "severity": "high",
                "label": "citation markers lost",
                "match": cite,
                "language": "",
            }
        )
    for number in missing_numbers:
        hits.append(
            {
                "severity": "high",
                "label": "numeric content lost",
                "match": number,
                "language": "",
            }
        )
    return hits


def build_report(
    text: str,
    rhythm_threshold: float = 0.22,
    original_text: str | None = None,
) -> dict[str, object]:
    paragraphs = split_paragraphs(text)
    doc_language = detect_language(text)
    paragraph_reports = []
    all_hits: list[dict[str, str]] = []

    for index, paragraph in enumerate(paragraphs, start=1):
        language, hits = scan_paragraph(paragraph)
        paragraph_reports.append(
            {
                "paragraph": index,
                "language": language,
                "hits": hits,
            }
        )
        for hit in hits:
            enriched_hit = dict(hit)
            enriched_hit["paragraph"] = index
            all_hits.append(enriched_hit)

    if original_text is not None:
        # Document-level cross-check: only emit hits for paragraphs that
        # actually contain the missing marker. We locate the position of
        # each marker in the original and map it to a paragraph index.
        orig_paragraphs = split_paragraphs(original_text)
        orig_paragraph_index: dict[str, int] = {}
        for idx, para in enumerate(orig_paragraphs, start=1):
            for cite in _CITATION_RE.findall(para):
                orig_paragraph_index.setdefault(cite, idx)
            for number in _NUMBER_RE.findall(para):
                orig_paragraph_index.setdefault(number, idx)
        for hit in _diff_citation_markers(original_text, text):
            hit["paragraph"] = orig_paragraph_index.get(hit["match"], 0)
            all_hits.append(hit)

    lengths = sentence_lengths(text)
    rhythm = None
    if len(lengths) >= 6:
        mean_length = statistics.mean(lengths)
        if mean_length:
            cv = statistics.pstdev(lengths) / mean_length
            if cv < rhythm_threshold:
                rhythm = {
                    "severity": "low",
                    "label": "uniform sentence rhythm",
                    "detail": f"coefficient of variation {cv:.2f}",
                }

    return {
        "language": doc_language,
        "paragraphs": len(paragraphs),
        "hits": all_hits,
        "paragraph_reports": paragraph_reports,
        "rhythm": rhythm,
    }


def _format_suggestion(label: str) -> str:
    suggestion = SUGGESTIONS.get(label)
    if not suggestion:
        return ""
    return f"  ↳ {suggestion}"


def print_plain(report: dict[str, object], include_suggestions: bool = False) -> None:
    print(f"Language: {report['language']}")
    print(f"Paragraphs: {report['paragraphs']}")
    print(f"Hits: {len(report['hits'])}")
    print()

    hits = report["hits"]
    if hits:
        for hit in hits:
            line = f"[P{hit['paragraph']}] {hit['severity']} {hit['label']}: {hit['match']}"
            print(line)
            if include_suggestions:
                suggestion = _format_suggestion(hit["label"])
                if suggestion:
                    print(suggestion)
    else:
        print("No pattern hits found.")

    rhythm = report["rhythm"]
    if rhythm:
        print()
        print(f"Doc note: {rhythm['severity']} {rhythm['label']} ({rhythm['detail']})")
        if include_suggestions:
            suggestion = _format_suggestion(rhythm["label"])
            if suggestion:
                print(f"  ↳ {suggestion}")


def _attach_suggestions(report: dict[str, object]) -> dict[str, object]:
    """Attach a 'suggestion' field to every hit and rhythm entry, suitable for JSON."""
    out = dict(report)
    enriched_hits = []
    for hit in out["hits"]:
        new_hit = dict(hit)
        new_hit["suggestion"] = SUGGESTIONS.get(hit["label"], "")
        enriched_hits.append(new_hit)
    out["hits"] = enriched_hits

    if out.get("rhythm"):
        new_rhythm = dict(out["rhythm"])
        new_rhythm["suggestion"] = SUGGESTIONS.get(new_rhythm["label"], "")
        out["rhythm"] = new_rhythm

    return out


def main() -> None:
    args = parse_args()
    text = read_text(args)
    original_text = (
        Path(args.compare).read_text(encoding="utf-8-sig") if args.compare else None
    )
    report = build_report(
        text,
        rhythm_threshold=args.rhythm_threshold,
        original_text=original_text,
    )
    include_suggestions = args.suggest or args.json
    if args.json:
        print(json.dumps(_attach_suggestions(report), ensure_ascii=False, indent=2))
    else:
        print_plain(report, include_suggestions=include_suggestions)


if __name__ == "__main__":
    main()
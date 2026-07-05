#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path


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
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan academic prose for common Chinese and English AI-writing patterns."
    )
    parser.add_argument("path", nargs="?", help="Path to a UTF-8 text file")
    parser.add_argument("--stdin", action="store_true", help="Read text from standard input")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of plain text")
    return parser.parse_args()


def read_text(args: argparse.Namespace) -> str:
    if args.stdin:
        return sys.stdin.read()
    if not args.path:
        raise SystemExit("Provide a file path or use --stdin.")
    return Path(args.path).read_text(encoding="utf-8-sig")


def detect_language(text: str) -> str:
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    latin_words = len(re.findall(r"[A-Za-z]+", text))
    if cjk and latin_words:
        if cjk > latin_words * 1.5:
            return "zh"
        if latin_words > cjk * 1.5:
            return "en"
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


def sentence_lengths(text: str) -> list[int]:
    parts = re.split(r"[。！？!?]+|(?<=[.])\s+", text)
    lengths = [token_length(part) for part in parts if token_length(part) > 0]
    return lengths


def scan_paragraph(text: str) -> tuple[str, list[dict[str, str]]]:
    language = detect_language(text)
    patterns = []
    if language in {"zh", "mixed"}:
        patterns.extend(ZH_PATTERNS)
    if language in {"en", "mixed"}:
        patterns.extend(EN_PATTERNS)

    hits = []
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
            }
        )
    return language, hits


def build_report(text: str) -> dict[str, object]:
    paragraphs = split_paragraphs(text)
    doc_language = detect_language(text)
    paragraph_reports = []
    all_hits = []

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

    lengths = sentence_lengths(text)
    rhythm = None
    if len(lengths) >= 6:
        mean_length = statistics.mean(lengths)
        if mean_length:
            cv = statistics.pstdev(lengths) / mean_length
            if cv < 0.22:
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


def print_plain(report: dict[str, object]) -> None:
    print(f"Language: {report['language']}")
    print(f"Paragraphs: {report['paragraphs']}")
    print(f"Hits: {len(report['hits'])}")
    print()

    hits = report["hits"]
    if hits:
        for hit in hits:
            print(
                f"[P{hit['paragraph']}] {hit['severity']} {hit['label']}: "
                f"{hit['match']}"
            )
    else:
        print("No pattern hits found.")

    rhythm = report["rhythm"]
    if rhythm:
        print()
        print(
            f"Doc note: {rhythm['severity']} {rhythm['label']} "
            f"({rhythm['detail']})"
        )


def main() -> None:
    args = parse_args()
    text = read_text(args)
    report = build_report(text)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_plain(report)


if __name__ == "__main__":
    main()

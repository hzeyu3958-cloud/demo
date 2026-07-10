# Changelog

All notable changes to this skill are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project
adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- `examples/` directory with paired before/after Chinese and English passages.
- `LICENSE` (MIT) and this `CHANGELOG`.
- GitHub Actions workflow at `.github/workflows/test.yml` running unit tests
  on Python 3.9–3.12 plus a scanner CLI smoke check.
- `--suggest` flag on `scripts/pattern_scan.py` to attach a repair suggestion
  to every hit in the plain-text output. JSON output always includes the
  `suggestion` field.
- `--compare <ORIGINAL_FILE>` flag on the scanner to flag citation markers
  and key numbers present in the original text but missing from the rewrite
  as `citation markers lost` or `numeric content lost` hits.
- `--rhythm-threshold` flag on the scanner to tune the uniform-rhythm CV.
- Em-dash staging detector (paragraph-level): three or more em-dashes in a
  paragraph are flagged.
- `casual drift` pattern (Chinese): catches `说白了`, `绕不开的坎`, etc.
- Suggestions table keyed by pattern label, exposed via the JSON path and
  through `--suggest` for plain-text output.
- `version` and `metadata` blocks in `agents/openai.yaml`, plus four example
  prompts that cover English polishing, Chinese polishing, AIGC-risk
  paragraph revision, and file-based batch processing.
- 50+ unit tests covering every Chinese and English pattern, abbreviation
  handling, language detection, mixed paragraphs, paragraph-level checks,
  citation/number diff, rhythm detection, suggestions, and stdin encoding.

### Changed

- `split_sentences` now protects full abbreviation tokens (e.g. `i.e.`,
  `et al.`, `Fig.`) via a sentinel replacement, so internal and trailing
  periods both survive sentence splitting.
- Each scan hit now carries a `language` tag (`"zh"`, `"en"`, or `""` for
  document-level checks) so mixed paragraphs no longer conflate language
  attribution.
- `agents/openai.yaml` `default_prompt` clarified to remind callers that
  facts, citations, terminology, and numbers must stay stable.
- `SKILL.md` frontmatter `description` shortened to a routing summary;
  detailed trigger words now live only in the relevant reference files.

### Notes

- The scanner is a writing-risk locator, not a detector verdict. Lower
  hit counts after a rewrite are encouraging but not a guarantee.
- Suggestion text is curated to stay aligned with the rewriting guidance in
  `references/chinese-academic.md` and `references/english-academic.md`.
  When you change one, update the other.

## [0.1.0] — Initial skill

- `SKILL.md` with bilingual polishing, AIGC-risk reduction, and route-by-size
  workflow.
- `references/polishing.md`, `references/workflow.md`,
  `references/chinese-academic.md`, `references/english-academic.md`.
- `scripts/pattern_scan.py` with regex-based Chinese/English pattern
  scanning, JSON output, stdin support, and rhythm heuristic.
- `tests/test_pattern_scan.py` with the original four smoke tests.
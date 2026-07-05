# Academic Humanizer

`academic-humanizer` is a Codex-compatible skill for revising Chinese and English academic prose so it reads more natural and less templated while preserving facts, citations, terminology, and academic register.

## What it does

- Reduces obvious AI-writing traces in CN/EN academic text
- Preserves structure, terminology, formulas, citations, and claim strength
- Includes separate Chinese and English rewriting guides
- Includes a lightweight pattern scanner for detector-prone phrasing

## Repository layout

```text
.
|- SKILL.md
|- agents/
|  |- openai.yaml
|- references/
|  |- chinese-academic.md
|  |- english-academic.md
|- scripts/
|  |- pattern_scan.py
```

## Use in Codex

Place this folder where Codex can discover skills, or invoke it by path.

Example prompt:

```text
Use $academic-humanizer to revise this academic passage so it sounds natural, stays formal, and preserves facts and citations.
```

## Pattern scanner

You can scan a text file before rewriting:

```bash
python scripts/pattern_scan.py path/to/text.txt
python scripts/pattern_scan.py path/to/text.txt --json
Get-Content path/to/text.txt | python scripts/pattern_scan.py --stdin
```

## Notes

- This skill focuses on rewriting quality and register control.
- It is designed for academic papers, theses, literature reviews, methods, results, discussions, and technical reports.

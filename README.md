# Academic Humanizer

`academic-humanizer` is a Codex-compatible skill for revising Chinese and English academic prose so it reads more natural and less templated while preserving facts, citations, terminology, and academic register.

## What it does

- Reduces obvious AI-writing traces in CN/EN academic text
- Handles Chinese thesis/CNKI-style AIGC wording risks such as AI rate, red/high-risk passages, and detector-prone academic paragraphs
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
|  |- workflow.md
|- scripts/
|  |- pattern_scan.py
|- tests/
|  |- test_pattern_scan.py
```

## Install for Codex

Place this folder where Codex can discover skills, or invoke it by path.

Windows PowerShell:

```powershell
$skills = Join-Path $env:USERPROFILE ".codex\skills"
$target = Join-Path $skills "academic-humanizer"
New-Item -ItemType Directory -Force $target | Out-Null
Copy-Item -Recurse -Force SKILL.md, agents, references, scripts $target
```

macOS/Linux:

```bash
skills_dir="${CODEX_HOME:-$HOME/.codex}/skills"
target="$skills_dir/academic-humanizer"
mkdir -p "$target"
cp -R SKILL.md agents references scripts "$target/"
```

Validate the skill:

```powershell
$env:PYTHONUTF8="1"
$quickValidate = Join-Path $env:USERPROFILE ".codex\skills\.system\skill-creator\scripts\quick_validate.py"
python $quickValidate .
```

Or, with a different Codex home, run the same `quick_validate.py` from your installed `skill-creator` skill.

## Use in Codex

Example prompt:

```text
Use $academic-humanizer to revise this Chinese thesis paragraph flagged as high AI risk. Keep facts, citations, terminology, and academic register.
```

## Pattern scanner

You can scan a text file before rewriting:

```bash
python scripts/pattern_scan.py path/to/text.txt
python scripts/pattern_scan.py path/to/text.txt --json
python -X utf8 scripts/pattern_scan.py path/to/text.txt --json
Get-Content -Raw -Encoding UTF8 path/to/text.txt | python -X utf8 scripts/pattern_scan.py --stdin
```

Run tests:

```bash
python -m unittest discover -s tests
```

## Notes

- This skill focuses on rewriting quality and register control.
- It is designed for academic papers, theses, literature reviews, methods, results, discussions, and technical reports.
- It does not guarantee a specific detector score. Treat scanner output as a writing-risk locator, not a detector verdict.

# Examples

Each example pairs a typical AI-flagged paragraph with a revised version. The scanner output between the two shows what the skill tries to detect and fix.

```bash
# Scan before/after text and compare what the scanner catches
python scripts/pattern_scan.py examples/chinese-thesis-before.txt --suggest
python scripts/pattern_scan.py examples/chinese-thesis-after.txt
```

Use these as a sanity check when you change the scanner, the rewriting guides, or the suggestion table.

| File | What it covers |
| --- | --- |
| `chinese-thesis-before.txt` / `chinese-thesis-after.txt` | Theory-first opening, template goal, list symmetry, abstract noun chain, empty ending |
| `english-abstract-before.txt` / `english-abstract-after.txt` | Aim boilerplate, significance inflation, participle padding, rule of three, generic conclusion |
---
name: academic-humanizer
description: >
  Revise and polish Chinese and English academic prose while preserving facts, citations, terminology,
  structure, and academic register. Supports normal bilingual academic polishing, grammar correction,
  clarity improvement, journal-style language editing, thesis polishing, and Chinese academic-paper AIGC
  risk reduction. Use when the user asks to polish, copyedit, proofread, improve clarity, improve flow,
  revise academic writing, lower AIGC rate, reduce AI rate, remove AI tone, humanize academic writing,
  revise detector-prone text, or says 润色, 语言润色, 学术润色, 表达优化, 修改病句, 语法修改, 去AI味,
  降AIGC, 知网AIGC, AI率, 红色显著, 论文降AI, 论文润色, 毕业论文, 硕博论文, 中文学术段落改写, or 降低AI查重误判.
---

# Academic Humanizer

## Overview

Revise academic prose so it reads like careful human writing rather than templated model output. Support both ordinary academic polishing and detector-risk reduction. Prefer specific, disciplined edits over sweeping paraphrase. Treat detector reduction as a writing-quality task, not a promise to bypass any particular platform.

## Non-negotiables

- Preserve facts, numbers, formulas, citations, figure/table references, named methods, and conclusions unless the user explicitly asks to change substance.
- Preserve paragraph order and section logic by default. Keep roughly the same paragraph count unless the original structure is clearly broken.
- Keep academic register. Do not replace AI stiffness with slang, marketing tone, or casual chat.
- Do not invent sources, examples, experiments, limitations, future work, or stronger claims than the text supports.
- If the text already reads naturally, minimize edits instead of forcing variation.

## Choose the path

- Read `references/polishing.md` when the user asks for normal polishing, grammar correction, clarity, readability, journal-style editing, 润色, 学术润色, 表达优化, 修改病句, or 语法修改 without explicit AIGC/detector language.
- Read `references/workflow.md` for long text, file-based work, CNKI/AIGC report passages, or batch paragraph selection.
- Read `references/chinese-academic.md` when the text is mostly Chinese and the user asks for 去AI味, 降AIGC, 知网AIGC, AI率, 红色显著, or 中文学术改写.
- Read `references/english-academic.md` when the text is mostly English and the user asks to humanize, de-template, or reduce detector-prone academic writing.
- If the document is mixed, handle each paragraph in its dominant language.
- If the user provides a writing sample, match its rhythm, transition habits, level of directness, and preferred degree of author presence.

## Audit first

For long text, file-based work, AIGC requests, or uncertain detector-risk cases, run the scanner before rewriting:

```bash
python scripts/pattern_scan.py <path-to-text-file>
python scripts/pattern_scan.py <path-to-text-file> --json
Get-Content <path-to-text-file> | python scripts/pattern_scan.py --stdin
python -X utf8 scripts/pattern_scan.py <path-to-text-file>
```

Treat the scanner as a heuristic, not a verdict. Use it to locate likely trouble spots, then apply judgment. For ordinary polishing requests, do not run the scanner unless it helps locate awkward phrasing in a long file.

## Rewrite workflow

1. Choose the mode: polishing, AIGC-risk reduction, or both if the user explicitly asks for both.
2. For polishing, improve grammar, clarity, concision, cohesion, and academic register while preserving meaning.
3. For AIGC-risk reduction, identify 3 to 8 high-risk patterns with paragraph references and remove templated signals first.
4. Rebuild sentence rhythm only as much as the mode requires. Keep formal control.
5. Normalize terminology. Stop synonym cycling when one term should stay stable across the paper.
6. Self-audit by asking: "Did I preserve the evidence and satisfy the requested mode?" Fix issues before delivering.

## Section strategy

- Abstract: compress ceremony; keep aim, method, result, and takeaway.
- Literature review: synthesize tensions and group findings; avoid `A says / B says / C says` listing.
- Methods: prefer precise actions, conditions, and measurements over inflated framing.
- Results: state what the data shows; avoid generic statements about importance.
- Discussion: keep interpretation, uncertainty, and scope aligned with the evidence.
- Conclusion: avoid "broad prospects" boilerplate; end with a concrete implication, limitation, or next question already grounded in the text.

## Whole-document handling

- For a full paper or thesis chapter, rewrite section by section rather than regenerating the entire document in one freeform pass.
- Keep citations and cross-references stable. If a change would force citation rewiring, stop and preserve the original structure.
- If the document contains tables, formulas, or figure captions, edit surrounding prose first and touch those elements only when necessary.

## Output

Default to:

1. The final polished or revised text.
2. A short note on main changes only when useful or requested.

For AIGC-risk requests, include a short audit of main risks before the rewrite unless the user asks for final text only. Only include a draft version, detailed change log, or paragraph-by-paragraph notes when the user asks for them or the differences are subtle.

## Resources

- `scripts/pattern_scan.py`: heuristic scanner for common Chinese and English AI-writing patterns.
- `references/polishing.md`: bilingual academic polishing guide for Chinese and English grammar, clarity, flow, and journal-style language editing.
- `references/workflow.md`: routing, batch handling, and self-audit workflow for Chinese AIGC/CNKI-style scenarios.
- `references/chinese-academic.md`: Chinese academic rewriting guide with register constraints and high-risk patterns.
- `references/english-academic.md`: English academic rewriting guide with high-risk patterns and section-specific advice.

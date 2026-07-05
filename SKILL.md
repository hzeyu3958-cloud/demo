---
name: academic-humanizer
description: >
  Revise Chinese and English academic prose to reduce obvious AI-writing traces while preserving facts,
  citations, terminology, structure, and academic register. Strongly supports Chinese academic-paper
  scenarios such as CNKI AIGC checks, red/high-risk detector passages, thesis paragraph rewriting,
  literature reviews, methods/results/discussion sections, and technical reports. Use when the user asks
  to lower AIGC rate, reduce AI rate, remove AI tone, humanize academic writing, revise detector-prone
  text, or says 去AI味, 降AIGC, 知网AIGC, AI率, 红色显著, 论文降AI, 论文润色, 毕业论文, 硕博论文,
  中文学术段落改写, or 降低AI查重误判.
---

# Academic Humanizer

## Overview

Revise academic prose so it reads like careful human writing rather than templated model output. Prefer specific, disciplined edits over sweeping paraphrase. Treat detector reduction as a writing-quality task, not a promise to bypass any particular platform.

## Non-negotiables

- Preserve facts, numbers, formulas, citations, figure/table references, named methods, and conclusions unless the user explicitly asks to change substance.
- Preserve paragraph order and section logic by default. Keep roughly the same paragraph count unless the original structure is clearly broken.
- Keep academic register. Do not replace AI stiffness with slang, marketing tone, or casual chat.
- Do not invent sources, examples, experiments, limitations, future work, or stronger claims than the text supports.
- If the text already reads naturally, minimize edits instead of forcing variation.

## Choose the path

- Read `references/workflow.md` for long text, file-based work, CNKI/AIGC report passages, or batch paragraph selection.
- Read `references/chinese-academic.md` when the text is mostly Chinese or when the user asks for 去AI味, 降AIGC, 知网AIGC, AI率, 红色显著, 论文润色, or 中文学术改写.
- Read `references/english-academic.md` when the text is mostly English or when the user asks to humanize, de-template, or polish English academic writing.
- If the document is mixed, handle each paragraph in its dominant language.
- If the user provides a writing sample, match its rhythm, transition habits, level of directness, and preferred degree of author presence.

## Audit first

For long text, file-based work, or uncertain cases, run the scanner before rewriting:

```bash
python scripts/pattern_scan.py <path-to-text-file>
python scripts/pattern_scan.py <path-to-text-file> --json
Get-Content <path-to-text-file> | python scripts/pattern_scan.py --stdin
python -X utf8 scripts/pattern_scan.py <path-to-text-file>
```

Treat the scanner as a heuristic, not a verdict. Use it to locate likely trouble spots, then apply judgment.

## Rewrite workflow

1. Identify 3 to 8 high-risk patterns with paragraph references.
2. Remove templated signals first: canned openers, generic significance claims, vague attributions, filler transitions, rule-of-three symmetry, and boilerplate endings.
3. Rebuild sentence rhythm. Mix shorter and longer sentences, but stay formal and controlled.
4. Replace abstract inflation with concrete claims, observations, limits, or mechanisms already supported by the text.
5. Normalize terminology. Stop synonym cycling when one term should stay stable across the paper.
6. Self-audit by asking: "What still sounds obviously AI-written?" Fix those traces before delivering.

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

1. A short audit of the main risks.
2. The final rewrite.

Only include a draft version, detailed change log, or paragraph-by-paragraph notes when the user asks for them or the differences are subtle.

## Resources

- `scripts/pattern_scan.py`: heuristic scanner for common Chinese and English AI-writing patterns.
- `references/workflow.md`: routing, batch handling, and self-audit workflow for Chinese AIGC/CNKI-style scenarios.
- `references/chinese-academic.md`: Chinese academic rewriting guide with register constraints and high-risk patterns.
- `references/english-academic.md`: English academic rewriting guide with high-risk patterns and section-specific advice.

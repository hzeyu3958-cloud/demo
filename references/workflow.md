# Academic AIGC workflow

Read this file for long Chinese academic text, file-based work, pasted CNKI/AIGC report excerpts, or requests that mention AI rate, red/high-risk passages, detector-prone paragraphs, or batch thesis revision.

## Core stance

- Reduce detector-prone writing patterns by improving prose quality and variation.
- Do not promise a target score or guaranteed bypass.
- Preserve facts, numbers, variables, equations, citations, terminology, model names, table/figure references, and claim strength.
- Keep paragraph order and section logic unless the user asks for structural revision.
- Prefer local edits to full regeneration.

## Route by input size

### Route A: focused revision under 800 Chinese characters

Use this when the user pastes one short paragraph or one red/high-risk segment.

1. Identify the 2 to 4 strongest risk patterns.
2. Rewrite the paragraph while preserving all hard constraints.
3. Check that the paragraph length stays close to the original, usually within about 15 percent unless the original is padded.
4. Return the revised paragraph plus a short note on the main edits when useful.

Default output:

```text
主要风险：...

改写版：
...
```

If the user says "只给终稿" or "直接改", return only the rewrite.

### Route B: batch handling above 800 Chinese characters

Use this when the user pastes a full section, thesis chapter, or multiple paragraphs.

1. Segment by original paragraphs.
2. Rank paragraphs by risk instead of rewriting everything immediately.
3. Report the high-risk paragraph list with short labels, such as symmetry, vague attribution, data boilerplate, abstract noun chain, or empty ending.
4. Ask the user which paragraphs to revise only if the scope is large or ambiguous. If the user clearly asks to process all, revise section by section.
5. Preserve paragraph numbering, headings, references, equations, and list structure.

Default ranking format:

```text
高风险段落：
- P2：模板目标句、三项并列、泛化结尾
- P5：数据套话、段末元话语
- P7：抽象名词链、术语主语位置固定
```

### Route C: file-based work

Use the scanner first for plain text files:

```bash
python -X utf8 scripts/pattern_scan.py path/to/file.txt --json
```

For Windows PowerShell pipelines, prefer:

```powershell
Get-Content -Raw -Encoding UTF8 path\to\file.txt | python -X utf8 scripts\pattern_scan.py --stdin
```

Treat the scanner as a locator. It is not a detector verdict and should not override close reading.

## Chinese paper hard constraints

Before returning a rewrite, verify:

- Numbers, percentages, p values, coefficients, variables, formulas, years, author names, and citation markers are unchanged.
- Domain terms are stable. Do not replace accepted terms just for variety.
- Model names and method names remain unchanged, such as fixed effects, mediation effect, robustness test, SEM, DID, LSTM, or ANOVA.
- The rewrite does not add new causes, sources, samples, experiments, limitations, or conclusions.
- The academic register remains intact; avoid turning a thesis paragraph into a blog paragraph.

## High-risk Chinese academic patterns

### Red/high-risk report segments

When a user says a paragraph is "红色显著", "疑似", or "AI率高", focus on local structure:

- repetitive sentence openings
- theory-first openings
- evenly weighted triads
- abstract noun chains
- generic final sentences
- vague attributions without a source
- data-reporting boilerplate

### Abstract noun chains

Risk:

```text
传导机制的动态监测体系为创新能力转化路径提供支撑
```

Prefer concrete relations already present in the text:

```text
该指标主要用于观察外部技术能否继续转化为企业创新能力
```

### Paragraph-final meta commentary

Risk:

```text
上述结果表明……具有重要意义。
这一结论为后续研究提供了理论依据。
```

Prefer a grounded close:

```text
这一差异主要出现在高技术行业，传统制造业样本中的变化并不明显。
```

### Fixed term position

Risk:

```text
逆向技术溢出转化为创新能力。
```

Prefer moving the term into a topic or object position when the meaning allows:

```text
企业能否把逆向技术溢出转化为创新能力，取决于内部研发投入是否跟得上。
```

### Parallel exposition plus closing summary

Risk:

```text
从产业基础看……；从人力资本看……；从投资动机看……。上述分析说明……
```

Prefer uneven emphasis:

```text
产业基础是更直接的解释。中部地区仍处于工业化中期，对外投资后的技术吸收空间较大。人力资本也有影响，但主要体现在工程技术劳动力供给上。投资动机则更像边界条件。
```

## Self-audit

Ask these questions before delivery:

- Does any paragraph still open with a theory/framework formula?
- Does the ending only repeat "important significance" or "future prospects"?
- Are there two or more triads in the same paragraph?
- Did the rewrite change any numeric or citation content?
- Did the prose drift into casual speech?
- Did synonym variation weaken a technical term?

If any answer reveals a problem, revise locally before returning.

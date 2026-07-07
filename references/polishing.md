# Bilingual academic polishing

Read this file when the user asks for academic polishing, language editing, grammar correction, clarity improvement, readability improvement, journal style editing, or says 润色, 语言润色, 学术润色, 修改病句, 语法修改, 表达优化, polish, copyedit, proofread, improve clarity, improve flow, or journal-ready language.

Use this mode when the request is about improving writing quality rather than reducing AIGC risk. If the user does not mention AIGC, AI rate, detector, CNKI, red/high-risk passages, or 去AI味, do not force detector-oriented edits.

## Scope

Polish Chinese and English academic writing by improving:

- grammar, punctuation, and word choice
- sentence clarity and logical flow
- academic register and concision
- cohesion between sentences and paragraphs
- consistency of terminology, tense, voice, and notation
- title, abstract, introduction, literature review, methods, results, discussion, conclusion, captions, and technical reports

## Non-negotiables

- Preserve facts, data, citations, formulas, table/figure references, terminology, and claim strength.
- Do not add sources, data, explanations, limitations, or conclusions.
- Do not translate unless the user asks for translation.
- Do not turn formal academic writing into conversational prose.
- Keep the original language unless the user asks for bilingual output or translation.
- Keep paragraph structure by default. Merge or split paragraphs only when the user asks for structural editing or the original flow is clearly broken.

## Choose polishing intensity

### Light polish

Use when the text is already acceptable or the user asks for minor polishing.

- Fix grammar, punctuation, typos, and awkward phrasing.
- Preserve sentence order and most wording.
- Avoid changing terminology or rhetorical stance.

### Standard polish

Use by default for academic proofreading and journal-style language editing.

- Improve clarity, concision, transitions, and sentence rhythm.
- Remove redundancy and unclear modifiers.
- Smooth paragraph flow while preserving structure.

### Deep polish

Use only when the user asks for heavy revision, journal-ready language, native-like expression, or major readability improvement.

- Rebuild awkward sentences.
- Improve paragraph-level cohesion.
- Clarify logical relations and reduce ambiguity.
- Note any places where meaning is uncertain instead of guessing.

## Chinese academic polishing

Prioritize:

- Replace unclear long sentences with controlled shorter clauses.
- Remove duplicated modifiers such as `一定程度上`, `较为`, `有效`, `显著` when they do not add meaning.
- Keep formal connectors when they support logic: `因此`, `然而`, `相较而言`, `在此基础上`, `这意味着`.
- Make subjects and actions explicit when the sentence is too abstract.
- Keep accepted terms stable across the paragraph.
- Avoid excessive colloquial phrasing, rhetorical questions, internet expressions, or emotional emphasis.

Common fixes:

| Issue | Polish toward |
| --- | --- |
| 句子过长、层层嵌套 | Split into two sentences or reorder clauses |
| 主语缺失 | Add the actor, variable, method, or study object already present |
| 抽象名词堆叠 | Convert some nouns into verbs or relations |
| 连接词重复 | Keep only the connector that carries the real logic |
| 语义泛化 | State the concrete scope, mechanism, or boundary |

## English academic polishing

Prioritize:

- Use precise verbs over inflated academic verbs.
- Fix article use, prepositions, tense consistency, agreement, and parallelism.
- Reduce nominalization when it hides the action.
- Keep hedging appropriate: use `may`, `suggest`, or `is associated with` only when the evidence requires it.
- Preserve field-specific terms and conventional phrasing.
- Prefer clear sentence order: topic, evidence, interpretation.

Common fixes:

| Issue | Polish toward |
| --- | --- |
| wordy framing | direct academic statement |
| vague pronoun reference | explicit noun phrase |
| stacked nouns | clearer prepositional or verbal structure |
| inconsistent tense | tense appropriate to section |
| overstrong claim | claim strength aligned with evidence |

## Section guidance

- Title: make it concise and specific; do not add claims absent from the paper.
- Abstract: keep aim, method, result, and conclusion dense but readable.
- Introduction: clarify problem, gap, and contribution without exaggeration.
- Literature review: improve synthesis and transitions between research streams.
- Methods: prioritize precision, reproducibility, and stable terminology.
- Results: state trends, comparisons, and statistical outcomes clearly.
- Discussion: separate result interpretation from speculation.
- Conclusion: remove repetition and close with the actual contribution or boundary.

## Output

Default output:

```text
润色版 / Polished version:
...
```

If edits are substantial, add a short note:

```text
主要调整：精简重复表达；统一术语；理顺因果关系。
```

If the user asks for tracked changes, comparison, or explanation, provide:

- original sentence
- polished sentence
- reason for the change

For long text, polish section by section and avoid expanding the full explanation unless requested.

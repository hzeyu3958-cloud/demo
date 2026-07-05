# Chinese academic rewriting guide

Read this file when the text is mostly Chinese or when the request is about 去AI味, 降AIGC, 知网AIGC, AI率, 红色显著, 论文润色, 学术改写, or 中文学术表达.

## Keep these constraints

- Preserve facts, data, formulas, citations, terminology, and the original claim strength.
- Preserve numbers, percentages, p values, coefficients, variables, years, author names, table/figure references, and citation markers exactly.
- Preserve model names and accepted field terms. Do not replace terms such as `固定效应`, `中介效应`, `稳健性检验`, `逆向技术溢出`, or `互补效应` only for stylistic variety.
- Preserve academic register. Allow controlled directness, but do not drift into spoken Chinese or internet slang.
- Keep `本文` / `本研究` / `笔者` only when the genre and source text support them.
- Prefer concrete observations and mechanisms over ceremonial phrasing.
- Do not add new causes, samples, data, sources, limitations, future work, or conclusions.

## CNKI-style paragraph handling

For paragraphs reported as `红色显著`, `疑似`, or high `AI率`, prioritize structural edits over synonym replacement.

For one short paragraph, identify the 2 to 4 most important risks and revise directly.

For a long section, rank paragraphs first. Do not rewrite the whole section in one pass unless the user explicitly asks for full-section treatment.

When reporting risks, use paragraph labels such as:

- theory-first opening
- abstract noun chain
- paragraph-final meta commentary
- even triad or parallel exposition
- data-reporting boilerplate
- vague attribution
- fixed term position
- generic significance ending

## Prioritize these fixes

### 1. Theory-first openings

Risk patterns:

- `基于……理论`
- `依据……框架`
- `从……视角出发`
- `在……理论框架下`

Prefer:

- Lead with the phenomenon, dataset, or problem first.
- Move the theory into the middle of the sentence if it still matters.

### 2. Template goals and inflated mission statements

Risk patterns:

- `本文旨在`
- `本研究致力于`
- `具有重要的理论意义和实践价值`
- `进行了深入分析`

Prefer:

- State the actual task directly.
- Replace broad significance claims with the specific contribution already present in the text.

### 3. Generic importance inflation

Risk patterns:

- `至关重要`
- `不可忽视`
- `深远影响`
- `广阔前景`
- `具有重要意义`

Prefer:

- Say what changed, where it applies, or what remains uncertain.
- If the sentence still works after deleting the adjective, delete it.

### 4. Vague attributions

Risk patterns:

- `有研究表明`
- `学界普遍认为`
- `众所周知`
- `相关研究指出`

Prefer:

- Cite the source if one is already available.
- Otherwise turn the claim into the paper's own judgment or remove it.

### 5. Symmetry and list addiction

Risk patterns:

- `首先 / 其次 / 最后`
- `理论上 / 实践上 / 方法上`
- three equally weighted clauses in one sentence or paragraph

Prefer:

- Break symmetry.
- Keep two points if only two matter.
- Give the most important point more space than the others.

### 6. Data boilerplate

Risk patterns:

- `从图中可以看出`
- `数据显示`
- `分析结果表明`
- `实验结果表明`

Prefer:

- Mention the concrete trend or comparison.
- Use direct phrasing such as `图2显示……` or `三组数据的差异主要体现在……`.

### 7. Empty endings

Risk patterns:

- `综上所述`
- `由此可见`
- `具有重要意义`
- `有待进一步研究`

Prefer:

- End with a specific implication, limit, unresolved point, or next step grounded in the existing text.

### 8. Overused connectors

Risk patterns:

- `此外`
- `与此同时`
- `值得注意的是`
- `需要指出的是`
- `具体而言`

Prefer:

- Delete many of them.
- Let paragraph adjacency or sentence order do the transition work.

### 9. Synonym cycling

Risk patterns:

- The same object is renamed repeatedly only for variation.
- The same method or indicator rotates through multiple near-synonyms.

Prefer:

- Choose one term when precision matters.
- Vary only where the field genuinely uses multiple accepted terms.

### 10. Overclean rhythm

Risk patterns:

- Every sentence is medium length.
- Every paragraph closes with the same kind of summary.

Prefer:

- Introduce mild variation in cadence.
- Insert one short sentence when it sharpens the point, but stay formal.

### 11. Abstract noun chains

Risk patterns:

- `传导机制的动态监测体系`
- `创新能力转化路径`
- `多维协同治理框架`
- `高质量发展赋能机制`

Prefer:

- Convert stacked nouns into actor-action-object relations.
- Keep the technical term if it is a field term, but make the sentence say what changes, who does it, or where it appears.

### 12. Paragraph-final meta commentary

Risk patterns:

- `上述结果表明`
- `这一结论说明`
- `该发现为后续研究提供了依据`
- `这一分析具有重要意义`

Prefer:

- End with the concrete difference, boundary, or unresolved point already supported by the paragraph.
- Delete final summary sentences when they only restate the paragraph.

### 13. Fixed term position

Risk patterns:

- A technical term repeatedly appears as the grammatical subject.
- Adjacent sentences share the same `术语 + 动词 + 抽象宾语` structure.

Prefer:

- Move the term into topic, object, or condition position when meaning permits.
- Keep the term itself stable.

### 14. Parallel exposition plus closing summary

Risk patterns:

- `从X看……从Y看……从Z看……`
- `一方面……另一方面……同时……`
- Several equally long clauses followed by `因此/由此可见/综上`.

Prefer:

- Give the strongest point more space.
- Merge or shorten weaker points.
- Let the paragraph end on a specific analytical observation instead of a generic summary.

### 15. Over-correction into casual prose

Risk patterns:

- The rewrite removes all academic connectors.
- The paragraph starts to sound like commentary, blog writing, or spoken explanation.
- Phrases such as `说白了`, `其实就是`, `很明显`, or `绕不开的坎` appear in formal thesis prose.

Prefer:

- Keep a few restrained academic connectors such as `因此`, `鉴于`, `相较而言`, `二者`, `在此基础上`, or `这意味着`.
- Use controlled author judgment without colloquial performance.

## Keep the register academic

Allowed:

- Mild author judgment
- Controlled uncertainty
- Concrete operational details
- Specific limits and boundary conditions

Avoid:

- Network slang
- Emotional language
- Chatty fillers
- Motivational or promotional tone

## Quick replacements

| Risky phrase | Prefer |
| --- | --- |
| `本文旨在探讨` | `本文考察` / `本研究聚焦于` |
| `具有重要意义` | state the specific value directly |
| `值得注意的是` | delete / `一个细节是` |
| `从图中可以看出` | `图X显示` |
| `实验结果表明` | `结果显示` / `该结果提示` |
| `未来研究可进一步` | `本文暂未覆盖……` / state the concrete next question |
| `综上所述` | delete or replace with a precise closing claim |
| `上述结果表明` | state the concrete result directly |
| `为后续研究提供参考` | name the specific unresolved question |
| `传导机制较为契合` | explain which relation is consistent with which evidence |
| `在统计推断意义上获得支持` | `样本结果支持这一判断` |
| `从X角度来看` | make X the topic only when it carries real analytical weight |

## Section tips

- Abstract: keep density high and ceremony low.
- Literature review: group studies by tension, method, or finding instead of stacking names.
- Methods: sound like a researcher describing operations, not like a brochure.
- Results: let the numbers carry the sentence.
- Discussion: preserve uncertainty when the evidence is partial.
- Conclusion: cut slogans and keep the real boundary of the work visible.

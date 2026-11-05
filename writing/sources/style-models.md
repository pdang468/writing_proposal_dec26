# Style models: Murphy, Stanley, Ha

Three writers read as models, 2026-11-03. Samples per text: abstract, intro paragraphs 1 and 2, one numeric results paragraph, first discussion paragraph; counts are from those samples (about 30 sentences per text) and are approximate.

Texts. Murphy: arXiv 2204.07576 (Distributed IB), 2211.17264 (ICLR 2023), 2307.04755 (PNAS 2024). Stanley: NEAT (Evol. Comp. 2002), novelty search (Lehman and Stanley, Evol. Comp. 2011), POET (arXiv 1901.01753). Ha: World Models (1803.10122), Weight Agnostic Neural Networks (1906.04358), Evolutionary Model Merging (2403.13187, Ha last author).

Note on provenance: "Ken's Writing Tips" is Kenneth O. Stanley's page from his EPlex lab site (2008, updated 2011). The file `advisor-writing-tips.md` calls it the advisor's note; the rules are Stanley's.

## Measured habits

| Habit | Murphy | Stanley | Ha |
| --- | --- | --- | --- |
| Mean sentence length (words) | 27 | 21 (NEAT), 29 to 31 (later) | 22 to 25 |
| "we" per 10 sentences | 1.9 | 1.2 to 2.5 (5 in the whole 2011 paper) | 2.4 to 4.1 |
| "use" per 10 sentences | 0.5 | 0 to 0.9 | 0.4 to 2.2 |
| Bare "this" as subject | rare | 0 | rare |
| Hedges | "can" for capability; none in abstracts | 4 to 5 per 10 on claims about search, 0 on numbers | modal ("may", "we believe") |
| Intensifiers | "particularly", "only"; no "very" | "significantly", "counterintuitively", "dramatically" | "even" is the signature; "remarkably" |
| Typical subject | the method, the quantity, the structure | the method, the search, the paper | the agent, the model, humans or animals, "we" |
| Paragraph opener | setup, then the claim at the end of paragraph 1 or 2 | thesis sentence first, then support | general claim about humans or the field, then the pivot to agents |
| Result sentence | number, then meaning | number, control, significance, then a separate reading | number, baseline, then the method contrast |
| Limitations | inside prose, as trade-offs | one paragraph, each limit with its mechanism | folded into the discussion as "may" possibilities |

## What each does that the others do not

Murphy. Abstract nouns act: information is "throttled", "eroded", "allocated"; the method "compresses", "localizes", "reveals". The subject is the quantity under study, so "we" is needed only at the pivot ("We introduce") and the finding ("we found"). Standard terms stay standard; the named thing is the output object (spectrum, continuum, decomposition), not the method. Sentences are long but each carries one subject-verb pair early and links backward by repeating a noun. Tension framing: the field has a strength and a block; the method keeps the strength and removes the block ("full complexity").

Stanley. Argument first. Paragraph one names the assumption to be attacked ("tempting to believe", "the prevailing assumption") and undercuts it with "Yet". Coinages are defined in apposition once, then owned without quotes (novelty search, stepping stones, deception). Analogy precedes mechanism (the finger trap, the giraffe). Objections are pre-empted inline ("no silver bullet"; the random-selection control answers "is it just random"). Results: the number, the control, the test, then the interpretive sentence on its own. He keeps his own rules strictly in the 2011 paper and relaxes them in multi-author papers; intensifiers appear in his framing paragraphs against his own "emphasis is bad".

Ha. The reader's intuition is the entry: humans, batters, ducklings, then "In contrast, when we train artificial agents". Vocabulary is plain and concrete; a concept gets a short noun phrase at first use, then an acronym. Figures and demos carry the argument and the number confirms what the reader has seen. "We" and "use" are frequent; the voice is closer to a talk than to Gopen and Swan's prose. Limitations arrive as possibilities for future work, not as bounds on the claim.

## Where the models conflict with the rulebook

| Rulebook | Model that breaks it | Resolution for the proposal |
| --- | --- | --- |
| Never "we" | Ha (4 per 10); Stanley after 2011 | Keep the rule. Murphy and the 2011 novelty paper show the method-as-subject prose works at full length. Allow "we" nowhere in the proposal; the pivot sentence reads "This proposal introduces". |
| No emphasis | Stanley's "counterintuitively", "dramatically"; Ha's "even" | Keep the rule. Stanley's emphasis sits on arguments, not numbers, and his numbers are reported flat; copy the flat number sentence, not the adverbs. |
| Fewest tokens (your preference) | Murphy and Stanley average 27 to 31 words per sentence | The sentence rules (one subject-verb pair early, old before new, one point) matter more than the word count. A 30-word sentence with one point reads faster than two 12-word sentences that split it. Cut repetition, not length. |
| Hedge once per claim | Stanley hedges 4 to 5 per 10 sentences on general claims | Hedge the generality of a claim once (seeds, corpus), never the number. |
| Conclusion first | Murphy opens with setup; Ha opens with analogy | Chapter and section openers state the claim first (style.md). Analogy and setup belong in the introduction chapter only, and after the claim. |

## What to take from each

- From Murphy: the quantity as subject; physical verbs for information (compress, leak, erode, allocate); the method named once and then the object it produces; "can" for capability only; the tension framing of Chapter 1.
- From Stanley: the thesis-first paragraph; a coinage defined once in apposition and then used bare (hub, anchor, budget, leak); the result sentence as number, control, test, then a separate reading; a limitations paragraph that gives a mechanism per limit; objections answered by a named control.
- From Ha: the concrete entry point for a non-specialist reader (the split-inference server that holds vectors it cannot read); figures that show the behavior before the table gives the number; one plain noun phrase per concept at first use.

## How the three sets of rules stack

1. Draft to find the argument (Hunt): pages every day, no rereading of notes, no sentence rules yet.
2. Revise structure (Gopen and Swan): each sentence opens with the term the reader holds and ends on the one new thing; the verb names the action; one point per unit.
3. Strip (Stanley's tips): "we", "use", bare "this", intensifiers, "in order to", "actually".
4. Check against the models: would Murphy let the quantity act here; would Stanley state the thesis before the support; would Ha's reader know why this matters by the end of the first paragraph.

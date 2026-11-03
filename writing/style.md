# Communication

One rulebook for every output: chat reply, plan, report, handoff, commit message. Revised 2026-10-25; replaces every earlier writing rule.

## Aim

The reader scans once and leaves with the answer, how sure it is, and what to do next. A message fails if it provokes "what does that mean", "how sure", or "so what do I do".

## Order: conclusion, then support

- Line one is the answer, verdict, or recommendation. Nothing precedes it: no preamble, no narration of the work, no "I checked".
- Each later block supports line one, in decreasing importance. A reader who stops anywhere has the most important part.
- Qualifications, units, and evidence sit beside the claim they qualify, never in a later section.
- Every explicit question in the request gets a visible answer. Unanswerable: say so where the answer would be.

## Blocks

- One block, one claim: a descriptive bold lead that states the claim itself ("**Batch 8192 gains only below budget 30.**", never "**Result.**"), then at most two sentences. The bold leads alone carry the whole argument.
- Numbers compared across items go in a table with both sides, the metric, and n. A single number stays inline or in the bold lead.
- Parallel items: list. Sequence: numbered. Comparison: table. Prose only for a single argument that needs its links.
- Executable commands, multi-line excerpts, and error text: fenced block. A short path or flag stays inline, at most one per sentence.
- A missing fact is named as missing ("no seed-2 run exists"), never guessed around.
- Stop when the content stops: no recap, no offer, no "let me know".

## Shapes

Default slots per message kind; a slot with nothing to say is dropped, and labels are adapted when the request needs it.

| Kind | Slots, in order |
| --- | --- |
| Answer | the answer; why; what the user does next |
| Status | done (number); running (lands at); blocked (cause). Table when more than three items |
| Options | pick (one option, one reason); the limit that bounds the result now (number); options numbered, each with what it changes, what it measures, its decisive trade-off; what remains unknown |
| Result | claim with its number; table; what the claim asserts but does not show; next run |
| Handoff | state (what exists, paths); open items; next command in a fenced block |
| Operational | one to three lines, no labels |

Meaning for the project, confidence (seeds, prompts, runs, what was not checked), and the next action appear in every Answer, Options, and Result message when the reader would otherwise ask for them; they are folded into the blocks, not appended as boilerplate.

An advisor-facing document follows the `report` skill, the one output that carries headers.

## Sentence rules (advisor's rules, `documents/writing/advisor-writing-tips.md`, apply to every output)

- Never "we". The subject is the model, the run, the map, the number, the user, the advisor. Passive voice beats "we". "I" appears only for an opinion or an uncertainty; "you" only for the user's own next action.
- The verb names the action: the map sends, the decoder generates, the run writes, the table lists. Never "use", "used", "using"; never filler (handles, involves, leverages, serves as, represents).
- "This" always carries a noun: "this run", never "This means".
- Old before new: open with a term the reader holds, end with the one new thing. Define a term once, at first use, then repeat it bare. Project terms come from the glossary; no coined names, no synonyms.
- One idea per sentence; a sentence carrying two new things is split.
- No intensifiers, no "actually", "essentially", "seems that", no colloquialisms, no advertising a result. At most one hedge per claim.
- A claim's generality is no stronger than its evidence. State the observation plainly ("seed 1 gains 0.03"), then bound its reach ("one seed, one corpus"); never "X hurts" from one run, never that a line of work is finished.
- A research question is one plain sentence; a plan with two questions numbers them and names the primary.
- No em dashes. Math only in `$$` display blocks.

## Length

| Output | Default budget |
| --- | --- |
| Operational | 3 lines |
| Answer, Status, Handoff | 80 words |
| Options, Result | 150 words plus one table |
| Report | `report` skill |

Completeness wins over the budget: a request with more parts gets a longer single message, never a split or an omission. Half the words otherwise: cut any sentence that restates a lead, a row, or a definition. No headers in chat.

## Experiment content

- Method as input -> process -> output; model direction explicit (A layer 3 -> hub -> B projector -> frozen B decoder). Compared paths name the one difference.
- Every metric: what was compared, how calculated, over how many examples; baseline and target when a gap is claimed.
- Round to what the sample size supports. A corpus's first text-overlap report shows a low, medium, and high example.
- Close a claim with what it asserts but does not show. Discarded methods stay out of the main narrative.
- Check models, direction, prompt count, and calculation against the config and evaluation code before writing. Never infer a metric's meaning from its name.

## Check before sending

Line one answers; every requested part is covered; evidence and limits sit beside their claims; grep finds no "we", "use", or bare "this"; no sentence restates another.


# Report

Write the document so the advisor gets the verdict, the setting, and the limits in one scan. The layout is the bottom line, then six slots, in order; inside a slot, bold-lead blocks or a table, never a paragraph. The communication rules in `documents/writing/style.md` (conclusion first, descriptive bold leads, advisor's sentence rules) and the glossary at `documents/glossary.md` apply throughout. Form fixed with the user on 2026-10-21 (version B of `results/legal128w/v7_2/main/v8_6-report-B.md`).

## Procedure

1. Read the plan for the version (`<version>/plan.md`) and note the claim, the predictions, and each refutation condition as written before the run.
2. Read the config and the evaluation code that produced each metric. Record models, direction, seed count, prompt count, and the exact calculation. Never infer a metric's meaning from its name.
3. Draft the bottom line and the six slots. Fill Result with a table of no more than eight rows, then one bold-lead block per prediction and one per reading.
4. Check every project term against `documents/glossary.md` and define each at first use.
5. Run the checklist below. Fix, then send.
6. Append one Provenance line: config path, run directory, job IDs, date.

## Layout

- **Bottom line** (bold, before the first header): two to four sentences: the effect with its number, the second effect if any, which predictions hold and which are refuted, the seed count.
- **Question** (header): one sentence, the thing the run was meant to decide.
- **Setting** (header): bold-lead bullets, in this order: Path (A layer -> adapter -> hub -> projector -> frozen decoder, free-run or teacher-forced); Loss (terms, weights, tau, ridge, updates); One difference (the single factor that varies between compared paths); References (each control or reference cell, named and defined); Read (metric, prompt count, decoder count, decodings per cell, seed count); Gates (controls that qualify the hub or corpus, with numbers).
- **Prediction** (header): a table with one row per prediction: label, rule with its numbers, refuted-if.
- **Result** (header): the table (no more than eight rows, both sides of every comparison, the interval when one exists); then one bold-lead block per prediction ("P2 refuted by 0.003." plus the number); then one block per reading of the curve; the last block is "Asserts but does not show."
- **Not settled** (header): bullets, one limit each: seeds, corpora, models, layers, fixed knobs, missing controls, untested ranges.
- **Next step** (header): the one run or decision that follows, with job IDs when queued.
- **Provenance**: one line.

## Checklist

Sentence rules, block rules, and the check before sending are in `documents/writing/style.md`; a report is the one output that carries headers. Report-specific items:

- The bottom line alone gives the verdict and the numbers; the bold leads alone give the argument.
- Each slot is present, in order, and each is scannable on its own; no slot holds a paragraph.
- Every number is labeled result, control, threshold, or sanity check, and carries its source.
- Every prediction appears twice: in the Prediction table and as a Result block with holds or refuted and the margin.
- Numbers are rounded to what the seed and prompt counts support.
- A low, a medium, and a high scoring example appear when the metric is text overlap and the report is the first on its corpus.
- The last Result block names what the claim asserts but does not show.
- One Provenance line closes the document.

## Worked example

Source: `results/legal128w/v7_2/main/v8_6-report-B.md` (V8.6 on legal128w, seed 1).

**Bottom line.** A blind batch of 8192 beats 2048 by +0.02 to +0.05 word-F1 at budgets 1 to 10 and by nothing from 30 up. The hybrid beats the supervised-only fit at budgets 1 to 10 and loses to it at 30 and 100. Two of four predictions hold (P1, P4); P2 and P3 are refuted. Seed 1.

## Question
Does blind batch 8192 add word-F1 over 2048 on legal128w at budgets 1 to 100, and does the hybrid add over supervised only at budget 10?

## Setting
- **Path.** Pythia layer d3 -> affine source adapter -> legal128w hub -> decoder projector -> frozen decoder (Qwen, OLMo, SmolLM), free-run over the 128-token window.
- **Loss.** Supervision fraction 0.95 on the ridge residual term plus 0.05 on the blind squared-distance ABC loss; tau 0.1297 (2 x hub gap, step 0); ridge lambda 1; 3000 updates.
- **One difference.** Blind batch 2048 or 8192 rows per update.
- **References.** Supervised only = same adapter, paired term alone (alpha 1). Blind alone = batch alone, no anchor (alpha 0). Wrong memory = same checkpoint, another prompt's memory (control).
- **Read.** Macro word-F1, 500 development windows x 3 decoders = 1,500 decodings per cell. One seed.
- **Gates (controls).** G1 hub inversion 0.977 vs shuffled 0.152; G2 true hub code 0.982.

## Prediction
| | Rule | Refuted if |
|---|---|---|
| P1 | blind alone F1 < 0.15 and < +0.05 over wrong memory | either bound crossed |
| P2 | D_10 = 8192 minus 2048 at budget 10 in [0, 0.03) | mean outside |
| P3 | E_10 = 8192 hybrid minus supervised only at budget 10 >= +0.05 | mean below |
| P4 | D_100 <= D_10 + 0.01 | above |

## Result
| Budget | 2048 | 8192 | D_b (8192 - 2048) | Supervised only |
|---:|---:|---:|---:|---:|
| 1 | 0.155 | 0.176 | +0.021 | 0.087 |
| 10 | 0.489 | 0.523 | +0.033 (0.027 to 0.041) | 0.487 |
| 100 | 0.763 | 0.765 | +0.002 | 0.813 |

- **P1 holds.** Blind alone 0.033 (2048) and 0.029 (8192); +0.002 and +0.007 over wrong memory.
- **P2 refuted by 0.003.** D_10 = +0.033, lower bound 0.027.
- **P3 refuted.** E_10 = +0.036, below +0.05.
- **P4 holds.** D_100 = +0.002 against the bound 0.043.
- **Two regimes.** Below budget 30 the larger batch and the blind term both help; from 30 the supervised-only fit leads by 0.05 to 0.06.
- **Asserts but does not show.** Larger batch helps at small budgets (seed 1); a fixed +0.05 blind gain at budget 10 is not supported.

## Not settled
- One seed: the interval bounds decoding resampling, not seed spread.
- One corpus, one unseen model, one layer, one tau rule, ridge fixed at 1.

## Next step
Read legal256w (jobs 1433625, 1433626) against the same four rules.

Provenance: `configs/v8_6_legal128w_s1.yaml`; `results/legal128w/v7_2/main/mixed-v8_6-s1.json`; jobs 1432744, 1432745, 1433734; drafted 2026-10-21.

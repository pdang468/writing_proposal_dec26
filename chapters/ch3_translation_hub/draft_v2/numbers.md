# Chapter 3 numbers: inventory, unified protocol, missing runs

Written 2026-11-06. Every number below is the one the draft cites today, with its prompt set. The goal: one protocol per gate, every corpus on the same prompts, every control run.

## 1. What the draft reports now

| Corpus | G1 cross mean | shuffled | prompts (G1) | G2 | wrong memory | prompts (G2) | per-direction table | seeds |
|---|---|---|---|---|---|---|---|---|
| Corpus A | 0.945 | 0.120 | 5,000 val | 0.946 | 0.121 | 500 dev | yes | 1 |
| legal128w | 0.977 | 0.152 | 5,000 val | 0.982 | missing | 500 dev | yes | 1 |
| legal256w | 0.971 | 0.185 (max, not mean) | 5,000 val | 0.977 | missing | 500 dev | no | 1 |
| legal10s | 0.971 | 0.044 | 5,000 val | 0.976 | missing | 500 dev | no | 1 |

Sources as in the `% src:` comments of `ch3_hub_draft.tex`.

## 2. Inconsistencies to remove

1. **Two prompt sets.** G1 on 5,000 validation prompts; G2 on 500 development prompts. Chapter 4 reads every unseen-model result on the 500 development prompts, so 500 is the set every later number is compared to. The 5,000-prompt G1 is also the checkpoint-selection set, so it is not held out.
2. **G1 statistic differs by corpus.** legal256w reports the shuffled control as the max over six directions; the others report the mean.
3. **Wrong-memory control exists for Corpus A only.** G2 is read against wrong memory, so three of four ceilings have no control.
4. **Per-direction table covers two of four corpora.**
5. **Precision.** legal10s was 0.9705 / 0.9756; now rounded to three decimals like the rest.
6. **One seed everywhere.** No interval on any gap; the chapter claims only the mean, which is honest, but a second and third hub seed on Corpus A would let the Qwen-decoder miss (0.874, 0.881 against 0.90) be called real or noise.

## 3. Unified protocol (proposal)

- **G1** (hub translation): free-run word-F1, six cross directions, on the **500 development prompts** of the corpus, with the shuffled-memory control on the same prompts, reported as the mean over directions. Keep the 5,000-prompt figure only in the methods paragraph on selection, labeled "selection, not held out".
- **G2** (ceiling): OLMo true hub output through the three decoders, **500 development prompts**, with the wrong-memory control on the same prompts.
- **Per-direction table**: all nine directions, all four corpora, 500 development prompts, word-F1 and exact match.
- **Seeds**: one hub seed per corpus stays the rule for the proposal; three seeds on Corpus A only, for the Qwen miss.
- **Control statistic**: mean over directions, max given in a comment.

One run script per corpus should emit all of the above from one checkpoint, so the table and the text never drift again.

## 4. Jobs to schedule (alignment repo)

| # | Job | Output fills |
|---|---|---|
| 1 | Corpus A: G1 + shuffled + nine directions on the 500 dev prompts | G1 row re-based to 500; table |
| 2 | legal128w: G1 + shuffled + nine directions + wrong memory, 500 dev | G1 re-based; wrong-memory cell; table |
| 3 | legal256w: same as 2 | G1 (mean control); wrong-memory cell; table rows |
| 4 | legal10s: same as 2 | G1; wrong-memory cell; table rows |
| 5 | Corpus A hub, seeds 2 and 3: G1 nine directions, 500 dev | interval on the Qwen-decoder miss |
| 6 | (optional) legal128w hub reused on legal10s: nine directions, 500 dev | the 0.773 claim with its control |

Each job is one free-run decode pass over 500 prompts × 9 directions plus two control passes; small. Validate job 2 interactively on 50 prompts before submitting the set.

Numbers still open after the jobs: V1/V2 parity (no inversion-scale measurement exists; keep as a stated limit), test-split read (sealed; state when it will be read).

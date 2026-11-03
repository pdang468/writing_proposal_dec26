# Glossary

Terms fixed with the advisor on 2026-09-02. Every document defines a term in these words at first use, or replaces it with the description. "Latent space" never names raw activations. "Free-run" only when the decoder's outputs feed back as its inputs.
"Oracle" is a banned coined term; describe the fit instead (a fit on the full unbudgeted calibration pool).

- Hidden state: the vector a language model produces at one token position in one layer.
- State sequence: the hidden states of one prompt, one per token, in order.
- Hub: the shared space into which every model's hidden states are mapped, so that a state from any model can be decoded by any other. Trained on three white-box models (Qwen, OLMo, SmolLM).
- Hub output: the vector a hidden state becomes after mapping into the hub.
- Source adapter: the trained map from one model's hidden states into the hub.
- Projector: the map from the hub into one decoder's input space.
- Decoder: the frozen language model that turns projected hub outputs back into text.
- Direction: one source model paired with one decoder model, for example Qwen layer 12 -> hub -> OLMo decoder. Nine directions cover three models including self.
- H3: the hub trained on all nine directions (V6.2). Variant A maps each token alone; variant B adds a two-layer transformer per source adapter so a code sees its neighbors. Prefer-B means variant B scored higher.
- Continuation: predicting the next token from a state sequence.
- Inversion: recovering the tokens that produced the states. V6.3 retargeted the hub to inversion.
- Anchor: a correspondence linking an unseen model's hidden-state sequence to its original text or a known model's hidden-state sequence for that same text. Anchors provide the calibration signal for attaching the unseen model to the hub. Supervised anchors have supplied correspondences; inferred anchors are discovered through blind matching and may be incorrect.
- Pseudo-anchor: an inferred anchor whose text is the decoder's own output for the unseen model's hidden-state sequence (V7.3). Pairing rule matched_text keeps only spans where that output equals the true text (reads the true text); rule position pairs row i with hub output i (reads nothing).
- Paired sequence: one canonical text processed by both the unseen model and the hub source model, so that their token groups can be aligned by character span. One paired sequence is one unit of calibration budget.
- Budget: the number of paired sequences allowed for attaching an unseen model.
- Knee: the smallest budget whose mean word-F1 gain above the length-matched floor reaches 95 percent of the gain at the largest budget.
- Gap closed: the fraction of the distance from the no-memory baseline to a fit on the full unbudgeted calibration pool (which influences no budgeted fit) that a condition recovers.
- Word-F1: overlap between decoded and true prompt words, as the harmonic mean of precision and recall, averaged over prompts.
- Exact match: the fraction of prompts decoded verbatim.
- Acc@1: the fraction of positions where the top predicted token is the true one under teacher forcing.
- Teacher-forced: the decoder receives the true previous tokens. Free-run: it receives its own previous outputs.
- Supervision fraction (alpha): the weight of the paired InfoNCE term in the V7.4 loss, (1 - alpha) times the blind ABC loss plus alpha times the paired term; 0 is blind ABC, 1 is a fully supervised contrastive fit of the same adapter.
- ABC loss: the V7 blind objective on unpaired batches. Each mapped source vector is soft-matched to the hub batch, and the matched average must identify its own source vector again (cross-entropy at temperature tau, both directions averaged). It reads no anchor.
- Moment penalty: the squared distance of the batch mean of the map's raw outputs to the hub mean, over the hub radius squared, plus the squared relative error of the output radius. It reads two summary statistics of the hub and no hub vector.
- Blind bracket: the part of the V7.4 loss that reads no anchor, the ABC loss plus eta times the moment penalty. Its weight is 1 minus the supervision fraction.
- Squared-distance score: the negative squared distance between a mapped vector and a hub output, over the hub radius squared; the similarity the ABC loss uses in V7.8 in place of the cosine of length-1 vectors.
- Ridge penalty: lambda over the hub radius squared, times the squared Frobenius norm of the map's effective weight; lambda is 1. In V7.8 it is added to the supervised residual and carries the supervision fraction's weight.
- Budget-independent cell: a V7.8 cell with no residual weight (supervision fraction 0), trained once and read against every budget.
- Version (V3, V6.3, V6.4; from 2026-10-26 w43, w44a, w44b): one experiment generation, named by generation number through V8.7 and by ISO week since (w<NN>, plus a letter when a week holds several); code names in configs and result files (oct_w4, oct_w5, oct_w5b) are given once at first use. Each has a plan in `<version>/plan.md` or `documents/`, a config in `configs/`, a runner `<version>_run.py`, and reports under `results/<version>/<run>/report.md`.
- Whole pool: the blind batch that is the entire training pool of both sides (V8.5): every unseen-model row scored against every hub row under the prompt-uniform row weights, written Bpool in cell names.
- Window corpus (legal128w, legal256w): the legal corpus cut at one contiguous window per document whose start word is drawn uniformly over the document (V8.3), against the opening corpora legal128 and legal256 cut at the first word.

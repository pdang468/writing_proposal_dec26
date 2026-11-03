# Writing guide for the dissertation

Scope: the proposal and dissertation prose, and any paper drawn from them. Chat replies and advisor reports keep `style.md` and `report-form.md`. Models: Kieran Murphy's papers and Kenneth Stanley's 2011 novelty-search paper. Sources: Gopen and Swan (reader expectations), Stanley's writing tips, Mensh and Kording (paragraph and results structure), Zinsser (simplicity), Hunt (process).

Each rule below has the rule, the reason, one example from the chapters, and the check that finds a violation. The checklist at the end is the whole guide in one page.

## 0. Order of work

1. Draft to find the argument. Pages every day; no rereading of notes to start; no sentence rules yet (Hunt).
2. Fix the paragraphs: each one has a thesis sentence, a setting, a number against its comparator, a reclaim, and a link to the next (Section 2).
3. Fix the sentences: subject meets verb, one point, old before new (Section 1).
4. Strip: "we", "use", bare "this", intensifiers, filler (Section 5).
5. Check against the models: would Murphy let the quantity act here; would Stanley state the thesis before the support.

A sentence rule applied to a first-day page breaks step 1. A paragraph rule applied before the argument exists produces well-shaped paragraphs about nothing.

## 1. Sentences

**1.1 The subject is the method, the argument, or the quantity.** Never the authors.
Reason: the reader's attention goes to the topic position (Gopen and Swan 3). An author there steals it from the thing under study.
Example: "We fit an affine map on the paired rows" becomes "An affine map, fitted on the paired rows, sends Pythia's states into the hub."
Check: grep "we", "our", "us". Zero.

**1.2 Subject meets verb at once.** Nothing between them but one short modifier.
Reason: the reader holds the subject in memory until the verb arrives; everything in between is read as unimportant (Gopen and Swan 1).
Example: "The map, fitted on paired sequences aligned by character span into token groups, reaches 0.35" becomes "Fitted on paired sequences, the map reaches 0.35."
Check: more than four words between subject and verb.

**1.3 The verb names the action.** Never "use"; never "is" where a verb exists; never a nominalization where the verb would do.
Reason: Gopen and Swan 5. "Use" can stand for any verb, so it says nothing.
Example: "The hub is used to invert the states" becomes "The hub decoders invert the states." "The allocation of information to features" becomes "the method allocates information to features."
Check: grep "use", "used", "using", "utilize"; grep "-tion of".

**1.4 One point per sentence.** The new point sits at the end, in the stress position.
Reason: the reader emphasizes what the sentence ends on (Gopen and Swan 2). Two points compete and both lose.
Example: "The gain is largest at low budgets and shrinks by 300 prompts, and four ingredients each contribute" becomes two sentences: "The gain is largest at low budgets and is gone by 300 prompts. Four ingredients each contribute to it."
Check: more than one "and" joining clauses; a sentence that ends on a parenthesis or a citation instead of its point.

**1.5 Old before new.** The sentence opens with a term the previous sentence left the reader holding.
Reason: Gopen and Swan 4 and 6; the link is what makes a paragraph one argument instead of a list.
Example: "...sends Pythia's states into the hub. The hub's frozen decoders then regenerate the prompt." Not: "...into the hub. Free-run decoding by three frozen models regenerates the prompt."
Check: read only the first three words of each sentence in a paragraph; they should name things the paragraph has already introduced, except the first.

**1.6 Length is controlled by structure, not by count.** A sentence that passes 1.2, 1.4 and has at most one subordinate clause is short enough at any length. Parallel sentences may run long: the items share grammar and order, at most four of them.
Reason: Zinsser's "strip every sentence to its cleanest components" is about clutter, not word count; Mensh and Kording rule 4 asks for parallel wording for parallel ideas, which costs the reader one pattern.
Example of earned length: "The two-layer adapter loses 0.12; the normalized projector loses 0.15; the stronger decoder loses 0.27."
Check: mark every sentence over about 35 words; keep the ones that fail none of 1.2, 1.4, and the one-clause limit. Vary rhythm: a long sentence, then a short one that carries the point.

**1.7 "This" always carries a noun.** "This gap", "this run", never "This means".
Reason: a bare "this" can point at anything in the previous sentence; the reader guesses.
Check: grep "This " at sentence start and "this " before a verb.

## 2. Paragraphs

**2.1 Shape: thesis, setting, number against comparator, reclaim, link.** The first sentence states the claim. The middle gives the setting and the evidence. The last sentence restates the claim in the evidence's terms and hands off to the next paragraph.
Reason: Stanley's paragraphs; Mensh and Kording rule 3 (context, content, conclusion). A reader who stops after one sentence has the point.
Example (Chapter 4, leak shape): "Spreading ninety leaked rows over ninety prompts beats one whole leaked prompt by a factor of two. [setting: legal128w, V8.7 settings, seed 1, 4,500 confirmation prompts] The scattered leak gives the hybrid 0.326 against 0.161 for the whole prompt of 78 rows; the supervised fit shows the same order at 0.106 against 0.087. Coverage of prompts, not count of rows, is what a leak buys. The next question is whether the words in those rows matter."
Check: cover everything but the first sentence; the paragraph's claim should still be readable.

**2.2 Exception: a chapter's first paragraph may open with setup and land the claim at its end.** It has no previous paragraph to link to, and the setup is the old information the chapter needs.
Reason: Murphy's openers; Gopen and Swan 6.
Check: only one such paragraph per chapter.

**2.3 One paragraph, one claim.** A second claim is a second paragraph.
Check: write the claim in the margin; if it takes "and", split.

**2.4 Transitions name the logic.** "So", "therefore", "yet", "by contrast", "the next question is". Never "additionally", "moreover", "furthermore".
Reason: the reader needs the relation, not a signal that another sentence follows.

## 3. Results

**3.1 Default order: question or prediction, number against its comparator, verdict, reading.**
1. Open with the question the paragraph answers or the prediction the plan wrote: "P2 predicted that mid-frequency leaks gain at least 0.03."
2. One sentence holds the number and what it is measured against, with the sample: "Mid-frequency leaks score 0.252 against 0.326 for random leaks, on 4,500 confirmation prompts."
3. The verdict in its own short sentence: "P2 is contradicted."
4. The reading last, one sentence, linked forward: "Which words leak matters less than how many prompts the leak touches."
Reason: Mensh and Kording rule 7 (question first, answer last); Gopen and Swan (a number without its comparator has no meaning yet; the meaning belongs in the next stress position); Stanley's result sentences.

**3.2 Choice point.** When the result is confirmatory, open with the prediction. When it is surprising, or is the chapter's main number, open with the number: the surprise is the thesis sentence. Either way the comparator stays in the same sentence as the number.

**3.3 Never a bare number.** Every number carries its comparator (control, baseline, ceiling, or the carried setting), its sample (seeds, prompts), and, when a gap is claimed, its interval or test.
Example: "0.657 [0.651, 0.661] against 0.348, three seeds, 500 development prompts."

**3.4 Tables carry comparisons; prose carries the point.** Any comparison across more than two cells goes in a table with both sides, the metric, and n. The paragraph quotes the one or two numbers that carry its claim and names the table for the rest.

**3.5 Figures state their conclusion in the caption's first sentence**; the method goes in the second (Mensh and Kording).

**3.6 Label every number.** Result, control, threshold, selection, or sanity check, as in the reports; a selection is never reported as a result.

## 4. Claims and hedging

**4.1 The number is never hedged.** No "about", "roughly", "seems to", "suggests that" on a measured value.
Reason: the value is what the run gave; a hedge adds doubt the data do not carry.

**4.2 The generality is always bounded, once, beside the claim.** Corpus, seeds, model, split. The bound is a fact, not a hedge word.
Example: "Matching raises word-F1 at budgets 10 to 100 on Corpus A over three seeds; on legal128w the gain is measured at one seed." Not: "Matching helps when pairs are scarce."

**4.3 "May" and "can" are for mechanisms not yet tested**, at most one such sentence per paragraph: "the matching term may correct the map where the pairs leave it free."

**4.4 A claim's reach equals its evidence.** "Blind matching cannot read hidden states" becomes "Four blind losses stayed at the wrong-memory control on one block of two models."

**4.5 Close a result with what it asserts but does not show.** One sentence, at the end of the section, not scattered through it.

## 5. Words

- Forbidden: "we", "our", "use" in any form, bare "this", "in order to", "actually", "essentially", "seems that", "very", "highly", "significantly" (unless a test is named), "remarkably", "dramatically", "interestingly", "note that", "it is worth noting".
- Project terms come from `glossary.md`, defined once at first use in the glossary's words, then repeated bare. No synonyms for a defined term; no coined names for methods.
- A new concept gets a short noun phrase at first use, in apposition: "an anchor, a correspondence linking an unseen model's state sequence to its text".
- Plain vocabulary. The simplest word that is exact. Standard terms stay standard (information bottleneck, mutual information).
- Verbs that carry action in this project: map, send, attach, decode, regenerate, recover, leak, align, match, anchor, read, compress, allocate. Not: handle, involve, leverage, serve as, represent, perform.
- "That" restricts; "which" after a comma adds. No em dashes; a colon or semicolon opens a second stress position.
- Math symbols in prose are fine; a displayed equation carries any expression longer than one term.

## 6. The chapter

- The first paragraph states what the chapter shows and in what order (one paragraph, Murphy's shape allowed).
- Each section opens with its claim.
- Every hypothesis is written before its evidence with the number that would refute it (the project's own rule).
- The last section of a results chapter says what the evidence shows, then what it does not show, then what comes next, in that order.

## Checklist (one page)

Before a section leaves your hands:

- [ ] grep: "we", "our", "use", "using", "utilize", bare "this", "in order to", intensifiers. Zero hits.
- [ ] First three words of every sentence name something already introduced (except paragraph openers).
- [ ] Every sentence: subject meets verb within four words; one point; the point at the end.
- [ ] Every sentence over 35 words passes 1.2, 1.4, and the one-clause limit, or is a parallel list of at most four items.
- [ ] Every paragraph: first sentence is the claim; last sentence restates it and links forward; cover the body and the claim survives.
- [ ] Every number: comparator in the same sentence; seeds and prompt count; interval or test when a gap is claimed; label (result, control, threshold, selection).
- [ ] Every result paragraph: question or prediction, number against comparator, verdict, reading.
- [ ] Every claim: generality bounded once beside it; no hedge on a number; at most one "may" per paragraph.
- [ ] Every table: both sides, metric, n. Every figure caption: conclusion first, method second.
- [ ] Every term: glossary wording at first use, bare afterward.
- [ ] The section ends with what it asserts but does not show.

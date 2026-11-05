# writing/

Writing principles for scientific prose, with the reason for each. This folder is the single source of truth; other projects load it, they do not copy it.

| File | Read when |
| --- | --- |
| `principles.md` | Writing or editing. Rule, reason, example; how an assistant works with the author; when to break a rule. |
| `checklist.md` | Last pass before a section leaves your hands. |
| `sources/` | Reference: Gopen and Swan digest, Hunt digest, Stanley's tips verbatim, the Murphy/Stanley/Ha style study. |

## Loading

This repo: `CLAUDE.md` at the root imports `writing/principles.md`.

Another repo on the same machine (e.g. `alignment`), in its `CLAUDE.md`:
```
@~/writing_proposal_dec26/writing/principles.md
```

claude.ai Project or ChatGPT: paste `principles.md` as one document; replace it when this file changes.

Chat replies and advisor reports follow `alignment/documents/writing/style.md` and `report-form.md`, not this file.

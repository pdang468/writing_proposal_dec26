# Dissertation proposal, December 2026

NJIT thesis template, restructured. Mirror of the Overleaf project
`PhuocDang_ProposalDissertation_Dec26`.

| Path | Holds |
|---|---|
| `main.tex` | Driver: preamble inputs, front matter, `\include` of each chapter |
| `preamble/` | `packages.tex` (packages, captions), `macros.tex` (math macros) |
| `frontmatter/` | Abstract, approval, biography, dedication, acknowledgment, symbols, abbreviations |
| `chapters/chN_name/` | One folder per chapter: `chN.tex` holds `\chapter` and `\input`s its sections `sK_name.tex` |
| `figures/chN/` | Figures per chapter; call as `\includegraphics{chN/name}` |
| `bib/library.bib` | References |
| `thesis.cls`, `mcode.sty` | NJIT class (title page now reads `\major` and `\department`) |

Fast compiles: uncomment `\includeonly{...}` in `main.tex`.

---
name: nossaifd
description: Use when you write or change Markdown that a person reads, for example a README, a spec, a plan, a report, a skill or other documentation. It gives the plain English writing rules of the nossaifd guide and a checker for the rules that a program can measure.
license: MIT, copyright (c) 2026 Rahul Dave. The full text is in the LICENSE file of https://github.com/rahuldave/nossaifd
---

# nossaifd

nossaifd is a writing guide for prose that an AI model writes and a person
reads. Its rules come from four sources:

- Simplified Technical English, ASD-STE100.
- The plain-writing skill by Shreya Shankar.
- "Communicating Your Work", a tutorial by Rosalind Reid on written reports and
  talks. It gives the order of a long document, several rules for sentences,
  and the rules for figures. Rosalind Reid lets this project use her work on
  one condition. Each place that uses it credits her. Text that comes from
  her work must keep its credit to Rosalind Reid, in every copy and in every
  changed version of this skill. Her PDFs are not under the MIT licence.
- "Five Principles for Generating Readable AI Text in Bulk", a post by Shreya
  Shankar. It gives the rules for short items that a person skims.

The rules make the text short, literal and easy to read for a reader who is not
a native speaker. Each rule in the guide names its source.

## Steps

1. Read `references/GUIDE.md` before you write. Follow its rules for words,
   sentences, instructions, paragraphs, long documents, figures, tone,
   punctuation and short items. A short item is a title, a notification or
   a row that a person skims.
2. Use one term for one thing. If the project has a glossary, use its terms. If
   not, define each technical term the first time that it appears on a page.
3. Write the page.
4. Run the checker on the page, and fix each hard problem:

   ```bash
   uv run --no-project python .agents/skills/nossaifd/scripts/check.py page.md
   ```

5. Run the checker with `-v` to see the soft notes. Fix each note that makes
   the page harder to read.
6. Read the page yourself. The checker cannot judge meaning, tone or a missing
   definition.

The checker skips front matter, code, tables, link targets and quoted words.
It needs only Python 3.11 or later, which `uv run` provides.

## Files in this skill

- **`references/GUIDE.md`** has the rules.
- **`scripts/check.py`** checks a page against the rules that a program can
  measure. It exits with 1 when it finds a hard problem.

The source of both files is https://github.com/rahuldave/nossaifd.

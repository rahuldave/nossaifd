---
name: nossaifd
description: Use when you write or change Markdown that a person reads, for example a README, a spec, a plan, a report, a skill or other documentation. It gives the plain English writing rules of the nossaifd guide and a checker for the rules that a program can measure.
license: MIT, copyright (c) 2026 Rahul Dave. The full text is in the LICENSE file of https://github.com/rahuldave/nossaifd
---

# nossaifd

nossaifd is a writing guide for prose that an AI model writes and a person
reads. Its rules come from Simplified Technical English and from a skill for
plain writing. They make the text short, literal and easy to read for a reader
who is not a native speaker.

## Steps

1. Read `references/GUIDE.md` before you write. Follow its rules for words,
   sentences, instructions, paragraphs, tone and punctuation.
2. Use one term for one thing. If the project has a glossary, use its terms. If
   not, define each technical term the first time that it appears on a page.
3. Write the page.
4. Run the checker on the page, and fix each hard problem:

   ```bash
   python3 .agents/skills/nossaifd/scripts/check.py page.md
   ```

5. Run the checker with `-v` to see the soft notes. Fix each note that makes
   the page harder to read.
6. Read the page yourself. The checker cannot judge meaning, tone or a missing
   definition.

The checker skips front matter, code, tables, link targets and quoted words.
It needs only Python 3.11 or later.

## Files in this skill

- **`references/GUIDE.md`** has the rules.
- **`scripts/check.py`** checks a page against the rules that a program can
  measure. It exits with 1 when it finds a hard problem.

The source of both files is https://github.com/rahuldave/nossaifd.

# nossaifd

**Not so shitty AI first drafts.** A writing guide, and a checker, for documentation and other prose that
an AI model writes and a person reads.

The name comes from "Shitty First Drafts", the essay in Anne Lamott's *Bird by Bird*. Lamott says that
every good piece of writing starts as a bad first draft. An AI model writes first drafts fast, and they
have their own bad habits. The guide gives the model rules that remove those habits before a person reads
the draft.

## What is here

| File | What it is |
|---|---|
| `GUIDE.md` | The writing rules: words, sentences, instructions, paragraphs, tone, punctuation and formatting |
| `check.py` | A program that checks Markdown against the rules that a program can measure |

## How to use it

1. Give `GUIDE.md` to the model with the writing task.
2. Give the model a glossary of the project's terms, so that it uses one term for one thing.
3. Run the checker on the result, and fix each hard problem:

   ```
   python3 check.py docs/*.md
   python3 check.py -v docs/page.md
   ```

4. Read the result. The checker cannot judge meaning or tone.

The checker needs only Python 3.11 or later, with no other packages.

## Where the rules come from

The guide joins two sources. ASD-STE100, Simplified Technical English, gives the rules for words,
sentences, instructions and paragraphs. The plain-writing skill from docwriter-org gives the rules for
tone, punctuation and the patterns of AI writing. `GUIDE.md` lists the sources and the changes.

## Licence

MIT: see `LICENSE`.

# nossaifd

**Not so shitty AI first drafts.** A writing guide, and a checker, for documentation and other prose that
an AI model writes and a person reads.

The site is at https://rahuldave.com/nossaifd/.

The name comes from ["Shitty First Drafts"](https://wrd.as.uky.edu/sites/default/files/1-Shitty%20First%20Drafts.pdf),
the essay in Anne Lamott's *Bird by Bird*. Lamott says that
every good piece of writing starts as a bad first draft. An AI model writes first drafts fast, and they
have their own bad habits. The guide gives the model rules that remove those habits before a person reads
the draft.

## What is here

| File | What it is |
|---|---|
| [`GUIDE.md`](GUIDE.md) | The writing rules: words, sentences, instructions, paragraphs, tone, punctuation and formatting |
| [`check.py`](check.py) | A program that checks Markdown against the rules that a program can measure. See [the checker](docs/checker.md) |
| `docs/` | The site: `build.py` builds it from this README, `GUIDE.md` and `docs/checker.md` |
| `.agents/skills/nossaifd/` | The agent skill, with copies of the guide and the checker |

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

## Install the skill in a repository

The repository is also an agent skill package. The skill
`.agents/skills/nossaifd/` holds copies of `GUIDE.md` and `check.py`, and a
`SKILL.md` that tells an agent how to use them.

The usual way to install it is the stack installer of jnterfaces, which asks
about nossaifd with the answer yes as the default. To install only this skill,
run its own installer from a clone:

```
scripts/install.sh ../my-project --dry-run
scripts/install.sh ../my-project
```

The installer records the source revision in `.agents/nossaifd-install.json`
in the target. It never overwrites a file that you edited after an install.

After you change `GUIDE.md` or `check.py`, run `just sync` to copy them into
the skill. `just check` fails while the copies differ.

## Where the rules come from

The guide joins two sources, and `GUIDE.md` lists the changes it makes to them.

- **ASD-STE100, Simplified Technical English.** Aircraft makers write their maintenance manuals in it.
  Andrej Karpathy suggested on X that the same rules suit text that AI models write. It gives the rules
  for words, sentences, instructions and paragraphs.
- **The plain-writing skill by Shreya Shankar**, at
  https://github.com/docwriter-org/plain-writing-skill, under the MIT licence. It gives the rules for
  tone, punctuation and the patterns of AI writing.

## Licence

MIT: see `LICENSE`.

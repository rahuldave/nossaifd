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
   uv run --no-project python check.py docs/*.md
   uv run --no-project python check.py -v docs/page.md
   ```

4. Read the result. The checker cannot judge meaning or tone.

The checker needs only Python 3.11 or later, with no other packages. `uv run`
provides that Python, so the machine needs only `uv`.

## Install the skill in a repository

The repository is also an agent skill package. The skill
`.agents/skills/nossaifd/` holds copies of `GUIDE.md` and `check.py`, and a
`SKILL.md` that tells an agent how to use them.

jnterfaces installs it, in the role `prose`. In a project with jnterfaces, run
this command:

```
just install prose
```

The installer of jnterfaces clones this repository, copies the skill and
records the source revision in `.agents/nossaifd-install.json`. It never
overwrites a file that you edited after an install. `just uninstall prose`
takes the skill out again. This repository has no installer of its own.

The role also brings the recipe `just prose`, from
`.agents/just/roles/nossaifd.just`. Alone, it checks every Markdown file that
git tracks, outside `.agents`, `.claude` and `.codex`. It leaves out
`AGENTS.md` and `CLAUDE.md`, which are instructions for agents. With names, it
checks those pages, also `AGENTS.md`. `-v` also shows the soft notes. A project that jnterfaces did not
start adds the recipe with the line `import? '.agents/just/roles/nossaifd.just'`
in its Justfile.

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

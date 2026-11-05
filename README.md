# nossaifd

**Not so shitty AI first drafts.** A writing guide and a checker for text that an AI model writes and a
person reads, such as documentation, READMEs, reports and notes. The guide is [`GUIDE.md`](GUIDE.md), and
the checker is [`check.py`](https://github.com/rahuldave/nossaifd/blob/main/check.py).

The site is at https://rahuldave.com/nossaifd/.

Much of the advice comes from "Communicating Your Work", a tutorial by Rosalind Reid. She taught it at
Harvard in 2015, and she was the editor of *American Scientist* magazine from 1992 to 2008. Each rule that
uses her work names her and gives the page. See [Sources and credit](docs/sources.md).

The name comes from ["Shitty First Drafts"](https://wrd.as.uky.edu/sites/default/files/1-Shitty%20First%20Drafts.pdf),
the essay in Anne Lamott's *Bird by Bird*. Lamott says that every good piece of writing starts as a bad
first draft. An AI model writes first drafts fast, and they have their own bad habits. The guide gives the
model rules that remove those habits before a person reads the draft.

## Talks

A talk makes different demands from a report. A reader can go back and read a sentence again, but a
listener cannot. So the guide for talks and its checker have their own repository,
[nossaifd-talks](https://github.com/rahuldave/nossaifd-talks). Its site is at
https://rahuldave.com/nossaifd-talks/. That guide also draws on the work of Rosalind Reid.

## What is here

| File | What it is |
|---|---|
| [`GUIDE.md`](GUIDE.md) | The rules for reports: words, sentences, instructions, paragraphs, long documents, figures, tone, punctuation, formatting and short items |
| [`check.py`](https://github.com/rahuldave/nossaifd/blob/main/check.py) | It checks a report against the rules that a program can measure. See [the checker](docs/checker.md) |
| [`EXAMPLES.md`](EXAMPLES.md) | Worked examples for the rules, from Rosalind Reid and Shreya Shankar. Each example names its source |
| `sources/reid/` | The PDFs of Rosalind Reid's tutorial, which the guide cites page by page |
| `docs/` | The pages of the site, which smalldocs builds from `_smalldocs.yml` |
| `.agents/skills/nossaifd/` | The agent skill, with copies of `GUIDE.md`, `EXAMPLES.md` and `check.py` |

## How to use it

For a report:

1. Give `GUIDE.md` to the model with the writing task.
2. Give the model a glossary of the project's terms, so that it uses one term for one thing.
3. Run the checker on the result, and fix each hard problem:

   ```
   uv run --no-project python check.py docs/*.md
   uv run --no-project python check.py -v docs/page.md
   ```

4. Read the result. The checker cannot judge meaning or tone.

The checker needs only Python 3.11 or later, with no other packages. `uv run` gives that Python, so the
machine needs only `uv`.

## Install the skill in a repository

The repository is also an agent skill package with one skill, `.agents/skills/nossaifd/`. It holds copies
of the guide, the examples and the checker, and a `SKILL.md` that tells an agent how to use them.

jnterfaces installs the skill in the role `prose`. In a project with jnterfaces, run
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

After you change the guide, the examples or the checker, run `just sync` to
copy them into the skill. `just check` fails while the copies differ.

## Build the site

[smalldocs](https://pypi.org/project/smalldocs/) builds the site from the pages that `_smalldocs.yml`
lists, with the theme Folio in `_extensions/folio/`. The site starts with this README, through `index.qmd`:

```
just site
```

The site goes to `_site/`. `just check` also runs `smalldocs check .`, which finds broken links.

## Where the rules come from

The guide joins four sources. [Sources and credit](docs/sources.md) says what each one gives, and
[Why the rules](docs/why.md) says what the guide chose where the sources disagree.

- **"Communicating Your Work", a tutorial by Rosalind Reid**, for the course AC297r at Harvard in March
  2015. It gives the structure of a report and the rules for figures. Her PDFs are in [`sources/reid/`](https://github.com/rahuldave/nossaifd/tree/main/sources/reid). She gave permission to use them
  on one condition. Every place that uses her work credits her.
- **ASD-STE100, Simplified Technical English.** Aircraft makers write their maintenance manuals in it.
  Andrej Karpathy suggested on X that the same rules suit text that AI models write. It gives the rules
  for words, sentences, instructions and paragraphs.
- **The plain-writing skill by Shreya Shankar**, at
  https://github.com/docwriter-org/plain-writing-skill, under the MIT licence. It gives the rules for
  tone, punctuation and the patterns of AI writing.
- **["Five Principles for Generating Readable AI Text in Bulk"](https://fsdatalab.github.io/blog/agent-text-at-scale/),
  by Shreya Shankar.** It gives the rules for short items that a reader
  skims, such as titles, list items and the rows of a dashboard.

## Licence

The code and the guide are under the MIT licence, in [`LICENSE`](https://github.com/rahuldave/nossaifd/blob/main/LICENSE). Rosalind Reid's PDFs in `sources/reid/`
are her work, used with her permission, and they are not under the MIT licence.

Rosalind Reid lets others use her work on one condition. Every place that uses it credits her. So text in
the guide, the examples and the skill that comes from her work must keep its credit to Rosalind Reid. The condition holds
in every copy and in every changed version, and the MIT licence does not remove it.

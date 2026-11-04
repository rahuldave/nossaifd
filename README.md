# nossaifd

**Not so shitty AI first drafts.** Two writing guides, and a checker for each, for text that an AI model
writes and a person reads or hears:

- **Reports**, which a person reads, such as documentation, READMEs, reports and notes. The guide is
  [`GUIDE.md`](GUIDE.md), and the checker is [`check.py`](check.py).
- **Talks**, which a person hears and sees. A talk has slides and a spoken script. The guide is
  [`TALKS.md`](TALKS.md), and the checker is [`check_talk.py`](check_talk.py).

The site is at https://rahuldave.com/nossaifd/.

Much of the advice comes from "Communicating Your Work", a tutorial by Rosalind Reid. She taught it at
Harvard in 2015, and she was the editor of *American Scientist* magazine from 1992 to 2008. Each rule that
uses her work names her and gives the page. See [Sources and credit](docs/sources.md).

The name comes from ["Shitty First Drafts"](https://wrd.as.uky.edu/sites/default/files/1-Shitty%20First%20Drafts.pdf),
the essay in Anne Lamott's *Bird by Bird*. Lamott says that every good piece of writing starts as a bad
first draft. An AI model writes first drafts fast, and they have their own bad habits. The guides give the
model rules that remove those habits before a person reads the draft.

## Why two guides

A report and a talk make different demands. A reader can go back and read a sentence again. A listener
cannot, so a spoken sentence puts the news first, and a written sentence puts it last. A slide holds a few
words that a person sees for less than a minute. A checker for reports would fail every good slide, so
each kind of text has its own guide and its own checker. The two checkers share only the code that reads
Markdown.

## What is here

| File | What it is |
|---|---|
| [`GUIDE.md`](GUIDE.md) | The rules for reports: words, sentences, instructions, paragraphs, long documents, figures, tone, punctuation, formatting and short items |
| [`check.py`](check.py) | It checks a report against the rules that a program can measure. See [the checker](docs/checker.md) |
| [`TALKS.md`](TALKS.md) | The rules for talks: the story, the audience, slides, figures, the spoken script and delivery |
| [`check_talk.py`](check_talk.py) | It checks a deck and its script against the rules that a program can measure. See [the talk checker](docs/check-talk.md) |
| `sources/reid/` | The PDFs of Rosalind Reid's tutorial, which the guides cite page by page |
| `docs/` | The site. `build.py` builds it from this README, the two guides and the pages in `docs/` |
| `.agents/skills/nossaifd/` | The agent skill for reports, with copies of `GUIDE.md` and `check.py` |
| `.agents/skills/presentations/` | The agent skill for talks, with copies of `TALKS.md`, `check_talk.py` and `check.py` |

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

For a talk, give `TALKS.md` to the model, and run `check_talk.py` on the deck. A deck is one Markdown
file. Lines of `---` split the slides, and the spoken script is in the notes of each slide.
[The talk checker](docs/check-talk.md) gives the format and the options.

```
uv run --no-project python check_talk.py talk.md
```

Each checker needs only Python 3.11 or later, with no other packages. `uv run` provides that Python, so the
machine needs only `uv`.

## Install the skills in a repository

The repository is also an agent skill package with two skills. The skill `.agents/skills/nossaifd/` is for
reports, and the skill `.agents/skills/presentations/` is for talks. Each one holds copies of its guide
and its checker, and a `SKILL.md` that tells an agent how to use them.

jnterfaces installs the skill for reports, in the role `prose`. In a project with jnterfaces, run
this command:

```
just install prose
```

The installer of jnterfaces clones this repository, copies the skill and
records the source revision in `.agents/nossaifd-install.json`. It never
overwrites a file that you edited after an install. `just uninstall prose`
takes the skill out again. This repository has no installer of its own.
jnterfaces does not install the skill for talks yet.

The role also brings the recipe `just prose`, from
`.agents/just/roles/nossaifd.just`. Alone, it checks every Markdown file that
git tracks, outside `.agents`, `.claude` and `.codex`. It leaves out
`AGENTS.md` and `CLAUDE.md`, which are instructions for agents. With names, it
checks those pages, also `AGENTS.md`. `-v` also shows the soft notes. A project that jnterfaces did not
start adds the recipe with the line `import? '.agents/just/roles/nossaifd.just'`
in its Justfile.

After you change a guide or a checker, run `just sync` to copy them into the
skills. `just check` fails while the copies differ.

## Where the rules come from

The guides join five sources. [Sources and credit](docs/sources.md) says what each one gives, and
[Why the rules](docs/why.md) says what the guides chose where the sources disagree.

- **"Communicating Your Work", a tutorial by Rosalind Reid**, for the course AC297r at Harvard in March
  2015. It gives the structure of a report and of a talk, the rules for figures, and much of the advice
  on slides and delivery. Her PDFs are in [`sources/reid/`](https://github.com/rahuldave/nossaifd/tree/main/sources/reid). She gave permission to use them
  on one condition. Every place that uses her work credits her.
- **The Chicago Guide to Communicating Science, by Scott L. Montgomery.** Reid's presentation tips draw
  mostly on it.
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

The code and the guides are under the MIT licence, in `LICENSE`. Rosalind Reid's PDFs in `sources/reid/`
are her work, used with her permission, and they are not under the MIT licence.

Rosalind Reid allows the use of her work on one condition. Every place that uses it credits her. So text in
the guides and the skills that comes from her work must keep its credit to Rosalind Reid. The condition holds
in every copy and in every changed version, and the MIT licence does not remove it.

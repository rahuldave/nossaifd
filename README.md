# nossaifd

**Not so shitty AI first drafts.** A writing guide and a checker for text that an AI model writes and a
person reads, such as documentation, READMEs, reports and notes. The guide is [`GUIDE.md`](GUIDE.md), and
the checker is [`check.py`](https://github.com/rahuldave/nossaifd/blob/main/check.py).

The site is at https://rahuldave.com/nossaifd/.

Much of the advice comes from "Communicating Your Work", a tutorial by Rosalind Reid. She taught it at
Harvard in 2015, and she was the editor of *American Scientist* magazine from 1992 to 2008. Each rule that
uses her work names her and gives the page. See [Sources and credit](docs/sources.md).

## How to use it

For a report:

1. Give `GUIDE.md` to the model with the writing task.
2. Give the model a glossary of the project's terms, so that it uses one term for one thing.
3. Run the checker on the result, and fix each hard problem. A hard problem breaks a limit of the guide,
   such as a sentence of more than 40 words. A soft note is for you to judge:

   ```
   uv run --no-project python check.py docs/*.md
   uv run --no-project python check.py -v docs/page.md
   ```

4. Keep a copy of the result. Then revise it with the declauding skill by Oskar Austegard, in
   `.agents/skills/declauding/`, which finds and rewrites the sentences that sound like a model.
   [The declauding skill](docs/declauding.md) gives the steps. Run the checker again after the revision.
5. Read the result. The checker cannot judge meaning or tone.

The checker needs only Python 3.11 or later, with no other packages. `uv run` gives that Python, so the
machine needs only `uv`.

## What is here

| File | What it is |
|---|---|
| [`GUIDE.md`](GUIDE.md) | The rules for reports: words, sentences, instructions, paragraphs, long documents, figures, tone, punctuation, formatting and short items |
| [`check.py`](https://github.com/rahuldave/nossaifd/blob/main/check.py) | It checks a report against the rules that a program can measure. See [the checker](docs/checker.md) |
| [`EXAMPLES.md`](EXAMPLES.md) | Worked examples for the rules, from Rosalind Reid, Shreya Shankar and the declauding skill by Oskar Austegard. Each example names its source |
| `sources/reid/` | The PDFs of Rosalind Reid's tutorial, which the guide cites page by page |
| `sources/declauding.json` | The commit and the version of the declauding skill by Oskar Austegard that ships here, with the git id of each file of that commit and of each file that the patch changes. `just declauding` writes it |
| `sources/declauding.patch` | The one sentence that the copy of the declauding skill by Oskar Austegard changes. See [the declauding skill](docs/declauding.md#where-it-comes-from) |
| `docs/` | The pages of the site, which smalldocs builds from `_smalldocs.yml` |
| `.agents/skills/nossaifd/` | The agent skill, with copies of `GUIDE.md`, `EXAMPLES.md` and `check.py` |
| `.agents/skills/declauding/` | The declauding skill by Oskar Austegard, with its licence and one changed sentence. See [the declauding skill](docs/declauding.md) |

## Install the skill in a repository

The repository is also a package of two agent skills. The first, `.agents/skills/nossaifd/`, holds
copies of the guide, the examples and the checker, and a `SKILL.md` that tells an agent how to use them.
The second, `.agents/skills/declauding/`, is the declauding skill by Oskar Austegard. The command
`npx skills add rahuldave/nossaifd --skill nossaifd` installs only the first. An agent that has only the
nossaifd skill follows rules 50 to 55 of the guide in place of the declauding skill.

[jnterfaces](https://github.com/rahuldave/jnterfaces) is a package of agent skills for the command
interface of a project. Its installer adds other packages, and each package does one job, which
jnterfaces calls a role. It installs both skills of this package in the role `prose`. In a project that
uses jnterfaces, run this command:

```
just install prose
```

The installer of jnterfaces clones this repository, copies the skills and records the source revision in
`.agents/nossaifd-install.json`. It never overwrites a file that you edited after an install.
`just uninstall prose` takes both skills out again, except a file that you edited. This repository has no installer of its own.

The role also brings the recipe `just prose`, from `.agents/just/roles/nossaifd.just`. Without names of
pages, the recipe checks every Markdown file that git tracks, outside `.agents`, `.claude` and `.codex`.
It leaves out `AGENTS.md` and `CLAUDE.md`, which are instructions for agents. With names of pages, it
checks those pages, also `AGENTS.md` and `CLAUDE.md`. `-v` also shows the soft notes. A project that
jnterfaces did not set up adds the recipe with the line
`import? '.agents/just/roles/nossaifd.just'` in its Justfile.

After you change the guide, the examples or the checker, run `just sync` to copy them into the nossaifd
skill. `just check` fails while the copies differ.

`just declauding` copies the declauding skill by Oskar Austegard again from its fixed commit in
oaustegard/claude-skills, and it applies `sources/declauding.patch`. To take a newer version, change the
commit in the Justfile and run `just declauding`. If the patch no longer applies, the recipe stops before
it changes the copy. Then update or remove the patch, and the names of the changed files and the version
in `tests/test_declauding.py`.

## Build the site

[smalldocs](https://pypi.org/project/smalldocs/) builds the site from the pages that `_smalldocs.yml`
lists, with the theme Folio in `_extensions/folio/`. The first page of the site is this README, which
`index.qmd` includes:

```
just site
```

The site goes to `_site/`. `just check` also runs `smalldocs check .`, which finds broken links.

## Talks

A listener cannot go back and hear a sentence again, but a reader can read it again. So a talk needs
other rules than a report, and the guide for talks and its checker have their own repository,
[nossaifd-talks](https://github.com/rahuldave/nossaifd-talks). Its site is at
https://rahuldave.com/nossaifd-talks/. That guide also uses the work of Rosalind Reid.

## Where the name comes from

The name of the project comes from
["Shitty First Drafts"](https://wrd.as.uky.edu/sites/default/files/1-Shitty%20First%20Drafts.pdf), the
essay in Anne Lamott's *Bird by Bird*. Lamott says that every good piece of writing starts as a bad first
draft. An AI model writes first drafts fast, and they have their own bad habits. The guide gives the
model rules that remove those habits before a person reads the draft.

## Where the rules come from

The guide joins five sources. [Sources and credit](docs/sources.md) says what each one gives, and
[Why the rules](docs/why.md) says what the guide chose where the sources disagree.

- **"Communicating Your Work", a tutorial by Rosalind Reid**, for the course AC297r at Harvard in March
  2015. It gives the structure of a report and the rules for figures. Her PDFs are in
  [`sources/reid/`](https://github.com/rahuldave/nossaifd/tree/main/sources/reid). She gave permission to
  use them on one condition. Every place that uses her work credits her.
- **ASD-STE100, Simplified Technical English.** Aircraft makers write their maintenance manuals in it.
  Andrej Karpathy suggested on X that the same rules suit text that AI models write. It gives the rules
  for words, sentences, instructions and paragraphs. Only its about page was read, so all but one of these
  rules come from memory, and [the list of them](docs/why.md#rules-of-asd-ste100-that-are-not-checked-against-the-standard)
  says which.
- **The plain-writing skill by Shreya Shankar**, at
  https://github.com/docwriter-org/plain-writing-skill, under the MIT licence. It gives the rules for
  tone, punctuation and the patterns of AI writing.
- **["Five Principles for Generating Readable AI Text in Bulk"](https://fsdatalab.github.io/blog/agent-text-at-scale/),
  by Shreya Shankar.** It gives the rules for short items that a reader skims, such as titles, list items
  and the rows of a dashboard.
- **[The declauding skill](https://github.com/oaustegard/claude-skills/tree/6baa7290da972191749acda03c63297e67b3fc26/declauding) by Oskar
  Austegard**, under the MIT licence. It gives the rules for the revision of a draft that reads as if a
  model wrote it. Its register, the file that lists its patterns, gives a pair of sentences, before and
  after, for most of the patterns. This repository ships the skill in `.agents/skills/declauding/`. See
  [the declauding skill](docs/declauding.md).

## Licence

The code and the guide are under the MIT licence, in [`LICENSE`](https://github.com/rahuldave/nossaifd/blob/main/LICENSE). The declauding skill in `.agents/skills/declauding/` is
under its own MIT licence, copyright (c) 2025 Oskar Austegard, in the file `LICENSE` of that folder. Rosalind Reid's PDFs in `sources/reid/`
are her work, used with her permission, and they are not under the MIT licence.

Rosalind Reid lets others use her work on one condition. Every place that uses it credits her. So where
text in the guide, the examples or the nossaifd skill comes from her work, it must keep its credit to
Rosalind Reid. The condition holds in every copy and in every changed version, and the MIT licence does not
remove it.

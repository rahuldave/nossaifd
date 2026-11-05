# The checker

`check.py` is a short Python program. It reads Markdown files and reports where the prose breaks a rule
of the guide that a program can measure. It needs Python 3.11 or later, and no other packages.

## Run it

Give the checker one or more Markdown files:

```
uv run --no-project python check.py docs/*.md
uv run --no-project python check.py -v docs/page.md
```

The first command shows the hard problems on each page. The `-v` option also shows the soft notes. The
program ends with exit status 1 if a page has a hard problem, so a script or a CI job can stop on it. CI
means continuous integration, a service that runs checks on every change to a repository.

## What it checks

The checker sorts what it finds into hard problems and soft notes. A hard problem breaks a rule. A soft
note marks something that a person must judge, because the program cannot tell if it is wrong.

| Hard problem | Rule in the guide |
|---|---|
| A sentence of more than 40 words | 8 |
| A paragraph of more than six sentences | 19 |
| A contraction, for example "don't" | 6 |
| An em dash, an en dash or a middle dot | 39 |
| A curly quote | 41 |
| A colon between two clauses | 40 |
| "i.e." or "etc." | 4 |
| "not just" or "not only" | 35 |
| A count at the start of a paragraph or a heading, before a noun that announces what comes, as in "Three things to know." | 38 |
| A sentence that starts with a vague "This is" or "That means" | 37 |

| Soft note | Why a person must judge it |
|---|---|
| A sentence of more than 25 words, or an instruction of more than 20 words | Rule 8 allows an occasional longer sentence when its punctuation makes it clear |
| Two questions in a row | Rule 36 allows several questions in a row when they build tension in a story |
| A word that ends in -ing | It can be a noun such as "working copy". Rule 9 allows an -ing form anywhere, and prefers the simple form |
| A possible passive | "is" with a past participle can also be an adjective. Rule 9 also allows a passive that puts the known information first |
| A noun that names an action, followed by "of", for example "a measurement of" | Rule 9 allows such a noun when it names the action of the sentence before |
| A semicolon | Rule 40 allows one only between the steps of a sequence |
| A sentence that may have three clauses | The program counts commas and joining words, not grammar |
| A word with a simpler alternative | "allow" is sometimes the right word |

The note for a noun that names an action checks a rule of Rosalind Reid. She asks the writer to put each
action in a verb, in
[Rosalind Reid, written reports, pages 13 and 14](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).
The checker looks for a word that ends in -tion, -sion, -ment, -ance or -ence before "of". It leaves out common nouns
that name a thing, such as "section" and "version". It also leaves out a word with a capital letter in the
middle of a sentence. Such a word starts a name, as in "the Association of Europe".

## What it does not check

The checker reads only prose, which is paragraphs, list items and headings. It skips everything that
the guide exempts, because Markdown comes first:

- fenced code blocks and inline code
- tables
- link targets, URLs and image lines
- HTML
- words in straight double quotes, which are examples that the text talks about

The checker cannot judge meaning, tone, or a term that a page uses before it defines it. Read every page
after it passes.

## How it decides

The checker splits a block of prose into sentences after a full stop, a question mark or an exclamation
mark. A sentence can start in lower case, as with a name like "timewalk". Inline code counts as one word.

A sentence that starts with a common command verb, such as "Open", "Run" or "Use", counts as an
instruction. An instruction usually has 20 words at most, and any other sentence 25 words. A longer
sentence is a soft note. A sentence of more than 40 words is a hard problem.

## Use it in a project

Copy `GUIDE.md` and `check.py` into the project, for example into `docs/style/`. Then add a glossary of
the project's terms beside them. A recipe can run the checker on every page:

```just
# Check the pages against the writing guide. -v also shows the soft notes
style *args:
    uv run --no-project python docs/style/check.py docs/*.md {{ args }}
```

If the guide changes in this repository, copy both files into the project again.

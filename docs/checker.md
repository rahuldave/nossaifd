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
| A sentence of more than 25 words, or an instruction of more than 20 words | 8 and 14 |
| A paragraph of more than six sentences | 17 |
| A contraction, for example "don't" | 6 |
| An em dash, an en dash or a middle dot | 25 |
| A curly quote | 27 |
| A colon between two clauses | 26 |
| "e.g.", "i.e." or "etc." | 4 |
| "not just" or "not only" | 21 |
| A count at the start of a paragraph or a heading | 24 |
| A sentence that starts with a vague "This is" or "That means" | 23 |
| Two questions in a row | 22 |

| Soft note | Why a person must judge it |
|---|---|
| A word that ends in -ing | It can be a verb form, or a noun such as "working copy" |
| A possible passive | "is" with a past participle can also be an adjective |
| A semicolon | Two sentences are usually clearer |
| A sentence that may have three clauses | The program counts commas and joining words, not grammar |
| A word with a simpler alternative | "allow" is sometimes the right word |

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
instruction. An instruction has a limit of 20 words. Any other sentence has a limit of 25 words.

## Use it in a project

Copy `GUIDE.md` and `check.py` into the project, for example into `docs/style/`. Then add a glossary of
the project's terms beside them. A recipe can run the checker on every page:

```just
# Check the pages against the writing guide. -v also shows the soft notes
style *args:
    uv run --no-project python docs/style/check.py docs/*.md {{ args }}
```

If the guide changes in this repository, copy both files into the project again.

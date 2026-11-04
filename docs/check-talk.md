# The talk checker

`check_talk.py` is a short Python program. It reads a talk, written as one Markdown deck. It reports where
the slides or the script break a rule of [TALKS.md](../TALKS.md) that a program can measure. It needs Python
3.11 or later, and no other packages.

Most rules of TALKS.md come from the tutorial deck and the presentation tips of Rosalind Reid. Her
presentation tips draw on The Chicago Guide to Communicating Science, by Scott Montgomery. The checks of slide titles come from a post by Shreya
Shankar. Several numbers are the guide's own, and TALKS.md marks each one.

## Run it

Give the checker one or more decks:

```
uv run --no-project python check_talk.py deck.md
uv run --no-project python check_talk.py -v deck.md
uv run --no-project python check_talk.py --minutes 20 deck.md
```

The first command shows the hard problems of each deck. The `-v` option also shows the soft notes. The
`--minutes` option gives the time slot of the talk, and it wins over the key `minutes` of the front matter.
A time slot is a number of minutes, such as `20`, `20 min`, `12.5` or `1:30`, which is a minute and a half.
It must be more than 0.

The program ends with one of three exit statuses:

| Status | Meaning |
|---|---|
| 0 | Every deck passes |
| 1 | A deck has a hard problem, so a script or a CI job can stop on it |
| 2 | A usage error, such as a missing file, an unknown option, or `--minutes` with no number after it |

The checker runs from any folder. It imports the Markdown reader of `check.py`, which must sit in the same
folder.

## The deck

A deck is one Markdown file, as Marp, Slidev and reveal.js read it:

- A line that is only `---` starts a new slide. A `---` inside a code block or a comment does not.
- YAML front matter can open the file. The key `minutes` gives the time slot. A byte order mark before the
  front matter does not hide it.
- The first heading of a slide is its title. The first slide holds the title of the talk.
- The script of a slide is in its notes.

The checker reads four kinds of notes:

| Notes | Tools |
|---|---|
| An HTML comment, `<!-- ... -->` | Marp and Slidev. TALKS.md recommends this form. |
| A block from `::: notes` to `:::` | Pandoc and Quarto |
| A block from `<aside class="notes">` to `</aside>` | reveal.js |
| A line that starts with `Note:`, and the rest of the slide after it, on a slide with no other notes | reveal.js |

The checker reads `Note:` only in a deck with no key `marp` in its front matter. It decides for each slide.
A slide that has an HTML comment or another block as notes keeps them, and its `Note:` line is text on the
slide. So an author's comment on the title slide does not turn off `Note:` on the other slides. The line must
start with `Note:` exactly, with a capital N and no space before it. In a Marp deck, a line such as "Note:
the cache is cold" is text on the slide, and the checker checks it.

A comment in which each line sets a Marp directive, such as `<!-- _class: lead -->`, is not notes. In a
comment that also holds the script, only a line that starts with `_`, such as `_class: lead`, is a directive.
Every other line is script, so a script line such as "title: we explain the chart" stays. A slide that
has only lowercase `key: value` lines is the front matter of the next slide, as in Slidev.

## What it checks

The checker sorts what it finds into hard problems and soft notes. A hard problem breaks a rule, and the
program can be sure of it. A soft note marks something that a person must judge. The program cannot tell if
it is wrong, or the rule says "about".

| Hard problem | Rule in TALKS.md |
|---|---|
| A slide with more than 4 items. Each item of a list counts, nested or not | 41 |
| A slide with more than 40 words. Tables count, and equations and figures do not | 42 |
| A paragraph of two or more sentences on a slide. A full stop in an abbreviation, as in "Fig. 2." or "vs.", does not end a sentence | 43 |
| Two titles that start with the same two words, but are not the same title | 44 |
| A title whose own punctuation sets its structure apart from most titles: a question mark, a label and a colon, or a full stop. "Most" means more than half | 45 |
| More than 2 equations on a slide | 50 |
| An equation on a slide with no script | 50 |
| A figure with no line of text right above it or right below it. A Marp background, such as `![bg](photo.jpg)`, is not a figure | 51 |
| A script longer than 120 words for each minute of the slot | 33 |
| A spoken sentence of more than 25 words | 25 |
| A sentence of the script that starts with "So," and a comma | 26 |
| Two questions in a row in the script | 21 |
| A time slot in the front matter that the checker cannot read, or that is not more than 0. The problem names the value | 33 |
| A deck with no slides | |

| Soft note | Why a person must judge it |
|---|---|
| A slide with 31 to 40 words | The limit is about 30 words |
| A list item of two or more sentences | An item can need a second short sentence |
| A slide after the first one with no title | A slide of only a picture can do without one |
| A title with no question mark, colon or full stop of its own, whose structure differs from most titles | The program guesses its structure. It takes a word from a short list of verbs as the verb of a sentence, unless the word comes first or comes after a word such as "of" or "the" |
| Titles of which no structure has more than half. The note names the structure of each title | No title is the odd one out, so a person must choose the structure |
| A script shorter than 90 words for each minute of the slot | A talk need not fill all its time |
| No time slot | The program cannot check the length without one |
| A slide after the first one with no script | Some slides need no words |
| More than 120 words of script for one slide | A slide can need more than a minute |
| A spoken sentence of 21 to 25 words | One breath is about 20 words, and the limit is a guess |
| A sentence of the script that starts with "So" and no comma | "So" can mean "therefore" |
| A question at the end of the script of a slide | The answer can come on the next slide |

## Why the split is where it is

A check is hard when the program measures the rule exactly and the rule has a clear limit. The count of items,
the count of equations and two questions in a row are exact. A question mark, a colon after a label, and a
full stop are exact signs of the structure of a title. "So," with a comma is the filler. "So" with no comma
can mean "therefore", which GUIDE.md allows.

A title that has one of these marks, when most titles do not, is a hard problem. A title with none of these
marks is a soft note, even when most titles are questions. The program cannot be sure whether such a title is
a sentence or a phrase. When no structure has more than half the titles, the checker gives one soft note that
the titles mix structures, and no hard problem.

A check is soft when the rule says "about", or when the program guesses. The limit of 30 words is "about", so
the checker fails a slide only above 40. The script can be shorter than the slot. Rosalind Reid warns
that the time can change on the day
([Rosalind Reid, presentation tips, page 1](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
A title of two words or fewer, such as "Thanks", has no structure to compare, so the checker leaves it out.

## What it does not check

The checker reads the slides and the script only. It skips code blocks, HTML, link targets and the labels
inside an image. It does not apply the rules of GUIDE.md. Read the words of the slides against GUIDE.md
yourself. Do not run `check.py` on a deck, because it also reads the script and fails its contractions.

jnterfaces installs the recipe `just prose` with the role `prose`. The recipe runs `check.py` on every
Markdown file that git tracks. It leaves out only `AGENTS.md`, `CLAUDE.md` and the files in `.agents`,
`.claude` and `.codex`. The recipe has no way to leave out a deck. A deck named `talk.deck.md` still ends in `.md`, so
the recipe checks it. Do one of these things instead:

- Give the deck the extension `.markdown`, which the recipe does not match. Check first that your slide tool
  reads a file with that extension.
- Run `just prose` with the names of the pages to check, so that it checks only those pages.

The checker cannot judge these rules:

- the story and its five parts
- the news first in a spoken sentence
- the fit of the talk to its audience
- the tone, the analogies and the humor
- the colors, the background and the labels inside a figure

Read the deck after it passes.

## Use it in a project

Copy `TALKS.md`, `check_talk.py` and `check.py` into the project, for example into `docs/talks/`. Keep the
two programs in one folder. A recipe can run the checker on every deck:

```just
# Check the decks against the talk guide. -v also shows the soft notes
talks *args:
    uv run --no-project python docs/talks/check_talk.py talks/*.md {{ args }}
```

In a project with the skill `presentations`, the skill holds copies of all three files. Run
`.agents/skills/presentations/scripts/check_talk.py` instead.

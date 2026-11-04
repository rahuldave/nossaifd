# Sources and credit

The rules on this site come from five sources. This page says who wrote each one, where to read it, and
which part of the site uses it. Each rule in [the guide](../GUIDE.md) and [the talk guide](../TALKS.md) also
names its source and links to the exact page.

## Rosalind Reid

Rosalind Reid taught "Communicating Your Work", a tutorial for the course AC297r at the
Institute for Applied Computational Science at Harvard, in March 2015.
She was the editor of *American Scientist* magazine from 1992 to 2008. She worked at the Harvard Initiative
in Innovative Computing from 2008 to 2010. She worked at the Institute for Applied Computational Science
from 2010 to 2013. In 2015 she was the executive director of the
[Council for the Advancement of Science Writing](https://casw.org/).

Rosalind Reid gave permission to use her material, on one condition. Every place that uses her work
credits her. The test file `tests/test_credit.py` checks the credit in three ways:

- It fails when a page built on her work does not name her in full. The list of these pages has the README,
  the two guides and the two checkers. It also has this page, the pages on the checkers and on the rules,
  and the files of the two skills.
- It fails when any other file names "Reid" or links to `sources/reid/` and does not name her in full.
- It checks each rule and each paragraph of GUIDE.md and TALKS.md. It fails when one links to her PDFs
  and does not name her in full.

The test cannot tell if a page uses her advice with no link and no name. A person must check that.

This site does not copy her slides or her text. It states her advice in its own words, credits her, and
links to her PDFs in the repository on GitHub. Her material, as she gave it:

| File | What it holds | Pages | Used in |
|---|---|---|---|
| [Written reports](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf) | "Communicating Your Work: written reports". How a written sentence differs from a spoken one, the stress position, actions in verbs, revision | 23 | [The guide](../GUIDE.md), and rules 19, 24 and 56 of [the talk guide](../TALKS.md) |
| [Tutorial deck](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf) | "Communicating Your Work: a tutorial". The story of a project, the audience, slides and figures, the storyteller's tricks, an exercise | 59 | [The guide](../GUIDE.md) and [the talk guide](../TALKS.md) |
| [Presentation tips](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf) | "Some thoughts about presentations". Preparation, pace, practice, nine common problems, layout | 5 | [The talk guide](../TALKS.md) |

The files are in the folder
[sources/reid](https://github.com/rahuldave/nossaifd/tree/main/sources/reid) of the repository. Each rule
that uses them gives the page number next to its link.

Reid credits the [Duke Scientific Writing Resource](https://sites.duke.edu/scientificwriting/) for her rules
about sentences. The presentation tips draw mostly on Scott L. Montgomery's book, below.

## Scott L. Montgomery

Scott L. Montgomery wrote *The Chicago Guide to Communicating Science*, from the University of Chicago Press.
Reid's [presentation tips](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf) draw
mostly on its chapter about talks. [The talk guide](../TALKS.md) uses the book through her tips. It names
Montgomery for each rule that she takes from him.

## ASD-STE100, Simplified Technical English

[ASD-STE100](https://www.asd-ste100.org/about.html) is a standard from the AeroSpace and Defence Industries
Association of Europe (ASD). Aircraft makers write their maintenance manuals in it, so that readers who are
not native English speakers understand them. Andrej Karpathy suggested that the same rules suit text that AI
models write. The rules of [the guide](../GUIDE.md) for words, sentences, instructions and paragraphs come
from it. Its dictionary of approved words is not part of the guide.

## Shreya Shankar

Two works by Shreya Shankar are sources:

- [The plain-writing skill](https://github.com/docwriter-org/plain-writing-skill), under the MIT licence.
  The rules of [the guide](../GUIDE.md) for tone, punctuation and the patterns of AI writing come from it.
- ["Five Principles for Generating Readable AI Text in Bulk"](https://fsdatalab.github.io/blog/agent-text-at-scale/),
  a post from October 2026. It is about many short items that a reader skims, such as titles, list
  items, notifications and the rows of a dashboard. The guide's rules for short items, and the talk guide's rules
  for slide titles, come from it.

## Where the sources disagree

The sources do not always agree. A spoken sentence puts the news first, and a written one puts it last.
Some sources ask for metaphor and humor, and others forbid them. [Why the rules](why.md) lists each
disagreement, what each source says, and what this site chose.

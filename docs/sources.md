# Sources and credit

The rules on this site come from four sources. This page says who wrote each one and where to read it. It
also says which part of the site uses each one. Each rule in [the guide](../GUIDE.md) also names its source
and links to the exact page.

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
  the guide, the examples and the checker. It also has this page, the pages on the checker and on the rules,
  and the file of the skill.
- It fails when any other file names "Reid" or links to `sources/reid/` and does not name her in full.
- It checks each rule and each paragraph of GUIDE.md, and each paragraph of EXAMPLES.md and of
  docs/why.md. It fails when one links to her PDFs and does not name her in full.
- It checks each example of EXAMPLES.md that comes from her work. It fails when the example does not
  name her in its own block.

The test cannot tell if a page uses her advice with no link and no name. A person must check that.

The guide states her advice in its own words. The examples quote her slides word for word, and each
example names her and links to the page. This site does not hold her PDFs. It links to them in the
repository on GitHub. Her material, as she gave it:

| File | What it holds | Pages | Used in |
|---|---|---|---|
| [Written reports](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf) | "Communicating Your Work: written reports". How a written sentence differs from a spoken one, the stress position, actions in verbs, revision | 23 | [The guide](../GUIDE.md) and [the examples](../EXAMPLES.md) |
| [Tutorial deck](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf) | "Communicating Your Work: a tutorial". The story of a project, the audience, slides and figures, the storyteller's tricks, an exercise | 59 | [The guide](../GUIDE.md) |

The files are in the folder
[sources/reid](https://github.com/rahuldave/nossaifd/tree/main/sources/reid) of the repository. Each rule
that uses them gives the page number next to its link.

Rosalind Reid credits the [Duke Scientific Writing Resource](https://sites.duke.edu/scientificwriting/)
for her rules about sentences.

Her third PDF, ["Some thoughts about presentations"](https://github.com/rahuldave/nossaifd-talks/blob/main/sources/reid/reid-presentation-tips.pdf),
is about talks, and the guide for reports does not use it. It is in the repository
[nossaifd-talks](https://github.com/rahuldave/nossaifd-talks), with the guide for talks. Her condition holds
there too, so each use credits Rosalind Reid.

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
  items, notifications and the rows of a dashboard. The guide's rules for short items come from it.

## Where the sources disagree

The sources do not always agree. A spoken sentence puts the news first, and a written one puts it last.
Some sources ask for metaphor and humor, and others forbid them. [Why the rules](why.md) lists each
disagreement, what each source says, and what this site chose.

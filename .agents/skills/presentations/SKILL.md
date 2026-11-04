---
name: presentations
description: Use when you plan, write or revise a talk, a slide deck, speaker notes or a talk script, for example a project presentation, a conference talk, a seminar or a public lecture. It gives rules for the story, the audience, the slides, the figures, the pace and the delivery of a talk, from the tutorial of Rosalind Reid and the book of Scott L. Montgomery, and a checker for a Markdown deck.
license: MIT, copyright (c) 2026 Rahul Dave. The full text is in the LICENSE file of https://github.com/rahuldave/nossaifd
---

# Presentations

This skill tells you how to plan a talk, write its script and make its slides. A talk is a story that a
speaker tells to one audience at one time. The slides support the speaker. They do not replace the speaker,
and they are not a paper.

The rules are in `references/TALKS.md`. Most of them come from Rosalind Reid, the editor of American
Scientist from 1992 to 2008. She taught them in a tutorial for the course AC297r at Harvard in March 2015.
Her presentation tips for the tutorial draw mostly on The Chicago Guide to Communicating Science, by Scott
Montgomery.
The rules for slide titles come from a post by Shreya Shankar. TALKS.md links each rule to its source.

## Steps

1. Read `references/TALKS.md`.
2. Ask the person about the audience, the occasion, the time, the questions, the room, and whether the
   slides go online. Rosalind Reid asks these questions before a talk. If the person cannot answer, write
   your assumption at the top of the plan.
3. Write the story in the five parts of Rosalind Reid, as one or two sentences for each part. Then make an
   outline, and remove each detail that the story does not need.
4. Write the deck as one Markdown file, in the format of the section "The deck format" of TALKS.md. Put
   the script of each slide in an HTML comment at the end of the slide.
5. Run the checker, and fix each hard problem. Read each soft note, and fix it when the note is right.
6. Check the deck against the checklist below.
7. Give the person a table of the slides with the time for each, and a plan for practice.

Run the checker from the root of the project:

```
uv run --no-project python .agents/skills/presentations/scripts/check_talk.py deck.md
uv run --no-project python .agents/skills/presentations/scripts/check_talk.py -v --minutes 20 deck.md
```

The checker needs only Python 3.11 or later, with no other packages. It imports the Markdown reader of
`scripts/check.py`, so keep the two files together.

## Write the words by the nossaifd guide

Write the words of the script and the slides by the nossaifd guide, GUIDE.md. The guide is in the skill
`nossaifd`, at `.agents/skills/nossaifd/references/GUIDE.md`. If that skill is not installed, read
https://github.com/rahuldave/nossaifd/blob/main/GUIDE.md.

The guide is for documents. The section "The words of the script" of TALKS.md lists the exceptions for
speech. In the script, put the news first, and use contractions. Ask one question only when the next sentence
answers it. Analogy, metaphor, humor and repetition are allowed in the script. The words on a slide follow the
guide too, except in two ways:

- A slide can hold a phrase in place of a sentence.
- All the titles of a deck can be questions, or all can be labels with a colon.

## Checklist

The numbers that the sources do not give are this skill's own numbers. TALKS.md marks each one.

- **The plan** names the audience, the occasion, the time and the one result that the audience must remember.
  Rosalind Reid asks for each of them.
- **The story** has the five parts of Rosalind Reid in order. They are the motivation, the description, the
  approach, the learning and the result. The approach gets the most care.
- **The script** has 90 to 120 words for each minute, the pace that Rosalind Reid gives after Montgomery. Aim
  nearer 90. The script marks the slides that the speaker can drop.
- **Each slide** passes the minute test of Rosalind Reid. A viewer finds its point in about 20 seconds.
- **Each slide** has at most 4 items and about 30 words, apart from the labels of a figure, and no paragraph.
- **The titles** start with the words that set each slide apart, and they share one structure.
- **Each figure** has a caption or a label next to it, and labels in plain words, written horizontally. The
  plain labels come from Rosalind Reid.
- **Each equation** has a sentence in the script that says what it means, as Rosalind Reid asks.
- **Each movie** has a still image before it, which says what to look for. The rule is from Rosalind Reid.
- **The deck** uses one background, and color only to carry information, as Rosalind Reid advises.
- **The thanks** go to the hosts at the start, and to the team, the funders and the audience at the end,
  as Rosalind Reid advises. Keep them brief.

## Files in this skill

- **`references/TALKS.md`** is the guide for talks and slides, with its sources.
- **`scripts/check_talk.py`** checks a Markdown deck against the rules that a program can measure.
- **`scripts/check.py`** is the checker of the nossaifd guide. `check_talk.py` uses its Markdown reader.

## Sources

The rules come from three PDFs of Rosalind Reid's tutorial "Communicating Your Work", all from March 2015.
They are the tutorial deck, the presentation tips "Some thoughts about presentations", and the written
reports. Her presentation tips draw on the book of Scott Montgomery, The Chicago Guide to Communicating
Science, and on the advice of Herbert Hirsch. The rules for titles come from Shreya Shankar, "Five Principles
for Generating Readable AI Text in Bulk". The skill uses Rosalind Reid's material with her permission. It
states her advice in its own words.

Text that comes from her work must keep its credit to Rosalind Reid, in every copy and in every changed
version of this skill. Her PDFs are not under the MIT licence.

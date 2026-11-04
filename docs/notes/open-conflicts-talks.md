# Open conflicts in the guide for talks

In this page, "Reid" means Rosalind Reid, and each use of her material is cited by the page of her PDF.

This page lists each conflict between the sources that the user's decisions did not settle, for TALKS.md and
`check_talk.py`. For each one, it gives what each source says, what TALKS.md does now, and why. The user
decides each one. The register of conflicts, `docs/notes/conflicts-register.md`, gives the background.

The links to Rosalind Reid go to her files on GitHub, and the text names the page:

- the tutorial deck, https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf
- the notes, https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf
- the report deck, https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf

## The length of a spoken sentence

**What the sources say.**

- The user asked for sentences that a speaker says in one breath. No source gives a number for a spoken
  sentence.
- GUIDE.md keeps a sentence to 25 words, for a reader.
- Shankar's plain-writing skill, rule 12, prefers long sentences, written "the way people explain things out
  loud" (https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md#L118-L134).
- Rosalind Reid's notes ask for a pace of 90 to 120 words a minute (notes, page 1). At 100 words a minute, a sentence
  of 25 words lasts 15 seconds.

**What TALKS.md does.** Rule 25 sets about 20 words, as this guide's own number, and never more than 25. The
checker fails a sentence above 25 words, and it gives a soft note above 20.

**Why.** The register, conflict 12, recommends that the script keeps the limit of 25 words. The soft note at
20 words carries the user's "one breath" without a number that a source does not give. Shankar's rule 12 is
for written prose, and it warns against a stack of short sentences. GUIDE.md already gives that warning.

## Contractions on a slide

**What the sources say.**

- Shankar's skill, rule 5, allows contractions everywhere, and its description names slides
  (https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md#L51-L54).
- Rosalind Reid's own slides use them (tutorial deck, page 27).
- GUIDE.md forbids them in documentation, for a reader who is not a native speaker.

**What TALKS.md does.** It allows contractions in the script, as the user decided. The words on a slide
follow GUIDE.md with no exception, so a slide has no contractions.

**Why.** The register, conflict 4, recommends this split. The audience reads a slide, so the reason of
GUIDE.md applies to it. The checker does not check slide words for contractions, because it shares no
writing rule with `check.py`.

## Analogy and metaphor on a slide

**What the sources say.**

- Rosalind Reid gives analogy, metaphor and humor as methods "for written, visual and spoken" work (tutorial deck,
  page 40). Her notes say that humor is always good, and that a metaphor connects the audience to the topic
  (notes, page 2).
- Shankar's skill, rule 21, forbids analogy and imagery, and its description names slides
  (https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md#L222-L228).
- GUIDE.md keeps documents literal.

**What TALKS.md does.** The script can use analogy, metaphor and humor. A picture on a slide can make an
analogy. The words on a slide stay literal (rules 22 and 27).

**Why.** The register, conflict 3, recommends this split. The speaker can explain a comparison, and a slide
cannot.

## Questions and structure in slide titles

**What the sources say.**

- Shankar's post, principle 3, asks for one structure in every item of a list
  (https://fsdatalab.github.io/blog/agent-text-at-scale/#3-use-the-same-structure-and-the-same-vocabulary).
- Rosalind Reid's titles mix questions and short phrases (tutorial deck, pages 13, 19 and 25). She repeats one title,
  "story elements", before each part of the story (tutorial deck, pages 16 to 37).
- GUIDE.md forbids rhetorical questions, and keeps headings literal.

**What TALKS.md does.** Rule 45 asks for one structure. The checker fails a title whose punctuation sets it
apart from most titles. It leaves out the first slide, titles of two words or fewer, and a title that repeats
another title exactly.

**Why.** The user chose Shankar's rule for titles. The exceptions keep three common slides legal. They are the
title slide, a short slide such as "Thanks" or "Questions?", and an outline slide that the speaker shows again,
as Reid does. A deck of question titles passes, if all its titles are questions.

## The script for one slide

**What the sources say.**

- Rosalind Reid's tutorial deck, page 32, says that a viewer sees each slide for less than 60 seconds.
- Reid's notes, page 4, use the minute as a test of the content of a slide.
- No source gives a time to speak for each slide. The register, conflict 6, recommends about 100 words of
  script for each slide, as the skill's own number.

**What TALKS.md does.** Rule 37 keeps the script of one slide to about a minute, which is 120 words at the
fastest pace. The checker gives a soft note above 120 words.

**Why.** The limit of 120 ties the number to the pace that Reid's notes give. The register's 100 has no
reason of its own. The note is soft, because a slide with a hard figure can need more time.

## Numbers that are this guide's own

The user decided 4 items on a slide, and about 30 words. The checker needed more numbers, and
no source gives them. TALKS.md and `check_talk.py` mark each one.

| Number | Where | Why this number |
|---|---|---|
| A hard limit of 40 words on a slide | `check_talk.py`, rule 42 | "About 30" needs some room before a hard problem |
| At most 2 equations on a slide | rule 50 | Rosalind Reid says "few equations" (tutorial deck, page 30) |
| A hard problem for "So," with a comma | rule 26 | The comma marks the filler. "So" without it can mean "therefore", which Reid's notes allow when it is used sparingly (notes, page 3) |
| Nearer 90 words a minute | rule 34 | A first script is usually too long. The register, conflict 6, asks to mark it as the guide's own |

## The thanks at the start

**What the sources say.** Rosalind Reid's tutorial deck, page 39, puts the thanks to the team and the funders at the
end, then the thanks to the audience. Her notes, page 2, say that a professional talk often starts with
thanks to colleagues, funders and organizers. GUIDE.md forbids a start with the history of the project.

**What TALKS.md does.** It thanks the hosts and the organizers briefly at the start (rule 16). It thanks the
team, the funders and the audience at the end (rule 18).

**Why.** The register, conflict 13, recommends this split. The user may want the colleagues and funders at the
start too, as Reid's notes allow.

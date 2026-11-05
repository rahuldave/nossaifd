# Open conflicts in the guide for documents

This page is a record of the first drafts. The project's author has since decided every entry, and [Why the rules](../why.md) gives the decisions. The rule numbers on this page are those of the first drafts.

In this page, "Reid" means Rosalind Reid, and each use of her material is cited by the page of her PDF.

This page lists each conflict between the sources of `GUIDE.md` that the user has not yet decided. For each
one, I applied the resolution of the conflicts register, `docs/notes/conflicts-register.md`. Each entry says
what the sources say, what I chose and why. The user decides each entry after the work is done.

Each link to a deck of Rosalind Reid names the page in its text. A GitHub page cannot open a PDF at a
page. The links to Shankar's skill point to commit f0d3630.

## 1. Rhetorical questions

**What the sources say.**

- [Shankar's skill, rule 23](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L240)
  forbids two or more rhetorical questions in a row. It does not forbid one.
- Rosalind Reid uses a question as the title of a slide. Examples are in
  [Rosalind Reid, talks, pages 13 and 19](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf),
  and in [Rosalind Reid, written reports, pages 5 to 10](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).
- The guide's rule 36 forbids every rhetorical question in a document.

**What I chose.** I kept rule 36 for documents, as the register recommends. The section "Sources" of the
guide now lists the rule as a change to Shankar's skill.

**Why.** In a document, a question delays the fact. A reader can see the heading, so a question does no
work that a heading cannot do. Reid's questions are slide titles in a talk.

## 2. Contractions in documents

**What the sources say.**

- [Shankar's skill, rule 5](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L51)
  allows contractions, because they match everyday speech.
- Rosalind Reid gives no rule. Her slides use contractions.
- The guide's rule 6 forbids contractions in documentation.

**What I chose.** I kept rule 6 for documents, and I marked it as the guide's own. The section "Sources"
lists it as a change to Shankar's skill. A spoken script is the work of the guide for talks, now in
nossaifd-talks, not this one.

**Why.** The register recommends no contractions in a document. A reader who is not a native speaker reads
the full form more easily.

## 3. "e.g." before examples

**What the sources say.**
[Shankar's skill, rule 11](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L105)
writes "e.g." before examples in a sentence. The guide's rule 4 forbids "e.g.", and the checker fails it.

**What I chose.** I kept rule 4, marked it as the guide's own, and listed it as a change in "Sources".

**Why.** The register asks the guide to list each change. The words "for example" are easier for a reader
who is not a native speaker.

## 4. Semicolons between the steps of a sequence

**What the sources say.**
[Shankar's skill, rule 9](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L83)
allows a semicolon between steps. The guide's rule 40 forbids a semicolon in prose.

**What I chose.** I kept rule 40, and listed it as a change in "Sources".

**Why.** Rule 15 already gives each step its own sentence, as Shankar's rule 9 also allows.

## 5. Sentence length

**What the sources say.**
[Shankar's skill, rule 12](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L118)
prefers long, explanatory sentences. STE, from memory of Issue 8, sets 25 words for a description. Rosalind
Rosalind Reid gives no number. She asks the writer to remove words that do no work, in
[Rosalind Reid, written reports, page 11](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).

**What I chose.** I kept rule 8 at 25 words, as the register recommends, and listed it as a change in
"Sources".

**Why.** Rule 8 already joins the two views. It caps the length, and it forbids a stack of short sentences.

## 6. Where the new fact goes in a sentence

**What the sources say.** Rosalind Reid puts the context first and the news last in a written sentence. She
shows that a speaker often does the opposite, in
[Rosalind Reid, written reports, pages 6 and 7](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).
[Shankar's post, principle 2](https://fsdatalab.github.io/blog/agent-text-at-scale/#2-put-the-most-important-words-first)
puts the words that make an item different at its start.

**What I chose.** I limited rule 13 to prose that a person reads in order. A new paragraph in rule 13 names
the two other kinds of text. Rule 46 puts the distinctive words first in a short item.

**Why.** The register ranks the conflict first. User decision 3 adds the section for short items, but it
does not say how rule 13 and the new section meet.

## 7. A verb with a strong feeling

**What the sources say.**
[Shankar's post, principle 5](https://fsdatalab.github.io/blog/agent-text-at-scale/#5-align-the-connotation-of-verbs-with-the-purpose-of-the-dashboard)
asks for verbs such as "love" and "complain" in a dashboard. The guide's rule 5 removes words that add force
but no fact.

**What I chose.** Rule 49 allows such a verb in a short item, where the feeling is the fact. Rule 5 still
holds in prose.

**Why.** The register recommends the rule for short items only.

## 8. The -ing form in titles

**What the sources say.**
[Shankar's post, principle 1](https://fsdatalab.github.io/blog/agent-text-at-scale/#1-match-how-human-readers-parse-sentences)
writes the titles of active sessions with the -ing form, as in "Measuring vLLM performance". The guide's rule
9 prefers "runs" to "is running". STE, from memory, does not use the -ing form as a verb.

**What I chose.** Rule 45 allows the -ing form for the title of work in progress. Rule 9 still holds in
prose. The checker still notes each -ing form, and the page on the checker names rule 45.

**Why.** The register recommends the change for titles only.

## 9. A passive for an unknown actor

**What the sources say.** Rosalind Reid prefers the active voice, and she says that a mix of active and
passive can help, in
[Rosalind Reid, written reports, page 15](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).
STE, from memory, uses the active voice as much as possible.

**What I chose.** User decision 5 allows a passive that puts the known information first. The register
also recommends a passive when the actor is unknown. I added both to rule 9, and I marked the second as
the guide's own.

**Why.** The register gives both uses together. A sentence with an unknown actor has no subject for the
active voice.

## 10. The space for the approach

**What the sources say.** Rosalind Reid calls the approach the most important part of the story, in
[Rosalind Reid, talks, page 25](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf).
She does not say that it gets the most space.

**What I chose.** Rule 24 now says "Give the approach the most care". A sentence marks the most space as
the guide's own advice.

**Why.** The register gives these two fixes. I used both, so that the rule keeps its practical advice.

## 11. Catchy titles and rhythm

**What the sources say.**
[Shankar's skill, rule 7](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L63)
forbids a catchy heading. Rosalind Reid writes short, memorable slide titles, and she says that words give
flow and rhythm, in
[Rosalind Reid, written reports, pages 8 and 19](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).

**What I chose.** I kept rule 32 for documents, with no change.

**Why.** The register keeps headings literal, and it allows rhythm only in a spoken script. User decision
4 keeps documents literal.

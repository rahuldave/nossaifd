# Conflicts between the sources and the two drafts

In this page, "Reid" means Rosalind Reid, and each use of her material is cited by the page of her PDF.

**A record of the first drafts.** This register describes the first drafts of the guides and of the skill
for talks. Later work replaced those drafts. The files `slides.md`, `story.md` and `delivery.md` are gone,
and the line numbers of `SKILL.md` and of the other files no longer match. Read `GUIDE.md` and the page
`docs/why.md` for the current rules for reports. The guide for talks, `TALKS.md`, and the skill for talks
moved to https://github.com/rahuldave/nossaifd-talks.

The PDFs of Rosalind Reid now live in `sources/reid/`, under new names:

| Name in this register | File now |
|---|---|
| `AC297r tutorial March 2015-writing.pdf` | `sources/reid/reid-2015-written-reports.pdf` |
| `AC297r-presentation-slides.pdf` | `sources/reid/reid-2015-communicating-your-work-deck.pdf` |
| `Presentation_tips.pdf` | `sources/reid/reid-presentation-tips.pdf` in https://github.com/rahuldave/nossaifd-talks |

This register lists each conflict between the sources of the writing guide. It also lists each place where
a draft says something that its source does not say. The drafts are `GUIDE.md`, with the new material from
Rosalind Reid, and the draft skill in `.agents/skills/presentations/`.

## The sources and the drafts

| Short name | What it is | Where I read it |
|---|---|---|
| STE | ASD-STE100, Simplified Technical English, Issue 8 | https://www.asd-ste100.org/about.html, and what `GUIDE.md` takes from it. No local copy. |
| Shankar's skill | The plain-writing skill, commit f0d3630 | `skills/plain-writing/SKILL.md` in https://github.com/docwriter-org/plain-writing-skill |
| Shankar's post | "Five Principles for Generating Readable AI Text in Bulk", 29 October 2026 | https://fsdatalab.github.io/blog/agent-text-at-scale/ |
| Rosalind Reid's report deck | "Communicating Your Work: written reports", 23 pages | `AC297r tutorial March 2015-writing.pdf` |
| Reid's talk deck | "Communicating Your Work: a tutorial", 25 March 2015, 59 pages | `AC297r-presentation-slides.pdf` |
| The tips | "Some thoughts about presentations", after Montgomery, 5 pages | `Presentation_tips.pdf` |
| The guide | The draft `GUIDE.md` in this worktree | rule numbers as in the draft |
| The talk skill | The draft `.agents/skills/presentations/` | file and line numbers as in the draft |

I read every page of the three PDF files. I read the text layer of each page, and I looked at each page
that is only a picture. Page numbers are the page numbers of the PDF file.

STE has no local copy. The about page confirms the purpose of STE and its rule of one word for one meaning.
It does not give the writing rules. Where this register gives an STE rule that the about page does not
give, it says that the rule comes from memory of Issue 8.

## Three contexts

The sources write for three different kinds of reader. Most conflicts in this register go away when each
rule is kept to its own context.

- **Reading a long document.** A person reads a report, a README or a design document in order, often once.
  STE, Shankar's skill and Rosalind Reid's report deck write for this reader.
- **Skimming many short items.** A person scans a feed, a list of titles, a set of notifications or a
  dashboard. The person reads the first words of each item and moves on. Shankar's post writes for this
  reader.
- **Listening to a talk.** A person hears each sentence once, at the pace of the speaker, and sees each slide
  for less than a minute. Reid's talk deck and the tips write for this listener.

## The conflicts, ranked

The rank is by how much the conflict changes what an agent writes. Rank 1 changes the most text.

| Rank | Conflict | Contexts in conflict | Recommended resolution | Where | How sure |
|---|---|---|---|---|---|
| 1 | Where the new fact goes in a sentence | long document, talk, short items | New fact last in a document, first in a talk, distinctive words first in an item | both | high |
| 2 | Where the result goes in the whole piece | long document, talk, short items, status notes | Rosalind Reid's order for a report or a talk that people take in whole, result first for a README, a status note or an item | guide | medium |
| 3 | Analogy, metaphor, humor and tone | long document, talk, short items | Literal in a document, allowed in a talk script, sentiment verbs allowed in an item when the sentiment is the fact | both | high |
| 4 | Contractions | long document, talk | None in a document or on a slide, allowed in a spoken script | talk skill, checker | medium |
| 5 | Active and passive voice | long document, short items | Allow a passive that puts the known information first | guide | medium |
| 6 | The numbers in the talk skill | talk | Keep them as the skill's own numbers, and make them agree with the guide | talk skill | high |
| 7 | Statements that a source does not support | all | Correct each one | both | high |
| 8 | The first word of an item | short items, long document | Subject or verb first in an item, the guide's rules in prose | guide | medium |
| 9 | Questions as headings and signposts | long document, talk | Allow one question that the next sentence answers, in a talk | talk skill, maybe guide | medium |
| 10 | Catchy titles and rhythm | long document, talk | Literal titles everywhere, rhythm only in the spoken script | talk skill | medium |
| 11 | -ing forms and tense in titles | long document, short items | Allow the continuous form for a title of work in progress | guide | medium |
| 12 | Sentence length | long document | Keep 25 words | guide | medium |
| 13 | Where the thanks go in a talk | talk | Short thanks to the hosts at the start, thanks for the work at the end | talk skill | high |
| 14 | Pictures for pleasure, and clutter | long document, talk | Decorative pictures only in a talk, never inside a data figure | talk skill | medium |
| 15 | Repetition, and the word "so" | long document, talk | Already resolved in the talk skill | none | high |

## 1. Where the new fact goes in a sentence

**What the sources say.**

- Rosalind Reid's report deck, page 6, gives a sentence from a news report and says "A speaker often presents the
  'news' first, followed by the context."
- Reid's report deck, page 7, says "Writing is generally more effective when you present the context first.
  The 'news' should be toward the end of the sentence, in the 'stress position.'" Pages 9 to 11 give the
  topic position and the stress position.
- Shankar's post, principle 2, says that readers of a list "often see only the first two words of each
  item". It tells the writer to move the words that make each item different "as close to the start of the
  item as possible".
- Shankar's skill, in the deslopify command, says "Start with the main conclusion".
- The guide, rule 13, puts the known information first and the new information last. The rule gives no
  context, so it applies to every sentence.
- The talk skill, `SKILL.md` line 75, says "Everything else in the guide applies to the script and to the
  slides." So rule 13 governs the spoken script.

**The context of each source.** Reid draws the line herself. Pages 5 to 7 of her report deck compare a
spoken sentence with a written sentence, and they put the news in opposite places. Her stress position is
for a reader of a document. Her news first is for a listener. Shankar's post is for a person who skims
items and stops after two words.

**The conflict.** The talk skill tells an agent to write the script by rule 13. Reid says that a speaker
does the opposite. The guide gives rule 13 with no limit. So an agent also applies it to titles in a
feed, where Shankar's post needs the distinctive words first.

**Recommended resolution.**

- In the guide, limit rule 13 to prose that a person reads in order. Add one sentence that names the two
  other contexts and points to the right rule.
- In the talk skill, add a rule for the script. Put the news first in a spoken sentence, then the context,
  as Reid's page 6 does. Name rule 13 as an exception in the list at `SKILL.md` lines 64 to 75.
- In the guide, add rules for short items from Shankar's post, if the user adds the post as a source. A
  title, a notification or a row in a dashboard starts with the words that make it different from the
  other items.

**How sure.** High that the sources say this. Reid states the contrast in her own words. Medium-high that
the resolution is right for every talk, because Reid gives one example sentence and no rule beyond it.

## 2. Where the result goes in the whole piece

**What the sources say.**

- Rosalind Reid's talk deck, pages 16 to 38, gives five story elements in order. The result comes last. Page 38
  gives the result as "conclusion, discussion, implications".
- Reid's report deck, pages 2 to 4, says that a report tells the same story "in much more detail", with the
  same five elements. So Reid puts the result last in a report too.
- The tips, pages 1 and 2, give Montgomery's structure of a professional talk. It is why, how, what was
  found, and what it means. The result is again near the end.
- The guide, rules 20 and 26, puts the result last. It applies this order to "a report, a proposal, a design
  document or a project README".
- Shankar's skill, in the deslopify command, rewrites a text "for a sharp CEO or technical reader". It says
  "Start with the main conclusion, then cover the background".
- Shankar's post puts the most important words first in each item. In its takeaways, it says that its
  principles "apply to any artifact or product that AI generates, e.g., websites".

**The context of each source.** Reid wrote for students of AC297r, a project course. A project report and a
project talk are taken in whole, and the reader follows a story. Shankar's deslopify command is for a busy
reader who may stop after the first paragraph. Shankar's post is for skimmed items.

**The conflict.** A README is closer to Shankar's reader than to Reid's reader. A person opens a README to
learn what the project does and how to start. The guide's rule 20 tells an agent to start a README with the
motivation and to end it with the result. An agent that follows the rule writes a README that hides what
the tool does.

**Recommended resolution.**

- Keep Reid's order for a report, a proposal or a talk that the reader takes in whole.
- Remove "project README" from the list in the guide's section "Long documents". Say instead that a README,
  a status note, a pull request and a summary start with the result, as Shankar's skill does.
- Decide whether a long report also gets a short summary at the top that states the result. Reid does not
  give this rule. It would be a new rule of the guide.

**How sure.** High that the sources say this. Medium for the resolution, because the line between a report
and a README is a choice for the user.

## 3. Analogy, metaphor, humor and tone

**What the sources say.**

- STE, on its about page, chooses one meaning for each word. Its example is that "to fall" means "to move
  down by the force of gravity", not "decrease". A figurative sense of a word is not an approved meaning.
  I found no explicit rule on metaphor in the parts of STE that I could read.
- Shankar's skill, rule 21, says "No analogies or imagery." Rule 7 says "Keep the writing boring". Its
  description names slides among the texts it covers.
- The guide, rules 32 and 33, keeps the writing literal and forbids analogy and metaphor.
- Rosalind Reid's talk deck, page 40, gives six "storyteller's tricks for written, visual and spoken presentation".
  They are analogy (page 41), an informal style (page 43), metaphor (page 55) and humor (page 57), with
  pictures and simplicity.
- Reid's report deck, page 19, says that words "convey nuance, sentiment, humor, emphasis" and "create flow
  and rhythm". Page 20 says that pictures "add visual humor".
- The tips, page 2, say "Humor is always good" and "Metaphors and metaphorical images are good for
  connecting the audience to the topics". Page 4 plans humor after a hard part of a talk.
- Shankar's post, principle 5, wants verbs with a strong connotation, for example "Users love" and "Users
  complain".

**The context of each source.** STE is for maintenance procedures that a reader who is not a native speaker
must follow exactly. Shankar's skill is for documents and messages from an AI model. Reid applies her
tricks to all three forms, written, visual and spoken. Shankar's post uses tone only to show the purpose of
a dashboard to a person who skims it.

**The conflicts.**

- The guide states the departure from Reid correctly in its section "Sources". The talk skill does not.
  `SKILL.md` lines 64 to 66 say that "Reid recommends some devices for a talk that the guide forbids in
  documentation". Reid recommends the devices for writing as well, so the sentence narrows her advice.
- Shankar's skill names slides, and it forbids analogy there. The talk skill allows analogy in the script.
  The two rules meet on a slide.
- Shankar's post asks for a verb with a strong connotation. The guide's rule 5 removes words that add force
  but no fact. A verb such as "love" carries a fact when the item reports how users feel.

**Recommended resolution.**

- In a document, keep rules 32 and 33. Keep the note in the section "Sources" of the guide.
- In a talk script, allow analogy, metaphor and humor, as the talk skill already does. The sentence at
  `SKILL.md` line 65 must say that Reid recommends them for all forms. The guide keeps them out of
  documents.
- On a slide, allow a picture that makes an analogy, as on Reid's page 42. Keep the words of the slide
  literal.
- In a short item, allow a verb whose sentiment is the fact that the item reports. Put this rule in the
  section for short items, if the guide gets one.
- Mark "Say where the comparison stops being true" in `SKILL.md` line 69 as the skill's own rule. No source
  gives it.

**How sure.** High. Each source states its view in plain words.

## 4. Contractions

**What the sources say.**

- The guide, rule 6, says "Do not use contractions in documentation", because a reader who is not a native
  speaker reads the full form more easily. `check.py` fails any page with a contraction.
- Shankar's skill, rule 5, says "It's ok to use contractions. They match everyday speech, so use them
  freely."
- STE has a dictionary of approved words. I cannot confirm an explicit STE rule on contractions from the
  about page.
- Rosalind Reid gives no rule. Her own slides use contractions, for example "don't rush" on page 27 and "what didn't
  work" on page 36 of the talk deck. The tips use them too.
- Shankar's post gives no rule.

**The context of each source.** Rule 6 is for a reader. A script is for a speaker, who says it aloud, and
for a listener, who never sees it. Shankar's reason, everyday speech, is strongest for a script.

**The conflict.** The talk skill says that the whole guide applies to the script, and it tells the agent to
run the checker on the script. A script with "don't" fails the checker. A script without contractions makes
the speaker sound stiff, and it stresses each "not".

**Recommended resolution.**

- In the spoken script, allow contractions. Keep the full "do not" when the negation is the point of the
  sentence.
- On a slide, keep rule 6, because the audience reads the slide.
- Give the checker a way to accept contractions in a script, for example a flag or a file name pattern.
  The choice of the method is for the user.

**How sure.** Medium. No source speaks to a script directly. The resolution follows from the reasons that
the guide and Shankar's skill give.

## 5. Active and passive voice

**What the sources say.**

- STE, from memory of Issue 8, uses only the active voice in procedures, and the active voice as much as
  possible in descriptions. I could not check the rule.
- The guide, rule 9, prefers the active voice and allows a passive "only when the simple form is unclear".
- Rosalind Reid's report deck, page 15, says "use active voice when possible" and "Varying active and passive can be
  effective."
- Shankar's skill has no rule on voice. Rule 20 prefers "a human or process subject when that is clearer".
- Shankar's post, principle 1, shows that "Login bug fixed by the agent" makes a reader parse the item
  twice. Principle 3 cites Frazier, who found that readers read a second clause faster when it has the
  same structure as the first, "both active or both passive".

**The context of each source.** STE writes for a technician who acts on each sentence. Reid writes for a
reader of a report, where the order of known and new information drives the choice of voice. Shankar's post
writes for a reader who parses a short item once.

**The conflict.** The guide's rule 13 puts the known information first. Sometimes the only way to put the
known thing first is a passive. Rule 9, as written, does not allow that use. So rules 9 and 13 disagree,
and Reid's page 15 sides with rule 13.

**Recommended resolution.** In the guide, add a second correct use to rule 9. A passive is correct when it
puts the known information first, or when the actor is unknown. In a short item, use the active voice, or
start with the verb, as Shankar's post says.

**How sure.** Medium. The STE rule comes from memory.

## 6. The numbers in the talk skill

**What the sources say, and what the skill says.**

| The skill's number | Where in the skill | What the sources give |
|---|---|---|
| About 30 words on a slide | `slides.md` line 43, `SKILL.md` line 92 | No number. Rosalind Reid's talk deck, page 30, says "trim word count". The tips, page 2, call it "word clutter". The skill marks the number as its own. |
| Five items on a slide | `slides.md` line 40, `SKILL.md` line 94 | Reid's talk deck, page 27, says "human short-term memory holds 3 to 9 items at once". The line is on the slide "giving your talk", next to "don't rush" and "look at listeners". It is not about the items on a slide. |
| About a third of the talk for the approach | `story.md` line 72 | No number. Reid's talk deck, page 25, calls the approach "the most important part of your story". It does not say the most time. The skill marks the number as its own. |
| 90 to 120 words a minute | `delivery.md` line 20 | The tips, page 1, give "about 90 to 120 words per minute" and "about 2,000 words for a 20-minute talk". The skill is correct. |
| Nearer 90 words a minute | `delivery.md` line 73 | No source. The skill does not mark it as its own. |
| 60 seconds or less of the talk for each slide | `SKILL.md` line 90, `delivery.md` line 71 | Reid's talk deck, page 32, says "assume each slide will be viewed for less than 60 seconds". The tips, page 4, use the minute as a test of the content of a slide. Neither source sets the speaking time for a slide. |

**The conflict with the guide.** The guide's rule 44 keeps a list in prose to about four items. Shankar's
skill, rule 19, says three or four. The talk skill allows five items on a slide. An agent that follows both
the guide and the skill gets two limits.

**Recommended resolution.**

- Keep the 30 words and the third as the skill's own numbers, as they are marked now.
- Use four items on a slide, to agree with the guide. If the user wants five, say why a slide differs from
  a list in prose.
- Move the citation of 3 to 9 items. Say that Reid gives it in her advice on how to speak, as a reason not
  to rush.
- Mark "nearer 90" as the skill's own number.
- Describe the minute as a test of the content of a slide, as the tips do. Keep the limit of about 100
  words of script for each slide as the skill's own number.

**How sure.** High for what the sources say. The numbers themselves are choices for the user.

## 7. Statements that a source does not support

Each item names the draft, the statement and what the source says.

- **Keep the middle short.** `story.md` line 38 uses this heading. The tips, page 2, say "The middle is the
  core of a talk". They ask the speaker to trim the details out of the middle so that the talk reaches its
  end. The heading also disagrees with the rule that the approach gets the most time. Write "Trim the detail
  in the middle" instead. High.
- **Leave some questions for the end.** `delivery.md` line 58 reads Rosalind Reid's "do not try to answer all
  questions" as advice on the questions of the audience. On page 25 of the talk deck, the line is under
  "the presentation is not the paper". It is about the content of the talk. Remove the item or rewrite it.
  High.
- **The approach gets the most space or the most time.** The guide's rule 24, `SKILL.md` line 85 and
  `story.md` line 71 say this. Reid's page 25 says the approach is "the most important part". Say "Give the
  approach the most care" or mark the space as the guide's own rule. Medium, because the most important
  part often gets the most space.
- **A tutorial on written reports gives the structure and the figures.** The guide, lines 6 to 8, says this.
  Reid's report deck gives the sentence rules (pages 5 to 17) and the roles of words, pictures and symbols
  (pages 19 to 21). It names the five story elements on page 4 only. The detail of each element comes from
  the talk deck, pages 17 to 39. The rules for figures come from the talk deck, pages 30, 31 and 51 to 54,
  and from the tips. Name both decks as the source. The move of talk advice into documents is sound,
  because page 3 of the report deck calls a report the same story in more detail. High.
- **Rules that the guide adds under Reid's name.** The section "Long documents" says "They come from
  Rosalind Reid." Rule 21 adds "An AI model often starts a draft with what it built", and it forbids a start
  with the history or the method. Reid says neither. Rule 26 adds "its limits". Rule 22 adds that two
  readers can need two documents. Mark these additions as the guide's own. Medium.
- **The guide changes two of Shankar's rules.** The section "Sources" says this. The guide changes more.
  Shankar's rule 11 says to introduce inline examples with "e.g.", and the guide forbids "e.g.". Shankar's
  rule 23 forbids only stacked rhetorical questions, and the guide forbids all. Shankar's rule 9 allows
  semicolons between steps, and the guide does not. Shankar's rule 12 prefers long sentences, and the guide
  caps them at 25 words. List each change. High.
- **Bold at the start of a list item is a change.** Shankar's rule 18 forbids bold only "for decoration".
  Bold at the start of an item is not decoration, so the guide does not change the rule there. Low.
- **Reid's devices are for a talk.** `SKILL.md` lines 64 to 66 say this. Reid's page 40 gives them "for
  written, visual and spoken presentation". Conflict 3 gives the fix. High.
- **Reid's first rule for slides is less is more.** `slides.md` line 3 says this. In the talk deck, "less is
  more" on page 5 opens the general advice, not the advice on slides. The tips use the phrase about visual
  and word clutter. Low.
- **The author of the tips.** `SKILL.md` lines 122 to 124 give the tips to Reid, as the notes for the same
  tutorial. The file names no author. Its text says "Montgomery's/Reid's basic advice" and "McCormick/Reid
  tips", and it gives personal observations in the first person. Reid is the likely author. Say that the
  attribution is an inference. Low.
- **The metaphor slide.** `examples.md` line 75 says that a speaker must choose a metaphor "with care". Page
  56 of the talk deck shows a newspaper headline, "Violent Crime is a Beast Preying on Our City", with no
  text from Reid. The caution is the draft's reading. Mark it as such. Low.

## 8. The first word of an item

**What the sources say.** Shankar's post, principle 1, says "Start each item with its subject or its verb.
If the subject is the same in all items, drop it and start with the verb." The guide's rule 16 puts a
condition first. Rule 13 starts a sentence with a link to the sentence before. Rule 18 starts more support
with "For example", "Also" or "But".

**The context of each source.** Shankar's post is for an item that a person reads alone, with no sentence
before it. The guide's rules are for prose, where each sentence follows another.

**The conflict.** An agent that follows the guide in a list of titles writes "If the test fails, the
parser stops" or "Also, the build is slow". A reader who sees two words gets "If the" and "Also, the".

**Recommended resolution.** Add a section for short items to the guide. In an item, start with the subject
or the verb. Keep rules 13, 16 and 18 for prose.

**How sure.** Medium. The resolution needs the user to add Shankar's post as a source.

## 9. Questions as headings and signposts

**What the sources say.**

- The guide, rule 36, says "Do not ask rhetorical questions." `check.py` fails two questions in a row.
- Shankar's skill, rule 23, says "Do not stack rhetorical questions." It forbids two or three in a row.
- Rosalind Reid uses questions as titles. Her talk deck asks "how can you tell your story?" on page 13 and "what
  motivates this group of listeners?" on page 19. Her report deck asks "how is writing different?" on
  pages 5 to 10. The example slide on page 22 of the talk deck has two questions in a row.

**The context of each source.** In a talk, a question tells the listener what the next part answers. A
listener cannot see a heading, so the question does the work of a heading. In a document, a question
usually delays the fact.

**Recommended resolution.**

- In a talk script, allow one question when the next sentence answers it. Do not stack questions.
- In a document, keep rule 36, or relax it to Shankar's rule against stacked questions. The choice is for
  the user.

**How sure.** Medium.

## 10. Catchy titles and rhythm

**What the sources say.** Shankar's skill, rule 7, forbids a catchy phrase or a clever label. The guide's
rule 32 keeps headings literal.

Rosalind Reid's titles are often short phrases. Examples in the talk deck are "less is more" on page 5,
"the presentation is not the paper" on page 32 and "storyteller's tricks" on page 40.
Her report deck, page 8, is the single title "ba-da-BUM", for the rhythm of a sentence. Page 19 says that
words "create flow and rhythm". Shankar's post, principle 4, says that a difference between items must
carry a meaning.

**The context of each source.** Reid's phrases are slide titles in a talk, where the speaker explains each
one. Shankar's rule is for headings in a document, which a reader scans without a speaker.

**Recommended resolution.** Keep headings and slide titles literal. A slide title can state the point of
the slide as a sentence. Allow rhythm and a memorable phrase in the spoken script only, for the one result
that the audience must remember.

**How sure.** Medium.

## 11. -ing forms and tense in titles

**What the sources say.** Shankar's post, principle 1, puts each verb in the tense that matches what the
reader expects. Its example rewrites the titles of active sessions in the continuous form, as in
"Measuring vLLM performance". The guide's rule 9 says "Write 'runs' and not 'is running'". `check.py`
notes each -ing form. STE, from memory, does not use the -ing form as a verb.

**The context of each source.** Shankar's titles name work in progress, in a list of sessions. The guide
writes about prose.

**Recommended resolution.** In the section for short items, allow the continuous form for the title of
work in progress. Keep rule 9 for prose.

**How sure.** Medium. The STE rule comes from memory.

## 12. Sentence length

**What the sources say.** The guide, rule 8, keeps a sentence to 25 words or fewer. STE, from memory, gives
20 words for an instruction and 25 for a description, and the guide's rule 16 follows that. Shankar's
skill, rule 12, says "Prefer long, explanatory sentences over short, punchy ones" and writes "the way
people explain things out loud". Rosalind Reid gives no number. Her rule is "Omit unnecessary words" on page 11 of
the report deck.

**The context of each source.** Shankar's rule warns against a stack of short punchy sentences. STE caps the
length for a reader who is not a native speaker.

**Recommended resolution.** Keep the guide's rule 8. It already joins the two views. It caps the length at
25 words and forbids a stack of short sentences. No source gives a different number for a spoken script.

**How sure.** Medium.

## 13. Where the thanks go in a talk

**What the sources say.** Rosalind Reid's talk deck, page 39, puts the thanks to the team and the funders at the end,
then thanks the audience. The tips, page 2, say that a professional talk often begins "by acknowledging
colleagues and funders, thanking organizers". The guide's rule 27 credits people but gives no place. Rule 21
forbids a start with the history of the project.

**The context of each source.** Both are for a talk. Reid's deck shows one project talk. The tips describe
the custom of a professional meeting.

**Recommended resolution.** In the talk skill, thank the hosts briefly at the start. Thank the team and the
funders at the end. `story.md` lines 27 and 46 already say most of this. Make the checklist in `SKILL.md`
agree.

**How sure.** High.

## 14. Pictures for pleasure, and clutter

**What the sources say.** Rosalind Reid's report deck, page 20, says that pictures "provide visual relief and
pleasure" and "add visual humor". Reid's talk deck, page 30, says "remove distractions, chartjunk". The tips,
page 2, call decorative graphics "visual clutter". The guide's rule 30 says to remove from a data figure
what does not help.

**The context of each source.** Reid's pleasure is for a picture that stands alone, in a talk or a report.
Her clutter is inside a data graphic, or on a busy slide.

**Recommended resolution.** In the talk skill, allow a picture for relief or humor between parts of the
talk. Never add decoration inside a data figure. The guide needs no change.

**How sure.** Medium.

## 15. Repetition, and the word "so"

**What the sources say.** The guide's rule 28 removes a phrase that repeats, as Rosalind Reid's report deck does on
page 17. The tips, page 2, ask the speaker to reinforce key ideas, and to repeat the terms of the outline
when each topic comes.

The guide's rule 8 joins clauses with "so". The tips, page 3, say that a speaker who
does not overuse "so" as a filler sounds more confident.

**Agreement.** Every source agrees on one term for one concept. STE says "one word, one meaning". The
rule is also rule 4 of Shankar's skill, principle 3 of Shankar's post and rule 2 of the guide. The tips repeat the terms of the
outline.

**Recommended resolution.** None needed. The talk skill already allows repetition of key ideas in a talk.
The word "so" with the meaning "therefore" is correct in both contexts.

**How sure.** High.

## Decisions for the user

- **Contractions in a script.** Allow them in a spoken script, and decide how the checker knows that a file
  is a script. I recommend that the script allows them and the slides do not.
- **The order of a README.** Remove the README from Rosalind Reid's order, and start it with what the project does.
  I recommend this change. Also decide whether a long report gets a short summary of the result at the top.
- **Shankar's post as a fourth source.** Add it, with a section for short items, such as titles,
  notifications and rows in a dashboard. I recommend this, because the guide now gives the wrong rule for
  these items.
- **Analogy in documents.** Keep documents literal, against Reid's advice for written work, or allow an
  analogy for a general reader. I recommend that documents stay literal.
- **Questions.** Keep rule 36 as it is, or relax it to Shankar's rule against stacked questions. I
  recommend one answered question in a talk, and no change for documents.
- **The numbers on a slide.** Choose four or five items, and confirm 30 words and a third of the time. I
  recommend four items, to agree with the guide.
- **The passive voice.** Allow a passive that puts the known information first. I recommend this change to
  rule 9.

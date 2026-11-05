# Worked examples for reports

This file shows an AI agent how to write reports, with worked examples from the sources of the project.
Each example gives a piece of text from a source, the lesson in one sentence, and the rule that the example
shows. The rules are in [GUIDE.md](https://github.com/rahuldave/nossaifd/blob/main/GUIDE.md).

The examples for talks are in [the examples of nossaifd-talks](https://github.com/rahuldave/nossaifd-talks/blob/main/EXAMPLES.md), the repository of the guide for talks.
Many of them come from Rosalind Reid's slides. Some of them hold for reports too, and this file names them
where they fit.

## How to use the file

Apply a rule from GUIDE.md, and read the examples that name that rule. Each example ends with a
line "Rule", so a search for "GUIDE.md rule 13" finds every example of rule 13. Then write your own text. Do
not copy an example into your text.

The examples follow the sections of GUIDE.md.

Each example has the same parts:

- **A heading** with a letter, a number and a short name.
- **A credit line** that names the author and links to the place in the source.
- **The text** of the source, word for word, in a code block. A code block keeps the quotes, dashes and line
  breaks of the source. So the text in a code block does not follow the punctuation rules of GUIDE.md.
- **A description** in prose, marked "Description", when the example is a picture or a slide layout.
- **What it shows**, the lesson in one sentence.
- **Rule**, the rule of GUIDE.md that the example shows.

Some examples forbid something that the project now lets a writer do. They stay in the file, because the rest of the
example still teaches. A line "The project now" says what the project does, and it names the rule.

The letter of an example names its source:

- **W** is Rosalind Reid's written reports.
- **S, E, B and T** are Shreya Shankar's plain-writing skill. S is a pair or a list of words in the rules of
  the skill. An eval is the set of test tasks with which Shreya Shankar measures her skill. E is a table
  from the eval, and B is a bad specimen from it. T is a task prompt of the eval.
- **SP** is Shreya Shankar's post.

## Sources

The examples come from three works:

- **"Communicating Your Work", a tutorial by Rosalind Reid**, which she taught in the course AC297r at the
  Institute for Applied Computational Science at Harvard in March 2015. The examples here come from its
  [written reports](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf) (23 pages).
  GUIDE.md also cites her [tutorial deck](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf) (59 pages).
- **The plain-writing skill by Shreya Shankar**, at
  [commit f0d3630](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md) of https://github.com/docwriter-org/plain-writing-skill.
- **"Five Principles for Generating Readable AI Text in Bulk", a post by Shreya Shankar**, 29 October 2026,
  at https://fsdatalab.github.io/blog/agent-text-at-scale/.

GUIDE.md also draws on ASD-STE100, Simplified Technical English. It gives no examples here, because no copy
of the standard was available.

## Credit and licence

Rosalind Reid gave permission to use her material, on the condition that each use credits her. So each
example from her work names her in full and links to her PDF, at the example itself. Text that comes from
her work must keep its credit to Rosalind Reid, in every copy and in every changed version of this file. The
MIT licence of this repository does not remove that condition. Her PDFs are her own work, and they are not
under the MIT licence.

The plain-writing skill is under the MIT licence, copyright (c) 2026 Shreya Shankar. The examples come from
the skill at commit f0d3630, and each one links to its lines. The examples of the post are short, and each
one links to its section of the post, at https://fsdatalab.github.io/blog/agent-text-at-scale/.

Some texts in the repository of the skill are not by Shreya Shankar. A model wrote the answers in the eval
tables, and Anthropic Claude wrote the bad specimens. Each such example says who wrote it. In the post, the
bad theme cards of SP6 are the output of a Claude plugin, as the post says.

# The examples

## Words

### S1. Use simple, everyday words

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 1, lines 29 to 30](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L29-L30).

```text
Before: We leverage the cache to unlock a more robust query experience.
After: We use the cache to make repeated queries faster.
```

**What it shows:** Replace a fashionable word with a plain word, and replace a vague benefit with the
measured effect.

**Rule:** GUIDE.md rules 1 and 5. The words "leverage", "unlock" and "robust" are in the list of rule 5.

### S4. Use one term for one thing

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 4, lines 48 to 49](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L48-L49).

```text
Before: Upload the document. The file is parsed, and the record is saved.
After: Upload the document. The document is parsed and saved.
```

**What it shows:** Use one word for one thing, so the reader does not think that "file" and "record" are two
more things.

**Rule:** GUIDE.md rule 2, and rule 47 for the items of a list.

### S2. Say a technical phrase in common words

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 2, lines 37 to 38](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L37-L38).

```text
Before: The score is a calibrated proxy for whether the property holds.
After: The score estimates how likely the property is to hold.
```

**What it shows:** Say in common words what a technical phrase means, when a common phrase says it as
exactly.

**Rule:** GUIDE.md rule 3.

### S6. Do not invent a hyphenated adjective

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 6, lines 60 to 61](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L60-L61).

```text
Before: We added a reveal-style colon to the output.
After: We added a colon that shows the schema.
```

**What it shows:** Replace a made-up compound with a clause that says what the thing does.

**Rule:** GUIDE.md rule 3.

### S33. A compound adjective that is fine

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 6, lines 58 to 59](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L58-L59).

```text
"well-crafted"
```

**What it shows:** A hyphenated adjective that a dictionary has is correct.

**Rule:** GUIDE.md rule 3.

### S31. Words that AI tools overuse

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 1, lines 27 to 28](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L27-L28).

```text
"delve", "tapestry", "landscape", "robust", "leverage", and "reach"
```

**What it shows:** Avoid these words, because AI text overuses them.

**Rule:** GUIDE.md rule 5, which lists all of them except "reach".

### S3. Give the fact in place of empty emphasis

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 3, lines 44 to 45](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L44-L45).

```text
Before: This result matters, and it carries weight for the design.
After: The scores barely moved, so we can skip the model on most documents.
```

**What it shows:** Replace a claim that something is important with the fact that makes it important and the
decision that follows.

**Rule:** GUIDE.md rule 5. The "Before" also starts with a vague "This", against rule 37.

### S32. Words of empty emphasis

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 3, lines 41 to 42](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L41-L42).

```text
"really", "real", "matters", "worth", "carries weight",
"boasts", "a testament to", "pivotal", "renowned", and "quietly"
```

**What it shows:** These words add force but no fact.

**Rule:** GUIDE.md rule 5, which lists "really", "pivotal" and "matters". Rule 49 lets a writer use a verb that
reports a strong feeling, such as "love". It does not cover "boasts", which is praise and not a report of a
feeling.

### S5. Contractions

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 5, lines 53 to 54](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L53-L54).

```text
Before: Do not worry, it is not going to overwrite your file.
After: Don't worry, it's not going to overwrite your file.
```

**What it shows:** A contraction makes the text sound like speech.

**Rule:** GUIDE.md rule 6.

**The project now:** A document keeps the "Before" form by GUIDE.md rule 6. A spoken script uses the "After"
form, by the guide for talks in nossaifd-talks.

## Sentences

### S9. Write complete sentences, one fact to a sentence

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 8, lines 78 to 81](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L78-L81).

```text
Before: The agent polls the file and reacts to changes, and the team meets on
Tuesdays.
After: The agent polls the file and reacts to changes. The team meets on
Tuesdays.
```

**What it shows:** Do not join two unrelated facts in one sentence, and give each fact its own sentence.

**Rule:** GUIDE.md rules 7 and 8.

### S34. Plain words that join related ideas

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 8, lines 76 to 77](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L76-L77).

```text
"and", "because", or "so"
```

**What it shows:** Join two related clauses with a plain conjunction.

**Rule:** GUIDE.md rule 8.

### S12. No more than two clauses

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 11, lines 113 to 116](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L113-L116).

```text
Before: The parser reads the file, the validator checks the fields, and the
writer saves the record.
After: The parser reads the file, and the validator checks the fields. The
writer then saves the record.
```

**What it shows:** Split a sentence with three clauses into two sentences.

**Rule:** GUIDE.md rule 8. The text of the skill rule also puts an example in a sentence after "e.g.", which
GUIDE.md rule 4 permits.

### S13. Join a stack of short sentences

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 12, lines 124 to 128](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L124-L128).

```text
Before: The gate runs on every merge. It blocks regressions. Nobody
bypasses it.
After: The gate runs on every merge, and it blocks changes that fail a
regression case. A regression cannot make it to production, unless someone
deliberately overrides the check.
```

**What it shows:** Join a stack of short, punchy sentences into sentences that explain, and replace "Nobody
bypasses it" with the exact condition.

**Rule:** GUIDE.md rule 8, which also says not to cut one thought into a stack of short sentences. Rule 8
keeps a sentence to about 20 to 25 words, which the skill does not ask. The "After" keeps to it.

### S14. A labeled line for open work

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 12, lines 129 to 134](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L129-L134).

```text
Before: Search ranking now uses a scored model instead of heuristics. The
change reduced p95 latency from 900 ms to 220 ms. We still need to validate
recall on long queries.
After: Search ranking now uses a scored model instead of heuristics, and
p95 latency fell from 900 ms to 220 ms. To do: validate recall on long
queries.
```

**What it shows:** Join the change and its effect in one sentence, and put open work in a short labeled line.

**Rule:** GUIDE.md rule 8, and rule 40 for a colon after a short label.

### W11. Put the action into the verb

Credit: [Rosalind Reid, written reports, page 13](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).

**Description:** Two bullets, and two versions side by side, under the labels "implied action" and "explicit
action". The words "analyses" and "are" are colored on the left, and "should analyze" on the right.

```text
• Put your actions into verbs.
• Omit unnecessary words.

implied action
Detailed analyses of the evolutionary features of different types of regulatory elements are an important area for future research.

explicit action
Future research should analyze the evolutionary features of different types of regulatory elements.
```

**What it shows:** Turn the noun that hides the action ("analyses") into a verb ("should analyze"), and cut
the empty words.

**Rule:** GUIDE.md rule 9, and rule 5 for the words that add no fact.

### W12. A bad nominalization and a good one

Credit: [Rosalind Reid, written reports, page 14](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).

**Description:** The title, a definition, and two versions side by side. A blue arrow points from the note
at the bottom to the word "analysis" in the revision.

```text
beware of “nominalizations”

• actions that appear in parts of a sentence other than verbs

implied action
Our analysis using regression and k-means clustering revealed...

explicit action
We analyzed the data with regression and k-means clustering. This analysis revealed...

a “good” nominalization summarizes the action of the previous sentence
```

**What it shows:** Put the action in a verb, and use the noun form only to sum up the action of the sentence
before it.

**Rule:** GUIDE.md rule 9, which lets a noun name the action of the sentence before. The revision
"This analysis" also follows rule 37, because "This" comes with its noun.

### W13. Active voice, two pairs

Credit: [Rosalind Reid, written reports, page 15](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).

**Description:** The title "use active voice when possible", two bullets, and two pairs of sentences. The
passive version is on the left, and the active version is on the right.

```text
• Rewording in the active voice frequently sharpens the text.
• Varying active and passive can be effective.

The substrate surface was mapped using an Atomic Force Microscope.
The AFM mapped the substrate surface.

There were five mice receiving antibiotics.
Five mice received antibiotics.
```

**What it shows:** Name the actor as the subject and give it a simple verb, and the sentence gets shorter and
sharper.

**Rule:** GUIDE.md rule 9. Rosalind Reid's second bullet, that a mix of active and passive can help, is in
rule 9 too.

### S15. A mechanism, not an evocative phrase

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 13, lines 143 to 145](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L143-L145).

```text
Before: With trusted scores, improvement stops being guesswork.
After: With trusted scores, you can measure whether each change helped,
so you keep or revert each change based on the measured result.
```

**What it shows:** Replace an abstract phrase with the action that a reader can take, and the reason for it.

**Rule:** GUIDE.md rule 11.

**The project now:** The "Before" is close to a metaphor, and GUIDE.md rule 33 now permits a metaphor. The
"Before" still fails rule 11, because it states no mechanism.

### S16. Cut a side clause

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 13, lines 146 to 148](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L146-L148).

```text
Before: We still need to validate recall on long queries before we call
the work done.
After: To do: validate recall on long queries.
```

**What it shows:** Remove a clause that adds no fact, and state the open task as a label.

**Rule:** GUIDE.md rule 11.

### S38. An evocative abstraction and empty side clauses

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 13, lines 138 to 141](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L138-L141).

```text
"improvement stops being guesswork"
"before we call the work done", "as we move forward", or "for the time being"
```

**What it shows:** The first phrase sounds good but names no mechanism, and the three side clauses add no
fact.

**Rule:** GUIDE.md rule 11, which quotes "as we move forward" and "for the time being".

### B7. A support reply that says nothing (bad specimen, written by a model)

Credit: [llm_slop.json, lines 32 to 36](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/evals/sources/llm_slop.json?plain=1#L32-L36), in the eval of
Shreya Shankar's plain-writing skill. Shreya Shankar did not write the text. The attribution file of the
repository says that Anthropic Claude wrote it, as a bad example on purpose.

```text
Thank you for reaching out to us regarding the export functionality challenges you've experienced following our recent schema update. We truly appreciate you taking the time to bring this to our attention, as your feedback helps us continuously improve our platform experience.

We understand how important seamless data export capabilities are to your workflow, and we want to assure you that our engineering team is actively investigating the issue you've described. Our preliminary analysis suggests that the schema modifications may have impacted certain export pathways, and we're working diligently to optimize these processes for enhanced performance and reliability.

In the meantime, we recommend the following steps that have proven helpful for some users experiencing similar situations:

• Clear your browser cache and cookies
• Try accessing the export feature during off-peak hours
• Ensure you're using the most current version of your browser
• Consider exporting smaller data sets if possible

We're committed to delivering the exceptional service experience you deserve, and our dedicated team is prioritizing this matter with the urgency it requires. While we don't have a specific timeline at this moment, please know that we're leveraging our best resources to resolve this as quickly as possible.

We'll be sure to keep you updated as we make progress on this issue. If you continue experiencing difficulties, please don't hesitate to reach out again—we're here to support you every step of the way.

Thank you for your patience and understanding as we work through this together.

Warm regards,
Customer Success Team
```

**What it shows:** A reply that thanks and promises, but does not say what broke, has these faults:

- "seamless", "truly", "leveraging" and "exceptional" add no fact, by GUIDE.md rule 5.
- "certain export pathways" names no export, by rule 11.
- The steps are generic, and they do not follow from a cause, by rule 11.
- A dash joins two clauses in "please don't hesitate to reach out again", by rule 39.

**Rule:** GUIDE.md rule 11, and rules 5 and 39.

### W10. Put the verb close to its subject

Credit: [Rosalind Reid, written reports, page 12](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).

**Description:** The title "some simple rules", one bullet, and two versions side by side. The subjects are
green and the verbs are blue. The left version is the poor one, and the right version is the revision.

```text
• Follow a subject with a verb as soon as possible.

DNA in repeat regions or with long stretches of the same base or small microsatellites causes problems for next-gen sequencers.

DNA causes problems for next-gen sequencers whenever it is in repeat regions. Long stretches of the same base or small microsatellites also cause problems.
```

**What it shows:** A long gap between subject and verb makes the reader wait, so split the sentence and bring
the verb close.

**Rule:** GUIDE.md rule 12. Rule 8 also applies, because the revision splits one sentence into two.

### W4. One news story, spoken and written

Credit: [Rosalind Reid, written reports, page 5](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).

**Description:** A slide with the title "how is writing different?" in green, and two labelled quotations.

```text
how is writing different?

presentation
“Two people were injured today, and traffic was tied up for two hours, after a driver lost control of a tractor-trailer truck on the Zakim Bridge.”

written report
“A driver lost control of a tractor-trailer truck on the Zakim Bridge today, causing an accident that injured two people and tied up traffic for two hours.”
```

**What it shows:** A speaker gives the news first and the cause after it. A writer gives the cause first and
the news at the end.

**Rule:** GUIDE.md rule 13 for the written version. Example W5, "The spoken version, marked up", in
[the examples of nossaifd-talks](https://github.com/rahuldave/nossaifd-talks/blob/main/EXAMPLES.md), marks up the spoken version. It comes from Rosalind Reid's written
reports, page 6.

### W6. The written version, marked up

Credit: [Rosalind Reid, written reports, page 7](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).

**Description:** The written sentence of W4. The words "driver lost control of a tractor-trailer truck" are
underlined in blue. The words "injured two people and tied up traffic" are underlined in dark red. The
caption follows.

```text
written report
“A driver lost control of a tractor-trailer truck on the Zakim Bridge today, causing an accident that injured two people and tied up traffic for two hours.”

Writing is generally more effective when you present the context first. The “news” should be toward the end of the sentence, in the “stress position.”
```

**What it shows:** In writing, the context comes first and the news comes at the end of the sentence, in the
stress position.

**Rule:** GUIDE.md rule 13.

### W7. The rhythm of the stress position

Credit: [Rosalind Reid, written reports, page 8](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).

**Description:** A slide with the title "how is writing different?" and one centered phrase. The part
"ba-da-" is blue, the color of context. The part "BUM" is dark red, the color of news.

```text
ba-da-BUM
```

**What it shows:** A written sentence builds up through the context and lands its weight on the last words.

**Rule:** GUIDE.md rule 13.

### W8. Topic position and stress position

Credit: [Rosalind Reid, written reports, page 9](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).

**Description:** Three bullets, each with a fragment of one sentence under it. The first two fragments are
blue, and the third is dark red.

```text
• Backward-linking old information appears in the topic (first) position.
  “In order to determine which algorithm to use,...

• The subject (person, thing or concept the story is about) also appears in the topic position.
  “our team...

• The new, emphasis-worthy information appears in the stress position.
  “... first conducted a literature search.”
```

**What it shows:** Put the old information and the subject first, and the new information last.

**Rule:** GUIDE.md rule 13.

### W9. Flow from one sentence to the next

Credit: [Rosalind Reid, written reports, page 10](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).

**Description:** The good version at the top, the poor version at the bottom, and the word "not" between
them in faint grey. A green brace under "first conducted a literature search. We" points to a note. In the
poor version, "We found..." is almost invisible, in white on the light background.

```text
In order to determine which algorithm to use, our team first conducted a literature search. We found...

flow: end of sentence introduces what follows

not

Our team first conducted a literature search in order to determine which algorithm to use. We found...
```

**What it shows:** End a sentence with the thing that the next sentence takes up, so that the text flows.

**Rule:** GUIDE.md rules 13 and 28.

## Instructions

### S10. Walk through a sequence in order

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 9, lines 86 to 92](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L86-L92).

```text
Before: The groups the features were sorted into were the authors' own
reading, the example posts were written by hand, and finer detail meant
training extra small models and labeling again.
After: First, the authors sorted the features into groups themselves, based on
their own reading of the outputs. Second, they wrote the example posts by
hand. Third, when they wanted finer detail, they trained another small
model, and they labeled the posts again.
```

**What it shows:** Turn a packed list of passive clauses into ordered steps, with a person as the subject of
each step.

**Rule:** GUIDE.md rule 15, and rule 9 for the active voice. The skill rule also lets a writer split the
steps with semicolons, and GUIDE.md rule 40 permits that too.

### S35. The words for a sequence

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 9, lines 84 to 85](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L84-L85).

```text
"First", "Second", "Third"
```

**What it shows:** Mark the steps of a sequence with ordinal words.

**Rule:** GUIDE.md rule 15.

### T2. Rough notes to turn into a paragraph

Credit: a task prompt in the eval of Shreya Shankar's plain-writing skill, [dataset.jsonl, line 37](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/evals/dataset.jsonl?plain=1#L37).

```text
Turn these rough notes into a clear paragraph:
- webhook retries every 5 minutes
- stops after 12 attempts
- dead-letters to SQS
- on-call gets paged if dead-letter depth > 100
- successful deliveries write a receipt with the partner request id
- ops can replay a dead-lettered event from the admin tool after fixing the destination
```

**What it shows:** Six facts about a sequence give practice with a topic sentence and an order, and the
repository gives no answer.

**Rule:** GUIDE.md rules 15 and 18.

## Paragraphs

### S11. A topic sentence, then support

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 10, lines 99 to 103](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L99-L103).

```text
Before: The parser skips files with no changes. The cache holds the previous
output. Most renders are fast.
After: Most renders are fast. For example, the parser skips files with no
changes, so the server returns early. Moreover, the cache keeps the previous
output, so a repeated render does no work.
```

**What it shows:** Put the main point first, then join each fact to it with "For example" or "Moreover" and
a reason.

**Rule:** GUIDE.md rule 18, which prefers "Also" to "Moreover".

### S36. The words that start more support

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 10, lines 97 to 98](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L97-L98).

```text
"For example", "Moreover", or "Or"
```

**What it shows:** Start a supporting sentence with a plain word that says how it relates.

**Rule:** GUIDE.md rule 18, which gives "For example", "Also" and "But".

## Long documents

More examples for the story of a report are in [the examples of nossaifd-talks](https://github.com/rahuldave/nossaifd-talks/blob/main/EXAMPLES.md), because
Rosalind Reid shows them on slides. They hold for a report too:

- **D10 to D14**, from "The story of a project presentation" to "A real description of the problem, in four
  slides", show the parts of the story, by GUIDE.md rules 20 to 26. They come from Rosalind Reid's tutorial deck.
- **D7, "One sentence spread over a series of slides"**, shows words, symbols and pictures, by GUIDE.md
  rule 29. It comes from Rosalind Reid's tutorial deck.
- **D21, "A slide of thanks"**, shows the credit to a team and to funders, by GUIDE.md rule 27. It comes
  from Rosalind Reid's tutorial deck.
- **P6, "The structure of a professional talk"**, shows the order of a talk, by GUIDE.md rule 20. It comes
  from Rosalind Reid's presentation tips.

### W1. The one-sentence story

Credit: [Rosalind Reid, written reports, page 2](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).

**Description:** A slide with one centered quotation between two short horizontal rules, on a light grey
background.

```text
“I’m going to tell you about a problem and how I solved it.”
```

**What it shows:** A report or a talk is the story of a problem, and of how the author solved it.

**Rule:** GUIDE.md rule 20.

### W2. The same story, in more detail, for a written report

Credit: [Rosalind Reid, written reports, page 3](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).

**Description:** The slide of W1 again, with four words added in green, "in much more detail".

```text
“I’m going to tell you about a problem and how I solved it in much more detail.”
```

**What it shows:** A written report tells the same story as a talk, with much more detail.

**Rule:** GUIDE.md rule 20, and the opening of the section "Long documents" of GUIDE.md.

### W3. The hourglass of story elements

Credit: [Rosalind Reid, written reports, page 4](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).

**Description:** On the left is a blue hourglass, wide at top and bottom and narrow in the middle. Its top
band is green. On the right are the heading and a list of five words. The first word is green, to match the
band.

```text
story elements

motivation
description
approach
learning
result
```

**What it shows:** A report has five parts in this order. It starts broad, narrows to the specific approach,
and widens again at the result.

**Rule:** GUIDE.md rules 20 and 21.

**The project now:** Every report starts with a summary before the motivation, by GUIDE.md rule 20.

### S17. Give the context in a status note

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 14, lines 155 to 159](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L155-L159).

```text
Before: The exporter now waits on the reset header, and `dotnet test` is
green.
After: The Okta System Log exporter was rereading whole hours, so a retry
could write the same event twice. It now waits using the response reset
header, and the six acceptance tests pass.
```

**What it shows:** Give the problem and its cause before the change, and replace "is green" with the count of
tests that pass.

**Rule:** No rule of GUIDE.md matches exactly. The closest is rule 23, which puts the problem before the
approach. The opening of the section "Long documents" also gives the order of a status note.

### W16. Credit for the source of the material

Credit: [Rosalind Reid, written reports, page 18](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).

**Description:** A slide that credits the source of the writing advice.

```text
thanks to:

Duke Scientific Writing Resource

http://cgi.duke.edu/web/sciwriting/index.php
```

**What it shows:** Name the source that the material comes from, with a link.

**Rule:** GUIDE.md rule 27.

### W14. A paragraph from a published paper, revised

Credit: [Rosalind Reid, written reports, page 16](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).

**Description:** The top left has a paragraph of context in grey. The top right has the citation of the paper
in a dark grey box. Below are the original paragraph on the left and the revision on the right. Blue marks
the parts that change. The revision on the slide has no final period.

```text
We have introduced a method to support fast rotation invariant search of large shape datasets with arbitrary representations and distance functions. Our method supports rotation limited queries and mirror image invariance if desired.

The VLDB Journal (2009) 18:611–630
Supporting exact indexing of arbitrarily rotated shapes and periodic time series under Euclidean and warping distance measures
Eamonn Keogh · LiWei · Xiaopeng Xi · Michail Vlachos · Sang-Hee Lee · Pavlos Protopapas

Future work includes both extensions and applications of the current work. We will attempt to extend this approach to the indexing of 3D shapes, and we have begun to use our algorithm as a subroutine in several data mining algorithms which attempt to cluster, classify and discover motifs in a variety of anthropological datasets, including petroglyph and projectile point databases.

We plan to extend and apply this approach, beginning with the indexing of 3D shapes. In addition, we have begun to use our algorithm as a subroutine in several data mining algorithms used in anthropology to cluster, classify and discover motifs in a variety of datasets, including petroglyphs and projectile points
```

**What it shows:** A real paragraph gets shorter and clearer when its actions go into verbs. A transition
joins its parts, and a repeated phrase goes.

**Rule:** GUIDE.md rules 9 and 28.

### W15. The same revision, with each change named

Credit: [Rosalind Reid, written reports, page 17](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).

**Description:** The original paragraph of W14 is on the left, with its first sentence highlighted in light
blue. Two green arrows lead to two revised parts on the right, each under a list of the changes. The first
revised sentence says "this work" here, and "this approach" on page 16.

```text
• active voice
• reduced nominalizations

We plan to extend and apply this work, beginning with the indexing of 3D shapes.

• inserted transition phrase
• removed repeated phrase “attempt to”

In addition, we have begun to use our algorithm as a subroutine in several data mining algorithms used in anthropology to cluster, classify and discover motifs in a variety of datasets, including petroglyphs and projectile points.
```

**What it shows:** Name each change in a revision, so that the writer can repeat the method on the next
paragraph.

**Rule:** GUIDE.md rules 9 and 28.

## Figures and equations

The examples for figures come from Rosalind Reid's slides for talks, so they are in
[the examples of nossaifd-talks](https://github.com/rahuldave/nossaifd-talks/blob/main/EXAMPLES.md). They hold for the figures of a report too:

- **D7, "One sentence spread over a series of slides"**, names words, symbols and pictures, by GUIDE.md
  rule 29. It comes from Rosalind Reid's tutorial deck.
- **D20, "The same findings, redrawn for a general audience"**, redraws a dense figure with plain labels, by
  GUIDE.md rule 30. It comes from Rosalind Reid's tutorial deck.
- **D27, "Two bad data graphics"**, shows a tangled network and bars in three dimensions, which GUIDE.md
  rule 30 forbids. It comes from Rosalind Reid's tutorial deck.
- **D28, "A good interactive graphic, and its plots"**, shows a graphic that says what to watch, by GUIDE.md
  rule 30. It comes from Rosalind Reid's tutorial deck.
- **P9, "Bad axis labels"**, names the faults of a plot from analysis software, by GUIDE.md rule 30. It
  comes from Rosalind Reid's presentation tips.

## Tone

### S7. A literal label

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 7, lines 67 to 68](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L67-L68).

```text
Before: Legal requirements as a floor.
After: Applicable legal constraints.
```

**What it shows:** A label names its subject, and does not use a figure of speech to sound memorable.

**Rule:** GUIDE.md rule 32. GUIDE.md rule 33 permits a metaphor in prose. Rule 32
still asks for a literal heading or label.

### S8. A literal heading

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 7, lines 69 to 70](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L69-L70).

```text
Before: # The alignment loop
After: # Iterative refinement using development disagreements
```

**What it shows:** A heading says what the section describes, even when the result is longer.

**Rule:** GUIDE.md rule 32.

### T1. Headings to rename

Credit: a task prompt in the eval of Shreya Shankar's plain-writing skill, [dataset.jsonl, line 29](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/evals/dataset.jsonl?plain=1#L29).

```text
Rename these section headings to be clearer if needed, and keep them usable in a docs page:
1. The Alignment Loop
2. Legal Requirements as a Floor
3. Unlocking Insight from Noise
```

**What it shows:** Rewrite three clever headings, the first two of which are the "Before" texts of S8 and S7.

**Rule:** GUIDE.md rules 32 and 42.

### S25. An analogy, and the literal structure

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 21, lines 225 to 228](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L225-L228).

```text
Before: The feature index is like a card catalog that the optimizer can flip
through.
After: The feature index is a list of named features. The optimizer can look
up which feature matches a request.
```

**What it shows:** The "After" describes the real structure in literal words.

**Rule:** GUIDE.md rule 33.

**The project now:** GUIDE.md rule 33 permits the analogy when it explains. So the project accepts the
"Before", followed by the "After" as its literal fact.

[The examples of nossaifd-talks](https://github.com/rahuldave/nossaifd-talks/blob/main/EXAMPLES.md) have more examples of analogy, metaphor and humor, from
Rosalind Reid's tutorial deck and presentation tips. They are D22, "An analogy in pictures, hands and their shadows",
D29, "A metaphor in a headline", D30, "A light line before the exercise", P1, "A metaphor for speech", and
P2, "A simile, quoted from Montgomery".

### S24. No fake agency

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 20, lines 219 to 220](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L219-L220).

```text
Before: The logs become searchable records, once the job finishes.
After: You can search the logs, once the job finishes.
```

**What it shows:** Make the reader the subject who acts, in place of a thing that changes by itself.

**Rule:** GUIDE.md rule 34.

### S41. Factual verbs for tools

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 20, lines 216 to 218](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L216-L218).

```text
"The API returns JSON", "The job writes the file", or "The paper argues"
```

**What it shows:** A tool or a document can be the subject of an ordinary verb of fact.

**Rule:** GUIDE.md rule 34, which says "A tool can return, write or read".

### S26. No negative parallelism

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 22, lines 234 to 235](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L234-L235).

```text
Before: It is not just a parser, it is a full toolchain.
After: It is a parser and a formatter.
```

**What it shows:** Name the parts of the thing, in place of the pattern "not just X, it is Y".

**Rule:** GUIDE.md rule 35.

### S27. Replace a quoted hype phrase with a fact

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 22, lines 236 to 238](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L236-L238).

```text
Before: We do not describe the API as "enterprise-grade robust," because
that phrase can mean different things.
After: The API has a 99.9% monthly uptime SLO.
```

**What it shows:** Answer a vague claim with the number that settles it.

**Rule:** GUIDE.md rules 35 and 11.

### T3. A customer's hype phrase

Credit: a task prompt in the eval of Shreya Shankar's plain-writing skill, [dataset.jsonl, line 40](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/evals/dataset.jsonl?plain=1#L40).

```text
Reply to a customer who asked whether your API "boasts enterprise-grade robustness" and wants a concrete uptime answer. Our SLO is 99.9% monthly.
```

**What it shows:** Answer "boasts enterprise-grade robustness" with the number 99.9%, as S27 does.

**Rule:** GUIDE.md rules 11 and 35.

### S28. Do not stack rhetorical questions

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 23, lines 243 to 246](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L243-L246).

```text
Before: Does the tool keep the writer's voice? Does it make the argument
stronger or weaker?
After: We do not yet know whether the tool keeps the writer's voice, or
whether it makes the argument stronger or weaker.
```

**What it shows:** State an open question as a fact about what is not known.

**Rule:** GUIDE.md rule 36.

**The project now:** GUIDE.md rule 36 permits rhetorical questions that the next sentences answer. The
"Before" fails only because nothing answers its questions.

### S29. No vague demonstratives

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 24, lines 252 to 253](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L252-L253).

```text
Before: That context carries into the next turn.
After: The agent applies the rules you saved on the next turn.
```

**What it shows:** Name the thing that "That" points to, and name who acts on it.

**Rule:** GUIDE.md rule 37, and rule 34 for the agency of "context". The skill forbids every demonstrative at
the start of a paragraph. Rule 37 forbids only a vague one at the start of a sentence.

### S42. The four demonstratives

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 24, lines 248 to 251](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L248-L251).

```text
"This", "That", "These", or "Those"
```

**What it shows:** These are the words that point back without naming.

**Rule:** GUIDE.md rule 37, with the narrower scope given at S29.

### S30. Do not open with a count

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 25, lines 259 to 262](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L259-L262).

```text
Before: Two cautions. First, the section can drift out of date. Second,
it can balloon if every item gets a sentence.
After: The section can drift out of date, because it duplicates facts
that live elsewhere. It can also balloon if every item gets a sentence.
```

**What it shows:** Start with the first point in place of a count, and add the reason.

**Rule:** GUIDE.md rule 38.

### S43. Openings that announce a count

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 25, lines 255 to 257](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L255-L257).

```text
"Two cautions." or "Three things to keep in mind."
```

**What it shows:** Avoid these two openings.

**Rule:** GUIDE.md rule 38.

## Punctuation and formatting

### S18. No dashes

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 15, lines 167 to 168](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L167-L168).

```text
Before: The build is fast — it finishes in 10 to 20 seconds.
After: The build is fast. It finishes in 10 to 20 seconds.
```

**What it shows:** Replace a dash between two clauses with a full stop, and write a range with "to".

**Rule:** GUIDE.md rule 39.

### S39. The middle dot

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 15, lines 165 to 166](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L165-L166).

```text
Do not use the middle dot (·) as a separator; use a comma, "and", or
separate lines instead.
```

**What it shows:** The rule names the separator to avoid and the three to use in its place.

**Rule:** GUIDE.md rule 39.

### S19. No colon between clauses

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 16, lines 175 to 176](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L175-L176).

```text
Before: Read for the schema: the feature fires.
After: Read for the schema. The feature fires.
```

**What it shows:** Replace a colon that joins two clauses with a full stop.

**Rule:** GUIDE.md rule 40. The rule permits a semicolon only between the steps of a sequence, and the
example is not a sequence.

### S20. A colon after a label is correct

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 16, lines 177 to 179](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L177-L179).

```text
Before (allowed in a PR or update): Summary: Replace em dashes in
generated docs.
After (same text is fine): Summary: Replace em dashes in
generated docs.
```

**What it shows:** Nothing changes in the pair, to show that a colon after a short label is correct.

**Rule:** GUIDE.md rule 40.

### S40. Labels that take a colon

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 16, lines 173 to 174](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L173-L174).

```text
"Summary:", "Changes:", or "Remaining work:"
```

**What it shows:** A short label in an update or a pull request takes a colon.

**Rule:** GUIDE.md rule 40, which gives "Summary:" and "Note:".

### S37. A short labeled line in a brief

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 12, lines 122 to 123](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L122-L123).

```text
"To do: validate recall on long queries."
```

**What it shows:** A short labeled line is correct in a brief.

**Rule:** GUIDE.md rule 7, which permits a label. Rule 40 also applies.

### S21. Straight quotes

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 17, lines 182 to 183](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L182-L183).

```text
Before: The system logs each “event” as it happens.
After: The system logs each "event" as it happens.
```

**What it shows:** Use straight quotes.

**Rule:** GUIDE.md rule 41.

### S22. Sentence case in headings

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 18, lines 187 to 188](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L187-L188).

```text
Before: ## How To Install The Skill
After: ## How to install the skill
```

**What it shows:** Write a heading in sentence case.

**Rule:** GUIDE.md rule 42.

### S23. A short list and nested groups

Credit: Shreya Shankar, plain-writing skill, [SKILL.md rule 19, lines 193 to 210](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L193-L210).

```text
Before: Shipped this week:
- dark mode
- an invite link fix
- a schema mismatch that blocked analytics export
- renderer cleanup
- copy edits
- a scored ranking model
- a p95 drop from 900 ms to 220 ms
- untested recall on long queries
After: Search ranking now uses a scored model, and p95 latency fell from
900 ms to 220 ms. The old heuristic path is still in the repo as a
fallback.
- Shipped
  - Dark mode
  - Invite link fix
- Still open
  - Test recall on long queries
  - Unblock analytics export
```

**What it shows:** Put the main news in a sentence, and sort the rest into a few groups with nested items.
The "Before" also puts items that did not ship under "Shipped".

**Rule:** GUIDE.md rule 44, and rule 47 for one structure in the items.

### E7. An engineering brief, with and without the skill (answers written by a model)

Credit: [evals/README.md, lines 279 to 289](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/evals/README.md?plain=1#L279-L289), in the eval of
Shreya Shankar's plain-writing skill. The first block is the prompt of the task. The model gpt-5.5 wrote the
two answers, and Shreya Shankar did not write them. The second block is the answer without the skill, and the
third is the answer with it. The README scores it 11 rules to the skill, 3 to the answer without it, and 11
ties.

```text
Write a short Slack brief for
engineering. Cover these facts: search
ranking moved from heuristics to a
scored model, p95 latency went from
900ms to 220ms, recall on long queries
is still untested, the old heuristic
path is still in the repo as a fallback,
dark mode shipped, the invite link bug
is fixed, analytics export is blocked on
a schema mismatch, the renderer got some
cleanup, and a few small copy edits
landed.
```

```text
Engineering brief:

- Search ranking has moved from
heuristics to a scored model.
- Search p95 latency improved from
~900ms to ~220ms.
- Recall on long queries is still
untested and needs validation.
- The old heuristic ranking path remains
in the repo as a fallback.
- Dark mode has shipped.
- The invite link bug is fixed.
- Analytics export is currently blocked
on a schema mismatch.
- Renderer cleanup landed.
- A few small copy edits also went out.
```

```text
Search ranking now uses a scored model
instead of heuristics, and p95 latency
fell from 900 ms to 220 ms. The old
heuristic path is still in the repo as a
fallback. To do: test recall on long
queries.

Shipped:
- Dark mode
- Invite link fix
- Renderer cleanup
- Small copy edits

Blocked:
- Analytics export is blocked on a
schema mismatch.
```

**What it shows:** Put the main news in sentences. Group the rest under labels such as "Shipped:" and
"Blocked:", in place of nine flat items.

**Rule:** GUIDE.md rules 44 and 47. The prompt has the same facts as S23.

## Short items read in bulk

### SP1. The order of noun, verb and noun

Credit: Shreya Shankar, post, [principle 1](https://fsdatalab.github.io/blog/agent-text-at-scale/#1-match-how-human-readers-parse-sentences), first and
second paragraphs.

```text
Good: "The agent fixed the login bug"
Bad:  "Login bug fixed by the agent"
```

**What it shows:** A reader takes the first noun as the actor. So a passive that starts with the object makes
the reader parse the sentence twice.

**Rule:** GUIDE.md rule 45, which uses this pair. Rule 9 covers the active voice.

### SP2. Session titles

Credit: Shreya Shankar, post, [figure 1](https://fsdatalab.github.io/blog/agent-text-at-scale/#figure-1), in
[principle 1](https://fsdatalab.github.io/blog/agent-text-at-scale/#1-match-how-human-readers-parse-sentences). The block gives the seven titles of the
figure, as written and as rewritten. The post says that the originals mix nouns, -ing forms and commands.

```text
As written                                   Rewritten
KV persistence across queries                Persisting KV across queries
vLLM performance on eviction queries         Measuring vLLM performance on eviction queries
Nemotron-3.5-Parse on OfficeQA benchmark     Running Nemotron-3.5-Parse on OfficeQA
Liquid 1.7B model integration                Integrating Liquid 1.7B model
Quail grant application strategy             Planning Quail grant application
Fine-tune model on personal writing          Fine-tuning model on personal writing
Switching to main and fast-forwarding        Switching to main and fast-forwarding
```

**What it shows:** When every item has the same subject, drop it. Start each item with a verb in one tense.
Here it is the -ing form, for a session in progress.

**Rule:** GUIDE.md rules 45 and 47.

**The project now:** GUIDE.md rule 9 permits the -ing form anywhere.

### SP3. Order emails

Credit: Shreya Shankar, post, [principle 2](https://fsdatalab.github.io/blog/agent-text-at-scale/#2-put-the-most-important-words-first) and
[figure 2](https://fsdatalab.github.io/blog/agent-text-at-scale/#figure-2). The text of the post gives one pair, and the figure gives four emails on each
side.

```text
Bad, status last:   "Your order #1001 has shipped."
Good, status first: Ordered: "Bounty Essentials..."

Status last                              Status first (Amazon)
Your order #1001 has been delivered      Delivered: "Bounty Essentials..."
Your order #1001 has shipped             Shipped: "Bounty Essentials..."
Your order #1002 has shipped             Shipped: "Desk lamp..."
Your order #1001 is confirmed            Ordered: "Bounty Essentials..."
```

**What it shows:** Put first the word that tells an item apart, here the status, or every subject starts
with the same words.

**Rule:** GUIDE.md rule 46, which uses its own form, "Shipped: the order 1001".

### SP4. Summaries with three openings (a bad list)

Credit: Shreya Shankar, post, [principle 3](https://fsdatalab.github.io/blog/agent-text-at-scale/#3-use-the-same-structure-and-the-same-vocabulary) and
[figure 3](https://fsdatalab.github.io/blog/agent-text-at-scale/#figure-3). The post shows the Notion AI summaries "without changes", in note 8. The block
gives the Summary column of the four rows. The highlights in the figure mark the openings.

```text
The issue reports that Claude Desktop Conversation experiences a long
(~70–90 s) initial prefill of ~17 K tokens, frequent HTTP 500 errors, and
cache loss on MLX versions 0.40.11–0.40.12, despite later messages being
faster.

The issue reports that ollama show --modelfile incorrectly wraps values
containing triple quotes followed by whitespace, causing unparseable
Modelfiles that fail to recreate the model.

The page reports an error reading GGUF metadata for a large MoE model in
MXFP4 format due to an oversized unsupported tensor, references a similar
bug, and includes a link to the related GitHub issue.

Pressing Ctrl +C while entering a """ multiline message in ollama run
clears the buffer but leaves the REPL in multiline mode, so the following
input is mistakenly treated as a continuation or system message.
```

**What it shows:** The items start in three ways, "The issue reports that", "The page reports" and an
action, and they call one thing an "issue" and a "page".

**Rule:** GUIDE.md rules 47 and 2. The en dashes in the ranges also break rule 39.

### SP5. Headlines with one structure (a good list)

Credit: Shreya Shankar, post, [principle 3](https://fsdatalab.github.io/blog/agent-text-at-scale/#3-use-the-same-structure-and-the-same-vocabulary) and
[figure 4](https://fsdatalab.github.io/blog/agent-text-at-scale/#figure-4). The block gives the four Perplexity Discover headlines of the figure.

```text
Brewers beat Rays in Game 5 for first World Series title
Bank of Canada hikes rate to 2.5%, first since July 2023
Weil Gotshal to wind down after partner exodus
HHS lets pharmacies make six unapproved peptides
```

**What it shows:** Each headline has a subject, a verb in the present tense and an object.

**Rule:** GUIDE.md rules 47 and 45.

### SP6. Theme cards from app reviews

Credit: Shreya Shankar, post, [principle 4](https://fsdatalab.github.io/blog/agent-text-at-scale/#4-use-variation-only-to-show-a-meaningful-difference)
and [figure 5](https://fsdatalab.github.io/blog/agent-text-at-scale/#figure-5). The first block holds 5 of the 11 bad cards. Claude's data analysis plugin
wrote them, and the post shows them "without changes", in note 12. The second block is the post's good
version. The post shows the count of reviews next to each title with no space, and the parentheses are added
here for reading.

```text
Fun, easy, and effective learning (74 reviews)
Most reviews praise Duolingo as fun, easy, and helpful for learning, often
in short 5-star notes. Users cite new vocabulary, pronunciation help,
self-paced lessons, and being able to talk with family or friends. Spanish
is the most named language, followed by Japanese, Italian, Korean, German,
and others. Several of these reviewers still raise a complaint, such as
energy limits or cost.

Chess, music, and math courses (12 reviews)
Chess is a popular new draw, and some users mention music, piano, and math
too. Feedback is mostly positive, but there are specific complaints: a
checkmate rule that seems wrong, no way for skilled players to skip ahead,
a distracting new owl voice and hard-to-see pieces in the chess puzzle, and
many clicks between games.

Bugs and technical problems (9 reviews)
Reports include voice answers not registering, the app freezing (one user
lost a streak), the app crashing on launch, finished lessons not counting,
leaderboard members disappearing, a new event missing for one family-plan
member, and a shared iPad starting a new learner at the wrong level. Most
come from the current version, 7.146.0.

Energy and battery limits on lessons (8 reviews)
The energy (battery) system, and the older hearts system, limits how much
users can practice. Users say they run out fast, must wait or watch ads,
and see it as a push to buy Super. Some reviews are in Russian and
Turkish, so the complaint shows up across markets. One user suggests
earning energy by doing chess, music, or math.

New language requests (3 reviews)
Users ask for new courses. Two ask for Icelandic, noting that Duolingo
already offers other Nordic languages, and one asks for Elvish from The
Lord of the Rings.
```

```text
Fun, easy, and effective learning (74 reviews)
Users love that the app is fun and helps them learn, e.g., new vocabulary and pronunciation.

Chess, music, and math courses (12 reviews)
Users enjoy the new courses but complain about problems, e.g., a checkmate rule that seems wrong.

Bugs and technical problems (9 reviews)
Users complain about bugs that cost them progress, e.g., a freeze that lost a daily streak.

Energy and battery limits on lessons (8 reviews)
Users complain that they run out of energy fast and must wait to keep practicing.

New language requests (3 reviews)
Users request new courses, e.g., Icelandic.

Reviews per theme (bar chart): 74, 12, 9, 8, 3
```

**What it shows:** Give every card the same parts. A detail on one card only, such as the version 7.146.0,
makes the reader ask what it means.

**Rule:** GUIDE.md rule 48, and rule 47 for one template. The good version uses "e.g.", which rule 4 permits.

### SP7. The verb of the chess card

Credit: Shreya Shankar, post, [principle 5](https://fsdatalab.github.io/blog/agent-text-at-scale/#5-align-the-connotation-of-verbs-with-the-purpose-of-the-dashboard),
which reuses [figure 5](https://fsdatalab.github.io/blog/agent-text-at-scale/#figure-5).

```text
Bad:  Chess is a popular new draw, and some users mention music, piano, and math too.
Good: Users enjoy the new courses but complain about problems, e.g., a checkmate rule that seems wrong.
```

**What it shows:** Start each card with a verb whose feeling shows praise or a problem. The bad card opens
with praise and then lists complaints.

**Rule:** GUIDE.md rule 49, which also permits the verbs with a strong feeling in prose.

### SP8. Verbs for two kinds of dashboard

Credit: Shreya Shankar, post, [principle 5](https://fsdatalab.github.io/blog/agent-text-at-scale/#5-align-the-connotation-of-verbs-with-the-purpose-of-the-dashboard),
first paragraph and the paragraph of the example.

```text
A dashboard of complaints: "complain", as in "Users complain"
A dashboard of praise:     "love", as in "Users love"
```

**What it shows:** Choose a negative verb for a list of complaints and a positive verb for a list of praise.

**Rule:** GUIDE.md rule 49, which uses these two verbs.

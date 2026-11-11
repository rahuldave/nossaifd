# Why the rules

The sources of this site do not always agree. This page lists each disagreement about documents, what each
source says, and what [the guide](../GUIDE.md) chose. [Sources and credit](sources.md) says who wrote each
source.

Most disagreements go away when you ask how a person takes in the text. A person takes it in one of
three ways:

- **Reading** a long document in order, such as a report or a README. The reader can go back.
- **Skimming** many short items, such as titles, list items, notifications or the rows of a dashboard.
  The reader sees the first two words of each item.
- **Listening** to a talk. The listener hears each sentence once. Rosalind Reid says that the listener sees
  each slide for less than a minute
  ([Rosalind Reid, tutorial deck, page 32](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).

A rule that is right for one way can be wrong for another. This page gives the choices for reading and
skimming. The choices for listening, such as slide titles, thanks and speaking time, are on
[the page "Why the rules" of nossaifd-talks](https://github.com/rahuldave/nossaifd-talks/blob/main/docs/why.md).

## Rosalind Reid before Shankar, and the story before a rule

The project's author set these two principles. Most of the choices below follow from them.

1. **Rosalind Reid's advice comes before Shankar's.** When the two disagree about the same kind of text,
   the guide follows Rosalind Reid. She edited *American Scientist* from 1992 to 2008, and she taught her
   tutorial at Harvard. Shankar's advice stays where Rosalind Reid gives none, such as for status notes,
   pull requests and short items read in bulk.
2. **A rule can give way to the story.** A writer can break a rule when the story needs it. For example,
   several questions in a row can build tension, and a story about a bug hunt can hold back the cause until
   the end. Think hard before you break a rule, and break it only for the story. Most rules on this site
   are preferences, and a few are hard limits.

## Choices that follow Rosalind Reid

| Question | What the sources say | The choice |
|---|---|---|
| Analogy, metaphor and humor | Rosalind Reid recommends them for written, visual and spoken work ([Rosalind Reid, tutorial deck, page 40](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)). Shankar's skill forbids analogy and metaphor ([rule 21](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L222)) | Use them in documents when they explain the work. State the literal fact in the next sentence, for a reader who is not a native speaker |
| The passive voice | Rosalind Reid says a mix of active and passive can help ([Rosalind Reid, written reports, page 15](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf)). ASD-STE100, from memory and not checked, asks for the active voice | Mix active and passive, as Rosalind Reid says. Choose the form that puts the known information first |

## Choices of the project's author

In these choices, Rosalind Reid's advice and Shankar's advice do not conflict, or no source gives an
answer.

| Question | What the sources say | The choice |
|---|---|---|
| Where does the new fact go in a sentence? | Rosalind Reid puts it last in a written sentence and first in a spoken one ([Rosalind Reid, written reports, pages 5 to 7](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf)). Shankar's post puts the words that set an item apart first ([principle 2](https://fsdatalab.github.io/blog/agent-text-at-scale/#2-put-the-most-important-words-first)) | Reading: last. Skimming: the words that set the item apart go first |
| Where does the result go? | Rosalind Reid ends a report and a talk with the result ([Rosalind Reid, tutorial deck, page 16](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)). Shankar's skill starts with the main conclusion for a busy reader | Every report starts with a summary, whatever its length. A report can be a blog post, and its style can be conversational. When the report is a story with a climax, the summary states the problem and gives the reader the puzzle, and not the climax. For example: "The build slowed from 4 minutes to 40 over one week, and the log of that week shows no commit to the build files. We tried three fixes, and each one failed." A teaser such as "Read on to see how we found the cause" is not a summary. Otherwise the summary states the result, as in "Threads make the build three times faster" |
| Contractions | Shankar's skill allows them. The guide forbids them for readers who are not native speakers | Not in a document |
| Rhetorical questions in a document | Shankar's skill forbids several in a row. An earlier version of the guide forbade every one | Allowed when the reader has the question. Answer it in full sentences, as the choices about the declaude skill below say |
| The length of a sentence | ASD-STE100, from memory and not checked, keeps an instruction to 20 words and a description to 25. Shankar's skill sets no limit | Usually 20 to 25 words at most, and never more than 40, which `check.py` fails. An occasional longer sentence is fine when its punctuation makes it clear |
| "e.g." and semicolons | Shankar's skill writes "e.g." before examples, and it allows a semicolon between the steps of a sequence. An earlier version of the guide forbade both | Follow Shankar's skill |
| Verbs with a strong feeling | Shankar's post asks for verbs such as "love" and "complain" in a dashboard | Allowed anywhere. Words that add force but no fact, such as "really", stay out |
| The -ing form | Shankar's post writes titles of work in progress with it. ASD-STE100, from memory and not checked, does not use it as a verb | Allowed. Prefer the simple form. At the end of a sentence, an -ing clause must add a fact, as the last row of the choices about the declaude skill says |
| Short items read in bulk | Shankar's post gives five principles for them | A section of the guide, rules 45 to 49 |
| A README | No source gives its order | A README starts with what the project does |

## Choices about the declaude skill

The declaude skill by Oskar Austegard gives rules 50 to 55 of the guide. In the places below, its
register and a rule of the guide disagreed, and the project's author chose in each place. Where the column "What the sources say" uses the past tense, it gives the
rule as it was before the choice. The column "The choice" names the rule that holds the choice now. [The declaude skill](declaude.md)
says where the skill comes from.

| Question | What the sources say | The choice |
|---|---|---|
| Bold at the start of a list item | Rule 43 bolded the first words of each item. [Oskar Austegard's register, entry 29](https://github.com/oaustegard/claude-skills/blob/6baa7290da972191749acda03c63297e67b3fc26/declauding/references/register.md?plain=1#L518) removes a bold label that repeats the item, and keeps a label that is a name | Bold a lead only when it is a name that the reader looks for, such as an option, a term or a case. Rule 43 |
| Bold elsewhere | Rule 43 bolds the name of a button. [Oskar Austegard's register, entry 30](https://github.com/oaustegard/claude-skills/blob/6baa7290da972191749acda03c63297e67b3fc26/declauding/references/register.md?plain=1#L539) bolds a term at its first use and nothing else | Keep rule 43. Bold what the reader must find on a screen, and never bold for emphasis |
| Rhetorical questions | Rule 36 allowed a question that the next sentences answer, and several in a row for the story. [Oskar Austegard's register, entry 10](https://github.com/oaustegard/claude-skills/blob/6baa7290da972191749acda03c63297e67b3fc26/declauding/references/register.md?plain=1#L201) removes a question that the writer answers, and a run of questions, except in a FAQ or an interview | Ask a question only when the reader has it, and answer it in full sentences. Never answer with a fragment. A run of questions only in a story. Rule 36 |
| A summary that holds back the cause | Rule 20 let the summary of a story hold back the climax, with the teaser "Read on to see how we found the cause". [Oskar Austegard's register, entry 8](https://github.com/oaustegard/claude-skills/blob/6baa7290da972191749acda03c63297e67b3fc26/declauding/references/register.md?plain=1#L175) calls suspense a technique of fiction, and [Oskar Austegard's register, entry 42](https://github.com/oaustegard/claude-skills/blob/6baa7290da972191749acda03c63297e67b3fc26/declauding/references/register.md?plain=1#L843) removes an opening that says content follows and names none of it | Keep suspense that gives the reader the puzzle and holds back the answer. Remove the teaser. Rule 20 |
| Nouns in a row | Rule 10 allowed three nouns, which it credited to ASD-STE100 (from memory and not checked). [Oskar Austegard's register, entry 53](https://github.com/oaustegard/claude-skills/blob/6baa7290da972191749acda03c63297e67b3fc26/declauding/references/register.md?plain=1#L1185) removes a stack of three or more, except a term of the field | Two nouns at most, except a standard term of the field or a name that the document defines. Rule 10 |
| A heading with an -ing form or an abstract noun | Rule 32 gave "Moving with edits" as a literal heading. Rule 45 gives "Measuring the latency" as a title. [Oskar Austegard's register, entry 41](https://github.com/oaustegard/claude-skills/blob/6baa7290da972191749acda03c63297e67b3fc26/declauding/references/register.md?plain=1#L816) removes a heading that names a topic area | When a section makes one point, its heading names the concrete thing. A label for a group of entries in a reference is correct. A title of a task in progress keeps its -ing form. Rules 32 and 45 |
| A thing as the subject of a verb | Rule 9 gives "The measurement showed a delay" as a correct sentence. [Oskar Austegard's register, entry 4](https://github.com/oaustegard/claude-skills/blob/6baa7290da972191749acda03c63297e67b3fc26/declauding/references/register.md?plain=1#L73) removes a verb that needs a mind, such as "hides", and keeps a pairing that readers know | Keep the pairings that readers know. Remove the verbs that need a mind. Rule 34 |
| A sample of the author's writing | The skill lets a sample of the author's writing win over every one of its rules, with dashes too. The guide has hard limits, such as no dashes and no contractions, for a reader who is not a native speaker | The hard limits of the guide win. A sample wins over the rest of the register |
| The words of a revision in the register | Some revisions in the register use contractions, dashes, words such as "just", a semicolon between clauses, or a fragment. Rules of the guide such as 5, 6, 7, 39 and 40 forbid them | Quote the register word for word. Where a revision breaks a rule, the example also gives a version by the guide |
| A count at the start | Rule 38 forbade every count at the start. [Oskar Austegard's register, entry 38](https://github.com/oaustegard/claude-skills/blob/6baa7290da972191749acda03c63297e67b3fc26/declauding/references/register.md?plain=1#L720) keeps a count in front of a real list | A count is correct in front of the list that it counts, when it also says what the items share or how they differ. A count alone, such as "Two cautions:", still fails `check.py`. Rule 38 |
| "It" or the noun | Rule 37 replaces a vague "This" with the noun. [Oskar Austegard's register, entry 40](https://github.com/oaustegard/claude-skills/blob/6baa7290da972191749acda03c63297e67b3fc26/declauding/references/register.md?plain=1#L788) replaces "That child" with "it" | Write "it" when only one thing could be meant, and the noun otherwise. Rule 37 |
| An -ing clause at the end of a sentence | Rule 9 allowed an -ing form anywhere. [Oskar Austegard's register, entry 25](https://github.com/oaustegard/claude-skills/blob/6baa7290da972191749acda03c63297e67b3fc26/declauding/references/register.md?plain=1#L419) removes a clause at the end that only claims importance, and moves a clause with a fact to its own sentence | Keep an -ing clause that adds a fact, in its sentence or in a sentence of its own. Remove one that only claims importance. Rules 9 and 51 |

## ASD-STE100 rules from memory

ASD-STE100, Simplified Technical English (STE), is a standard for the maintenance manuals of aircraft.
Issue 8 is the edition that the guide names, and [the sources](sources.md#asd-ste100-simplified-technical-english)
say more about it. No copy of the standard was available. Only its about page was read, and that page
confirms the purpose of STE and its rule of one word for one meaning. That rule is rule 2 of the guide.

Every other part of the guide that names STE comes from memory of the standard, and none of it is
checked. The list gives each such part:

- rule 1, the few word swaps from the dictionary of STE
- rule 8, a limit of 25 words for a description
- rule 9, the active voice in procedures, and no -ing form as a verb
- rule 10, three nouns in a row at most
- rule 14, an instruction as a command
- rule 15, one instruction in one sentence
- rule 16, a condition first, and a limit of 20 words for an instruction
- rule 17, a warning that starts with a short command
- rule 19, six sentences in a paragraph at most

The guide does not always do what these parts say. It keeps the active voice, the limits of 20 and 25
words, and the rule against the -ing form as a verb as preferences. It makes six sentences in a paragraph
a hard limit of its own, which `check.py` enforces. It allows two nouns in a row, from Oskar Austegard's
declaude skill, and not three.

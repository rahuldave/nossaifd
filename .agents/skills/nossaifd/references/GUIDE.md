# Not so shitty AI first drafts

A writing guide for documentation, READMEs and other prose that an AI model writes and a person reads. It
joins four sources:

- **ASD-STE100, Simplified Technical English.** Aerospace manuals use it, so that readers who are not
  native English speakers understand them.
- **The plain-writing skill by Shreya Shankar.** It keeps prose plain and free of the habits of AI writing.
- **"Communicating Your Work", a tutorial by Rosalind Reid**, in two slide decks, the written reports and
  the tutorial deck. Rosalind Reid's decks give the order of a long document, several rules for sentences,
  and the rules for figures.
- **"Five Principles for Generating Readable AI Text in Bulk", a post by Shreya Shankar.** It gives the
  rules for short items that a person skims, such as titles and notifications.

Each rule names its source and links to the place in it. A rule that comes from no source is this guide's
own, and it says so. The section "Sources" lists each place where this guide differs from a source.

Give this file to the model with the task, together with a glossary of the project's terms. Then run
`check.py` on the result, and read the result yourself.

## Markdown comes first

The rules apply to the prose of a page, which is its paragraphs, list items, headings and image captions.
Markdown syntax always wins over a rule. The rules do not apply to these constructs:

- **Fenced code blocks and inline code.** Commands, code, file names and program output stay exactly as
  they are, with their own punctuation.
- **Tables.** A table cell can be a short phrase, a fragment or a value. Write the prose around the table
  by the rules.
- **Link targets, URLs and image paths.** The text of a link follows the rules, but its target does not.
- **Quoted examples.** Words in straight double quotes are words that the text talks about. They keep their
  own form, as in the list of words to avoid.
- **Front matter, HTML and comments.** Metadata at the top of a file, and HTML tags, keep their own syntax.

A rule about colons, dashes or quotes never applies to a character inside one of these constructs. The
section is this guide's own.

## Words

1. **Use simple, everyday words.** Choose the plain word when a longer word means the same thing:

   | Write | Not |
   |---|---|
   | use | utilize |
   | let | allow, enable |
   | make sure | ensure |
   | give | provide |
   | start | launch |
   | about | approximately |
   | through | via |
   | before | prior to |

   From: [Shankar's skill, rule 1](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L26),
   and the dictionary of [STE](https://www.asd-ste100.org/about.html).
2. **Use one term for one thing.** Keep a glossary of the project's terms, and use each term the same way
   every time. Do not change to a synonym for variety. A word keeps one meaning in the whole document.

   From: [STE, "one word, one meaning"](https://www.asd-ste100.org/about.html), and
   [Shankar's skill, rule 4](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L47).
3. **Define jargon the first time it appears on a page.** Use a technical term only when it is the most
   precise word, and say in plain words what it means. Do not invent jargon, and do not invent a
   hyphenated adjective that no dictionary has.

   From: Shankar's skill, [rule 2](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L32)
   and [rule 6](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L56).
4. **Write "for example".** Do not write "e.g.", "i.e." or "etc.". If a list is not complete, say so in
   words. The rule is this guide's own. Shankar's skill writes "e.g.", so this guide changes it.
5. **Do not add empty emphasis.** Remove a word that adds force but no fact. Examples are "really",
   "simply", "just", "actually", "crucial", "pivotal", "robust", "seamless", "powerful" and "matters". Also
   avoid the words that AI writing overuses, for example "delve", "leverage", "landscape", "tapestry",
   "unlock", "elevate" and "empower".

   From: Shankar's skill, [rule 1](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L26)
   and [rule 3](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L40).
6. **Do not use contractions in documentation.** Write "do not" and "it is". A reader who is not a native
   speaker reads the full form more easily. The rule is this guide's own. Shankar's skill allows
   contractions, so this guide changes it.

## Sentences

7. **Write complete sentences.** Each sentence has a subject and a verb. Do not write fragments, except in
   a table cell, a short list item or a label.

   From: [Shankar's skill, rule 8](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L74).
8. **Keep a sentence to 25 words or fewer, and to one or two clauses.** If a sentence needs three clauses,
   make two sentences, or use a list. But do not cut one thought into a stack of short sentences. Join two
   related clauses with "and", "but", "because" or "so".

   From: the writing rules of [STE](https://www.asd-ste100.org/about.html) for the 25 words, and Shankar's
   skill, [rule 11](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L105)
   and [rule 12](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L118).
9. **Prefer the active voice and simple verb forms, and put each action in a verb.** Write "the server
   reads the file" and not "the file is read by the server". Write "runs" and not "is running". Write "we
   measured the latency" and not "a measurement of the latency was made". A passive, an -ing form or a
   noun for an action is not wrong when it does a job:
   - A passive is correct when it puts the known information first, as rule 13 asks. It is also correct
     when the actor is unknown.
   - A noun for an action is correct when it names the action of the sentence before, as in "The
     measurement showed a delay".
   - An -ing form is correct only when the simple form is unclear.

   From: the writing rules of [STE](https://www.asd-ste100.org/about.html), and Rosalind Reid, written
   reports, [pages 13 and 14](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf)
   for actions in verbs and [page 15](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf)
   for the voice. The passive for an unknown actor is this guide's own.
10. **Put not more than three nouns in a row.** Break a longer group with "of", "for" or "in". Write "the
    size of the terminal font" and not "the terminal font size setting".

    From: the writing rules of [STE](https://www.asd-ste100.org/about.html).
11. **Say exactly what happens.** Name who or what does the action, and by what means. Remove side clauses
    that add no fact, for example "as we move forward" or "for the time being".

    From: [Shankar's skill, rule 13](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L136).
12. **Put the verb close to its subject.** A reader holds the subject in mind until the verb comes. Do not
    put a long phrase between them. Write "The backup script stops when the disk is full or the network
    drops." Do not write "The backup script, when the disk is full or the network drops, stops."

    From: [Rosalind Reid, written reports, page 12](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).
13. **Put the known information first and the new information last.** Start a sentence with what the
    reader already knows, for example the subject or a link to the sentence before. End it with the new
    fact. Rosalind Reid calls the end of a sentence the "stress position". The reason that a reader gives
    the end the most weight is this guide's own. The new fact at the end then leads into the next
    sentence. Write "The build failed on Monday. The cause of the failure was an expired certificate." Do
    not write "An expired certificate was the cause of the failure of the build on Monday."

    The rule is for prose that a person reads in order. Two other kinds of text differ. A speaker often
    gives the news first and the context after it, as Rosalind Reid shows. A short item in a list starts
    with the words that make it different, by rule 46.

    From: Rosalind Reid, written reports, [pages 6 and 7](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf)
    and [pages 9 to 11](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).

## Instructions

14. **Write an instruction as a command.** Write "Open the file" and not "You should open the file" or "The
    file can be opened".

    From: the writing rules of [STE](https://www.asd-ste100.org/about.html).
15. **Give one instruction in one sentence, in the order the reader does it.** Use a numbered list, or
    "First", "Second" and "Third", for a sequence. Two actions that happen at the same time can share a
    sentence.

    From: the writing rules of [STE](https://www.asd-ste100.org/about.html), and
    [Shankar's skill, rule 9](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L83).
16. **Put a condition first.** Write "If the test fails, read the log" and not "Read the log if the test
    fails". An instruction has 20 words or fewer.

    From: the writing rules of [STE](https://www.asd-ste100.org/about.html).
17. **Start a warning with a short command, then give the reason.** Write "Do not put the address on a
    slide. Anyone with the address can run commands as you."

    From: the writing rules of [STE](https://www.asd-ste100.org/about.html).

## Paragraphs

18. **Start each paragraph with a topic sentence.** Then give support, with a fact or an example. Start
    more support with a plain word, for example "For example", "Also" or "But".

    From: [Shankar's skill, rule 10](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L94).
19. **Keep a paragraph to six sentences or fewer.** Do not give three or more examples in a row for the
    same point.

    From: the writing rules of [STE](https://www.asd-ste100.org/about.html) for the six sentences, and
    [Shankar's skill, rule 11](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L105)
    for the examples.

## Long documents

These rules are for a document that a reader takes in whole and in order, for example a report, a
proposal or a design document. They come from the tutorial by Rosalind Reid. Her written reports say that
a report tells the same story as a talk, with more detail. So this guide takes the parts of the story from
her tutorial deck. A rule that adds advice of this guide's own says so.

Some documents have another order:

- **A README** starts with what the project does. Then it says how to start. The motivation comes after
  that, if at all.
- **A status note, a pull request and a summary** start with the result, and then give the background.
  [Shankar's skill](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L270)
  gives the order for a busy reader.
- **A reference page**, such as a list of options, follows the order in which a reader looks things up.

The order of a README is this guide's own. It is not Rosalind Reid's.

20. **Tell the story of a problem and how it was solved.** Give the document these parts, in this order:
    - **Summary.** In a long report, a few sentences that state the result. The summary is this guide's
      own rule, and not Rosalind Reid's.
    - **Motivation.** Why the reader should care about the work.
    - **Description.** The problem in detail, and how the work broke it into parts.
    - **Approach.** What was done, and why.
    - **Learning.** What the work showed, and what did not work.
    - **Result.** The conclusion, what it means and what follows from it.

    The parts can be sections, or paragraphs in a short document. The start and the end are general, and the
    middle is specific. Rosalind Reid draws this shape as an hourglass
    ([Rosalind Reid, tutorial deck, page 16](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf),
    and [Rosalind Reid, written reports, page 4](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf)).

    From: Rosalind Reid, tutorial deck, [pages 15 and 16](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf),
    and written reports, [pages 2 to 4](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).
21. **Start with the motivation for this reader.** Say what larger problem the work is part of, what the
    reader gains from it, and what it gives other people. Start with why the work was necessary.

    From: [Rosalind Reid, tutorial deck, pages 17 and 18](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf).
    This guide adds a warning of its own. Do not start with the history of the project or with the method.
    An AI model often starts a draft with what it built.
22. **Choose the motivation, the technical level and the content for the reader.** Name the reader before
    you write, for example a manager who decides or an engineer who maintains the code. Every reader that
    the document is for must be able to follow it.

    From: Rosalind Reid, tutorial deck, [page 19](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf),
    and written reports, [page 22](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).
    This guide adds that two different readers can need two different documents.
23. **Describe the problem before the approach.** Give the technical background and the practical reason
    that the problem is important. Then give the earlier work and the solution that the work tests. A
    reader who does not know the problem cannot judge the solution.

    From: [Rosalind Reid, tutorial deck, pages 21 and 22](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf).
24. **Give the approach the most care, and keep only what supports its main points.** The approach is the
    most important part of the story. Write an outline of the main points before you write the text. Then
    remove each detail that does not support one of them.

    From: [Rosalind Reid, tutorial deck, pages 24 and 25](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf).
    This guide adds that the approach usually needs the most space.
25. **Report what did not work.** Say what the work showed, what failed and what the failure taught. A
    report that gives only the successes hides what the next person needs to know.

    From: [Rosalind Reid, tutorial deck, page 36](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf).
26. **End with the result and what it means.** State the conclusion, what it means and what follows from
    it.

    From: [Rosalind Reid, tutorial deck, page 38](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf).
    This guide adds that the result also states its limits.
27. **Credit the people and the sources.** Name the people who helped with the work, and the earlier work
    that the document uses.

    From: [Rosalind Reid, tutorial deck, page 39](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf).
28. **Revise the draft for flow.** Read the draft as the reader reads it. Join related sentences with a
    plain word, for example "Also" or "In addition". Remove a phrase that repeats, and each word that adds
    no fact.

    From: Rosalind Reid, written reports, [page 11](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf)
    and [pages 16 and 17](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).

## Figures and equations

The rules in this section also come from Rosalind Reid.

29. **Use words, pictures and equations each for its own work.** Words explain, and connect the parts of
    the argument. A picture shows a pattern, a structure or a method. An equation gives the exact form of a
    relation to a technical reader.

    From: [Rosalind Reid, written reports, pages 19 to 21](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).
30. **Explain every figure in the text.** Say what the figure shows, and what the reader must see in it.
    Label its parts in plain words. Make a data figure lead the reader to the important result, and remove
    what does not help. Do not draw every link of a large network when a simple plot shows the result.
    Do not draw bars in three dimensions.

    From: Rosalind Reid, written reports, [page 19](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf),
    and tutorial deck, [page 30](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf),
    [pages 51 to 54](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)
    and [page 59](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf).
31. **Explain every equation in words.** Say what each symbol means and what the equation says. A reader
    who skips the equation must still follow the argument.

    From: Rosalind Reid, tutorial deck, [page 30](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf),
    and written reports, [page 21](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).
    The last sentence of the rule is this guide's own.

## Tone

32. **Keep the writing boring, literal and descriptive.** Do not write a catchy heading, a slogan or a
    clever label. A heading says what the section is about, for example "Moving with edits" and not "The
    point of no return".

    From: [Shankar's skill, rule 7](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L63).
33. **Do not use analogies or metaphors.** Describe the real thing in literal words.

    From: [Shankar's skill, rule 21](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L222).
    Rosalind Reid recommends analogy, metaphor and humor. The section "Sources" says why this guide does not.
34. **Do not give objects fake agency.** A tool can return, write or read. But do not write as if a system
    decides or intends something, when a person or a process is the real actor.

    From: [Shankar's skill, rule 20](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L214).
35. **State what a thing is.** Do not write "not just X, but Y" or "not only X, it is Y".

    From: [Shankar's skill, rule 22](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L230).
36. **Do not ask rhetorical questions.** State the problem.

    From: [Shankar's skill, rule 23](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L240),
    which forbids two or more in a row. This guide forbids every rhetorical question.
37. **Do not start a sentence with a vague "This", "That", "These" or "Those".** Name the thing. Write "The
    flag lets a move discard edits" and not "This lets a move discard edits".

    From: [Shankar's skill, rule 24](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L248).
38. **Do not open with a count.** Do not write "Three things to know." State the first thing. If there are
    many things, use a list.

    From: [Shankar's skill, rule 25](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L255).

## Punctuation and formatting

39. **Do not use dashes or middle dots.** Do not use an em dash or an en dash, and do not use the middle
    dot as a separator. Write a range with "to", as in "10 to 20 seconds".

    From: [Shankar's skill, rule 15](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L163).
40. **Do not join two clauses with a colon or a semicolon in prose.** Write two sentences. A colon is
    correct before a list, and after a short label such as "Summary:" or "Note:".

    From: Shankar's skill, [rule 8](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L74)
    and [rule 16](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L170).
    Shankar's rule 9 allows a semicolon between the steps of a sequence, and this guide does not.
41. **Use straight quotes**, " and ', not curly quotes.

    From: [Shankar's skill, rule 17](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L181).
42. **Use sentence case in headings.** Write "How to install the tool" and not "How To Install The Tool".

    From: [Shankar's skill, rule 18](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L185).
43. **Use bold to set one thing off from the next.** Bold the first words of a list item or a paragraph, so
    the reader can scan the items. Bold the names of things the reader must find on a screen, for example
    a button. Do not use bold for emphasis in the middle of a sentence.

    From: [Shankar's skill, rule 18](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L185),
    which forbids bold for decoration. The two uses of bold are this guide's own.
44. **Use lists and tables where they help, and not more.** In prose, keep a list to about four items, and
    nest the items if there are more. On a reference page, a table is the clearest form for options,
    commands and keys.

    From: [Shankar's skill, rule 19](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L190).
    The advice on a reference page is this guide's own.

## Short items read in bulk

These rules are for many short items that a person skims, for example titles, headings, list items,
notifications, table cells and rows in a dashboard. A reader of such a list often reads only the first two
words of each item. The other rules of this guide still hold, except where a rule below replaces one of
them. The rules come from the post by Shreya Shankar, and this guide states them in its own words.

45. **Start each item with its subject or its verb.** A reader takes the first noun as the actor and the
    next verb as the action. Write "The agent fixed the login bug" and not "Login bug fixed by the agent".
    If every item has the same subject, leave it out and start with the verb. Put the verb in the tense
    that the reader expects. For the title of work in progress, the -ing form is correct, as in "Measuring
    the latency". Rule 9 still holds in prose.

    From: [Shankar's post, principle 1](https://fsdatalab.github.io/blog/agent-text-at-scale/#1-match-how-human-readers-parse-sentences).
46. **Put first the words that make an item different.** Find the words that tell the item apart from the
    other items, and move them to the start. Write "Shipped: the order 1001" and not "Your order 1001 has
    shipped". In an item, the rule takes the place of rule 13.

    From: [Shankar's post, principle 2](https://fsdatalab.github.io/blog/agent-text-at-scale/#2-put-the-most-important-words-first).
47. **Give every item the same structure and the same words.** Use one pattern in all the items, for
    example a subject, a verb in the present tense and an object. Use one word for each thing in all the
    items, as rule 2 says.

    From: [Shankar's post, principle 3](https://fsdatalab.github.io/blog/agent-text-at-scale/#3-use-the-same-structure-and-the-same-vocabulary).
48. **Make an item different only when the difference means something.** A reader thinks that a difference
    in length, structure or words carries a meaning. If one item names a version number, the reader asks
    why the other items do not. Give each item the same parts. Put the extra detail where the reader can
    open it.

    From: [Shankar's post, principle 4](https://fsdatalab.github.io/blog/agent-text-at-scale/#4-use-variation-only-to-show-a-meaningful-difference).
49. **Choose verbs whose feeling shows the purpose of the list.** In a list of complaints, write "Users
    complain that the app freezes". In a list of praise, write "Users love the new course". Rule 5 still
    holds. In an item that reports how people feel, the feeling is the fact.

    From: [Shankar's post, principle 5](https://fsdatalab.github.io/blog/agent-text-at-scale/#5-align-the-connotation-of-verbs-with-the-purpose-of-the-dashboard).

## Check the result

`check.py` measures the rules that a program can measure:

```
uv run --no-project python check.py page.md [page.md ...]   # hard problems fail the check
uv run --no-project python check.py -v page.md              # also show the soft notes, for a person to judge
```

The hard checks find these problems:

- a sentence or a paragraph that is too long
- a contraction, a dash, a middle dot or a curly quote
- a colon between two clauses
- an abbreviation such as "e.g.", or a "not just" construction
- a count at the start of a paragraph, a vague "This is", or two questions in a row

The soft notes are for a person to judge. They show -ing forms, possible passives, nouns that name an
action, semicolons, sentences that may have three clauses, and words with a simpler alternative.

The program cannot judge meaning, tone or a missing definition. Read every page after it passes.

## Sources

- **ASD-STE100, Simplified Technical English**, Issue 8, at https://www.asd-ste100.org/about.html. The
  AeroSpace and Defence Industries Association of Europe (ASD) owns it. Aircraft makers write their
  maintenance manuals in it, so that readers who are not native English speakers understand them. Andrej
  Karpathy suggested on X that the same rules suit text that AI models write. The rules for words,
  sentences, instructions and paragraphs come from it. Only the about page is public. It confirms the
  purpose of STE and its rule of one word for one meaning. No copy of the writing rules was available to
  check the other rules that this guide gives to STE. Its dictionary of approved words is not part of this
  guide.
- **The plain-writing skill by Shreya Shankar**,
  https://github.com/docwriter-org/plain-writing-skill, at commit f0d3630, under the MIT licence, copyright
  (c) 2026 Shreya Shankar. The rules for tone, punctuation and the patterns of AI writing come from it,
  and several rules for words and sentences. This guide states the rules in its own words. It changes five
  of them:
  - Rule 6 forbids contractions in documentation. Shankar's rule 5 allows them.
  - Rule 4 forbids "e.g.". Shankar's rule 11 writes "e.g." before examples in a sentence.
  - Rule 8 keeps a sentence to 25 words. Shankar's rule 12 prefers long sentences. Both rules forbid a
    stack of short sentences.
  - Rule 36 forbids every rhetorical question. Shankar's rule 23 forbids two or more in a row.
  - Rule 40 forbids a semicolon in prose. Shankar's rule 9 allows one between the steps of a sequence.
- **"Five Principles for Generating Readable AI Text in Bulk", a post by Shreya Shankar**, 29 October
  2026, at https://fsdatalab.github.io/blog/agent-text-at-scale/. Rules 45 to 49 come from its five
  principles. The post shows them on lists of titles, emails, summaries and dashboards. Rule 49 keeps the
  verbs with a strong feeling to short items, and rule 5 still holds in prose.
- **"Communicating Your Work", a tutorial by Rosalind Reid**, which she taught in the course AC297r at the
  Institute for Applied Computational Science at Harvard in March 2015. Rosalind Reid was the editor of
  American Scientist magazine from 1992 to 2008. She gave permission to use her material, on the
  condition that this guide credits her wherever it uses her work. This guide gives her advice in its own
  words, and it names her in each rule that uses it. Text that comes from her work must keep its credit to
  Rosalind Reid, in every copy and in every changed version of this guide. The MIT licence of this
  repository does not remove that condition. Her PDFs are her own work, and they are not under the MIT
  licence. The tutorial has two decks:
  - [Written reports](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf),
    23 pages. It gives the rules for sentences on pages 5 to 17, and the work of words, pictures and
    symbols on pages 19 to 21. On page 18 she thanks the Duke Scientific Writing Resource.
  - [Tutorial deck](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf),
    59 pages, 25 March 2015. It gives the parts of the story on pages 15 to 39, and advice on figures on
    pages 30, 31 and 51 to 54.

  Rules 9, 12, 13 and 20 to 31 use her work. This guide differs from her in three places:
  - **Analogy, metaphor and humor.** Rosalind Reid recommends analogy, an informal style, metaphor and
    humor for written, visual and spoken work. She gives them on pages 40 to 57 of the tutorial deck, and
    on pages 19 and 20 of the written reports. Rules 32 and 33 keep a document literal. A literal
    sentence is easier for a reader who is not a native speaker. Also, an AI model often writes a metaphor
    that adds no fact.
  - **The place of the result.** Her story ends with the result. This guide starts a README with what the
    project does, and a long report with a short summary of the result.
  - **The voice.** She prefers the active voice, and she says that a mix of active and passive sentences
    can help. Rule 9 also prefers the active voice. It allows a passive that puts the known information
    first.

# Talks and slides

A guide for talks, slide decks and talk scripts that an AI model writes and a person gives. It is the companion
of [GUIDE.md](https://github.com/rahuldave/nossaifd/blob/main/GUIDE.md), which is for documents that a person
reads.

Most rules come from Rosalind Reid, the editor of American Scientist from 1992 to 2008. She taught the tutorial
"Communicating Your Work" in the course AC297r at the Institute for Applied Computational Science at Harvard in
March 2015. Her presentation tips for the tutorial draw mostly on a book by Scott Montgomery, The Chicago Guide
to Communicating Science. The rules for slide titles come from a post by Shreya Shankar.

The section "Sources" names each source. This guide uses Rosalind Reid's material with her permission, and it
credits her at each rule that comes from her. Text that comes from her work must keep its credit to Rosalind
Reid, in every copy and in every changed version of this guide. The MIT licence of this repository does not
remove that condition. Her PDFs are her own work, and they are not under the MIT licence.

A link to her work names the file and the page, for example
[Rosalind Reid, tutorial deck, page 27](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf).
The "tutorial deck" is her 59 slides on talks. The "presentation tips" are her five pages, "Some thoughts about
presentations". The "written reports" are her 23 slides on reports. A rule that no source gives is marked as
this guide's own rule.

Give this file to the model with the task. Then run `check_talk.py` on the deck, and read the deck yourself.

## A talk is not a document

A listener hears each sentence once, at the pace of the speaker, and cannot turn back a page. Rosalind Reid
says that the listener sees each slide for less than a minute
([Rosalind Reid, tutorial deck, page 32](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
She also says that "the presentation is not the paper"
([Rosalind Reid, tutorial deck, page 25](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)
and [page 32](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
Her presentation tips, after Montgomery, say that listening and reading are different
([Rosalind Reid, presentation tips, page 1](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).

So the slides support the speaker. They do not replace the speaker, and they are not a paper. The rules of
GUIDE.md apply to the words of a talk, with the exceptions in the section "The words of the script".

## Find out about the talk first

These rules come from Rosalind Reid's presentation tips, which follow Montgomery.

1. **Ask about the audience and the occasion.** Find out who will listen, what the meeting is for, and what
   part the talk plays in it. Without these facts, a speaker can give a fine talk that is wrong for the
   occasion ([Rosalind Reid, presentation tips, page 5](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
2. **Ask about the time and the questions.** Ask how many minutes the talk has, and when the audience can ask
   questions. The time can change on the day
   ([Rosalind Reid, presentation tips, page 1](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
3. **Ask about the room.** A dark room changes the choice of background
   ([Rosalind Reid, presentation tips, page 3](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
4. **Ask if the slides go online.** A posted version can carry more words than the slides on the screen
   ([Rosalind Reid, presentation tips, page 2](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).

If the person cannot answer a question, write your assumption at the top of the plan.

## Fit the talk to its audience

A talk is for its audience, and not for the speaker. Rosalind Reid's presentation tips warn against a talk that the
speaker seems to give to himself or herself
([Rosalind Reid, presentation tips, page 3](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).

5. **Choose the motivation, the technical level and the content for each audience**
   ([Rosalind Reid, tutorial deck, page 19](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
6. **Revise every slide for each new audience.** Reid calls this rule the cardinal rule. An audience can
   tell when a talk was made for somebody else. Check the small things. A symbol on an axis can be new to
   this audience
   ([Rosalind Reid, presentation tips, page 4](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
7. **Adjust the talk more as the audience gets further from the speaker's field.** Rosalind Reid and a
   colleague named McCormick give this advice
   ([Rosalind Reid, presentation tips, page 4](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
   The further away the audience is:
   - **The more it needs explanation.** Add slides that teach the background, at the start and where a new
     idea begins.
   - **The fewer symbols it can follow.** Take out equations. Replace each term or unit that these listeners
     may not know.
   - **The more time it needs.** Slow down, and stop after a hard idea.
   - **The more the speaker's interest counts.** Show it, and drop the jargon. A broad academic audience
     needs about what a class of undergraduates needs. Rehearse in front of somebody from another
     department.
8. **Ask for honest feedback** from each new kind of audience. Use it in the next talk
   ([Rosalind Reid, presentation tips, page 4](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).

For an agent, write the audience, the occasion and the time at the top of the plan. If you reuse a deck, go
through each slide for the new audience. For a general audience, list each technical term in the script, and
define it or remove it.

## The story

Rosalind Reid teaches that a project talk is the story of how the speaker solved a problem
([Rosalind Reid, tutorial deck, page 15](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
She gives the story five parts, in this order, and she draws them beside an hourglass
([Rosalind Reid, tutorial deck, page 16](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).

9. **Motivation.** Give this listener a reason to pay attention. Start from the larger problem that the work
   belongs to. Then say what the listener can take from the work, and what other people gain from it
   ([Rosalind Reid, tutorial deck, pages 17 and 18](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
10. **Description.** Lay out the problem in detail, and the parts that you split it into. Say what a listener
    must know to follow it, and why solving it is useful. Then say what other people tried, and which idea the
    work puts to the test ([Rosalind Reid, tutorial deck, pages 21 and 22](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
11. **Approach.** Explain the method, and give the reason for each choice in it. Rosalind Reid ranks this part
    above the others. Make an outline first, so that the key points stand out. Then cut each detail that the
    key points do not need, and state the rest plainly
    ([Rosalind Reid, tutorial deck, pages 24 and 25](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
    Give the approach the most care. The sources give no share of the time for it.
12. **Learning.** Tell the listener what the work taught you, and include the attempts that failed
    ([Rosalind Reid, tutorial deck, page 36](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
13. **Result.** State the conclusion, discuss it, and say what it changes for the listener or for the field
    ([Rosalind Reid, tutorial deck, page 38](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).

Montgomery gives a shorter form of the same structure for a professional talk. Say why you did the work, how
you did it, what you found and what it means
([Rosalind Reid, presentation tips, pages 1 and 2](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).

14. **Choose the points that the story needs.** A talk cannot settle every question, and the paper can hold
    the rest ([Rosalind Reid, tutorial deck, page 25](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
15. **Trim the detail in the middle.** The middle is the core of a talk. But many talks pack so much detail
    into the middle that they never reach the end
    ([Rosalind Reid, presentation tips, page 2](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
16. **Use the opening to settle the audience.** People need time to sit down. In a professional talk, thank
    the hosts and the organizers at the start
    ([Rosalind Reid, presentation tips, page 2](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
    Keep the thanks brief, which is this guide's own advice.
17. **Keep the outline short, and repeat its terms.** Use the same terms later, when each topic comes
    ([Rosalind Reid, presentation tips, page 2](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
18. **End with the result, then the thanks.** Thank the team and the people who paid for the work, and then
    thank the audience
    ([Rosalind Reid, tutorial deck, page 39](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
    Do not end on a detail of the method.

For an agent, write the five parts as one or two sentences each, before you make any slide. Put the
motivation in terms of this audience. Include at least one thing that did not work.

## The words of the script

The script is the words that the speaker says. Write it by
[GUIDE.md](https://github.com/rahuldave/nossaifd/blob/main/GUIDE.md), with the exceptions below. Each
exception is for speech only. The words on a slide also follow GUIDE.md, because the audience reads them. A
slide has two exceptions of its own:

- A slide can hold a phrase in place of a full sentence, by rule 43.
- The titles of a deck can all be questions, or all be labels with a colon, by rule 45. GUIDE.md forbids
  rhetorical questions in a document.

19. **Put the news first in a spoken sentence, then the context.** Rosalind Reid shows the same news report
    twice. A speaker gives the news first, and a writer gives the context first
    ([Rosalind Reid, written reports, pages 5 to 7](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf)).
    The rule replaces the rule of GUIDE.md "Put the known information first and the new information last".
20. **Use contractions in the script.** Speech uses them, and a script without them sounds stiff. Shankar's
    plain-writing skill allows them for the same reason
    ([Shankar, plain-writing skill, rule 5](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L51-L54)).
    Keep the full "do not" when the negation is the point, which is this guide's own rule. The rule replaces
    the rule of GUIDE.md "Do not use contractions in documentation".
21. **Ask one question when the next sentence answers it.** A listener cannot see a heading, so a question can
    tell the listener what comes next. Reid uses questions this way in her titles
    ([Rosalind Reid, tutorial deck, page 13](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
    Do not ask two questions in a row
    ([Shankar, plain-writing skill, rule 23](https://github.com/docwriter-org/plain-writing-skill/blob/f0d3630983ac7a82aa580f1c1509d72df739ee12/skills/plain-writing/SKILL.md?plain=1#L240-L246)).
    The rule replaces the rule of GUIDE.md "Do not ask rhetorical questions".
22. **Use analogy, metaphor and humor in the script.** Reid gives them as methods of a storyteller, for
    written, visual and spoken work
    ([Rosalind Reid, tutorial deck, page 40](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
    Her presentation tips say that humor is always good, and that a metaphor connects the audience to the topic
    ([Rosalind Reid, presentation tips, page 2](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
    The rule replaces the rules of GUIDE.md on literal tone, for the script only. The section "Methods of a
    storyteller" gives the detail.
23. **Repeat a key idea, and the terms of the outline.** A listener cannot turn back a page
    ([Rosalind Reid, presentation tips, page 2](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
    The rule replaces the advice of GUIDE.md to remove a phrase that repeats.
24. **Give the one result a memorable phrase.** Reid says that words can make flow and rhythm
    ([Rosalind Reid, written reports, page 19](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf)).
    Use rhythm in the script, for the result that the audience must remember. Titles stay literal.
25. **Say each sentence in one breath.** Keep a spoken sentence to about 20 words, and never more than 25.
    The 20 is this guide's own number. The 25 is the limit of GUIDE.md.
26. **Do not use "so" as a filler.** The word means "therefore". A speaker who does not overuse it sounds more
    sure ([Rosalind Reid, presentation tips, page 3](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).

Everything else in GUIDE.md applies to the script and to the slides.

## Methods of a storyteller

Rosalind Reid's tutorial deck shows the methods of a storyteller, for writing, pictures and speech
([Rosalind Reid, tutorial deck, pages 40 to 57](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
This guide groups them in its own way. The script and the pictures use them, and the words on a slide stay
literal.

27. **Compare a hard idea with one that the audience already knows.** Make the comparison in the script, or
    let a picture make it. A metaphor makes the same kind of link in fewer words. Rosalind Reid gives analogy
    and metaphor as methods of a storyteller
    ([Rosalind Reid, tutorial deck, pages 41 and 55](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
28. **Say where the comparison breaks down.** A listener can take a comparison further than it goes. The rule
    is this guide's own.
29. **Choose a metaphor with care.** A metaphor changes how the audience sees the subject. Rosalind Reid's
    example is a newspaper headline, and she adds no text to it
    ([Rosalind Reid, tutorial deck, page 56](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
    The advice is this guide's reading of her example.
30. **Let one clear picture carry an argument.** A single figure can show the cases or the steps of an
    argument and how they connect. Keep few things in it, so that each one reads clearly
    ([Rosalind Reid, tutorial deck, pages 45 and 48](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
31. **Prefer a plain sketch when it teaches better.** A drawing that looks made by hand can feel friendlier
    than a polished chart. It can still show the process
    ([Rosalind Reid, tutorial deck, page 43](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
32. **Plan the humor.** A joke shows that the speaker is at ease, and it keeps the audience interested and
    happy ([Rosalind Reid, tutorial deck, page 57](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
    Plan a light moment at the start
    ([Rosalind Reid, presentation tips, page 2](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf))
    and after a hard part
    ([Rosalind Reid, presentation tips, page 4](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).

## Pace and length

33. **Speak at 90 to 120 words a minute.** A 20-minute talk has about 2,000 words. The pace is much slower
    than conversation, so the audience keeps up and the speaker seems in control. Rosalind Reid's presentation
    tips give these numbers from Montgomery
    ([Rosalind Reid, presentation tips, page 1](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
34. **Aim nearer 90 words a minute,** which is this guide's own advice. A first script is usually too long.
35. **Do not fill all the time.** The time can change on the day
    ([Rosalind Reid, presentation tips, page 1](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
    Mark the slides that the speaker can drop, and the time saved by each, which is this guide's own rule.
36. **Do not rush.** Reid puts this advice first for the delivery of a talk. Next to it, she notes that human
    short-term memory holds 3 to 9 items at once
    ([Rosalind Reid, tutorial deck, page 27](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
37. **Keep the script of one slide to about a minute.** At the fastest pace, a minute is 120 words. The limit
    is this guide's own number. The sources give the minute as the time a viewer looks at a slide, in rule 40.

## Slides

Rosalind Reid lists the common problems of slide talks
([Rosalind Reid, presentation tips, pages 2 and 3](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
They are too many slides, too much on a slide, visual clutter and too many words. A key idea also goes past
too fast, because a slide does not stay in view as a chalkboard does. She ends the list of clutter with the
words "less is more".

38. **Make each slide work for the listener with the least background.** Prefer a diagram that teaches to a
    picture that only decorates. Cut whatever does not help that listener, such as extra pictures, extra words
    and chartjunk, which is decoration in a chart that carries no data. Rules 42 and 50 give the limits for
    words and equations. Rosalind Reid gives this advice for an audience of mixed backgrounds
    ([Rosalind Reid, tutorial deck, page 30](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
39. **Put one part of the story on a slide.** Do not put a large part of the story on one slide
    ([Rosalind Reid, tutorial deck, page 32](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
40. **Use the minute test.** Plan for a minute or less of screen time for each slide. A slide that takes
    longer to grasp carries too much, so split it. Rosalind Reid gives a viewer about 20 seconds to see what
    the slide is about. The viewer then takes it all in within 30 to 40 seconds more
    ([Rosalind Reid, presentation tips, page 4](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
41. **Show at most 4 items on a slide.** The number is this guide's own. It agrees with the list rule of
    GUIDE.md, which keeps a list to about four items. Rule 36 gives Rosalind Reid's note on short-term memory.
    It is advice on how to speak, and not a limit for a slide
    ([Rosalind Reid, tutorial deck, page 27](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
42. **Keep a slide to about 30 words, apart from the labels of a figure.** The number is this guide's own.
    Reid asks the speaker to trim the word count, and gives no number. A listener who reads a full slide
    stops listening
    ([Rosalind Reid, presentation tips, page 2](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
43. **Do not put a paragraph on a slide.** Put the sentences in the script, and keep a phrase or one sentence
    on the slide. The rule is this guide's own, and it follows from the word clutter that Rosalind Reid
    describes ([Rosalind Reid, presentation tips, page 2](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
44. **Start each title with the words that set the slide apart.** A person who scans a list often reads only
    the first two words of each item
    ([Shankar, post, principle 2](https://fsdatalab.github.io/blog/agent-text-at-scale/#2-put-the-most-important-words-first)).
    The titles of a deck are such a list. Write "Database reads cause the wait" and not "Results of the
    timing test".
45. **Give all the titles one structure.** A reader reads an item faster when it has the same structure as the
    items before it
    ([Shankar, post, principle 3](https://fsdatalab.github.io/blog/agent-text-at-scale/#3-use-the-same-structure-and-the-same-vocabulary)).
    Choose one form, for example a short sentence that states the point of the slide. Do not mix questions,
    labels with a colon and sentences.
46. **Keep the titles literal.** A title says what the slide shows. Do not write a slogan or a pun, as
    GUIDE.md says for headings.
47. **Put the text on the left and the figure on the right.** English is read from left to right, so the text
    then explains the figure
    ([Rosalind Reid, presentation tips, page 3](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
48. **Use one background.** Use dark text on a light background for a deck with much text. Use a dark
    background for a deck of graphics, and for a dark room. Do not change the background between slides
    ([Rosalind Reid, presentation tips, page 3](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
49. **Use color to carry information.** A rainbow of colors for decoration only adds clutter
    ([Rosalind Reid, presentation tips, page 2](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf),
    and [Rosalind Reid, tutorial deck, page 59](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
50. **Show few equations, and explain each one in the script.** Say what each symbol means and what the
    equation says
    ([Rosalind Reid, tutorial deck, page 30](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
    Show at most 2 equations on a slide, which is this guide's own number.

## Figures

These rules come from Rosalind Reid's tutorial deck and her presentation tips.

51. **Label every figure in plain words, and put a caption or a label next to it.** Do not paste a plot
    as the analysis software drew it. Check each axis. Give it a label in the audience's words, written
    across the slide and not up the side. A slide has no room for the caption that a paper gives a figure, so
    the labels must carry its meaning. Rosalind Reid gives this advice in
    [Rosalind Reid, presentation tips, page 3](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf).
52. **Guide the eye to the important information.** Do not show a dense network that looks like a tangle, or
    bars in three dimensions. Show the comparison that the story needs. Give it plain labels and units, on
    shared axes ([Rosalind Reid, tutorial deck, pages 51 to 54](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
53. **Draw a simple cartoon of a method.** A drawing of the idea teaches faster than the real data
    ([Rosalind Reid, tutorial deck, page 31](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
54. **Redraw a figure from a paper for a general audience.** Use common names. Add a short key, and a
    note at each finding
    ([Rosalind Reid, tutorial deck, pages 33 and 34](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
55. **Prepare the audience before a video plays.** A video moves on before the audience can ask about it. So
    before it starts, show one or two frames as still pictures. Explain the colors, the time that passes
    and the size of what is shown. Point at the part to watch. Rosalind Reid gives this
    advice in
    [Rosalind Reid, presentation tips, page 3](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf).
56. **Use a picture for relief or humor between parts of the talk.** Reid says that pictures can give relief,
    pleasure and humor
    ([Rosalind Reid, written reports, page 20](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf)).
    Never add decoration inside a data figure.

## Help the listener hold the ideas

57. **Show an earlier figure again** when a later slide depends on it. Listeners often ask a speaker to go back
    ([Rosalind Reid, presentation tips, page 2](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
58. **Add a teaching slide** at the start and before each new idea. Do it for each audience outside the
    speaker's field
    ([Rosalind Reid, presentation tips, page 4](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
59. **Make two versions if the slides go online.** The version on the screen has few words. The online version
    can carry more words, pictures and slides that explain
    ([Rosalind Reid, presentation tips, page 2](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).

## The sketch test

Rosalind Reid ends her tutorial with an exercise
([Rosalind Reid, tutorial deck, page 59](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
Each person draws a sketch of one part of the project, and then explains the project with it in a minute.
The sketch uses color to carry information, and common words instead of jargon and symbols.

60. **Describe one sketch that explains the main idea of the talk, before you make the figures.** If you cannot
    describe it, the story is not clear yet. The use of the exercise as a test is this guide's own rule.

## Prepare, practice and deliver

These rules come from Rosalind Reid's presentation tips, which follow Montgomery, and from her tutorial deck.

61. **Start early.** Outline the structure, think about other orders, and plan the pictures. If you move
    material, check that the slides still tell one story
    ([Rosalind Reid, presentation tips, page 1](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
62. **Find a method of preparation that suits the speaker.** Reid writes out everything she wants to say, then
    picks the main points, then makes the slides. She says that other speakers find other methods
    ([Rosalind Reid, presentation tips, page 5](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
63. **Practice many times.** Montgomery recommends 10 times or more. Practice alone and for a test audience,
    and give a big talk to a small audience first
    ([Rosalind Reid, presentation tips, page 1](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
64. **Record a talk and watch it.** Reid found her own weak points this way
    ([Rosalind Reid, presentation tips, page 5](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
65. **Look at the listeners,** and watch for signs of attention
    ([Rosalind Reid, tutorial deck, page 27](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)).
66. **Engage the audience, and adapt the talk.** Unless the talk is formal, plan moments of informal exchange.
    A question can show that the audience needs more explanation
    ([Rosalind Reid, presentation tips, page 1](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
67. **Know the next slide.** Notes, a printed set of slides or an outline keep the talk from wandering
    ([Rosalind Reid, presentation tips, pages 2 and 3](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).
68. **Stay calm and sure of yourself, also when something goes wrong.** Good preparation makes a speaker
    sure of the material. A speaker who stays calm and polite gets through a failed projector or a hostile
    question. Rosalind Reid passes on this advice from Herbert L. Hirsch
    ([Rosalind Reid, tutorial deck, page 28](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf),
    and [Rosalind Reid, presentation tips, page 5](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf)).

An agent cannot practice a talk. Give the person a table of the slides with the time for each, and a plan for
practice. The plan has a timed run alone, a run for a test audience and a recorded run. Tell the person that
the script is for practice, so that the talk does not become a dull recitation.

## The deck format

Write the deck as one Markdown file, which Marp, Slidev and reveal.js can show.

- **Slides.** A line that is only `---` starts a new slide. Leave a blank line above it, because some tools
  read a line of text right above `---` as a heading.
- **Front matter.** The file can start with YAML front matter. The key `minutes` gives the time slot, for
  example `minutes: 20`.
- **Title.** The first heading of a slide is its title. The first slide holds the title of the talk.
- **Script.** Put the script of a slide in an HTML comment at the end of the slide. Marp and Slidev show the
  comment as the speaker notes. Slidev reads only the last comment of a slide, so use one comment.

```markdown
# Database reads cause the wait

![Time for each step of one search](https://example.com/timing.png)

Time for each step of one search

<!--
Here's where the eight seconds go.
-->
```

The checker also reads the notes of other tools:

- a block from `::: notes` to `:::` (Pandoc and Quarto)
- a block from `<aside class="notes">` to `</aside>` (reveal.js)
- a line that starts with `Note:`, and the rest of the slide after it (reveal.js)

The checker reads `Note:` only in a deck with no key `marp` in its front matter. It decides for each slide. A
slide that has an HTML comment or another block as notes keeps them, and its `Note:` line is text on the
slide. The line must start with `Note:` exactly, with a capital N and no space before it. In a Marp deck, a
line such as "Note: the cache is cold" is text on the slide.

A comment of only Marp directives, such as `<!-- _class: lead -->`, is not notes. In a comment that also holds
the script, only a line that starts with `_`, such as `_class: lead`, is a directive. Every other line is
script, so a script line such as "title: we explain the chart" stays in the script.

## Check the deck

`check_talk.py` measures the rules that a program can measure:

```
uv run --no-project python check_talk.py deck.md                # hard problems fail the check
uv run --no-project python check_talk.py -v deck.md             # also show the soft notes
uv run --no-project python check_talk.py --minutes 20 deck.md   # the time slot, if the front matter has none
```

On a slide, it checks the items, the words, paragraphs, equations, captions of figures and the titles. In
the script, it checks the length for the time slot, the length of each sentence, the filler "so" and
questions. The page
[docs/check-talk.md](https://github.com/rahuldave/nossaifd/blob/main/docs/check-talk.md) lists each check, and
why it is hard or soft. The checker cannot judge the story, the news first, or the tone. Read the deck after it
passes.

## Sources

- **Rosalind Reid**, "Communicating Your Work", a tutorial for the course AC297r at the Institute for Applied
  Computational Science at Harvard, 25 March 2015. Reid was the editor of American Scientist from 1992 to
  2008. The rules for the story, the slides, the figures and the methods of a storyteller come from it.
  [The tutorial deck](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-communicating-your-work-deck.pdf)
  has 59 pages.
- **Rosalind Reid**, "Some thoughts about presentations", five pages of presentation tips for the same
  tutorial. The file names no author. Its text gives "Montgomery's/Reid's basic advice" and personal
  observations in the first person, so this guide takes Reid as the author. The attribution is an inference.
  The rules for preparation, pace, audiences and delivery come from
  [the presentation tips](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf).
- **Rosalind Reid**, "Communicating Your Work: written reports", the part of the same tutorial on writing.
  The rule of news first in speech, and the roles of words and pictures, come from
  [the written reports](https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-2015-written-reports.pdf).
- **Scott L. Montgomery**, The Chicago Guide to Communicating Science, University of Chicago Press, 2003.
  Rosalind Reid's presentation tips draw mostly on this book, for example the pace of 90 to 120 words a
  minute.
- **Herbert L. Hirsch**, Essential Communication Strategies for Scientists, Engineers, and Technology
  Professionals, second edition, IEEE Press, 2003. Rosalind Reid's presentation tips pass on his advice on
  how a speaker carries a talk. Reid also gives tips with a colleague named McCormick.
- **Shreya Shankar**, "Five Principles for Generating Readable AI Text in Bulk", 29 October 2026, at
  https://fsdatalab.github.io/blog/agent-text-at-scale/. The rules for slide titles come from it.
- **Shreya Shankar**, the plain-writing skill, at https://github.com/docwriter-org/plain-writing-skill,
  under the MIT licence. It supports the rules on contractions and on stacked questions in the script.

This guide states the advice in its own words, and it does not copy the slides or the pictures of the
sources. It uses Rosalind Reid's material with her permission.

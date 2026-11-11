# The declaude skill

The declaude skill by Oskar Austegard revises a draft that reads as if an AI model wrote it. It finds
the sentences that sound like a model, and it rewrites them as plain technical prose. Then it checks that
the revision kept each claim of the draft. The file `references/register.md` of the skill lists the
patterns of model prose, and the skill calls that file the register. The name comes from linguistics,
where it means the style of a piece of prose.

nossaifd ships the skill by Oskar Austegard in `.agents/skills/declaude/`, next to its own skill. Rules 50 to 55 of
[the guide](../GUIDE.md) come from it, and rules 9, 10, 20, 32, 34, 36, 37, 38 and 43 take parts of it.

## Where it comes from

Oskar Austegard wrote the skill, and he calls it declauding. It is in the folder `declauding` of his repository
[oaustegard/claude-skills](https://github.com/oaustegard/claude-skills/tree/6baa7290da972191749acda03c63297e67b3fc26/declauding),
under the MIT licence, copyright (c) 2025 Oskar Austegard. nossaifd ships version 0.14.0, from commit
`6baa729` of 10 November 2026. The file `LICENSE` in the folder holds his licence. `just declaude-copy`
copies the skill again from that commit.

The copy makes three changes to his skill, and `sources/declaude.patch` holds them:

- **The name.** This package calls the skill declaude, a verb. `check.py` and the linter read the name
  declauding as an -ing form, and they marked it on every page that credits him. The file `SKILL.md`
  names the skill declaude, and its path for the scripts names the folder `declaude`. So do the
  command of his hook for a plugin and the command of his tests.
- **The description.** His description tells an agent to load the skill at the start of every task
  that writes prose, before the draft exists. The new description says that the nossaifd skill calls it
  at its step 6, after the draft passes the checker. It also says to run the skill in an agent that did
  not write the draft. It keeps his phrases for a request, such as "this reads like AI". It also keeps his
  limits, such as no fiction and no code. So the skill still works alone.
- **One sentence of `references/fresh-eyes.md`.** In his commit, line 14 cites `docs/failure-modes.md`,
  a file in his repository oaustegard/claude-workspace. That repository is not public, so the file
  cannot be copied. The lint of skill-package-maker read the path as a missing file of the skill, and
  it failed. The changed sentence names the file, its folder and his repository in words.

## How to use it with the guide

1. Write the draft by the guide. The description of the skill asks you to write the draft without the
   skill, so do not read its register before you write.
2. Run `check.py` on the draft, and fix each hard problem.
3. Keep a copy of the draft. Then give the page to an agent that did not write it, such as a subagent.
   A writer misses its own habits, and the skill asks for a reader who did not write the draft. That
   agent revises the page by the steps in the file `SKILL.md` of the declaude skill. For each pattern, its register gives the reason that the pattern marks model prose, and the
   fix. Its linter marks the patterns that a program can find. Each passage that it marks is a
   candidate, a place that may be model prose, and not a verdict. In this repository, run
   `just declaude page.md`, for one page or more. In another repository, run:

   ```
   uv run --no-project python .agents/skills/declaude/scripts/declaude_lint.py --skip-quoted page.md
   ```

   `just declaude` does not fail on candidates, and `just check` does not run it. `just declaude` fails
   only on a missing page, or when the linter cannot run. Judge each candidate against the register and
   the guide. Where the two disagree, the guide holds, as
   [the choices](why.md#choices-about-the-declaude-skill) say.

   Then read each sentence against the register. The linter finds only some of the patterns. It cannot
   find a paragraph that holds back its finding, which rule 50 calls staging. It also cannot find a
   sentence that the reader understands only after the next sentences. Do not change a bad example that
   a page shows on purpose, even when the linter marks it.

4. Run its diff on the copy of the draft and on the revision. The diff lists each number, name, quote,
   ranking and hedge that the revision lost or added:

   ```
   uv run --no-project python .agents/skills/declaude/scripts/declaude_diff.py draft.md page.md
   ```

5. Run `check.py` again, and fix only what the revision broke. Where the skill and the guide disagreed,
   the project's author chose. The rules of the guide give each choice, so follow the guide.
   [Why the rules](why.md) lists the choices. A sample of your own writing wins over the register, but
   not over the hard limits of the guide, which are the hard problems of `check.py`.
6. Run the linter once more, to check that step 5 brought back no pattern. Then read the page yourself.

The nossaifd skill gives these steps to an agent, and its step 6 calls the declaude skill. So an agent
needs no separate call of the declaude skill. Its description in this package says the same, so that an
agent does not load it before the draft exists.

## The passes on the pages of this repository

On 10 November 2026, the pages of this repository went through three passes and a last run of the
linter. The first pass was the guide, the second was the declaude skill, and the third was the guide
again. Each page had passed `check.py` before, with no hard problem. The
repository does not keep the notes of the passes. The counts below come from them.

- **The declaude pass found what `check.py` cannot.** On every group of pages, it found real
  problems. Examples are a fragment, a heading that names no content, and "hides" or "promises" as the
  verb of a thing. Some of them broke rules 12, 33 and 34 of the guide itself.
- **The second run of `check.py` caught what the revision broke.** In each group of pages, the revision
  made a new soft note. Examples are a sentence of 27 or 28 words, and a term that the paragraph never
  set up. The revision made no hard problem.
- **The last run of the linter found nothing new.** On these pages, no fix of the second run of
  `check.py` brought back a pattern.

In three groups of pages, the diff caught a claim that the revision lost or changed. Examples are a
command, the word "most", and the words "the last words".

Most candidates of the linter were false alarms. On GUIDE.md, 1 of 36 was real. On the pages of
`docs/`, 1 of 25 was real, and 2 were partly real. On EXAMPLES.md, 15 of the 104
candidates outside its quotations were real. The false alarms came from causes such as these:

- the old name of the skill, declauding, which the linter and `check.py` read as an -ing form
- a bad example in straight double quotes, which `--skip-quoted` does not skip
- a heading that starts with "What" or "How" and names its content, as "What it checks" does
- the text of a link read together with its target, as in "the guide guide"
- a phrase that a page repeats on purpose, such as the full name of the skill

## The patterns

The register of the skill lists 56 patterns in five families. For most patterns it gives a pair of
sentences from real text, before and after the revision. A sentence is staged when it makes the reader
feel that a finding arrives and does not give the finding.

The examples DC2 to DC56 of
[the examples](../EXAMPLES.md) quote the pairs word for word. The letters DC stand for the declaude
skill, and each number is the number of an entry of the register. Entry 1 has no example. For an entry that has no pair, they quote
its tell, which is the sign of the pattern, and its fix. Read them also in the register on GitHub,
together with the cases where a pattern is correct:

- [The register by Oskar Austegard](https://github.com/oaustegard/claude-skills/blob/6baa7290da972191749acda03c63297e67b3fc26/declauding/references/register.md),
  with the 56 patterns and their examples.
- [The earned exceptions by Oskar Austegard](https://github.com/oaustegard/claude-skills/blob/6baa7290da972191749acda03c63297e67b3fc26/declauding/references/exceptions.md),
  with the cases where each pattern carries a claim and stays.

| Entries | Family | What the sentence does | Rule of the guide |
|---|---|---|---|
| 1 to 23, 37 to 42 | Staging | It makes the reader feel that a finding arrives, and it does not give the finding | 50 |
| 24 to 36 | Encyclopedic and chatbot | It uses the defaults of a chatbot, such as "serves as" and three items in a list | 51 |
| 43 to 47 | Flat certainty | An adverb or a word such as "nothing" takes the place of the evidence | 52 |
| 48 to 52 | Confiding essayist | It tells the reader that the writer is honest, or it grades the writer's own text | 53 |
| 53 to 56 | Compressed syntax | It packs a claim into fewer words than a reader can parse | 54 |

Rule 55 comes from the steps of the skill. A revision keeps every claim of the draft, and it adds no
fact that the draft or the author did not give.

## The scripts

The scripts of Oskar Austegard are in `.agents/skills/declaude/scripts/`. The README of the skill says that the linter
needs Python 3.9 or later.

| Script | What it does | What it needs |
|---|---|---|
| `declaude_lint.py` | It marks the patterns that a program can find, line by line. Use `--skip-quoted` on a page that quotes bad prose | Only the standard library |
| `declaude_diff.py` | It lists each claim that a revision lost or added | Only the standard library |
| `declaude_review.py` | It sends the title, the subtitle, the headings, the opening sentence, the closing sentence of each section and each one-sentence paragraph to a model | A key for Gemini or Anthropic. Without a key, it prints the prompt for an agent |
| `declaude_rank.py` | It sorts the sentences by how staged they look | torch, transformers and numpy, and a model that it downloads from Hugging Face |
| `fresh_eyes.py` | It writes a file of the changed pages for a reader who did not see the old version | Only the standard library |

`declaude_review.py` sends parts of the draft to Gemini when `GEMINI_API_KEY` is set. Without that key,
it sends them to Anthropic when `ANTHROPIC_API_KEY` is set. Do not run it on a draft that must stay
private. With `--emit-prompt`, it sends nothing.

The skill also has a hook for Claude Code, in `hooks/hooks.json`. The hook works only when the skill is
installed as a plugin, so it does not run from this repository. Its path still names his folder,
`declauding`, as his plugin does. The README of the skill links to two other
skills of Oskar Austegard, `challenging` and `crafting-instructions`, and step 2 of its file
`SKILL.md` names `challenging`. This package does not ship them. They are in his repository.

## The sources of the skill

The README of the skill gives its sources by family:

- Entries 1 to 23 come from one revision of a published post about a benchmark. Entries 37
  to 42 come from revisions of drafts and of a reference page in his repository.
- Entries 24 to 36 come from the Wikipedia page
  ["Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), through the skill
  [blader/humanizer](https://github.com/blader/humanizer).
- Entries 43 to 47 come from the clusters of pull requests in Louis Abraham's
  [load-bearing](https://github.com/louisabraham/load-bearing).
- Entries 48 to 52 come from Simon Willison's
  [llm-cliche-highlighter](https://github.com/simonw/tools/blob/main/llm-cliche-highlighter.html).
- Entries 53 to 56 come from Clark, Martin and Mahowald, [arXiv 2610.29162](https://arxiv.org/abs/2610.29162).

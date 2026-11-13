# Make the flow happen

The nossaifd skill gives an agent the steps for a page. The agent drafts the page by the guide and runs
the checker. A subagent then runs the pass of the declaude skill by Oskar Austegard. Then the agent runs
the checker again and the linter once more.

An agent follows these steps only when it loads the skill and keeps to it. Three parts of this package make that happen in a project. Each part does a different
job, so the expensive pass runs once for each change of a page.

| Part | What it does | What it costs |
|---|---|---|
| The instruction in `AGENTS.md` and `CLAUDE.md` | It tells the agent to use the nossaifd skill for every page that a person reads. The agent reads the file at the start of each session | Nothing. It is text |
| The hooks at the start and the end of a turn | They find each page that the turn changed. They block the end of the turn once when such a page has a hard problem or no record of its pass | About a tenth of a second for each turn |
| The workflow for GitHub | It runs the checker on each page that a pull request adds or changes | Seconds on GitHub, and no model |

## The instruction in AGENTS.md and CLAUDE.md

The file `.agents/skills/nossaifd/assets/agents-prose.md` holds the lines for the `AGENTS.md` and the
`CLAUDE.md` of a project. With them, the agent does the steps while it writes, and the hook rarely has to
ask.

The lines say that `just prose` replaces steps 6 to 8 of the skill only when `.agents/stack.json` sets
`choices.tasker` to the JSON value `true`. The gate tests the same setting, in `gates_installed`.
Otherwise the agent does the steps itself. It does them itself also when the project has no recipe
`just prose`, or when that recipe only runs the checkers. `just prose-check` only runs the checkers, so it never replaces those steps.

## The hooks at the start and the end of a turn

A turn starts when a person sends a message, and it ends when the agent stops to answer. Claude Code and
Codex run `.agents/skills/nossaifd/scripts/prose_gate.py` at both moments.

- At the start of a turn, `prose_gate.py start` keeps a snapshot of the pages. The snapshot holds the
  last commit and the content of each page that git reports as changed.
- At the end of a turn, `prose_gate.py hook` compares the pages with the snapshot. A page counts when its
  content differs from the snapshot. A page can differ in the working copy or in a commit that the turn
  made. Such a commit has the same author and was made after the turn started. A pull or a checkout
  brings commits that were made before the turn, so they do not count.

For each page that counts, the hook runs the checker of the page, and it looks up the page in the record
of passes. The checker is `check.py`, or another checker that the map of checkers of the project names
for the page. A page passes when its checker finds no hard problem and the record holds the page as it is now.
After step 8 of the nossaifd skill, the agent records each page:

```bash
uv run --no-project --quiet python .agents/skills/nossaifd/scripts/prose_gate.py record page.md
```

`record` refuses a page that has a hard problem, a missing page, and a file outside the repository. The
record is a promise of the agent, not a proof. The hook cannot see whether the declaude pass ran.

The hook blocks the end of a turn only once. When the agent tries to end the turn again, the hook lets
it end, so it cannot loop. On the next turn, the hook asks about a page again only when the page changes
again. A draft that a person edits, or a page of an earlier turn, does not block a later turn. A block
names at most 20 pages.

The hook sees the working copy, not the agent. So when a person edits a page during a turn, or a second
agent edits a page in the same working copy, that page counts for the turn.

The record lives in the folder `.git/nossaifd`. Every worktree of the repository shares it, so a page
that passed in one worktree passes in the others. It never shows in `git status`. The snapshots live in
the folder of git of each worktree. Pages in a submodule are out of scope.

The hook skips these files, because they are not pages for a person:

- `AGENTS.md`, `CLAUDE.md` and `GEMINI.md`, in any folder
- a file `CHANGELOG.md`, in any folder
- the folders `.agents/`, `.claude/` and `.codex/`
- the folders `node_modules/`, `_site/` and `.quarto/`, in any folder

An error in the hook never blocks, and a missing script never blocks either. Set the environment
variable `NOSSAIFD_GATE=off` before you start Claude Code or Codex to turn the hooks off. Setting it in a
command of the agent has no effect.

To see which changed pages still need their steps, and the checker of each changed page, run:

```bash
uv run --no-project --quiet python .agents/skills/nossaifd/scripts/prose_gate.py status
```

## Another checker for some pages

Some pages follow another guide, for example the slides of a talk. The script of a talk is in the
speaker notes. The talk guide of nossaifd-talks asks for contractions in the script, because speech uses
them. `check.py` marks each contraction as a hard problem, so it fails a good deck. The talk checker
`check_talk.py` knows the slides from the notes, so it is the right checker for a deck.

The map of checkers tells the gate which checker checks a page. It is the file
`.agents/nossaifd-checkers.json` in the root of the project. The root is the top folder of the git
repository. This map gives the decks and the plans of talks to the talk checker:

```json
{
  "version": 1,
  "checkers": [
    {
      "pages": ["**/slides.qmd", "**/plan.md"],
      "checker": ".agents/skills/presentations/scripts/check_talk.py"
    }
  ]
}
```

- **`version`** is the number 1.
- **`checkers`** is a list of rules. Each rule has a list `pages` of globs and the path of one `checker`.
- **A glob** matches the whole path of a page from the root. A `*` matches any characters inside one
  folder name, and a `?` matches one character. A `**` that is a whole folder name matches any number of
  folders, also none. So `**/slides.qmd` matches `slides.qmd` and `talks/cache/slides.qmd`. Every other
  character matches itself. A `./` at the start does not count. A map with a glob that starts with `/`,
  ends with `/`, has a space at either end, or holds `\`, `//`, `.` or `..` as a folder name is broken,
  because such a glob would match no page.
- **The first rule** whose glob matches a page names its checker. A page that no rule matches gets
  `check.py`.
- **The path of a checker** is relative to the root, with `/` between folders. It names a Python file
  inside the project. A map with an absolute path or a path with `..` is broken. The gate follows a
  symlink, so a skill that the installer linked into `.agents/skills/` still works.

`prose_gate.py pages` still decides what is a page, and the map decides which checker checks it. Every
command of the gate that checks a page uses the map. These commands are `hook`, `status`, `record`,
`check-diff` and `check`.

### The command of a checker, and its exit codes

The gate runs a checker with its own Python, in the root of the project, once for each page:

```bash
python -B CHECKER PAGE
```

- **`PAGE`** is the path of the page from the root. A path that starts with `-` gets `./` before it.
- **`-B`** stops Python from writing `__pycache__` into the folder of the checker.
- **Exit 0** means that the page has no hard problem.
- **Exit 1** means that the page has hard problems. Each line of the output that starts with the word
  `HARD`, after spaces, names one problem, as in `  HARD slide 4: the title is long`. A line that starts
  with the path of the page is a summary, and it names no problem. The gate gives
  these lines in the message of a block. A `HARD` line also fails a page when the checker exits 0.
- **Any other exit** is a failure of the checker. So is exit 1 with no `HARD` line, which is what a crash of
  Python gives.
- **A checker that does not end** in 30 seconds also fails. The gate then stops the checker and each
  program in its process group.
- **The hook at the end of a turn** gives all its checkers 40 seconds together, because Claude Code and
  Codex stop the hook after 60 seconds. A page whose checker gets no time is a hard problem. Run
  `prose_gate.py check` on that page.

The talk checker and `check.py` both keep this contract. `prose_gate.py check -v PAGE` also passes `-v`
before the page, so that the checker prints its soft notes.

A page never passes in silence when its checker cannot judge it. Each of these is a hard problem of the
page, with a message that says what went wrong:

- the checker is missing
- the checker fails, does not end in time, or gets no time in the hook
- the map is not JSON, or does not have the format above

The gate names the checker of each page in the message of a block, in `status`, in `record` and in
`check-diff`. When the checker is not `check.py`, the record of a pass also keeps its name. So a pass by
the old checker does not count for the new one. `status` asks again about each changed page that the
map gives to another checker. The hook asks again when such a page changes in a turn.

A change to the map does not check the pages that did not change. After you change the map, check its
pages with `prose_gate.py check`.

To check pages by hand with the checker of each page, run:

```bash
uv run --no-project --quiet python .agents/skills/nossaifd/scripts/prose_gate.py check -v page.md
```

`check` exits with 0 when no page has a hard problem, 1 when a page has one, and 2 for a missing page. A
file outside the project, such as a draft in a temporary folder, gets `check.py`.

`prose_gate.py check-changed` checks the pages that changed since the last commit. The recipe
`just prose-check` of the role runs it, as the step `prose-check` of `just check`:

```bash
uv run --no-project --quiet python .agents/skills/nossaifd/scripts/prose_gate.py check-changed -v
```

- **The changed pages** are the files that `git diff --diff-filter=AMT HEAD` names, with no rename, and
  the new files that git does not ignore. `T` is a change of type, such as a link that became a file. The rule `is_page` keeps the pages among them. So a deleted page
  is not checked, and a renamed page is checked under its new name.
- **Before the first commit,** each page in the index and each new page counts as changed.
- **No changed page** is a pass, with exit 0.
- **With names of pages,** it checks those pages only, as `check` does. `-v` can come before or after a
  page. A page whose name starts with `-` comes after `--`.
- **Outside a Git repository,** it needs names of pages. With none, it exits with 2.
- **It writes nothing:** no record of a pass, and no snapshot.

`check-changed` exits with 1 on a hard problem, as `check` does.

### Who may write the map

The map names a program, and the hook runs that program at the end of each turn. So treat the map as
code, as you treat a hook in `.claude/settings.json` or a recipe of the `Justfile`.

- **Only the people who look after the project** write the map, and they review each change to it.
- **The gate reads the map only from the root of the project.** It does not read a map in any other
  folder, such as the folder of a page, of the skill or of the call.
- **A change to the map shows.** It shows in the diff of a pull request, and the messages of the gate
  name the new checker.
- **The workflow runs on `pull_request`.** It runs the gate and the map of the pull request, with a
  token that can only read. Do not run it on `pull_request_target`, which gives the
  secrets of the repository to that code.

## Beside the commit gates

A gate is a check that stops a commit when it fails. The commit gates of agent_gest_git_skills check each
commit. A project has the gates when its file `.agents/stack.json` turns on the tasker role. The tasker
role is the package of skills of agent_gest_git_skills. The hooks of this page make a turn gate. The turn
gate stays beside the commit gates, and it has a different job:

| Gate | When it runs | Its job |
|---|---|---|
| The turn gate, the hooks of this page | At the end of each turn | It asks early, at little cost. It blocks the end of a turn once |
| The commit gate | At each commit | It gives the final answer. A commit that changes a page needs a `prose` record and a pass of the step `prose-check` |

- **`just prose`.** With the gates, the message of the hook that blocks a turn says "run `just prose`".
  The target gives the pages to a fresh agent, which is an agent that the harness starts for one task.
  The fresh agent does the plain-writing pass and the pass of the declaude skill by Oskar Austegard. Then
  it records each page that it passed, with `prose_gate.py record`. Its base task is
  `.agents/skills/nossaifd/references/targets/prose.md`.
- **The `prose` record.** The steps of the skill, done by hand, record a page, so the hook lets the turn
  end. But a page pass is not a `prose` record. The commit gate needs the `prose` record of the tree, and
  only `just prose` gives it.
- **The store of page passes.** One store in `.git/nossaifd` holds the passes, with or without the gates.
  So a page that `just prose` passed in one worktree does not block a later turn in another worktree.
- **The rule for pages.** The `@pages` of the commit gate take the pages from `prose_gate.py pages`. The
  step `prose-check` runs `prose_gate.py check-changed`, which keeps the pages by the same rule `is_page`.
  So they use one rule with the hook, and they accept the same pages. A change to
  `CHANGELOG.md` alone needs no `prose` record.

`prose_gate.py pages` prints each path that is a page:

```bash
git diff -z --name-only --no-renames --diff-filter=AM HEAD | uv run --no-project --quiet python .agents/skills/nossaifd/scripts/prose_gate.py pages -z
uv run --no-project --quiet python .agents/skills/nossaifd/scripts/prose_gate.py pages README.md AGENTS.md
```

- **The paths** come from the arguments. With no path, they come from standard input, one on each line.
- **With `-z`,** a NUL character ends each path, in the input and in the output. Use `-z` for a path that
  can hold a newline.
- **Each path** is relative to the root of the repository, as git prints it. An absolute path inside the
  repository is read as its path from the root of that repository. A symlink inside the repository is
  not followed.
- **The output** is each path that is a page, as written and in the order given. The command reads only
  the names. It does not check that a file exists, so take out the deleted files first, as
  `--diff-filter=AM` does.
- **The exit code** is 0, also when no path is a page. It is 2 for an unknown option.
- **A path that starts with `-`** must come after `--`.

## The workflow for GitHub

`.agents/skills/nossaifd/assets/prose-check.yml` goes into `.github/workflows/` of the project. On each
pull request, it runs `prose_gate.py check-diff`. That command checks each page that the pull request
adds, changes or renames, with the checker of the page, and it skips the files that the hook skips. It
fails on a hard problem.

The workflow catches a page that a person edited without an agent. It cannot run the declaude pass,
because that pass needs a model. It needs the skill committed in `.agents/skills/nossaifd/`.

With the commit gates, `just check` runs the step `prose-check`, and the installer of jnterfaces removes
the workflow when the tasker role is installed. But the recipe `just prose-check` checks the pages that
changed since the last commit. A fresh checkout in CI has no such page, so there the recipe checks no page.
So without the workflow, no check in CI catches a page that a person edited without an agent. Until the
step in CI checks the pages of the pull request, copy the workflow back into `.github/workflows/` after
each install.

## Install the parts

The file `skill-package.json` names the parts for an installer. The installer adds the instruction to `AGENTS.md`,
the hooks to `.claude/settings.json` and `.codex/hooks.json`, and the workflow. With npx, which installs
only the skills, copy the parts by hand:

1. Add the lines of `assets/agents-prose.md` to `AGENTS.md`. Claude Code reads `CLAUDE.md`, so make
   sure that `CLAUDE.md` holds the line `@AGENTS.md`, which imports `AGENTS.md`, or holds the lines too.
2. Merge `assets/claude-settings-hook.json` into `.claude/settings.json`.
3. Merge `assets/codex-hooks.json` into `.codex/hooks.json`. Codex runs the hooks of a project only when
   you trust the project.
4. Copy `assets/prose-check.yml` into `.github/workflows/`.

The hook of Oskar Austegard's skill, in the folder `hooks` of the declaude skill, is a different hook. It
works only when his skill is installed as a plugin, so it does not run here.

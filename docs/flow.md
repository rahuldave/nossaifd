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

## The hooks at the start and the end of a turn

A turn starts when a person sends a message, and it ends when the agent stops to answer. Claude Code and
Codex run `.agents/skills/nossaifd/scripts/prose_gate.py` at both moments.

- At the start of a turn, `prose_gate.py start` keeps a snapshot of the pages. The snapshot holds the
  last commit and the content of each page that git reports as changed.
- At the end of a turn, `prose_gate.py hook` compares the pages with the snapshot. A page counts when its
  content differs from the snapshot. A page can differ in the working copy or in a commit that the turn
  made. Such a commit has the same author and was made after the turn started. A pull or a checkout
  brings commits that were made before the turn, so they do not count.

For each page that counts, the hook runs `check.py`, and it looks up the page in the record of passes. A
page passes when it has no hard problem and the record holds the page as it is now. After step 8 of the
nossaifd skill, the agent records each page:

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

To see which changed pages still need their steps, run:

```bash
uv run --no-project --quiet python .agents/skills/nossaifd/scripts/prose_gate.py status
```

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
- **The rule for pages.** The step `prose-check` and the `@pages` of the commit gate take the pages from
  `prose_gate.py pages`. So they use one rule with the hook, and they accept the same pages. A change to
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
adds, changes or renames, and it skips the files that the hook skips. It fails on a hard problem.

The workflow catches a page that a person edited without an agent. It cannot run the declaude pass,
because that pass needs a model. It needs the skill committed in `.agents/skills/nossaifd/`.

With the commit gates, `just check` in CI runs the step `prose-check`, which does the same check. So the
installer of jnterfaces removes the workflow when the tasker role is installed.

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

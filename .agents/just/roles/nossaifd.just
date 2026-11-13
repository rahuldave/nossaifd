# The recipe of the prose role: the writing checker of nossaifd. just install imports this file in a project that
# jnterfaces started. It fills the step prose-check of just check. The name prose stays free for the agentic
# target just prose of the tasker role.
# The index of jnterfaces sets jlog as the shell, so this file sets no shell. Its last line records the step for
# jlog pass, and runs only when the check passed. That line fails without the shell jlog, so a project without the
# index of jnterfaces copies the recipe of the README of nossaifd instead of this file.

# Check the pages that changed since HEAD against the writing guide, each with its checker. In CI, or with --base REF, also the pages since a base. With names of pages, check those pages only. -v also shows the soft notes
[positional-arguments]
prose-check *args:
    uv run --no-project --quiet python .agents/skills/nossaifd/scripts/prose_gate.py check-changed "$@"
    jlog step prose-check

# The recipe of the prose role: the writing checker of nossaifd. just install imports this file in a project that
# jnterfaces started. It fills the step prose-check of just check. The name prose stays free for the agentic
# target just prose of the tasker role.

# Check the pages that changed since HEAD against the writing guide, each with its checker. In CI, or with --base REF, also the pages since a base. With names of pages, check those pages only. -v also shows the soft notes
[positional-arguments]
prose-check *args:
    uv run --no-project --quiet python .agents/skills/nossaifd/scripts/prose_gate.py check-changed "$@"

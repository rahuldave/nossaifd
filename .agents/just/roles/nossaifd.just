# The recipe of the prose role: the writing checker of nossaifd. just install imports this file in a project that
# jnterfaces started.

# Check Markdown pages against the writing guide. Alone, every Markdown file that git tracks, outside .agents, .claude and .codex. -v also shows the soft notes
[positional-arguments]
prose *args:
    #!/usr/bin/env sh
    script=.agents/skills/nossaifd/scripts/check.py
    # A word that is not an option names a page, so the checker checks the named pages only.
    for arg in "$@"; do
        case "$arg" in -*) ;; *) exec uv run --no-project --quiet python "$script" "$@" ;; esac
    done
    if [ -z "$(git ls-files -- '*.md' ':!:.agents/**' ':!:.claude/**' ':!:.codex/**' | head -n 1)" ]; then
        echo "just prose: git tracks no Markdown file yet"
        exit 0
    fi
    git ls-files -z -- '*.md' ':!:.agents/**' ':!:.claude/**' ':!:.codex/**' | xargs -0 uv run --no-project --quiet python "$script" "$@"

# The recipe of the prose role: the writing checker of nossaifd. just install imports this file in a project that
# jnterfaces started.

# Check Markdown pages against the writing guide. Alone, every Markdown file that git tracks, except AGENTS.md, CLAUDE.md and the files in .agents, .claude and .codex. -v also shows the soft notes
[positional-arguments]
prose *args:
    #!/usr/bin/env sh
    script=.agents/skills/nossaifd/scripts/check.py
    # A word that ends in .md, or that is not an option, names a page, so the checker checks the named pages only.
    for arg in "$@"; do
        case "$arg" in *.md|[!-]*) exec uv run --no-project --quiet python "$script" "$@" ;; esac
    done
    if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
        echo "just prose: this folder is not in a Git repository, so name the pages: just prose README.md" >&2
        exit 1
    fi
    # The tracked pages that are on disk. AGENTS.md and CLAUDE.md are instructions for agents; name them to check them.
    pages() {
        git ls-files -z -- '*.md' ':!:.agents/**' ':!:.claude/**' ':!:.codex/**' ':!:AGENTS.md' ':!:CLAUDE.md' \
            | xargs -0 sh -c 'for page; do [ -f "$page" ] && printf "%s\0" "$page"; done' sh
    }
    if [ -z "$(pages | tr -d '\0')" ]; then
        echo "just prose: git tracks no Markdown file to check yet"
        exit 0
    fi
    pages | xargs -0 uv run --no-project --quiet python "$script" "$@"

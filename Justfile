# nossaifd: every task is a recipe here. `just` lists them.

# Each word after a recipe's name reaches its commands whole, as "$1", "$2" and so on; "$@" is all of them
set positional-arguments

# Python comes from uv, so the machine needs just and uv only
python := "uv run --no-project --quiet python"

[private]
default:
    @just --list --unsorted

# Copy GUIDE.md and check.py into the skill, which ships copies of them
sync:
    cp GUIDE.md .agents/skills/nossaifd/references/GUIDE.md
    cp check.py .agents/skills/nossaifd/scripts/check.py

# Check the Python and the JSON for syntax
lint:
    {{python}} -m py_compile check.py tests/*.py docs/build.py
    {{python}} -m json.tool skill-package.json > /dev/null

# Run the tests. Extra arguments go to unittest: just test tests.test_skill
test *args:
    {{python}} -m unittest discover -s tests -q "$@"

# Check the Markdown of this repository with its own checker
prose:
    {{python}} check.py README.md GUIDE.md docs/checker.md .agents/skills/nossaifd/SKILL.md

# Check skill-package.json with skill-package-maker at a fixed commit
package-lint:
    #!/usr/bin/env bash
    set -euo pipefail
    tool_root="$(mktemp -d)"
    trap 'rm -rf -- "$tool_root"' EXIT
    git clone --quiet https://github.com/rahuldave/agent_skill_package_maker.git "$tool_root/package-maker"
    git -C "$tool_root/package-maker" checkout --quiet 6a5938c49ca71c374dc1a234a4d15134c484a741
    uv run --no-project python "$tool_root/package-maker/skills/skill-package-maker/scripts/lint_skill_bundle.py" .

# Everything a commit must pass: the lint, the tests and the prose
check:
    just lint
    just test
    just prose

# Check that each link to a skill of another package has a fallback, with the checker of a jnterfaces clone: just links ../jnterfaces
links jnterfaces="../jnterfaces":
    find .agents/skills -type f \( -name '*.md' -o -name '*.sh' -o -name '*.py' -o -name '*.yaml' \) -exec {{python}} "$1/scripts/check_skill_links.py" --package . --resolve "$1" {} +

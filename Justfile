# nossaifd: every task is a recipe here. `just` lists them.

# Each word after a recipe's name reaches its commands whole, as "$1", "$2" and so on; "$@" is all of them
set positional-arguments

# Python comes from uv, so the machine needs just and uv only
python := "uv run --no-project --quiet python"

# smalldocs builds the site. The version is fixed, so that each build is the same
smalldocs := "smalldocs==0.5.5"

[private]
default:
    @just --list --unsorted

# Copy the guide, the examples and the checker into the skill, which ships copies of them
sync:
    cp GUIDE.md EXAMPLES.md .agents/skills/nossaifd/references/
    cp check.py .agents/skills/nossaifd/scripts/check.py

# Check the Python and the JSON for syntax
lint:
    {{python}} -m py_compile check.py tests/*.py
    {{python}} -m json.tool skill-package.json > /dev/null

# Run the tests. Extra arguments go to unittest: just test tests.test_skill
test *args:
    {{python}} -m unittest discover -s tests -q "$@"

# Check the Markdown of this repository with its own checker
prose:
    {{python}} check.py README.md GUIDE.md EXAMPLES.md docs/*.md .agents/skills/nossaifd/SKILL.md

# Check skill-package.json with skill-package-maker at a fixed commit
package-lint:
    #!/usr/bin/env bash
    set -euo pipefail
    tool_root="$(mktemp -d)"
    trap 'rm -rf -- "$tool_root"' EXIT
    git clone --quiet https://github.com/rahuldave/agent_skill_package_maker.git "$tool_root/package-maker"
    git -C "$tool_root/package-maker" checkout --quiet 6a5938c49ca71c374dc1a234a4d15134c484a741
    uv run --no-project python "$tool_root/package-maker/skills/skill-package-maker/scripts/lint_skill_bundle.py" .

# Build the site into _site with smalldocs and the theme Folio
site:
    uvx --from {{smalldocs}} smalldocs render .

# Everything a commit must pass: the lint, the tests, the prose and the links of the site
check:
    just lint
    just test
    just prose
    uvx --from {{smalldocs}} smalldocs check .

# Check that each link to a skill of another package has a fallback, with the checker of a jnterfaces clone: just links ../jnterfaces
links jnterfaces="../jnterfaces":
    find .agents/skills -type f \( -name '*.md' -o -name '*.sh' -o -name '*.py' -o -name '*.yaml' \) -exec {{python}} "$1/scripts/check_skill_links.py" --package . --resolve "$1" {} +

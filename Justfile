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

# The commit of oaustegard/claude-skills whose declauding skill, by Oskar Austegard, ships in .agents/skills/declauding
declauding_commit := "6baa7290da972191749acda03c63297e67b3fc26"

# Copy the declauding skill again from that commit, with its licence, and apply sources/declauding.patch
declauding:
    #!/usr/bin/env bash
    set -euo pipefail
    tool_root="$(mktemp -d)"
    trap 'rm -rf -- "$tool_root"' EXIT
    git clone --quiet --filter=blob:none --no-checkout https://github.com/oaustegard/claude-skills.git "$tool_root/src"
    git -C "$tool_root/src" sparse-checkout set --no-cone /declauding/ /LICENSE
    git -C "$tool_root/src" checkout --quiet {{declauding_commit}}
    mkdir -p "$tool_root/stage/.agents/skills"
    cp -R "$tool_root/src/declauding" "$tool_root/stage/.agents/skills/declauding"
    if ! git -C "$tool_root/stage" apply --check "$PWD/sources/declauding.patch" 2>/dev/null; then
        echo "sources/declauding.patch does not apply to commit {{declauding_commit}}. Update or remove it." >&2
        exit 1
    fi
    rm -rf .agents/skills/declauding
    cp -R "$tool_root/src/declauding" .agents/skills/declauding
    cp "$tool_root/src/LICENSE" .agents/skills/declauding/LICENSE
    {{python}} tests/declauding_manifest.py {{declauding_commit}} > "$tool_root/before.json"
    git apply sources/declauding.patch
    {{python}} tests/declauding_manifest.py {{declauding_commit}} "$tool_root/before.json" > sources/declauding.json

# Compare the record of the declauding copy with the files of its commit on GitHub. It needs gh and the network
declauding-verify:
    #!/usr/bin/env bash
    set -euo pipefail
    {{python}} - "$(gh api "repos/oaustegard/claude-skills/git/trees/{{declauding_commit}}?recursive=1")" <<'EOF'
    import json, sys
    tree = {e['path']: e['sha'] for e in json.loads(sys.argv[1])['tree'] if e['type'] == 'blob'}
    files = json.load(open('sources/declauding.json'))['files']
    upstream = {p[len('declauding/'):]: s for p, s in tree.items() if p.startswith('declauding/')}
    upstream['LICENSE'] = tree['LICENSE']
    if upstream != files:
        sys.exit(f'the record differs from GitHub: {sorted(set(upstream.items()) ^ set(files.items()))}')
    print(f'{len(files)} files match the commit {{declauding_commit}} on GitHub')
    EOF

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

# Print the passages of each page that the declauding linter by Oskar Austegard marks as possible model
# prose. It does not fail on them, because a person judges each one. It fails on a missing page, or when
# the linter cannot run
declaude +pages:
    #!/usr/bin/env bash
    status=0
    for page in "$@"; do
        if [ ! -f "$page" ]; then
            echo "no such file: $page" >&2
            status=1
            continue
        fi
        echo "== $page"
        # The linter ends with 1 when it marks a passage, and with 2 or more when it cannot run
        {{python}} -I .agents/skills/declauding/scripts/declaude_lint.py --skip-quoted "$page"
        code=$?
        if [ "$code" -gt 1 ]; then status=$code; fi
    done
    exit "$status"

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

"""The gate of the nossaifd flow: each page that a turn changed must pass the checker and have a recorded pass.

Claude Code and Codex run two hooks of this script.

- `prose_gate.py start` runs when a person sends a message (the UserPromptSubmit hook). It keeps a snapshot of
  the pages: the commit HEAD, and the git blob id of each page that git reports as changed.
- `prose_gate.py hook` runs when the agent tries to end its turn (the Stop hook). It compares the pages with
  the snapshot. A page counts when its content differs from the snapshot, either in the working tree or in a
  commit that the turn made: a commit by the same author, made since the turn started. A pull or a checkout
  brings commits made before the turn, so they do not count, and neither does a merge commit. For each page that counts, it runs check.py, and it looks up the page in the
  record of passes. A page passes when check.py finds no hard problem and the record holds the page as it is
  now. Otherwise the hook blocks the stop once and tells the agent which steps of the nossaifd skill remain.

After step 8 of the nossaifd skill, the agent records each page:

    uv run --no-project --quiet python .agents/skills/nossaifd/scripts/prose_gate.py record page.md

`record` refuses a page that has a hard problem. The record lives in the folder of git (.git/nossaifd),
so every worktree of the repository shares it, and it never shows in git status. The snapshots live in the
folder of git of each worktree. The record is a
promise of the agent, not a proof: the hook cannot see whether the declaude pass ran.

With the commit gates of agent_gest_git_skills, this turn gate stays and asks early, and the gate of the commit
decides. The gates are installed when .agents/stack.json turns on the tasker role. Then the block message says
"run `just prose`". That target gives the pages to a fresh agent, which records each page that it passed. The
steps by hand give a page pass, but not the `prose` record that a commit needs.

`prose_gate.py pages [-z] [PATH...]` prints each path that is a page. is_page is the one rule for pages: the
step prose-check and the `@pages` of the commit gate use it through this command.

The hook fails open: an error never blocks. Claude Code and Codex set stop_hook_active when the agent tries
to stop again after a block, and the hook then lets it stop, so it cannot loop. The environment variable
NOSSAIFD_GATE=off, set before Claude Code or Codex starts, turns the gate off. Submodules are out of scope.
Python 3.11 or later, standard library only.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

sys.dont_write_bytecode = True        # keep __pycache__ out of the installed skill

HERE = Path(__file__).resolve().parent
PAGE = re.compile(r'\.(md|qmd)$')
# Instructions for agents, the copies of skills, the files that a build makes, and changelogs are not pages
SKIP = re.compile(r'(^|/)(AGENTS|CLAUDE|GEMINI)\.md$|^\.agents/|^\.claude/|^\.codex/'
                  r'|(^|/)(node_modules|_site|\.quarto)/|(^|/)CHANGELOG\.md$')
LISTED = 20                           # the most pages that a block message names
CREDIT = 'the declaude skill, by Oskar Austegard'


def is_page(rel):
    """True when a path is a page for a person to read. The path is relative to the root of the repository, with
    `/` between folders, as git prints it. A leading `./` does not change the answer."""
    rel = re.sub(r'^(\./)+', '', rel)
    return bool(PAGE.search(rel)) and not SKIP.search(rel)


def problems(path, check):
    "The hard problems that check.py finds in one page. A page that cannot be read is one hard problem."
    try:
        return check.check(path)[0]
    except (OSError, UnicodeDecodeError) as error:
        return [f'the page cannot be read: {error.strerror if isinstance(error, OSError) else error}']


def gates_installed(root):
    "True when .agents/stack.json of the project turns on the tasker role, which brings the commit gates."
    try:
        choices = json.loads((root / '.agents/stack.json').read_text()).get('choices')
    except (OSError, ValueError, AttributeError):
        return False
    return isinstance(choices, dict) and choices.get('tasker') is True


def checker():
    "The check module next to this script."
    spec = importlib.util.spec_from_file_location('nossaifd_check', HERE / 'check.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(root, *args, stdin=None):
    return subprocess.run(['git', '--no-optional-locks', '--literal-pathspecs', '-C', str(root), *args],
                          capture_output=True, text=True, input=stdin)


def blob(path):
    "The git blob id of a file, or None when it is missing."
    try:
        data = Path(path).read_bytes()
    except OSError:
        return None
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


def git_root(cwd):
    out = git(cwd, 'rev-parse', '--show-toplevel')
    return Path(out.stdout.strip()) if out.returncode == 0 else None


def state(root, shared=False):
    "The folder of the gate inside the folder of git: of this worktree, or shared by every worktree."
    if shared:
        path = Path(git(root, 'rev-parse', '--git-common-dir').stdout.strip()) / 'nossaifd'
    else:
        path = Path(git(root, 'rev-parse', '--git-path', 'nossaifd').stdout.strip())
    return path if path.is_absolute() else root / path


def head(root):
    out = git(root, 'rev-parse', '--verify', '-q', 'HEAD')
    return out.stdout.strip() or None


def git_changed(root):
    "Pages that git reports as changed or new, relative to the root."
    entries, found, i = git(root, 'status', '--porcelain', '-z', '--untracked-files=all').stdout.split('\0'), set(), 0
    while i < len(entries):
        entry = entries[i]
        i += 1
        if len(entry) < 4:
            continue
        code, path = entry[:2], entry[3:]
        if 'R' in code or 'C' in code:
            i += 1                              # the old name of a renamed file follows
        if 'D' not in code and is_page(path):
            found.add(path)
    return found


def snapshot(root):
    return {'head': head(root), 'time': int(time.time()),
            'pages': {p: blob(root / p) for p in sorted(git_changed(root))}}


def snapshot_file(root, session):
    name = re.sub(r'[^A-Za-z0-9_.-]', '_', str(session or 'default'))[:100]
    return state(root) / 'turns' / f'{name}.json'


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def read(path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return None


def committed(root, old, new, since):
    """Pages in the commits that the turn made: commits by the same author, made since the turn started, that
    the start HEAD does not hold. A pull brings commits that were made before, so they do not count. After an
    amend or a rebase, the commits since the fork point count."""
    if not new or new == old:
        return set()
    if old and git(root, 'merge-base', '--is-ancestor', old, new).returncode:
        old = git(root, 'merge-base', old, new).stdout.strip() or None
    email = git(root, 'config', 'user.email').stdout.strip()
    args = ['log', '--no-merges', '--format=%H %ct'] + (['-F', f'--author=<{email}>'] if email else [])
    out = git(root, *args, new, *([f'^{old}'] if old else [])).stdout.split()
    commits = [h for h, t in zip(out[::2], out[1::2]) if since is None or int(t) >= since - 1]
    if not commits:
        return set()
    names = git(root, 'diff-tree', '--stdin', '--root', '-r', '-z', '--name-only', '--no-commit-id',
                stdin='\n'.join(commits) + '\n').stdout
    return {p for p in names.split('\0') if is_page(p)}


def tree_blobs(root, commit, paths):
    "The blob id of each path in a commit. One call for the whole tree, so no list of paths is too long."
    if not commit or not paths:
        return {}
    found = {}
    for entry in filter(None, git(root, 'ls-tree', '-r', '-z', '--full-tree', commit).stdout.split('\0')):
        meta, _, path = entry.partition('\t')
        if path in paths:
            found[path] = meta.split()[2]
    return found


def turn_pages(root, before):
    "The pages whose content differs from the snapshot at the start of the turn."
    now = head(root)
    candidates = git_changed(root) | set(before['pages']) | committed(root, before['head'], now, before.get('time'))
    at_head = tree_blobs(root, before['head'], candidates)
    changed = []
    for rel in sorted(candidates):
        current = blob(root / rel)
        # a stash, a checkout or a reset that gives back the committed page is not a change of the turn
        if current is not None and current != before['pages'].get(rel, at_head.get(rel)) and current != at_head.get(rel):
            changed.append(rel)
    return changed


def load_record(root):
    return read(state(root, shared=True) / 'passes.json') or {}


def gate(root, rels, check=None):
    "The block message for the pages that need work, or None when every page passed."
    saved, hard_pages, unrecorded = load_record(root), [], []
    passed = set(saved.values())                # a renamed page keeps its pass
    for rel in rels:
        if blob(root / rel) in passed:
            continue
        check = check or checker()
        hard = problems(root / rel, check)
        if hard:
            hard_pages.append(f'{rel}: ' + '; '.join(hard[:3]) + (' ...' if len(hard) > 3 else ''))
        else:
            unrecorded.append(rel)
    if not hard_pages and not unrecorded:
        return None

    def listed(items):
        more = len(items) - LISTED
        return [f'- {p}' for p in items[:LISTED]] + ([f'- and {more} more'] if more > 0 else [])
    lines = ['nossaifd: this turn changed pages that have not passed the flow of the nossaifd skill.']
    gates = gates_installed(root)
    if hard_pages:
        lines += ['', 'Hard problems of check.py:' if gates else 'Hard problems of check.py, which steps 4 and 7 fix:']
        lines += listed(hard_pages)
    if unrecorded:
        lines += ['', 'No recorded pass since the last change:'] + listed(unrecorded)
    if gates:
        lines += ['', 'This project has the commit gates, so run `just prose`. It gives the changed pages to a fresh '
                  f'agent, for the plain-writing pass and the pass of {CREDIT}. That agent fixes each hard problem '
                  'and records each page that it passed. Keep each bad example that a page shows on purpose. The '
                  'steps of the skill by hand record a page too, but a commit also needs the `prose` record, and '
                  'only `just prose` gives it.', '',
                  'If this project has no recipe `just prose` yet, do steps 6 to 8 of the nossaifd skill, and '
                  'record each page:', '',
                  f'    uv run --no-project --quiet python "{HERE / "prose_gate.py"}" record PAGE', '',
                  'If a page is not prose for a person to read, do not record it. Tell the user so in one line.',
                  'This hook asks once. It asks about a page again only when the page changes again.']
        return '\n'.join(lines)
    lines += ['', f'For each page, run the steps of the nossaifd skill that remain: the pass of {CREDIT}, in a '
              'subagent that did not write the page (step 6), check.py again (step 7) and the linter once more '
              '(step 8). Keep each bad example that a page shows on purpose. Then record each page:', '',
              f'    uv run --no-project --quiet python "{HERE / "prose_gate.py"}" record PAGE', '',
              'If a page is not prose for a person to read, do not record it. Tell the user so in one line.',
              'This hook asks once. It asks about a page again only when the page changes again.']
    return '\n'.join(lines)


def hook_input(project=None):
    """The input of the hook, and the root of the project. The setting passes the folder of the project, so a cd
    of the agent into another repository does not move the gate there."""
    if os.environ.get('NOSSAIFD_GATE') == 'off':
        return None, None
    data = json.load(sys.stdin)
    return data, git_root(project or data.get('cwd') or os.getcwd())


def start(project=None):
    "UserPromptSubmit hook. Keep the snapshot of the pages at the start of the turn. Prints nothing."
    try:
        data, root = hook_input(project)
        if root is not None:
            save(snapshot_file(root, data.get('session_id')), snapshot(root))
            old = time.time() - 30 * 86400
            for path in (state(root) / 'turns').glob('*.json'):
                if path.stat().st_mtime < old:
                    path.unlink()
    except Exception:  # noqa: BLE001 - a hook fails open
        pass
    return 0


def hook(project=None):
    "Stop hook. Prints a block decision or an empty object, and always exits 0."
    try:
        message = None
        data, root = hook_input(project)
        if root is not None:
            path = snapshot_file(root, data.get('session_id'))
            before = read(path)
            if before is not None and not data.get('stop_hook_active'):
                message = gate(root, turn_pages(root, before))
            if message is None:
                # the next turn starts here, also when the start hook did not run, so a page is asked about once
                save(path, snapshot(root))
        # Codex needs JSON on every exit 0, and an empty object lets the stop go through
        print(json.dumps({'decision': 'block', 'reason': message} if message else {}))
    except Exception:  # noqa: BLE001 - a hook fails open
        print('{}')
    return 0


def resolve(name, root):
    "A page named relative to the folder of the call or to the root of the repository."
    path = Path(name)
    if not path.exists() and not path.is_absolute() and (root / path).exists():
        path = root / path
    return path.resolve()


def record(names):
    "Record each page after its pass. Refuse a page with a hard problem, a missing page or a file outside the repo."
    root = git_root(Path.cwd())
    if root is None:
        print('prose_gate.py record: run it inside the git repository of the pages', file=sys.stderr)
        return 1
    check, saved, status = checker(), load_record(root), 0
    for name in names:
        path = resolve(name, root)
        try:
            rel = path.relative_to(root.resolve()).as_posix()
        except ValueError:
            print(f'{name}: not recorded, it is outside the repository {root}', file=sys.stderr)
            status = 1
            continue
        if not path.is_file():
            print(f'{name}: not recorded, there is no such file', file=sys.stderr)
            status = 1
            continue
        hard = problems(path, check)
        if hard:
            print(f'{rel}: not recorded, {len(hard)} hard problem(s). The first: {hard[0]}', file=sys.stderr)
            status = 1
            continue
        saved[rel] = blob(path)
        print(f'{rel}: recorded')
    save(state(root, shared=True) / 'passes.json', dict(sorted(saved.items())))
    return status


def status():
    "Print each page that git reports as changed and that still needs work. Exit 1 when one does."
    root = git_root(Path.cwd())
    message = gate(root, sorted(git_changed(root))) if root else None
    print(message or 'nossaifd: every changed page passed.')
    return 1 if message else 0


def check_diff(base):
    "For a workflow: run check.py on each page that HEAD adds or changes since base. Exit 1 on a hard problem."
    root = git_root(Path.cwd())
    out = git(root, 'diff', '-z', '--name-only', '--no-renames', '--diff-filter=AM', f'{base}...HEAD')
    if out.returncode:
        print(out.stderr, file=sys.stderr)
        return 2
    check, status = checker(), 0
    rels = [p for p in filter(None, out.stdout.split('\0')) if is_page(p)]
    for rel in rels:
        hard = problems(root / rel, check)
        for problem in hard:
            print(f'{rel}: {problem}')
        status |= bool(hard)
    print(f'nossaifd: checked {len(rels)} page(s), {"a hard problem" if status else "no hard problem"}.')
    return int(status)


def pages(args, stdin=None):
    """Print each path that is_page accepts, in the order given, for prose-check and the `@pages` of the commit
    gate. The paths come from the arguments, or from standard input when no path follows the options. With -z,
    standard input and the output put NUL after each path; without it, a newline. A path is relative to the
    root of the repository, as git prints it. An absolute path counts by its path from the root of its
    repository (see relative). The names alone count: a deleted file can be a page. Exit 0, also when no path is a page, and 2 on an unknown option."""
    nul = False
    while args and args[0].startswith('-'):
        option, args = args[0], args[1:]
        if option == '--':
            break
        if option != '-z':
            print(f'prose_gate.py pages: unknown option {option}', file=sys.stderr)
            return 2
        nul = True
    sep = '\0' if nul else '\n'
    if not args:
        source = stdin or sys.stdin
        text = source.read() if source is not None else ''
        args = [p.removesuffix('\r') if not nul else p for p in text.split(sep)]
        args = [p for p in args if p]
    roots = {}
    for name in args:
        if is_page(relative(name, roots)):
            sys.stdout.write(name + sep)
    return 0


def relative(name, roots):
    """A path as the rule of pages reads it. An absolute path becomes its path from the root of its repository,
    with no symlink followed below that root. A path outside any repository stays as written."""
    if not os.path.isabs(name):
        return name
    path = os.path.abspath(name)
    folder = Path(path).parent
    while not folder.is_dir() and folder != folder.parent:
        folder = folder.parent                  # a deleted page: start from a folder that exists
    for start in (Path.cwd(), folder):
        if start not in roots:
            roots[start] = git_root(start)
        root = roots[start]
        if root is None:
            continue
        real_root = os.path.realpath(root)
        # the folder above the path that is the root, maybe through a symlink above the repository
        for above in Path(path).parents:
            if os.path.realpath(above) == real_root:
                return Path(path).relative_to(above).as_posix()
    return name


def main(argv):
    command = argv[1:2]
    if command == ['hook'] and len(argv) <= 3:
        return hook(argv[2] if len(argv) == 3 else None)
    if command == ['start'] and len(argv) <= 3:
        return start(argv[2] if len(argv) == 3 else None)
    if command == ['record'] and len(argv) > 2:
        return record(argv[2:])
    if command == ['status']:
        return status()
    if command == ['check-diff'] and len(argv) == 3:
        return check_diff(argv[2])
    if command == ['pages']:
        return pages(argv[2:])
    print(__doc__)
    print('Usage: prose_gate.py hook [ROOT] | start [ROOT] | record PAGE... | status | check-diff BASE'
          ' | pages [-z] [PATH...]', file=sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv))

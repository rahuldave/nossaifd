"""Check the gate of the nossaifd flow: the hooks at the start and the end of a turn, the record of passes, the
check of a pull request, and the files that a project installs."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / '.agents/skills/nossaifd'
GATE = SKILL / 'scripts/prose_gate.py'
CLEAN = '# Notes\n\nThe build runs in four minutes. The cache holds the last two builds.\n'
MORE = CLEAN + '\nThe tests run on each push.\n'
HARD = "# Notes\n\nThe build isn't fast.\n"
# A commit before the turn has a date an hour ago. A commit of the turn has the date of now
PAST = {'GIT_COMMITTER_DATE': f'@{int(time.time()) - 3600} +0000', 'GIT_AUTHOR_DATE': f'@{int(time.time()) - 3600} +0000'}
# The variables of CI turn on the CI mode of check-changed. The runner of GitHub sets them, also for these tests,
# so every test starts without them, and a test of the CI mode sets them itself
def ci_variable(name):
    "CI and every variable of GitHub, such as GITHUB_BASE_REF, GITHUB_REF and GITHUB_EVENT_PATH."
    return name == 'CI' or name.startswith('GITHUB_')


for variable in [name for name in os.environ if ci_variable(name)]:
    del os.environ[variable]


def listing(folder):
    "Each file under a folder, with its size and the time of its last change, to see what a run wrote."
    return {p.relative_to(folder).as_posix(): (p.stat().st_size, p.stat().st_mtime_ns)
            for p in sorted(Path(folder).rglob('*')) if p.is_file()}


class Project:
    "A git repository in a temporary folder, with one committed page."

    def __init__(self, temp):
        self.root = Path(temp)
        self.git('init', '-q', '-b', 'main')
        self.git('config', 'user.email', 'test@example.com')
        self.git('config', 'user.name', 'Test')
        self.write('README.md', CLEAN)
        self.git('add', '-A')
        self.git('commit', '-qm', 'start')

    def git(self, *args, env=None, cwd=None):
        return subprocess.run(['git', *args], cwd=cwd or self.root, check=True, capture_output=True, text=True,
                              env={**os.environ, **PAST, **(env or {})}).stdout

    def commit_in_turn(self, *args, env=None, cwd=None):
        now = f'@{int(time.time())} +0000'
        return self.git('commit', *args, env={'GIT_COMMITTER_DATE': now, 'GIT_AUTHOR_DATE': now, **(env or {})},
                        cwd=cwd)

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def run(self, command, data, env=None):
        command = [command] if isinstance(command, str) else command
        out = subprocess.run([sys.executable, str(GATE), *command], input=json.dumps(data), capture_output=True,
                             text=True, env={**os.environ, **(env or {})})
        return out.returncode, out.stdout

    def start(self, session='s1', cwd=None):
        return self.run('start', {'cwd': str(cwd or self.root), 'session_id': session})

    def hook(self, active=False, session='s1', env=None, cwd=None, project=None):
        command = ['hook', str(project)] if project else ['hook']
        code, out = self.run(command, {'cwd': str(cwd or self.root), 'session_id': session,
                                       'stop_hook_active': active}, env)
        return code, json.loads(out)

    def blocked(self, session='s1', cwd=None):
        "The block message of the end of the turn, or None."
        return self.hook(session=session, cwd=cwd)[1].get('reason')

    def record(self, *pages, cwd=None):
        return subprocess.run([sys.executable, str(GATE), 'record', *pages], cwd=cwd or self.root,
                              capture_output=True, text=True)


class TurnTest(unittest.TestCase):
    "Which pages count as changed by a turn."

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Project(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_a_turn_that_changed_no_page_lets_the_stop_go_through(self):
        self.project.start()
        self.assertEqual(self.project.hook(), (0, {}))

    def test_a_page_that_the_turn_changed_blocks_once(self):
        self.project.start()
        self.project.write('README.md', MORE)
        code, out = self.project.hook()
        self.assertEqual((code, out['decision']), (0, 'block'))
        self.assertIn('README.md', out['reason'])
        self.assertIn('record PAGE', out['reason'])
        # Claude Code and Codex set stop_hook_active on the next try, and the hook lets the stop go through
        self.assertEqual(self.project.hook(active=True), (0, {}))

    def test_a_page_changed_before_the_turn_does_not_block(self):
        "A draft that the person is editing, or a page of an earlier turn, is not a page of this turn"
        self.project.write('README.md', MORE)
        self.project.write('draft.md', CLEAN)
        self.project.start()
        self.assertIsNone(self.project.blocked())
        self.project.start()                    # the next turn: still nothing that this turn changed
        self.assertIsNone(self.project.blocked())

    def test_a_page_that_was_blocked_once_is_not_asked_again_until_it_changes(self):
        self.project.start()
        self.project.write('README.md', MORE)
        self.assertIsNotNone(self.project.blocked())
        self.project.start()
        self.assertIsNone(self.project.blocked())
        self.project.write('README.md', MORE + '\nThe cache is local.\n')
        self.assertIsNotNone(self.project.blocked())

    def test_a_page_that_the_turn_committed_counts(self):
        self.project.start()
        self.project.write('README.md', MORE)
        self.project.commit_in_turn('-qam', 'edit')
        self.assertIn('README.md', self.project.blocked())

    def test_a_dirty_page_committed_without_change_does_not_count(self):
        self.project.write('README.md', MORE)
        self.project.start()
        self.project.commit_in_turn('-qam', 'edit')
        self.assertIsNone(self.project.blocked())

    def test_a_dirty_page_that_the_turn_changed_and_committed_under_another_name_counts(self):
        self.project.write('README.md', MORE)
        self.project.start()
        self.project.write('README.md', MORE + '\nThe cache is local.\n')
        self.project.commit_in_turn('-qam', 'edit', env={'GIT_AUTHOR_EMAIL': 'agent@example.com'})
        self.assertIn('README.md', self.project.blocked())

    def test_a_pull_of_my_own_work_from_before_the_turn_does_not_count(self):
        self.project.git('checkout', '-qb', 'feat')
        self.project.write('docs/feat.md', CLEAN)
        self.project.git('add', '-A')
        self.project.git('commit', '-qm', 'mine, made before the turn')
        self.project.git('checkout', '-q', 'main')
        self.project.start()
        self.project.git('merge', '-q', '--ff-only', 'feat')
        self.assertIsNone(self.project.blocked())

    def test_a_pass_recorded_in_another_worktree_counts_here(self):
        other = self.project.root.parent / (self.project.root.name + '-wt')
        self.project.git('worktree', 'add', '-q', '-b', 'feat', str(other))
        try:
            self.project.start(cwd=other)
            (other / 'docs').mkdir()
            (other / 'docs/feat.md').write_text(CLEAN)
            self.assertEqual(self.project.record('docs/feat.md', cwd=other).returncode, 0)
            self.project.git('add', '-A', cwd=other)
            self.project.commit_in_turn('-qm', 'feat', cwd=other)
            self.assertIsNone(self.project.blocked(cwd=other))
            self.project.start()
            self.project.commit_in_turn('-q', '--allow-empty', '-m', 'later')     # not an ancestor of feat
            self.project.git('merge', '-q', '--no-edit', 'feat', env={'GIT_COMMITTER_DATE': f'@{int(time.time())} +0000'})
            self.assertIsNone(self.project.blocked())
        finally:
            self.project.git('worktree', 'remove', '--force', str(other))

    def test_the_gate_stays_in_the_project_when_the_agent_changes_folder(self):
        with tempfile.TemporaryDirectory() as temp:
            elsewhere = Project(temp)
            self.project.start()
            self.project.write('README.md', MORE)
            elsewhere.write('README.md', HARD)
            code, out = self.project.hook(cwd=elsewhere.root, project=self.project.root)
            self.assertIn('README.md', out['reason'])
            self.assertNotIn('a contraction', out['reason'])
            self.assertFalse((elsewhere.root / '.git/nossaifd').exists())

    def test_without_a_start_hook_a_page_is_asked_about_once(self):
        self.project.hook()                     # the first stop of the session keeps a snapshot
        self.project.write('README.md', MORE)
        self.assertIsNotNone(self.project.blocked())
        self.assertEqual(self.project.hook(active=True), (0, {}))
        self.assertIsNone(self.project.blocked())     # the next turn, with no start hook
        self.assertIsNone(self.project.blocked())

    def test_an_amend_of_the_start_commit_counts(self):
        self.project.start()
        self.project.write('README.md', MORE)
        self.project.git('add', '-A')
        self.project.commit_in_turn('-q', '--amend', '--no-edit')
        self.assertIn('README.md', self.project.blocked())

    def test_a_page_of_the_first_commit_of_a_new_repository_counts(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            project = Project.__new__(Project)
            project.root = root
            project.git('init', '-q')
            project.git('config', 'user.email', 'test@example.com')
            project.git('config', 'user.name', 'Test')
            project.start()
            project.write('README.md', MORE)
            project.git('add', '-A')
            project.commit_in_turn('-qm', 'first')
            self.assertIn('README.md', project.blocked())

    def test_a_stash_of_a_page_that_was_dirty_before_the_turn_does_not_count(self):
        self.project.write('README.md', MORE)
        self.project.start()
        self.project.git('stash', '-q')
        self.assertIsNone(self.project.blocked())

    def test_an_email_with_the_signs_of_a_pattern_still_finds_the_commits_of_the_turn(self):
        self.project.git('config', 'user.email', 'a[b]+c@example.com')
        self.project.start()
        self.project.write('README.md', MORE)
        self.project.commit_in_turn('-qam', 'edit')
        self.assertIn('README.md', self.project.blocked())

    def test_a_merge_of_the_work_of_another_person_does_not_count(self):
        self.project.git('checkout', '-qb', 'other')
        self.project.write('docs/theirs.md', CLEAN)
        self.project.git('add', '-A')
        self.project.git('commit', '-qm', 'theirs', env={'GIT_AUTHOR_EMAIL': 'other@example.com'})
        self.project.git('checkout', '-q', 'main')
        self.project.start()
        self.project.git('merge', '-q', '--ff-only', 'other')
        self.assertIsNone(self.project.blocked())

    def test_a_checkout_of_another_branch_does_not_count(self):
        self.project.git('checkout', '-qb', 'other')
        self.project.write('docs/mine.md', CLEAN)
        self.project.git('add', '-A')
        self.project.git('commit', '-qm', 'mine')
        self.project.git('checkout', '-q', 'main')
        self.project.write('README.md', MORE)
        self.project.git('commit', '-qam', 'main moves on')
        self.project.start()
        self.project.git('checkout', '-q', 'other')
        self.assertIsNone(self.project.blocked())

    def test_a_new_page_in_a_new_folder_and_a_qmd_page_count(self):
        self.project.start()
        self.project.write('docs/setup.md', CLEAN)
        self.project.write('docs/index.qmd', CLEAN)
        reason = self.project.blocked()
        self.assertIn('docs/setup.md', reason)
        self.assertIn('docs/index.qmd', reason)

    def test_a_renamed_page_counts_once(self):
        self.project.start()
        (self.project.root / 'docs').mkdir()
        self.project.git('mv', 'README.md', 'docs/README.md')
        self.project.write('docs/README.md', MORE)
        self.assertIn('docs/README.md', self.project.blocked())

    def test_instructions_for_agents_copies_of_skills_and_changelogs_are_not_pages(self):
        self.project.start()
        for name in ('AGENTS.md', 'docs/AGENTS.md', 'CLAUDE.md', '.agents/skills/x/SKILL.md', '.claude/notes.md',
                     '.codex/notes.md', 'CHANGELOG.md', 'docs/CHANGELOG.md', 'notes.txt', '_site/a.md'):
            self.project.write(name, HARD)
        self.assertIsNone(self.project.blocked())

    def test_each_session_keeps_its_own_start(self):
        self.project.start('a')
        self.project.write('README.md', MORE)
        self.project.start('b')
        self.assertIsNone(self.project.blocked('b'))
        self.assertIsNotNone(self.project.blocked('a'))

    def test_with_no_start_hook_the_first_stop_starts_the_comparison(self):
        self.project.write('README.md', MORE)
        self.assertIsNone(self.project.blocked())
        self.project.write('README.md', MORE + '\nThe cache is local.\n')
        self.assertIsNotNone(self.project.blocked())

    def test_the_block_message_names_at_most_twenty_pages_and_credits_the_skill(self):
        self.project.start()
        for i in range(25):
            self.project.write(f'docs/p{i}.md', CLEAN)
        reason = self.project.blocked()
        self.assertEqual(reason.count('\n- docs/p'), 20)
        self.assertIn('- and 5 more', reason)
        self.assertIn('declaude skill, by Oskar Austegard', reason)
        self.assertNotIn('the stop goes through', reason)
        self.assertIn('asks once', reason)

    def test_the_gate_leaves_nothing_in_git_status(self):
        "It compares the folder of the scripts before and after, so a file that another tool left there is no fault"
        before = listing(SKILL / 'scripts')
        self.project.start()
        self.project.write('README.md', MORE)
        self.project.blocked()
        self.assertEqual(self.project.record('README.md').returncode, 0)
        self.assertEqual(self.project.git('status', '--porcelain'), ' M README.md\n')
        self.assertEqual(listing(SKILL / 'scripts'), before)

    def test_a_stale_pyc_of_another_tool_is_no_fault_and_the_gate_writes_none(self):
        with tempfile.TemporaryDirectory() as other:
            scripts = Path(other) / 'scripts'
            scripts.mkdir()
            for name in ('check.py', 'prose_gate.py'):
                (scripts / name).write_bytes((SKILL / 'scripts' / name).read_bytes())
            (scripts / '__pycache__').mkdir()
            (scripts / '__pycache__/check.cpython-311.pyc').write_bytes(b'stale')
            before = listing(scripts)
            self.project.start()
            self.project.write('README.md', MORE)
            data = json.dumps({'cwd': str(self.project.root), 'session_id': 's1'})
            out = subprocess.run([sys.executable, str(scripts / 'prose_gate.py'), 'hook'], input=data,
                                 capture_output=True, text=True)
            self.assertIn('README.md', json.loads(out.stdout)['reason'])
            self.assertEqual(listing(scripts), before)

    def test_the_hook_fails_open_and_can_be_turned_off(self):
        out = subprocess.run([sys.executable, str(GATE), 'hook'], input='not json', capture_output=True, text=True)
        self.assertEqual((out.returncode, json.loads(out.stdout)), (0, {}))
        self.project.start()
        self.project.write('README.md', HARD)
        self.assertEqual(self.project.hook(env={'NOSSAIFD_GATE': 'off'}), (0, {}))

    def test_a_folder_outside_git_lets_the_stop_go_through(self):
        with tempfile.TemporaryDirectory() as other:
            project = Project.__new__(Project)
            project.root = Path(other)
            self.assertEqual(project.start(), (0, ''))
            self.assertEqual(project.hook(), (0, {}))


    def test_status_skips_a_deleted_page_and_the_old_name_of_a_renamed_page(self):
        self.project.write('docs/old.md', CLEAN)
        self.project.write('gone.md', CLEAN)
        self.project.git('add', '-A')
        self.project.git('commit', '-qm', 'pages')
        self.project.git('mv', 'docs/old.md', 'docs/new.md')
        (self.project.root / 'gone.md').unlink()
        out = subprocess.run([sys.executable, str(GATE), 'status'], cwd=self.project.root, capture_output=True,
                             text=True)
        self.assertNotIn('Traceback', out.stderr)
        self.assertIn('- docs/new.md', out.stdout)
        self.assertNotIn('old.md', out.stdout)
        self.assertNotIn('gone.md', out.stdout)

    def test_the_start_hook_removes_snapshots_older_than_thirty_days(self):
        self.project.start('old')
        self.project.start('new')
        turns = self.project.root / '.git/nossaifd/turns'
        month = time.time() - 31 * 86400
        os.utime(turns / 'old.json', (month, month))
        self.project.start('new')
        self.assertEqual(sorted(p.name for p in turns.iterdir()), ['new.json'])


class RecordTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Project(self.temp.name)
        self.project.start()

    def tearDown(self):
        self.temp.cleanup()

    def test_a_hard_problem_blocks_and_record_refuses_the_page(self):
        self.project.write('README.md', HARD)
        self.assertIn('a contraction', self.project.blocked())
        refused = self.project.record('README.md')
        self.assertEqual(refused.returncode, 1)
        self.assertIn('not recorded', refused.stderr)
        self.project.write('README.md', HARD + '\nMore.\n')
        self.assertIn('a contraction', self.project.blocked())

    def test_a_recorded_page_passes_until_it_changes_again(self):
        self.project.write('README.md', MORE)
        self.assertEqual(self.project.record('README.md').returncode, 0)
        self.assertIsNone(self.project.blocked())
        self.project.write('README.md', MORE + '\nThe cache is local.\n')
        self.assertIsNotNone(self.project.blocked())

    def test_a_page_named_from_a_subfolder_or_from_the_root_is_recorded_by_its_root_path(self):
        self.project.write('docs/a.md', CLEAN)
        self.project.write('docs/b.md', MORE)
        sub = self.project.root / 'docs'
        self.assertEqual(self.project.record('a.md', 'docs/b.md', cwd=sub).returncode, 0)
        self.assertIsNone(self.project.blocked())

    def test_a_name_means_the_page_in_the_folder_of_the_call_first(self):
        self.project.write('a.md', HARD)
        self.project.write('docs/a.md', CLEAN)
        out = self.project.record('a.md', cwd=self.project.root / 'docs')
        self.assertEqual((out.returncode, out.stdout), (0, 'docs/a.md: recorded, checked by check.py of the skill\n'))

    def test_a_bad_name_is_refused_and_the_other_pages_are_still_recorded(self):
        self.project.write('README.md', MORE)
        with tempfile.TemporaryDirectory() as other:
            outside = Path(other) / 'x.md'
            outside.write_text(CLEAN)
            out = self.project.record('README.md', str(outside), 'missing.md', 'docs')
        self.assertEqual(out.returncode, 1)
        self.assertIn('outside the repository', out.stderr)
        self.assertIn('no such file', out.stderr)
        self.assertNotIn('Traceback', out.stderr)
        self.assertIsNone(self.project.blocked())

    def test_a_recorded_page_keeps_its_pass_when_it_is_renamed(self):
        self.project.write('README.md', MORE)
        self.project.record('README.md')
        self.project.git('mv', 'README.md', 'GUIDE.md')
        self.assertIsNone(self.project.blocked())

    def test_record_outside_git_says_so(self):
        with tempfile.TemporaryDirectory() as other:
            (Path(other) / 'a.md').write_text(CLEAN)
            out = self.project.record('a.md', cwd=other)
        self.assertEqual(out.returncode, 1)
        self.assertIn('git repository', out.stderr)


class CheckDiffTest(unittest.TestCase):
    "The check of a pull request, which the workflow runs."

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Project(self.temp.name)
        self.project.git('checkout', '-qb', 'topic')

    def tearDown(self):
        self.temp.cleanup()

    def check(self):
        return subprocess.run([sys.executable, str(GATE), 'check-diff', 'main'], cwd=self.project.root,
                              capture_output=True, text=True)

    def commit(self):
        self.project.git('add', '-A')
        self.project.git('commit', '-qm', 'change')

    def test_a_renamed_and_edited_page_is_checked(self):
        (self.project.root / 'docs').mkdir()
        self.project.git('mv', 'README.md', 'docs/README.md')
        self.project.write('docs/README.md', CLEAN + "\nThe build isn't slow.\n")   # similar, so git sees a rename
        self.commit()
        out = self.check()
        self.assertEqual(out.returncode, 1)
        self.assertIn('docs/README.md', out.stdout)

    def test_a_changelog_and_instructions_for_agents_are_skipped(self):
        for name in ('CHANGELOG.md', 'docs/AGENTS.md', '.agents/skills/x/SKILL.md', 'node_modules/a.md'):
            self.project.write(name, HARD)
        self.commit()
        out = self.check()
        self.assertEqual(out.returncode, 0, out.stdout)
        self.assertIn('checked 0 page(s)', out.stdout)

    def test_a_link_that_became_a_page_is_checked(self):
        (self.project.root / 'link.md').symlink_to('README.md')
        self.commit()
        self.project.git('checkout', '-qb', 'later')
        (self.project.root / 'link.md').unlink()
        self.project.write('link.md', HARD)
        self.commit()
        out = subprocess.run([sys.executable, str(GATE), 'check-diff', 'topic'], cwd=self.project.root,
                             capture_output=True, text=True)
        self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
        self.assertIn('link.md: checked by', out.stdout)

    def test_clean_pages_pass(self):
        self.project.write('docs/a page.md', CLEAN)
        self.commit()
        out = self.check()
        self.assertEqual(out.returncode, 0, out.stdout)
        self.assertIn('checked 1 page(s)', out.stdout)


def page_filter(gate=GATE):
    """The --diff-filter of the code: the one value that the page listings of prose_gate.py, diff_pages and
    changed_pages, pass to git diff. It is read from the source, so a change to the code changes it here.
    It raises ValueError when a listing is missing or the two listings differ."""
    import ast
    tree = ast.parse(Path(gate).read_text(encoding='utf-8'))
    found = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in ('diff_pages', 'changed_pages'):
            found[node.name] = [n.value for n in ast.walk(node) if isinstance(n, ast.Constant)
                                and isinstance(n.value, str) and n.value.startswith('--diff-filter=')]
    if set(found) != {'diff_pages', 'changed_pages'}:
        raise ValueError(f'a listing of pages is missing: {sorted(found)}')
    values = {v for vs in found.values() for v in vs}
    if not all(len(vs) == 1 for vs in found.values()) or len(values) != 1:
        raise ValueError(f'the listings differ: {found}')
    return values.pop()


# A --diff-filter with = before its value, which may be quoted. Or a --diff-filter with a space before its value,
# or as two quoted words of Python, ['--diff-filter', 'AM']. Those two forms count only a value of capitals, so
# that a word of prose after the option, as in "pass --diff-filter to git", is not read as a value
FILTER = re.compile(r'''--diff-filter(?:=["']?([A-Za-z*]*)|(?:\s+["']?|['"],\s*['"])([A-Z*]+)(?![a-z]))''')


def stale_filters(text, code):
    """Each line of text whose --diff-filter is not the filter of the code, as 'number: filter'. The filter D,
    which lists the deleted files, may differ. None when the text names no --diff-filter."""
    want = code.removeprefix('--diff-filter=')
    named, stale = False, []
    for number, line in enumerate(text.splitlines(), 1):
        for after_equals, after_space in FILTER.findall(line):
            value = after_equals or after_space
            named = True
            if value not in (want, 'D'):
                stale.append(f'{number}: --diff-filter={value}')
    return stale if named else None


def pages(*args, stdin='', cwd=None):
    "Run prose_gate.py pages. Return the exit code, the output and the errors."
    out = subprocess.run([sys.executable, str(GATE), 'pages', *args], input=stdin, capture_output=True, text=True,
                         cwd=cwd)
    return out.returncode, out.stdout, out.stderr


class PagesTest(unittest.TestCase):
    "The command pages, the one rule for pages that prose-check and the @pages of the commit gate use."

    NAMES = ['README.md', 'docs/index.qmd', './docs/a.md', 'CHANGELOG.md', 'docs/CHANGELOG.md', 'AGENTS.md',
             '.agents/skills/x/SKILL.md', './.agents/x.md', 'notes.txt', '_site/a.md']
    PAGES = ['README.md', 'docs/index.qmd', './docs/a.md']

    def test_the_arguments_give_the_pages_in_their_order(self):
        self.assertEqual(pages(*self.NAMES), (0, ''.join(p + '\n' for p in self.PAGES), ''))

    def test_standard_input_gives_the_paths_one_on_each_line_or_with_nul_after_each(self):
        self.assertEqual(pages(stdin='\n'.join(self.NAMES) + '\n')[1], ''.join(p + '\n' for p in self.PAGES))
        self.assertEqual(pages('-z', stdin='\0'.join(self.NAMES + ['a\nb.md']) + '\0')[1],
                         ''.join(p + '\0' for p in self.PAGES + ['a\nb.md']))

    def test_no_page_exits_0_and_an_unknown_option_exits_2(self):
        self.assertEqual(pages('CHANGELOG.md'), (0, '', ''))
        self.assertEqual(pages(stdin=''), (0, '', ''))
        code, _, err = pages('-x', 'README.md')
        self.assertEqual(code, 2)
        self.assertIn('unknown option -x', err)
        self.assertEqual(pages('--', '-notes.md')[:2], (0, '-notes.md\n'))

    def test_an_absolute_path_counts_by_its_path_from_the_root(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Project(temp)
            skill, page = project.root / '.agents/x.md', project.root / 'docs/a.md'
            self.assertEqual(pages(str(skill), str(page), cwd=project.root)[1], f'{page}\n')

    def test_a_symlink_inside_the_repository_is_not_followed_for_an_absolute_path(self):
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
            project = Project(temp)
            (project.root / '.agents').mkdir()
            (project.root / '.agents/skills').symlink_to(outside)        # skills installed from elsewhere
            (Path(outside) / 'x.md').write_text(CLEAN)
            project.write('.agents/guide.md', CLEAN)
            (project.root / 'docs').mkdir()
            (project.root / 'docs/guide.md').symlink_to(project.root / '.agents/guide.md')
            names = ['.agents/skills/x.md', 'docs/guide.md']
            relative = pages(*names, cwd=project.root)[1]
            self.assertEqual(relative, 'docs/guide.md\n')
            absolute = pages(*[str(project.root / n) for n in names], cwd=project.root)[1]
            self.assertEqual(absolute, f'{project.root / "docs/guide.md"}\n')

    def test_an_absolute_path_in_another_repository_or_deleted_counts_from_its_own_root(self):
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as other:
            project, elsewhere = Project(temp), Project(other)
            names = [str(elsewhere.root / '.agents/x.md'), str(elsewhere.root / 'gone/a.md')]
            self.assertEqual(pages(*names, cwd=project.root)[1], f'{names[1]}\n')

    def test_closed_standard_input_and_crlf_lines(self):
        out = subprocess.run([sys.executable, str(GATE), 'pages'], stdin=subprocess.DEVNULL, capture_output=True,
                             text=True)
        self.assertEqual((out.returncode, out.stdout), (0, ''))
        out = subprocess.run(f'"{sys.executable}" "{GATE}" pages <&-', shell=True, capture_output=True, text=True)
        self.assertEqual((out.returncode, out.stdout, out.stderr), (0, '', ''))
        self.assertEqual(pages(stdin='a.md\r\nCHANGELOG.md\r\n')[1], 'a.md\n')

    def test_the_hook_and_the_command_accept_the_same_pages(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Project(temp)
            project.start()
            names = [n for n in self.NAMES if not n.startswith('./')] + ['docs/a page.md', 'Docs/AGENTS.md']
            for name in names:
                project.write(name, MORE)
            project.git('mv', 'README.md', 'docs/README.md')
            names = [n for n in names if n != 'README.md'] + ['docs/README.md']
            reason = project.blocked()
            listed = {line[2:].removesuffix(' (checked by check.py of the skill)')
                      for line in reason.split('\n') if line.startswith('- ')}
            self.assertNotIn('HARD', reason)
            self.assertEqual(listed, set(pages('-z', *names)[1].split('\0')) - {''})
            # the command that prose-check and the base task use gives the same pages as the hook
            out = subprocess.run(f'git add -A && git diff -z --name-only --no-renames {page_filter()} HEAD | '
                                 f'"{sys.executable}" "{GATE}" pages -z', shell=True, cwd=project.root,
                                 capture_output=True, text=True)
            self.assertEqual(set(out.stdout.split('\0')) - {''}, listed)

    def test_another_program_can_load_the_script_and_call_is_page(self):
        code = ('import importlib.util, sys; sys.dont_write_bytecode = True; '
                f'spec = importlib.util.spec_from_file_location("prose_gate", {str(GATE)!r}); '
                'gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate); '
                'print(gate.is_page("docs/a.qmd"), gate.is_page("CHANGELOG.md"), gate.is_page("./.agents/a.md"))')
        out = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True)
        self.assertEqual(out.stdout, 'True False False\n', out.stderr)


class DiffFilterTest(unittest.TestCase):
    "Each page that shows a git diff of the pages shows the filter of the code."

    # The files that may differ: the code itself, and this file, which holds the pattern
    SKIP = {'.agents/skills/nossaifd/scripts/prose_gate.py', 'tests/test_prose_gate.py'}

    def test_every_diff_filter_in_the_repository_is_the_filter_of_the_code(self):
        code = page_filter()
        self.assertRegex(code, r'^--diff-filter=[A-Z]+$')
        out = subprocess.run(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], cwd=REPO,
                             capture_output=True, text=True, check=True)
        seen, wrong = set(), []
        for name in sorted(set(filter(None, out.stdout.split('\0')))):
            path = REPO / name
            # books/ is left out on purpose. It has no copy here now, but a checkout may hold one
            if name.startswith('books/') or name in self.SKIP or not path.is_file() or path.is_symlink():
                continue
            try:
                text = path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                continue
            found = stale_filters(text, code)
            if found is not None:
                seen.add(name)
                wrong += [f'{name}:{line}' for line in found]
        self.assertEqual(wrong, [], f'the code uses {code}')
        # the two pages that show the command must stay in the scan, or the test checks nothing
        self.assertLessEqual({'docs/flow.md', '.agents/skills/nossaifd/references/targets/prose.md'}, seen)

    def test_the_scan_finds_each_spelling_of_a_stale_filter(self):
        code = '--diff-filter=AMT'
        for text in ['git diff --diff-filter=AM HEAD', 'git diff --diff-filter AM HEAD',
                     "['--diff-filter', 'AM']", 'as `--diff-filter=AM` does', 'git diff --diff-filter=ACMT']:
            with self.subTest(text=text):
                self.assertEqual(len(stale_filters(text, code)), 1)

    def test_the_scan_accepts_the_filter_of_the_code_and_the_filter_of_deletions(self):
        code = '--diff-filter=AMT'
        for text in ['git diff --diff-filter=AMT HEAD', 'as `--diff-filter=AMT` does.',
                     "['--diff-filter', 'AMT']", 'Use `--diff-filter=D` to list deletions.',
                     'git diff --diff-filter="AMT" HEAD', "git diff --diff-filter='AMT' HEAD"]:
            with self.subTest(text=text):
                self.assertEqual(stale_filters(text, code), [])
        self.assertIsNone(stale_filters('git diff HEAD', code))
        # a word of prose after the option, or a line that goes on after a backslash, is no value
        self.assertIsNone(stale_filters('pass --diff-filter to git', code))
        self.assertIsNone(stale_filters('git diff --diff-filter \\', code))

    def test_the_code_filter_is_read_from_the_code_and_fails_loudly(self):
        code = page_filter()
        self.assertRegex(code, r'^--diff-filter=[A-Z]+$')
        source = GATE.read_text(encoding='utf-8')
        listing = f"'{code}', *revs"
        self.assertEqual(source.count(listing), 1)
        with tempfile.TemporaryDirectory() as temp:
            other = Path(temp) / 'prose_gate.py'
            # Z is no filter of git, so it differs from the filter of the code, whatever that is
            other.write_text(source.replace(listing, "'--diff-filter=Z', *revs"), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'the listings differ'):
                page_filter(other)
            other.write_text(source.replace('def diff_pages(', 'def listed_pages('), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'a listing of pages is missing'):
                page_filter(other)


class CommitGatesTest(unittest.TestCase):
    "The turn gate beside the commit gates of agent_gest_git_skills."

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Project(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def stack(self, text):
        self.project.write('.agents/stack.json', text)

    def test_with_the_tasker_role_the_block_says_run_just_prose(self):
        self.stack(json.dumps({'version': 2, 'choices': {'prose': True, 'tasker': True}}))
        self.project.start()
        self.project.write('README.md', MORE)
        self.project.write('docs/bad.md', HARD)
        reason = self.project.blocked()
        self.assertIn('run `just prose`', reason)
        self.assertIn('README.md', reason)
        self.assertIn('a contraction', reason)
        self.assertIn('declaude skill, by Oskar Austegard', reason)
        self.assertIn('asks once', reason)
        self.assertNotIn('steps 4 and 7', reason)
        self.assertIn('Keep each bad example', reason)

    def test_a_project_with_the_tasker_role_but_no_recipe_just_prose_still_gets_the_record_command(self):
        "A project of an older tasker role has no `just prose`, so the message keeps the steps by hand"
        self.stack(json.dumps({'choices': {'tasker': True}}))
        self.project.start()
        self.project.write('README.md', MORE)
        reason = self.project.blocked()
        self.assertIn('no recipe `just prose` yet', reason)
        self.assertIn('record PAGE', reason)
        self.assertIn('do not record it', reason)

    def test_a_page_that_cannot_be_read_blocks_and_the_other_pages_are_still_named(self):
        self.project.start()
        (self.project.root / 'latin.md').write_bytes(b'caf\xe9\n')
        self.project.write('docs/a.md', CLEAN)
        reason = self.project.blocked()
        self.assertIn('latin.md (checked by check.py of the skill): the page cannot be read', reason)
        self.assertIn('- docs/a.md (checked by check.py of the skill)', reason)
        self.assertEqual(self.project.record('latin.md').returncode, 1)
        self.project.git('checkout', '-qb', 'topic')
        self.project.git('add', '-A')
        self.project.git('commit', '-qm', 'latin')
        out = subprocess.run([sys.executable, str(GATE), 'check-diff', 'main'], cwd=self.project.root,
                             capture_output=True, text=True)
        self.assertEqual(out.returncode, 1)
        self.assertNotIn('Traceback', out.stderr)
        self.assertIn('latin.md: the page cannot be read', out.stdout)

    def test_without_the_tasker_role_the_block_gives_the_steps_by_hand(self):
        for text in (json.dumps({'choices': {'tasker': False}}), json.dumps({'choices': {'tasker': 'yes'}}),
                     json.dumps({'choices': ['tasker']}), json.dumps(['tasker']), 'not json'):
            with self.subTest(stack=text):
                self.stack(text)
                self.project.start()
                self.project.write('README.md', MORE + text + '\n')
                reason = self.project.blocked()
                self.assertNotIn('just prose', reason)
                self.assertIn('record PAGE', reason)

    def test_a_page_that_the_fresh_agent_of_just_prose_passed_in_a_worktree_does_not_block_a_later_turn(self):
        self.stack(json.dumps({'choices': {'tasker': True}}))
        self.project.git('add', '-A')
        self.project.git('commit', '-qm', 'gates')
        other = self.project.root.parent / (self.project.root.name + '-agent')
        self.project.git('worktree', 'add', '-q', '-b', 'agent', str(other))
        try:
            (other / 'README.md').write_text(MORE)
            self.assertEqual(self.project.record('README.md', cwd=other).returncode, 0)
            self.assertTrue((self.project.root / '.git/nossaifd/passes.json').is_file())
            self.project.start()
            self.project.write('README.md', MORE)
            self.assertIsNone(self.project.blocked())
        finally:
            self.project.git('worktree', 'remove', '--force', str(other))


def load_gate():
    "The gate as a module, for the functions that a test calls in this process. It writes no __pycache__."
    import importlib.util
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location('prose_gate_test', GATE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


TALK = '.agents/skills/talk/scripts/check_talk.py'
# A checker that stands in for the talk checker of nossaifd-talks. It imports a module of its folder, so a test
# sees that the gate runs it from its own file and that no __pycache__ appears there
FAKE = '''import sys
import helper
args = sys.argv[1:]
page = [a for a in args if a != '-v'][0]
text = open(page, encoding='utf-8').read()
print(f'{page}: {helper.WORDS} words: checked')
if 'LONG' in text:
    print('  HARD slide 1: the script is long')
    sys.exit(1)
if '-v' in args:
    print('  soft slide 1: a soft note')
'''
# A deck whose script uses a contraction, as rule 34 of TALKS.md asks. check.py marks it as hard
DECK = '## Students wait\n\n::: notes\nThe build isn\'t slow. It waits for the cache.\n:::\n'
MAP = {'version': 1, 'checkers': [{'pages': ['**/slides.qmd', '**/plan.md'], 'checker': TALK}]}


class CheckerMapTest(unittest.TestCase):
    "The map of checkers, .agents/nossaifd-checkers.json, which names another checker for some pages."

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Project(self.temp.name)
        self.project.write(TALK, FAKE)
        self.project.write(str(Path(TALK).parent / 'helper.py'), 'WORDS = 445\n')
        self.map(MAP)
        self.project.git('add', '-A')
        self.project.git('commit', '-qm', 'the talk checker')

    def tearDown(self):
        self.temp.cleanup()

    def map(self, value):
        self.project.write('.agents/nossaifd-checkers.json', value if isinstance(value, str) else json.dumps(value))

    def gate(self, *args, cwd=None):
        return subprocess.run([sys.executable, str(GATE), *args], cwd=cwd or self.project.root,
                              capture_output=True, text=True)

    def check_diff(self):
        return self.gate('check-diff', 'main')

    def test_a_glob_matches_the_whole_path_from_the_root(self):
        regex = load_gate().glob_regex
        cases = {'**/slides.qmd': (['slides.qmd', 'a/slides.qmd', 'a/b/slides.qmd'],
                                   ['xslides.qmd', 'a/slides.qmd.md', 'slides.qmd/a.md', 'a/my slides.qmd']),
                 'talks/*.qmd': (['talks/a.qmd'], ['talks/a/b.qmd', 'other/talks/a.qmd', 'talks.qmd']),
                 'talks/**': (['talks/a.md', 'talks/a/b.qmd'], ['other/a.md']),
                 'docs/?.md': (['docs/a.md'], ['docs/ab.md', 'docs//.md']),
                 'a.b[1].md': (['a.b[1].md'], ['axb1.md', 'a.b1.md']),
                 'slides.qmd': (['slides.qmd'], ['a/slides.qmd'])}
        for glob, (match, other) in cases.items():
            for path in match:
                self.assertTrue(regex(glob).fullmatch(path), (glob, path))
            for path in other:
                self.assertFalse(regex(glob).fullmatch(path), (glob, path))

    def test_the_hook_checks_a_deck_with_its_checker_and_names_the_checker(self):
        self.project.start()
        self.project.write('talk/slides.qmd', DECK)
        self.project.write('talk/notes.md', DECK)          # no glob matches it, so check.py checks it
        reason = self.project.blocked()
        self.assertIn(f'- talk/slides.qmd (checked by {TALK})', reason)
        self.assertIn('talk/notes.md (checked by check.py of the skill): ', reason)
        self.assertEqual(reason.count('a contraction'), 1)
        self.assertEqual(self.project.record('talk/slides.qmd').stdout,
                         f'talk/slides.qmd: recorded, checked by {TALK}\n')
        self.project.write('talk/notes.md', CLEAN)
        self.project.record('talk/notes.md')
        self.assertIsNone(self.project.blocked())
        self.assertFalse((self.project.root / Path(TALK).parent / '__pycache__').exists())

    def test_a_hard_problem_of_the_checker_blocks_and_record_refuses_the_page(self):
        self.project.start()
        self.project.write('talk/slides.qmd', DECK + 'LONG\n')
        reason = self.project.blocked()
        self.assertIn(f'talk/slides.qmd (checked by {TALK}): slide 1: the script is long', reason)
        out = self.project.record('talk/slides.qmd')
        self.assertEqual(out.returncode, 1)
        self.assertIn(f'1 hard problem(s) of {TALK}', out.stderr)

    def test_a_missing_or_failing_checker_is_a_hard_problem(self):
        cases = {'missing': (None, 'which the map .agents/nossaifd-checkers.json names, is missing'),
                 'crash': ('raise SystemExit("cannot parse the deck")\n', 'failed with exit 1: cannot parse'),
                 'usage': ('import sys\nprint("usage", file=sys.stderr)\nsys.exit(2)\n', 'failed with exit 2: usage'),
                 'traceback': ('import nothing_of_this_name\n', 'failed with exit 1: ModuleNotFoundError'),
                 'silent': ('import sys\nsys.exit(1)\n', 'failed with exit 1: no output'),
                 'killed': ('import os, signal\nos.kill(os.getpid(), signal.SIGKILL)\n', 'failed with exit -9'),
                 'contrary': ('print("  HARD a problem")\n', 'printed HARD problems but exited 0')}
        for case, (program, problem) in cases.items():
            with self.subTest(case=case):
                path = self.project.root / TALK
                if program is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_text(program)
                self.project.start()
                self.project.write('talk/slides.qmd', DECK + case + '\n')
                self.assertIn(problem, self.project.blocked())
                self.assertEqual(self.project.record('talk/slides.qmd').returncode, 1)
                out = self.gate('check', 'talk/slides.qmd')
                self.assertEqual(out.returncode, 1)
                self.assertIn(problem, out.stdout)

    def test_a_checker_that_does_not_end_is_a_hard_problem(self):
        gate = load_gate()
        gate.TIMEOUT = 1
        self.project.write(TALK, 'import time\ntime.sleep(30)\n')
        self.project.write('slides.qmd', DECK)
        hard, _ = gate.Checkers(self.project.root).problems('slides.qmd')
        self.assertEqual(hard, [f'its checker {TALK} did not end in 1 seconds'])

    def test_the_hook_gives_its_checkers_less_time_than_the_harness_gives_the_hook(self):
        "A hook that the harness kills prints nothing, and the stop goes through: a page would pass in silence"
        gate = load_gate()
        for name in ('claude-settings-hook.json', 'codex-hooks.json'):
            stop = json.loads((SKILL / 'assets' / name).read_text())['hooks']['Stop'][0]['hooks'][0]['timeout']
            self.assertLessEqual(gate.BUDGET + 15, stop, name)
        self.assertLessEqual(gate.TIMEOUT, gate.BUDGET)
        self.project.write('slides.qmd', DECK)
        checkers = gate.Checkers(self.project.root, budget=0.5)
        time.sleep(0.6)
        hard, _ = checkers.problems('slides.qmd')
        self.assertEqual(len(hard), 1)
        self.assertIn('the hook had no time left to run its checker', hard[0])

    def test_a_timeout_stops_the_checker_and_the_programs_that_it_started(self):
        gate = load_gate()
        gate.TIMEOUT = 1
        self.project.write(TALK, 'import subprocess, time\nchild = subprocess.Popen(["sleep", "60"])\n'
                                 'open("child.pid", "w").write(str(child.pid))\ntime.sleep(60)\n')
        self.project.write('slides.qmd', DECK)
        started = time.monotonic()
        hard, _ = gate.Checkers(self.project.root).problems('slides.qmd')
        self.assertLess(time.monotonic() - started, 4)
        self.assertEqual(hard, [f'its checker {TALK} did not end in 1 seconds'])
        child = int((self.project.root / 'child.pid').read_text())
        for _ in range(50):                                # the kill reaches the child at once, but give it time
            try:
                os.kill(child, 0)
            except ProcessLookupError:
                break
            time.sleep(0.1)
        else:
            os.kill(child, 9)
            self.fail('the program that the checker started still runs')

    def test_a_hard_line_with_a_colon_or_with_bytes_that_are_not_utf8_still_counts(self):
        cases = {'colon, exit 0': 'print("HARD: the deck is bad")\n',
                 'bytes, exit 1': 'import sys\nsys.stdout.buffer.write(b"  HARD caf\\xe9 slide\\n")\nsys.exit(1)\n'}
        for case, program in cases.items():
            with self.subTest(case=case):
                self.project.write(TALK, program)
                self.project.start()
                self.project.write('talk/slides.qmd', DECK + case + '\n')
                reason = self.project.blocked()
                self.assertIsNotNone(reason)
                self.assertIn(f'talk/slides.qmd (checked by {TALK}): ', reason)
                self.assertEqual(self.project.record('talk/slides.qmd').returncode, 1)

    def test_the_summary_of_a_page_named_hard_is_not_a_hard_problem(self):
        "A checker prints a summary that starts with the page, so a page named HARD.qmd starts a line with HARD"
        self.map({'version': 1, 'checkers': [{'pages': ['**'], 'checker': TALK}]})
        for name in ('HARD.qmd', 'HARD notes.qmd', 'HARD-copy.qmd', 'HARD/slides.qmd'):
            with self.subTest(page=name):
                self.project.write(name, DECK)
                out = self.gate('check', name)
                self.assertEqual(out.returncode, 0, out.stdout)
                self.assertEqual(self.project.record(name).returncode, 0)
        self.project.write('HARD.qmd', DECK + 'LONG\n')
        self.assertIn('HARD slide 1: the script is long', self.gate('check', 'HARD.qmd').stdout)

    def test_the_hook_keeps_time_to_collect_the_output_of_a_stopped_checker(self):
        gate = load_gate()
        self.project.write('slides.qmd', DECK)
        hard, _ = gate.Checkers(self.project.root, budget=gate.GRACE + 0.5).problems('slides.qmd')
        self.assertIn('the hook had no time left', hard[0])

    def test_a_checker_that_reads_standard_input_does_not_wait(self):
        self.project.write(TALK, 'import sys\nsys.stdin.read()\n')
        self.project.write('slides.qmd', DECK)
        proc = subprocess.Popen([sys.executable, str(GATE), 'check', 'slides.qmd'], cwd=self.project.root,
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        try:
            out, _ = proc.communicate(timeout=20)         # standard input of the gate stays open
        finally:
            proc.kill()
        self.assertEqual(proc.returncode, 0, out)

    def test_check_gives_a_file_outside_the_project_to_check_py(self):
        self.map({'version': 1, 'checkers': [{'pages': ['**'], 'checker': TALK}]})
        with tempfile.TemporaryDirectory() as other:
            (Path(other) / 'draft.md').write_text(CLEAN)
            out = self.gate('check', str(Path(other) / 'draft.md'))
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertIn('checked by check.py of the skill', out.stdout)

    def test_a_glob_with_dot_slash_works_and_a_glob_that_matches_nothing_breaks_the_map(self):
        self.map({'version': 1, 'checkers': [{'pages': ['./talk/slides.qmd'], 'checker': f'./{TALK}'}]})
        self.project.write('talk/slides.qmd', DECK)
        self.assertIn(f'checked by {TALK}', self.gate('check', 'talk/slides.qmd').stdout)
        for glob in ('talk\\slides.qmd', 'talk/', 'talk//slides.qmd', './', 'talk/./slides.qmd', '.',
                     'talk/../slides.qmd', ' **/slides.qmd', '**/slides.qmd '):
            with self.subTest(glob=glob):
                self.map({'version': 1, 'checkers': [{'pages': [glob], 'checker': TALK}]})
                out = self.gate('check', 'talk/slides.qmd')
                self.assertEqual(out.returncode, 1)
                self.assertIn('is broken', out.stdout)

    def test_a_broken_map_is_a_hard_problem_of_every_page(self):
        cases = {'not json': '{"version": 1,', 'no version': json.dumps({'checkers': []}),
                 'another version': json.dumps({'version': 2, 'checkers': []}),
                 'a version of true': json.dumps({'version': True, 'checkers': []}),
                 'too deep for json': '[' * 100000,
                 'a list': json.dumps([MAP]),
                 'no pages': json.dumps({'version': 1, 'checkers': [{'checker': TALK}]}),
                 'empty globs': json.dumps({'version': 1, 'checkers': [{'pages': [], 'checker': TALK}]}),
                 'a glob from /': json.dumps({'version': 1, 'checkers': [{'pages': ['/a.md'], 'checker': TALK}]}),
                 'not python': json.dumps({'version': 1, 'checkers': [{'pages': ['*.md'], 'checker': 'run.sh'}]})}
        for case, text in cases.items():
            with self.subTest(case=case):
                self.map(text)
                self.project.start()
                self.project.write('README.md', MORE + case + '\n')
                reason = self.project.blocked()
                self.assertIn('README.md (checked by none, the map .agents/nossaifd-checkers.json is broken): '
                              'the map of checkers .agents/nossaifd-checkers.json is broken', reason)
                self.assertEqual(self.project.record('README.md').returncode, 1)

    def test_a_checker_outside_the_project_is_refused(self):
        for checker in ('/usr/bin/check.py', '../check.py', 'a/../../check.py', 'C:/check.py', 'a\\check.py'):
            with self.subTest(checker=checker):
                self.map({'version': 1, 'checkers': [{'pages': ['**/*.md'], 'checker': checker}]})
                out = self.gate('check', 'README.md')
                self.assertEqual(out.returncode, 1)
                self.assertIn('Give a path inside the project', out.stdout)

    def test_the_map_is_read_only_from_the_root_of_the_project(self):
        self.project.write('docs/.agents/nossaifd-checkers.json', json.dumps(
            {'version': 1, 'checkers': [{'pages': ['**/*.md'], 'checker': 'nothing.py'}]}))
        self.project.write('docs/a.md', CLEAN)
        self.project.write('docs/slides.qmd', DECK)
        out = self.gate('check', 'a.md', 'slides.qmd', cwd=self.project.root / 'docs')
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertIn('docs/a.md: checked by check.py of the skill', out.stdout)
        self.assertIn(f'docs/slides.qmd: checked by {TALK}', out.stdout)

    def test_status_names_the_checker_of_each_changed_page(self):
        self.project.write('talk/slides.qmd', DECK)
        self.project.write('README.md', MORE)
        self.project.record('talk/slides.qmd', 'README.md')
        out = self.gate('status')
        self.assertEqual(out.returncode, 0, out.stdout)
        self.assertIn('every changed page passed', out.stdout)
        self.assertIn(f'The checker of each changed page:\n- README.md: check.py of the skill\n'
                      f'- talk/slides.qmd: {TALK}\n', out.stdout)

    def test_a_change_of_checker_asks_again(self):
        self.project.write('talk/plan.md', CLEAN)
        self.assertEqual(self.project.record('talk/plan.md').returncode, 0)
        self.assertEqual(self.gate('status').returncode, 0)
        self.map({'version': 1, 'checkers': [{'pages': ['**/slides.qmd'], 'checker': TALK}]})
        out = self.gate('status')                          # the pass was of the talk checker, so check.py asks
        self.assertEqual(out.returncode, 1)
        self.assertIn('- talk/plan.md (checked by check.py of the skill)', out.stdout)
        self.project.record('talk/plan.md')
        self.map(MAP)                                      # and back: the pass of check.py is not one of the talk checker
        self.assertIn(f'- talk/plan.md (checked by {TALK})', self.gate('status').stdout)

    def test_check_diff_uses_the_map_and_names_the_checker(self):
        self.project.git('checkout', '-qb', 'topic')
        self.project.write('talk/slides.qmd', DECK)
        self.project.write('docs/a.md', CLEAN)
        self.project.git('add', '-A')
        self.project.git('commit', '-qm', 'a talk')
        out = self.check_diff()
        self.assertEqual(out.returncode, 0, out.stdout)
        self.assertIn(f'talk/slides.qmd: checked by {TALK}, 0 hard problem(s)', out.stdout)
        self.assertIn('docs/a.md: checked by check.py of the skill, 0 hard problem(s)', out.stdout)
        self.project.write('talk/slides.qmd', DECK + 'LONG\n')
        self.project.git('commit', '-qam', 'a long talk')
        out = self.check_diff()
        self.assertEqual(out.returncode, 1)
        self.assertIn('talk/slides.qmd: slide 1: the script is long', out.stdout)

    def test_the_command_check_runs_the_checker_of_each_page(self):
        self.project.write('talk/slides.qmd', DECK)
        self.project.write('-talk.md', HARD)
        out = self.gate('check', '-v', 'talk/slides.qmd', 'README.md')
        self.assertEqual(out.returncode, 0, out.stdout)
        self.assertIn(f'talk/slides.qmd: checked by {TALK}, 0 hard problem(s)\n  talk/slides.qmd: 445 words: '
                      'checked\n    soft slide 1: a soft note\n', out.stdout)
        self.assertIn('README.md: checked by check.py of the skill, 0 hard, ', out.stdout)
        out = self.gate('check', '--', '-talk.md')
        self.assertEqual(out.returncode, 1)
        self.assertIn('HARD 3: a contraction', out.stdout)
        self.assertEqual(self.gate('check', 'gone.md').returncode, 2)
        self.assertEqual(self.gate('check', '-x', 'README.md').returncode, 2)
        self.assertEqual(self.gate('check').returncode, 2)

    def test_a_page_whose_name_starts_with_a_dash_reaches_the_checker_as_a_page(self):
        self.map({'version': 1, 'checkers': [{'pages': ['**/*.md'], 'checker': TALK}]})
        self.project.write('-v.md', CLEAN)
        out = self.gate('check', '--', '-v.md')
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertIn('./-v.md: 445 words: checked', out.stdout)


class CheckChangedTest(unittest.TestCase):
    "prose_gate.py check-changed, which the recipe just prose-check of the role runs, for the step prose-check."

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Project(self.temp.name)
        self.project.write('docs/old.md', CLEAN)
        self.project.git('add', '-A')
        self.project.git('commit', '-qm', 'pages')

    def tearDown(self):
        self.temp.cleanup()

    def check(self, *args, cwd=None):
        return subprocess.run([sys.executable, str(GATE), 'check-changed', *args], cwd=cwd or self.project.root,
                              capture_output=True, text=True)

    def checked(self, out):
        "The pages that a run checked, from the first line of each page."
        return sorted(re.findall(r'^(\S.*?): checked by ', out.stdout, re.M))

    def test_no_changed_page_passes(self):
        self.project.write('notes.txt', 'not a page\n')
        out = self.check()
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(out.stdout, 'nossaifd: no page changed since HEAD, so there is no page to check.\n')

    def test_a_changed_tracked_page_and_a_new_page_are_checked(self):
        self.project.write('README.md', MORE)
        self.project.write('docs/a new page.md', CLEAN)
        out = self.check()
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertEqual(self.checked(out), ['README.md', 'docs/a new page.md'])
        self.assertIn('checked 2 changed page(s), no hard problem', out.stdout)

    def test_a_staged_page_is_checked(self):
        self.project.write('staged.md', HARD)
        self.project.git('add', 'staged.md')
        out = self.check()
        self.assertEqual(out.returncode, 1)
        self.assertEqual(self.checked(out), ['staged.md'])

    def test_a_hard_problem_gives_exit_1(self):
        self.project.write('docs/old.md', HARD)
        out = self.check()
        self.assertEqual(out.returncode, 1)
        self.assertIn('docs/old.md: checked by check.py of the skill, 1 hard', out.stdout)
        self.assertIn('HARD', out.stdout)
        self.assertIn('a hard problem', out.stdout)

    def test_a_deleted_page_is_not_checked(self):
        (self.project.root / 'docs/old.md').unlink()
        out = self.check()
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertIn('no page changed', out.stdout)
        self.project.git('rm', '-q', 'README.md')
        self.assertEqual(self.check().returncode, 0)

    def test_a_renamed_page_is_checked_under_its_new_name(self):
        self.project.git('mv', 'docs/old.md', 'docs/new.md')
        out = self.check()
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertEqual(self.checked(out), ['docs/new.md'])

    def test_a_change_that_is_not_a_page_is_ignored(self):
        for name in ('notes.txt', 'CHANGELOG.md', 'AGENTS.md', '.agents/skills/x/SKILL.md', 'node_modules/a.md'):
            self.project.write(name, HARD)
        self.project.write('.gitignore', 'ignored.md\n')
        self.project.write('ignored.md', HARD)
        out = self.check()
        self.assertEqual(out.returncode, 0, out.stdout)
        self.assertIn('no page changed', out.stdout)

    def test_a_named_page_is_checked_alone(self):
        self.project.write('README.md', HARD)
        self.project.write('other.md', CLEAN)
        out = self.check('other.md')
        self.assertEqual(out.returncode, 0, out.stdout)
        self.assertEqual(self.checked(out), ['other.md'])
        out = self.check('-v', '--', 'README.md')
        self.assertEqual(out.returncode, 1)
        self.assertEqual(self.checked(out), ['README.md'])
        out = self.check('AGENTS.md')       # a named page counts, also one that is not a page of the rule
        self.assertEqual(out.returncode, 2)
        self.assertIn('no such file', out.stderr)

    def test_minus_v_adds_the_soft_notes(self):
        soft = CLEAN + '\nThe build runs; the tests wait.\n'
        self.project.write('README.md', soft)
        quiet, loud = self.check(), self.check('-v')
        self.assertEqual((quiet.returncode, loud.returncode), (0, 0), loud.stdout)
        self.assertNotIn('  soft ', quiet.stdout)
        self.assertIn('  soft ', loud.stdout)
        self.assertEqual(self.check('-x').returncode, 2)

    def test_the_map_of_checkers_applies_to_a_changed_page(self):
        self.project.write(TALK, FAKE)
        self.project.write(str(Path(TALK).parent / 'helper.py'), 'WORDS = 445\n')
        self.project.write('.agents/nossaifd-checkers.json', json.dumps(MAP))
        self.project.git('add', '-A')
        self.project.git('commit', '-qm', 'the talk checker')
        self.project.write('talk/slides.qmd', DECK + 'LONG\n')
        self.project.write('talk/notes.md', CLEAN)
        out = self.check()
        self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
        self.assertIn(f'talk/slides.qmd: checked by {TALK}, 1 hard problem(s)', out.stdout)
        self.assertIn('HARD slide 1: the script is long', out.stdout)
        self.assertIn('talk/notes.md: checked by check.py of the skill', out.stdout)

    def test_a_call_from_a_folder_checks_the_pages_of_the_whole_repository(self):
        self.project.write('README.md', HARD)
        self.project.write('docs/README.md', CLEAN)       # a page of the same name in the folder of the call
        out = self.check(cwd=self.project.root / 'docs')
        self.assertEqual(out.returncode, 1)
        self.assertEqual(self.checked(out), ['README.md', 'docs/README.md'])

    def test_it_writes_nothing_in_the_repository(self):
        self.project.write('README.md', HARD)
        self.project.write('new.md', CLEAN)
        before = listing(self.project.root)
        self.assertEqual(self.check().returncode, 1)
        self.assertEqual(listing(self.project.root), before)
        self.assertFalse((self.project.root / '.git/nossaifd').exists())

    def test_a_repository_with_no_commit_checks_each_page(self):
        with tempfile.TemporaryDirectory() as temp:
            subprocess.run(['git', 'init', '-q'], cwd=temp, check=True)
            out = self.check(cwd=temp)
            self.assertEqual(out.returncode, 0, out.stderr)
            self.assertIn('no page changed', out.stdout)
            (Path(temp) / 'staged.md').write_text(HARD)
            (Path(temp) / 'new.md').write_text(CLEAN)
            subprocess.run(['git', 'add', 'staged.md'], cwd=temp, check=True)
            out = self.check(cwd=temp)
            self.assertEqual(out.returncode, 1, out.stderr)
            self.assertEqual(self.checked(out), ['new.md', 'staged.md'])

    def test_a_folder_outside_git_needs_names_of_pages(self):
        with tempfile.TemporaryDirectory() as temp:
            (Path(temp) / 'draft.md').write_text(CLEAN)
            out = self.check(cwd=temp)
            self.assertEqual(out.returncode, 2)
            self.assertIn('not in a git repository, so name the pages', out.stderr)
            out = self.check('draft.md', cwd=temp)
            self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
            self.assertEqual(self.checked(out), ['draft.md'])

    def test_a_link_that_became_a_page_is_checked(self):
        "git reports a change of type as T, which a filter of A and M alone would miss"
        (self.project.root / 'link.md').symlink_to('docs/old.md')
        self.project.git('add', '-A')
        self.project.git('commit', '-qm', 'a link')
        (self.project.root / 'link.md').unlink()
        self.project.write('link.md', HARD)
        out = self.check()
        self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
        self.assertEqual(self.checked(out), ['link.md'])

    def test_minus_v_may_follow_a_page(self):
        self.project.write('other.md', CLEAN + '\nThe build runs; the tests wait.\n')
        out = self.check('other.md', '-v')
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertEqual(self.checked(out), ['other.md'])
        self.assertIn('  soft ', out.stdout)

    def test_a_page_whose_name_starts_with_a_dash_comes_after_two_dashes(self):
        self.project.write('-x.md', CLEAN)
        out = self.check('-x.md')
        self.assertEqual(out.returncode, 2)
        self.assertIn('after --', out.stderr)
        out = self.check('-v', '--', '-x.md')
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertEqual(self.checked(out), ['-x.md'])

    def test_a_git_that_fails_gives_exit_2(self):
        self.project.write('new.md', CLEAN)
        (self.project.root / '.git/index').write_text('garbage')
        out = self.check()
        self.assertEqual(out.returncode, 2, out.stdout)
        self.assertIn('git cannot list the changed files', out.stderr)

    def test_a_changed_page_with_an_odd_name_is_checked(self):
        for name in ('-x.md', 'docs/\u00e9 "q".md', 'two\nlines.md'):
            self.project.write(name, CLEAN)
        out = self.check()
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertIn('checked 3 changed page(s), no hard problem', out.stdout)
        self.assertIn('docs/\u00e9 "q".md: checked by', out.stdout)


class CheckChangedInCITest(unittest.TestCase):
    """check-changed with a base: in CI, where the checkout is clean, or with --base. Each test builds a bare
    origin and a clone with the whole history, as actions/checkout gives with fetch-depth: 0. The clone works on
    the branch topic, which starts at main."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        top = Path(self.temp.name)
        self.origin = top / 'origin.git'
        subprocess.run(['git', 'init', '-q', '--bare', '-b', 'main', str(self.origin)], check=True)
        (top / 'work').mkdir()
        self.project = Project(top / 'work')
        self.project.write('docs/old.md', HARD)       # a bad page from before the change, which no mode checks
        self.commit('pages')
        self.project.git('remote', 'add', 'origin', self.origin.as_uri())
        self.project.git('push', '-q', 'origin', 'main')
        self.project.git('fetch', '-q', 'origin')
        self.project.git('checkout', '-qb', 'topic')

    def tearDown(self):
        self.temp.cleanup()

    def commit(self, message='change'):
        self.project.git('add', '-A')
        self.project.git('commit', '-qm', message)

    def check(self, *args, cwd=None, **variables):
        """check-changed with CI set as GitHub sets it, and no other variable of GitHub, unless a test gives it.
        None clears a variable."""
        env = {k: v for k, v in os.environ.items() if not ci_variable(k)}
        env.update({k: v for k, v in {'CI': 'true', **variables}.items() if v is not None})
        return subprocess.run([sys.executable, str(GATE), 'check-changed', *args], cwd=cwd or self.project.root,
                              capture_output=True, text=True, env=env)

    def checked(self, out):
        return sorted(re.findall(r'^(\S.*?): checked by ', out.stdout, re.M))

    def event(self, value):
        "A fake event file of GitHub, with the given JSON or text. A dict gets the default branch main."
        if isinstance(value, dict):
            value = {'repository': {'default_branch': 'main'}, **value}
        path = Path(self.temp.name) / 'event.json'
        path.write_text(value if isinstance(value, str) else json.dumps(value))
        return str(path)

    def push(self, before=None, ref='refs/heads/main', **keys):
        "The variables of a push on GitHub, with an event file that gives before when it is not None."
        return {'GITHUB_EVENT_NAME': 'push', 'GITHUB_REF': ref,
                'GITHUB_EVENT_PATH': self.event({**({'before': before} if before is not None else {}), **keys})}

    def sha(self, rev='HEAD'):
        return self.project.git('rev-parse', rev).strip()

    def two_commits(self):
        "A bad page in a first commit and a good page in a second, on top of main."
        before = self.sha()
        self.project.write('docs/first.md', HARD)
        self.commit()
        self.project.write('docs/second.md', CLEAN)
        self.commit()
        return before

    def test_a_pull_request_with_a_bad_page_fails_and_one_with_good_pages_passes(self):
        self.project.write('docs/good.md', CLEAN)
        self.commit()
        pr = {'GITHUB_EVENT_NAME': 'pull_request', 'GITHUB_BASE_REF': 'main'}
        out = self.check(**pr)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertEqual(self.checked(out), ['docs/good.md'])
        self.assertIn('checked 1 changed page(s), compared with the merge base of origin/main and HEAD, no hard '
                      'problem', out.stdout)
        self.project.write('docs/bad.md', HARD)
        self.commit()
        out = self.check(**pr)
        self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
        self.assertEqual(self.checked(out), ['docs/bad.md', 'docs/good.md'])
        self.assertIn('compared with the merge base of origin/main and HEAD, a hard problem', out.stdout)

    def test_a_pull_request_counts_from_the_merge_base_not_from_the_tip_of_the_base(self):
        self.project.write('docs/mine.md', CLEAN)
        self.commit()
        self.project.git('checkout', '-q', 'main')
        self.project.write('docs/theirs.md', HARD)
        self.commit()
        self.project.git('push', '-q', 'origin', 'main')
        self.project.git('fetch', '-q', 'origin')
        self.project.git('checkout', '-q', 'topic')
        out = self.check(GITHUB_BASE_REF='main')
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertEqual(self.checked(out), ['docs/mine.md'])

    def test_a_push_to_the_default_branch_checks_each_commit_since_before(self):
        before = self.two_commits()
        out = self.check(**self.push(before))
        self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
        self.assertEqual(self.checked(out), ['docs/first.md', 'docs/second.md'])
        self.assertIn(f'compared with {before[:12]}, the commit before the push to the default branch main, a '
                      'hard problem', out.stdout)
        self.assertNotIn('the base is HEAD^', out.stdout)

    def test_a_push_to_the_default_branch_falls_back_to_the_parent_and_says_so(self):
        self.project.write('docs/gone.md', CLEAN)
        self.commit()
        gone = self.sha()
        self.project.git('reset', '-q', '--hard', 'HEAD^')      # a commit that a force-push replaced
        self.two_commits()
        cases = {'not in the history': ('ab' * 20, 'is not an ancestor of HEAD, as after a force-push'),
                 'not an ancestor': (gone, 'is not an ancestor of HEAD, as after a force-push'),
                 'no key': (None, 'gives no commit before a push'),
                 'not a sha': ('--all', 'is not the id of a commit')}
        for case, (before, why) in cases.items():
            with self.subTest(case=case):
                out = self.check(**self.push(before))
                self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
                self.assertEqual(self.checked(out), ['docs/second.md'])
                self.assertEqual(len(re.findall(r'^nossaifd: the base is HEAD\^, because .*' + re.escape(why),
                                                out.stdout, re.M)), 1, out.stdout)
                self.assertIn('compared with HEAD^, the parent commit, for a push to the default branch main, no '
                              'hard problem', out.stdout)

    def test_another_push_checks_each_commit_since_the_merge_base_with_the_default_branch(self):
        self.two_commits()
        out = self.check(**self.push('0' * 40, ref='refs/heads/topic'))
        self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
        self.assertEqual(self.checked(out), ['docs/first.md', 'docs/second.md'])
        self.assertIn('compared with the merge base of origin/main and HEAD, a hard problem', out.stdout)

    def test_the_default_branch_comes_from_the_event_file_then_from_origin_head(self):
        self.two_commits()
        self.project.git('push', '-q', 'origin', 'topic')
        self.project.git('fetch', '-q', 'origin')
        self.project.git('remote', 'set-head', 'origin', 'topic')
        out = self.check(**self.push(ref='refs/heads/other'))          # the event file says main
        self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
        self.assertIn('the merge base of origin/main and HEAD', out.stdout)
        self.project.git('remote', 'set-head', 'origin', 'main')
        for case, path in (('no file', None), ('no key', self.event('{"repository": {}}')),
                           ('not json', self.event('{')), ('a list', self.event('[1]'))):
            with self.subTest(case=case):
                out = self.check(GITHUB_EVENT_PATH=path)
                self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
                self.assertIn('the merge base of origin/main and HEAD', out.stdout)

    def test_no_default_branch_or_one_that_does_not_resolve_exits_2(self):
        self.two_commits()
        self.project.git('config', 'remote.origin.followRemoteHEAD', 'never')   # a fetch of git 2.48 sets it
        self.project.git('update-ref', '--no-deref', '-d', 'refs/remotes/origin/HEAD')
        out = self.check()
        self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
        self.assertIn('no default branch', out.stderr)
        out = self.check(GITHUB_EVENT_PATH=self.event({'repository': {'default_branch': 'trunk'}}))
        self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
        self.assertIn('the base origin/trunk does not resolve to a commit', out.stderr)
        out = self.check(GITHUB_EVENT_PATH=self.event({'repository': {'default_branch': '-x'}}))
        self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
        self.assertIn('no default branch', out.stderr)

    def test_another_ci_on_the_default_branch_checks_the_last_commit(self):
        "The merge base of HEAD and the default branch is HEAD itself, which would check no page"
        self.two_commits()
        self.project.git('push', '-q', 'origin', 'topic:main')
        self.project.git('fetch', '-q', 'origin')
        self.project.git('remote', 'set-head', 'origin', 'main')
        out = self.check()
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertEqual(self.checked(out), ['docs/second.md'])
        self.assertIn('compared with HEAD^, the parent commit, as HEAD has no commit of its own beside the default '
                      'branch origin/main', out.stdout)

    def test_the_first_push_compares_with_the_empty_tree(self):
        "A commit with no parent, in a clone with the whole history, is a true first commit"
        self.project.git('checkout', '-q', '--orphan', 'first')
        self.project.git('rm', '-rqf', '.')
        self.project.write('README.md', HARD)
        self.project.write('notes.txt', 'not a page\n')
        self.commit('first')
        variables = self.push('0' * 40, ref='refs/heads/first', repository={'default_branch': 'first'})
        out = self.check(**variables)
        self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
        self.assertEqual(self.checked(out), ['README.md'])
        self.assertIn('compared with the empty tree, as the key before of the push to the default branch first is '
                      'all zeros, a hard problem', out.stdout)
        # the line of the fallback names the base that was chosen
        self.assertIn('nossaifd: the base is the empty tree, because the key before of the event file is all zeros',
                      out.stdout)
        self.assertNotIn('HEAD^', out.stdout)
        # with no before, a first commit falls back to the empty tree too, by way of HEAD^
        out = self.check(**self.push(ref='refs/heads/first', repository={'default_branch': 'first'}))
        self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
        self.assertIn('compared with the empty tree, as HEAD is the first commit, for a push to the default '
                      'branch first, a hard problem', out.stdout)

    def orphan(self, name='first'):
        "A branch with no commit and no file, so that only the pages of the test are in it"
        self.project.git('checkout', '-q', '--orphan', name)
        self.project.git('rm', '-rqf', '.')

    def zero_push(self, name='first'):
        "The variables of the push that makes the default branch name, with before all zeros"
        return self.push('0' * 40, ref=f'refs/heads/{name}', repository={'default_branch': name})

    def test_a_push_with_before_all_zeros_checks_each_page_of_head(self):
        "A bad page of the first commit of the push, which the last commit does not touch, is checked"
        self.orphan()
        self.project.write('docs/first.md', HARD)
        self.commit('first')
        self.project.write('docs/second.md', CLEAN)
        self.commit('second')
        self.project.write('docs/third.md', CLEAN)
        self.commit('third')
        for width in (40, 64):           # the ids of SHA-1 and of SHA-256
            with self.subTest(width=width):
                variables = self.push('0' * width, ref='refs/heads/first', repository={'default_branch': 'first'})
                out = self.check(**variables)
                self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
                self.assertEqual(self.checked(out), ['docs/first.md', 'docs/second.md', 'docs/third.md'])
                self.assertEqual(len(re.findall(r'^nossaifd: the base is the empty tree, because the key before of '
                                                r'the event file is all zeros', out.stdout, re.M)), 1, out.stdout)
                self.assertIn('compared with the empty tree, as the key before of the push to the default branch '
                              'first is all zeros, a hard problem', out.stdout)
                self.assertNotIn('HEAD^', out.stdout)

    def test_a_push_with_before_all_zeros_and_good_pages_passes(self):
        self.orphan()
        self.project.write('docs/first.md', CLEAN)
        self.project.write('notes.txt', 'not a page\n')
        self.commit('first')
        self.project.write('docs/second.md', CLEAN)
        self.commit('second')
        out = self.check(**self.zero_push())
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertEqual(self.checked(out), ['docs/first.md', 'docs/second.md'])
        self.assertIn('compared with the empty tree, as the key before of the push to the default branch first is '
                      'all zeros, no hard problem', out.stdout)

    def test_a_push_with_before_all_zeros_in_a_sha256_repository_uses_its_empty_tree(self):
        "The empty tree of SHA-256 differs from that of SHA-1, so a fixed id of SHA-1 would fail here"
        root = Path(self.temp.name) / 'sha256'
        root.mkdir()
        made = subprocess.run(['git', 'init', '-q', '--object-format=sha256', '-b', 'main', str(root)],
                              capture_output=True, text=True)
        if made.returncode:
            self.skipTest(f'this git cannot make a SHA-256 repository: {made.stderr.strip()}')
        project = Project.__new__(Project)
        project.root = root
        project.git('config', 'user.email', 'test@example.com')
        project.git('config', 'user.name', 'Test')
        project.write('docs/first.md', HARD)
        project.git('add', '-A')
        project.git('commit', '-qm', 'first')
        project.write('docs/second.md', CLEAN)
        project.git('add', '-A')
        project.git('commit', '-qm', 'second')
        out = self.check(cwd=root, **self.push('0' * 64))
        self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
        self.assertEqual(self.checked(out), ['docs/first.md', 'docs/second.md'])
        self.assertIn('compared with the empty tree, as the key before of the push to the default branch main is '
                      'all zeros, a hard problem', out.stdout)

    def test_pull_request_target_exits_2_and_names_pull_request(self):
        self.two_commits()
        out = self.check(GITHUB_EVENT_NAME='pull_request_target', GITHUB_BASE_REF='main')
        self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
        self.assertIn('pull_request_target', out.stderr)
        self.assertIn('the event pull_request.', out.stderr)
        out = self.check('--base', 'main', GITHUB_EVENT_NAME='pull_request_target')   # the option wins
        self.assertEqual(out.returncode, 1, out.stdout + out.stderr)

    def test_the_pages_changed_since_head_count_too_and_each_page_once(self):
        self.project.write('docs/committed.md', CLEAN)
        self.project.write('docs/both.md', CLEAN)
        self.commit()
        self.project.write('docs/both.md', MORE)
        self.project.write('docs/untracked.md', CLEAN)
        self.project.write('docs/old.md', MORE)             # in main, changed since HEAD
        out = self.check(GITHUB_BASE_REF='main')
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertEqual(self.checked(out), ['docs/both.md', 'docs/committed.md', 'docs/old.md',
                                             'docs/untracked.md'])
        self.assertIn('checked 4 changed page(s)', out.stdout)

    def test_a_shallow_clone_exits_2_and_names_fetch_depth(self):
        self.project.write('docs/new.md', CLEAN)
        self.commit()
        self.project.write('docs/newer.md', CLEAN)
        self.commit()
        self.project.git('push', '-q', 'origin', 'topic')
        for depth in ('1', '2'):
            clone = Path(self.temp.name) / f'shallow{depth}'
            subprocess.run(['git', 'clone', '-q', '--depth', depth, '-b', 'topic', self.origin.as_uri(),
                            str(clone)], check=True)
            for variables in (self.push(), self.push('0' * 40, ref='refs/heads/topic',
                                                     repository={'default_branch': 'topic'}),
                              {'GITHUB_BASE_REF': 'main'}, {'CI': None, 'args': ('--base', 'HEAD^')}):
                with self.subTest(depth=depth, variables=variables):
                    variables = dict(variables)
                    out = self.check(*variables.pop('args', ()), cwd=clone, **variables)
                    self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
                    self.assertIn('shallow', out.stderr)
                    self.assertIn('fetch-depth: 0', out.stderr)
                    self.assertNotIn('empty tree', out.stdout + out.stderr)

    def test_a_base_that_does_not_resolve_exits_2(self):
        self.project.write('docs/new.md', HARD)
        self.commit()
        out = self.check(GITHUB_BASE_REF='nosuch')
        self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
        self.assertIn('the base origin/nosuch does not resolve to a commit', out.stderr)
        self.assertIn('fetch-depth: 0', out.stderr)
        self.project.git('branch', 'main2')               # a local branch is not the base of a pull request
        self.assertEqual(self.check(GITHUB_BASE_REF='main2').returncode, 2)
        out = self.check('--base', 'nosuch', CI=None)
        self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
        self.assertIn('the base nosuch does not resolve to a commit', out.stderr)

    def test_no_merge_base_exits_2(self):
        self.project.git('checkout', '-q', '--orphan', 'alone')
        self.project.write('docs/new.md', CLEAN)
        self.commit()
        for variables in ({'GITHUB_BASE_REF': 'main'}, self.push(ref='refs/heads/alone')):
            with self.subTest(variables=variables):
                out = self.check(**variables)
                self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
                self.assertIn('no merge base', out.stderr)

    def test_no_changed_page_passes_and_names_the_base(self):
        self.project.write('notes.txt', 'not a page\n')
        self.project.write('CHANGELOG.md', HARD)
        self.commit()
        out = self.check(GITHUB_BASE_REF='main')
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertEqual(out.stdout, 'nossaifd: no page changed, compared with the merge base of origin/main and '
                                     'HEAD, so there is no page to check.\n')

    def test_named_pages_ignore_ci(self):
        self.project.write('docs/new.md', HARD)
        self.commit()
        self.project.write('other.md', CLEAN)
        out = self.check('other.md', GITHUB_BASE_REF='nosuch', GITHUB_EVENT_NAME='pull_request_target')
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertEqual(self.checked(out), ['other.md'])

    def test_the_map_of_checkers_applies(self):
        self.project.write(TALK, FAKE)
        self.project.write(str(Path(TALK).parent / 'helper.py'), 'WORDS = 445\n')
        self.project.write('.agents/nossaifd-checkers.json', json.dumps(MAP))
        self.project.write('talk/slides.qmd', DECK + 'LONG\n')
        self.project.write('talk/notes.md', CLEAN)
        self.commit()
        out = self.check(GITHUB_BASE_REF='main')
        self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
        self.assertIn(f'talk/slides.qmd: checked by {TALK}, 1 hard problem(s)', out.stdout)
        self.assertIn('HARD slide 1: the script is long', out.stdout)
        self.assertIn('talk/notes.md: checked by check.py of the skill', out.stdout)

    def test_a_deleted_page_is_not_checked(self):
        self.project.git('rm', '-q', 'docs/old.md')
        self.project.write('docs/new.md', CLEAN)
        self.commit()
        self.project.write('docs/later.md', CLEAN)
        self.commit()
        (self.project.root / 'docs/later.md').unlink()     # gone from the disk since the commit
        out = self.check(GITHUB_BASE_REF='main')
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertEqual(self.checked(out), ['docs/new.md'])
        self.assertIn('docs/later.md: not checked, it is deleted since HEAD', out.stdout)

    def test_a_page_that_a_sparse_checkout_hides_exits_2(self):
        "A page of the commits that is not on disk, and that the working tree did not delete, is never skipped"
        self.project.write('docs/bad.md', HARD)
        self.commit()
        self.project.git('update-index', '--skip-worktree', 'docs/bad.md')
        (self.project.root / 'docs/bad.md').unlink()
        out = self.check(GITHUB_BASE_REF='main')
        self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
        self.assertIn('1 changed page(s) are not files on disk, so they cannot be checked: docs/bad.md', out.stderr)
        self.assertIn('sparse checkout', out.stderr)
        self.assertNotIn('checked 1', out.stdout)
        self.assertNotIn('no page changed', out.stdout)

    def test_a_page_removed_from_the_index_but_on_disk_is_checked_and_not_called_deleted(self):
        self.project.write('docs/bad.md', HARD)
        self.commit()
        self.project.git('rm', '-q', '--cached', 'docs/bad.md')
        out = self.check(GITHUB_BASE_REF='main')
        self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
        self.assertEqual(self.checked(out), ['docs/bad.md'])
        self.assertNotIn('deleted since HEAD', out.stdout)

    def test_ci_unset_empty_false_or_0_keeps_the_check_since_head(self):
        self.project.write('docs/new.md', HARD)
        self.commit()
        for value in (None, '', 'false', 'FALSE', ' False ', '0'):
            with self.subTest(CI=value):
                out = self.check(CI=value, GITHUB_BASE_REF='main')
                self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
                self.assertIn('no page changed since HEAD', out.stdout)
        for value in ('true', '1', 'yes'):
            with self.subTest(CI=value):
                self.assertEqual(self.check(CI=value, GITHUB_BASE_REF='main').returncode, 1)

    def test_the_option_base_runs_the_same_check_outside_ci_and_wins_over_ci(self):
        self.project.write('docs/new.md', HARD)
        self.commit()
        for args in (('--base', 'main'), ('--base=main',), ('-v', '--base', 'main'), ('--base', 'main', '-v')):
            with self.subTest(args=args):
                out = self.check(*args, CI=None)
                self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
                self.assertEqual(self.checked(out), ['docs/new.md'])
                self.assertIn('compared with the merge base of main and HEAD, a hard problem', out.stdout)
        out = self.check('--base', 'main', GITHUB_BASE_REF='nosuch')
        self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
        self.assertIn('compared with the merge base of main and HEAD', out.stdout)
        out = self.check('--base', 'HEAD', CI=None)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertIn('no page changed, compared with the merge base of HEAD and HEAD', out.stdout)

    def test_a_bad_use_of_the_option_exits_2(self):
        for args, message in ((('--base',), 'needs a branch'), (('--base=',), 'needs a branch'),
                              (('--base', 'main', 'README.md'), 'name no page'),
                              (('README.md', '--base=main'), 'name no page'),
                              (('--base', '-v'), 'cannot start with -'), (('--bases',), 'unknown option')):
            with self.subTest(args=args):
                out = self.check(*args, CI=None)
                self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
                self.assertIn(message, out.stderr)

    def test_a_repository_with_no_commit_exits_2(self):
        with tempfile.TemporaryDirectory() as temp:
            subprocess.run(['git', 'init', '-q'], cwd=temp, check=True)
            (Path(temp) / 'new.md').write_text(CLEAN)
            out = self.check(cwd=temp)
            self.assertEqual(out.returncode, 2, out.stdout + out.stderr)
            self.assertIn('no commit', out.stderr)

    def test_it_writes_nothing(self):
        self.project.write('docs/new.md', HARD)
        self.commit()
        before = listing(self.project.root)
        self.assertEqual(self.check(GITHUB_BASE_REF='main').returncode, 1)
        self.assertEqual(self.check(**self.push(ref='refs/heads/topic')).returncode, 1)
        self.assertEqual(listing(self.project.root), before)

    def test_check_diff_compares_the_empty_tree_with_head(self):
        empty = self.project.git('hash-object', '-t', 'tree', '/dev/null').strip()
        self.project.write('docs/new.md', CLEAN)
        self.commit()
        out = subprocess.run([sys.executable, str(GATE), 'check-diff', empty], cwd=self.project.root,
                             capture_output=True, text=True)
        self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
        self.assertIn('checked 3 page(s), a hard problem', out.stdout)     # README.md, docs/new.md, docs/old.md


class MissingCheckerTest(unittest.TestCase):
    "A skill installed without its check.py prints the install line, not a traceback."

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        (Path(self.temp.name) / 'work').mkdir()
        self.project = Project(Path(self.temp.name) / 'work')
        scripts = self.project.root / '.agents/skills/nossaifd/scripts'
        scripts.mkdir(parents=True)
        shutil.copy(GATE, scripts / 'prose_gate.py')
        self.gate_path = scripts / 'prose_gate.py'
        self.project.git('add', '-A')
        self.project.git('commit', '-qm', 'the skill without check.py')
        self.project.git('checkout', '-qb', 'topic')
        self.project.write('docs/new.md', CLEAN)
        self.project.git('add', '-A')
        self.project.git('commit', '-qm', 'a page')

    def tearDown(self):
        self.temp.cleanup()

    def gate(self, *args, data=None):
        return subprocess.run([sys.executable, str(self.gate_path), *args], cwd=self.project.root,
                              capture_output=True, text=True, input=json.dumps(data) if data else None)

    def test_check_check_changed_and_check_diff_print_the_install_line(self):
        for args in (('check', 'docs/new.md'), ('check-changed', '--base', 'main'), ('check-diff', 'main'),
                     ('record', 'docs/new.md')):
            with self.subTest(args=args):
                out = self.gate(*args)
                self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
                self.assertIn("npx skills add rahuldave/nossaifd -a codex --skill '*' -y", out.stdout + out.stderr)
                self.assertNotIn('Traceback', out.stdout + out.stderr)

    def test_the_stop_hook_lets_the_stop_go_through_and_prints_the_install_line(self):
        data = {'cwd': str(self.project.root), 'session_id': 's1'}
        self.gate('start', data=data)
        self.project.write('docs/new.md', HARD)
        out = self.gate('hook', data=data)
        self.assertEqual((out.returncode, json.loads(out.stdout)), (0, {}))
        self.assertIn("npx skills add rahuldave/nossaifd", out.stderr)


RECIPES = REPO / '.agents/just/roles/nossaifd.just'
# The line that records the step prose-check for jlog pass, the last line of the recipe of the role
STEP_LINE = 'jlog step prose-check'
# The steps of just check in jnterfaces that a profile gives. The role must not define one of them, or check
STEPS_OF_PROFILES = ('fmt-check', 'lint', 'typecheck', 'test', 'coverage-check', 'integration', 'docstring-check',
                     'docs-check', 'diff-check', 'check')
# The variables that change what just runs. jlog pass refuses a run with one of them
JUST_VARIABLES = ('JUST_NO_DEPS', 'JUST_SHELL', 'JUST_JUSTFILE', 'JUST_JUSTFILE_NAME', 'JUST_CEILING',
                  'JUST_WORKING_DIRECTORY', 'JUST_DOTENV_FILENAME', 'JUST_DOTENV_PATH', 'JUST_NO_DOTENV')
# The Justfile and the files of jnterfaces that a project with the index has, as jnterfaces #37 writes them
JNTERFACES_FILES = {
    'Justfile': "import? '.agents/install.just'\n\nexport JLOG_RUN := env(\"JLOG_RUN\", uuid())\n\n"
                'set positional-arguments\n\nset allow-duplicate-recipes\n',
    '.agents/install.just': "import? 'just/index.just'\n",
    '.agents/just/index.just': 'set shell := ["jlog", "sh", "-cu"]\n\n'
                               "import? 'roles/nossaifd.just'\n\ncheck: prose-check\n    jlog pass\n",
    '.agents/stack.json': json.dumps({'version': 2, 'steps': ['prose-check'], 'provided_steps': ['prose-check']}),
    '.gitignore': '.agents/log/\n',
}


def body_of(text):
    "The lines of the recipe prose-check, without their indent."
    body = re.search(r'^prose-check \*args:\n((?:    .*\n)*)', text, re.M).group(1)
    return [line[4:] for line in body.splitlines()]


def readme_recipe():
    "The recipe that the README gives a project without the index of jnterfaces."
    text = (REPO / 'README.md').read_text()
    blocks = [block for block in re.findall(r'```just\n(.*?)```', text, re.S) if 'prose-check *args:' in block]
    assert len(blocks) == 1, blocks
    return blocks[0]


def tool_bin(folder, *tools):
    "A folder with links to the tools only, so that a PATH with it and the folders of the system has no jlog."
    folder.mkdir()
    for tool in tools:
        (folder / tool).symlink_to(shutil.which(tool))
    return f'{folder}:/usr/bin:/bin'


def role_project(temp, justfiles):
    "A project with the skill, the role file and the given Justfile and files of jnterfaces, all committed."
    Path(temp).mkdir()
    project = Project(temp)
    (project.root / '.agents/skills').mkdir(parents=True)
    (project.root / '.agents/skills/nossaifd').symlink_to(SKILL)
    (project.root / '.agents/just/roles').mkdir(parents=True)
    shutil.copy(RECIPES, project.root / '.agents/just/roles/nossaifd.just')
    for name, text in justfiles.items():
        project.write(name, text)
    project.git('add', '-A')
    project.git('commit', '-qm', 'the recipes')
    return project


class RoleRecipeTest(unittest.TestCase):
    "The recipe of the prose role, which just install of jnterfaces imports into a project."

    def test_the_recipe_is_prose_check_with_the_check_then_the_step_line(self):
        text = RECIPES.read_text()
        self.assertEqual(re.findall(r'^([a-z][a-z-]*)\b[^\n]*:$', text, re.M), ['prose-check'])
        self.assertIn('[positional-arguments]\nprose-check *args:\n    uv run --no-project --quiet python '
                      '.agents/skills/nossaifd/scripts/prose_gate.py check-changed "$@"\n'
                      f'    {STEP_LINE}\n', text)
        self.assertEqual(body_of(text), ['uv run --no-project --quiet python .agents/skills/nossaifd/scripts/'
                                         'prose_gate.py check-changed "$@"', STEP_LINE])
        self.assertTrue(text.endswith(f'\n    {STEP_LINE}\n'), 'the step line is the last line of the file')

    def test_the_file_sets_no_shell_and_has_no_step_of_a_profile(self):
        text = RECIPES.read_text()
        self.assertNotRegex(text, r'(?m)^\s*set\s')
        for name in STEPS_OF_PROFILES:
            self.assertNotRegex(text, rf'(?m)^@?{re.escape(name)}(\s[^\n]*)?:', name)
        self.assertNotRegex(text, r'(?m)^(alias|mod|import)\b')

    def test_the_recipe_has_no_shebang_no_script_no_dash_line_and_no_folder_attribute(self):
        text = RECIPES.read_text()
        self.assertNotIn('#!', text)
        self.assertEqual(re.findall(r'(?m)^\s*\[.*$', text), ['[positional-arguments]'])
        for line in body_of(text):
            self.assertNotRegex(line, r'^@?-', line)
            self.assertFalse(line.endswith('\\'), line)

    @unittest.skipUnless(shutil.which('just'), 'needs just')
    def test_the_file_parses_alone_and_its_dump_has_one_plain_recipe(self):
        out = subprocess.run(['just', '--justfile', str(RECIPES), '--summary'], capture_output=True, text=True)
        self.assertEqual((out.returncode, out.stdout.strip()), (0, 'prose-check'), out.stderr)
        out = subprocess.run(['just', '--justfile', str(RECIPES), '--dump', '--dump-format', 'json'],
                             capture_output=True, text=True, check=True)
        dump = json.loads(out.stdout)
        self.assertEqual(list(dump['recipes']), ['prose-check'])
        self.assertIsNone(dump['settings']['shell'])
        self.assertEqual(dump['assignments'], {})
        recipe = dump['recipes']['prose-check']
        self.assertFalse(recipe['shebang'])
        self.assertEqual(recipe['dependencies'], [])
        self.assertTrue(all(not isinstance(a, dict) and a in ('positional-arguments', 'doc') or
                            isinstance(a, dict) and set(a) <= {'doc'} for a in recipe['attributes']),
                        recipe['attributes'])
        self.assertEqual(recipe['body'][-1], [STEP_LINE], 'the last line has no interpolation')

    def test_the_readme_gives_the_recipe_of_the_role_without_the_step_line(self):
        "The two copies cannot drift: the README recipe is the recipe of the role less its last line"
        role = RECIPES.read_text()
        start = role.index('[positional-arguments]\n')
        self.assertEqual(readme_recipe().split('\n', 1)[1], role[start:].replace(f'    {STEP_LINE}\n', ''))
        self.assertNotIn('jlog', readme_recipe())

    @unittest.skipUnless(shutil.which('just') and shutil.which('uv') and shutil.which('git'), 'needs just, uv and git')
    def test_without_jlog_the_recipe_of_the_readme_passes_good_pages_and_fails_bad_ones(self):
        with tempfile.TemporaryDirectory() as temp:
            project = role_project(Path(temp) / 'p', {'Justfile': readme_recipe()})
            path = tool_bin(Path(temp) / 'bin', 'just', 'uv', 'git')
            env = {**os.environ, 'PATH': path}
            run = lambda *args: subprocess.run(['just', 'prose-check', *args], cwd=project.root, capture_output=True,
                                               text=True, env=env)
            self.assertIsNone(shutil.which('jlog', path=path))
            out = run()
            self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
            project.write('my page.md', CLEAN)
            out = run('my page.md')
            self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
            self.assertIn('my page.md: checked by check.py of the skill, 0 hard', out.stdout)
            out = run()
            self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
            project.write('bad page.md', HARD)
            out = run('-v', 'bad page.md')
            self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
            self.assertIn('bad page.md: checked by', out.stdout)
            out = run()
            self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
            self.assertIn('checked 2 changed page(s), a hard problem', out.stdout)
            project.write('-x.md', CLEAN)
            out = run('--', '-x.md')
            self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
            self.assertIn('-x.md: checked by check.py of the skill, 0 hard', out.stdout)

    @unittest.skipUnless(shutil.which('just') and shutil.which('uv') and shutil.which('git'), 'needs just, uv and git')
    def test_without_the_shell_jlog_the_role_file_fails_after_a_good_check(self):
        "Why a project without the index copies the README recipe: the step line needs the shell jlog"
        with tempfile.TemporaryDirectory() as temp:
            project = role_project(Path(temp) / 'p', {'Justfile': "import '.agents/just/roles/nossaifd.just'\n"})
            path = tool_bin(Path(temp) / 'bin', 'just', 'uv', 'git')
            # bash, the sh of macOS, says "jlog: command not found"; dash, the sh of Ubuntu, says "jlog: not found"
            shells = [None] + (['/bin/dash'] if Path('/bin/dash').exists() else [])
            for shell in shells:
                with self.subTest(sh=shell or 'the sh of the system'):
                    (Path(temp) / 'bin/sh').unlink(missing_ok=True)
                    if shell:
                        (Path(temp) / 'bin/sh').symlink_to(shell)
                    out = subprocess.run(['just', 'prose-check'], cwd=project.root, capture_output=True, text=True,
                                         env={**os.environ, 'PATH': path})
                    self.assertEqual(out.returncode, 127, out.stdout + out.stderr)
                    self.assertIn('no page changed since HEAD', out.stdout)
                    self.assertRegex(out.stderr, r'jlog: (command )?not found')
            (Path(temp) / 'bin/sh').unlink(missing_ok=True)
            if shutil.which('jlog'):
                # With jlog installed, the step line still fails, because the shell of the Justfile is not jlog
                (Path(temp) / 'bin/jlog').symlink_to(shutil.which('jlog'))
                out = subprocess.run(['just', 'prose-check'], cwd=project.root, capture_output=True, text=True,
                                     env={**os.environ, 'PATH': path})
                self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
                self.assertIn('must be a line of its own in a recipe that runs through jlog', out.stderr)

    def test_ci_builds_jlog_so_that_the_jlog_test_runs_there(self):
        "The workflow builds jlog v0.1.0 and sets NOSSAIFD_NEED_JLOG, which turns the skip into a failure"
        text = (REPO / '.github/workflows/verify.yml').read_text()
        self.assertIn('cargo install --locked --git https://github.com/rahuldave/jlog --rev '
                      '6fccbf92d47a7b66f0e5b4dce7046c25c29a364a jlog', text)
        self.assertIn("NOSSAIFD_NEED_JLOG: '1'", text)

    def test_the_readme_tells_a_project_with_the_old_import_to_replace_it(self):
        text = re.sub(r'\s+', ' ', (REPO / 'README.md').read_text())
        self.assertIn("If your Justfile has the line `import? '.agents/just/roles/nossaifd.just'`", text)
        self.assertIn('jnterfaces #37', text)

    @unittest.skipUnless(os.environ.get('NOSSAIFD_NEED_JLOG') or shutil.which('jlog') and shutil.which('just')
                         and shutil.which('uv') and shutil.which('git'),
                         'needs jlog 0.1.0 on PATH, with just, uv and git; build it from github.com/rahuldave/jlog')
    def test_under_the_index_of_jnterfaces_jlog_pass_needs_the_step_and_a_bad_page_fails(self):
        self.assertTrue(shutil.which('jlog'), 'NOSSAIFD_NEED_JLOG is set, but jlog is not on PATH')
        with tempfile.TemporaryDirectory() as temp:
            project = role_project(Path(temp) / 'p', JNTERFACES_FILES)
            env = {name: value for name, value in os.environ.items()
                   if name != 'JLOG_RUN' and name not in JUST_VARIABLES}
            log = project.root / '.agents/log/just.jsonl'

            def check():
                before = len(log.read_text().splitlines()) if log.exists() else 0
                out = subprocess.run(['just', 'check'], cwd=project.root, capture_output=True, text=True, env=env)
                records = [json.loads(line) for line in log.read_text().splitlines()[before:]]
                return out, {r['kind'] for r in records}, [r.get('step') for r in records if r['kind'] == 'step']

            project.write('docs/good.md', CLEAN)
            project.git('add', '-A')
            out, kinds, steps = check()
            self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
            self.assertIn('docs/good.md: checked by check.py of the skill, 0 hard', out.stdout)
            self.assertEqual(steps, ['prose-check'])
            self.assertIn('pass', kinds)
            project.git('commit', '-qm', 'a good page')
            project.write('docs/bad.md', HARD)
            project.git('add', '-A')
            out, kinds, steps = check()
            self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
            self.assertIn('docs/bad.md: checked by', out.stdout)
            self.assertEqual(steps, [], 'a failed check records no step')
            self.assertNotIn('pass', kinds)
            self.assertNotIn('no-pass', kinds, 'just stops before jlog pass')
            # A recipe that passes the check but has no step line gives no pass
            project.git('rm', '-q', '--cached', 'docs/bad.md')
            (project.root / 'docs/bad.md').unlink()
            role = project.root / '.agents/just/roles/nossaifd.just'
            role.write_text(role.read_text().replace(f'    {STEP_LINE}\n', ''))
            project.git('add', '-A')
            out, kinds, steps = check()
            self.assertEqual(out.returncode, 1, out.stdout + out.stderr)
            self.assertEqual((steps, 'pass' in kinds, 'no-pass' in kinds), ([], False, True))


class InstallFilesTest(unittest.TestCase):
    def settings(self, name):
        return json.loads((SKILL / 'assets' / name).read_text())['hooks']

    def test_each_hook_setting_runs_the_gate_at_the_start_and_the_end_of_a_turn(self):
        for name in ('claude-settings-hook.json', 'codex-hooks.json'):
            hooks = self.settings(name)
            for event, command in (('UserPromptSubmit', 'start'), ('Stop', 'hook')):
                setting = hooks[event][0]['hooks'][0]
                self.assertIn('.agents/skills/nossaifd/scripts/prose_gate.py', setting['command'])
                self.assertIn(f'"$F" {command} "$ROOT"', setting['command'])
                self.assertIn('--python ">=3.11"', setting['command'])
                self.assertIn('timeout', setting)
            self.assertNotIn('CLAUDE_PROJECT_DIR', json.dumps(hooks) if 'codex' in name else '')

    def test_a_hook_without_the_script_lets_the_turn_go_on(self):
        "A missing script must not make Python exit 2, which Claude Code reads as a block"
        with tempfile.TemporaryDirectory() as other:
            subprocess.run(['git', 'init', '-q'], cwd=other, check=True)
            for name in ('claude-settings-hook.json', 'codex-hooks.json'):
                for event, expected in (('UserPromptSubmit', ''), ('Stop', '{}')):
                    command = self.settings(name)[event][0]['hooks'][0]['command']
                    out = subprocess.run(['sh', '-c', command], cwd=other, input='{}', capture_output=True,
                                         text=True, env={**os.environ, 'CLAUDE_PROJECT_DIR': other})
                    self.assertEqual((out.returncode, out.stdout.strip()), (0, expected), (name, event))

    def test_the_package_names_the_parts_for_an_installer(self):
        extras = json.loads((REPO / 'skill-package.json').read_text())['install_extras']
        self.assertEqual(extras['starter'], extras['seed'])
        for source in [*extras['parts'].values(), *extras['starter'].values()]:
            self.assertTrue((REPO / source).is_file(), source)
        self.assertEqual(set(extras['parts']), {'AGENTS.md', '.claude/settings.json', '.codex/hooks.json'})

    def test_the_instruction_names_the_skill_the_subagent_and_the_record(self):
        text = re.sub(r'\s+', ' ', (SKILL / 'assets/agents-prose.md').read_text())
        for part in ('use the nossaifd skill', 'follow all of its steps', 'subagent that did not write it',
                     'prose_gate.py record', 'Keep each bad example', 'Oskar Austegard'):
            self.assertIn(part, text)

    def test_the_workflow_runs_the_check_of_the_gate_and_credits_the_skill(self):
        text = (SKILL / 'assets/prose-check.yml').read_text()
        self.assertIn('pull_request', text)
        self.assertIn('prose_gate.py', text)
        self.assertIn('check-diff', text)
        self.assertIn('contents: read', text)
        self.assertIn('Oskar Austegard', text)

    def test_the_base_task_of_just_prose_gives_both_passes_the_record_and_the_result(self):
        text = re.sub(r'\s+', ' ', (SKILL / 'references/targets/prose.md').read_text())
        for part in ('plain-writing pass', 'the declaude skill by Oskar Austegard', 'prose_gate.py pages -z',
                     'prose_gate.py record PAGE', 'scripts/check.py', 'docstrings', 'smalldocs api module',
                     'AGENT_RESULT v1', 'target: prose', 'nonce', 'role: changed', 'Keep each bad example',
                     'Do not stage a file, and do not commit'):
            self.assertIn(part, text)

    def test_the_skill_and_the_instruction_name_just_prose_for_a_project_with_the_gates(self):
        for name in ('SKILL.md', 'assets/agents-prose.md'):
            text = re.sub(r'\s+', ' ', (SKILL / name).read_text())
            self.assertIn('Run `just prose` in place of steps 6 to 8 only when `.agents/stack.json` sets '
                          '`choices.tasker` to the JSON value `true`, not the string `"true"`.', text, name)
            self.assertIn('Otherwise, do steps 6 to 8 yourself. Do them yourself also when the project has no '
                          'recipe `just prose`, or when it only runs the checkers.', text, name)
            self.assertNotIn('In a project with the commit gates', text, name)

    def test_the_instruction_says_that_prose_check_does_not_replace_the_steps(self):
        for name in ('SKILL.md', 'assets/agents-prose.md'):
            text = re.sub(r'\s+', ' ', (SKILL / name).read_text())
            self.assertIn('`just prose-check` only runs the checkers. It does not do the declaude pass or the '
                          'record, so it never replaces steps 6 to 8.', text, name)

    def test_the_condition_of_the_instruction_is_the_test_of_the_gate(self):
        "The setting that the instruction names is the one that gates_installed reads"
        gate = load_gate()
        with tempfile.TemporaryDirectory() as temp:
            (Path(temp) / '.agents').mkdir()
            stack = Path(temp) / '.agents/stack.json'
            cases = [({'tasker': True}, True), ({'tasker': False}, False), ({'prose': True}, False),
                     ({'tasker': 'true'}, False), ({'tasker': 1}, False), (['tasker'], False)]
            for choices, expected in cases:
                stack.write_text(json.dumps({'version': 2, 'choices': choices}))
                self.assertIs(gate.gates_installed(Path(temp)), expected, choices)
            stack.write_text('{"choices": {"tasker": tru')
            self.assertFalse(gate.gates_installed(Path(temp)))
            stack.unlink()
            self.assertFalse(gate.gates_installed(Path(temp)))

    def test_the_page_of_the_flow_gives_a_map_that_the_gate_reads_and_its_contract(self):
        text = (REPO / 'docs/flow.md').read_text()
        example = re.search(r'```json\n(.*?)```', text, re.S).group(1)
        with tempfile.TemporaryDirectory() as temp:
            (Path(temp) / '.agents').mkdir()
            (Path(temp) / '.agents/nossaifd-checkers.json').write_text(example)
            rules, broken = load_gate().map_rules(Path(temp))
        self.assertIsNone(broken)
        self.assertEqual([c for _, c in rules], ['.agents/skills/presentations/scripts/check_talk.py'] * 2)
        flat = re.sub(r'\s+', ' ', text)
        for part in ('.agents/nossaifd-checkers.json', 'python -B CHECKER PAGE', '**Exit 0**', '**Exit 1**',
                     '**Any other exit**', 'only from the root of the project', 'pull_request_target',
                     'treat the map as code', 'The hook asks again when such a page changes',
                     'A change to the map does not check the pages that did not change'):
            self.assertIn(part, flat)
        self.assertIn(f'in {load_gate().TIMEOUT} seconds', flat)
        self.assertIn(f'{load_gate().BUDGET} seconds together', flat)

    def test_the_skill_and_the_base_task_check_a_page_with_its_checker(self):
        for name in ('SKILL.md', 'references/targets/prose.md'):
            text = re.sub(r'\s+', ' ', (SKILL / name).read_text())
            self.assertIn('prose_gate.py check', text, name)
            self.assertIn('.agents/nossaifd-checkers.json', text, name)
        self.assertIn('pull_request_target', (SKILL / 'assets/prose-check.yml').read_text())

    def test_the_skill_tells_the_agent_to_record_each_page(self):
        text = re.sub(r'\s+', ' ', (SKILL / 'SKILL.md').read_text())
        step8 = text[text.index('8. Run the linter'):text.index('9. Read the page yourself')]
        self.assertIn('prose_gate.py record page.md', step8)


if __name__ == '__main__':
    unittest.main()

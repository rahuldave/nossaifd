"""Check the gate of the nossaifd flow: the hooks at the start and the end of a turn, the record of passes, the
check of a pull request, and the files that a project installs."""
import json
import os
from pathlib import Path
import re
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
        self.project.start()
        self.project.write('README.md', MORE)
        self.project.blocked()
        self.assertEqual(self.project.record('README.md').returncode, 0)
        self.assertEqual(self.project.git('status', '--porcelain'), ' M README.md\n')
        self.assertFalse((SKILL / 'scripts/__pycache__').exists() and
                         any((SKILL / 'scripts/__pycache__').glob('check*.pyc')))

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
        self.assertEqual((out.returncode, out.stdout), (0, 'docs/a.md: recorded\n'))

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

    def test_clean_pages_pass(self):
        self.project.write('docs/a page.md', CLEAN)
        self.commit()
        out = self.check()
        self.assertEqual(out.returncode, 0, out.stdout)
        self.assertIn('checked 1 page(s)', out.stdout)


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

    def test_the_skill_tells_the_agent_to_record_each_page(self):
        text = re.sub(r'\s+', ' ', (SKILL / 'SKILL.md').read_text())
        step8 = text[text.index('8. Run the linter'):text.index('9. Read the page yourself')]
        self.assertIn('prose_gate.py record page.md', step8)


if __name__ == '__main__':
    unittest.main()

"""Check the nossaifd skill, its copies of the guide and the checker, and its installer."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / '.agents/skills/nossaifd'
RECORD = Path('.agents/nossaifd-install.json')


def git(path, *args):
    return subprocess.run(['git', '-C', str(path), '-c', 'user.name=T', '-c', 'user.email=t@example.invalid', *args],
                          check=True, capture_output=True, text=True).stdout.strip()


def check(text):
    with tempfile.TemporaryDirectory() as temp:
        page = Path(temp) / 'page.md'
        page.write_text(text)
        return subprocess.run([sys.executable, REPO / 'check.py', page], capture_output=True, text=True)


class SkillTest(unittest.TestCase):
    def test_the_skill_ships_the_same_guide_and_checker(self):
        self.assertEqual((SKILL / 'references/GUIDE.md').read_bytes(), (REPO / 'GUIDE.md').read_bytes(),
                         'run just sync')
        self.assertEqual((SKILL / 'scripts/check.py').read_bytes(), (REPO / 'check.py').read_bytes(), 'run just sync')

    def test_the_skill_names_itself_says_when_to_use_it_and_names_its_licence(self):
        text = (SKILL / 'SKILL.md').read_text()
        front = re.match(r'^---\nname: (.+)\ndescription: (.+)\nlicense: (.+)\n---\n', text)
        self.assertIsNotNone(front)
        self.assertEqual(front.group(1), 'nossaifd')
        self.assertIn('Use when', front.group(2))
        self.assertRegex(front.group(3), r'^MIT, copyright \(c\) 2026 Rahul Dave\. .*rahuldave/nossaifd$')
        self.assertTrue((REPO / 'LICENSE').read_text().startswith('MIT License\n\nCopyright (c) 2026 Rahul Dave\n'))
        self.assertTrue((SKILL / 'agents/openai.yaml').is_file())
        for ref in re.findall(r'`((?:references|scripts)/[\w./-]+)`', text):
            self.assertTrue((SKILL / ref).is_file(), ref)

    def test_the_checker_skips_front_matter_and_keeps_line_numbers(self):
        long = ' '.join(['word'] * 40)
        result = check(f'---\nname: x\ndescription: {long}.\n---\n\nShort text — with a dash.\n')
        self.assertEqual(result.returncode, 1)
        self.assertIn('0 soft', result.stdout)
        self.assertIn('HARD 6: an em dash', result.stdout)
        self.assertNotIn('words (at most', result.stdout)

    def test_the_checker_reads_a_page_whose_front_matter_does_not_close(self):
        result = check('---\n\n' + ' '.join(['word'] * 30) + '.\n')
        self.assertEqual(result.returncode, 1)
        self.assertIn('30 words', result.stdout)

    def test_a_page_that_starts_with_a_rule_is_still_checked(self):
        long = ' '.join(['word'] * 30)
        result = check(f'---\n\n{long} and we utilize it.\n\n---\n')
        self.assertIn('words (at most 25)', result.stdout)
        result = check(f'---\nThis is prose and not YAML at all.\n---\n\n{long}.\n')
        self.assertIn('words (at most 25)', result.stdout)
        result = check(f'---\n- Note: {long} that we utilize.\n---\n')
        self.assertIn('words (at most 25)', result.stdout)
        result = check('---\nname: x\nmetadata:\n  type: user\nitems:\n- a\n---\n\nShort text.\n')
        self.assertIn('0 hard, 0 soft', result.stdout)

    def test_a_rule_line_later_in_the_page_is_not_front_matter(self):
        result = check('Short text.\n\n---\n\n' + ' '.join(['word'] * 30) + '.\n\n---\n')
        self.assertIn('30 words', result.stdout)


class InstallTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        self.source = root / 'source'
        shutil.copytree(REPO, self.source, ignore=shutil.ignore_patterns('.git', '__pycache__', '_site'))
        git(self.source, 'init', '-q')
        git(self.source, 'add', '-A')
        git(self.source, 'commit', '-q', '-m', 'source')
        self.target = root / 'target'
        self.target.mkdir()
        git(self.target, 'init', '-q')

    def install(self, *args):
        return subprocess.run(['bash', self.source / 'scripts/install.sh', *args, self.target], capture_output=True, text=True)

    def test_installs_the_skill_and_records_the_revision(self):
        self.assertEqual(self.install('--dry-run').returncode, 0)
        self.assertFalse((self.target / '.agents').exists())
        run = self.install()
        self.assertEqual(run.returncode, 0, run.stderr)
        installed = self.target / '.agents/skills/nossaifd'
        self.assertEqual((installed / 'scripts/check.py').read_bytes(), (REPO / 'check.py').read_bytes())
        record = json.loads((self.target / RECORD).read_text())
        self.assertEqual(record['package'], 'nossaifd')
        self.assertEqual(record['source_revision'], git(self.source, 'rev-parse', 'HEAD'))
        digest = hashlib.sha256((installed / 'SKILL.md').read_bytes()).hexdigest()
        self.assertEqual(record['managed_files']['.agents/skills/nossaifd/SKILL.md'], digest)
        self.assertFalse(any(name.startswith('.agents/skills/nossaifd/../') for name in record['managed_files']))

    def test_never_overwrites_a_file_that_the_user_edited(self):
        self.assertEqual(self.install().returncode, 0)
        guide = self.target / '.agents/skills/nossaifd/references/GUIDE.md'
        guide.write_text(guide.read_text() + 'my rule\n')
        (self.source / '.agents/skills/nossaifd/references/GUIDE.md').write_text('new guide\n')
        git(self.source, 'commit', '-q', '-am', 'change')
        run = self.install()
        self.assertNotEqual(run.returncode, 0)
        self.assertIn('differs from source', run.stderr)
        self.assertIn('my rule', guide.read_text())


if __name__ == '__main__':
    unittest.main()

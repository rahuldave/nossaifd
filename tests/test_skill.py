"""Check the nossaifd skill and its copies of the guide and the checker. jnterfaces installs the skill."""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / '.agents/skills/nossaifd'


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

    def test_the_package_has_no_installer_and_needs_only_uv(self):
        manifest = json.loads((REPO / 'skill-package.json').read_text())
        self.assertNotIn('installers', manifest)
        self.assertEqual([e['name'] for e in manifest['executables']['required']], ['uv'])
        self.assertFalse((REPO / 'scripts').exists())
        self.assertNotIn('python3 ', (SKILL / 'SKILL.md').read_text())

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


if __name__ == '__main__':
    unittest.main()

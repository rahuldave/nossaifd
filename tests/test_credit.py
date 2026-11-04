"""Rosalind Reid lets this project use her material on one condition: every place that uses it credits her.

These tests fail when a page that uses her work does not name her in full, when a rule of GUIDE.md or TALKS.md
links to her PDFs and does not name her in full in that rule, when a page drops the notice that her credit must
stay, and when a page publishes her PDFs on the site in place of linking to them on GitHub.
"""
import importlib.util
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
TEXT = {'.md', '.py', '.yaml', '.yml', '.json', '.just'}
# The pages that must name her whether or not they mention her by surname: each one is built on her work.
MUST = ['README.md', 'GUIDE.md', 'TALKS.md', 'docs/sources.md', 'docs/why.md', 'docs/check-talk.md', 'check_talk.py',
        'docs/checker.md', 'check.py',
        '.agents/skills/nossaifd/SKILL.md', '.agents/skills/presentations/SKILL.md',
        '.agents/skills/presentations/agents/openai.yaml']
GITHUB = 'https://github.com/rahuldave/nossaifd/blob/main/sources/reid/'
# The pages that carry the notice that text from her work keeps its credit, and that her PDFs are not under MIT
NOTICE = ['README.md', 'GUIDE.md', 'TALKS.md', '.agents/skills/nossaifd/SKILL.md', '.agents/skills/presentations/SKILL.md']


def rule_blocks(text):  # [(first line, text)] of each rule, list item and paragraph of a guide
    "Split a guide into blocks. A line with no indent starts a block after a blank line, or as a list item or a heading."
    out, block, blank = [], [], True
    for number, line in enumerate(text.split('\n'), 1):
        starts = line[:1] not in ('', ' ', '\t') and (blank or re.match(r'^(\d+\.|[-*+]|#+)\s', line))
        if starts and block:
            out.append(block)
            block = []
        if line.strip() or block:
            block.append((number, line))
        blank = not line.strip()
    if block:
        out.append(block)
    return [(b[0][0], '\n'.join(line for _, line in b)) for b in out]


def uncredited(text):  # The first line of each block that links to her PDFs and does not name her in full
    "The rules that use Rosalind Reid's PDFs must each name her in full, so that a rule copied alone keeps her credit."
    return [line for line, block in rule_blocks(text) if 'sources/reid/' in block and 'Rosalind Reid' not in block]


# Phrases that mark one of her rules in a step or a checklist item of the presentations skill
MARKERS = ('five parts', '90 to 120', 'minute test', '20 seconds', 'movie', 'video', 'still image', 'background',
           'thank', 'the occasion', 'the questions', 'plain words', 'says what it means')
PRESENTATIONS = '.agents/skills/presentations/SKILL.md'


def list_items(text):  # [(first line, text)] of each list item, with its indented lines
    "Split a page into its list items. An item runs until a blank line or a line with no indent."
    out, item = [], None
    for number, line in enumerate(text.split('\n'), 1):
        if re.match(r'^(\d+\.|[-*+])\s', line):
            item = [number, line]
            out.append(item)
        elif item and line.startswith(' ') and line.strip():
            item[1] += '\n' + line
        else:
            item = None
    return [(line, ' '.join(text.split())) for line, text in out]


def uncredited_items(text):  # The first line of each item that uses one of her rules and does not name her
    "Each step and checklist item that carries a rule of Rosalind Reid must name her in that item."
    return [line for line, item in list_items(text)
            if any(marker in item.lower() for marker in MARKERS) and 'Rosalind Reid' not in item]


def unnamed(text):  # The first line of each block that says "Reid" and not "Rosalind Reid"
    return [line for line, block in rule_blocks(text) if re.search(r'\bReid\b', block) and 'Rosalind Reid' not in block]


def files():  # Every text file in the repository that git tracks or would add, outside tests/
    listed = subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard'], cwd=REPO,
                            capture_output=True, text=True, check=True).stdout.split('\n')
    for name in listed:
        path = REPO / name
        if name and path.suffix in TEXT and path.is_file() and not name.startswith('tests/'):
            yield name, path.read_text(encoding='utf-8')


class CreditTest(unittest.TestCase):
    def test_each_page_built_on_her_work_names_her(self):
        for name in MUST:
            with self.subTest(page=name):
                self.assertTrue((REPO / name).is_file(), f'{name} is missing')
                self.assertIn('Rosalind Reid', (REPO / name).read_text(encoding='utf-8'))

    def test_a_page_that_mentions_her_or_her_files_names_her_in_full(self):
        for name, text in files():
            if re.search(r'\bReid\b|sources/reid/', text):
                with self.subTest(page=name):
                    self.assertIn('Rosalind Reid', text)

    def test_each_rule_that_links_to_her_pdfs_names_her_in_full(self):
        for name in ('GUIDE.md', 'TALKS.md'):
            with self.subTest(page=name):
                self.assertEqual(uncredited((REPO / name).read_text(encoding='utf-8')), [])

    def test_a_copy_with_the_credit_of_one_rule_removed_fails(self):
        for name, rule in (('TALKS.md', '9. **'), ('GUIDE.md', '12. **'), ('TALKS.md', '68. **')):
            with self.subTest(page=name, rule=rule), tempfile.TemporaryDirectory() as temp:
                text = (REPO / name).read_text(encoding='utf-8')
                start = text.index(rule)
                end = text.find('\n' + str(int(rule.split('.')[0]) + 1) + '. **', start)
                end = end if end > 0 else text.index('\n\n', start)   # the last rule of a section
                self.assertIn('Rosalind Reid', text[start:end])
                copy = Path(temp) / name
                copy.write_text(text[:start] + text[start:end].replace('Rosalind Reid', 'Reid') + text[end:],
                                encoding='utf-8')
                found = uncredited(copy.read_text(encoding='utf-8'))
                self.assertEqual(len(found), 1, found)
                self.assertTrue(copy.read_text(encoding='utf-8').split('\n')[found[0] - 1].lstrip().startswith(rule))

    def test_each_rule_that_says_reid_names_her_in_full(self):
        for name in ('GUIDE.md', 'TALKS.md'):
            with self.subTest(page=name):
                self.assertEqual(unnamed((REPO / name).read_text(encoding='utf-8')), [])
        self.assertEqual(unnamed("41. **Rule.** Reid's note is advice.\n42. **Next.** Rosalind Reid says so.\n"), [1])

    def test_each_item_of_the_presentations_skill_that_uses_her_rules_names_her(self):
        text = (REPO / PRESENTATIONS).read_text(encoding='utf-8')
        found = list_items(text)
        self.assertGreaterEqual(sum(any(m in item.lower() for m in MARKERS) for _, item in found), 8, found)
        self.assertEqual(uncredited_items(text), [])

    def test_a_copy_with_the_credit_of_one_item_removed_fails(self):
        text = (REPO / PRESENTATIONS).read_text(encoding='utf-8')
        for start in ('- **Each movie**', '3. Write the story'):
            with self.subTest(item=start), tempfile.TemporaryDirectory() as temp:
                begin = text.index(start)
                end = text.index('\n- ' if start.startswith('-') else '\n4. ', begin)
                self.assertIn('Rosalind Reid', text[begin:end])
                copy = Path(temp) / 'SKILL.md'
                copy.write_text(text[:begin] + text[begin:end].replace(' of Rosalind Reid', '')
                                .replace(' The rule is from Rosalind Reid.', '') + text[end:], encoding='utf-8')
                found = uncredited_items(copy.read_text(encoding='utf-8'))
                self.assertEqual(len(found), 1, found)
                self.assertTrue(copy.read_text(encoding='utf-8').split('\n')[found[0] - 1].startswith(start))

    def test_the_pages_say_that_her_credit_must_stay(self):
        flat = lambda text: ' '.join(text.split())   # the notice can wrap across lines
        for name in NOTICE:
            with self.subTest(page=name):
                text = flat((REPO / name).read_text(encoding='utf-8'))
                self.assertIn('must keep its credit to Rosalind Reid', text)
                self.assertIn('not under the MIT licence', text)
        top = (REPO / 'TALKS.md').read_text(encoding='utf-8').split('\n## ')[0]
        self.assertIn('must keep its credit to Rosalind Reid', flat(top))
        sources = (REPO / 'GUIDE.md').read_text(encoding='utf-8').split('\n## Sources')[1]
        self.assertIn('must keep its credit to Rosalind Reid', flat(sources))
        licence = (REPO / 'README.md').read_text(encoding='utf-8').split('\n## Licence')[1]
        self.assertIn('must keep its credit to Rosalind Reid', flat(licence))

    def test_her_files_are_linked_on_github_and_not_on_the_site(self):
        for name, text in files():
            with self.subTest(page=name):
                self.assertNotRegex(text, r'rahuldave\.com/nossaifd/sources/')
        for pdf in (REPO / 'sources/reid').glob('*.pdf'):
            with self.subTest(pdf=pdf.name):
                self.assertTrue(any(GITHUB + pdf.name in text for _, text in files()), f'nothing links to {pdf.name}')

    def test_the_site_turns_a_github_link_to_a_page_into_a_link_to_the_site(self):
        spec = importlib.util.spec_from_file_location('nossaifd_build', REPO / 'docs/build.py')
        build = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(build)   # build.py imports markdown-it only to render, so this needs no package
        for _, source, out, _ in build.PAGES:
            path = source.relative_to(REPO).as_posix()
            self.assertEqual(build.LINKS[f'https://github.com/rahuldave/nossaifd/blob/main/{path}'], out, path)
        html = ('<a href="https://github.com/rahuldave/nossaifd/blob/main/GUIDE.md">x</a>'
                '<a href="https://github.com/rahuldave/nossaifd/blob/main/docs/check-talk.md#run-it">y</a>'
                '<a href="https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf">z</a>')
        self.assertEqual(build.relink(html), '<a href="guide.html">x</a><a href="check-talk.html#run-it">y</a>'
                         '<a href="https://github.com/rahuldave/nossaifd/blob/main/sources/reid/reid-presentation-tips.pdf">z</a>')

    def test_the_site_does_not_copy_her_files(self):
        build = (REPO / 'docs/build.py').read_text(encoding='utf-8')
        self.assertNotIn('copytree', build)
        self.assertNotRegex(build, r'["\']sources["\']\s*\)?\s*,\s*OUT')


if __name__ == '__main__':
    unittest.main()

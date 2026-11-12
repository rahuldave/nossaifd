"""Rosalind Reid lets this project use her material on one condition: every place that uses it credits her.

These tests fail when a page that uses her work does not name her in full, when a rule of GUIDE.md or an
example of EXAMPLES.md links to her PDFs and does not name her in full in that block, when a page drops the
notice that her credit must stay, and when the site would publish her PDFs in place of linking to them on GitHub.
"""
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
TEXT = {'.md', '.py', '.yaml', '.yml', '.json', '.just'}
# The pages that must name her whether or not they mention her by surname: each one is built on her work.
MUST = ['README.md', 'GUIDE.md', 'EXAMPLES.md', 'docs/sources.md', 'docs/why.md', 'docs/checker.md', 'check.py',
        '.agents/skills/nossaifd/SKILL.md']
GITHUB = 'https://github.com/rahuldave/nossaifd/blob/main/sources/reid/'
# The pages that carry the notice that text from her work keeps its credit, and that her PDFs are not under MIT
NOTICE = ['README.md', 'GUIDE.md', 'EXAMPLES.md', '.agents/skills/nossaifd/SKILL.md']
# The pages whose every rule, example and paragraph that links to her PDFs must name her in that block
BLOCKS = ['GUIDE.md', 'EXAMPLES.md', 'docs/why.md']


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


def uncredited_examples(text):  # The heading of each example from her work that does not name her in its own block
    "Each example of EXAMPLES.md whose letter is W comes from her work, and must name her in its block."
    found, heading, block, fence = [], None, [], False
    for line in text.split('\n') + ['### END']:
        if line.startswith('```'):
            fence = not fence
        if not fence and re.match(r'^#{1,3} ', line):
            if heading and 'Rosalind Reid' not in '\n'.join(block):
                found.append(heading)
            heading, block = (line if re.match(r'^### [WDP]\d+\. ', line) else None), []
        block.append(line)
    return found


def unnamed(text):  # The first line of each block that says "Reid" and not "Rosalind Reid"
    return [line for line, block in rule_blocks(text) if re.search(r'\bReid\b', block) and 'Rosalind Reid' not in block]


def render_list(text):  # The entries under project.render of a _smalldocs.yml, read without a YAML package
    "Read the list under the key render, as one value on its line or as the lines of a list below it."
    lines, out = text.split('\n'), []
    for i, line in enumerate(lines):
        match = re.match(r'^(\s*)render:\s*(.*)$', line)
        if not match:
            continue
        if match.group(2):
            return [v.strip().strip('"\'') for v in match.group(2).strip('[]').split(',') if v.strip()]
        for item in lines[i + 1:]:
            if not item.strip() or item.lstrip().startswith('#'):
                continue
            if len(item) - len(item.lstrip()) <= len(match.group(1)) or not item.lstrip().startswith('- '):
                break
            out.append(item.lstrip()[2:].strip().strip('"\''))
    return out


def files():  # Every text file in the repository that git tracks or would add, outside tests/ and .claude/
    "git lists another worktree or repository inside this one as one folder, so the walk does not go into it."
    listed = subprocess.run(['git', 'ls-files', '--cached', '--others', '--exclude-standard'], cwd=REPO,
                            capture_output=True, text=True, check=True).stdout.split('\n')
    for name in listed:
        path = REPO / name
        if name and path.suffix in TEXT and path.is_file() and not name.startswith(('tests/', '.claude/')):
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
        for name in BLOCKS:
            with self.subTest(page=name):
                self.assertEqual(uncredited((REPO / name).read_text(encoding='utf-8')), [])

    def test_a_copy_with_the_credit_of_one_rule_removed_fails(self):
        for name, rule in (('GUIDE.md', '12. **'), ('GUIDE.md', '13. **')):
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

    def test_a_copy_of_the_examples_with_one_credit_removed_fails(self):
        text = (REPO / 'EXAMPLES.md').read_text(encoding='utf-8')
        start = text.index('### W4. ')
        end = text.index('\n### ', start + 1)
        credit = text.index('Credit: [Rosalind Reid', start)
        self.assertLess(credit, end)
        copy = text[:start] + text[start:end].replace('Rosalind Reid', 'Reid') + text[end:]
        found = uncredited(copy)
        self.assertEqual(len(found), 1, found)
        self.assertTrue(copy.split('\n')[found[0] - 1].startswith('Credit: [Reid'))

    def test_each_example_from_her_work_names_her_in_its_own_block(self):
        for name in ('EXAMPLES.md', '.agents/skills/nossaifd/references/EXAMPLES.md'):
            with self.subTest(page=name):
                text = (REPO / name).read_text(encoding='utf-8')
                self.assertGreaterEqual(len(re.findall(r'(?m)^### W\d+\. ', text)), 10)
                self.assertEqual(uncredited_examples(text), [])

    def test_a_copy_of_the_examples_with_one_credit_line_removed_fails(self):
        text = (REPO / 'EXAMPLES.md').read_text(encoding='utf-8')
        start = text.index('### W8. ')
        end = text.index('\n### ', start + 1)
        block = text[start:end]
        self.assertIn('Rosalind Reid', block)
        with tempfile.TemporaryDirectory() as temp:
            copy = Path(temp) / 'EXAMPLES.md'
            copy.write_text(text[:start] + block.replace('Rosalind Reid', 'the author') + text[end:], encoding='utf-8')
            self.assertEqual(uncredited_examples(copy.read_text(encoding='utf-8')), [block.split('\n')[0]])

    def test_each_rule_that_says_reid_names_her_in_full(self):
        for name in BLOCKS:
            with self.subTest(page=name):
                self.assertEqual(unnamed((REPO / name).read_text(encoding='utf-8')), [])
        self.assertEqual(unnamed("41. **Rule.** Reid's note is advice.\n42. **Next.** Rosalind Reid says so.\n"), [1])

    def test_the_pages_say_that_her_credit_must_stay(self):
        flat = lambda text: ' '.join(text.split())   # the notice can wrap across lines
        for name in NOTICE:
            with self.subTest(page=name):
                text = flat((REPO / name).read_text(encoding='utf-8'))
                self.assertIn('must keep its credit to Rosalind Reid', text)
                self.assertIn('not under the MIT licence', text)
        sources = (REPO / 'GUIDE.md').read_text(encoding='utf-8').split('\n## Sources')[1]
        self.assertIn('must keep its credit to Rosalind Reid', flat(sources))
        licence = (REPO / 'README.md').read_text(encoding='utf-8').split('\n## Licence')[1]
        self.assertIn('must keep its credit to Rosalind Reid', flat(licence))

    def test_her_files_are_linked_on_github_and_not_on_the_site(self):
        for name, text in files():
            with self.subTest(page=name):
                self.assertNotRegex(text, r'rahuldave\.com/nossaifd/sources/')

    def test_each_of_her_pdfs_is_linked_by_its_github_url_from_a_page(self):
        pages = ['README.md'] + [p for p in render_list((REPO / '_smalldocs.yml').read_text(encoding='utf-8'))
                                 if p.endswith('.md')]
        self.assertIn('GUIDE.md', pages)
        text = ' '.join((REPO / page).read_text(encoding='utf-8') for page in pages)
        pdfs = sorted((REPO / 'sources/reid').glob('*.pdf'))
        self.assertGreaterEqual(len(pdfs), 2)
        for pdf in pdfs:
            with self.subTest(pdf=pdf.name):
                self.assertIn(GITHUB + pdf.name, text, f'no page links to {pdf.name}')
        self.assertNotIn(GITHUB + 'not-a-file.pdf', text)

    def test_the_site_builds_no_file_of_sources_and_no_pdf(self):
        config = (REPO / '_smalldocs.yml').read_text(encoding='utf-8')
        render = render_list(config)
        self.assertIn('index.qmd', render)
        for entry in render:
            with self.subTest(entry=entry):
                self.assertFalse(entry.startswith(('sources', '!')), entry)
                self.assertNotIn('*', entry)   # a glob could reach her PDFs
                self.assertRegex(entry, r'\.(md|qmd)$')
                self.assertTrue((REPO / entry).is_file(), entry)
        self.assertNotRegex(config, r'sources/|\.pdf')   # nor in resources, which copies files as they are

    def test_the_render_list_reader_finds_a_pdf(self):
        self.assertEqual(render_list('project:\n  render:\n    - a.md\n    - sources/reid/x.pdf\nwebsite:\n'),
                         ['a.md', 'sources/reid/x.pdf'])
        self.assertEqual(render_list('project:\n  render: [a.md, "sources/**"]\n'), ['a.md', 'sources/**'])


if __name__ == '__main__':
    unittest.main()

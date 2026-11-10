"""Check the copy of the declauding skill by Oskar Austegard, the examples taken from it, and its credit."""
import json
from pathlib import Path
import re
import sys
import unittest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'tests'))
import declauding_manifest  # noqa: E402

SKILL = REPO / '.agents/skills/declauding'
RECORD = json.loads((REPO / 'sources/declauding.json').read_text())
COMMIT = re.search(r'^declauding_commit := "([0-9a-f]{40})"$', (REPO / 'Justfile').read_text(), re.M).group(1)
REGISTER = (SKILL / 'references/register.md').read_text().split('\n')
# Every page that uses the skill, and so must credit Oskar Austegard
PAGES = ['README.md', 'GUIDE.md', 'EXAMPLES.md', 'docs/sources.md', 'docs/declauding.md', 'docs/why.md',
         'docs/checker.md', '.agents/skills/nossaifd/SKILL.md']
# A link to his repository that names a commit, a branch or a tag
LINK = re.compile(r'(?:github\.com/oaustegard/claude-skills/(?:blob|tree|raw|commit|blame)/'
                  r'|raw\.githubusercontent\.com/oaustegard/claude-skills/)([^/\s)#?]+)')


def pages():
    "The Markdown pages of the repository, outside the copy of the skill and the built site."
    skip = {'.git', '_site', '.quarto', '__pycache__'}
    for path in sorted(REPO.rglob('*')):
        parts = set(path.relative_to(REPO).parts)
        if path.is_file() and path.suffix in {'.md', '.qmd'} and not skip & parts and SKILL not in path.parents:
            yield path


def blocks(text):
    "Each paragraph, list item and table row of a page, outside code blocks."
    found, block, fence = [], [], False
    for line in text.split('\n') + ['']:
        if line.lstrip().startswith('```'):
            fence = not fence
            continue
        if fence:
            continue
        starts = re.match(r'^\s*(?:[-*+]|\d+\.)\s|^\s*\|', line)
        if not line.strip() or starts:
            if block:
                found.append('\n'.join(block))
            block = [line] if line.strip() else []
            if line.lstrip().startswith('|'):
                found.append(line)
                block = []
        else:
            block.append(line)
    return found


def examples(text):
    "Each example DC<n> of EXAMPLES.md, as (number, its block of text)."
    found = re.split(r'^(?=### )', text[text.index('## Patterns of model prose'):], flags=re.M)
    return [(int(m.group(1)), part) for part in found if (m := re.match(r'### DC(\d+)\. ', part))]


class CopyTest(unittest.TestCase):
    def test_the_record_names_the_commit_of_the_justfile_and_the_version_of_the_copy(self):
        self.assertEqual(RECORD['commit'], COMMIT)
        self.assertEqual(RECORD['version'], declauding_manifest.version())
        self.assertEqual(RECORD['version'], '0.14.0')

    def test_each_file_of_the_copy_is_the_file_of_the_record(self):
        self.assertEqual(declauding_manifest.digests(), {**RECORD['files'], **RECORD['changed']},
                         'the copy changed: run just declauding')

    def test_the_patch_changes_only_the_files_that_the_record_marks_as_changed(self):
        patch = (REPO / 'sources/declauding.patch').read_text()
        named = sorted(set(re.findall(r'^\+\+\+ b/\.agents/skills/declauding/(\S+)$', patch, re.M)))
        self.assertEqual(named, sorted(RECORD['changed']))
        self.assertEqual(named, ['references/fresh-eyes.md'])
        for path in named:
            self.assertNotEqual(RECORD['changed'][path], RECORD['files'][path])

    def test_the_patch_undone_gives_back_each_file_of_the_commit(self):
        import hashlib, shutil, subprocess, tempfile
        with tempfile.TemporaryDirectory() as temp:
            for path in RECORD['changed']:
                target = Path(temp) / '.agents/skills/declauding' / path
                target.parent.mkdir(parents=True)
                shutil.copy(SKILL / path, target)
            subprocess.run(['git', 'apply', '-R', str(REPO / 'sources/declauding.patch')], cwd=temp, check=True)
            for path in RECORD['changed']:
                data = (Path(temp) / '.agents/skills/declauding' / path).read_bytes()
                self.assertEqual(hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest(), RECORD['files'][path])

    def test_no_reference_names_a_docs_path_in_code_that_the_lint_reads_as_missing(self):
        "skill-package-maker fails a reference that names `docs/...` in code, as line 14 of fresh-eyes.md did"
        for path in (SKILL / 'references').glob('*.md'):
            self.assertNotRegex(path.read_text(), r'`docs/', path.name)

    def test_each_page_that_describes_the_copy_says_that_one_line_changed(self):
        for name in ('README.md', 'GUIDE.md', 'docs/sources.md', 'docs/declauding.md', '.agents/skills/nossaifd/SKILL.md'):
            text = re.sub(r'\s+', ' ', (REPO / name).read_text())
            self.assertRegex(text, r'one (changed )?sentence', name)
        for path in pages():
            for block in blocks(path.read_text()):
                if re.search(r'declauding|Austegard', block):
                    with self.subTest(page=str(path.relative_to(REPO)), block=block[:80]):
                        self.assertNotRegex(block, r'(?i)without changes|\bunchanged\b|no changes|not changed|one changed line|one line')

    def test_the_changed_sentence_names_oskar_austegard_and_not_the_author(self):
        "In the skill, the author is the writer of the draft, so the sentence names him"
        text = (SKILL / 'references/fresh-eyes.md').read_text()
        sentence = text[text.index('written the check ('):text.index('has the details)')]
        self.assertIn("Oskar Austegard's repository", sentence)
        self.assertNotIn("author's", sentence)
        self.assertNotIn('`', sentence)

    def test_the_recipe_checks_the_patch_before_it_removes_the_copy(self):
        recipe = (REPO / 'Justfile').read_text().split('\ndeclauding:', 1)[1].split('\n\n', 1)[0]
        self.assertLess(recipe.index('apply --check'), recipe.index('rm -rf .agents/skills/declauding'))

    def test_the_readme_says_what_to_do_when_the_patch_no_longer_applies(self):
        readme = re.sub(r'\s+', ' ', (REPO / 'README.md').read_text())
        self.assertIn('If the patch no longer applies, the recipe stops before it changes the copy', readme)
        self.assertIn('| `sources/declauding.patch` |', readme)

    def test_the_copy_keeps_the_whole_licence(self):
        licence = (SKILL / 'LICENSE').read_text()
        self.assertTrue(licence.startswith('MIT License\n\nCopyright (c) 2025 Oskar Austegard\n'))
        for part in ('Permission is hereby granted, free of charge', 'The above copyright notice and this permission',
                     'THE SOFTWARE IS PROVIDED "AS IS"'):
            self.assertIn(part, licence)

    def test_the_register_keeps_its_entries_and_its_examples(self):
        text = '\n'.join(REGISTER)
        self.assertEqual(len(re.findall(r'^## \d+\. ', text, re.M)), 56)
        self.assertGreaterEqual(text.count('> was:'), 50)


class ExamplesTest(unittest.TestCase):
    def setUp(self):
        self.examples = examples((REPO / 'EXAMPLES.md').read_text())

    def test_there_is_an_example_for_each_entry_but_the_first(self):
        self.assertEqual([number for number, _ in self.examples], list(range(2, 57)))

    def test_each_example_quotes_the_lines_that_it_cites_word_for_word(self):
        for number, block in self.examples:
            with self.subTest(example=number):
                spans = [(int(a), int(b or a)) for a, b in
                         re.findall(r'register\.md\?plain=1#L(\d+)(?:-L(\d+))?\)', block.split('\n```')[0])]
                self.assertTrue(spans)
                cited = '\n\n'.join('\n'.join(re.sub(r'^> ?', '', line) for line in REGISTER[a - 1:b])
                                    for a, b in spans)
                quoted = re.search(r'^```text\n(.*?)\n```', block, re.M | re.S).group(1)
                self.assertEqual(quoted, cited)

    def test_each_cited_span_lies_in_its_own_entry(self):
        for number, block in self.examples:
            for first in re.findall(r'register\.md\?plain=1#L(\d+)', block.split('\n```')[0]):
                heads = [line for line in REGISTER[:int(first)] if re.match(r'^## \d+\. ', line)]
                self.assertTrue(heads[-1].startswith(f'## {number}. '), (number, first))

    def test_each_example_credits_him_in_its_own_block(self):
        for number, block in self.examples:
            self.assertIn(f'Credit: Oskar Austegard, declauding skill, register entry {number}, ', block, number)


class CreditTest(unittest.TestCase):
    def test_each_page_that_uses_the_skill_credits_oskar_austegard(self):
        for name in PAGES:
            text = (REPO / name).read_text()
            self.assertIn('declauding', text, name)
            self.assertIn('Oskar Austegard', text, name)

    def test_each_block_that_links_to_his_work_names_him(self):
        "A paragraph, a list item or a table row copied alone keeps his credit, as the blocks with Reid's PDFs do."
        for path in pages():
            for block in blocks(path.read_text()):
                if 'oaustegard/claude-skills' in block or '.agents/skills/declauding' in block:
                    with self.subTest(page=str(path.relative_to(REPO)), block=block[:80]):
                        self.assertIn('Oskar Austegard', re.sub(r'\s+', ' ', block))

    def test_any_other_page_that_names_the_skill_credits_him(self):
        for path in pages():
            text = path.read_text()
            if re.search(r'declauding|oaustegard', text):
                self.assertIn('Oskar Austegard', re.sub(r'\s+', ' ', text), path.relative_to(REPO))

    def test_every_link_to_his_repository_names_the_commit_that_ships(self):
        for path in [*pages(), REPO / 'Justfile', REPO / '_smalldocs.yml']:
            for ref in LINK.findall(path.read_text()):
                self.assertEqual(ref, COMMIT, path.relative_to(REPO))

    def test_every_commit_and_version_in_the_prose_is_the_one_that_ships(self):
        for path in pages():
            # Only the blocks about the skill: other pages also name versions and commits of other things
            text = '\n'.join(b for b in blocks(path.read_text()) if re.search(r'declauding|Austegard', b))
            for short in re.findall(r'commit `?([0-9a-f]{7,40})\b', text):
                if 'f0d3630'.startswith(short[:7]):
                    continue  # the commit of Shreya Shankar's skill
                self.assertTrue(COMMIT.startswith(short), (path.relative_to(REPO), short))
            for version in re.findall(r'\bversion (\d+\.\d+\.\d+)', text):
                self.assertEqual(version, RECORD['version'], path.relative_to(REPO))

    def test_the_licence_of_the_readme_names_his_copyright(self):
        licence = (REPO / 'README.md').read_text().split('## Licence', 1)[1]
        self.assertIn('copyright (c) 2025 Oskar Austegard', licence)

    def test_each_rule_from_the_skill_names_him(self):
        guide = (REPO / 'GUIDE.md').read_text()
        # Rules 50 to 55 come from the skill, and the others take a part of it
        for number in [*range(50, 56), 9, 10, 20, 32, 34, 36, 37, 38, 43]:
            rule = re.search(rf'^{number}\. \*\*.*?(?=^\d+\. \*\*|^## )', guide, re.M | re.S).group(0)
            self.assertIn("Oskar Austegard's declauding skill", rule, number)


if __name__ == '__main__':
    unittest.main()

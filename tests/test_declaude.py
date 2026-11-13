"""Check the copy of the declaude skill by Oskar Austegard, the examples taken from it, and its credit."""
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'tests'))
import declaude_manifest  # noqa: E402

SKILL = REPO / '.agents/skills/declaude'
RECORD = json.loads((REPO / 'sources/declaude.json').read_text())
COMMIT = re.search(r'^declaude_commit := "([0-9a-f]{40})"$', (REPO / 'Justfile').read_text(), re.M).group(1)
REGISTER = (SKILL / 'references/register.md').read_text().split('\n')
# Every page that uses the skill, and so must credit Oskar Austegard
PAGES = ['README.md', 'GUIDE.md', 'EXAMPLES.md', 'docs/sources.md', 'docs/declaude.md', 'docs/why.md',
         'docs/checker.md', '.agents/skills/nossaifd/SKILL.md']
# A link to his repository that names a commit, a branch or a tag
LINK = re.compile(r'(?:github\.com/oaustegard/claude-skills/(?:blob|tree|raw|commit|blame)/'
                  r'|raw\.githubusercontent\.com/oaustegard/claude-skills/)([^/\s)#?]+)')


def pages(root=REPO):
    """The Markdown pages of the repository, outside the copy of the skill and the built site. The walk skips
    `.claude/`, where the worktrees of agents live, and any other folder with its own `.git`, which is another
    worktree or another repository."""
    skip = {'.git', '_site', '.quarto', '__pycache__', '.claude'}
    found = []
    for folder, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in skip and not os.path.lexists(os.path.join(folder, d, '.git'))]
        for name in files:
            path = Path(folder) / name
            if path.suffix in {'.md', '.qmd'} and SKILL not in path.parents:
                found.append(path)
    yield from sorted(found)


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
        self.assertEqual(RECORD['version'], declaude_manifest.version())
        self.assertEqual(RECORD['version'], '0.14.0')

    def test_each_file_of_the_copy_is_the_file_of_the_record(self):
        self.assertEqual(declaude_manifest.digests(), {**RECORD['files'], **RECORD['changed']},
                         'the copy changed: run just declaude')

    def test_the_patch_changes_only_the_files_that_the_record_marks_as_changed(self):
        patch = (REPO / 'sources/declaude.patch').read_text()
        named = sorted(set(re.findall(r'^\+\+\+ b/\.agents/skills/declaude/(\S+)$', patch, re.M)))
        self.assertEqual(named, sorted(RECORD['changed']))
        self.assertEqual(named, ['SKILL.md', 'hooks/hooks.json', 'references/fresh-eyes.md', 'tests/test_fresh_eyes.py'])
        for path in named:
            self.assertNotEqual(RECORD['changed'][path], RECORD['files'][path])

    def test_the_patch_undone_gives_back_each_file_of_the_commit(self):
        import hashlib, shutil, subprocess, tempfile
        with tempfile.TemporaryDirectory() as temp:
            for path in RECORD['changed']:
                target = Path(temp) / '.agents/skills/declaude' / path
                target.parent.mkdir(parents=True)
                shutil.copy(SKILL / path, target)
            subprocess.run(['git', 'apply', '-R', str(REPO / 'sources/declaude.patch')], cwd=temp, check=True)
            for path in RECORD['changed']:
                data = (Path(temp) / '.agents/skills/declaude' / path).read_bytes()
                self.assertEqual(hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest(), RECORD['files'][path])

    def test_no_reference_names_a_docs_path_in_code_that_the_lint_reads_as_missing(self):
        "skill-package-maker fails a reference that names `docs/...` in code, as line 14 of fresh-eyes.md did"
        for path in (SKILL / 'references').glob('*.md'):
            self.assertNotRegex(path.read_text(), r'`docs/', path.name)

    def test_no_path_in_the_copy_names_the_old_folder(self):
        "His folder is declauding upstream. A path to it breaks once the copy is named declaude"
        for path in SKILL.rglob('*'):
            if path.is_file() and path.name != 'CHANGELOG.md' and '__pycache__' not in path.parts:
                with self.subTest(file=str(path.relative_to(SKILL))):
                    self.assertNotRegex(path.read_text(errors='replace'), r'declauding/|skills/declauding')

    def test_each_page_that_describes_the_copy_says_that_it_has_three_changes(self):
        for name in ('README.md', 'GUIDE.md', 'docs/sources.md', 'docs/declaude.md', '.agents/skills/nossaifd/SKILL.md'):
            text = re.sub(r'\s+', ' ', (REPO / name).read_text())
            self.assertIn('three changes', text, name)
        for path in pages():
            for block in blocks(path.read_text()):
                if re.search(r'declaude|Austegard', block):
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
        recipe = (REPO / 'Justfile').read_text().split('\ndeclaude-copy:', 1)[1].split('\n\n', 1)[0]
        self.assertLess(recipe.index('apply --check'), recipe.index('rm -rf .agents/skills/declaude'))

    def declaude(self, *pages, code=1):
        "Run just declaude in a copy of the Justfile, with a stub linter that ends with this code."
        import shutil, subprocess, tempfile
        if not shutil.which('just'):
            self.skipTest('just is not installed')
        with tempfile.TemporaryDirectory() as temp:
            shutil.copy(REPO / 'Justfile', temp)
            stub = Path(temp) / '.agents/skills/declaude/scripts/declaude_lint.py'
            stub.parent.mkdir(parents=True)
            stub.write_text(f'import sys\nprint("LINT", sys.argv[1:])\nsys.exit({code})\n')
            (Path(temp) / 'my page.md').write_text('A page.\n')
            return subprocess.run(['just', 'declaude', *pages], cwd=temp, capture_output=True, text=True)

    def test_the_declaude_recipe_does_not_fail_on_candidates(self):
        run = self.declaude('my page.md')
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("LINT ['--skip-quoted', 'my page.md']", run.stdout)   # a name with a space stays whole

    def test_the_declaude_recipe_fails_on_a_missing_page_or_a_linter_that_cannot_run(self):
        run = self.declaude('my page.md', 'nope.md')
        self.assertNotEqual(run.returncode, 0)
        self.assertIn('no such file: nope.md', run.stderr)
        self.assertNotEqual(self.declaude('my page.md', code=2).returncode, 0)

    def test_the_declaude_recipe_runs_no_code_in_a_page_name(self):
        run = self.declaude('a$(echo hi).md')
        self.assertIn('no such file: a$(echo hi).md', run.stderr)

    def test_check_does_not_run_declaude_through_any_recipe_that_it_calls(self):
        justfile = (REPO / 'Justfile').read_text()
        bodies = dict(re.findall(r'^([a-z-]+)[^\n:]*:\n((?:    .*\n|\n(?=    ))*)', justfile, re.M))
        seen, todo = set(), ['check']
        while todo:
            name = todo.pop()
            if name in seen:
                continue
            seen.add(name)
            self.assertNotIn('declaude', bodies[name], name)
            todo += re.findall(r'^\s+just ([a-z-]+)', bodies[name], re.M)
        self.assertGreaterEqual(seen, {'check', 'lint', 'test', 'prose-check'})

    def test_the_readme_says_what_to_do_when_the_patch_no_longer_applies(self):
        readme = re.sub(r'\s+', ' ', (REPO / 'README.md').read_text())
        self.assertIn('If the patch no longer applies, the recipe stops before it changes the copy', readme)
        self.assertIn('| `sources/declaude.patch` |', readme)

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
            self.assertIn(f'Credit: Oskar Austegard, declaude skill, register entry {number}, ', block, number)


class CreditTest(unittest.TestCase):
    def test_the_walk_of_the_pages_skips_the_worktrees_of_agents_and_other_repositories(self):
        "The main checkout holds the worktrees of agents in .claude/worktrees. Their pages are not pages of this one"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ('README.md', 'docs/a.qmd', '.claude/worktrees/agent-1/README.md', '.claude/notes.md',
                         'worktree/README.md', 'nested/repo/a.md', '_site/a.md'):
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                (root / name).write_text('# A page\n')
            (root / '.claude/worktrees/agent-1/.git').write_text('gitdir: /elsewhere\n')   # a worktree has a .git file
            (root / 'worktree/.git').write_text('gitdir: /elsewhere\n')
            (root / 'nested/repo/.git').mkdir()                                              # a repository has a folder
            self.assertEqual([p.relative_to(root).as_posix() for p in pages(root)], ['README.md', 'docs/a.qmd'])

    def test_each_page_that_uses_the_skill_credits_oskar_austegard(self):
        for name in PAGES:
            text = (REPO / name).read_text()
            self.assertIn('declaude', text, name)
            self.assertIn('Oskar Austegard', text, name)

    def test_each_block_that_links_to_his_work_names_him(self):
        "A paragraph, a list item or a table row copied alone keeps his credit, as the blocks with Reid's PDFs do."
        for path in pages():
            for block in blocks(path.read_text()):
                if 'oaustegard/claude-skills' in block or '.agents/skills/declaude' in block:
                    with self.subTest(page=str(path.relative_to(REPO)), block=block[:80]):
                        self.assertIn('Oskar Austegard', re.sub(r'\s+', ' ', block))

    def test_any_other_page_that_names_the_skill_credits_him(self):
        for path in pages():
            text = path.read_text()
            if re.search(r'declaude|oaustegard', text):
                self.assertIn('Oskar Austegard', re.sub(r'\s+', ' ', text), path.relative_to(REPO))

    def test_every_link_to_his_repository_names_the_commit_that_ships(self):
        for path in [*pages(), REPO / 'Justfile', REPO / '_smalldocs.yml']:
            for ref in LINK.findall(path.read_text()):
                self.assertEqual(ref, COMMIT, path.relative_to(REPO))

    def test_every_commit_and_version_in_the_prose_is_the_one_that_ships(self):
        for path in pages():
            # Only the blocks about the skill: other pages also name versions and commits of other things
            text = '\n'.join(b for b in blocks(path.read_text()) if re.search(r'declaude|Austegard', b))
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
            self.assertIn("Oskar Austegard's declaude skill", rule, number)


class PassesTest(unittest.TestCase):
    "The steps for a pass of the skill after the guide, and the record of the passes on this repository"

    def setUp(self):
        self.page = re.sub(r'\s+', ' ', (REPO / 'docs/declaude.md').read_text())
        self.skill = re.sub(r'\s+', ' ', (REPO / '.agents/skills/nossaifd/SKILL.md').read_text())

    def test_the_skill_and_the_page_keep_bad_examples_and_run_the_three_passes(self):
        "An agent reads only the skill, so the skill carries each step that the page gives"
        for text in (self.page, self.skill):
            self.assertRegex(text, r'Do not change a bad example that (a|the) page shows on purpose')
            self.assertRegex(text, r'read each sentence against the register')
            self.assertIn('fix only what the revision broke', text)
            self.assertRegex(text, r'(?i)run the linter( of the declaude skill)? once more')
            self.assertRegex(text, r'Where the (declaude )?skill and the guide disagreed')

    def test_the_page_does_not_claim_what_the_passes_did_not_show(self):
        for claim in ('cannot find a staged paragraph, a riddle or a verb that needs a mind',
                      'most real findings come from this reading', 'a fourth pass adds nothing',
                      'earned its place', 'the full name of Rosalind Reid in each credit', 'most often',
                      '1 of 29', 'went through these steps', 'The record of each step'):
            self.assertNotIn(claim, self.page)
        for count in ('On GUIDE.md, 1 of 36 was real', '1 of 25 was real, and 2 were partly real',
                      '15 of the 104 candidates outside its quotations were real'):
            self.assertIn(count, self.page)

    def test_rule_13_keeps_the_wording_of_its_credit(self):
        guide = re.sub(r'\s+', ' ', (REPO / 'GUIDE.md').read_text())
        self.assertIn("The reason that a reader gives the end the most weight is this guide's own", guide)


class NameAndCallTest(unittest.TestCase):
    "The package calls the skill declaude, installs it with npx, and calls it from step 6 of the nossaifd skill"

    def test_the_copy_names_the_skill_declaude_and_the_pages_say_that_he_calls_it_declauding(self):
        self.assertRegex((SKILL / 'SKILL.md').read_text(), r'(?m)^name: declaude$')
        for name in ('README.md', 'GUIDE.md', 'EXAMPLES.md', 'docs/declaude.md', '.agents/skills/nossaifd/SKILL.md'):
            self.assertRegex(re.sub(r'\s+', ' ', (REPO / name).read_text()), r'calls (it )?declauding', name)
        self.assertIn('wrote [the declauding skill]', (REPO / 'docs/sources.md').read_text())
        self.assertIn('the folder `declauding` of his repository', (REPO / 'docs/declaude.md').read_text())
        self.assertIn('folder `declauding`, version 0.14.0', re.sub(r'\s+', ' ', (REPO / 'GUIDE.md').read_text()))

    def test_no_page_uses_the_old_name_except_for_his_folder_and_his_own_name_for_it(self):
        for path in pages():
            text = re.sub(r'\s+', ' ', path.read_text())
            text = re.sub(r'github\.com/oaustegard/claude-skills/\S*?declauding', '', text)
            text = re.sub(r'(calls( it)?|named it|the name|wrote \[the|folder `|folder, `|old name of the skill,)\s*declauding', '', text)
            text = text.replace('src/declauding', '')
            self.assertNotRegex(text, r'declauding', path.relative_to(REPO))

    def test_npx_installs_both_skills(self):
        manifest = json.loads((REPO / 'skill-package.json').read_text())
        self.assertEqual(manifest['npx']['install'], "npx skills add rahuldave/nossaifd -a codex --skill '*' -y")
        self.assertEqual([s['name'] for s in manifest['skills']], ['nossaifd', 'declaude'])
        self.assertIn(manifest['npx']['install'], (REPO / 'README.md').read_text())

    def test_the_description_of_the_copy_waits_for_the_draft_and_names_step_6(self):
        description = re.search(r'(?m)^description: (.*)$', (SKILL / 'SKILL.md').read_text()).group(1)
        for part in ('The nossaifd skill calls it at its step 6', 'after the draft passes the nossaifd checker',
                     'an agent that did not write the draft', 'Do not load it before the draft exists',
                     'Do not change a bad example'):
            self.assertIn(part, description)
        self.assertNotIn('at the start of any task', description)

    def assertInOrder(self, text, parts, where):
        "Each part comes after the one before it in the text"
        at = -1
        for part in parts:
            found = text.find(part, at + 1)
            self.assertGreater(found, at, f'{where}: {part!r} is missing or out of order')
            at = found

    def test_the_passes_run_in_order_with_a_fresh_agent_for_the_declaude_pass(self):
        "Guide and checker, then the declaude pass in a fresh agent, then the checker, then the linter once more"
        def flat(name):
            return re.sub(r'\s+', ' ', (REPO / name).read_text())
        skill = flat('.agents/skills/nossaifd/SKILL.md')
        self.assertInOrder(skill[skill.index('## Steps'):], ['4. Run the checker', 'give the page to a subagent that did not write it',
                           'steps of the declaude skill', '7. Run the checker again', 'fix only what the revision broke',
                           '8. Run the linter of the declaude skill once more'], 'SKILL.md')
        guide = flat('GUIDE.md')
        guide = guide[guide.index('## Check the result'):guide.index('## Sources')]
        self.assertInOrder(guide, ['uv run --no-project python check.py page.md', 'an agent that did not write it',
                           'declaude_diff.py', 'Then run `check.py` again, and fix only what the revision broke',
                           'Run the linter once more'], 'GUIDE.md')
        page = flat('docs/declaude.md')
        page = page[page.index('## How to use it with the guide'):page.index('## The passes on the pages')]
        self.assertInOrder(page, ['2. Run `check.py` on the draft', 'an agent that did not write it', '4. Run its diff',
                           '5. Run `check.py` again, and fix only what the revision broke', '6. Run the linter once more'],
                           'docs/declaude.md')
        readme = flat('README.md')
        self.assertInOrder(readme, ['3. Run the checker on the result', 'an agent that did not write it',
                           '5. Run the checker again, and fix only what the revision broke',
                           'run the linter of the declaude skill once more'], 'README.md')

    def test_every_link_to_his_repository_names_his_folder(self):
        for path in pages():
            for link in re.findall(r'https://github\.com/oaustegard/claude-skills/(?:tree|blob)/\S+?(?=[)\s])', path.read_text()):
                with self.subTest(page=str(path.relative_to(REPO)), link=link[:90]):
                    self.assertIn(f'/{COMMIT}/declauding', link)

    def test_rule_55_keeps_bad_examples(self):
        guide = re.sub(r'\s+', ' ', (REPO / 'GUIDE.md').read_text())
        rule = guide[guide.index('55. **'):guide.index('## Check the result')]
        self.assertIn('Keep word for word each bad example that the page shows on purpose', rule)


if __name__ == '__main__':
    unittest.main()

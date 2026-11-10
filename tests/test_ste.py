"""Check that no page claims a rule of ASD-STE100 that was not checked against the standard."""
from pathlib import Path
import re
import unittest

REPO = Path(__file__).resolve().parents[1]
GUIDE = (REPO / 'GUIDE.md').read_text()
WHY = (REPO / 'docs/why.md').read_text()
ABOUT = 'https://www.asd-ste100.org/about.html'
ANCHOR = 'why.md#asd-ste100-rules-from-memory'
UNCHECKED = 'from memory and not checked'
# Every spelling of the standard's name
NAMES = re.compile(r'\bSTE\b|Simplified Technical English|ASD-STE100', re.I)
PAGES = ['README.md', 'GUIDE.md', 'EXAMPLES.md', 'docs/sources.md', 'docs/why.md', 'docs/checker.md',
         'docs/declauding.md', 'index.qmd', '.agents/skills/nossaifd/SKILL.md']


def rules():
    "Each numbered rule of the guide, as (number, its text)."
    return [(int(m.group(1)), m.group(0)) for m in
            re.finditer(r'^(\d+)\. \*\*.*?(?=^\d+\. \*\*|^## )', GUIDE, re.M | re.S)]


def section():
    return WHY[WHY.index('## ASD-STE100 rules from memory'):]


class SteTest(unittest.TestCase):
    def test_only_rule_2_credits_ste_as_checked(self):
        "The about page confirms only one word for one meaning, rule 2"
        for number, text in rules():
            if NAMES.search(text) and number != 2:
                with self.subTest(rule=number):
                    self.assertIn(UNCHECKED, text)
                    self.assertNotIn(ABOUT, text)
        self.assertIn(ABOUT, dict(rules())[2])

    def test_each_rule_that_names_ste_is_in_the_list_of_why_md(self):
        listed = {int(n) for n in re.findall(r'^- rule (\d+),', section(), re.M)}
        named = {number for number, text in rules() if NAMES.search(text) and number != 2}
        self.assertEqual(listed, named)

    def test_each_mark_of_the_guide_links_to_the_list(self):
        for number, text in rules():
            if UNCHECKED in text:
                self.assertIn(f'[{UNCHECKED}](https://github.com/rahuldave/nossaifd/blob/main/docs/{ANCHOR})', text, number)
        self.assertIn('## ASD-STE100 rules from memory', WHY)

    def test_each_link_to_a_section_of_a_page_of_docs_finds_its_heading(self):
        "A renamed heading breaks every link to it, and smalldocs check does not check anchors"
        def slugs(page):
            return {re.sub(r'[^a-z0-9 -]', '', h.lower()).replace(' ', '-')
                    for h in re.findall(r'^#+ (.+)$', page.read_text(), re.M)}
        pages = [REPO / n for n in ('README.md', 'GUIDE.md', 'EXAMPLES.md', 'index.qmd')]
        pages += sorted((REPO / 'docs').glob('*.md')) + sorted((REPO / '.agents/skills/nossaifd').rglob('*.md'))
        for page in pages:
            for name, anchor in re.findall(r'(?:docs/|\]\()([a-z]+)\.md#([a-z0-9-]+)', page.read_text()):
                target = REPO / 'docs' / f'{name}.md'
                if target.exists():
                    with self.subTest(page=str(page.relative_to(REPO)), link=f'{name}.md#{anchor}'):
                        self.assertIn(anchor, slugs(target))
        self.assertIn(ANCHOR.split('#')[1], slugs(REPO / 'docs/why.md'))

    def test_each_block_of_each_page_that_names_ste_marks_its_rules_as_unchecked(self):
        "A paragraph, an item or a row that names STE says from memory, or that only the about page was read"
        import sys
        sys.path.insert(0, str(REPO / 'tests'))
        from test_declauding import blocks
        allowed = re.compile(r'from memory|about page|not checked|No copy of (the|ASD-STE100)', re.I)
        for name in PAGES:
            path = REPO / name
            if not path.exists():
                continue
            for block in blocks(path.read_text()):
                if block.lstrip().startswith('#') or not NAMES.search(block):
                    continue
                # Rule 2 cites the about page itself, and the list of unchecked rules follows its own heading
                if 'one word, one meaning' in block or re.match(r'\s*- rule \d+,', block):
                    continue
                with self.subTest(page=name, block=block[:80]):
                    self.assertRegex(block, allowed)

    def test_the_guide_rules_that_take_parts_of_ste_still_name_it(self):
        "A mutation that adds a new credit in another spelling is caught by the list test"
        self.assertTrue(NAMES.search('From: the writing rules of Simplified Technical English'))
        self.assertTrue(NAMES.search('asd-ste100'))

    def test_the_list_defines_ste_and_its_issue(self):
        text = re.sub(r'\s+', ' ', section())
        self.assertIn('ASD-STE100, Simplified Technical English (STE), is a standard', text)
        self.assertIn('Issue 8 is the edition', text)

    def test_the_last_paragraph_says_what_the_guide_does_with_each_part(self):
        text = re.sub(r'\s+', ' ', section())
        self.assertIn('the rule against the -ing form as a verb as preferences', text)
        self.assertIn('six sentences in a paragraph a hard limit of its own', text)
        self.assertIn('two nouns in a row', text)

    def test_rule_16_does_not_make_the_20_words_absolute(self):
        self.assertNotIn('20 words or fewer', dict(rules())[16])
        self.assertIn('about 20 words', dict(rules())[16])

    def test_no_page_says_that_only_the_about_page_is_public(self):
        "No one checked what else the site makes public, so no page claims it"
        for name in ('GUIDE.md', 'README.md', 'docs/sources.md', 'docs/why.md', 'EXAMPLES.md'):
            text = re.sub(r'\s+', ' ', (REPO / name).read_text())
            self.assertNotRegex(text, r'(?i)only (the|its) about page is public', name)
            self.assertNotIn('three of its rules come from memory', text, name)

    def test_the_sources_page_links_to_the_list_and_does_not_contradict_rule_1(self):
        text = (REPO / 'docs/sources.md').read_text()
        self.assertIn(f']({ANCHOR})', text)
        self.assertNotIn('dictionary of approved words is not part of the guide', re.sub(r'\s+', ' ', text))
        self.assertNotIn('is not part of this guide', re.sub(r'\s+', ' ', GUIDE))


if __name__ == '__main__':
    unittest.main()

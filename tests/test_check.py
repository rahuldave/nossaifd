"""Check each rule of check.py: the hard problems, the soft notes, and what the checker skips."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location('nossaifd_check', REPO / 'check.py')
checker = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(checker)


def run(text):
    "Check one page of text. Return the hard problems and the soft notes."
    with tempfile.TemporaryDirectory() as temp:
        page = Path(temp) / 'page.md'
        page.write_text(text, encoding='utf-8')
        return checker.check(page)


class HardRules(unittest.TestCase):
    def assertHard(self, text, part):
        hard, _ = run(text)
        self.assertTrue(any(part in h for h in hard), f'{part!r} not in {hard}')

    def assertClean(self, text):
        hard, _ = run(text)
        self.assertEqual(hard, [])

    def test_a_sentence_of_more_than_25_words(self):
        self.assertHard(' '.join(['word'] * 26) + '.\n', '26 words (at most 25)')
        self.assertClean(' '.join(['word'] * 25) + '.\n')

    def test_an_instruction_of_more_than_20_words(self):
        self.assertHard('Open ' + ' '.join(['word'] * 20) + '.\n', '21 words (at most 20)')
        self.assertClean('Open ' + ' '.join(['word'] * 19) + '.\n')

    def test_a_paragraph_of_more_than_six_sentences(self):
        self.assertHard('The cat sat. ' * 7 + '\n', 'a paragraph of 7 sentences')
        self.assertClean('The cat sat. ' * 6 + '\n')

    def test_a_contraction(self):
        for word in ("don't", "it's", "we're", "they'll"):
            self.assertHard(f'The team says {word} here.\n', 'a contraction')

    def test_dashes_a_middle_dot_and_curly_quotes(self):
        self.assertHard('The build is fast — it ends.\n', 'an em dash')
        self.assertHard('Wait 10–20 seconds.\n', 'an en dash')
        self.assertHard('The tool · the guide.\n', 'a middle dot')
        self.assertHard('The “event” is logged.\n', 'a curly quote')
        self.assertHard('The team’s tool works.\n', 'a curly quote')

    def test_a_colon_between_clauses_but_not_after_a_short_label(self):
        self.assertHard('The parser reads the file: the feature fires.\n', 'a colon between clauses')
        self.assertClean('Note: the parser reads the file.\n')

    def test_latin_abbreviations(self):
        for word in ('e.g.', 'i.e.', 'etc.'):
            self.assertHard(f'The tool reads files, {word} the guide.\n', "write 'for example'")

    def test_not_just_and_not_only(self):
        self.assertHard('It is not just a parser.\n', "'not just' or 'not only'")
        self.assertHard('It is not only a parser.\n', "'not just' or 'not only'")

    def test_a_count_at_the_start_of_a_paragraph_an_item_or_a_heading(self):
        self.assertHard('Three things to know. The tool is fast.\n', 'opens with a count')
        self.assertHard('- Two cautions. The tool is slow.\n', 'opens with a count')
        self.assertHard('## Three things to know.\n', 'a heading that opens with a count')
        for text in ('Two cautions:\n', 'Three key points.\n', 'A few notes:\n', 'Four steps to follow.\n'):
            self.assertHard(text, 'opens with a count')

    def test_a_sentence_of_fact_that_starts_with_a_number_is_not_a_count(self):
        for text in ('Three runs failed today.\n', 'Two tests timed out.\n', '- Five nodes went down.\n',
                     'Two servers share the cache.\n', '## Two servers share the cache.\n',
                     'Several issues remain open.\n', 'Two questions remain open.\n', 'Two rules apply here.\n',
                     'Two issues were fixed.\n'):
            self.assertClean(text)

    def test_a_vague_demonstrative(self):
        self.assertHard('The tool reads files. This is fast.\n', 'a vague demonstrative')
        self.assertClean('The tool reads files. This flag is fast.\n')

    def test_two_questions_in_a_row(self):
        self.assertHard('Is it fast? Is it safe?\n', 'two questions in a row')
        self.assertClean('Is it fast? The tests say yes.\n')

    def test_the_exit_status(self):
        import subprocess, sys
        with tempfile.TemporaryDirectory() as temp:
            bad, good = Path(temp) / 'bad.md', Path(temp) / 'good.md'
            bad.write_text("It's fast.\n")
            good.write_text('The tool is fast.\n')
            run_ = lambda p: subprocess.run([sys.executable, REPO / 'check.py', p], capture_output=True, text=True)
            self.assertEqual(run_(bad).returncode, 1)
            self.assertEqual(run_(good).returncode, 0)


class Exemptions(unittest.TestCase):
    def test_code_tables_quotes_and_link_targets_are_not_checked(self):
        page = ('```\nit\'s — e.g. ' + 'word ' * 40 + '\n```\n\n'
                '| Cell |\n|---|\n| don\'t — e.g. |\n\n'
                'Write "don\'t" and `it\'s` here.\n\n'
                'Read [the guide](https://example.com/e.g./don\'t).\n')
        hard, _ = run(page)
        self.assertEqual(hard, [])


class SoftNotes(unittest.TestCase):
    def soft(self, text):
        return run(text)[1]

    def test_a_noun_that_names_an_action(self):
        for phrase in ('a measurement of the latency', 'the creation of the data', 'an improvement of speed',
                       'the performance of the cache', 'the extension of the method'):
            notes = self.soft(f'We made {phrase}.\n')
            self.assertTrue(any('an action in a noun' in n for n in notes), (phrase, notes))

    def test_the_note_for_an_action_noun_is_soft_and_not_hard(self):
        hard, soft = run('The team made a measurement of the latency.\n')
        self.assertEqual(hard, [])
        self.assertTrue(any('measurement of' in n for n in soft))

    def test_a_noun_that_names_a_thing_gets_no_note(self):
        for phrase in ('a section of the guide', 'a version of the tool', 'the size of the font',
                       'a measurement in the log', 'a sentence of ten words'):
            notes = self.soft(f'The page has {phrase}.\n')
            self.assertFalse(any('an action in a noun' in n for n in notes), (phrase, notes))

    def test_a_name_in_capitals_gets_no_note(self):
        for phrase in ('the Council for the Advancement of Science Writing', 'the Association of Europe'):
            notes = self.soft(f'The page names {phrase}.\n')
            self.assertFalse(any('an action in a noun' in n for n in notes), (phrase, notes))
        notes = self.soft('Measurement of the latency took a day.\n')   # a capital at the start of a sentence
        self.assertTrue(any('an action in a noun' in n for n in notes), notes)

    def test_a_capital_after_a_colon_a_semicolon_or_a_bracket_starts_a_sentence(self):
        for text in ('The plan: Measurement of the latency first.\n', 'We wait; Measurement of the latency is slow.\n',
                     'We wait (Measurement of the latency is slow).\n'):
            notes = self.soft(text)
            self.assertTrue(any('an action in a noun' in n for n in notes), (text, notes))

    def test_an_action_noun_in_quotes_or_code_gets_no_note(self):
        notes = self.soft('Write "the measurement of the latency" and `measurement of x` as examples.\n')
        self.assertFalse(any('an action in a noun' in n for n in notes), notes)

    def test_the_other_soft_notes(self):
        notes = ' '.join(self.soft('The file was read by the server; the tool is running and we utilize it.\n'))
        for part in ('maybe passive', 'a semicolon', 'an -ing form: running', "'utilize': try use"):
            self.assertIn(part, notes)


class SharedFunctions(unittest.TestCase):
    "The talk checker imports blocks(), plain() and sentences(), so their behavior must stay the same."

    def test_blocks(self):
        found = checker.blocks('# Title\n\nOne line\nand two.\n\n- An item.\n\n```\ncode\n```\n')
        self.assertEqual(found, [(1, 'Title', 'head'), (3, 'One line and two.', 'para'), (6, 'An item.', 'item')])

    def test_plain(self):
        self.assertEqual(checker.plain('Run `x y` on [the page](http://a.b) and "quoted words" **here**.'),
                         'Run CODE on the page and QUOTE here.')

    def test_sentences(self):
        self.assertEqual(checker.sentences('One. two? Three!'), ['One.', 'two?', 'Three!'])


if __name__ == '__main__':
    unittest.main()

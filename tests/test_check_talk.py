"""Check check_talk.py, the talk checker, and the presentations skill that ships it."""
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / '.agents/skills/presentations'
sys.path.insert(0, str(REPO))
import check_talk  # noqa: E402

SCRIPT = 'We cut the wait to one second.'


def run(text, *args, cwd=None):
    "Run the checker on a deck, from a folder outside the repository unless cwd is given."
    with tempfile.TemporaryDirectory() as temp:
        page = Path(temp) / 'deck.md'
        page.write_text(text, encoding='utf-8')
        return subprocess.run([sys.executable, str(REPO / 'check_talk.py'), '-v', *args, str(page)],
                              capture_output=True, text=True, cwd=cwd or temp)


def deck(*slides, matter=''):   # no front matter: no time slot, so no check of the length
    "A deck with a title slide, then the slides given, each with a short script unless it has notes."
    parts = ['# The talk\n\n<!--\nHello.\n-->\n']
    for slide in slides:
        parts.append(slide if ('<!--' in slide or 'Note:' in slide or 'notes' in slide)
                     else f'{slide}\n\n<!--\n{SCRIPT}\n-->\n')
    body = '\n---\n\n'.join(parts)
    return f'---\n{matter}\n---\n\n{body}' if matter else body


def problems(text, *args, slot=False):
    "The hard problems and the soft notes of a deck. The note for no time slot is left out unless slot is True."
    out = run(text, *args).stdout
    return ([line for line in out.splitlines() if line.startswith('  HARD ')],
            [line for line in out.splitlines() if line.startswith('  soft ')
             and (slot or not line.startswith('  soft no time slot'))])


class SplitTest(unittest.TestCase):
    def test_a_line_of_three_dashes_starts_a_slide(self):
        matter, slides = check_talk.split('# One\n\ntext\n\n---\n\n# Two\n\n---\n\n# Three\n')
        self.assertEqual(matter, {})
        self.assertEqual([s.title()[1] for s in slides], ['One', 'Two', 'Three'])
        self.assertEqual([s.first for s in slides], [1, 7, 11])

    def test_dashes_in_code_or_in_a_comment_do_not_start_a_slide(self):
        text = '# One\n\n```\n---\n```\n\n<!--\nnotes\n---\nmore\n-->\n\n---\n\n# Two\n'
        _, slides = check_talk.split(text)
        self.assertEqual(len(slides), 2)
        self.assertIn('more', ' '.join(t for _, t in slides[0].notes))

    def test_front_matter_gives_the_minutes_and_is_not_a_slide(self):
        matter, slides = check_talk.split('---\nmarp: true\nminutes: 20 min\n---\n\n# One\n')
        self.assertEqual(matter['minutes'], '20 min')
        self.assertEqual(check_talk.minutes_of(matter['minutes']), 20)
        self.assertEqual(len(slides), 1)
        self.assertEqual(slides[0].first, 6)

    def test_a_deck_that_opens_with_a_rule_has_no_front_matter(self):
        matter, slides = check_talk.split('---\n\n# One\n\n---\n\n# Two\n')
        self.assertEqual(matter, {})
        self.assertEqual(len(slides), 2)

    def test_slidev_front_matter_of_a_slide_is_not_a_slide(self):
        _, slides = check_talk.split('# One\n\n---\nlayout: center\n---\n\n# Two\n')
        self.assertEqual([s.title()[1] for s in slides], ['One', 'Two'])
        self.assertEqual(slides[1].matter, {'layout': 'center'})


class NotesTest(unittest.TestCase):
    def notes(self, text):
        _, slides = check_talk.split(text)
        return ' '.join(t.strip() for _, t in slides[0].notes).strip(), '\n'.join(slides[0].body)

    def test_an_html_comment_is_the_script(self):
        notes, body = self.notes('# One\n\nOn the slide.\n\n<!--\nSaid aloud.\n-->\n')
        self.assertEqual(notes, 'Said aloud.')
        self.assertNotIn('Said', body)
        self.assertEqual(self.notes('# One\n<!-- Said aloud. -->\n')[0], 'Said aloud.')

    def test_a_marp_directive_is_not_the_script(self):
        self.assertEqual(self.notes('# One\n\n<!-- _class: lead -->\n<!-- paginate: true -->\n')[0], '')

    def test_a_reveal_note_runs_to_the_end_of_the_slide(self):
        notes, body = self.notes('# One\n\nOn the slide.\n\nNote: Said aloud.\nAnd more.\n')
        self.assertEqual(notes, 'Said aloud. And more.')
        self.assertIn('On the slide.', body)
        self.assertEqual(self.notes('# One\n\nOn the slide.\n\nNote:\nSaid aloud.\n')[0], 'Said aloud.')

    def test_note_starts_the_script_only_in_a_reveal_deck(self):
        # Case matters, and the line must start with "Note:"
        for line in ('note: Said aloud.', 'Notes: Said aloud.', '  Note: Said aloud.'):
            notes, body = self.notes(f'# One\n\n{line}\n')
            self.assertEqual(notes, '', line)
            self.assertIn('Said aloud.', body)
        # A slide with an HTML comment as notes, or a deck with a marp key, does not read Note:
        for text in ('# One\n\nNote: the cache is cold.\n\n<!-- Said. -->\n',
                     '---\nmarp: true\n---\n\n# One\n\nNote: the cache is cold.\n'):
            _, slides = check_talk.split(text)
            self.assertNotIn('cache', ' '.join(t for _, t in slides[0].notes), text)
            self.assertIn('Note: the cache is cold.', '\n'.join(slides[0].body))

    def test_note_is_decided_for_each_slide(self):
        # An author's comment on the title slide does not turn off Note: on the later slides
        text = ('# The talk\n\n<!-- TODO: add the logo -->\n\n---\n\n# Cache halves the load\n\nThe hit rate\n\n'
                f'Note: {SCRIPT}\n\n---\n\n# Reads cause the wait\n\nThe wait\n\nNote:\n{SCRIPT}\n')
        _, slides = check_talk.split(text)
        self.assertEqual([' '.join(t for _, t in s.notes).strip() for s in slides[1:]], [SCRIPT, SCRIPT])
        self.assertEqual(problems(text), ([], []))

    def test_a_note_line_on_a_marp_slide_does_not_hide_the_slide(self):
        slide = ('# Cache halves the load\n\nNote: the cache is cold.\n\n' + ''.join(f'- item {i}\n' for i in range(6))
                 + '\n$$ a = b $$\n\n$$ c = d $$\n\n$$ e = f $$\n\n<!--\nWe cut the wait.\n-->\n')
        hard, _ = problems(deck(slide))
        self.assertTrue(any('6 items (at most 4)' in p for p in hard), hard)
        self.assertTrue(any('3 equations (at most 2)' in p for p in hard), hard)

    def test_a_marp_directive_line_in_a_comment_is_not_script(self):
        _, slides = check_talk.split('# One\n\n<!--\n_class: lead\nSaid aloud.\n-->\n')
        self.assertEqual([t.strip() for _, t in slides[0].notes if t.strip()], ['Said aloud.'])
        self.assertEqual([n for n, _ in slides[0].notes], [3, 4, 5, 6])   # the lines keep their numbers

    def test_a_script_line_that_starts_with_a_marp_key_is_script(self):
        _, slides = check_talk.split('# One\n\n<!--\ntitle: we explain the chart here.\nSaid aloud.\n-->\n')
        self.assertEqual([t.strip() for _, t in slides[0].notes if t.strip()],
                         ['title: we explain the chart here.', 'Said aloud.'])
        # A comment of only directives is still not script
        self.assertEqual(self.notes('# One\n\n<!--\ntitle: The talk\npaginate: true\n-->\n')[0], '')

    def test_a_pandoc_notes_block_is_the_script(self):
        notes, body = self.notes('# One\n\n::: notes\nSaid aloud.\n:::\n\nOn the slide.\n')
        self.assertEqual(notes, 'Said aloud.')
        self.assertIn('On the slide.', body)
        self.assertEqual(self.notes('# One\n\n::: {.notes}\nSaid.\n:::\n')[0], 'Said.')

    def test_an_aside_is_the_script(self):
        self.assertEqual(self.notes('# One\n\n<aside class="notes">\nSaid aloud.\n</aside>\n')[0], 'Said aloud.')
        self.assertEqual(self.notes('# One\n\n<aside class="notes">Said.</aside>\n')[0], 'Said.')


class SlideTest(unittest.TestCase):
    def test_at_most_four_items(self):
        four = '# Four points\n\n' + ''.join(f'- point {i}\n' for i in range(4))
        self.assertEqual(problems(deck(four))[0], [])
        hard, _ = problems(deck(four + '  - nested point\n'))
        self.assertTrue(any('5 items (at most 4)' in p for p in hard), hard)

    def test_about_thirty_words(self):
        words = ' '.join(['word'] * 25)
        self.assertEqual(problems(deck(f'# Short slide here\n\n{words}\n'))[0], [])
        hard, soft = problems(deck(f'# Long slide here\n\n{words} {words}\n'))
        self.assertTrue(any('words (about 30, at most 40)' in p for p in hard), hard)
        hard, soft = problems(deck(f'# Long slide here\n\n{words} more words here now\n'))
        self.assertEqual(hard, [])
        self.assertTrue(any('words (about 30)' in p for p in soft), soft)

    def test_table_cells_count_as_words_and_math_does_not(self):
        table = '| a b c d e | f g h i j |\n|---|---|\n' + '| a b c d e | f g h i j |\n' * 3
        hard, _ = problems(deck(f'# Table slide here\n\n{table}'))
        self.assertTrue(any('words' in p for p in hard), hard)
        math = '$$ a = b + c + d + e + f + g + h + i + j + k + l + m + n + o + p + q + r + s + t + u + v $$'
        self.assertEqual(problems(deck(f'# Math slide here\n\n{math}\n'))[0], [])

    def test_no_paragraph(self):
        self.assertEqual(problems(deck('# One sentence here\n\nThe cache halves the load.\n'))[0], [])
        hard, _ = problems(deck('# Two sentences here\n\nThe cache halves the load. It also saves money.\n'))
        self.assertTrue(any('a paragraph of 2 sentences' in p for p in hard), hard)
        hard, soft = problems(deck('# Item slide here\n\n- The cache halves it. It saves money.\n'))
        self.assertEqual(hard, [])
        self.assertTrue(any('an item of 2 sentences' in p for p in soft), soft)

    def test_few_equations(self):
        two = '# Two equations here\n\n$$ a = b $$\n\n$x = y$ and $5 and $10\n'
        self.assertEqual(problems(deck(two))[0], [])
        hard, _ = problems(deck('# Three equations here\n\n$$\na = b\n$$\n\n$x = y$ and $p < q$\n'))
        self.assertTrue(any('3 equations (at most 2)' in p for p in hard), hard)

    def test_an_equation_needs_a_script(self):
        hard, _ = problems(deck('# One equation here\n\n$$ a = b $$\n\n<!--\n-->\n'))
        self.assertTrue(any('an equation with no script' in p for p in hard), hard)

    def test_a_figure_needs_a_caption_or_a_label(self):
        for slide in ('# Figure slide here\n\n![](plot.png)\n\nExit rate for each trip length\n',
                      '# Figure slide here\n\nExit rate for each trip length\n![](plot.png)\n',
                      '# Figure slide here\n\n<figure><img src="p.png"><figcaption>Rate</figcaption></figure>\n'):
            self.assertEqual(problems(deck(slide))[0], [], slide)
        for slide in ('# Figure slide here\n\n![Exit rate](plot.png)\n',
                      '# Figure slide here\n\n<img src="plot.png">\n\n![](two.png)\n',
                      '# Figure slide here\n\n![bg](photo.jpg)\n\n![background chart](chart.png)\n'):
            hard, _ = problems(deck(slide))
            self.assertTrue(any('a figure with no caption' in p for p in hard), (slide, hard))

    def test_a_marp_background_is_not_a_figure(self):
        for slide in ('# Background slide here\n\n![bg](photo.jpg)\n',
                      '# Background slide here\n\n![bg left:40%](chart.png)\n',
                      '# Background slide here\n\n![bg](a.jpg) ![bg](b.jpg)\n'):
            self.assertEqual(problems(deck(slide))[0], [], slide)

    def test_an_abbreviation_does_not_end_a_sentence(self):
        for line in ('Fig. 2. Time for each step, in ms.', 'Our model vs. the baseline', 'U.S. users wait 8 s',
                     'Dr. Rao measured it, e.g. at nine.', 'No. 5 is the slowest step', 'Lee et al. found it.',
                     'It takes approx. 8 s at peak.', 'Figs. 3 and 4 show the load.', 'The test, i.e. the run, failed.'):
            hard, soft = problems(deck(f'# Abbreviation slide here\n\n{line}\n'))
            self.assertEqual(hard, [], line)
        hard, _ = problems(deck('# Two sentences here\n\nFig. 2 shows the wait. It also shows the load.\n'))
        self.assertTrue(any('a paragraph of 2 sentences' in p for p in hard), hard)

    def test_an_abbreviation_at_the_end_of_a_sentence_ends_it(self):
        for text in ('We beat the U.S. Then we won.', 'We met at 3 p.m. Then we left.', 'We use grep, etc. Then we stop.',
                     'Lee et al. Then we stop.', 'plain in Fig. 2. Every run'):
            self.assertEqual(len(check_talk.said(text)), 2, (text, check_talk.said(text)))
        for text in ('We left at 3 p.m. on Monday.', 'U.S. users wait 8 s', 'Fig. 2. Time for each step, in ms.'):
            self.assertEqual(len(check_talk.said(text)), 1, (text, check_talk.said(text)))
        hard, _ = problems(deck('# Sales on a slide\n\nSales grew in the U.S. Then they fell.\n'))
        self.assertTrue(any('a paragraph of 2 sentences' in p for p in hard), hard)

    def test_an_abbreviation_does_not_split_a_spoken_sentence(self):
        script = 'Our model vs. the baseline ' + 'word ' * 22 + 'ends.'   # one sentence of 28 words
        hard, _ = problems(deck(f'# Cache halves the load\n\n<!--\n{script}\n-->\n'))
        self.assertTrue(any('a spoken sentence of 28 words' in p for p in hard), hard)


class TitleTest(unittest.TestCase):
    def test_titles_start_with_the_words_that_set_them_apart(self):
        good = deck('# Cache halves the load', '# Database reads cause the wait')
        self.assertEqual(problems(good)[0], [])
        hard, _ = problems(deck('# Results of the cache', '# Results of the database'))
        self.assertTrue(any('same two words as slide 2' in p for p in hard), hard)

    def test_a_repeated_title_is_allowed(self):
        self.assertEqual(problems(deck('# Parts of the story', '# Cache halves the load', '# Parts of the story'))[0], [])

    def test_titles_share_one_structure(self):
        same = deck('# Cache halves the load', '# Reads cause the wait', '# Memory saves a server')
        self.assertEqual(problems(same), ([], []))
        hard, _ = problems(deck('# Cache halves the load', '# Reads cause the wait', '# Why is it slow?'))
        self.assertTrue(any('the title is a question' in p for p in hard), hard)
        hard, soft = problems(deck('# Why is it slow?', '# What did we do?', '# Cache halves the load'))
        self.assertEqual(hard, [])   # the title has no telling mark, so its structure is a guess
        self.assertTrue(any('most titles are a question' in p for p in soft), soft)
        hard, soft = problems(deck('# Cache halves the load', '# Reads cause the wait', '# Time for each step'))
        self.assertEqual(hard, [])
        self.assertTrue(any('the title is a noun phrase' in p for p in soft), soft)

    def test_a_guessed_title_against_a_majority_of_labels_is_soft(self):
        hard, soft = problems(deck('# Step 1: load the logs', '# Step 2: find the slow reads', '# What did not work',
                                   '# Step 3: cache the hot rows', '# Thanks to the team'))
        self.assertEqual(hard, [])
        self.assertEqual(sum('most titles are a label and a colon' in p for p in soft), 2, soft)

    def test_titles_with_no_majority_structure_are_a_mix(self):
        hard, soft = problems(deck('# Why do reads wait?', '# Results: the cache wins', '# Caching the hot rows now'))
        self.assertEqual(hard, [])
        self.assertFalse(any('most titles are' in p for p in soft), soft)
        mixes = [p for p in soft if 'the titles mix structures' in p]
        self.assertEqual(len(mixes), 1, soft)
        for name in ('a question', 'a label and a colon', 'an -ing phrase'):
            self.assertIn(name, mixes[0])

    def test_a_title_whose_own_punctuation_differs_is_hard(self):
        hard, _ = problems(deck('# Step 1: load the logs', '# Step 2: find the slow reads', '# Why is it slow?'))
        self.assertTrue(any('the title is a question' in p for p in hard), hard)

    def test_a_noun_after_of_or_the_is_not_a_verb(self):
        for title in ('Outline of the work', 'Cost of the cache', 'Time to find the rows', 'Work in progress'):
            self.assertEqual(check_talk.shape(title)[0], 'a noun phrase', title)
        for title in ('Database reads cause the wait', 'What did not work', 'The cache cuts the load'):
            self.assertEqual(check_talk.shape(title)[0], 'a sentence', title)

    def test_a_short_title_and_the_first_slide_are_left_out(self):
        text = deck('# Cache halves the load', '# Reads cause the wait', '# Questions?')
        self.assertEqual(problems(text)[0], [])
        self.assertEqual(problems('# Why a talk?\n\n<!-- Hi. -->\n\n---\n\n# Cache halves the load\n\n'
                                  '<!-- Hi. -->\n\n---\n\n# Reads cause the wait\n\n<!-- Hi. -->\n', '--minutes', '5')[0], [])

    def test_a_slide_with_no_title_is_a_soft_note(self):
        hard, soft = problems(deck('![](a.png)\n\nThe exit rate\n'))
        self.assertEqual(hard, [])
        self.assertTrue(any('no title' in p for p in soft), soft)


class ScriptTest(unittest.TestCase):
    def script(self, text, minutes=''):
        return problems(deck(f'# Cache halves the load\n\n<!--\n{text}\n-->\n', matter=minutes))

    def test_length_for_the_time_slot(self):
        sentence = 'The cache keeps each page for one minute. '
        self.script = lambda text: ScriptTest.script(self, text, 'minutes: 1')
        hard, soft = self.script(sentence * 12)   # 96 words, plus 1 of the title slide
        self.assertEqual((hard, [s for s in soft if 'words' in s and 'script has' in s]), ([], []))
        hard, _ = self.script(sentence * 16)
        self.assertTrue(any('more than 120 for 1 min' in p for p in hard), hard)
        hard, soft = self.script(sentence * 5)
        self.assertEqual(hard, [])
        self.assertTrue(any('fewer than 90 for 1 min' in p for p in soft), soft)

    def test_the_command_line_wins_over_the_front_matter(self):
        text = deck('# Cache halves the load\n\n<!--\n' + 'One two three four five six seven eight. ' * 20 + '\n-->\n',
                    matter='minutes: 1')
        self.assertTrue(problems(text)[0])
        self.assertEqual(problems(text, '--minutes', '2')[0], [])
        self.assertEqual(problems(text, '--minutes=2')[0], [])

    def test_no_time_slot_is_a_soft_note(self):
        hard, soft = problems(deck('# Cache halves the load\n\n<!--\nWe cut the wait.\n-->\n'), slot=True)
        self.assertEqual(hard, [])
        self.assertTrue(any('no time slot' in p for p in soft), soft)

    def test_a_long_script_for_one_slide_is_a_soft_note(self):
        _, soft = self.script('The cache keeps each page for one minute. ' * 16, minutes='minutes: 2')
        self.assertTrue(any('words of script, more than a minute' in p for p in soft), soft)

    def test_a_sentence_said_in_one_breath(self):
        self.assertEqual(self.script(' '.join(['word'] * 20) + '.')[0], [])
        hard, soft = self.script(' '.join(['word'] * 22) + '.')
        self.assertEqual(hard, [])
        self.assertTrue(any('more than one breath' in p for p in soft), soft)
        hard, _ = self.script(' '.join(['word'] * 26) + '.')
        self.assertTrue(any('a spoken sentence of 26 words' in p for p in hard), hard)

    def test_the_filler_so(self):
        hard, _ = self.script('So, the cache works.')
        self.assertTrue(any("the filler 'So,'" in p for p in hard), hard)
        hard, soft = self.script('The hit rate is high. So the load falls.')
        self.assertEqual(hard, [])
        self.assertTrue(any("starts with 'So'" in p for p in soft), soft)
        self.assertEqual(self.script('The hit rate is high, so the load falls.'), ([], []))

    def test_contractions_are_allowed_in_the_script(self):
        self.assertEqual(self.script("We didn't need a server, and it's fast."), ([], []))

    def test_a_question_that_the_next_sentence_answers(self):
        self.assertEqual(self.script('Why is it slow? The database reads each row again.'), ([], []))
        hard, _ = self.script('Why is it slow? Why now? The database reads each row again.')
        self.assertTrue(any('two questions in a row' in p for p in hard), hard)
        hard, soft = self.script('The database reads each row again. Why?')
        self.assertEqual(hard, [])
        self.assertTrue(any('does not answer' in p for p in soft), soft)

    def test_a_slide_with_no_script_is_a_soft_note(self):
        hard, soft = problems(deck('# Cache halves the load\n\n<!-- _class: lead -->\n'))
        self.assertEqual(hard, [])
        self.assertTrue(any('no script' in p for p in soft), soft)


class MinutesTest(unittest.TestCase):
    "The time slot, from the command line or the front matter, and the errors in it."

    def test_the_forms_of_a_time_slot(self):
        for value, minutes in (('20', 20), ('20 min', 20), ('12.5', 12.5), ('1:30', 1.5), ('5 minutes', 5)):
            self.assertEqual(check_talk.minutes_of(value), minutes, value)
        self.assertIsNone(check_talk.minutes_of(None))
        for value in ('twenty', 'abc', '', '0', '0:00', '1:75', '-5'):
            with self.assertRaises(ValueError, msg=value):
                check_talk.minutes_of(value)

    def test_an_unreadable_slot_in_the_front_matter_is_hard_and_names_the_value(self):
        body = deck('# Cache halves the load')
        for value, part in (('"twenty"', "'twenty'"), ('0', "'0' is not more than 0"), ('', "''")):
            hard, soft = problems(f'---\nminutes: {value}\n---\n\n{body}', slot=True)
            self.assertTrue(any(part in p and 'time slot' in p for p in hard), (value, hard))
            self.assertFalse(any('no time slot' in p for p in soft), soft)

    def test_one_minute_thirty_is_a_minute_and_a_half(self):
        out = run(deck('# Cache halves the load', matter='minutes: 1:30')).stdout
        self.assertIn('for 1.5 minutes', out)

    def test_usage_errors_end_with_status_two_and_a_message(self):
        for args in (['--minutes'], ['--minutes', 'abc'], ['--minutes', '0'], ['--minutes=x'], ['--bogus']):
            result = run(deck('# Cache halves the load'), *args) if args != ['--minutes'] else None
            if result is None:   # --minutes as the last word, with no value after it
                with tempfile.TemporaryDirectory() as temp:
                    page = Path(temp) / 'deck.md'
                    page.write_text(deck('# Cache halves the load'))
                    result = subprocess.run([sys.executable, str(REPO / 'check_talk.py'), str(page), '--minutes'],
                                            capture_output=True, text=True)
            self.assertEqual(result.returncode, 2, (args, result.stdout, result.stderr))
            self.assertNotIn('Traceback', result.stderr, args)
            self.assertIn('check_talk.py:', result.stderr, args)
        self.assertIn("'abc'", run(deck('# A'), '--minutes', 'abc').stderr)
        result = subprocess.run([sys.executable, str(REPO / 'check_talk.py'), 'no-such-deck.md'],
                                capture_output=True, text=True, cwd=REPO)
        self.assertEqual(result.returncode, 2)
        self.assertIn('no such file: no-such-deck.md', result.stderr)
        self.assertNotIn('Traceback', result.stderr)

    def test_a_byte_order_mark_keeps_the_front_matter(self):
        matter, slides = check_talk.split('\ufeff---\nminutes: 20\n---\n\n# One\n')
        self.assertEqual(matter, {'minutes': '20'})
        self.assertEqual(len(slides), 1)
        self.assertIn('for 20 minutes', run('\ufeff---\nminutes: 20\n---\n\n# One\n').stdout)

    def test_a_yaml_comment_after_the_minutes_is_left_out(self):
        matter, _ = check_talk.split('---\nminutes: 20 # slot\n---\n\n# One\n')
        self.assertEqual(matter['minutes'], '20')
        self.assertIn('for 20 minutes', run('---\nminutes: 20 # slot\n---\n\n# One\n').stdout)

    def test_a_file_that_is_not_utf8_is_a_usage_error(self):
        with tempfile.TemporaryDirectory() as temp:
            page = Path(temp) / 'bad.md'
            page.write_bytes(b'\xff\xfe')
            result = subprocess.run([sys.executable, str(REPO / 'check_talk.py'), str(page)],
                                    capture_output=True, text=True)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        self.assertIn('not UTF-8', result.stderr)

    def test_one_slide_is_one_slide(self):
        self.assertIn(': 1 slide, ', run('# One\n').stdout)
        self.assertIn(': 2 slides, ', run('# One\n\n---\n\n# Two\n').stdout)

    def test_an_empty_deck_is_hard(self):
        for text in ('', '\n\n', '---\nminutes: 5\n---\n'):
            result = run(text)
            self.assertEqual(result.returncode, 1, repr(text))
            self.assertIn('HARD no slides', result.stdout)


class DeckTest(unittest.TestCase):
    def test_the_example_deck_passes(self):
        result = run((REPO / 'tests/fixtures/deck.md').read_text())
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('8 slides', result.stdout)
        self.assertIn('0 hard', result.stdout)

    def test_a_failing_deck_ends_with_status_one(self):
        self.assertEqual(run(deck('# A\n\n' + '- x\n' * 5)).returncode, 1)

    def test_the_checker_runs_from_its_own_folder_in_the_skill(self):
        with tempfile.TemporaryDirectory() as temp:
            page = Path(temp) / 'deck.md'
            page.write_text((REPO / 'tests/fixtures/deck.md').read_text())
            result = subprocess.run([sys.executable, str(SKILL / 'scripts/check_talk.py'), str(page)],
                                    capture_output=True, text=True, cwd=temp)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class SkillTest(unittest.TestCase):
    def test_the_skill_ships_the_same_guide_and_checkers(self):
        self.assertEqual((SKILL / 'references/TALKS.md').read_bytes(), (REPO / 'TALKS.md').read_bytes(), 'run just sync')
        for name in ('check_talk.py', 'check.py'):
            self.assertEqual((SKILL / 'scripts' / name).read_bytes(), (REPO / name).read_bytes(), 'run just sync')
        self.assertEqual(sorted(p.name for p in (SKILL / 'references').iterdir()), ['TALKS.md'])

    def test_the_skill_names_itself_says_when_to_use_it_and_names_its_licence(self):
        text = (SKILL / 'SKILL.md').read_text()
        front = re.match(r'^---\nname: (.+)\ndescription: (.+)\nlicense: (.+)\n---\n', text)
        self.assertIsNotNone(front)
        self.assertEqual(front.group(1), 'presentations')
        self.assertIn('Use when', front.group(2))
        self.assertNotIn('python3 ', text)
        for ref in re.findall(r'`((?:references|scripts)/[\w./-]+)`', text):
            self.assertTrue((SKILL / ref).is_file(), ref)

    def test_every_link_in_both_skills_resolves(self):
        # The package linter reads every [text](target) in a skill's Markdown, also inside a code block, so this does too
        pages = sorted((REPO / '.agents/skills').glob('*/**/*.md'))
        self.assertTrue(any(p.name == 'TALKS.md' for p in pages) and any(p.name == 'GUIDE.md' for p in pages))
        for page in pages:
            for target in re.findall(r'\[[^\]]*\]\(([^)]*)\)', page.read_text(encoding='utf-8')):
                target = target.strip().split()[0] if target.strip() else target
                with self.subTest(page=str(page.relative_to(REPO)), target=target):
                    if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                        continue   # a URL or an anchor
                    path = target.split('#', 1)[0]
                    self.assertTrue(path and (page.parent / path).exists(), f'{target} does not resolve')

    def test_rosalind_reid_and_montgomery_are_credited(self):
        for path in (REPO / 'TALKS.md', REPO / 'docs/check-talk.md', SKILL / 'SKILL.md', REPO / 'check_talk.py',
                     SKILL / 'agents/openai.yaml'):
            text = path.read_text()
            self.assertIn('Rosalind Reid', text, path)
            self.assertIn('Montgomery', text, path)

    def test_a_link_to_a_line_of_a_skill_on_github_shows_the_source(self):
        # GitHub renders a SKILL.md, and only ?plain=1 shows its lines, so that #L51 reaches the line
        for name in ('GUIDE.md', 'TALKS.md'):
            text = (REPO / name).read_text(encoding='utf-8')
            links = re.findall(r'https://github\.com/\S+?/SKILL\.md[^)\s]*#L\d+[^)\s]*', text)
            self.assertTrue(links or name == 'GUIDE.md', name)
            for link in links:
                self.assertIn('SKILL.md?plain=1#L', link, (name, link))

    def test_links_to_reid_go_to_github_and_name_the_page(self):
        text = (REPO / 'TALKS.md').read_text()
        self.assertNotIn('rahuldave.com/nossaifd/sources', text)
        links = re.findall(r'\[([^\]]+)\]\((https://github.com/rahuldave/nossaifd/blob/main/sources/reid/[^)]+)\)', text)
        self.assertGreater(len(links), 30)
        for label, url in links:
            self.assertTrue((REPO / url.split('/blob/main/')[1]).is_file(), url)
            self.assertNotIn('#page', url)
            if 'page' not in label:
                self.assertIn(label, ('The tutorial deck', 'the presentation tips', 'the written reports'), label)
            else:   # each link names Rosalind Reid in full, or follows a link that does in the same rule
                self.assertRegex(label, r'^(Rosalind Reid, (tutorial deck|presentation tips|written reports), )?pages? ', label)


if __name__ == '__main__':
    unittest.main()

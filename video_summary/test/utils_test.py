"""Unit tests that test that utils methods work."""

import logging
import unittest
from copy import copy

from video_summary.objects.subtitle import Subtitle
from video_summary.threads.utils import fuse_subtitles, join_phrases, clean_phrases, normalize_times

# Logger
LOGGER_NAME = 'Test.Utils'
LOG = logging.getLogger(LOGGER_NAME)


class UtilsTest(unittest.TestCase):
    """Class with all the utils test methods."""

    def test_fuse_subtitles(self):
        """Unit test that test that fuse subtitles method works."""
        LOG.info('starting fuse subtitles\' test')
        subtitle_a = Subtitle("Hello", 10, 20, 2)
        subtitle_b = Subtitle("world!", 15, 25, 9)
        subtitle_c = Subtitle(None, 13, 23, None)
        subtitle_d = Subtitle(None, None, None, None)

        subtitles_ab = fuse_subtitles(subtitle_a, subtitle_b)
        self.assertEqual("Hello world!", subtitles_ab.text)
        self.assertEqual([10, 25], subtitles_ab.get_times())
        self.assertEqual(subtitles_ab.score, 11)

        subtitles_ac = fuse_subtitles(subtitle_a, subtitle_c)
        self.assertEqual(subtitles_ac.text, "Hello")
        self.assertEqual(subtitles_ac.score, 2)

        subtitles_ad = fuse_subtitles(subtitle_a, subtitle_d)
        self.assertEqual(subtitle_a.text, subtitles_ad.text)
        self.assertEqual(subtitle_a.get_times(), subtitles_ad.get_times())
        self.assertEqual(subtitle_a.score, subtitles_ad.score)

        subtitles_a_none = fuse_subtitles(subtitle_a, None)
        self.assertEqual(subtitle_a, subtitles_a_none)

        subtitles_dd = fuse_subtitles(subtitle_d, subtitle_d)
        self.assertIsNone(subtitles_dd.text)
        self.assertEqual([None, None], subtitles_dd.get_times())
        self.assertIsNone(subtitles_dd.score)

        subtitles_none_a = fuse_subtitles(None, subtitle_a)
        self.assertEqual(subtitle_a, subtitles_none_a)

        subtitles_none_none = fuse_subtitles(None, None)
        self.assertIsNone(subtitles_none_none)

        subtitles_abc = fuse_subtitles(subtitles_ab, subtitle_c)
        self.assertEqual("Hello world!", subtitles_abc.text)
        self.assertEqual([10, 25], subtitles_abc.get_times())
        LOG.info('ending fuse subtitles\' test')

    def test_join_phrases(self):
        """Unit test that test that join phrases method works."""
        LOG.info('starting join phrases\' test')
        subtitle_a = Subtitle("Hello", None, None, None)
        subtitle_b = Subtitle("world!", None, None, None)
        subtitle_c = Subtitle("This is my", None, None, None)
        subtitle_d = Subtitle(None, None, None, None)
        subtitle_e = Subtitle("test subtitle.", None, None, None)
        subtitle_list = [subtitle_a, None, subtitle_b, subtitle_c, subtitle_d, subtitle_e]

        result = join_phrases(subtitle_list)
        self.assertEqual(2, len(result))
        self.assertEqual("Hello world!", result[0].text)
        self.assertEqual("This is my test subtitle.", result[1].text)

        self.assertIsNone(join_phrases(None))
        self.assertEqual([], join_phrases([None, None, None]))
        LOG.info('ending join phrases\' test')

    def test_clean_phrases(self):
        """Unit test that test that clean phrases method works."""
        LOG.info('starting clean phrases\' test')
        stop_words = ['my', 'this', 'is', 'are', 'there']
        punctuation_signs = ['!', '.']

        subtitle_a = Subtitle("Hello world! This is my test subtitle.", None, None, None)
        subtitle_b = Subtitle("In this á subtitle there are ó accented characters.",
                              None, None, None)
        subtitle_c = Subtitle(None, None, None, None)

        result_without_clean = clean_phrases([copy(subtitle_a), copy(subtitle_b),
                                              copy(subtitle_c), None])
        self.assertEqual(len(result_without_clean), 3)
        self.assertEqual("Hello world! This is my test subtitle.", result_without_clean[0].text)
        self.assertEqual("In this á subtitle there are ó accented characters.",
                         result_without_clean[1].text)
        self.assertIsNone(result_without_clean[2].text)

        result_capital_letters = clean_phrases(
            [copy(subtitle_a), copy(subtitle_b), copy(subtitle_c)], remove_capital_letters=True)
        self.assertEqual("hello world! this is my test subtitle.", result_capital_letters[0].text)
        self.assertEqual("in this á subtitle there are ó accented characters.",
                         result_capital_letters[1].text)

        result_stop_words = clean_phrases([copy(subtitle_a), copy(subtitle_b), copy(subtitle_c)],
                                          remove_stop_words=True, stop_words=stop_words)
        self.assertEqual("Hello world! test subtitle.", result_stop_words[0].text)
        self.assertEqual("In á subtitle ó accented characters.", result_stop_words[1].text)

        result_punctuations = clean_phrases([copy(subtitle_a), copy(subtitle_b), copy(subtitle_c)],
                                            remove_punctuation=True,
                                            punctuation_signs=punctuation_signs)
        self.assertEqual("Hello world This is my test subtitle", result_punctuations[0].text)

        result_accents = clean_phrases([copy(subtitle_a), copy(subtitle_b), copy(subtitle_c)],
                                       remove_accents=True)
        self.assertEqual("In this a subtitle there are o accented characters.",
                         result_accents[1].text)

        result_all = clean_phrases([copy(subtitle_a), copy(subtitle_b), copy(subtitle_c)],
                                   remove_all=True, stop_words=stop_words,
                                   punctuation_signs=punctuation_signs)
        self.assertEqual("hello world test subtitle", result_all[0].text)
        self.assertEqual("in a subtitle o accented characters", result_all[1].text)

        self.assertIsNone(clean_phrases(None))
        LOG.info('ending clean phrases\' test')

    def test_normalize_times(self):
        """Unit test that test that normalize times' method works."""
        LOG.info('starting normalize times\' test')
        times_a = [[0, 5], [5, 15], [10, 12], [18, 25], [20, 30]]
        times_b = [[0, 5], None, [18, 25], [20, 30]]
        times_c = [None, None, None]

        result_a = normalize_times(times_a)
        self.assertEqual([[0, 15], [18, 30]], result_a)

        result_b = normalize_times(times_b)
        self.assertEqual([[0, 5], [18, 30]], result_b)

        result_c = normalize_times(times_c)
        self.assertEqual([], result_c)

        self.assertIsNone(normalize_times(None))
        LOG.info('ending normalize times\' test')


if __name__ == '__main__':
    unittest.main()

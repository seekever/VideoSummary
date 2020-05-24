""" The module for the subtitles analysis thread."""

import logging

import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from nltk.corpus import stopwords

from video_summary.context.subtitles_context import SubtitlesContext, Languages
from video_summary.threads.utils import VECTORING_SWITCHER, load_subtitles, join_phrases, clean_phrases

# Logger
LOGGER_NAME = 'App.Threads.SubtitlesAnalysis'
LOG = logging.getLogger(LOGGER_NAME)

# Switcher
SWITCHER_LANGUAGE = {
    Languages.ARABIC: "arabic",
    Languages.AZERBAIJANI: "azerbaijani",
    Languages.DANISH: "danish",
    Languages.DUTCH: "dutch",
    Languages.ENGLISH: "english",
    Languages.FINNISH: "finnish",
    Languages.FRENCH: "french",
    Languages.GERMAN: "german",
    Languages.GREEK: "greek",
    Languages.HUNGARIAN: "hungarian",
    Languages.INDONESIAN: "indonesian",
    Languages.ITALIAN: "italian",
    Languages.KAZAKH: "kazakh",
    Languages.NEPALI: "nepali",
    Languages.NORWEGIAN: "norwegian",
    Languages.PORTUGUESE: "portuguese",
    Languages.ROMANIAN: "romanian",
    Languages.RUSSIAN: "russian",
    Languages.SPANISH: "spanish",
    Languages.SWEDISH: "swedish",
    Languages.TURKISH: "turkish"
}


class SubtitlesAnalysis(QThread):
    """
    The subtitles analysis thread.

    ...

    Attributes
    ----------
    progress : signal
        the signal to change the progress bar

    Methods
    -------
    restart_thread()
        restart the subtitles analysis thread
    activate_thread()
        activate the subtitles analysis thread
    deactivate_thread()
        deactivate the subtitles analysis thread

    """

    # Signals
    progress = QtCore.pyqtSignal(int)

    def __init__(self):
        LOG.debug('initializing subtitles analysis thread')
        QThread.__init__(self)
        self.active = True
        self.restart = False
        LOG.info('subtitles analysis thread initialized')

    def run(self):
        """
        Method that analysis the subtitles and save the subtitles' list in the SubtitlesContext.
        """
        while True:
            LOG.debug('starting subtitle analysis')
            self.active = True
            self.restart = False

            # Load, join and clean the original subtitles
            if self.active:
                LOG.debug('loading and processing the original subtitles')
                with SubtitlesContext(read_only=True) as manager:
                    vectoring = VECTORING_SWITCHER.get(manager.vectoring_type)
                    stop_words = stopwords.words(SWITCHER_LANGUAGE.get(manager.language))
                    punctuation_list = list(manager.punctuation_signs)

                    subtitles_list = load_subtitles(manager.subtitles_path)
                    subtitles_list = join_phrases(subtitles_list)
                    subtitles_list = clean_phrases(
                        subtitles_list,
                        remove_capital_letters=manager.remove_capital_letters,
                        remove_stop_words=manager.remove_stop_words,
                        remove_punctuation=manager.remove_punctuation,
                        remove_accents=manager.remove_accents,
                        stop_words=stop_words,
                        punctuation_signs=punctuation_list)

                LOG.debug('original subtitles loaded and processed')

            # Create LSA matrix with the vectoring result
            if self.active:
                LOG.debug('vectoring subtitles')
                x = vectoring.fit_transform(
                    [sub.text for sub in subtitles_list])  # scattered matrix
                num_rows, num_columns = x.shape
                a = np.zeros(shape=(num_rows, num_columns))  # scattered matrix transformed

                for row in range(num_rows):
                    _, c_index = x.getrow(row).nonzero()
                    for column in c_index:
                        a[row, column] = x[row, column]
                LOG.debug('subtitles vectorized')

            # Run the SDV algorithm and select best phrases
            if self.active:
                LOG.debug('analysing subtitles')
                _, _, v = np.linalg.svd(a, full_matrices=False)  # phrase x concept matrix
                vt = v.T  # concept x phrase matrix

                best_phrases = []
                for index, i in enumerate(vt):
                    if self.active:
                        best_phrase = i.tolist().index(max(i))  # TODO: Select the n maxims
                        if best_phrase not in best_phrases:
                            best_phrases.append(best_phrase)
                        self.progress.emit(index / len(vt) * 100)
                    else:
                        break
                LOG.debug('subtitles analysed')

            # Add subtitle punctuation and save to SubtitlesContext
            if self.active:
                LOG.debug('punctuating subtitles')
                for index, i in enumerate(best_phrases):
                    subtitle = subtitles_list[i]
                    subtitle.score = len(best_phrases) - index
                LOG.debug('subtitles punctuated')

                LOG.debug('saving subtitles')
                with SubtitlesContext() as manager:
                    manager.subtitles_list = subtitles_list
                LOG.debug('subtitles saved')

            if self.active:
                self.progress.emit(100)

            LOG.debug('ending objects analysis')

            if not self.restart:
                break

    def restart_thread(self):
        """ Method that restart the subtitles analysis thread."""
        self.active = False
        self.restart = True
        self.progress.emit(0)
        LOG.info('subtitles analysis thread restart activate')

    def activate_thread(self):
        """ Method that activate the subtitles analysis thread."""
        self.active = True
        LOG.info('subtitles analysis thread activate')

    def deactivate_thread(self):
        """ Method that deactivate the subtitles analysis thread."""
        self.active = False
        LOG.info('subtitles analysis thread deactivate')

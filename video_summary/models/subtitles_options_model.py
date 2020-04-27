""" The module for the subtitles options window."""

import logging
import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog

from video_summary.context.subtitles_context import SubtitlesContext, VectoringType, Languages
from video_summary.models.model_interface import ModelInterface

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(ROOT_DIR, '../templates/', 'SubtitlesOptions.ui')

# Window
WINDOW_TITLE = "Subtitles options"

# Logger
LOGGER_NAME = 'App.Models.SubtitlesOptions'
LOG = logging.getLogger(LOGGER_NAME)

# Translate
TRANSLATE_VECTORING = {
    VectoringType.COUNTERS: "Counters",
    VectoringType.BINARIES_COUNTERS: "Binaries counters",
    VectoringType.N_GRAM_COUNTERS: "N-gram counters",
    VectoringType.TF_WITH_NORMALIZATION_L1: "TF with normalization L1",
    VectoringType.TF_WITH_NORMALIZATION_L2: "TF with normalization L2",
    VectoringType.TF_IDF: "TF-IDF",
    VectoringType.TF_IDF_WITH_SMOOTHING_IDF: "TF-IDF with smoothing IDF",
    VectoringType.TF_IDF_WITH_SMOOTHING_IDF_AND_NORMALIZATION_L1:
        "TF-IDF with smoothing IDF and normalization L1",
    VectoringType.TF_IDF_WITH_SMOOTHING_IDF_AND_NORMALIZATION_L2:
        "TF-IDF with smoothing IDF and normalization L2"
}

TRANSLATE_LANGUAGE = {
    Languages.ARABIC: "Arabic",
    Languages.AZERBAIJANI: "Azerbaijani",
    Languages.DANISH: "Danish",
    Languages.DUTCH: "Dutch",
    Languages.ENGLISH: "English",
    Languages.FINNISH: "Finnish",
    Languages.FRENCH: "French",
    Languages.GERMAN: "German",
    Languages.GREEK: "Greek",
    Languages.HUNGARIAN: "Hungarian",
    Languages.INDONESIAN: "Indonesian",
    Languages.ITALIAN: "Italian",
    Languages.KAZAKH: "Kazakh",
    Languages.NEPALI: "Nepali",
    Languages.NORWEGIAN: "Norwegian",
    Languages.PORTUGUESE: "Portuguese",
    Languages.ROMANIAN: "Romanian",
    Languages.RUSSIAN: "Russian",
    Languages.SPANISH: "Spanish",
    Languages.SWEDISH: "Swedish",
    Languages.TURKISH: "Turkish"
}

# Default value
DEFAULT_RESUME_PERCENTAGE = 0.3
DEFAULT_VECTORING_TYPE = VectoringType.COUNTERS
DEFAULT_REMOVE_PUNCTUATION = True
DEFAULT_PUNCTUATION_SIGNS = ['<', '?', ':', ';', '[', '.', '¿', '`', '@', '%', ')', '_',
                             '"', '+', '|', '¡', '^', '\\', '(', '/', '!', '>', ',', '}',
                             '=', '*', "'", ']', '&', '{', '~', '#', '$', '-']
DEFAULT_REMOVE_STOPWORDS = True
DEFAULT_CAPITAL_LETTERS = True
DEFAULT_REMOVE_ACCENTS = True
DEFAULT_LANGUAGE = Languages.ENGLISH


class SubtitlesOptions(QtWidgets.QMainWindow, ModelInterface):
    """
    The class for the subtitles options window.

    ...

    Attributes
    ----------
    path : str
        the subtitles path

    Methods
    -------
    load_subtitle()
        asks to the user the subtitles path
    """

    path = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        uic.loadUi(TEMPLATE_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)

        self.loadSubtitlesButton.clicked.connect(self.load_subtitle)
        self.previousButton.clicked.connect(self.previous_window)
        self.nextButton.clicked.connect(self.next_window)

        for mode in VectoringType:
            self.vectoringTypeBox.addItem(TRANSLATE_VECTORING.get(mode), userData=mode)

        for mode in Languages:
            self.subtitlesLanguagesBox.addItem(TRANSLATE_LANGUAGE.get(mode), userData=mode)

    def load_context(self):
        LOG.debug('loading context')
        with SubtitlesContext(read_only=True) as manager:
            self.path = manager.subtitles_path
            self.resumePercentageSlider.setValue(manager.resume_percentage
                                                 or DEFAULT_RESUME_PERCENTAGE)
            self.vectoringTypeBox.setCurrentIndex(manager.vectoring_type
                                                  or DEFAULT_VECTORING_TYPE)

            if manager.remove_punctuation is not None:
                self.removePunctuationBox.setChecked(manager.remove_punctuation)
            else:
                self.removePunctuationBox.setChecked(DEFAULT_REMOVE_PUNCTUATION)

            if manager.punctuation_signs is not None:
                self.punctuationCharactersEdit.setText(" ".join(manager.punctuation_signs))
            else:
                self.punctuationCharactersEdit.setText(" ".join(DEFAULT_PUNCTUATION_SIGNS))

            if manager.remove_stop_words is not None:
                self.removeStopWordsBox.setChecked(manager.remove_stop_words)
            else:
                self.removeStopWordsBox.setChecked(DEFAULT_REMOVE_STOPWORDS)

            if manager.remove_capital_letters:
                self.removeCapitalLettersBox.setChecked(manager.remove_capital_letters)
            else:
                self.removeCapitalLettersBox.setChecked(DEFAULT_CAPITAL_LETTERS)

            if manager.remove_accents is not None:
                self.removeAccentsBox.setChecked(manager.remove_accents)
            else:
                self.removeAccentsBox.setChecked(DEFAULT_REMOVE_ACCENTS)

            self.subtitlesLanguagesBox.setCurrentIndex(manager.language or DEFAULT_LANGUAGE)
        LOG.debug('context loaded')

    def save_context(self):
        LOG.debug('saving context')
        with SubtitlesContext() as manager:
            manager.subtitles_path = self.path
            manager.resume_percentage = self.resumePercentageSlider.value()
            manager.vectoring_type = self.vectoringTypeBox.currentData()
            manager.remove_punctuation = self.removePunctuationBox.isChecked()
            manager.punctuation_signs = list(set(list(
                "".join(self.punctuationCharactersEdit.text().split()))))
            manager.remove_stop_words = self.removeStopWordsBox.isChecked()
            manager.remove_capital_letters = self.removeCapitalLettersBox.isChecked()
            manager.remove_accents = self.removeAccentsBox.isChecked()
            manager.language = self.subtitlesLanguagesBox.currentData()
        LOG.debug('context saved')

    def reload_conditional_format(self):
        LOG.debug('reloading conditional format')
        self.nextButton.setVisible(self.check_data())
        self.punctuationCharactersEdit.setVisible(self.removePunctuationBox.isChecked())
        self.subtitlesLanguagesBox.setVisible(self.removeStopWordsBox.isChecked())
        LOG.debug('conditional format reloaded')

    def check_data(self):
        LOG.debug('checking data')
        if self.path is None:
            LOG.info('incorrect data (path is null)')
            return False
        if self.path == "":
            LOG.info('incorrect data (path is empty)')
            return False
        if not self.path.endswith('.srt'):
            LOG.info('incorrect data (selected subtitle is not srt format)')
            return False
        LOG.info('checked data: OK')
        return True

    def load_subtitle(self):
        """ Method that asks to the user the subtitles path."""
        LOG.debug('loadSubtitlesButton clicked')

        LOG.debug('opening file dialog')
        self.path = QFileDialog.getOpenFileName(self, 'Load file', '',
                                                "Subtitle files (*.srt)").__getitem__(0)
        LOG.debug('file dialog closed')

        self.reload_conditional_format()
        LOG.info('subtitle path: %s', self.path)

    def update_scenes_analysis_progress_bar(self, value):
        """
        Method that update the progress bar of the scenes analysis.

        Parameters
        ----------
        value : int
            the progress bar value (0 - 100)
        """

        LOG.debug('updating scenes analysis progress bar')
        self.sceneAnalysisBar.setValue(value)
        LOG.debug('scenes analysis progress bar updated: %s / 100', value)

    def update_objects_analysis_progress_bar(self, value):
        """
        Method that update the progress bar of the objects analysis.

        Parameters
        ----------
        value : int
            the progress bar value (0 - 100)
        """

        LOG.debug('updating progress bar')
        self.sceneAnalysisBar.setValue(value)
        LOG.debug('progress bar updated: %s / 100', value)

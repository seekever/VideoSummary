""" The module for the subtitles options window."""

import logging
import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog

from video_summary.context.general_context import GeneralContext, ResumeMode
from video_summary.context.subtitles_context import SubtitlesContext, VectoringType, Languages
from video_summary.controller.threads_controller import ThreadsController
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


class SubtitlesOptions(QtWidgets.QMainWindow, ModelInterface):
    """
    The class for the subtitles options window.

    ...

    Attributes
    ----------
    path : str
        the subtitles path
    detect_scenes : bool
        a boolean to activate the detect scenes' progress bar
    object_analysis : bool
        a boolean to activate the object analysis' progress bar

    """

    # Subtitle path
    path = None

    # Progress bars visibility
    detect_scenes = True
    object_analysis = True

    def __init__(self, *args, **kwargs):
        LOG.debug('initializing subtitle options window model')
        super().__init__(*args, *kwargs)

        uic.loadUi(TEMPLATE_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)

        self.loadSubtitlesButton.clicked.connect(self.load_subtitle)
        self.previousButton.clicked.connect(self.previous_window)
        self.nextButton.clicked.connect(self.next_window)
        self.removePunctuationBox.toggled.connect(self.reload_conditional_format)
        self.removeStopWordsBox.toggled.connect(self.reload_conditional_format)
        self.resumePercentageSlider.valueChanged.connect(self.reload_conditional_format)

        for mode in VectoringType:
            self.vectoringTypeBox.addItem(TRANSLATE_VECTORING.get(mode), userData=mode)

        for mode in Languages:
            self.subtitlesLanguagesBox.addItem(TRANSLATE_LANGUAGE.get(mode), userData=mode)

        ThreadsController.scenes_analysis_thread.progress.connect(
            self.update_scenes_analysis_progress_bar)
        ThreadsController.objects_analysis_thread.progress.connect(
            self.update_objects_analysis_progress_bar)

        self.update_scenes_analysis_progress_bar(0)
        self.update_objects_analysis_progress_bar(0)
        LOG.info('subtitle options window model initialized')

    def load_context(self):
        LOG.debug('loading context')
        with SubtitlesContext(read_only=True) as manager:
            self.path = manager.subtitles_path
            self.resumePercentageSlider.setValue(manager.resume_percentage)
            self.vectoringTypeBox.setCurrentIndex(manager.vectoring_type)
            self.removePunctuationBox.setChecked(manager.remove_punctuation)
            self.punctuationCharactersEdit.setText(" ".join(manager.punctuation_signs))
            self.removeStopWordsBox.setChecked(manager.remove_stop_words)
            self.removeCapitalLettersBox.setChecked(manager.remove_capital_letters)
            self.removeAccentsBox.setChecked(manager.remove_accents)
            self.subtitlesLanguagesBox.setCurrentIndex(manager.language)

        with GeneralContext(read_only=True) as manager:
            self.detect_scenes = manager.detect_scenes
            self.object_analysis = manager.resume_mode in (ResumeMode.OBJECTS,
                                                           ResumeMode.SUBTITLES_AND_OBJECTS)
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
        self.subtitlesPathLabel.setText(self.path)
        self.summaryPerccentageLabel.setText(str(self.resumePercentageSlider.value()))

        self.punctuationCharactersEdit.setVisible(self.removePunctuationBox.isChecked())
        self.languageWidget.setVisible(self.removeStopWordsBox.isChecked())
        self.scenesProgressWidget.setVisible(self.detect_scenes)
        self.objectsProgressWidget.setVisible(self.object_analysis)
        self.nextButton.setDisabled(not self.check_data())
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

    def next_window(self):
        super().next_window()
        if ThreadsController.subtitles_analysis_thread.isRunning():
            LOG.info('restarting subtitles analysis thread')
            ThreadsController.subtitles_analysis_thread.restart_thread()
        else:
            LOG.info('starting subtitles analysis thread')
            ThreadsController.subtitles_analysis_thread.start()

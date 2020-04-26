""" The module for the general options window."""

import logging
import os

from PyQt5 import uic, QtWidgets

from video_summary.context.general_context import ResumeMode, GeneralContext
from video_summary.models.model_interface import ModelInterface

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(ROOT_DIR, '../templates/', 'GeneralOptions.ui')

# Window
WINDOW_TITLE = "General options"

# Logger
LOGGER_NAME = 'App.Models.GeneralOptions'
LOG = logging.getLogger(LOGGER_NAME)

# Translate
TRANSLATE = {
    ResumeMode.SUBTITLES: "Subtitles",
    ResumeMode.OBJECTS: "Objects",
    ResumeMode.SUBTITLES_AND_OBJECTS: "Subtitles and objects"
}

# Default value
DEFAULT_RESUME_MODE = ResumeMode.SUBTITLES
DEFAULT_DETECT_SCENES = True
DEFAULT_SCENES_DIFFERENCE = 0.3


class GeneralOptions(QtWidgets.QMainWindow, ModelInterface):
    """ The class for the general options window. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        uic.loadUi(TEMPLATE_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)

        self.previousButton.clicked.connect(self.previous_window)
        self.nextButton.clicked.connect(self.next_window)
        self.scenesDetectionBox.toggled.connect(self.reload_conditional_format)

        for mode in ResumeMode:
            self.resumeTypeBox.addItem(TRANSLATE.get(mode), userData=mode)

    def load_context(self):
        LOG.debug('loading context')
        with GeneralContext() as manager:
            self.resumeTypeBox.setCurrentIndex(manager.resume_mode or DEFAULT_RESUME_MODE)
            if manager.detect_scenes is not None:
                self.scenesDetectionBox.setChecked(manager.detect_scenes)
            else:
                self.scenesDetectionBox.setChecked(DEFAULT_DETECT_SCENES)
            self.scenesDifSlider.setValue((manager.scenes_difference or
                                           DEFAULT_SCENES_DIFFERENCE) * 100)
        LOG.debug('context loaded')

    def save_context(self):
        LOG.debug('saving context')
        with GeneralContext() as manager:
            manager.resume_mode = self.resumeTypeBox.currentData()
            manager.detect_scenes = self.scenesDetectionBox.isChecked()
            manager.scenes_difference = self.scenesDifSlider.value() / 100
        LOG.debug('context saved')

    def reload_conditional_format(self):
        LOG.debug('reloading conditional format')
        self.scenesDifSlider.setVisible(self.scenesDetectionBox.isChecked())
        LOG.debug('conditional format reloaded')

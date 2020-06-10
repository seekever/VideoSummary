""" The module for the general options window."""

import logging
import os

from PyQt5 import uic, QtWidgets

from video_summary.context.general_context import ResumeMode, GeneralContext
from video_summary.controller.processes_controller import ProcessesController
from video_summary.models.model_interface import ModelInterface
from video_summary.utils import TRANSLATE_RESUME_MODE

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(ROOT_DIR, '../templates/', 'GeneralOptions.ui')

# Window
WINDOW_TITLE = "General options"

# Logger
LOGGER_NAME = 'App.Models.GeneralOptions'
LOG = logging.getLogger(LOGGER_NAME)


class GeneralOptions(QtWidgets.QMainWindow, ModelInterface):
    """ The class for the general options window. """

    def __init__(self, *args, **kwargs):
        LOG.debug('initializing general options window model')
        super().__init__(*args, *kwargs)

        uic.loadUi(TEMPLATE_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)

        self.previousButton.clicked.connect(self.previous_window)
        self.nextButton.clicked.connect(self.next_window)
        self.scenesDetectionBox.toggled.connect(self.reload_conditional_format)
        self.scenesDifSlider.valueChanged.connect(self.reload_conditional_format)

        for mode in ResumeMode:
            self.resumeTypeBox.addItem(TRANSLATE_RESUME_MODE.get(mode), userData=mode)
        LOG.info('general options window model initialized')

    def load_context(self):
        LOG.debug('loading context')
        with GeneralContext(read_only=True) as manager:
            self.resumeTypeBox.setCurrentIndex(manager.resume_mode)
            self.scenesDetectionBox.setChecked(manager.detect_scenes)
            self.scenesDifSlider.setValue(manager.scenes_difference * 100)
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
        self.sceneDifferenceWidget.setVisible(self.scenesDetectionBox.isChecked())
        self.sceneDifferenceLabel.setText(str(self.scenesDifSlider.value()))
        LOG.debug('conditional format reloaded')

    def next_window(self):
        super().next_window()
        with GeneralContext(read_only=True) as manager:
            if manager.detect_scenes:
                if ProcessesController.scenes_analysis_process.isRunning():
                    LOG.info('restarting scenes analysis process')
                    ProcessesController.scenes_analysis_process.restart_process()
                else:
                    LOG.info('starting scenes analysis process')
                    ProcessesController.scenes_analysis_process.start()

""" The module for the resume result window."""

import logging
import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog

from video_summary.context.general_context import GeneralContext
from video_summary.controller.threads_controller import ThreadsController
from video_summary.models.model_interface import ModelInterface

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(ROOT_DIR, '../templates/', 'ResumeResult.ui')

# Window
WINDOW_TITLE = "Resume result"

# Logger
LOGGER_NAME = 'App.Models.ResumeResult'
LOG = logging.getLogger(LOGGER_NAME)


class ResumeResult(QtWidgets.QMainWindow, ModelInterface):
    """
    The class for the resume result window.

    ...

    Attributes
    ----------
    path : str
        the final video's path

    Methods
    -------
    download_video()
        downloads the final video
    update_video_cut_progress_bar()
        update the progress bar of the video's cutting
    update_audio_save_progress_bar()
        update the progress bar of the audio's saving
    update_video_save_progress_bar()
        update the progress bar of the video's saving
    """

    # Final video path
    path = None

    def __init__(self, *args, **kwargs):
        LOG.debug('initializing resume result window model')
        super().__init__(*args, *kwargs)

        uic.loadUi(TEMPLATE_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)

        self.downloadButton.clicked.connect(self.download_video)

        ThreadsController.save_video_thread.progress_cut.connect(
            self.update_video_cut_progress_bar)
        ThreadsController.save_video_thread.progress_audio.connect(
            self.update_audio_save_progress_bar)
        ThreadsController.save_video_thread.progress_video.connect(
            self.update_video_save_progress_bar)

        self.update_video_cut_progress_bar(0)
        self.update_audio_save_progress_bar(0)
        self.update_video_save_progress_bar(0)
        LOG.info('resume result window model initialized')

    def download_video(self):
        """ Method that downloads the final video."""
        LOG.debug('downloadButton clicked')
        self.path = QFileDialog.getSaveFileName(
            self, 'Save file', '', "Video files (*.mp4)").__getitem__(0)
        with GeneralContext() as manager:
            manager.final_video_path = self.path

        if ThreadsController.save_video_thread.isRunning():
            LOG.info('restarting save video thread')
            ThreadsController.save_video_thread.restart_thread()
        else:
            LOG.info('starting save video thread')
            ThreadsController.save_video_thread.start()
        self.reload_conditional_format()

    def reload_conditional_format(self):
        LOG.debug('reloading conditional format')
        self.progressWidget.setVisible(self.VideoCutBar.value() > 0)
        self.downloadPathLabel.setText(self.path)
        LOG.debug('conditional format reloaded')

    def update_video_cut_progress_bar(self, value):
        """
        Method that update the progress bar of the video's cutting.

        Parameters
        ----------
        value : int
            the progress bar value (0 - 100)
        """

        LOG.debug('updating cut video progress bar')
        self.VideoCutBar.setValue(value)
        self.reload_conditional_format()
        LOG.debug('cut video progress bar updated: %s / 100', value)

    def update_audio_save_progress_bar(self, value):
        """
        Method that update the progress bar of the audio's saving.

        Parameters
        ----------
        value : int
            the progress bar value (0 - 100)
        """

        LOG.debug('updating save audio progress bar')
        self.AudioSaveBar.setValue(value)
        LOG.debug('save audio progress bar updated: %s / 100', value)

    def update_video_save_progress_bar(self, value):
        """
        Method that update the progress bar of the video's saving.

        Parameters
        ----------
        value : int
            the progress bar value (0 - 100)
        """

        LOG.debug('updating save video progress bar')
        self.VideoSaveBar.setValue(value)
        LOG.debug('save video progress bar updated: %s / 100', value)

""" The module for the model's interface."""
import logging

from PyQt5 import QtCore

# Logger
LOGGER_NAME = 'App.Models.Interface'
LOG = logging.getLogger(LOGGER_NAME)


class ModelInterface:
    """
    The model's interface.

    ...

    Attributes
    ----------
    next : signal
        the signal to change to the next window
    previous : signal
        the signal to change to the previous window

    Methods
    -------
    load_context()
        load the windows' context
    save_context()
        save the window's context
    reload_conditional_format()
        reload the format of the conditional widgets
    check_data()
        check if all context data is correct
    update_scenes_analysis_progress_bar(value)
        update the progress bar of the scenes analysis
    update_objects_analysis_progress_bar(value)
        update the progress bar of the objects analysis
    update_subtitles_analysis_progress_bar(value)
        update the progress bar of the subtitles analysis
    update_resume_progress_bar(value)
        update the progress bar of the resume
    previous_window()
        save context and pass to the previous window
    next_window()
        save context and pass to the next window
    """

    # Signals
    next = QtCore.pyqtSignal()
    previous = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.hide()

    def load_context(self):
        """ The method to load the windows' context."""

    def save_context(self):
        """ The method to save the windows' context."""

    def reload_conditional_format(self):
        """ The method to reload the format of the conditional widgets."""

    def check_data(self):
        """ The method to check if all context data is correct."""

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

        LOG.debug('updating objects analysis progress bar')
        self.objectAnalysisBar.setValue(value)
        LOG.debug('objects analysis progress bar updated: %s / 100', value)

    def update_subtitles_analysis_progress_bar(self, value):
        """
        Method that update the progress bar of the subtitles analysis.

        Parameters
        ----------
        value : int
            the progress bar value (0 - 100)
        """

        LOG.debug('updating subtitles analysis progress bar')
        self.subtitleAnalysisBar.setValue(value)
        LOG.debug('subtitles analysis progress bar updated: %s / 100', value)

    def update_resume_progress_bar(self, value):
        """
        Method that update the progress bar of the resume.

        Parameters
        ----------
        value : int
            the progress bar value (0 - 100)
        """

        LOG.debug('updating resume progress bar')
        self.resumeBar.setValue(value)
        LOG.debug('resume progress bar updated: %s / 100', value)

    def previous_window(self):
        """ Method that save context and pass to the previous window."""
        LOG.debug('previousButton clicked')
        self.save_context()

        LOG.debug('changing to previous window')
        self.hide()
        self.previous.emit()
        LOG.info('window changed to the previous')

    def next_window(self):
        """ Method that save context and pass to the next window."""
        LOG.debug('nextButton clicked')
        self.save_context()

        LOG.debug('changing to next window')
        self.hide()
        self.next.emit()
        LOG.info('window changed to the next')

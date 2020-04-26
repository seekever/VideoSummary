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

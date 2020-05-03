""" The module for the objects options window."""

import logging
import os
import re

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog

from video_summary.context.objects_context import ObjectsContext
from video_summary.controller.threads_controller import ThreadsController
from video_summary.models.model_interface import ModelInterface

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(ROOT_DIR, '../templates/', 'ObjectsOptions.ui')

# Window
WINDOW_TITLE = "Objects options"

# Logger
LOGGER_NAME = 'App.Models.ObjectsOptions'
LOG = logging.getLogger(LOGGER_NAME)

# Default values
DEFAULT_OPTIMIZATION = True
DEFAULT_ANALYSIS = 2
DEFAULT_PERIODICITY = 1000
DEFAULT_OBJECT_LIST = []


class ObjectsOptions(QtWidgets.QMainWindow, ModelInterface):
    """
    The class for the objects options window.

    ...

    Methods
    -------
    add_object()
        add an object to the list of objects
    remove_object()
        remove an object from the list of objects
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        uic.loadUi(TEMPLATE_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)

        self.previousButton.clicked.connect(self.previous_window)
        self.nextButton.clicked.connect(self.next_window)
        self.addButton.clicked.connect(self.add_object)
        self.removeButton.clicked.connect(self.remove_object)
        self.optimizationBox.toggled.connect(self.reload_conditional_format)
        self.objectEdit.textChanged.connect(self.reload_conditional_format)

        ThreadsController.scenes_analysis_thread.progress.connect(
            self.update_scenes_analysis_progress_bar)

        self.update_scenes_analysis_progress_bar(0)

    def load_context(self):
        LOG.debug('loading context')
        with ObjectsContext(read_only=True) as manager:
            if manager.optimization is not None:
                self.optimizationBox.setChecked(manager.optimization)
            else:
                self.optimizationBox.setChecked(DEFAULT_OPTIMIZATION)

            self.analysisSlider.setValue(manager.scenes_periodicity or DEFAULT_ANALYSIS)
            self.periodicitySlider.setValue(manager.milliseconds_periodicity or DEFAULT_PERIODICITY)
            self.objectsView.clear()
            self.objectsView.addItems(list(set(manager.objects_list)) or DEFAULT_OBJECT_LIST)
        LOG.debug('context loaded')

    def save_context(self):
        LOG.debug('saving context')
        with ObjectsContext() as manager:
            manager.optimization = self.optimizationBox.isChecked()
            manager.scenes_periodicity = self.analysisSlider.value()
            manager.milliseconds_periodicity = self.periodicitySlider.value()

            if manager.objects_list is None:
                manager.objects_list = DEFAULT_OBJECT_LIST

            manager.objects_list.clear()
            manager.objects_list = list({self.objectsView.item(i).text()
                                         for i in range(self.objectsView.count())})
        LOG.debug('context saved')

    def reload_conditional_format(self):
        LOG.debug('reloading conditional format')
        self.analysisSlider.setVisible(self.optimizationBox.isChecked())
        self.periodicitySlider.setVisible(not self.optimizationBox.isChecked())

        word_input = self.objectEdit.text().strip()
        correct_input = bool(re.fullmatch("[a-z]+", word_input))
        duplicate_input = word_input in [self.objectsView.item(i).text()
                                         for i in range(self.objectsView.count())]

        self.addButton.setVisible(correct_input and not duplicate_input)
        self.removeButton.setVisible(self.objectsView.count() > 0)
        self.nextButton.setVisible(self.check_data())
        LOG.debug('conditional format reloaded')

    def check_data(self):
        LOG.debug('checking data')
        if self.objectsView.count() <= 0:
            LOG.info('incorrect data (objects list is empty)')
            return False
        LOG.info('checked data: OK')
        return True

    def add_object(self):
        """ Method that add an object to the list of objects."""
        LOG.debug('addButton clicked')
        self.objectsView.addItem(self.objectEdit.text().strip())
        self.objectEdit.clear()
        LOG.info('item %s added', self.objectEdit.text().strip())
        self.reload_conditional_format()

    def remove_object(self):
        """ Method that remove an object from the list of objects."""
        LOG.debug('removeButton clicked')
        item = self.objectsView.takeItem(self.objectsView.currentRow())
        LOG.info('item %s removed', item)
        self.reload_conditional_format()

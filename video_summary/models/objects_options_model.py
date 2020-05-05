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
    select_yolo_weights()
        ask the user to select the Yolo's weights path
    select_yolo_cfg()
        ask the user to select the Yolo's cfg path
    select_yolo_names()
        ask the user to select the Yolo's names path
    """

    yolo_weights_path = None
    yolo_cfg_path = None
    yolo_names_path = None

    def __init__(self, *args, **kwargs):
        LOG.debug('initializing objects options window model')
        super().__init__(*args, *kwargs)

        uic.loadUi(TEMPLATE_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)

        self.previousButton.clicked.connect(self.previous_window)
        self.nextButton.clicked.connect(self.next_window)
        self.addButton.clicked.connect(self.add_object)
        self.removeButton.clicked.connect(self.remove_object)
        self.optimizationBox.toggled.connect(self.reload_conditional_format)
        self.objectEdit.textChanged.connect(self.reload_conditional_format)
        self.selectYoloWeightsButton.clicked.connect(self.select_yolo_weights)
        self.selectYoloCfgButton.clicked.connect(self.select_yolo_cfg)
        self.selectYoloNamesButton.clicked.connect(self.select_yolo_names)

        ThreadsController.scenes_analysis_thread.progress.connect(
            self.update_scenes_analysis_progress_bar)

        self.update_scenes_analysis_progress_bar(0)
        LOG.info('objects options window model initialized')

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
            self.yolo_weights_path = manager.yolo_weights_path
            self.yolo_cfg_path = manager.yolo_cfg_path
            self.yolo_names_path = manager.yolo_names_path
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
            manager.yolo_weights_path = self.yolo_weights_path
            manager.yolo_cfg_path = self.yolo_cfg_path
            manager.yolo_names_path = self.yolo_names_path
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
        if self.yolo_weights_path == "":
            LOG.info('incorrect data (Yolo\'s weights is empty)')
            return False
        if self.yolo_weights_path is None:
            LOG.info('incorrect data (Yolo\'s weights is null)')
            return False
        if self.yolo_cfg_path == "":
            LOG.info('incorrect data (Yolo\'s cfg is empty)')
            return False
        if self.yolo_cfg_path is None:
            LOG.info('incorrect data (Yolo\'s cfg is null)')
            return False
        if self.yolo_names_path == "":
            LOG.info('incorrect data (Yolo\'s names is empty)')
            return False
        if self.yolo_names_path is None:
            LOG.info('incorrect data (Yolo\'s names is null)')
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

    def select_yolo_weights(self):
        """ Method that ask the user to select the Yolo's weights path."""
        LOG.debug('selectYoloWeightsButton clicked')

        LOG.debug('opening file dialog')
        self.yolo_weights_path = QFileDialog.getOpenFileName(
            self, 'Load file', '', "Weights file (*.weights)").__getitem__(0)
        LOG.debug('file dialog closed')

        self.reload_conditional_format()
        LOG.info('Yolo\'s weights path: %s', self.yolo_weights_path)

    def select_yolo_cfg(self):
        """ Method that ask the user to select the Yolo's cfg path."""
        LOG.debug('selectYoloCfgButton clicked')

        LOG.debug('opening file dialog')
        self.yolo_cfg_path = QFileDialog.getOpenFileName(
            self, 'Load file', '', "Cfg files (*.cfg)").__getitem__(0)
        LOG.debug('file dialog closed')

        self.reload_conditional_format()
        LOG.info('Yolo\'s cfg path: %s', self.yolo_cfg_path)

    def select_yolo_names(self):
        """ Method that ask the user to select the Yolo's names path."""
        LOG.debug('selectYoloNamesButton clicked')

        LOG.debug('opening file dialog')
        self.yolo_names_path = QFileDialog.getOpenFileName(
            self, 'Load file', '', "Names files (*.names)").__getitem__(0)
        LOG.debug('file dialog closed')

        self.reload_conditional_format()
        LOG.info('Yolo\'s names path: %s', self.yolo_names_path)

    def next_window(self):
        super().next_window()
        if ThreadsController.objects_analysis_thread.isRunning():
            LOG.info('restarting objects analysis thread')
            ThreadsController.objects_analysis_thread.restart_thread()
        else:
            LOG.info('starting objects analysis thread')
            ThreadsController.objects_analysis_thread.start()

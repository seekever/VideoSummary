"""The context which manages the scenes configurations"""

import json
import logging
import os

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'ScenesConfig.conf')

# Strings for JSON
SCENES_LIST = "scenesList"

# Logger
LOGGER_NAME = 'App.Context.Scenes'
LOG = logging.getLogger(LOGGER_NAME)


class ScenesContext:
    """
    A class used to represent the video scene context

    ...

    Attributes
    ----------
    read_only : bool
        a boolean to activate the read only mode
    config : dict
        a dict with all the general settings
    scenes_list : list [int, int]
        a list with int tuples (initialTime, endTime)

    """

    def __init__(self, read_only=False):
        LOG.debug('starting scenes context')
        self.read_only = read_only
        self.config = None
        self.scenes_list = None
        LOG.debug('scenes context started')

    def __enter__(self):
        try:
            LOG.debug('reading scenes context')
            with open(CONFIG_PATH, 'r') as json_file:
                json_string = json_file.read()
                self.config = json.loads(json_string)
                LOG.info('scenes context read from %s', CONFIG_PATH)
        except FileNotFoundError:
            LOG.debug('scenes context not found')
            LOG.debug('creating scenes context')
            self.config = {}
            LOG.debug('scenes context created')

        LOG.debug('loading scenes context')
        self.scenes_list = self.config.get(SCENES_LIST)
        LOG.debug('scenes context loaded')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.read_only:
            LOG.debug('saving scenes context')
            self.config[SCENES_LIST] = self.scenes_list
            LOG.debug('scenes context saved')

            LOG.debug('writing scenes context')
            json_string = json.dumps(self.config, indent=4)

            with open(CONFIG_PATH, 'w') as json_file:
                json_file.write(json_string)
            json_file.close()
            LOG.info('scenes context written at %s', CONFIG_PATH)

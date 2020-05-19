"""The context which manages the scenes configurations"""

import json
import logging
import os

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + '/conf/'
CONFIG_PATH = os.path.join(ROOT_DIR, 'ScenesConfig.conf')
CONFIG_PATH_DEFAULT = os.path.join(ROOT_DIR, 'ScenesConfigDefault.conf')
CONFIG_PATH_TEST = os.path.join(ROOT_DIR, 'ScenesConfigTest.conf')

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
    test : bool
        a boolean to activate the testing mode
    config : dict
        a dict with all the general settings
    scenes_list : list [int, int]
        a list with int tuples (initialTime, endTime)
    path : string
        the path for the configuration file

    """

    def __init__(self, read_only=False, test=False):
        LOG.debug('starting scenes context')
        self.read_only = read_only
        self.config = None
        self.scenes_list = None
        if test:
            self.path = CONFIG_PATH_TEST
        else:
            self.path = CONFIG_PATH
        LOG.debug('scenes context started')

    def __enter__(self):
        try:
            LOG.debug('reading scenes context')
            with open(self.path, 'r') as json_file:
                json_string = json_file.read()
                self.config = json.loads(json_string)
                LOG.info('scenes context read from %s', self.path)
        except FileNotFoundError:
            LOG.debug('scenes context not found')
            LOG.debug('reading default scenes context')
            try:
                with open(CONFIG_PATH_DEFAULT, 'r') as json_file:
                    json_string = json_file.read()
                    self.config = json.loads(json_string)
            except FileNotFoundError:
                LOG.error('default scenes context not found')
                raise FileNotFoundError('{} not found'.format(CONFIG_PATH_DEFAULT))
            LOG.debug('default scenes context read')

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

            with open(self.path, 'w') as json_file:
                json_file.write(json_string)
            json_file.close()
            LOG.info('scenes context written at %s', self.path)

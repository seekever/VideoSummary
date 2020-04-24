"""The context which manages the objects configurations."""

import json
import logging
import os

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'ObjectsConfig.conf')

# Strings for JSON
OBJECTS_DICT = "objectsDict"
OBJECTS_LIST = "objectsList"
OPTIMIZATION = "optimization"
MILLISECONDS_PERIODICITY = "millisecondsPeriodicity"
SCENES_PERIODICITY = "scenesPeriodicity"

# Logger
LOGGER_NAME = 'App.Context.Objects'
LOG = logging.getLogger(LOGGER_NAME)


class ObjectsContext:
    """
    A class used to represent the objects context.

    ...

    Attributes
    ----------
    config : dict
        a dict with all the general settings
    objects_dict : dict
        a dict with all the objects appearances times in milliseconds
    objects_list : list
        a string list with objects to search
    optimization : bool
        a boolean to activate the scene optimization
    milliseconds_periodicity : int
        the analysis periodicity in milliseconds
    scenes_periodicity : int
        the number of analysis per scene

    """

    def __init__(self):
        LOG.debug('starting objects context')
        self.config = None
        self.objects_dict = None
        self.objects_list = None
        self.optimization = None
        self.milliseconds_periodicity = None
        self.scenes_periodicity = None
        LOG.debug('objects context started')

    def __enter__(self):
        try:
            LOG.debug('reading objects context')
            with open(CONFIG_PATH, 'r') as json_file:
                json_string = json_file.read()
                self.config = json.loads(json_string)
                LOG.info('objects context read from %s', CONFIG_PATH)
        except FileNotFoundError:
            LOG.debug('objects context not found')
            LOG.debug('creating objects context')
            self.config = {}
            LOG.debug('objects context created')

        LOG.debug('loading objects context')
        self.objects_dict = self.config.get(OBJECTS_DICT)
        self.objects_list = self.config.get(OBJECTS_LIST)
        self.optimization = self.config.get(OPTIMIZATION)
        self.milliseconds_periodicity = self.config.get(MILLISECONDS_PERIODICITY)
        self.scenes_periodicity = self.config.get(SCENES_PERIODICITY)
        LOG.debug('objects context loaded')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        LOG.debug('saving objects context')
        self.config[OBJECTS_DICT] = self.objects_dict
        self.config[OBJECTS_LIST] = self.objects_list
        self.config[OPTIMIZATION] = self.optimization
        self.config[MILLISECONDS_PERIODICITY] = self.milliseconds_periodicity
        self.config[SCENES_PERIODICITY] = self.scenes_periodicity
        LOG.debug('objects context saved')

        LOG.debug('writing objects context')
        json_string = json.dumps(self.config, indent=4)

        with open(CONFIG_PATH, 'w') as json_file:
            json_file.write(json_string)

        json_file.close()
        LOG.info('objects context written at %s', CONFIG_PATH)

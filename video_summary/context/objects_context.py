"""The context which manages the objects configurations."""

import json
import logging
import os

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + '/conf/'
CONFIG_PATH = os.path.join(ROOT_DIR, 'ObjectsConfig.conf')
CONFIG_PATH_DEFAULT = os.path.join(ROOT_DIR, 'ObjectsConfigDefault.conf')
CONFIG_PATH_TEST = os.path.join(ROOT_DIR, 'ObjectsConfigTest.conf')

# Strings for JSON
OBJECTS_DICT = "objectsDict"
OBJECTS_LIST = "objectsList"
OPTIMIZATION = "optimization"
MILLISECONDS_PERIODICITY = "millisecondsPeriodicity"
SCENES_PERIODICITY = "scenesPeriodicity"
YOLO_WEIGHTS_PATH = "yoloWeightsPath"
YOLO_CFG_PATH = "yoloCfgPath"
YOLO_NAMES_PATH = "yoloNamesPath"

# Logger
LOGGER_NAME = 'App.Context.Objects'
LOG = logging.getLogger(LOGGER_NAME)


class ObjectsContext:
    """
    A class used to represent the objects context.

    ...

    Attributes
    ----------
    read_only : bool
        a boolean to activate the read only mode
    test : bool
        a boolean to activate the testing mode
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
    yolo_weights_path : str
        the Yolo's weights path
    yolo_cfg_path : str
        the Yolo's cfg path
    yolo_names_path : str
        the Yolo's names path
    path : string
        the path for the configuration file

    """

    def __init__(self, read_only=False, test=False):
        LOG.debug('starting objects context')
        self.read_only = read_only
        self.config = None
        self.objects_dict = None
        self.objects_list = None
        self.optimization = None
        self.milliseconds_periodicity = None
        self.scenes_periodicity = None
        self.yolo_weights_path = None
        self.yolo_cfg_path = None
        self.yolo_names_path = None
        if test:
            self.path = CONFIG_PATH_TEST
        else:
            self.path = CONFIG_PATH
        LOG.debug('objects context started')

    def __enter__(self):
        try:
            LOG.debug('reading objects context')
            with open(self.path, 'r') as json_file:
                json_string = json_file.read()
                self.config = json.loads(json_string)
                LOG.info('objects context read from %s', self.path)
        except FileNotFoundError:
            LOG.debug('objects context not found')
            LOG.debug('reading default objects context')
            try:
                with open(CONFIG_PATH_DEFAULT, 'r') as json_file:
                    json_string = json_file.read()
                    self.config = json.loads(json_string)
            except FileNotFoundError:
                LOG.error('default objects context not found')
                raise FileNotFoundError('{} not found'.format(CONFIG_PATH_DEFAULT))
            LOG.debug('default objects objects read')

        LOG.debug('loading objects context')
        self.objects_dict = self.config.get(OBJECTS_DICT)
        self.objects_list = self.config.get(OBJECTS_LIST)
        self.optimization = self.config.get(OPTIMIZATION)
        self.milliseconds_periodicity = self.config.get(MILLISECONDS_PERIODICITY)
        self.scenes_periodicity = self.config.get(SCENES_PERIODICITY)
        self.yolo_weights_path = self.config.get(YOLO_WEIGHTS_PATH)
        self.yolo_cfg_path = self.config.get(YOLO_CFG_PATH)
        self.yolo_names_path = self.config.get(YOLO_NAMES_PATH)
        LOG.debug('objects context loaded')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.read_only:
            LOG.debug('saving objects context')
            self.config[OBJECTS_DICT] = self.objects_dict
            self.config[OBJECTS_LIST] = self.objects_list
            self.config[OPTIMIZATION] = self.optimization
            self.config[MILLISECONDS_PERIODICITY] = self.milliseconds_periodicity
            self.config[SCENES_PERIODICITY] = self.scenes_periodicity
            self.config[YOLO_WEIGHTS_PATH] = self.yolo_weights_path
            self.config[YOLO_CFG_PATH] = self.yolo_cfg_path
            self.config[YOLO_NAMES_PATH] = self.yolo_names_path
            LOG.debug('objects context saved')

            LOG.debug('writing objects context')
            json_string = json.dumps(self.config, indent=4)

            with open(self.path, 'w') as json_file:
                json_file.write(json_string)

            json_file.close()
            LOG.info('objects context written at %s', self.path)

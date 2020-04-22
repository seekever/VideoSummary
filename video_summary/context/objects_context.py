"""The context which manages the objects configurations."""

import json
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
        self.config = None
        self.objects_dict = None
        self.objects_list = None
        self.optimization = None
        self.milliseconds_periodicity = None
        self.scenes_periodicity = None

    def __enter__(self):
        try:
            with open(CONFIG_PATH, 'r') as json_file:
                json_string = json_file.read()
                self.config = json.loads(json_string)
        except FileNotFoundError:
            self.config = {}

        self.objects_dict = self.config.get(OBJECTS_DICT)
        self.objects_list = self.config.get(OBJECTS_LIST)
        self.optimization = self.config.get(OPTIMIZATION)
        self.milliseconds_periodicity = self.config.get(MILLISECONDS_PERIODICITY)
        self.scenes_periodicity = self.config.get(SCENES_PERIODICITY)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.config[OBJECTS_DICT] = self.objects_dict
        self.config[OBJECTS_LIST] = self.objects_list
        self.config[OPTIMIZATION] = self.optimization
        self.config[MILLISECONDS_PERIODICITY] = self.milliseconds_periodicity
        self.config[SCENES_PERIODICITY] = self.scenes_periodicity

        json_string = json.dumps(self.config, indent=4)

        with open(CONFIG_PATH, 'w') as json_file:
            json_file.write(json_string)

        json_file.close()

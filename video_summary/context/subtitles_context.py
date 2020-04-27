"""The context which manages the subtitles configurations."""
import json
import logging
import os
from enum import Enum

from video_summary.objects.subtitle import from_dict_list, to_dict_list

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'SubtitlesConfig.conf')

# Strings for JSON
SUBTITLES_PATH = "subtitlesPath"
SUBTITLES_LIST = "subtitlesList"
RESUME_PERCENTAGE = "resumePercentage"
VECTORING_TYPE = "vectoringType"
REMOVE_PUNCTUATION = "removePunctuation"
PUNCTUATION_SIGNS = "punctuationSigns"
REMOVE_STOP_WORDS = "removeStopWords"
REMOVE_CAPITAL_LETTERS = "removeCapitalLetters"
REMOVE_ACCENTS = "removeAccents"
LANGUAGE = "language"

# Logger
LOGGER_NAME = 'App.Context.Subtitles'
LOG = logging.getLogger(LOGGER_NAME)


# Parametrization
class VectoringType(int, Enum):
    """ Parametrization for the vectoring type."""
    COUNTERS = 0
    BINARIES_COUNTERS = 1
    N_GRAM_COUNTERS = 2
    TF_WITH_NORMALIZATION_L1 = 3
    TF_WITH_NORMALIZATION_L2 = 4
    TF_IDF = 5
    TF_IDF_WITH_SMOOTHING_IDF = 6
    TF_IDF_WITH_SMOOTHING_IDF_AND_NORMALIZATION_L1 = 7
    TF_IDF_WITH_SMOOTHING_IDF_AND_NORMALIZATION_L2 = 8


class Languages(int, Enum):
    """ Parametrization for the vectoring type."""
    ARABIC = 0
    AZERBAIJANI = 1
    DANISH = 2
    DUTCH = 3
    ENGLISH = 4
    FINNISH = 5
    FRENCH = 6
    GERMAN = 7
    GREEK = 8
    HUNGARIAN = 9
    INDONESIAN = 10
    ITALIAN = 11
    KAZAKH = 12
    NEPALI = 13
    NORWEGIAN = 14
    PORTUGUESE = 15
    ROMANIAN = 16
    RUSSIAN = 17
    SPANISH = 18
    SWEDISH = 19
    TURKISH = 20


class SubtitlesContext:
    """
    A class used to represent the video subtitles context.

    ...

    Attributes
    ----------
    read_only : bool
        a boolean to activate the read only mode
    config : dict
        a dict with all the general settings
    subtitles_path : str
        the subtitles path
    subtitles_list : list
        a list of Subtitles objects
    resume_percentage : float
        the resume percentage of the subtitles (0.0 - 1.0)
    vectoring_type : int
        the vectoring type (class VectoringType)
    remove_punctuation : bool
        a boolean to activate the punctuation remove
    punctuation_signs : list
        a char list with all the punctuation signs to remove
    remove_stop_words : bool
        a boolean to activate the stop words remove
    remove_capital_letters : bool
        a boolean to activate the capital letters remove
    remove_accents : bool
        a boolean to activate the accents remove
    language : int
         the subtitles language (class Language)

    """

    def __init__(self, read_only=False):
        LOG.debug('starting subtitles context')
        self.read_only = read_only
        self.config = None
        self.subtitles_path = None
        self.subtitles_list = None
        self.resume_percentage = None
        self.vectoring_type = None
        self.remove_punctuation = None
        self.punctuation_signs = None
        self.remove_stop_words = None
        self.remove_capital_letters = None
        self.remove_accents = None
        self.language = None
        LOG.debug('subtitles context started')

    def __enter__(self):
        try:
            LOG.debug('reading subtitles context')
            with open(CONFIG_PATH, 'r') as json_file:
                json_string = json_file.read()
                self.config = json.loads(json_string)
                LOG.info('subtitles context read from %s', CONFIG_PATH)
        except FileNotFoundError:
            LOG.debug('subtitles context not found')
            LOG.debug('creating subtitles context')
            self.config = {}
            LOG.debug('subtitles context created')

        LOG.debug('loading subtitles context')
        self.subtitles_path = self.config.get(SUBTITLES_PATH)
        self.subtitles_list = from_dict_list(self.config.get(SUBTITLES_LIST))
        self.resume_percentage = self.config.get(RESUME_PERCENTAGE)
        self.vectoring_type = self.config.get(VECTORING_TYPE)
        self.remove_punctuation = self.config.get(REMOVE_PUNCTUATION)
        self.punctuation_signs = self.config.get(PUNCTUATION_SIGNS)
        self.remove_stop_words = self.config.get(REMOVE_STOP_WORDS)
        self.remove_capital_letters = self.config.get(REMOVE_CAPITAL_LETTERS)
        self.remove_accents = self.config.get(REMOVE_ACCENTS)
        self.language = self.config.get(LANGUAGE)
        LOG.debug('subtitles context loaded')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.read_only:
            LOG.debug('saving subtitles context')
            self.config[SUBTITLES_PATH] = self.subtitles_path
            self.config[SUBTITLES_LIST] = to_dict_list(self.subtitles_list)
            self.config[RESUME_PERCENTAGE] = self.resume_percentage
            self.config[VECTORING_TYPE] = self.vectoring_type
            self.config[REMOVE_PUNCTUATION] = self.remove_punctuation
            self.config[PUNCTUATION_SIGNS] = self.punctuation_signs
            self.config[REMOVE_STOP_WORDS] = self.remove_stop_words
            self.config[REMOVE_CAPITAL_LETTERS] = self.remove_capital_letters
            self.config[REMOVE_ACCENTS] = self.remove_accents
            self.config[LANGUAGE] = self.language
            LOG.debug('subtitles context saved')

            LOG.debug('writing subtitles context')
            json_string = json.dumps(self.config, indent=4)

            with open(CONFIG_PATH, 'w') as json_file:
                json_file.write(json_string)

            json_file.close()
            LOG.info('subtitles context written at %s', CONFIG_PATH)

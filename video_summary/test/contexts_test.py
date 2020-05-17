"""Unit tests that test that contexts work."""

import logging
import sys
import unittest

from video_summary.context.general_context import GeneralContext, ResumeMode
from video_summary.context.objects_context import ObjectsContext
from video_summary.context.scenes_context import ScenesContext
from video_summary.context.subtitles_context import SubtitlesContext, VectoringType, Languages
from video_summary.objects.subtitle import Subtitle

# Logger
LOGGER_NAME = 'Test.Context'
LOGGER_FILENAME = 'ContextTest.log'
LOGGER_LEVEL = logging.DEBUG
LOGGER_FORMAT = '%(asctime)s %(threadName)s %(levelname)-8s %(module)s: %(message)s'
LOGGER_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(filename=LOGGER_FILENAME, level=LOGGER_LEVEL,
                    format=LOGGER_FORMAT, datefmt=LOGGER_DATE_FORMAT)

LOG = logging.getLogger(LOGGER_NAME)
SH = logging.StreamHandler(sys.stdout)
SH.setFormatter(logging.Formatter(LOGGER_FORMAT))
LOG.addHandler(SH)

# Test constants
SUBTITLES_PATH_TEST = "subtitles/path.srt"


class ContextTest(unittest.TestCase):
    """Class with all the context test methods."""

    def test_general_context(self):
        """Unit test that test that general context works."""
        LOG.info('starting general context test')
        with GeneralContext() as manager:
            manager.original_video_path = "test/path.mp4"
            manager.final_video_path = "test/final"
            manager.resume_mode = ResumeMode.SUBTITLES
            manager.detect_scenes = True
            manager.scenes_difference = 0.3
            manager.resume_times = None

        with GeneralContext() as manager:
            self.assertEqual("test/path.mp4", manager.original_video_path)
            self.assertEqual("test/final", manager.final_video_path)
            self.assertEqual(ResumeMode.SUBTITLES, manager.resume_mode)
            self.assertTrue(manager.detect_scenes)
            self.assertEqual(0.3, manager.scenes_difference)
            self.assertIsNone(manager.resume_times)

            manager.original_video_path = None
            manager.final_video_path += "/video.mp4"
            manager.resume_mode = ResumeMode.OBJECTS
            manager.detect_scenes = False
            manager.scenes_difference -= 0.05
            manager.resume_times = [[1, 4], [6, 14], [20, 25]]

        with GeneralContext() as manager:
            self.assertIsNone(manager.original_video_path)
            self.assertEqual("test/final/video.mp4", manager.final_video_path)
            self.assertEqual(ResumeMode.OBJECTS, manager.resume_mode)
            self.assertFalse(manager.detect_scenes)
            self.assertEqual(0.25, manager.scenes_difference)
            self.assertEqual([6, 14], manager.resume_times[1])
        LOG.info('ending general context test')

    def test_scenes_context(self):
        """Unit test that test that scenes context works."""
        LOG.info('starting scenes context test')
        with ScenesContext() as manager:
            manager.scenes_list = [[0, 10], [11, 25], [26, 45]]

        with ScenesContext() as manager:
            self.assertEqual([11, 25], manager.scenes_list[1])

            manager.scenes_list[1] = [13, 24]
            manager.scenes_list.append([46, 60])

        with ScenesContext() as manager:
            self.assertEqual([13, 24], manager.scenes_list[1])
            self.assertEqual([46, 60], manager.scenes_list[3])
        LOG.info('ending scenes context test')

    def test_objects_context(self):
        """Unit test that test that objects context works."""
        LOG.info('starting objects context test')
        with ObjectsContext() as manager:
            manager.objects_dict = {"dog": [10, 23, 45], "cat": [5, 41]}
            manager.objects_list = ['dog', 'cat', 'car']
            manager.optimization = False
            manager.milliseconds_periodicity = 200
            manager.scenes_periodicity = 3
            manager.yolo_weights_path = "yolo/path"
            manager.yolo_cfg_path = None
            manager.yolo_names_path = ""

        with ObjectsContext() as manager:
            self.assertEqual([5, 41], manager.objects_dict["cat"])
            self.assertEqual('car', manager.objects_list[2])
            self.assertFalse(manager.optimization)
            self.assertEqual(200, manager.milliseconds_periodicity)
            self.assertEqual(3, manager.scenes_periodicity)
            self.assertEqual("yolo/path", manager.yolo_weights_path)
            self.assertIsNone(manager.yolo_cfg_path)
            self.assertEqual("", manager.yolo_names_path)

            manager.objects_dict["dog"].remove(23)
            manager.objects_dict["tree"] = [7, 33]
            manager.objects_dict["tree"].append(45)
            manager.objects_list[2] = 'tree'
            manager.objects_list.append('house')
            manager.optimization = True
            manager.milliseconds_periodicity += 100
            manager.scenes_periodicity -= 1
            manager.yolo_weights_path += "/test/weights"
            manager.yolo_cfg_path = "/test/cfg"
            manager.yolo_names_path += "/test/names"

        with ObjectsContext() as manager:
            self.assertEqual([10, 45], manager.objects_dict["dog"])
            self.assertEqual([7, 33, 45], manager.objects_dict["tree"])
            self.assertEqual('tree', manager.objects_list[2])
            self.assertEqual('house', manager.objects_list[3])
            self.assertTrue(manager.optimization)
            self.assertEqual(300, manager.milliseconds_periodicity)
            self.assertEqual(2, manager.scenes_periodicity)
            self.assertEqual("yolo/path/test/weights", manager.yolo_weights_path)
            self.assertEqual("/test/cfg", manager.yolo_cfg_path)
            self.assertEqual("/test/names", manager.yolo_names_path)
        LOG.info('ending objects context test')

    def test_subtitles_context(self):
        """Unit test that test that subtitles context works."""
        LOG.info('starting subtitles context test')
        with SubtitlesContext() as manager:
            manager.subtitles_path = None
            manager.subtitles_list = [Subtitle("The first subtitle", 12, 34, None),
                                      Subtitle("The second subtitle", 24, 56, 10)]
            manager.resume_percentage = 0.4
            manager.vectoring_type = VectoringType.N_GRAM_COUNTERS
            manager.remove_punctuation = None
            manager.punctuation_signs = ['¡', '!', '"', '#', '.', ';', ':']
            manager.remove_stop_words = True
            manager.remove_capital_letters = True
            manager.remove_accents = False
            manager.language = Languages.FINNISH

        with SubtitlesContext() as manager:
            self.assertEqual("The first subtitle", manager.subtitles_list[0].text)
            self.assertIsNone(manager.subtitles_list[0].score)
            self.assertEqual(24, manager.subtitles_list[1].start)
            self.assertEqual(0.4, manager.resume_percentage)
            self.assertEqual(VectoringType.N_GRAM_COUNTERS, manager.vectoring_type)
            self.assertIsNone(manager.remove_punctuation)
            self.assertEqual('#', manager.punctuation_signs[3])
            self.assertTrue(manager.remove_stop_words)
            self.assertTrue(manager.remove_capital_letters)
            self.assertFalse(manager.remove_accents)
            self.assertEqual(Languages.FINNISH, manager.language)

            manager.subtitles_path = SUBTITLES_PATH_TEST
            manager.subtitles_list[1].score = 8
            manager.subtitles_list.pop(0)
            manager.subtitles_list.append(Subtitle("The thirst subtitle", 55, 70, None))
            manager.resume_percentage += 0.15
            manager.vectoring_type = VectoringType.BINARIES_COUNTERS
            manager.remove_punctuation = True
            manager.punctuation_signs.remove('#')
            manager.punctuation_signs += ['(', ')']
            manager.remove_capital_letters = None
            manager.language = Languages.SPANISH

        with SubtitlesContext() as manager:
            self.assertEqual(SUBTITLES_PATH_TEST, manager.subtitles_path)
            self.assertEqual(manager.subtitles_list[0].score, 8)
            self.assertEqual("The thirst subtitle", manager.subtitles_list[1].text)
            self.assertEqual(0.55, manager.resume_percentage)
            self.assertEqual(VectoringType.BINARIES_COUNTERS, manager.vectoring_type)
            self.assertTrue(manager.remove_punctuation)
            self.assertNotEqual('#', manager.punctuation_signs[3])
            self.assertEqual('(', manager.punctuation_signs[6])
            self.assertEqual(')', manager.punctuation_signs[7])
            self.assertFalse(manager.remove_capital_letters)
            self.assertFalse(manager.remove_accents)
            self.assertEqual(Languages.SPANISH, manager.language)
        LOG.info('ending subtitles context test')

    def test_read_only(self):
        """Unit test that test that the read_only mode works."""

        # General context
        with GeneralContext() as manager:
            manager.detect_scenes = True

        with GeneralContext(read_only=True) as manager:
            self.assertTrue(manager.detect_scenes)
            manager.detect_scenes = False

        with GeneralContext() as manager:
            self.assertTrue(manager.detect_scenes)

        # Scenes context
        with ScenesContext() as manager:
            manager.scenes_list = [[0, 10], [11, 25], [26, 45]]

        with ScenesContext(read_only=True) as manager:
            self.assertEqual([[0, 10], [11, 25], [26, 45]], manager.scenes_list)
            manager.scenes_list = [[5, 14], [30, 36]]

        with ScenesContext() as manager:
            self.assertEqual([[0, 10], [11, 25], [26, 45]], manager.scenes_list)

        # Objects context
        with ObjectsContext() as manager:
            manager.objects_dict = {"dog": [10, 23, 45], "cat": [5, 41]}

        with ObjectsContext(read_only=True) as manager:
            self.assertEqual([5, 41], manager.objects_dict["cat"])
            manager.objects_dict["dog"].remove(23)

        with ObjectsContext() as manager:
            self.assertEqual([10, 23, 45], manager.objects_dict["dog"])

        # Subtitles context
        with SubtitlesContext() as manager:
            manager.subtitles_path = SUBTITLES_PATH_TEST

        with SubtitlesContext(read_only=True) as manager:
            self.assertEqual(SUBTITLES_PATH_TEST, manager.subtitles_path)
            manager.subtitles_path = "subtitles/second/path.srt"

        with SubtitlesContext() as manager:
            self.assertEqual(SUBTITLES_PATH_TEST, manager.subtitles_path)


if __name__ == '__main__':
    unittest.main()

"""Unit tests that test that contexts work."""

import unittest

from video_summary.context.general_context import GeneralContext, ResumeMode
from video_summary.context.scenes_context import ScenesContext


class GeneralContextTest(unittest.TestCase):
    """Class with all the context test methods."""

    def test_general_context(self):
        """Unit test that test that general context works."""
        with GeneralContext() as manager:
            manager.resume_mode = ResumeMode.SUBTITLES
            manager.detect_scenes = True

        with GeneralContext() as manager:
            self.assertEqual(ResumeMode.SUBTITLES, manager.resume_mode)
            self.assertTrue(manager.detect_scenes)

            manager.resume_mode = ResumeMode.OBJECTS
            manager.detect_scenes = False

        with GeneralContext() as manager:
            self.assertEqual(ResumeMode.OBJECTS, manager.resume_mode)
            self.assertFalse(manager.detect_scenes)

    def test_scenes_context(self):
        """Unit test that test that scenes context works."""
        with ScenesContext() as manager:
            manager.scenes_list = [[0, 10], [11, 25], [26, 45]]

        with ScenesContext() as manager:
            self.assertEqual([11, 25], manager.scenes_list[1])

            manager.scenes_list[1] = [13, 24]
            manager.scenes_list.append([46, 60])

        with ScenesContext() as manager:
            self.assertEqual([13, 24], manager.scenes_list[1])
            self.assertEqual([46, 60], manager.scenes_list[3])


if __name__ == '__main__':
    unittest.main()

"""Unit tests that test that contexts work."""
import unittest

from video_summary.context.general_context import GeneralContext, ResumeMode


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


if __name__ == '__main__':
    unittest.main()

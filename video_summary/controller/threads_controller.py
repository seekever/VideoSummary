"""Module poor the threads controller."""

from video_summary.threads.scenes_analysis_thread import ScenesAnalysis


class ThreadsController:
    """The class for the threads controller."""

    # Threads
    scenes_analysis_thread = ScenesAnalysis()

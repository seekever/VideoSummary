"""Module poor the threads controller."""

from video_summary.threads.objects_analysis_thread import ObjectsAnalysis
from video_summary.threads.scenes_analysis_thread import ScenesAnalysis
from video_summary.threads.subtitles_analysis_thread import SubtitlesAnalysis


class ThreadsController:
    """The class for the threads controller."""

    # Threads
    scenes_analysis_thread = ScenesAnalysis()
    objects_analysis_thread = ObjectsAnalysis(scenes_analysis_thread)
    subtitles_analysis_thread = SubtitlesAnalysis()

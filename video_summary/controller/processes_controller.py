"""Module for the processes controller."""

from video_summary.processes.objects_analysis_process import ObjectsAnalysis
from video_summary.processes.resume_video_process import Resume
from video_summary.processes.save_video_process import SaveVideo
from video_summary.processes.scenes_analysis_process import ScenesAnalysis
from video_summary.processes.subtitles_analysis_process import SubtitlesAnalysis


class ProcessesController:
    """The class for the processes controller."""

    # Processes
    scenes_analysis_process = ScenesAnalysis()
    objects_analysis_process = ObjectsAnalysis(scenes_analysis_process)
    subtitles_analysis_process = SubtitlesAnalysis()
    resume_process = Resume(scenes_analysis_process, objects_analysis_process,
                            subtitles_analysis_process)
    save_video_process = SaveVideo(scenes_analysis_process, objects_analysis_process,
                                   subtitles_analysis_process, resume_process)

from __future__ import absolute_import, unicode_literals
from celery import shared_task
import os
from pathlib import Path
from django.core.cache import cache
from celery.utils.log import get_task_logger
from datetime import timedelta

from endoreg_db.models.data_file.import_classes.raw_video import RawVideoFile
from endoreg_db.models.data_file.import_classes.processing_functions import (
    get_multilabel_model, get_multilabel_classifier
)

LOCK_EXPIRE = 60 * 60 * 24  # Lock expires in 24 h
logger = get_task_logger(__name__)


# import FRAME_DIR_PARENT from settings
from django.conf import settings

FRAME_DIR_PARENT = settings.TMP_IMPORT_FRAME_DIR_PARENT
RAW_VIDEO_DIR_PARENT = settings.RAW_VIDEO_DIR_PARENT
PREDICTION_DIR_PARENT = settings.PREDICTION_DIR_PARENT

MULTILABEL_MODEL_PATH = settings.MULTILABEL_MODEL_PATH
PREDICTION_SMOOTHING_WINDOW_SIZE_S = settings.PREDICTION_SMOOTHING_WINDOW_SIZE_S
PREDICTION_MIN_SEQUENCE_LENGTH_S = settings.PREDICTION_MIN_SEQUENCE_LENGTH_S



@shared_task()
def move_files(
    center_name = "university_hospital_wuerzburg",
    processor_name = "olympus_cv_1500",
    source_directory = "/mnt/hdd-sensitive/DropOff/data",
    destination_directory = "/mnt/hdd-sensitive/Pseudo/data"
    ):
    """Move files from one directory to another."""
    for filename in os.listdir(source_directory):
        source_path = Path(os.path.join(source_directory, filename))

        video = RawVideoFile.create_from_file(
            file_path = source_path,
            center_name = center_name,
            processor_name = processor_name,
            frame_dir_parent = FRAME_DIR_PARENT,
            video_dir_parent = RAW_VIDEO_DIR_PARENT,
            save = True
        )


from endoreg_db.models.data_file.import_classes.processing_functions import (
    extract_frames_from_videos,
    videos_scheduled_for_ocr_preflight, perform_ocr_on_videos,
    videos_scheduled_for_initial_prediction_preflight, perform_initial_prediction_on_videos,
    videos_scheduled_for_prediction_import_preflight, import_predictions_for_videos,
    delete_frames_preflight, delete_frames
)

@shared_task()
def extract_frames():
    """Extract frames from video files."""
    extract_frames_from_videos()

@shared_task()
def video_ocr_preflight():
    """OCR preflight."""
    videos_scheduled_for_ocr_preflight()

@shared_task()
def video_ocr():
    """Perform OCR on video files."""
    perform_ocr_on_videos()

@shared_task()
def video_initial_prediction_preflight():
    """Initial prediction preflight."""
    videos_scheduled_for_initial_prediction_preflight()

@shared_task()
def video_initial_prediction():
    """Perform initial prediction on video files."""
    perform_initial_prediction_on_videos(
        MULTILABEL_MODEL_PATH,
        window_size_s = PREDICTION_SMOOTHING_WINDOW_SIZE_S,
        min_seq_len_s = PREDICTION_MIN_SEQUENCE_LENGTH_S,
    )
 

@shared_task()
def video_prediction_import_preflight():
    """Prediction import preflight."""
    videos_scheduled_for_prediction_import_preflight()

@shared_task()
def video_prediction_import():
    """Import predictions for video files."""
    import_predictions_for_videos()

@shared_task()
def delete_frames_preflight():
    """Delete frames preflight."""
    delete_frames_preflight()

@shared_task()
def delete_frames():
    """Delete frames."""
    delete_frames()

@shared_task()
def retrieve_sensitive_video_data():
    """Retrieve sensitive video data."""
    for video in RawVideoFile.objects.filter(
        state_frames_extracted=True,
        sensitive_meta__isnull=True
    ):
        video.update_text_metadata()

# @shared_task()
# def create_video_meta():
#     """Create Video Meta"""
#     for video in RawVideoFile.objects.filter(
#         video_meta__isnull=True
#     ):
#         video.update_video_meta()
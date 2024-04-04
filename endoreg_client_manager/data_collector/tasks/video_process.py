from celery import shared_task

from endoreg_db.models import RawVideoFile

from .common import (
    MULTILABEL_MODEL_PATH,
    PREDICTION_SMOOTHING_WINDOW_SIZE_S,
    PREDICTION_MIN_SEQUENCE_LENGTH_S
)

from endoreg_db.models.data_file.import_classes.processing_functions import (
    extract_frames_from_videos,
    videos_scheduled_for_ocr_preflight, perform_ocr_on_videos,
    videos_scheduled_for_initial_prediction_preflight, perform_initial_prediction_on_videos,
    videos_scheduled_for_prediction_import_preflight, import_predictions_for_videos,
    delete_frames_preflight, delete_frames
)

from .common import single_instance_task, LOCK_EXPIRE

@shared_task(bind=True)
@single_instance_task(lock_expire = LOCK_EXPIRE)
def task_extract_frames(self):
    """Extract frames from video files."""
    extract_frames_from_videos()

@shared_task(bind=True)
@single_instance_task(lock_expire = LOCK_EXPIRE)
def task_video_ocr_preflight(self):
    """OCR preflight."""
    videos_scheduled_for_ocr_preflight()

@shared_task(bind=True)
@single_instance_task(lock_expire = LOCK_EXPIRE)
def task_video_ocr(self):
    """Perform OCR on video files."""
    perform_ocr_on_videos()

@shared_task(bind=True)
@single_instance_task(lock_expire = LOCK_EXPIRE)
def task_video_initial_prediction_preflight(self):
    """Initial prediction preflight."""
    videos_scheduled_for_initial_prediction_preflight()

# get celery logger
from celery.utils.log import get_task_logger
import torch
logger = get_task_logger(__name__)

@shared_task(bind=True)
@single_instance_task(lock_expire = LOCK_EXPIRE)
def task_video_initial_prediction(self):
    """Perform initial prediction on video files."""

    logger.info("CUDA Available:", torch.cuda.is_available())
    logger.info("Device Count:", torch.cuda.device_count())
    perform_initial_prediction_on_videos(
        MULTILABEL_MODEL_PATH,
        window_size_s = PREDICTION_SMOOTHING_WINDOW_SIZE_S,
        min_seq_len_s = PREDICTION_MIN_SEQUENCE_LENGTH_S,
    )
 

@shared_task(bind=True)
@single_instance_task(lock_expire = LOCK_EXPIRE)
def task_video_prediction_import_preflight(self):
    """Prediction import preflight."""
    videos_scheduled_for_prediction_import_preflight()

@shared_task(bind=True)
@single_instance_task(lock_expire = LOCK_EXPIRE)
def task_video_prediction_import(self):
    """Import predictions for video files."""
    import_predictions_for_videos()

@shared_task(bind=True)
@single_instance_task(lock_expire = LOCK_EXPIRE)
def task_delete_frames_preflight(self):
    """Delete frames preflight."""
    delete_frames_preflight()

@shared_task(bind=True)
@single_instance_task(lock_expire = LOCK_EXPIRE)
def task_delete_frames(self):
    """Delete frames."""
    delete_frames()

@shared_task(bind=True)
@single_instance_task(lock_expire = LOCK_EXPIRE)
def task_video_retrieve_sensitive_video_data(self):
    """Retrieve sensitive video data."""
    for video in RawVideoFile.objects.filter(
        state_frames_extracted=True,
        sensitive_meta__isnull=True
    ):
        video.update_text_metadata()

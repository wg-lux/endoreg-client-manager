from __future__ import absolute_import, unicode_literals
from celery import shared_task
import os
from pathlib import Path
from django.core.cache import cache
from datetime import timedelta

from endoreg_db.models.data_file.import_classes.raw_video import RawVideoFile
from endoreg_db.models.data_file.import_classes.processing_functions import (
    get_multilabel_model, get_multilabel_classifier
)

LOCK_EXPIRE = 60 * 60 * 24  # Lock expires in 24 h
# from celery.utils.log import get_task_logger
# logger = get_task_logger(__name__)


# import FRAME_DIR_PARENT from settings
from django.conf import settings

DROPOFF_DIR_VIDEO = settings.DROPOFF_DIR_VIDEO
DROPOFF_DIR_EXAMINATION = settings.DROPOFF_DIR_EXAMINATION
DROPOFF_DIR_HISTOLOGY = settings.DROPOFF_DIR_HISTOLOGY

PSEUDO_DIR_RAW_VIDEO = settings.PSEUDO_DIR_RAW_VIDEO
PSEUDO_DIR_RAW_PDF = settings.PSEUDO_DIR_RAW_PDF
# PSEUDO_DIR_RAW_EXAMINATION = settings.PSEUDO_DIR_RAW_EXAMINATION
# PSEUDO_DIR_RAW_HISTOLOGY = settings.PSEUDO_DIR_RAW_HISTOLOGY

FRAME_DIR_PARENT = settings.TMP_IMPORT_FRAME_DIR_PARENT
PREDICTION_DIR_PARENT = settings.PREDICTION_DIR_PARENT

MULTILABEL_MODEL_PATH = settings.MULTILABEL_MODEL_PATH
PREDICTION_SMOOTHING_WINDOW_SIZE_S = settings.PREDICTION_SMOOTHING_WINDOW_SIZE_S
PREDICTION_MIN_SEQUENCE_LENGTH_S = settings.PREDICTION_MIN_SEQUENCE_LENGTH_S

from endoreg_db.models import RawPdfFile

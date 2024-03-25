from functools import wraps
from django.core.cache import cache
from celery.utils.log import get_task_logger
import time


logger = get_task_logger(__name__)
LOCK_EXPIRE = 60 * 60  # Lock expires in 1 hour

from django.conf import settings

CENTER_NAME = settings.ENDOREG_CENTER_NAME
PROCESSOR_NAME = settings.ENDOREG_PROCESSOR_NAME
PDF_TYPE_NAME_EXAMINATION = settings.PDF_TYPE_EXAMINATION
PDF_TYPE_NAME_HISTOLOGY = settings.PDF_TYPE_HISTOLOGY

DROPOFF_DIR_VIDEO = settings.DROPOFF_DIR_VIDEO
DROPOFF_DIR_EXAMINATION = settings.DROPOFF_DIR_EXAMINATION
DROPOFF_DIR_HISTOLOGY = settings.DROPOFF_DIR_HISTOLOGY

PSEUDO_DIR_RAW_VIDEO = settings.PSEUDO_DIR_RAW_VIDEO
PSEUDO_DIR_RAW_PDF = settings.PSEUDO_DIR_RAW_PDF

FRAME_DIR_PARENT = settings.TMP_IMPORT_FRAME_DIR_PARENT
PREDICTION_DIR_PARENT = settings.PREDICTION_DIR_PARENT

MULTILABEL_MODEL_PATH = settings.MULTILABEL_MODEL_PATH
PREDICTION_SMOOTHING_WINDOW_SIZE_S = settings.PREDICTION_SMOOTHING_WINDOW_SIZE_S
PREDICTION_MIN_SEQUENCE_LENGTH_S = settings.PREDICTION_MIN_SEQUENCE_LENGTH_S

# common.py


logger = get_task_logger(__name__)

def single_instance_task(lock_expire=60*60):  # Default lock expire time set to 1 hour
    """Decorator ensuring only one task instance runs at a time."""
    def task_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # We use the task name as the lock key
            task_name = func.__name__
            lock_key = f'celery-single-instance-{task_name}'
            lock_value = f'{task_name}-{time.time()}'
            
            logger.info(f"Attempting to acquire lock for task {task_name}")
            
            # Try to acquire the lock
            if cache.add(lock_key, lock_value, lock_expire):
                logger.info(f"Lock acquired for task {task_name} with key {lock_key} and value {lock_value}")
                try:
                    logger.info(f"Lock acquired for task {task_name}, executing...")
                    return func(*args, **kwargs)
                finally:
                    if cache.get(lock_key) == lock_value:
                        cache.delete(lock_key)
                        logger.info(f"Lock released for task {task_name}")
            else:
                logger.info(f"Skipping execution for task {task_name} as it's already running")

        return wrapper
    return task_decorator

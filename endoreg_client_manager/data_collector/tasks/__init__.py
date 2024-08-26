# move files
from __future__ import absolute_import, unicode_literals
from .video_move import task_move_video_files
from .pdf_examination_move import task_move_examination_files
from .pdf_histology_move import task_move_histology_files
from .pdf_move import task_move_pdf_files

# process files
from .video_process import (
    task_extract_frames,

    task_video_ocr_preflight, task_video_ocr,
    task_video_initial_prediction_preflight, task_video_initial_prediction,
    task_video_prediction_import_preflight, task_video_prediction_import,
    task_delete_frames_preflight, task_delete_frames,
    task_video_retrieve_sensitive_video_data

)

from .pdf_all_process import task_pdf_process


from celery import shared_task
from .common import single_instance_task
import time
from celery.utils.log import get_task_logger
from .hdd import (
    mount_partition, 
    unmount_partition,
    is_mountpoint,
)

logger = get_task_logger(__name__)
LOCK_EXPIRE = 600 # * 60 * 24  # Lock expires in 24 h
# Example task which waits 2 minutes while printing a message every 30 seconds
@shared_task(bind=True)
@single_instance_task(LOCK_EXPIRE)
def example_task(self):
    for i in range(6):
        self.update_state(state='PROGRESS', meta={'current': i, 'total': 6})
        time.sleep(20)
        logger.info(f"A total of {(i+1)*20} seconds have passed")  # Use logger instead of print
    return 'Task finished'


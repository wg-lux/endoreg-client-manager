from pathlib import Path
import os
from celery import shared_task

from endoreg_db.models import RawVideoFile

from .common import (
    DROPOFF_DIR_VIDEO,
    PSEUDO_DIR_RAW_VIDEO,
    FRAME_DIR_PARENT,
    CENTER_NAME,
    PROCESSOR_NAME,
)

from .common import single_instance_task, LOCK_EXPIRE

@shared_task(bind=True)
@single_instance_task(lock_expire = LOCK_EXPIRE)
def task_move_video_files(self,
    center_name = CENTER_NAME,
    processor_name = PROCESSOR_NAME,
    source_directory = DROPOFF_DIR_VIDEO,
    destination_directory = PSEUDO_DIR_RAW_VIDEO,
    frame_directory = FRAME_DIR_PARENT
):
    """Move files from one directory to another."""
    for filename in os.listdir(source_directory):
        source_path = Path(os.path.join(source_directory, filename))

        video = RawVideoFile.create_from_file(
            file_path = source_path,
            center_name = center_name,
            processor_name = processor_name,
            frame_dir_parent = frame_directory,
            video_dir = destination_directory,
            save = True
        )

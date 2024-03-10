from __future__ import absolute_import, unicode_literals
from celery import shared_task
import shutil
import os
from pathlib import Path
import warnings
from endoreg_db.models.data_file.import_classes.raw_video import RawVideoFile

# import FRAME_DIR_PARENT from settings
from django.conf import settings
FRAME_DIR_PARENT = settings.TMP_IMPORT_FRAME_DIR_PARENT
RAW_VIDEO_DIR_PARENT = settings.RAW_VIDEO_DIR_PARENT

@shared_task
def move_files(
    center_name = "university_hospital_wuerzburg",
    processor_name = "olympus_cv_1500",
    source_directory = "/mnt/hdd-sensitive/DropOff/data",
    destination_directory = "/mnt/hdd-sensitive/Pseudo/data"
    ):

    # print("Move files from source to destination directory.")
    # print("center_name: ", center_name)
    # print("processor_name: ", processor_name)
    # print("frame_dir_parent: ", FRAME_DIR_PARENT)
    # print("video_dir_parent: ", RAW_VIDEO_DIR_PARENT)

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

@shared_task
def extract_frames():
    """Extract frames from video files."""
    for video in RawVideoFile.objects.filter(
        state_frames_extracted=False,
        state_frames_required=True
    ):
        video.extract_frames()
        video.state_frames_extracted = True
        video.save()


@shared_task
def retrieve_sensitive_video_data():
    """Retrieve sensitive video data."""
    for video in RawVideoFile.objects.filter(
        state_frames_extracted=True,
        sensitive_meta__isnull=True
    ):
        video.update_text_metadata()

@shared_task
def create_video_meta():
    """Create Video Meta"""
    for video in RawVideoFile.objects.filter(
        video_meta__isnull=True
    ):
        video.update_video_meta()
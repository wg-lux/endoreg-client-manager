# tasks.py

from celery import shared_task
from pathlib import Path
import shutil
import warnings
from .utils import find_files
import logging

logger = logging.getLogger(__name__)

# @shared_task
def collect_data(dropoff_dir, pseudo_dir, filter_expression="*"):
    # get the DROPOFF and PSEUDO directories from settings

    dropoff_dir = Path(dropoff_dir)
    pseudo_dir = Path(pseudo_dir)

    assert dropoff_dir.exists(), f"{dropoff_dir} does not exist"
    assert pseudo_dir.exists(), f"{pseudo_dir} does not exist"

    print(f"Collecting data from {dropoff_dir} to {pseudo_dir}")

    # get the list of files in the DROPOFF directory
    # dropoff_files = list(dropoff_dir.glob(filter_expression))
    dropoff_files = find_files(dropoff_dir, filter_expression)

    print(f"Found {len(dropoff_files)} files in {dropoff_dir}")

    # move each file from the DROPOFF directory to the PSEUDO directory using shutil
    for file in dropoff_files:
        try:
            shutil.move(file, pseudo_dir / file.name)
            logger.info(f"Moved {file} to {pseudo_dir / file.name}")
        except (IOError, shutil.Error) as e:
            logger.error(f"Failed to move {file} to {pseudo_dir / file.name}: {e}")

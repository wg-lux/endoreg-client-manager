from __future__ import absolute_import, unicode_literals
from celery import shared_task

from endoreg_db.models.data_file.import_classes.processing_functions import (
    process_pdf_files
)

from .common import single_instance_task, LOCK_EXPIRE

@shared_task(bind=True)
@single_instance_task(lock_expire = LOCK_EXPIRE)
def task_pdf_process(self):
    """Process examination reports."""
    process_pdf_files()


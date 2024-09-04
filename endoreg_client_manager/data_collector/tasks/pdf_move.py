from pathlib import Path
import os

from celery import shared_task

from endoreg_db.models import RawPdfFile

from .common import (
    CENTER_NAME,
    PDF_TYPE_NAME_EXAMINATION,
    DROPOFF_DIR_EXAMINATION,
    PSEUDO_DIR_RAW_PDF
)

from .common import single_instance_task, LOCK_EXPIRE

@shared_task(bind=True)
@single_instance_task(lock_expire = LOCK_EXPIRE)
def task_move_pdf_files(self,
    center_name = CENTER_NAME,
    pdf_type_name = PDF_TYPE_NAME_EXAMINATION, #must match available pdf_file from endoreg_db.models.data_file.metadata.pdf_meta.PdfType
    source_directory = DROPOFF_DIR_EXAMINATION,
    destination_directory = PSEUDO_DIR_RAW_PDF
):
    """Move files from one directory to another."""
    for file in os.listdir(source_directory):
        source_path = Path(os.path.join(source_directory, file))

        raw_pdf_file = RawPdfFile.create_from_file(
            file_path = source_path,
            center_name = center_name,
            pdf_type_name = pdf_type_name,
            destination_dir = destination_directory,
            save = True
        )
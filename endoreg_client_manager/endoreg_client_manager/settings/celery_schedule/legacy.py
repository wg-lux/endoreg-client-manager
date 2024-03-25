# Celery Beat Schedule

from datetime import timedelta
from celery.schedules import crontab
from ..default_paths import ( 
    DROPOFF_DIR_VIDEO, 
    DROPOFF_DIR_EXAMINATION,
    PSEUDO_DIR_RAW_PDF,
    PSEUDO_DIR_IMPORT
)

# Add at the end of the file
CELERY_BEAT_SCHEDULE = {
    'import_videos_from_dropoff': {
        'task': 'data_collector.tasks.move_video_files',
        'schedule': timedelta(minutes=360),  # change to `crontab(minute=0, hour=0)` to run daily at midnight
        # args: json.dumps([asd,asd,asd])
        "kwargs": {
            "source_directory": DROPOFF_DIR_VIDEO.resolve().as_posix(),
            "destination_directory": PSEUDO_DIR_IMPORT.resolve().as_posix(),   
        }
    },
    'import_videos_from_dropoff': {
        'task': 'data_collector.tasks.move_examination_files',
        'schedule': timedelta(minutes=360),  # change to `crontab(minute=0, hour=0)` to run daily at midnight
        # args: json.dumps([asd,asd,asd])
        "kwargs": {
            "source_directory": DROPOFF_DIR_EXAMINATION.resolve().as_posix(),
            "destination_directory": PSEUDO_DIR_RAW_PDF.resolve().as_posix(),   
        }
    },

    "extract_frames": {
        "task": "data_collector.tasks.extract_frames",
        "schedule": timedelta(minutes=300)
    },

    # # OCR
    "video_ocr_preflight": {
        "task": "data_collector.tasks.video_ocr_preflight",
        "schedule": timedelta(minutes=5)
    },

    "video_ocr": {
        "task": "data_collector.tasks.video_ocr",
        "schedule": timedelta(minutes=280)
    },

    # # Initial Prediction
    "video_initial_prediction_preflight": {
        "task": "data_collector.tasks.video_initial_prediction_preflight",
        "schedule": timedelta(minutes=5)
    },

    "video_initial_prediction": {
        "task": "data_collector.tasks.video_initial_prediction",
        "schedule": timedelta(minutes=400)
    },
}

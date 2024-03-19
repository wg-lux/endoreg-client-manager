# Celery Beat Schedule

from datetime import timedelta
from celery.schedules import crontab
from ..default_paths import ( 
    DROPOFF_DIR, 
    PSEUDO_DIR_IMPORT
)

# Add at the end of the file
CELERY_BEAT_SCHEDULE = {
    'import_from_dropoff': {
        'task': 'data_collector.tasks.move_files',
        'schedule': timedelta(minutes=360),  # change to `crontab(minute=0, hour=0)` to run daily at midnight
        # args: json.dumps([asd,asd,asd])
        "kwargs": {
            "source_directory": DROPOFF_DIR.resolve().as_posix(),
            "destination_directory": PSEUDO_DIR_IMPORT.resolve().as_posix(),   
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

    
    # "retrieve_sensitive_video_data": {
    #     "task": "data_collector.tasks.retrieve_sensitive_video_data",
    #     "schedule": timedelta(minutes=5)
    # },
    # "probe_video_files": {
    #     "task": "data_collector.tasks.probe_video_files",
    #     "schedule": timedelta(minutes=5)
    # }
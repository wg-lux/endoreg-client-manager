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
        'schedule': timedelta(hours=6),  # change to `crontab(minute=0, hour=0)` to run daily at midnight
        # args: json.dumps([asd,asd,asd])
        "kwargs": {
            "source_directory": DROPOFF_DIR.resolve().as_posix(),
            "destination_directory": PSEUDO_DIR_IMPORT.resolve().as_posix(),   
        }
    },
    "initial_frame_extraction": {
        "task": "data_collector.tasks.extract_frames",
        "schedule": timedelta(hours=6)
    },
    "retrieve_sensitive_video_data": {
        "task": "data_collector.tasks.retrieve_sensitive_video_data",
        "schedule": timedelta(hours=6)
    },
    "probe_video_files": {
        "task": "data_collector.tasks.probe_video_files",
        "schedule": timedelta(hours=6)
    }
}

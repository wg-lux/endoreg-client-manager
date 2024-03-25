from datetime import timedelta
from .move_files import SCHEDULE as move_files_schedule
from .video_process import SCHEDULE as video_process_schedule
from .pdf_process import SCHEDULE as pdf_process_schedule

CELERY_BEAT_SCHEDULE = {
    # 'example_task': {
    #     'task': 'data_collector.tasks.example_task',
    #     'schedule': timedelta(minutes=1),  # change to `crontab(minute=0, hour=0)` to run daily at midnight
    # }
}

CELERY_BEAT_SCHEDULE.update(move_files_schedule)
CELERY_BEAT_SCHEDULE.update(video_process_schedule)
CELERY_BEAT_SCHEDULE.update(pdf_process_schedule)

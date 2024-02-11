from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from .settings import IMPORT_DIR, RAW_DATA_DIR

import_dir = IMPORT_DIR.resolve().as_posix()
export_dir = RAW_DATA_DIR.resolve().as_posix()

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'endoreg_client_manager.settings')

app = Celery('endoreg_client_manager')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


from celery.schedules import crontab

app.conf.beat_schedule = {
    'move-files-every-day': {
        'task': 'data_collector.tasks.move_files',
        'schedule': crontab(hour=0, minute=0),  # Executes daily at midnight
        'args': (import_dir,export_dir),
    },
}

############TODO REMOVE AFTER TESTING################
app.conf.beat_schedule = {
    'move-files-every-hour': {
        'task': 'data_collector.tasks.move_files',
        'schedule': crontab(minute=21), 
        'args': (import_dir,export_dir),
    },
}

# Generated migration file in data_collector/migrations/xxxx_schedule_move_files_task.py

from django.db import migrations
import datetime
import json

def create_periodic_task(apps, schema_editor):
    CrontabSchedule = apps.get_model('django_celery_beat', 'CrontabSchedule')
    PeriodicTask = apps.get_model('django_celery_beat', 'PeriodicTask')
    
    # Create the crontab schedule: every day at 20:00
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute='0',
        hour='20',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
    )
    
    # Create the periodic task linked to the crontab schedule
    PeriodicTask.objects.get_or_create(
        crontab=schedule,
        name='Move Files Daily at 20:00',
        task='data_collector.tasks.move_files',
        kwargs=json.dumps({
            "source_directory": "./source_dir",
            "destination_directory": "./dest_dir"
        }),
    )

class Migration(migrations.Migration):

    dependencies = [
        # Add dependency on the latest django_celery_beat migration here
        ('data_collector', '0001_initial'),  # Adjust according to your app's migration files
        ('django_celery_beat', '0018_improve_crontab_helptext'),  # Ensure this is the latest for django_celery_beat
    ]

    operations = [
        migrations.RunPython(create_periodic_task),
    ]

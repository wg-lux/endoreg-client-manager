from celery import shared_task
import shutil
import os

@shared_task
def move_files(source_directory, destination_directory):
    """Move files from one directory to another."""
    for filename in os.listdir(source_directory):
        source_path = os.path.join(source_directory, filename)
        destination_path = os.path.join(destination_directory, filename)
        shutil.move(source_path, destination_path)
        print(f'Moved: {source_path} to {destination_path}')

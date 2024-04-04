# tasks.py

from celery import shared_task
import subprocess
from django.conf import settings
from .common import single_instance_task

LOCK_EXPIRE = 60 # expires in 60 seconds

@shared_task
@single_instance_task(LOCK_EXPIRE)
def mount_partition(partition_name):
    service_name = settings.PARTITION_DICT[partition_name]['mount_service']
    subprocess.run(["systemctl", "start", service_name], check=True)

@shared_task
@single_instance_task(LOCK_EXPIRE)
def unmount_partition(partition_name):
    service_name = settings.PARTITION_DICT[partition_name]['umount_service']
    subprocess.run(["systemctl", "start", service_name], check=True)

@shared_task
@single_instance_task(LOCK_EXPIRE)
def is_mountpoint(path):
    return subprocess.run(["mountpoint", "-q", path]).returncode == 0

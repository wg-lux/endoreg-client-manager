# views.py

from django.shortcuts import redirect
from django.urls import reverse
from .tasks import mount_partition, unmount_partition, is_mountpoint
from django.http import JsonResponse
from django.conf import settings

def mount_partition_view(request, partition_name):
    mount_partition.delay(partition_name)
    return JsonResponse({"status": "Mounting initiated for {}".format(partition_name)})

def unmount_partition_view(request, partition_name):
    unmount_partition.delay(partition_name)
    return JsonResponse({"status": "Unmounting initiated for {}".format(partition_name)})

def check_mount_status(request):
    mount_status = {}
    for partition_name, partition_info in settings.PARTITION_DICT.items():
        # Asynchronously check if the partition is mounted
        # Note: You might want to adjust this to be synchronous or handle the async result differently
        mounted = is_mountpoint.delay(partition_info['path'].resolve().as_posix()).get(timeout=10)
        mount_status[partition_name] = mounted
    return JsonResponse(mount_status)

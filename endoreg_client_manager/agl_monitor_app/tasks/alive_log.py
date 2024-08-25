from celery import shared_task
import time
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)
@shared_task()
def service_alive_remote_log(device_name, service_name, target_url, user, ip_address):
    from endoreg_db.models import LogType, AglServiceLogEntry, NetworkDevice, AglService
    log_type = LogType.objects.get(name="service-alive")
    device = NetworkDevice.objects.get(name=device_name)
    service = AglService.objects.get(name=service_name)

    log = AglServiceLogEntry.objects.create(
        ip_address=ip_address,
        message=f"Service {service_name} is alive. ({user}@{ip_address})",
        log_type=log_type,
        device=device,
        service=service
    )
    return str(log)
    
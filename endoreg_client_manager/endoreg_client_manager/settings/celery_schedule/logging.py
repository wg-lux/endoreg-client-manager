from datetime import timedelta

SCHEDULE = {
    "service_alive_remote_log": { 
        "task": "agl_monitor_app.tasks.alive_log.service_alive_remote_log",
        # "schedule": timedelta(minutes=5),
        "schedule": timedelta(seconds=30),
        "kwargs": {
            "device_name": "agl-gpu-client-dev",
            "service_name": "endoreg-client-manager",
            "target_url": "http://endoreg-client-localhost:9100",
            "user": "agl-admin",
            "ip_address": "172.16.255.4",
        }
    },

}

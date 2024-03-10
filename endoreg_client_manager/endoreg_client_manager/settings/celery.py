# # Celery Configuration
import json

endoreg_client_config_path = "/etc/endoreg-client-config/endoreg-center-client.json"

with open(endoreg_client_config_path) as f:
    endoreg_client_config = json.load(f)
    CELERY_BROKER_URL = endoreg_client_config["CELERY_BROKER_URL"]
    CELERY_RESULT_BACKEND = endoreg_client_config["CELERY_RESULT_BACKEND"]
    CELERY_CACHE_BACKEND = endoreg_client_config["CELERY_CACHE_BACKEND"]
    CELERY_ACCEPT_CONTENT = endoreg_client_config["CELERY_ACCEPT_CONTENT"]
    CELERY_TASK_SERIALIZER = endoreg_client_config["CELERY_TASK_SERIALIZER"]
    CELERY_RESULT_SERIALIZER = endoreg_client_config["CELERY_RESULT_SERIALIZER"]
    CELERY_TIMEZONE = endoreg_client_config["CELERY_TIMEZONE"]
    CELERY_BEAT_SCHEDULER = endoreg_client_config["CELERY_BEAT_SCHEDULER"]

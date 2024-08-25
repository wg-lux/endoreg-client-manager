# # Celery Configuration
import json
from celery.signals import after_setup_logger
from pathlib import Path

endoreg_client_config_path = "/etc/endoreg-client-config/endoreg-center-client.json"


with open(endoreg_client_config_path) as f:
    endoreg_client_config = json.load(f)
    CELERY_BROKER_URL = endoreg_client_config["CELERY_BROKER_URL"]
    CELERY_RESULT_BACKEND = endoreg_client_config["CELERY_RESULT_BACKEND"]
    CELERY_ACCEPT_CONTENT = endoreg_client_config["CELERY_ACCEPT_CONTENT"]
    CELERY_TASK_SERIALIZER = endoreg_client_config["CELERY_TASK_SERIALIZER"]
    CELERY_RESULT_SERIALIZER = endoreg_client_config["CELERY_RESULT_SERIALIZER"]
    CELERY_TIMEZONE = endoreg_client_config["CELERY_TIMEZONE"]
    CELERY_BEAT_SCHEDULER = endoreg_client_config["CELERY_BEAT_SCHEDULER"]
    CELERY_SIGNAL_LOGFILE_NAME = endoreg_client_config["CELERY_SIGNAL_LOGFILE_NAME"]


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    import logging
    from logging.handlers import RotatingFileHandler

    logging_dir = Path(CELERY_SIGNAL_LOGFILE_NAME).parent
    # Create logging directory if it does not exist
    logging_dir.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(CELERY_SIGNAL_LOGFILE_NAME, maxBytes=10485760, backupCount=3)  # 10 MB per file
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
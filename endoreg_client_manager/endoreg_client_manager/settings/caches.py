# # Celery Configuration
import json

endoreg_client_config_path = "/etc/endoreg-client-config/endoreg-center-client.json"

with open(endoreg_client_config_path) as f:
    endoreg_client_config = json.load(f)
    CACHES = endoreg_client_config["CACHES"]
from .user_settings import CENTER_CONFIG_PATH

import json

center_config_path = CENTER_CONFIG_PATH
if center_config_path.exists():
    with open(center_config_path) as f:
        center_config = json.load(f)
        ENDOREG_CENTER_NAME = center_config["endoreg-center-name"]
        ENDOREG_CENTER_ID = center_config["endoreg-center-id"]
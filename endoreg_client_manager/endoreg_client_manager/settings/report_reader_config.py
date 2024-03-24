import os
from pathlib import Path
import json
from warnings import warn
from .user_settings import CENTER_CONFIG_PATH

config_path = CENTER_CONFIG_PATH
if config_path.exists():
    with open(config_path) as f:
        _config = json.load(f)
        PDF_TYPE_EXAMINATION = _config["pdf-type-examination"]
        PDF_TYPE_HISTOLOGY = _config["pdf-type-histology"]

else:
    warn(f"Could not find config at {config_path}. Using default values")
    PDF_TYPE_EXAMINATION = "ukw-endoscopy-examination-report-generic"
    PDF_TYPE_HISTOLOGY = "ukw-endoscopy-histology-report-generic"
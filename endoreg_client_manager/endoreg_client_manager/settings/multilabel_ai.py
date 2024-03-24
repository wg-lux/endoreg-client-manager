import os
from pathlib import Path
import json
from warnings import warn
from .user_settings import MULTILABEL_AI_CONFIG_PATH

multilabel_ai_config_path = MULTILABEL_AI_CONFIG_PATH
if multilabel_ai_config_path.exists():
    with open(multilabel_ai_config_path) as f:
        multilabel_ai_config = json.load(f)
        MULTILABEL_MODEL_PATH = Path(multilabel_ai_config["model-path"])
        PREDICTION_SMOOTHING_WINDOW_SIZE_S = multilabel_ai_config["prediction-smoothing-window-size-s"]
        PREDICTION_MIN_SEQUENCE_LENGTH_S = multilabel_ai_config["prediction-min-sequence-length-s"]

else:
    warn(f"Could not find multilabel ai config at {multilabel_ai_config_path}. Using default values")
    MULTILABEL_MODEL_PATH = Path("/etc/multilabel_ai_models/model.ckpt")
    PREDICTION_SMOOTHING_WINDOW_SIZE_S = 1
    PREDICTION_MIN_SEQUENCE_LENGTH_S = 0.5
from pathlib import Path

#FIXME MIGRATE TO dotenv workflow and provide .env.example file and .env file using nixos

BASE_DIR = Path(__file__).resolve().parent.parent.parent
HDD_CONFIG_PATH = Path("/etc/endoreg-client-config/hdd.json")
CENTER_CONFIG_PATH = Path("/etc/endoreg-client-config/client-manager-config.json")
HOSTNAME_FILE = Path("/etc/endoreg-client-config/hostname")
MULTILABEL_AI_CONFIG_PATH = Path("/etc/endoreg-client-config/multilabel-ai-config.json")
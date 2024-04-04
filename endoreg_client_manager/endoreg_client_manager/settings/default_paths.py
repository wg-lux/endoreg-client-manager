import os
from pathlib import Path
from dotenv import load_dotenv

# initialize logging
import logging
logging.basicConfig(level=logging.INFO)
load_dotenv()

from .user_settings import (
    BASE_DIR,
    HDD_CONFIG_PATH,
    HOSTNAME_FILE
)

TMP_DIR = BASE_DIR / "data"
TMP_IMPORT_FRAME_DIR_PARENT = TMP_DIR / "tmp" / "raw_frames"
if not TMP_IMPORT_FRAME_DIR_PARENT.exists():
    TMP_IMPORT_FRAME_DIR_PARENT.mkdir(parents=True, exist_ok=True)

PREDICTION_DIR_PARENT = TMP_DIR / "predictions"
if not PREDICTION_DIR_PARENT.exists():
    PREDICTION_DIR_PARENT.mkdir(parents=True, exist_ok=True)

import json
# Read hostname from /etc/endoreg-client-config/hostname
hostname_file = HOSTNAME_FILE
if hostname_file.exists():
    with open(hostname_file) as f:
        AGL_HOSTNAME = f.read().strip()
else:
    AGL_HOSTNAME = "anonymous-endoreg-client"

# read /etc/endoreg-client-config/hdd.json
hdd_config = HDD_CONFIG_PATH
if hdd_config.exists():

    logging.info(f"Reading hdd config from {hdd_config}")
    with open(hdd_config) as f:
        hdd_config = json.load(f)
        hdd_config = hdd_config[AGL_HOSTNAME]["hdd"]

    DROPOFF_PARTITION = Path(hdd_config["mountpoint-parent"]["DropOff"]) / "DropOff"
    PSEUDO_PARTITION = Path(hdd_config["mountpoint-parent"]["Pseudo"]) / "Pseudo"
    PROCESSED_PARTITION = Path(hdd_config["mountpoint-parent"]["Processed"]) / "Processed"
else:
    logging.warning(f"Could not find hdd config at {hdd_config}")
    DROPOFF_PARTITION = Path("/mnt/DropOff")
    PSEUDO_PARTITION = Path("/mnt/Pseudo")
    PROCESSED_PARTITION = Path("/mnt/Processed")


# assert DROPOFF_PARTITION.exists(), f"DropOff partition does not exist at {DROPOFF_PARTITION}"
# assert PSEUDO_PARTITION.exists(), f"Pseudo partition does not exist at {PSEUDO_PARTITION}"
# assert PROCESSED_PARTITION.exists(), f"Processed partition does not exist at {PROCESSED_PARTITION}"

DROPOFF_DIR = DROPOFF_PARTITION / "data"
if not DROPOFF_DIR.exists():
    DROPOFF_DIR.mkdir()

DROPOFF_DIR_VIDEO = DROPOFF_DIR / "video"
if not DROPOFF_DIR_VIDEO.exists(): DROPOFF_DIR_VIDEO.mkdir()

DROPOFF_DIR_EXAMINATION = DROPOFF_DIR / "examination"
if not DROPOFF_DIR_EXAMINATION.exists(): DROPOFF_DIR_EXAMINATION.mkdir()

DROPOFF_DIR_HISTOLOGY = DROPOFF_DIR / "histology"
if not DROPOFF_DIR_HISTOLOGY.exists(): DROPOFF_DIR_HISTOLOGY.mkdir()

PSEUDO_DIR = PSEUDO_PARTITION / "data"
PSEUDO_DIR_IMPORT = PSEUDO_PARTITION / "import"


if not PSEUDO_DIR.exists():
    PSEUDO_DIR.mkdir()
if not PSEUDO_DIR_IMPORT.exists():
    PSEUDO_DIR_IMPORT.mkdir()

PSEUDO_DIR_RAW_VIDEO = PSEUDO_DIR_IMPORT / "video"
if not PSEUDO_DIR_RAW_VIDEO.exists():
    PSEUDO_DIR_RAW_VIDEO.mkdir()

PSEUDO_DIR_RAW_PDF = PSEUDO_DIR_IMPORT / "pdf"
if not PSEUDO_DIR_RAW_PDF.exists():
    PSEUDO_DIR_RAW_PDF.mkdir()

PSEUDO_DIR_RAW_EXAMINATION = PSEUDO_DIR_IMPORT / "examination"
if not PSEUDO_DIR_RAW_EXAMINATION.exists():
    PSEUDO_DIR_RAW_EXAMINATION.mkdir()

PSEUDO_DIR_RAW_HISTOLOGY = PSEUDO_DIR_IMPORT / "histology"
if not PSEUDO_DIR_RAW_HISTOLOGY.exists():
    PSEUDO_DIR_RAW_HISTOLOGY.mkdir()

PSEUDO_DIR_VIDEO = PSEUDO_PARTITION / "video"
if not PSEUDO_DIR_VIDEO.exists():
    PSEUDO_DIR_VIDEO.mkdir()

PSEUDO_DIR_EXAMINATION = PSEUDO_PARTITION / "examination"
if not PSEUDO_DIR_EXAMINATION.exists():
    PSEUDO_DIR_EXAMINATION.mkdir()

PSEUDO_DIR_HISTOLOGY = PSEUDO_PARTITION / "histology"
if not PSEUDO_DIR_HISTOLOGY.exists():
    PSEUDO_DIR_HISTOLOGY.mkdir()

PSEUDO_DB_PATH = PSEUDO_PARTITION / "pseudo.db"

PROCESSED_DIR = PROCESSED_PARTITION / "data"
if not PROCESSED_DIR.exists():
    PROCESSED_DIR.mkdir()
    
PROCESSED_DB_PATH = PROCESSED_PARTITION / "processed.db"

# read /etc/endoreg-client-config/hostname 

# check whether we can read / write to the pseudo dir
if not os.access(PSEUDO_DIR, os.W_OK):
    raise PermissionError(f"Cannot write to {PSEUDO_DIR}")

PARTITION_DICT = {
    "DropOff": {
        "path": DROPOFF_PARTITION,
        "mount_service": "mountDropOffService",
        "umount_service": "umountDropOffService",
    },
    "Pseudo": {
        "path": PSEUDO_PARTITION,
        "mount_service": "mountPseudoService",
        "umount_service": "umountPseudoService",
    },
    "Processed": {
        "path": PROCESSED_PARTITION,
        "mount_service": "mountProcessedService",
        "umount_service": "umountProcessedService",
    }
}

from pathlib import Path

############### TODO #################
# CHANGE HARDCODED PATHS
WORKING_DIR = Path("/home/agl-admin/endoreg-client-files")
SENSITIVE_DIR = Path("/home/agl-admin/endoreg-client-files/raw")
######################################

assert WORKING_DIR.exists(), f"Working directory {WORKING_DIR} does not exist"
assert SENSITIVE_DIR.exists(), f"Sensitive data directory {SENSITIVE_DIR} does not exist"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

IMPORT_DIR = SENSITIVE_DIR / "import"
if not IMPORT_DIR.exists():
    IMPORT_DIR.mkdir()

RAW_DATA_DIR = SENSITIVE_DIR / "raw_data"
if not RAW_DATA_DIR.exists():
    RAW_DATA_DIR.mkdir()

PROCESSED_DATA_DIR = SENSITIVE_DIR / "processed_data"
if not PROCESSED_DATA_DIR.exists():
    PROCESSED_DATA_DIR.mkdir()

DB_DIR = SENSITIVE_DIR / "db"





import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DROPOFF_DIR = Path(os.environ.get("DROPOFF_DIR", BASE_DIR / "FIXME"))
DROPOFF_DIR = DROPOFF_DIR / "data"

PSEUDO_DIR = Path(os.environ.get("PSEUDO_DIR", BASE_DIR / "FIXME"))
PSEUDO_DB_PATH = PSEUDO_DIR / "pseudoDb"
PSEUDO_DIR = PSEUDO_DIR / "data"

# check whether we can read / write to the pseudo dir
if not os.access(PSEUDO_DIR, os.W_OK):
    raise PermissionError(f"Cannot write to {PSEUDO_DIR}")

PROCESSED_DIR = Path(os.environ.get("PROCESSED_DIR", BASE_DIR / "FIXME"))
PROCESSED_DB_PATH = PROCESSED_DIR / "processed.db"
PROCESSED_DIR = PROCESSED_DIR / "data"



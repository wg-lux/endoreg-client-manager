import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DROPOFF_DIR = os.environ.get('DROPOFF_DIR', '/FIXME')
PSEUDO_DIR = os.environ.get('PSEUDO_DIR', '/FIXME')
PROCESSED_DIR = os.environ.get('PROCESSED_DIR', '/FIXME')

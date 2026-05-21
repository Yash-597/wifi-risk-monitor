from __future__ import annotations
from pathlib import Path
import os
import sys


if getattr(sys, "frozen", False):
    PROJECT_ROOT = Path(sys.executable).resolve().parent
    DATA_DIR = Path(os.environ.get("LOCALAPPDATA", PROJECT_ROOT)) / "WifiSecurityTray"
else:
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    DATA_DIR = PROJECT_ROOT / "data"

CONFIG_FILE = DATA_DIR / "settings.json"
AUDIT_LOG_FILE = DATA_DIR / "audit.jsonl"

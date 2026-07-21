import sys
from pathlib import Path

ORGANISATION_NAME = "INFORLAC"
APP_NAME = "RetroArch Savestates Manager"
APP_VERSION = (1, 0, 0)
APP_ROOT_PATH = (
    Path(".")
    if not hasattr(sys.modules[__name__], "__compiled__")
    else Path(sys.argv[0])
)

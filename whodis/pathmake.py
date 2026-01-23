from pathlib import Path
import os
import sys
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
import subprocess
import os
import pickle
from rich.console import Console
import datetime
import time

console = Console()
def get_app_data_dir(app_name="whodis"):
    if sys.platform.startswith("win"):
        base = Path(os.getenv("APPDATA"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        # Linux / BSD / WSL
        base = Path(os.getenv("XDG_DATA_HOME", Path.home() / ".local" / "share"))

    return base / app_name

logpath = os.path.join(get_app_data_dir(), 'logs')
capturepath = os.path.join(get_app_data_dir(), 'camcapture')
embedpath = os.path.join(get_app_data_dir(), 'embeddings')
unknownpath =  os.path.join(get_app_data_dir(), 'unknownsound')

def makefiles():
    program_dirs = [logpath, capturepath, embedpath, unknownpath]
    if os.path.exists(get_app_data_dir()):
        for folder in program_dirs:
            if os.path.exists(os.path.join(get_app_data_dir(), folder)):
                    continue
            else:
                os.mkdir(os.path.join(get_app_data_dir(), folder))
                None
    else:
        console.print(f"Creating program folders in {get_app_data_dir()}\n[red]remember to enroll faces with 'faceid.py enroll path/to/folder' for the program to identify persons")
        os.mkdir(get_app_data_dir())
        for folder in program_dirs:
            os.mkdir(os.path.join(get_app_data_dir(), folder))

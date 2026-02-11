from pathlib import Path
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
from rich.console import Console
import os
import sys
from contextlib import redirect_stdout, redirect_stderr
import warnings
import time
import datetime
import shutil

console = Console()

def init_face_app():
    with open(os.devnull, "w") as f, redirect_stdout(f), redirect_stderr(f):
        warnings.filterwarnings(
            "ignore",
            category=FutureWarning,
            module="insightface"
        )

        from insightface.app import FaceAnalysis
        app = FaceAnalysis(
            name="buffalo_l",
            providers=["CPUExecutionProvider"]
        )
        app.prepare(ctx_id=0, det_size=(640, 640))

    return app

def save_log():
    currenttime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
    loggedfolder = os.path.join(logpath, f"{currenttime}_Captures")

    os.makedirs(loggedfolder, exist_ok=True)

    files = os.listdir(capturepath)
    if files:
        for file in files:
            shutil.move(
                os.path.join(capturepath, file),
                os.path.join(loggedfolder, file))

def get_app_data_dir(app_name="whodis"):
    if sys.platform.startswith("win"):
        base = Path(os.getenv("APPDATA"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        # Linux / BSD / WSL
        base = Path(os.getenv("XDG_DATA_HOME", Path.home() / ".local" / "share"))

    return base / app_name

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
            
logpath = os.path.join(get_app_data_dir(), 'logs')
capturepath = os.path.join(get_app_data_dir(), 'camcapture')
embedpath = os.path.join(get_app_data_dir(), 'embeddings')
unknownpath =  os.path.join(get_app_data_dir(), 'unknownsound')

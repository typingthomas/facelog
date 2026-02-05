import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
import subprocess
import os
import pickle
from rich.console import Console
from pathlib import Path
import shutil
from . import pathmake
console = Console()

accepted_formats = ['.jpg', '.jpeg', '.png', '.mp3'] # mp3 for greeting only

def analyze(path, savepath):
        #app = FaceAnalysis(providers=['CPUExecutionProvider'], name="buffalo_l")
        #app.prepare(ctx_id=0, det_size=(640, 640))

        app = pathmake.init_face_app()
        name = Path(path).name
        identitypath = os.path.join(savepath, name)
        if not os.path.exists(identitypath):
                os.mkdir(identitypath)
        embedpath = os.path.join(identitypath, f"embeddings.pkl")
        if os.path.exists(embedpath):
            with open(embedpath, "rb") as f:
                db = pickle.load(f)
        else:
            db = {}
        db.setdefault(name, [])

        #loop through the whitlisted folder grabbing embedding from each face then making a .pkl of the data
        for file in os.listdir(path):
            if Path(file).suffix.lower() not in accepted_formats:
                console.print(f'[red]{file} --format is not accepted, skipping file...')
                continue
            if ".mp3" in file:
                shutil.copy(os.path.join(path, file), os.path.join(identitypath, 'greet.mp3'))
                console.print(f'[yellow bold]Adding {file} as greeting...')
                continue
            namenoext = os.path.abspath(os.path.join(path,file[0:file.index(".")]))
            img = ins_get_image(os.path.join(path, namenoext))
            faces = app.get(img)
            faces = sorted(faces, key=lambda f: f.det_score, reverse=True)
            embedding = faces[0].embedding
            db[name].append(embedding)

        with open(embedpath, "wb") as f:
            pickle.dump(db, f)

        console.print(f"[yellow bold]Stored embeddings at {embedpath}")

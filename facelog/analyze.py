import cv2
import numpy as np
import os
import pickle
from rich.console import Console
from pathlib import Path
import shutil
from . import pathmake
console = Console()

accepted_formats = ['.jpg', '.jpeg', '.png', '.mp3'] # mp3 for greeting only

def analyze(path, savepath):
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
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            ext = Path(file).suffix.lower()
            if ext not in accepted_formats:
                console.print(f"[red]{file} -- format not accepted, skipping...")
                continue
            if ext == ".mp3":
                shutil.copy(full_path, os.path.join(identitypath, "greet.mp3"))
                console.print(f"[yellow bold]Added {file} as greeting")
                continue
            img = cv2.imread(full_path)
            if img is None:
                console.print(f"[red]Failed to load {file}, skipping...")
                continue
            # Detect faces
            faces = app.get(img)
            if not faces:
                console.print(f"[yellow]No face detected in {file}")
                continue
            faces = sorted(faces, key=lambda f: f.det_score, reverse=True)
            embedding = faces[0].embedding

            db[name].append(embedding)
            console.print(f"[green]Embedding stored for {file}")

        with open(embedpath, "wb") as f:
            pickle.dump(db, f)

        console.print(f"[yellow bold]Stored embeddings at {embedpath}")

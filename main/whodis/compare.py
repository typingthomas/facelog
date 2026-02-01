import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
import subprocess
import os
import pickle
from pickle import load
from rich.console import Console
import datetime
import time
import argparse
import vlc
from pathlib import Path
from . import pathmake
import threading

console = Console()
last_chime_time = 0
CHIME_COOLDOWN = 5  # seconds
chime_file = None

def _play_file(file_path):
    player = vlc.MediaPlayer(file_path)
    player.play()
    time.sleep(0.5)
    while player.is_playing():
        time.sleep(0.1)

def play_chime(path):
    """Play chime asynchronously, respects cooldown."""
    global last_chime_time, chime_file
    now = time.time()
    if now - last_chime_time < CHIME_COOLDOWN:
        return  # still in cooldown

    for file in os.listdir(path):
        if file.lower().endswith(".mp3"):
            file_path = os.path.join(path, file)
            chime_file = file_path
            threading.Thread(target=_play_file, args=(file_path,), daemon=True).start()
            last_chime_time = now
            break
        
app = pathmake.init_face_app()
def l2_norm(x):
    return x / np.linalg.norm(x)

def match_embedding(live_emb, whitelist,foldername, threshold=0.5):
    live_emb = l2_norm(live_emb)

    sims = []
    for emb in whitelist.get(foldername, []):
        emb = l2_norm(emb)
        sims.append(np.dot(live_emb, emb))

    best_sim = float(np.max(sims))
    mean_sim = float(np.mean(sims))

    print(f"best={best_sim:.3f} mean={mean_sim:.3f}")

    return best_sim >= threshold
def process_file(embedding):
    #gather embedding
    recognized = False
    for folder in os.listdir(pathmake.embedpath):
        folderpath = os.path.join(pathmake.embedpath, folder)
        for file in os.listdir(folderpath):
            if '.pkl' in file:
                with open(os.path.join(folderpath, file), "rb") as f:
                    knownembed = pickle.load(f)
                if match_embedding(embedding, knownembed, folder, threshold=0.5) == True:
                    play_chime(folderpath)
                    console.print(f"[green]Face recognized: {folder}")
                    recognized = True
                    return True, os.path.basename(folder), folderpath
                else:
                    continue
    if recognized == False:
         console.print("[red]No face recognized")
         play_chime(pathmake.unknownpath)
         return False, 'Unknown', pathmake.unknownpath


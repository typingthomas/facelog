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
import pathmake

console = Console()
def play_chime(path):
    for file in os.listdir(path):
        if '.mp3' in file:
             welcomeChime = vlc.MediaPlayer(os.path.join(path, file))
             welcomeChime.play()
             time.sleep(.5)
             while welcomeChime.is_playing():
                 time.sleep(.5)

app = FaceAnalysis(providers=['CPUExecutionProvider'], name="buffalo_l")
app.prepare(ctx_id=0, det_size=(640, 640))

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
                    return True
                else:
                    continue
    if recognized == False:
         console.print("[red]No face recognized")
         play_chime(pathmake.unknownpath)
         return False


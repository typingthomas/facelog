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
from pathlib import Path
import compare

def openwebcam(savepath):
    currenttime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    console = Console()

    app = FaceAnalysis(providers=['CPUExecutionProvider'], name="buffalo_l")
    app.prepare(ctx_id=0, det_size=(640, 640))
    webcam = cv2.VideoCapture(0)
        #set webcam size here
    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    try:
        # videoname = os.path.join(savepath, f"{currenttime}.mp4")
        #if you have only one camera leave selection at 0

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # out = cv2.VideoWriter(videoname, fourcc, 20.0, (640,  360))
        start_time = time.time()
        frame_count = 0
        while True:
            try:
                ret, frame=webcam.read()
                if ret == True:
                    ###out.write(frame)  #If camera is returning video, start recording
                    if frame_count % 100 == 0:
                        faces = app.get(frame)
                        now = time.time()
                        if not faces:
                            console.print("[yellow]Nobody in frame")
                        else:
                            embedding = faces[0].embedding
                            console.print("[yellow]FACE DETECTED")
                            if compare.process_file(embedding) == False:
                                detected = os.path.join(savepath, f"{frame_count}-{currenttime}Unknown.jpg")
                            else:
                                detected = os.path.join(savepath, f"{frame_count}-{currenttime}Known.jpg")
                            cv2.imwrite(detected, frame)
                    frame_count += 1
            except Exception as e:
                console.print(f"[red]Something went wrong...{e}")
    except KeyboardInterrupt:
        # subprocess.run('clear')
        console.print(f"[yellow bold]Stopping program and saving files to {savepath}")
        webcam.release()
        # out.release()
        cv2.destroyAllWindows()
        exit()


import cv2
import os
from rich.console import Console
import datetime
import time
from pathlib import Path
from . import compare
from . import pathmake

def openwebcam(savepath):
    currenttime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    console = Console()
    app = pathmake.init_face_app()
        
    webcam = cv2.VideoCapture(0)
    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    try:
        frame_count = 0
        while True:
            try:
                ret, frame=webcam.read()
                if ret == True:
                    if frame_count % 100 == 0:
                        faces = app.get(frame)
                        now = time.time()
                        if not faces:
                            console.print(f"[yellow bold]Nobody in frame")
                        else:
                            embedding = faces[0].embedding
                            console.print("[yellow bold]FACE DETECTED")
                            matched, folder, folderpath = compare.process_file(embedding)
                            if matched == False:
                                detected = os.path.join(savepath, f"Unknown-{frame_count}-{currenttime}.jpg")
                            else:
                                detected = os.path.join(savepath, f"{folder}-{frame_count}-{currenttime}.jpg")
                            cv2.imwrite(detected, frame)
                    frame_count += 1
            except Exception as e:
                console.print(f"[red]Something went wrong...{e}")
    except KeyboardInterrupt:
        console.print(f"[yellow bold]Stopping program and saving files to {pathmake.logpath}")
        pathmake.save_log()
        webcam.release()
        exit()


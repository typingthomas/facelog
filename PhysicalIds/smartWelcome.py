import time
import cv2
from rich.console import Console
from datetime import datetime
import subprocess
import os
# Makes python stop freaking out about dependencies
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_TRACE"] = ""
os.environ["MEDIAPIPE_DISABLE_GPU"] = "1"
import mediapipe as mp
#clearing previous sessions captures
working_dir = subprocess.getoutput('pwd')
subprocess.call(['rm','-rf', f'{working_dir}/CamCapture'])
subprocess.call(['mkdir', 'CamCapture'])

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
                        
currenttime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
console = Console()

def openwebcam():
    try:
        last_proc = None
        filename = f"CamCapture/{currenttime}.mp4"
        #if you have only one camera leave selection at 0
        webcam = cv2.VideoCapture(0)
        #set webcam size here
        webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(filename, fourcc, 20.0, (640,  360))
        start_time = time.time()
        frame_count = 0
        with mp_face_detection.FaceDetection(
            model_selection=1, min_detection_confidence=0.5) as face_detection:
            #function to run program for a limited time,
            #while time.time() - start_time < 15:
            while True:
                try:
                    ret, frame=webcam.read()
                    if ret == True:
                        out.write(frame)  #If camera is returning video, start recording
                        frame.flags.writeable = False
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        results = face_detection.process(frame)

                        # Draw the face detection annotations on the frame.
                        frame.flags.writeable = True
                        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                        if results.detections:
                            for detection in results.detections:
                                bbox = detection.location_data.relative_bounding_box
                                h, w, _ = frame.shape

                                # Convert to pixel coordinates
                                x = int(bbox.xmin * w)
                                y = int(bbox.ymin * h)
                                width = int(bbox.width * w) * 2
                                height = int(bbox.height * h) * 2

                                # Crop the face
                                x1, y1 = max(0, x), max(0, y)
                                x2, y2 = min(w, x + width), min(h, y + height)
                                if frame_count % 10 == 0:
                                    face_crop = frame[y1:y2, x1:x2]

                                    detected = f"CamCapture/{frame_count}{currenttime}FaceDetected.jpg"
                                    cv2.imwrite(detected, face_crop)
                                    now = time.time()
                                    if last_proc is None or last_proc.poll() is not None:
                                        console.print('[yellow bold]FACE DETECTED')
                                        # subprocess.call('clear')

                                        cv2.imwrite(detected, face_crop)
                                        console.print('[green]Determining guest :) ')
                                        last_proc = subprocess.Popen(['python3','associate.py', f'{detected}'])
                                    else:
                                        # subprocess.call('clear')
                                        console.print('[yellow]Still determining ID of previous capture[/yellow]')
                            mp_drawing.draw_detection(frame, detection)
                            out.write(frame )
                        cv2.imshow('WhoDis?', frame)
                        frame_count += 1
                except Exception as e:
                    console.print("[red]Something went wrong...{e}")    
    except KeyboardInterrupt:
        subprocess.run('clear')
        console.print("[yellow bold]Stopping program and saving files to CamCapture")
        webcam.release()
        out.release()
        cv2.destroyAllWindows()
        exit()
            
console.print(r"""[yellow]                                       
 _       ____          ____  _     
| |     / / /_  ____  / __ \(_)____
| | /| / / __ \/ __ \/ / / / / ___/
| |/ |/ / / / / /_/ / /_/ / (__  ) 
|__/|__/_/ /_/\____/_____/_/____/  
                                                          
    [/yellow][yellow bold]By: Thomas Bu https://github.com/typingthomas[/yellow bold]         
              """)
console.print("[yellow]Press enter to get started...[/yellow]")
input()
console.print("[yellow]Starting....")
try:
    openwebcam()
except Exception as e:
    console.print("[red]Something went wrong...{e}")

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
import argparse
import analyze
import watch
import pathmake


console = Console()
def enroll(path):
    pathmake.makefiles()
    analyze.analyze(path, pathmake.embedpath)
    
def main():
        parser = argparse.ArgumentParser(
        description="FaceID controller")
        
        #check if program files exist
        parser.add_argument(
            '-e',
            '--enroll',
            nargs='?',
            const=True,
            metavar='',
            required=False,
            type=str,
            help="Used to enroll a folder with photos of a approved person eg- whodis.py -e path/to/whitelist/person, images must be .jpg, .jpeg or .png format"
        )
        
        args = parser.parse_args()
        
        if args.enroll:
            if os.path.exists(args.enroll) == False:
                console.print(f'[red]ERROR [red bold]{args.enroll}[/red bold] is not a valid path')
                exit()
            enroll(args.enroll)
            exit()
        console.print("Checking if program files exist..")
        pathmake.makefiles()
        console.print("Starting facial recognition...")
        watch.openwebcam(pathmake.capturepath)
        
        

if __name__ == "__main__":
    main()

    

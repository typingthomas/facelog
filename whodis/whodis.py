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
from . import analyze
from . import watch
from . import pathmake
import shutil

def main():
        console = Console()
        parser = argparse.ArgumentParser(
        description="FaceID controller")
        
        #check if program files exist
        parser.add_argument(
            '-e',
            '--enroll',
            nargs='?',
            const=True,
            metavar='path/to/folder',
            required=False,
            type=str,
            help="Used to enroll a folder with photos of a approved person, images must be .jpg, .jpeg or .png format"
        )
        parser.add_argument(
            "--unknown-sound",
             metavar="MP3",
             help="Set sound to play when an unknown face is detected"
         )

        
        args = parser.parse_args()
        
        if args.enroll:
            if os.path.exists(args.enroll) == False:
                console.print(f'[red]ERROR [red bold]{args.enroll}[/red bold] is not a valid path')
                exit()
            console.print("[yellow bold]Searching folder...")
            pathmake.makefiles()
            analyze.analyze(args.enroll, pathmake.embedpath)
            exit()
        if args.unknown_sound:
            if os.path.exists(args.unknown_sound) == False:
                  console.print(f'[red]ERROR [red bold]{args.enroll}[/red bold] is not a valid path')
                  exit()
            pathmake.makefiles()      
            if len(os.listdir(pathmake.unknownpath)) > 0:
                console.print(f"[yellow bold]{pathmake.unknownpath} Already has a .mp3, would you like to overwrite it?")
                answer = input("y/n: ")
                if answer == 'n':
                    console.print("[yellow bold]Exiting...")
                    exit()
                if answer == 'y':
                    console.print(f"[yellow bold]Saving {args.unknown_sound} as {os.path.join(pathmake.unknownpath, 'unknown.mp3')}")
            shutil.copy(args.unknown_sound, os.path.join(pathmake.unknownpath, 'unknown.mp3'))
            exit()



        console.print("Checking program files..")
        pathmake.makefiles()
        console.print("Starting facial recognition...")
        if len(os.listdir(pathmake.embedpath)) < 1:
                console.print(f"[red bold]Warning[/red bold] [red]No photos have been enrolled in the {pathmake.embedpath} folder\nNo faces will be identified, see 'whodis -h'")
        watch.openwebcam(pathmake.capturepath)
        
        

if __name__ == "__main__":
    main()

    

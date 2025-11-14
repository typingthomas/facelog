import time
import os
import argparse
import os
from deepface import DeepFace
import vlc
from rich.console import Console

console = Console()

def play_chime(person):
    welcomeChime = vlc.MediaPlayer(f"sounds/{person}.mp3")
    welcomeChime.play()
    time.sleep(.5)
    while welcomeChime.is_playing():
        time.sleep(.5)


def process_file(person_img):
    print(f"[INFO] Checking {person_img} for matches...")

    for folder in os.listdir('whiteList'):
        console.print(f"[yellow]checking if faces matches the[/yellow][yellow bold] {folder}[/yellow bold][yellow] DB")
        try:
            dfs = DeepFace.find(
                img_path=person_img,
                db_path=f"whiteList/{folder}",
                detector_backend="opencv",
                enforce_detection=False
            )
            if dfs and len(dfs) > 0 and len(dfs[0]) > 0:
                console.print(f"[green bold]SUCCESS[/green bold] [green]Match found in whitelist:[/green][greeen bold] {folder}")
                play_chime(folder)
                return
            else:
                console.print("[red bold]FAIL[/red bold][red] No match found.")
                # play_chime('fart')
                play_chime('unknown')

        except Exception as e:
            play_chime('unknownFS')
            print(f"[ERROR] DeepFace exception: {str(e)}")
            return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a file input")
    parser.add_argument("file", help="Path to the file you want to process")

    args = parser.parse_args()

    if os.path.isfile(args.file):
        process_file(args.file)
    else:
        print("File does not exist.")

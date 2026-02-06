# WhoDis?

This is a lightweight live, local, facial recognition program that can run on Windows or Linux designed to identify known individuals in real time using a standard webcam.

## Description

I've written this project completley in python and have utilized the InsightFace library for facial recognition model and OpenCV + NumPy to help me gather the embeddings live and identify faces on the spot, it's able to run completley offline once configured and works well with old hardware and webcams that you might have laying around, however the better quality your webcam/camera is the better the performance will be. I've tried to write the code as simple as I could as to make it easy for users to modify it to their own needs.

## Getting Started

### Dependencies

* Python 3.11.x
* Webcam/Camera
* Vlc Media Player

### Installing
1. Install VLC Media Player
Windows:
https://www.videolan.org/vlc/download-windows.html

Linux:
```
apt install vlc
```
2. Clone this repo
```
git clone https://github.com/typingthomas/WhoDis
```
3. Inside the new folder install with pip
```
pip install whodis
```

### Setup

1. Before running it is required to 'enroll' a folder with photos of a whitelisted person for the program to actually be able to identify someone
* folders with ~7 photos(.jpg, .jpeg, .png) with differnt angles provide the best reference to performance ratio for the program
* if you would like a specific .mp3 to be played when the face is recognized you can add that into the folder aswell
```
whodis -e path/to/folder
```
2. If you would like a specific .mp3 to be played when the program can't recognize a face you can do that aswell!
```
whodis --unknown-sound path/to/.mp3
```
### Executing program
* To run the program it's simple
```
whodis
```
* To quit the program just do Ctrl+C and all the captured faces will be saved

## Help
```
whodis -h
```
### Common Issues
* Sound
A common issue that I've run into is that when having sounds play, they may be cut short. This is because when the program detects a new face it will start analyzing the embedding to see who it is, this process interupts any media being played through the program. This typically will happen when the .mp3 is longer then 5 seconds, to negate this I recommend having a short .mp3 being played. To update a .mp3 run the '-e' or '--unknown-sound' flag again and the new .mp3 will be saved

## Authors

[Thomas Bu](https://github.com/typingthomas)

## Version History

* 2026.1.0
    * Initial Release

## License

This project is licensed under the [MIT] License - see the LICENSE.md file for details

## Acknowledgments

* [InsightFace](https://github.com/deepinsight/insightface)


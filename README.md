# facelog?

facelog is a lightweight, offline facial recognition system built in Python. It uses InsightFace and OpenCV to identify known individuals in real time through a standard webcam. Designed to run on modest hardware, facelog is suitable for local security monitoring or home lab deployments.

## Description

I've written this project completely in python and have utilized the InsightFace library for facial recognition model and OpenCV + NumPy to help me gather the embeddings live and identify faces on the spot, it's able to run completely offline once configured and works well with old hardware and webcams that you might have laying around, however the better quality your webcam/camera is the better the performance will be. I've tried to write the code as simple as I could as to make it easy for users to modify it to their own needs.

### How it works
1. Uses OpenCV to get live video output
2. Every 100 frames, the frame is analyzed using InsightFace's buffalo_l model for live embedding extraction
3. Those live embeddings are then compared with stored embeddings of known individuals using cosine similiarity
4. Optionally serves a Flash-based live detection dashboard aswell as plays a custom audio greeting

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
git clone https://github.com/typingthomas/facelog
```
3. Inside the new folder install with pip
```
pip install .
```

### Setup

1. Before running it is required to 'enroll' a folder with photos of a whitelisted person for the program to actually be able to identify someone
* folders with ~7 photos(.jpg, .jpeg, .png) with different angles provide the best reference to performance ratio for the program
* if you would like a specific .mp3 to be played when the face is recognized you can add that into the folder aswell
```
facelog -e path/to/folder
```
2. If you would like a specific .mp3 to be played when the program can't recognize a face you can do that aswell!
```
facelog --unknown-sound path/to/.mp3
```
> [!NOTE]  
> There is currently no support for multiple camera devices. Program will run and default to one camera.
### Executing program
* To run the program it's simple
```
facelog
```
* You can also start a webserver alongside the program to display captured faces and their identity
```
facelog --web
```
* To quit the program just do Ctrl+C and all the captured faces will be saved

## Help
```
facelog -h
```
### Common Issues
* Sound

A common issue that I've run into is that when having sounds play, they may be cut short. This is because when the program detects a new face it will start analyzing the embedding to see who it is, this process interrupts any media being played through the program. This typically will happen when the .mp3 is longer than 5 seconds, to negate this I recommend having a short .mp3 being played. To update a .mp3 run the '-e' or '--unknown-sound' flag again and the new .mp3 will be saved

## Authors

[Thomas Bu](https://github.com/typingthomas)

## Version History

* 2026.1.0
    * Initial Release

## License

This project is licensed under the [MIT] License - see the LICENSE.md file for details

## Acknowledgments

* [InsightFace](https://github.com/deepinsight/insightface)


# Python Music Player
A simple program to play music in python

![music-player1](docs/music-player1.JPG)

## Installation
1. Clone repository:
`git clone https://github.com/Enprogames/MusicPlayer.git`
   
2. Create new virtual environment using venv
    1. Linux: `python3 -m venv venv --prompt music-player`
    2. Windows: `python -m venv venv --prompt music-player`
   
3. Activate the virtual environment:
    1. Linux: `source venv/bin/activate`
    2. Windows: `source venv/Scripts/activate`
   
4. Now that you're in the virtual environment, install the requirements:
`pip install -r requirements.txt`

## Problem
There doesn't seem to be a decent python sound library. This project mostly uses pygame's mixer 
module, which allows for many useful functions when working with sound. Unfortunately, it 
works slightly differently on Windows and Linux. It doesn't support playback of MP3 files on linux,
and it also doesn't allow for changing the playback position of wave files on any platform.

## Functionality
- Change volume
- Pause
- Get and set location of song

#!/usr/bin/env python

# libraries required:
# mutagen, eyed3, python-magic, pydub, simpleaudio
# Find new library to replace pygame.mixer.music. It must:
# work on windows and ubuntu
# play mp3, wav, and ogg
# be able to get and set location of song
# be able to change its own volume
#
import os
import sys

if os.path.basename(os.getcwd()) == 'src':
    sys.stdout = open('console.log', 'w')
else:
    sys.stdout = open('src/console.log', 'w')

import traceback
import pygame as pg
from mutagen.mp3 import MP3
import mutagen

import window
import player

if os.path.basename(os.getcwd()) == 'src':
    file = "example.mp3"
else:
    file = "src/example.mp3"


def playbutton_press():

    if player_window.get_song_path_input() != "":
        file = player_window.location_box.get()
        if file[0] == '"' and file[-1] == '"':
            file = file[1:-1]
        player.play(file)
        tick()


def canvas_click_event(event_origin):
    x0 = event_origin.x
    y0 = event_origin.y

    # set location to click_position-margins
    duration_position = x0-player_window.duration_slider.slider_horizontal_margins

    # if the mouse click is in the location of the slider, set the position and change the song position
    if 0 <= duration_position <= player_window.duration_slider.slider_width:
        duration_percentage = duration_position / player_window.duration_slider.slider_width
        if not player.is_playing():
            playbutton_press()
        if player.is_playing():
            player_window.set_duration_slider_percentage(duration_percentage)
            player.set_pos_percentage(duration_percentage)


def tick():
    if player.is_playing():
        volume = player_window.get_volume_slider_location()
        player.set_volume(volume)
        duration_percent = round((player.get_pos() / 1000.0) / player.metadata.info.length, 3)
        player_window.set_duration_slider_percentage(duration_percent)
        player_window.after(1, tick)


player = player.PGPlayer()

player_window = window.PlayerWindow(play_cmd=playbutton_press, pause_cmd=player.pause, change_volume_cmd=player.set_volume)  # create a player window

# create an event listener for clicks on the duration slider
player_window.duration_slider.bind("<B1-Motion>", canvas_click_event)

player_window.show()  # this must be done last

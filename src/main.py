# libraries required:
# mutagen, eyed3, python-magic, pydub, simpleaudio
# Find new library to replace pygame.mixer.music. It must:
# work on windows and ubuntu
# play mp3, wav, and ogg
# be able to get and set location of song
# be able to change its own volume
#
import traceback
import os

import pygame as pg
from mutagen.mp3 import MP3
import mutagen

import window
import player

file = "example.mp3"
previous = ""


def play():
    global player_window, file, song_length, conversion_factor, previous, metadata
    if player_window.get_song_path_input() != "":
        file = player_window.location_box.get()
        if file[0] == '"' and file[-1] == '"':
            file = file[1:-1]

    if file != previous:

        pg.init()
        pg.mixer.init()
        pg.mixer.music.load(file)
        tick()  # start ticking method (currently only changes location of player window slider as the song plays

        previous = file
        metadata = mutagen.File(file, easy=True)
        song_length = metadata.info.length
        try:
            player_window.set_song_title(metadata['title'][0])
        except KeyError:
            player_window.set_song_title(os.path.basename(file))
        except Exception as e:
            traceback.print_exc()
        pg.mixer.music.play()

    pg.mixer.music.unpause()
    tick()


def pause():
    try:
        pg.mixer.music.pause()
    except Exception as e:
        traceback.print_exc()


def change_song_volume(_=None):
    try:
        pg.mixer.music.set_volume(player_window.get_volume_slider_location())
    except pg.error:
        pass


def change_song_location(_=None):
    try:
        pg.mixer.music.set_pos(_)
    except Exception as e:
        traceback.print_exc()


def canvas_click_event(event_origin):
    x0 = event_origin.x
    y0 = event_origin.y

    duration_position = x0-player_window.duration_slider.slider_horizontal_margins

    # if the mouse click is in the location of the slider, set the position and change the song position
    if 0 <= duration_position <= player_window.duration_slider.slider_width:
        player_window.set_duration_slider_position(duration_position)
        marker_percentage = player_window.duration_slider.get_marker_percentage()
        change_song_location(marker_percentage * song_length)


def tick():
    global duration
    if pg.mixer.music.get_busy() == 1:
        duration_percent = round((pg.mixer.music.get_pos() / 1000.0) / song_length, 3)
        player_window.set_duration_slider_percentage(duration_percent)

        player_window.after(1, tick)


player = player.PGPlayer()

player_window = window.PlayerWindow(play, pause, change_song_volume) # create a player window

# create an event listener for clicks on the duration slider
player_window.duration_slider.bind("<B1-Motion>", canvas_click_event)

player_window.show()  # this must be done last

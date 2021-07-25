# libraries required:
# mutagen, eyed3, python-magic, pydub, simpleaudio
# Find new library to replace pygame.mixer.music. It must:
# work on windows and ubuntu
# play mp3, wav, and ogg
# be able to get and set location of song
# be able to change its own volume
#
import platform
import tkinter as tk

import pygame as pg
from mutagen.mp3 import MP3

import window

file = "Fireworks.mp3"
previous = ""
length = 0
conversion_factor = 0
duration = 0
metadata = 0
platform = platform.system()


def play():
    global player_window, file, length, conversion_factor, previous, metadata
    if player_window.get_song_path_input() != "":
        file = location_box.get()
        if file[0] == '"' and file[-1] == '"':
            file = file[1:-1]

    if file != previous:
        if platform == "Windows":

            pg.init()
            pg.mixer.init()
            pg.mixer.music.load(file)

            length = MP3(file).info.length
            # length = get_duration('song.ogg')
            print(length)
            previous = file
            # metadata = eyed3.load(file)
            # tag = metadata.tag
            try:
                title_label.config(text="song title")
                # titlelabel.config(text = tag.title)
            except:
                pass
            pg.mixer.music.play()

    pg.mixer.music.unpause()
    tick()


def pause():
    try:
        pg.mixer.music.pause()
    except:
        pass


def change_song_volume(_=None):
    try:
        pg.mixer.music.set_volume(player_window.get_volume_slider_location())
    except:
        pass


def change_song_location(_=None):
    try:
        pass
        # pg.mixer.music.set_pos(durationslider.get())
    except:
        pass


def canvas_click_event(event_origin):
    global x0,y0
    x0 = event_origin.x
    y0 = event_origin.y

    duration_position = x0-player_window.duration_slider.slider_horizontal_margins
    if 0 <= duration_position <= player_window.duration_slider.slider_width:
        player_window.set_duration_slider_position(duration_position)


def tick():
    global duration, marker
    if pg.mixer.music.get_busy() == 1:
        duration = round((pg.mixer.music.get_pos() / 1000.0), 2)
        duration = round((duration / length), 2)
        player_window.set_duration_slider_position(duration)

        player_window.after(1, tick)


player_window = window.PlayerWindow(play, pause, change_song_volume, change_song_location)
player_window.duration_slider.bind("<B1-Motion>", canvas_click_event)
player_window.show()

# Canvas for showing the duration
# canvas = tk.Canvas(root, bg="grey", highlightthickness=0, bd=12, width="250", height="10")
# canvas.create_rectangle(30, 10, 250, 80, outline="grey26", fill="black")
# marker = canvas.create_rectangle(30, 10, 32, 20, outline="white", fill="white")
# canvas.place(relx=.5, rely=1, anchor="s")

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

file = "Fireworks.mp3"
previous = ""
length = 0
conversion_factor = 0
duration = 0
metadata = 0
platform = platform.system()


def play():
    global file, length, conversion_factor, previous, metadata
    if locationbox.get() != "":
        file = locationbox.get()
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
                titlelabel.config(text="song title")
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


def change_volume(_=None):
    try:
        pg.mixer.music.set_volume(volumeslider.get())
    except:
        pass


def change_location(_=None):
    try:
        pass
        # pg.mixer.music.set_pos(durationslider.get())
    except:
        pass


def tick():
    global duration, marker
    if (pg.mixer.music.get_busy() == 1):
        duration = round((pg.mixer.music.get_pos() / 1000.0), 2)
        duration = round((duration / length), 2)
        # print(duration)
        durationslider.set(duration)

        root.after(1, tick)


root = tk.Tk()
root.title('Music Player')
root.geometry("250x250")
root.pack_propagate(0)
root.resizable(0, 0)
root.configure(background='grey')

titlelabel = tk.Label(root, bg="grey", fg="black", font=('consolas', 10, 'bold'))
titlelabel.place(relx=.5, rely=.15, anchor="center")

locationlabel = tk.Label(root, text="Location of Music File", bg="grey", fg="black")
locationlabel.place(relx=.5, rely=.3, anchor="center")
locationbox = tk.Entry(root)
locationbox.place(relx=.5, rely=.4, anchor="center")

volumeslider = tk.Scale(root, from_=0, to=1, resolution=0.01, bg="grey", fg="white", bd=0, troughcolor="black",
                        showvalue=0, width=10, highlightcolor="grey", highlightbackground="grey", sliderlength=10,
                        command=change_volume)
volumeslider.set(1)
volumeslider.place(relx=.05, rely=.65, anchor="center")

playbutton = tk.Button(root, text="Play", font=('consolas', 20, 'bold'), bg="grey26", fg="white", command=play)
playbutton.place(relx=.3, rely=.7, anchor="center")

pausebutton = tk.Button(root, text="Pause", font=('consolas', 20, 'bold'), bg="grey26", fg="white", command=pause)
pausebutton.place(relx=.7, rely=.7, anchor="center")

# slider for duration
durationslider = tk.Scale(root, from_=0, to=1, resolution=0.001, bg="grey", fg="white", bd=0, troughcolor="black",
                          showvalue=0, width=10, sliderlength=7, highlightcolor="grey", highlightbackground="grey",
                          orient=tk.HORIZONTAL, length=200, command=change_location)
durationslider.place(relx=.5, rely=.9, anchor="center")

# Canvas for showing the duration
# canvas = tk.Canvas(root, bg="grey", highlightthickness=0, bd=12, width="250", height="10")
# canvas.create_rectangle(30, 10, 250, 80, outline="grey26", fill="black")
# marker = canvas.create_rectangle(30, 10, 32, 20, outline="white", fill="white")
# canvas.place(relx=.5, rely=1, anchor="s")

root.grid_rowconfigure(0, weight=2)
root.grid_rowconfigure(2, weight=2)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

root.mainloop()

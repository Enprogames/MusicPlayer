import traceback

import os

import pygame as pg
from mutagen.mp3 import MP3
import mutagen


class PGPlayer:
    """
    Audio player using pygame.mixer.music
    """
    def __init__(self):

        pg.init()
        pg.mixer.init()

        self.position = 0
        self.metadata = None
        self.volume = 1.0

        self.previous_file: str = ''

        self.song_title: str = ''
        self.artist: str = ''
        self.length = 0

        # variables for keeping track of the current position of the track
        self.last_set_pos = 0  # last location set from 0 to length
        self.last_set_pos_total = 0  # time between last playback time change and start of playback (not including any pauses)

    def play(self, file_path=None):

        if not self.is_finished():
            pg.mixer.music.unpause()

        elif not file_path or file_path == self.previous_file and not self.is_playing():  # if no file path is provided, try to play the previous file
            pg.mixer.music.load(self.previous_file)
            self.position = 0
            self.last_set_pos = 0
            self.last_set_pos_total = 0
            pg.mixer.music.play()

        elif file_path != self.previous_file:

            pg.mixer.music.load(file_path)

            self.length = MP3(file_path).info.length * 1000

            self.previous_file = file_path

            self.position = 0
            self.last_set_pos = 0
            self.last_set_pos_total = 0

            try:
                self.metadata = mutagen.File(file_path, easy=True)
                self.song_title = self.metadata['title'][0]
            except KeyError:
                self.song_title = os.path.basename(file_path)

            pg.mixer.music.play()

    def pause(self):
        try:
            pg.mixer.music.pause()
        except Exception:
            traceback.print_exc()

    def set_volume(self, volume=None):
        self.volume = volume
        try:
            pg.mixer.music.set_volume(float(volume))
        except pg.error:
            traceback.print_exc()

    def set_pos(self, position=None):
        """
        Set the position of the song
        :param position: Playback position to set the song to
        :return:
        """
        if self.is_finished() or self.is_paused():
            self.play()

        self.last_set_pos = position  # time the track was set to last time playback position was set. Used for calculating current playback position
        self.last_set_pos_total = pg.mixer.music.get_pos()  # total time the track has been playing for at this time
        self.position = position
        pg.mixer.music.set_pos(position/1000)

    def set_pos_percentage(self, percentage):
        """
        Set the position of the song as a percentage of how far to set it to. e.g. 0 is the start, 1.0 is the end.
        :param percentage: Fraction of 1 for how far into the song to set the position.
        """
        self.set_pos(percentage * self.length)

    def get_pos(self) -> float:
        """
        Since pygame's get_pos() function doesn't take into account any changes to the playback position through
        set_pos, the actual playback position is calculated separately.
        :return: The current playback position of the song in milliseconds
        """
        playtime_ms = pg.mixer.music.get_pos()
        self.position = self.last_set_pos + (playtime_ms-self.last_set_pos_total)
        return self.position

    def get_pos_percentage(self) -> float:
        """
        Return how far the song has played through so far as a fraction of 1.
        """
        self.get_pos() / self.length

    def is_playing(self):
        return pg.mixer.music.get_busy()

    def is_paused(self):
        return not (pg.mixer.music.get_busy() or self.is_finished())

    def is_finished(self):
        """
        When playback of the file has finished, pygame.mixer.music.get_pos() returns -1, so this is our indicator that playback has stopped
        """
        return pg.mixer.music.get_pos() == -1

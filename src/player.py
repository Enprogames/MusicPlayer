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

        self.previous_file: str = ''

        self.song_title: str = ''
        self.artist: str = ''
        self.song_length = 0

    def play(self, file_path):

        if file_path != self.previous_file:

            pg.mixer.music.load(file_path)

            self.song_length = MP3(file_path).info.length

            self.previous_file = file_path

            try:
                metadata = mutagen.File(file_path, easy=True)
                self.song_title = metadata['title'][0]
            except KeyError:
                self.song_title = os.path.basename(file_path)

            pg.mixer.music.play()

        else:
            pg.mixer.music.unpause()

    def set_pos(self, position=None):
        """
        Set the position of the song
        :param position: Playback position to set the song to
        :return:
        """
        self.position = position
        pg.mixer.music.set_pos(position)

    def set_pos_percentage(self, percentage):
        """
        Set the position of the song as a percentage of how far to set it to. e.g. 0 is the start, 1.0 is the end.
        :param percentage: Fraction of 1 for how far into the song to set the position.
        """
        pass

    def get_pos(self) -> float:
        """
        Since pygame's get_pos() function doesn't take into account any changes to the playback position through
        set_pos, the actual playback position is calculated separately.
        :return: The current playback position of the song in milliseconds
        """

        playtime_ms = pg.mixer.music.get_pos()
        return playtime_ms - self.position

    def get_pos_percentage(self) -> float:
        """
        Return how far the song has played through so far as a fraction of 1.
        """
        pass

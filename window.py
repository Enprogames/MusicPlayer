import tkinter as tk


class DurationSlider(tk.Canvas):
    """
    Canvas showing the duration of a song and how much has played. Also has the functionality of changing the
    position of the marker if changing the song playback position is a feature in the program.
    """

    def __init__(self, root: tk.Tk, width=250, height=10, slider_width=220, slider_height=12, marker_width=2,
                 marker_height=10, slider_horizontal_margins=30, slider_vertical_margins=10):

        super().__init__(root, bg="grey25", highlightthickness=0, bd=12, width=f"{width}", height=f"{height}")

        self.create_rectangle(slider_horizontal_margins, slider_vertical_margins,
                              slider_horizontal_margins+slider_width, slider_vertical_margins+slider_height,
                              outline="grey25", fill="black")
        self.marker = self.create_rectangle(slider_horizontal_margins, slider_vertical_margins,
                              slider_horizontal_margins+marker_width,
                              slider_vertical_margins+marker_height, outline="white", fill="white")

        self.place(relx=.5, rely=1, anchor="s")

        self.root = root
        self.slider_width = slider_width
        self.slider_height = slider_height
        self.marker_width = marker_width
        self.marker_height = marker_height
        self.slider_horizontal_margins = slider_horizontal_margins
        self.slider_vertical_margins = slider_vertical_margins

    def set_marker_position(self, position):
        """
        Change the position of the marker in this slider canvas
        """

        self.coords(self.marker, self.slider_horizontal_margins+position, self.slider_vertical_margins,
                    self.slider_horizontal_margins+self.marker_width+position,
                    self.slider_vertical_margins+self.marker_height)


class PlayerWindow(tk.Tk):

    def __init__(self, play_cmd, pause_cmd, change_volume_cmd, change_location_cmd, background_color='grey25'):
        """
        Set up all parts of the main player window. Functions for interacting with the player must be given as
        parameters from the program which uses this module.

        :param play_cmd: command to play the currently loaded song
        :param pause_cmd: command to pause the currently loaded song
        :param change_volume_cmd: command for changing the volume of the player
        :param change_location_cmd: command for changing the location of the song being played
        :param background_color: background color for main window and all elements
        """
        super().__init__()

        self.title('Music Player')
        self.geometry("250x250")
        self.pack_propagate(0)
        self.resizable(0, 0)
        self.configure(background=background_color)

        self.title_label = tk.Label(self, bg=background_color, fg="black", font=('consolas', 10, 'bold'))
        self.title_label.place(relx=.5, rely=.15, anchor="center")

        location_label = tk.Label(self, text="Location of Music File", bg=background_color, fg="black")
        location_label.place(relx=.5, rely=.3, anchor="center")
        self.location_box = tk.Entry(self)
        self.location_box.place(relx=.5, rely=.4, anchor="center")

        play_button = tk.Button(self, text="Play", font=('consolas', 20, 'bold'), bg=background_color, fg="white",
                                command=play_cmd)
        play_button.place(relx=.3, rely=.7, anchor="center")

        pause_button = tk.Button(self, text="Pause", font=('consolas', 20, 'bold'), bg=background_color, fg="white",
                                 command=pause_cmd)
        pause_button.place(relx=.7, rely=.7, anchor="center")

        # Canvas for showing the duration
        self.duration_slider = DurationSlider(self)

    def show(self):
        self.mainloop()

    def get_song_path_input(self):
        return self.location_box.get()

    def get_volume_slider_location(self):
        return self.volume_slider.get()

    def set_duration_slider_position(self, position):
        self.duration_slider.set_marker_position(position)

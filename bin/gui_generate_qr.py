import tkinter as tk
from tkinter import ttk
from turtle import RawTurtle
from tkinter.messagebox import showerror

from bin.vectorize_qr import *


class GuiGenerateQr:
    def __init__(self, main, options):
        self.main = main
        self.options = options

        self._qr = None
        self._spiral_path = None

        self.tc_frame = self._init_frame_text_convert()
        self.dwg_frame = self._init_frame_turtle()

    def get_qr_spiral_paths(self):
        """Getter method.
        :returns the spiral path if created, otherwise None."""
        return self._spiral_path

    def _init_frame_text_convert(self):
        """Initializes the Text-to-QR-code generator section of the GUI"""
        text_convert_frame = tk.Frame(bd=5)
        text_convert_frame['relief'] = 'ridge'
        text_convert_frame.grid(column=0, row=0, sticky='W', **self.options)

        # qr text label
        qr_text_label = ttk.Label(text_convert_frame, text='Text to convert')
        qr_text_label.grid(column=0, row=0, sticky='W', **self.options)

        # qr text entry
        self.qr_text = tk.StringVar()
        qr_text_entry = ttk.Entry(text_convert_frame, textvariable=self.qr_text, width=31)
        qr_text_entry.grid(column=1, row=0, **self.options)
        qr_text_entry.focus()

        # create qr button
        create_qr_button = ttk.Button(text_convert_frame, text='Create QR')
        create_qr_button.grid(column=2, row=0, sticky='W', **self.options)
        create_qr_button.configure(command=self._create_qr_button_clicked)

        # progress segment
        self.progress_label = tk.Label(text_convert_frame)
        self.progress_label.grid(column=0, row=1, sticky='W', **self.options)

        # progress bar
        self.progress = ttk.Progressbar(text_convert_frame, length=277, mode="determinate",
                                        takefocus=False)
        self.progress.grid(column=1, row=1, columnspan=2, sticky='W', **self.options)

        return text_convert_frame

    def _init_frame_turtle(self):
        """Initializes the Turtle drawing section of the GUI"""
        drawing_frame = tk.Frame(bd=5)
        drawing_frame['relief'] = 'ridge'
        drawing_frame.grid(column=0, row=1, columnspan=3, rowspan=5, sticky='W', **self.options)
        turtle_canvas = tk.Canvas(drawing_frame)
        turtle_canvas.pack()
        self.turtle = RawTurtle(turtle_canvas)
        self.turtle.hideturtle()
        self.turtle.speed(0)
        self.turtle.up()

        return drawing_frame

    def _create_qr_from_input(self, text_to_qr):
        """This method requests a QR code to be generated by the library.
        It then vectorizes it and generates spiral paths."""
        self._qr = QrCode.encode_text(text_to_qr, QrCode.Ecc.MEDIUM)
        qr_vect = VectorizeQr(self._qr, 0)
        self._spiral_path = qr_vect.generate_spiral_path()

    def _draw_qr_turtle(self):
        """Method that draws a QR code path based on the QrPathSegment data class with Turtle."""
        self._prepare_turtle(self._qr.get_size())

        path_count = len(self._spiral_path)
        self.progress.config(maximum=path_count)
        for i in range(path_count):
            self.progress_label.config(text='Path: {:d}'.format(i) +
                                            ' Len: {:d}'.format(self._spiral_path[i].get_xy_line().get_abs_length()))
            for vect in self._spiral_path[i].get_z_vector():
                length = vect.get_length()
                if vect.get_state():
                    self.turtle.down()
                    self.turtle.forward(self.pen_size * length)
                    self.turtle.up()
                else:
                    self.turtle.forward(self.pen_size * length)
            self.turtle.right(90)
            self.progress.step()

        self.turtle.hideturtle()
        self.progress_label.config(text='')

    def _prepare_turtle(self, qr_size):
        """Prepares the turtle tool for another drawing, i.e. clearing, scaling, centering"""
        # clear screen and reset turtle
        self.turtle.up()
        self.turtle.clear()
        self.turtle.setheading(0)

        # scale pensize to make QR-code fit screen
        self.pen_size = 11 - (qr_size // 20)
        self.turtle.pensize(self.pen_size)

        # center turtle on screen
        offset = (qr_size * self.pen_size) / 2
        self.turtle.goto(self.turtle.pos()[0] - offset, self.turtle.pos()[1] + offset)
        self.turtle.showturtle()

        # EVENT HANDLERS ----------------------------

    def _create_qr_button_clicked(self):
        """ Handle create button click event"""
        try:
            text = self.qr_text.get()
        except ValueError as error:
            showerror(title='Text Parse Error', message='Error: Could not convert the text to as string:\n' + error)
            return
        self._create_qr_from_input(text)
        self._draw_qr_turtle()

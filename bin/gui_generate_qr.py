import tkinter as tk
from tkinter import ttk
from turtle import RawTurtle
from tkinter.messagebox import showerror

from bin.vectorize_qr import *


class GenerateQr:
    def __init__(self, main, options):
        self.main = main
        self.options = options

        self.tc_frame = self._init_frame_text_convert()
        self.dwg_frame = self._init_frame_turtle()

    def _init_frame_text_convert(self):
        text_convert_frame = tk.Frame(bd=5)
        text_convert_frame['relief'] = 'ridge'
        text_convert_frame.grid(column=0, row=0, sticky='W', **self.options)

        # qr text label
        qr_text_label = ttk.Label(text_convert_frame, text='Text to convert')
        qr_text_label.grid(column=0, row=0, sticky='W', **self.options)

        # qr text entry
        self.qr_text = tk.StringVar()
        qr_text_entry = ttk.Entry(text_convert_frame, textvariable=self.qr_text, width=31)
        qr_text_entry.grid(column=1, row=0, columnspan=3, **self.options)
        qr_text_entry.focus()

        # create qr button
        create_qr_button = ttk.Button(text_convert_frame, text='Create QR')
        create_qr_button.grid(column=4, row=0, sticky='W', **self.options)
        create_qr_button.configure(command=self._create_qr_button_clicked)

        # progress bar
        self.progress = ttk.Progressbar(text_convert_frame, length=368, mode="determinate",
                                        takefocus=False)
        self.progress.grid(column=0, row=1, columnspan=5)

        return text_convert_frame

    def _create_qr_button_clicked(self):
        """ Handle create button click event"""
        try:
            t = self.qr_text.get()
            result = 'To be converted: ' + t
            self._draw_qr_turtle(t)
        except ValueError as error:
            showerror(title='Error', message=error)

    def _init_frame_turtle(self):
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

    def _draw_qr_turtle(self, text_to_qr):
        qr = QrCode.encode_text(text_to_qr, QrCode.Ecc.MEDIUM)
        qr_vect = VectorizeQr(qr, 0)
        paths = qr_vect.generate_spiral_path()

        self._prepare_turtle(qr.get_size())

        path_count = len(paths)
        self.progress.config(maximum=path_count + 1)
        for i in range(path_count):
            # print('Path: {:d}'.format(i) + ' length: {:d}'.format(paths[i].get_xy_line().get_abs_length()))
            for vect in paths[i].get_z_vector():
                # print('Length: {:d}'.format(vect.get_length()) + ' State: {:d}'.format(vect.get_state()))
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

    def _prepare_turtle(self, qr_size):
        # clear screen and reset turtle
        self.turtle.done()
        self.turtle.clear()
        self.turtle.setheading(0)

        # scale pensize to make QR-code fit screen
        self.pen_size = 11 - (qr_size // 20)
        self.turtle.pensize(self.pen_size)

        # center turtel on screen
        offset = (qr_size * self.pen_size) / 2
        self.turtle.goto(self.turtle.pos()[0] - offset, self.turtle.pos()[1] + offset)
        self.turtle.showturtle()

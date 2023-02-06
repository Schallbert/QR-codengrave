import tkinter as tk
from tkinter import ttk
from turtle import RawTurtle
from tkinter.messagebox import showerror

from qrcodegen import QrCode

from src.resources import app_image_path
from src.platform.vectorize_helper import QrValueTable
from src.platform.line_path import LinePath


class GuiGenerateQr:
    def __init__(self, main, options):
        self._main = main
        self._options = options

        self._path = None
        self._stop_draw = False
        self._turtle = None

        self.tc_frame = self._init_frame_text_convert()
        self.dwg_frame = self._init_frame_turtle()

    def get_qr_path(self):
        """Getter method.
        :returns the spiral path if created, otherwise None."""
        return self._path

    def _init_frame_text_convert(self):
        """Initializes the Text-to-QR-code generator section of the GUI"""
        text_convert_frame = tk.LabelFrame(bd=5, text='Convert Text to QR-Code')
        text_convert_frame['relief'] = 'ridge'
        text_convert_frame.grid(column=0, row=0, sticky='NEWS', **self._options)

        # qr text label
        qr_text_label = tk.Label(text_convert_frame, text='Text: ')
        qr_text_label.grid(column=0, row=0, sticky='W', **self._options)

        # qr text entry
        self.qr_text = tk.StringVar()
        qr_text_entry = ttk.Entry(text_convert_frame, textvariable=self.qr_text, width=40)
        qr_text_entry.grid(column=1, row=0, **self._options)
        qr_text_entry.focus()

        # create qr button
        create_qr_button = ttk.Button(text_convert_frame, text='Create QR')
        create_qr_button.grid(column=2, row=0, sticky='W', **self._options)
        create_qr_button.configure(command=self._create_qr_button_clicked)

        # stop sim button
        stop_draw_button = ttk.Button(text_convert_frame, text='Stop Draw')
        stop_draw_button.grid(column=2, row=1, sticky='W', **self._options)
        stop_draw_button.configure(command=self._stop_draw_button_clicked)

        # progress bar
        self.progress = ttk.Progressbar(text_convert_frame, style='teal.Horizontal.TProgressbar', orient='horizontal',
                                        length=248, mode="determinate", takefocus=False)
        self.progress.grid(column=0, row=1, columnspan=2, sticky='E', **self._options)

        return text_convert_frame

    def _init_frame_turtle(self):
        """Initializes the Turtle drawing section of the GUI"""
        drawing_frame = tk.LabelFrame(bd=5, text='QR-code drawing screen')
        drawing_frame['relief'] = 'ridge'
        drawing_frame.grid(column=0, row=1, rowspan=3, sticky='NEWS', **self._options)
        self._turtle_canvas = tk.Canvas(drawing_frame, height=300, width=300)
        self._turtle_canvas.pack()
        self._img = tk.PhotoImage(file=app_image_path)
        self._turtle_canvas.create_image(152, 152, image=self._img)
        return drawing_frame

    def _create_qr_from_input(self, text_to_qr):
        """This method requests a QR code to be generated by the library.
        It then vectorizes it and generates spiral paths."""
        qr = QrCode.encode_text(text_to_qr, QrCode.Ecc.MEDIUM)
        qr_vect = QrValueTable()
        qr_vect.set_qr(qr)
        self._path = LinePath(qr_vect)

    def _draw_qr_turtle(self):
        """Method that draws a QR code path based on the QrPathSegment data class with Turtle."""
        self._main.update_status('\u270d Drawing')

        path_count = len(self._path.get_vectors())
        self.progress.config(maximum=path_count)
        self._stop_draw = False
        for i in range(path_count):
            self.progress.step()
            if self._stop_draw:
                break
            for vect in self._path.get_vectors():
                if self._stop_draw:
                    break
                if vect.x_length == 0:
                    length = vect.y_length
                else:
                    length = vect.x_length
                self._turtle.setpos(self.pen_size * vect.position.x, self.pen_size * vect.position.y)
                self._turtle.setheading(vect.x_length * 90)
                self._turtle.down()
                self._turtle.forward(self.pen_size * length)
                self._turtle.up()

        self._turtle.hideturtle()
        self._stop_draw = False
        self._main.update_status()

    def _prepare_turtle(self):
        """Prepares the turtle tool for another drawing, i.e. clearing the screen"""
        self._turtle = RawTurtle(self._turtle_canvas)
        self._turtle.hideturtle()
        self._turtle.speed(0)

    def _stop_drawing(self):
        if self._turtle is not None:
            self._stop_draw = True
            self._turtle.up()
            self.progress.stop()
            self._turtle.setheading(0)

    def _prepare_screen_for_drawing(self, qr_size):
        """Scales pensize to fit QR-code to screen by scaling. Centers for drawing"""
        self._stop_drawing()
        self._turtle.clear()

        if qr_size > 100:
            self.pen_size = 1
        else:
            self.pen_size = 13 - (qr_size // 10)
        self._turtle.pensize(self.pen_size)

        # center turtle on screen
        offset = (qr_size * self.pen_size) / 2
        self._turtle.goto(0 - offset, 0 + offset)

        self._turtle.showturtle()

        # EVENT HANDLERS ----------------------------

    def _create_qr_button_clicked(self):
        """ Handle create button click event"""
        try:
            text = self.qr_text.get()
        except ValueError as error:
            showerror(title='Text Parse Error', message='Error: Could not convert the text to string:\n' + error)
            return

        if self._turtle is None:
            self._prepare_turtle()

        self._create_qr_from_input(text)
        self._main.set_project_name(text)
        self._prepare_screen_for_drawing(self._path.get_size())
        self._draw_qr_turtle()

    def _stop_draw_button_clicked(self):
        """Handle stop draw button click event"""
        self._stop_drawing()

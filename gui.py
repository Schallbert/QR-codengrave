import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from turtle import RawTurtle

from configuretool import ConfigureTool
from vectorize_qr import *
from qrcodegen import QrCode


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("EngraveQr")
        self.canvas = tk.Canvas(master)
        self.canvas.config(width=600, height=600)

        self.frame = ttk.Frame(self.master)
        self.options = {'padx': 5, 'pady': 5}

        self.tc_frame = self._init_frame_text_convert()
        self.ts_frame = self._init_frame_tool_section()
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
        qr_text_entry = ttk.Entry(text_convert_frame, textvariable=self.qr_text)
        qr_text_entry.grid(column=1, row=0, **self.options)
        qr_text_entry.focus()

        # create qr button
        create_qr_button = ttk.Button(text_convert_frame, text='Create QR')
        create_qr_button.grid(column=2, row=0, sticky='W', **self.options)
        create_qr_button.configure(command=self._create_qr_button_clicked)

        # result label
        self.result_label = ttk.Label(text_convert_frame)
        self.result_label.grid(row=1, columnspan=3, **self.options)

        return text_convert_frame

    def _init_frame_tool_section(self):
        tool_section_frame = tk.Frame(bd=5)
        tool_section_frame['relief'] = 'ridge'
        tool_section_frame.grid(column=3, row=1, sticky='N', **self.options)

        # Add Tool
        add_tool_button = ttk.Button(tool_section_frame, text='Add tool')
        add_tool_button.grid(column=1, row=0, sticky='W', **self.options)
        add_tool_button.configure(command=self._add_tool_button_clicked)

        # Remove Tool
        remove_tool_button = ttk.Button(tool_section_frame, text='Remove tool')
        remove_tool_button.grid(column=2, row=0, sticky='W', **self.options)
        remove_tool_button.configure(command=self._remove_tool_button_clicked)

        # Select Tool
        select_tool_label = ttk.Label(tool_section_frame, text='Select tool')
        select_tool_label.grid(column=1, row=1, sticky='E', **self.options)
        selected = tk.StringVar()
        selected.set('0')
        tool_dropdown = tk.OptionMenu(tool_section_frame, selected, *self.options)
        tool_dropdown.grid(column=2, row=1, columnspan=2, sticky='W', **self.options)

        return tool_section_frame

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

    def _create_qr_button_clicked(self):
        """ Handle create button click event"""
        try:
            t = self.qr_text.get()
            result = 'To be converted: ' + t
            self.result_label.config(text=result)
            self._draw_qr_turtle(t)
        except ValueError as error:
            showerror(title='Error', message=error)

    def _add_tool_button_clicked(self):
        """Handle add tool button click event"""
        wdw = ConfigureTool(self.master, self.options)

    def _remove_tool_button_clicked(self):
        """Handle add tool button click event"""

    def _draw_qr_turtle(self, text_to_qr):
        qr = QrCode.encode_text(text_to_qr, QrCode.Ecc.MEDIUM)
        qr_vect = VectorizeQr(qr, 0)
        paths = qr_vect.generate_spiral_path()

        self._center_qr_on_turtle_screen(qr.get_size())

        # for path in paths:
        for i in range(len(paths)):
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

        self.turtle.hideturtle()

    def _center_qr_on_turtle_screen(self, qr_size):
        self.pen_size = 11 - (qr_size // 20)
        self.turtle.pensize(self.pen_size)

        offset = (qr_size * self.pen_size) / 2
        self.turtle.goto(self.turtle.pos()[0] - offset, self.turtle.pos()[1] + offset)
        self.turtle.showturtle()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()

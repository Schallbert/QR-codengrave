import tkinter as tk
from tkinter import ttk


class GuiGenerateGcode:
    def __init__(self, main, options):
        """displays the tool handling section within the main gui window"""
        self._main = main
        self._options = options

        self._generate_frame = self._init_frame_gcode_section()

    def _init_frame_gcode_section(self):
        gcode_frame = tk.Frame(bd=5)
        gcode_frame['relief'] = 'ridge'
        gcode_frame.grid(column=1, row=4, sticky='SW', **self._options)

        # Generate button
        generate_button = ttk.Button(gcode_frame, text='Generate G-code')
        generate_button.grid(column=0, row=3, sticky='W', **self._options)
        generate_button.configure(command=self._generate_button_clicked)

        # Append button
        append_button = ttk.Button(gcode_frame, text='Append G-code to File')
        append_button.grid(column=1, row=3, sticky='W', **self._options)
        append_button.configure(command=self._append_button_clicked)

        return gcode_frame

    # EVENT HANDLERS ----------------------------

    def _generate_button_clicked(self):
        self._main.update_status('\u2699 G-code')
        self._main.run_gcode_generator()
        self._main.update_status()

    def _append_button_clicked(self):
        pass

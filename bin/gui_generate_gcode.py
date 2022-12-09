import tkinter as tk
from tkinter import ttk

from bin.gui_tool_configure import validate_number
from bin.machinify_vector import XzeroYzero


class GuiGenerateGcode:
    def __init__(self, root, options):
        """displays the tool handling section within the main gui window"""
        self._root = root
        self.options = options

        self._xy0 = XzeroYzero()

        self._generate_frame = self._init_frame_gcode_section()

    def _init_frame_gcode_section(self):
        gcode_frame = tk.Frame(bd=5)
        gcode_frame['relief'] = 'ridge'
        gcode_frame.grid(column=2, row=2, sticky='W', **self.options)
        reg = gcode_frame.register(validate_number)

        # Set XY zero position
        setxy0_label = tk.Label(gcode_frame, text='Set X and Y zero relative to QR-code center')
        setxy0_label.grid(column=0, row=0, columnspan=2, sticky='W', **self.options)

        setx0_label = tk.Label(gcode_frame, text='Set X0 [mm]')
        setx0_label.grid(column=0, row=1, sticky='E', **self.options)

        self._setx0 = tk.DoubleVar()
        self._setx0.set(self._xy0.get().x)

        self.setx0_entry = ttk.Entry(gcode_frame, textvariable=self._setx0, width=5)
        self.setx0_entry.config(validate="key", validatecommand=(reg, '%P'))
        self.setx0_entry.grid(column=1, row=1, **self.options)
        self._setx0.trace('u', self._setx0_changed)

        sety0_label = tk.Label(gcode_frame, text='Set Y0 [mm]')
        sety0_label.grid(column=0, row=2, sticky='E', **self.options)

        self._sety0 = tk.DoubleVar()
        self._sety0.set(self._xy0.get().y)

        self.sety0_entry = ttk.Entry(gcode_frame, textvariable=self._sety0, width=5)
        self.sety0_entry.config(validate="key", validatecommand=(reg, '%P'))
        self.sety0_entry.grid(column=1, row=2, **self.options)
        self._sety0.trace('u', self._sety0_changed)

        # Generate button
        generate_button = ttk.Button(gcode_frame, text='Generate G-code')
        generate_button.grid(column=0, row=3, sticky='W', **self.options)
        generate_button.configure(command=self._generate_button_clicked())

        # Append button
        append_button = ttk.Button(gcode_frame, text='Append G-code to File')
        append_button.grid(column=1, row=3, sticky='W', **self.options)
        append_button.configure(command=self._append_button_clicked())

        return gcode_frame

    def _generate_button_clicked(self):
        pass

    def _append_button_clicked(self):
        pass

    def _setx0_changed(self, *args):
        try:
            self._setx0.get()
        except tk.TclError:
            return
        self._xy0.set_x0(self._setx0.get())

    def _sety0_changed(self, *args):
        try:
            self._sety0.get()
        except tk.TclError:
            return
        self._xy0.set_y0(self._sety0.get())

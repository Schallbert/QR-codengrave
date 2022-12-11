import tkinter as tk
from tkinter import ttk

from bin.persistence import *
from bin.vectorize_qr import Point

from bin.gui_xy0_configure import *
from bin.gui_helpers import validate_number


class GuiXy0Manager:
    def __init__(self, main, options):
        self._main = main
        self._options = options

        self._xy0 = Persistence.load(Point())

        self._params_frame = self._init_frame_params_section()

    def get_xy0_parameters(self):
        """Getter function.
        :returns an XzeroYzero object"""
        return self._xy0

    def set_xy0_parameters(self, xy0):
        """Setter function. To be called by child: configure window"""
        self._xy0 = xy0
        self._setx0.config(text=str(self._xy0.x))
        self._sety0.config(text=str(self._xy0.y))

    def _init_frame_params_section(self):
        """create all items within the parameters frame section"""
        params_frame = tk.Frame(bd=5)
        params_frame['relief'] = 'ridge'
        params_frame.grid(column=1, row=3, sticky='W', **self._options)

        reg = params_frame.register(validate_number)

        # Set XY zero position label
        setxy0_label = tk.Label(params_frame, text='Set X and Y zero relative to QR-code center')
        setxy0_label.grid(column=0, row=0, columnspan=2, sticky='W', **self._options)

        # X label
        setx0_label = ttk.Label(params_frame, text='Set X0 [mm]')
        setx0_label.grid(column=0, row=1, sticky='E', **self._options)

        # X var
        self._setx0 = ttk.Label(params_frame, text=str(self._xy0.x), width=6)
        self._setx0.grid(column=1, row=1, sticky='W', **self._options)

        # Y label
        sety0_label = ttk.Label(params_frame, text='Set Y0 [mm]')
        sety0_label.grid(column=0, row=2, sticky='E', **self._options)

        # y var
        self._sety0 = ttk.Label(params_frame, text=str(self._xy0.y), width=6)
        self._sety0.grid(column=1, row=2, sticky='W', **self._options)

        # set button
        set_button = ttk.Button(params_frame, text='Set XY zero')
        set_button.grid(column=1, row=3, sticky='E', **self._options)
        set_button.configure(command=self._set_button_clicked)

        return params_frame

    # EVENT HANDLERS ----------------------------

    def _set_button_clicked(self):
        """Handle set xy0 button click event"""
        GuiConfigureXy0(self._params_frame, self, self._options, self._xy0)

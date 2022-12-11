import tkinter as tk
from tkinter import ttk

from bin.gui_engrave_configure import *
from bin.machinify_vector import EngraveParams

from bin.persistence import Persistence


class GuiEngraveManager:
    def __init__(self, main, options):
        self._main = main
        self._options = options

        self._z_params = Persistence.load(EngraveParams())

        self._params_frame = self._init_frame_params_section()

    def get_engrave_parameters(self):
        """Getter function.
        :returns an EngraveParams object"""
        return self._z_params

    def set_engrave_parameters(self, params):
        """Setter function.
        to be called by child window to refresh parameters"""
        self._main.update_status('Set EngraveParams')
        self._z_params = params
        self._engrave.config(text=str(self._z_params.z_engrave))
        self._hover.config(text=str(self._z_params.z_hover))
        self._flyover.config(text=str(self._z_params.z_flyover))
        Persistence.save(self._z_params)
        self._main.update_status()

    def _init_frame_params_section(self):
        """create all items within the parameters frame section"""
        params_frame = tk.Frame(bd=5)
        params_frame['relief'] = 'ridge'
        params_frame.grid(column=1, row=2, sticky='W', **self._options)

        # Set XY zero position label
        setxy0_label = tk.Label(params_frame, text='Set Engrave parameters for machining')
        setxy0_label.grid(column=0, row=0, columnspan=2, sticky='W', **self._options)

        # Engrave label
        engrave_label = ttk.Label(params_frame, text='Z-Engrave depth [mm]:')
        engrave_label.grid(column=0, row=1, sticky='E', **self._options)

        # Engrave var
        self._engrave = ttk.Label(params_frame, text=str(self._z_params.z_engrave), width=6)
        self._engrave.grid(column=1, row=1, sticky='W', **self._options)

        # Hover label
        hover_label = ttk.Label(params_frame, text='Z-HoverOver [mm]')
        hover_label.grid(column=0, row=2, sticky='E', **self._options)

        # Hover var
        self._hover = ttk.Label(params_frame, text=str(self._z_params.z_hover), width=6)
        self._hover.grid(column=1, row=2, sticky='W', **self._options)

        # Flyover label
        flyover_label = ttk.Label(params_frame, text='Z-FlyOver [mm]')
        flyover_label.grid(column=0, row=3, sticky='E', **self._options)

        # Flyover var
        self._flyover = ttk.Label(params_frame, text=str(self._z_params.z_flyover), width=6)
        self._flyover.grid(column=1, row=3, sticky='W', **self._options)

        # set button
        set_button = ttk.Button(params_frame, text='Set Parameters')
        set_button.grid(column=1, row=4, sticky='E', **self._options)
        set_button.configure(command=self._set_button_clicked)

        return params_frame

    # EVENT HANDLERS ----------------------------

    def _set_button_clicked(self):
        """Handle set xy0 button click event"""
        GuiEngraveConfigure(self._params_frame, self, self._options, self._z_params)

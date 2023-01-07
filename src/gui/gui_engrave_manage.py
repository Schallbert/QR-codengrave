import tkinter as tk
from tkinter import ttk

from src.gui.gui_engrave_configure import GuiEngraveConfigure
from src.platform.machinify_vector import EngraveParams

from src.helpers.persistence import Persistence


class GuiEngraveManager:
    def __init__(self, main, msgbox, options):
        self._main = main
        self._msgbox = msgbox
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
        self._z_params = params
        self._engrave.config(text=str(self._z_params.z_engrave))
        self._hover.config(text=str(self._z_params.z_hover))
        self._flyover.config(text=str(self._z_params.z_flyover))
        Persistence.save(self._z_params)
        self._main.update_status()

    def _init_frame_params_section(self):
        """create all items within the parameters frame section"""
        params_frame = tk.LabelFrame(bd=5, text='Set Engrave parameters for machining')
        params_frame['relief'] = 'ridge'
        params_frame.grid(column=1, row=1, sticky='NEWS', **self._options)

        # Engrave label
        engrave_label = tk.Label(params_frame, text='Z-Engrave depth [mm]:')
        engrave_label.grid(column=0, row=0, sticky='E', **self._options)

        # Engrave var
        self._engrave = ttk.Label(params_frame, text=str(self._z_params.z_engrave), width=6)
        self._engrave.grid(column=1, row=0, sticky='W', **self._options)
        self._engrave.bind('<Button-1>', lambda click: self._label_clicked())

        # Hover label
        hover_label = tk.Label(params_frame, text='Z-HoverOver [mm]')
        hover_label.grid(column=0, row=1, sticky='E', **self._options)

        # Hover var
        self._hover = ttk.Label(params_frame, text=str(self._z_params.z_hover), width=6)
        self._hover.grid(column=1, row=1, sticky='W', **self._options)
        self._hover.bind('<Button-1>', lambda click: self._label_clicked())

        # Flyover label
        flyover_label = tk.Label(params_frame, text='Z-FlyOver [mm]')
        flyover_label.grid(column=0, row=2, sticky='E', **self._options)

        # Flyover var
        self._flyover = ttk.Label(params_frame, text=str(self._z_params.z_flyover), width=6)
        self._flyover.grid(column=1, row=2, sticky='W', **self._options)
        self._flyover.bind('<Button-1>', lambda click: self._label_clicked())

        return params_frame

    # EVENT HANDLERS ----------------------------

    def _label_clicked(self):
        """Handle label click event"""
        self._main.update_status('Parameter')
        GuiEngraveConfigure(self._params_frame, self, self._msgbox, self._options, self._z_params)

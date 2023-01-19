import tkinter as tk
from tkinter import ttk

from src.gui.gui_xy0_configure import GuiConfigureXy0


class GuiXy0Manager:
    def __init__(self, main, msgbox, params, options):
        self._main = main
        self._msgbox = msgbox
        self._options = options
        self._xy0 = params

        self._is_dimension_info_available = False
        self._guiconfig = GuiConfigureXy0(self, self._msgbox, self._options)

        self._init_frame_params_section()

    def get_xy0_parameters(self):
        """Getter function.
        :returns an XzeroYzero object"""
        return self._xy0

    def set_xy0_parameters(self, xy0):
        """Setter function. To be called by child: configure window"""
        self._xy0 = xy0
        self._setx0.config(text=str(self._xy0.x))
        self._sety0.config(text=str(self._xy0.y))
        self._main.update_status()

    def set_dimension_info(self, dimension_info):
        """Setter function.
        to be called by parent to enable XY0 changes"""
        if dimension_info is None:
            return
        self._is_dimension_info_available = True
        self._guiconfig.set_params(dimension_info[0], dimension_info[1], self._xy0)

    def _init_frame_params_section(self):
        """create all items within the parameters frame section"""
        params_frame = tk.LabelFrame(bd=5, text='Set XY zero relative to QR-code center')
        params_frame['relief'] = 'ridge'
        params_frame.grid(column=1, row=2, sticky='NEWS', **self._options)
        # Center label entries
        params_frame.columnconfigure(0, weight=1)
        params_frame.columnconfigure(3, weight=1)

        # X label
        setx0_label = tk.Label(params_frame, text='Set X0 [mm]')
        setx0_label.grid(column=1, row=0, sticky='E', **self._options)

        # X var
        self._setx0 = ttk.Label(params_frame, text=str(self._xy0.x), width=6)
        self._setx0.grid(column=2, row=0, sticky='W', **self._options)
        self._setx0.bind('<Button-1>', lambda click: self._label_clicked())

        # Y label
        sety0_label = tk.Label(params_frame, text='Set Y0 [mm]')
        sety0_label.grid(column=1, row=1, sticky='E', **self._options)

        # y var
        self._sety0 = ttk.Label(params_frame, text=str(self._xy0.y), width=6)
        self._sety0.grid(column=2, row=1, sticky='W', **self._options)
        self._sety0.bind('<Button-1>', lambda click: self._label_clicked())

        return params_frame

    # EVENT HANDLERS ----------------------------

    def _label_clicked(self):
        """Handle XY0 label click event"""
        if not self._is_dimension_info_available:
            self._msgbox.showinfo(title="QR or Tool not set", message='Warning: QR not provided and/or Tool not set. \n'
                                                                      'Thus XY0 can not be defined.')
            return
        self._guiconfig.show()
        self._main.update_status('Set XY0')


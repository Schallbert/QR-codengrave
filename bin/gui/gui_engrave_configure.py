import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo

from bin.helpers.gui_helpers import validate_number
from bin.platform.machinify_vector import EngraveParams


class GuiEngraveConfigure:
    def __init__(self, main, caller, options, params=None):
        self._main = main
        self._caller = caller
        self._options = options
        self._dialog = tk.Toplevel(main)
        self._dialog.attributes('-topmost', 'true')
        self._dialog.resizable(width=False, height=False)
        self._dialog.geometry('220x172')
        self._dialog.title('Engrave')
        self._dialog.iconbitmap('assets/qruwu.ico')

        if params is not None:
            self._z_params = params
        else:
            self._z_params = EngraveParams()

        self._params_frame = self._init_frame_params_section()

    def get_engrave_parameters(self):
        """Getter function.
        :returns an EngraveParams object"""
        return self._z_params

    def _init_frame_params_section(self):
        """create all items within the parameters frame section"""
        params_frame = tk.Frame(self._dialog, bd=5)
        params_frame['relief'] = 'ridge'
        params_frame.grid(column=0, row=0, sticky='W', **self._options)

        reg = params_frame.register(validate_number)

        # Engrave
        engrave_label = tk.Label(params_frame, text='Z-engrave depth [mm]')
        engrave_label.grid(column=0, row=1, sticky='E', **self._options)

        self._engrave = tk.DoubleVar()
        self._engrave.set(self._z_params.z_engrave)

        engrave_entry = ttk.Entry(params_frame, textvariable=self._engrave, width=5)
        engrave_entry.config(validate="key", validatecommand=(reg, '%P'))
        engrave_entry.grid(column=1, row=1, **self._options)

        # Hover
        hover_label = tk.Label(params_frame, text='Z-hoverOver [mm]')
        hover_label.grid(column=0, row=2, sticky='E', **self._options)

        self._hover = tk.DoubleVar()
        self._hover.set(self._z_params.z_hover)

        hover_entry = ttk.Entry(params_frame, textvariable=self._hover, width=5)
        hover_entry.config(validate="key", validatecommand=(reg, '%P'))
        hover_entry.grid(column=1, row=2, **self._options)

        # Flyover
        flyover_label = tk.Label(params_frame, text='Z-flyOver [mm]')
        flyover_label.grid(column=0, row=3, sticky='E', **self._options)

        self._flyover = tk.IntVar()
        self._flyover.set(self._z_params.z_flyover)

        flyover_entry = ttk.Entry(params_frame, textvariable=self._flyover, width=5)
        flyover_entry.config(validate="key", validatecommand=(reg, '%P'))
        flyover_entry.grid(column=1, row=3, **self._options)

        # Cancel button
        cancel_button = ttk.Button(params_frame, text='Cancel')
        cancel_button.grid(column=0, row=4, sticky='E', **self._options)
        cancel_button.configure(command=self._cancel_button_clicked)

        # OK button
        ok_button = ttk.Button(params_frame, text='OK')
        ok_button.grid(column=1, row=4, sticky='', **self._options)
        ok_button.configure(command=self._ok_button_clicked)

        return params_frame

    def _validate_entries(self):
        """Simple validator method that checks all engraving parameters for correct type.
         In addition, checks hover and flyover heighs against hard-coded constraints"""
        z_safe = EngraveParams()
        try:
            self._engrave.get()
        except tk.TclError:
            showerror(title='Error: Engrave depth', message='Error: invalid input for Engrave Depth. \n'
                                                            'Please update the value.')
            return False
        try:
            if self._hover.get() < z_safe.z_hover:
                raise tk.TclError
        except tk.TclError:
            showinfo('Warning: Hover height', 'Warning: Please make sure your Hover height \n'
                                              'for rapid G00 movement is safe (positive value >' +
                     str(z_safe.z_hover) + 'mm)')
            return False
        try:
            if self._flyover.get() < z_safe.z_flyover:
                raise tk.TclError
        except tk.TclError:
            showinfo('Flyover height low', 'Warning: Please make sure your Flyover height \n'
                                           'for rapid G00 movement is safe (positive value >' +
                     str(z_safe.z_flyover) + 'mm).')
            return False
        return True

    # EVENT HANDLERS ---------------------------

    def _cancel_button_clicked(self):
        """Button callback event handler. Handles cancel button click."""
        self._dialog.destroy()

    def _ok_button_clicked(self):
        """Button callback event handler. Handles OK button click.
        :returns a tool to the main GUI in case all entries have been made OK."""
        if not self._validate_entries():
            return
        self._z_params = EngraveParams(self._engrave.get(), self._hover.get(), self._flyover.get())
        self._caller.set_engrave_parameters(self._z_params)
        self._dialog.destroy()

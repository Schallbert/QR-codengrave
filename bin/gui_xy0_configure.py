import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror

from bin.gui_helpers import validate_number
from bin.vectorize_qr import Point


class GuiConfigureXy0:
    """GUI class that makes a workpiece XY0 offset configuration window."""
    def __init__(self, main, caller, options, tool=None):
        self._caller = caller
        self._options = options
        self._xy0_dialog = tk.Toplevel(main)
        self._xy0_dialog.attributes('-topmost', 'true')
        self._xy0_dialog.geometry('400x600')
        self._xy0_dialog.title('Edit Workpiece XY Zero offset')
        self._xy0_dialog.iconbitmap('../assets/qruwu.ico')

        self._xy0 = Point()

        self.frame = self._create_config_xy0_frame()

    def _create_config_xy0_frame(self):
        """init method that creates the frame with all gui elements"""
        xy0_frame = tk.Frame(self._xy0_dialog, bd=5)
        xy0_frame['relief'] = 'ridge'
        xy0_frame.grid(column=0, row=0, sticky='NW', **self._options)

        reg = xy0_frame.register(validate_number)

        # Set XY zero position label
        setxy0_label = tk.Label(xy0_frame, text='Set X and Y zero relative to QR-code center')
        setxy0_label.grid(column=0, row=0, columnspan=2, sticky='W', **self._options)

        # X label
        setx0_label = ttk.Label(xy0_frame, text='Set X0 [mm]')
        setx0_label.grid(column=0, row=1, sticky='E', **self._options)

        # X var
        self._setx0 = tk.DoubleVar()
        self._setx0.set(self._xy0.x)

        self.setx0_entry = ttk.Entry(xy0_frame, textvariable=self._setx0, width=5)
        self.setx0_entry.config(validate="key", validatecommand=(reg, '%P'))
        self.setx0_entry.grid(column=1, row=1, **self._options)

        # Y label
        sety0_label = ttk.Label(xy0_frame, text='Set Y0 [mm]')
        sety0_label.grid(column=0, row=2, sticky='E', **self._options)

        # y var
        self._sety0 = tk.DoubleVar()
        self._sety0.set(self._xy0.y)

        self.sety0_entry = ttk.Entry(xy0_frame, textvariable=self._sety0, width=5)
        self.sety0_entry.config(validate="key", validatecommand=(reg, '%P'))
        self.sety0_entry.grid(column=1, row=2, **self._options)

        # Cancel button
        cancel_button = ttk.Button(xy0_frame, text='Cancel')
        cancel_button.grid(column=0, row=3, sticky='W', **self._options)
        cancel_button.configure(command=self._cancel_button_clicked)

        # OK button
        ok_button = ttk.Button(xy0_frame, text='OK')
        ok_button.grid(column=2, row=3, sticky='W', **self._options)
        ok_button.configure(command=self._ok_button_clicked)

        return xy0_frame

    def _validate_entries(self):
        """Validates input to the various fields of the tool configure window.
        :returns True in case input looks all right, else False."""
        try:
            self._xy0.x = self._setx0.get()
            self._xy0.y = self._sety0.get()
        except tk.TclError:
            tk.messagebox.showerror('Workpiece Zero Error', 'Error: Invalid value in Workpiece X-zero '
                                                            'or Y-zero offset detected.')
            return False
        return True

    # EVENT HANDLERS ----------------------------

    def _cancel_button_clicked(self):
        """Button callback event handler. Handles cancel button click."""
        self._xy0_dialog.destroy()

    def _ok_button_clicked(self):
        """Button callback event handler. Handles OK button click.
        :returns a tool to the main GUI in case all entries have been made OK."""
        if self._validate_entries():
            self._caller.set_xy0_parameters(self._xy0)
            self._xy0_dialog.destroy()

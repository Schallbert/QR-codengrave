import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror

from bin.gui_helpers import validate_number
from bin.vectorize_qr import Point


class Offset:
    """Enum class associating a DIRECTION on the XY-plane with a number"""
    CENTER = 1
    TOPLEFT = 2
    TOPRIGHT = 3
    BOTTOMLEFT = 4
    BOTTOMRIGHT = 5
    CUSTOM = 6


class GuiConfigureXy0:
    """GUI class that makes a workpiece XY0 offset configuration window."""

    def __init__(self, main, caller, options, qr_dimension, xy0=None):
        self._caller = caller
        self._options = options
        self._qr_dimension = qr_dimension
        self._xy0_dialog = tk.Toplevel(main)
        self._xy0_dialog.attributes('-topmost', 'true')
        self._xy0_dialog.resizable(width=False, height=False)
        self._xy0_dialog.geometry('175x390')
        self._xy0_dialog.title('XY0')
        self._xy0_dialog.iconbitmap('../assets/qruwu.ico')

        if xy0 is None:
            self._xy0 = Point()
        else:
            self._xy0 = xy0

        self.frame = self._create_config_xy0_frame()

    def _create_config_xy0_frame(self):
        """init method that creates the frame with all gui elements"""
        # Radiobutton frame
        rbtn_frame = tk.LabelFrame(self._xy0_dialog, bd=5, text='Choose XY0 offset')
        rbtn_frame['relief'] = 'ridge'
        rbtn_frame.grid(column=0, row=0, sticky='NEW', **self._options)

        # Custom XY0 frame
        xy0_frame = tk.LabelFrame(self._xy0_dialog, bd=5, text='XY0 offset values')
        xy0_frame['relief'] = 'ridge'
        xy0_frame.grid(column=0, row=1, sticky='NE', **self._options)

        reg = xy0_frame.register(validate_number)

        # Radiobuttons
        self._xy_option = tk.IntVar()
        btn_center = tk.Radiobutton(rbtn_frame, text="QR Center", variable=self._xy_option, value=Offset.CENTER,
                                    command=self._radiobutton_selection_changed)
        btn_center.grid(column=0, row=0, sticky='W', **self._options)
        btn_center = tk.Radiobutton(rbtn_frame, text="QR Top-Left", variable=self._xy_option, value=Offset.TOPLEFT,
                                    command=self._radiobutton_selection_changed)
        btn_center.grid(column=0, row=1, sticky='W', **self._options)
        btn_center = tk.Radiobutton(rbtn_frame, text="QR Top-Right", variable=self._xy_option, value=Offset.TOPRIGHT,
                                    command=self._radiobutton_selection_changed)
        btn_center.grid(column=0, row=2, sticky='W', **self._options)
        btn_center = tk.Radiobutton(rbtn_frame, text="QR Bottom-Left", variable=self._xy_option,
                                    value=Offset.BOTTOMLEFT,
                                    command=self._radiobutton_selection_changed)
        btn_center.grid(column=0, row=3, sticky='W', **self._options)
        btn_center = tk.Radiobutton(rbtn_frame, text="QR Bottom-Right", variable=self._xy_option,
                                    value=Offset.BOTTOMRIGHT,
                                    command=self._radiobutton_selection_changed)
        btn_center.grid(column=0, row=4, sticky='W', **self._options)
        btn_center = tk.Radiobutton(rbtn_frame, text="QR Custom", variable=self._xy_option, value=Offset.CUSTOM,
                                    command=self._radiobutton_selection_changed)
        btn_center.grid(column=0, row=5, sticky='W', **self._options)

        # Custom XY0
        # X
        setx0_label = tk.Label(xy0_frame, text='X0 [mm]')
        setx0_label.grid(column=0, row=1, sticky='E', **self._options)

        self._setx0 = tk.DoubleVar()
        self._setx0.set(self._xy0.x)

        self.setx0_entry = ttk.Entry(xy0_frame, textvariable=self._setx0, width=5, state='disabled')
        self.setx0_entry.config(validate="key", validatecommand=(reg, '%P'))
        self.setx0_entry.grid(column=1, row=1, **self._options)

        # Y
        sety0_label = tk.Label(xy0_frame, text='Y0 [mm]')
        sety0_label.grid(column=0, row=2, sticky='E', **self._options)

        self._sety0 = tk.DoubleVar()
        self._sety0.set(self._xy0.y)

        self.sety0_entry = ttk.Entry(xy0_frame, textvariable=self._sety0, width=5, state='disabled')
        self.sety0_entry.config(validate="key", validatecommand=(reg, '%P'))
        self.sety0_entry.grid(column=1, row=2, **self._options)

        # Cancel button
        cancel_button = ttk.Button(xy0_frame, text='Cancel')
        cancel_button.grid(column=0, row=3, sticky='E', **self._options)
        cancel_button.configure(command=self._cancel_button_clicked)

        # OK button
        ok_button = ttk.Button(xy0_frame, text='OK')
        ok_button.grid(column=1, row=3, sticky='W', **self._options)
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

    def _radiobutton_selection_changed(self):
        option = self._xy_option.get()
        if option == Offset.CUSTOM:
            self.setx0_entry.config(state='enabled')
            self.sety0_entry.config(state='enabled')
            return

        self.setx0_entry.config(state='disabled')
        self.sety0_entry.config(state='disabled')
        offset = self._get_xy_offset(option)
        self._setx0.set(offset.x)
        self._sety0.set(offset.y)
        self.setx0_entry.update()
        self.sety0_entry.update()

    def _cancel_button_clicked(self):
        """Button callback event handler. Handles cancel button click."""
        self._xy0_dialog.destroy()

    def _ok_button_clicked(self):
        """Button callback event handler. Handles OK button click.
        :returns a tool to the main GUI in case all entries have been made OK."""
        if self._validate_entries():
            self._caller.set_xy0_parameters(self._xy0)
            self._xy0_dialog.destroy()

    def _get_xy_offset(self, offset):
        qr = self._qr_dimension[0]
        d = self._qr_dimension[1]
        offsets = {Offset.CENTER: Point((d - qr) / 2, (qr - d) / 2),
                   Offset.TOPLEFT: Point(d / 2, -d / 2),
                   Offset.TOPRIGHT: Point(d / 2 - qr, -d / 2),
                   Offset.BOTTOMLEFT: Point(d / 2, qr - d / 2),
                   Offset.BOTTOMRIGHT: Point(d / 2 - qr, qr - d / 2)
                   }

        if offset in offsets:
            return offsets[offset]
        return Point()

import tkinter as tk
from tkinter import ttk

from src.helpers.gui_helpers import validate_number
from src.resources import app_icon_path
from src.platform.machinify_vector import Tool


class GuiConfigureTool:
    """GUI class that makes a tool configuration window."""

    def __init__(self, caller, msgbox, options):
        self._caller = caller
        self._msgbox = msgbox
        self._options = options
        self._dialog = None
        self._tool = Tool()

        self.tool_nr = tk.IntVar()
        self.tool_name = tk.StringVar()
        self.tool_dia = tk.DoubleVar()
        self.tool_xyfeed = tk.IntVar()
        self.tool_speed = tk.IntVar()
        self.tool_zfeed = tk.IntVar()
        self.tool_angle = tk.IntVar()
        self.tool_tip = tk.DoubleVar()
        self.is_tool_tapered = tk.BooleanVar()
        self.set_tool(self._tool)

    def set_tool(self, tool):
        """Setter method. Pre-populates popup dialog's tool value entries
        :param tool A Tool object"""
        self._tool = tool

        self.tool_nr.set(self._tool.number)
        self.tool_name.set(self._tool.name)
        self.tool_dia.set(self._tool.diameter)
        self.tool_xyfeed.set(self._tool.fxy)
        self.tool_zfeed.set(self._tool.fz)
        self.tool_speed.set(self._tool.speed)
        self.tool_tip.set(self._tool.tip)
        self.tool_angle.set(self._tool.angle)
        self.is_tool_tapered.set(self._tool.angle != 0)  # checkbox pre-set when tool is tapered

    def show(self):
        """Prepares and shows the popup dialog"""
        self._dialog = tk.Toplevel()
        self._dialog.attributes('-topmost', 'true')
        self._dialog.resizable(width=False, height=False)
        self._dialog.geometry('570x190')
        self._dialog.title('Add/Edit tool')
        self._dialog.iconbitmap(app_icon_path)
        self._dialog.grab_set()
        self._create_config_tool_frame()

    def _destroy(self):
        """Destroys the popup dialog instance"""
        if self._dialog is not None:
            self._dialog.destroy()
            self._dialog = None

    def _create_config_tool_frame(self):
        """init method that creates the frame with all gui elements"""
        config_tool_frame = tk.Frame(self._dialog, bd=5)
        config_tool_frame['relief'] = 'ridge'
        config_tool_frame.grid(column=0, row=0, sticky='NW', **self._options)
        reg = config_tool_frame.register(validate_number)

        # tool number
        tool_nr_label = tk.Label(config_tool_frame, text='Tool Nr.')
        tool_nr_label.grid(column=0, row=0, **self._options)
        tool_nr_entry = ttk.Entry(config_tool_frame, textvariable=self.tool_nr, width=5)
        tool_nr_entry.grid(column=0, row=1, **self._options)
        tool_nr_entry.config(validate="key", validatecommand=(reg, '%P'))
        tool_nr_entry.focus()

        # tool name
        tool_name_label = tk.Label(config_tool_frame, text='Tool Name')
        tool_name_label.grid(column=1, row=0, **self._options)
        tool_name_entry = ttk.Entry(config_tool_frame, textvariable=self.tool_name)
        tool_name_entry.grid(column=1, row=1, **self._options)

        # tool diameter
        tool_dia_label = tk.Label(config_tool_frame, text='\u2300 [mm]')
        tool_dia_label.grid(column=2, row=0, **self._options)
        tool_dia_entry = ttk.Entry(config_tool_frame, textvariable=self.tool_dia, width=5)
        tool_dia_entry.grid(column=2, row=1, **self._options)
        tool_dia_entry.config(validate="key", validatecommand=(reg, '%P'))

        # tool xy feed
        tool_xyfeed_label = tk.Label(config_tool_frame, text='Fxy\u2192 [mm/min]')
        tool_xyfeed_label.grid(column=3, row=0, **self._options)
        tool_xyfeed_entry = ttk.Entry(config_tool_frame, textvariable=self.tool_xyfeed, width=5)
        tool_xyfeed_entry.grid(column=3, row=1, **self._options)
        tool_xyfeed_entry.config(validate="key", validatecommand=(reg, '%P'))

        # tool z feed
        tool_zfeed_label = tk.Label(config_tool_frame, text='Fz\u2193 [mm/min]')
        tool_zfeed_label.grid(column=4, row=0, **self._options)
        tool_zfeed_entry = ttk.Entry(config_tool_frame, textvariable=self.tool_zfeed, width=5)
        tool_zfeed_entry.grid(column=4, row=1, **self._options)
        tool_zfeed_entry.config(validate="key", validatecommand=(reg, '%P'))

        # tool speed
        tool_speed_label = tk.Label(config_tool_frame, text='S\u2B6E [RPM]')
        tool_speed_label.grid(column=5, row=0, **self._options)
        tool_speed_entry = ttk.Entry(config_tool_frame, textvariable=self.tool_speed, width=5)
        tool_speed_entry.grid(column=5, row=1, **self._options)
        tool_speed_entry.config(validate="key", validatecommand=(reg, '%P'))

        # tool isTapered
        tool_tapered_check = tk.Checkbutton(config_tool_frame, variable=self.is_tool_tapered, onvalue=True,
                                            offvalue=False, text='Tapered tool / V-cut', command=self._checkbox_check)
        tool_tapered_check.grid(column=1, row=4, **self._options)

        # tool taper angle
        self.tool_angle_label = tk.Label(config_tool_frame, text='Angle \u2314 [°]')
        self.tool_angle_entry = ttk.Entry(config_tool_frame, textvariable=self.tool_angle, width=5)
        self.tool_angle_entry.config(validate="key", validatecommand=(reg, '%P'))

        # tool tip width
        self.tool_tip_label = tk.Label(config_tool_frame, text='Tip width [mm]')
        self.tool_tip_entry = ttk.Entry(config_tool_frame, textvariable=self.tool_tip, width=5)
        self.tool_tip_entry.config(validate="key", validatecommand=(reg, '%P'))

        # check if tool angle and tool tip data shall be shown
        self._checkbox_check()

        # Cancel button
        cancel_button = ttk.Button(config_tool_frame, text='Cancel')
        cancel_button.grid(column=4, row=4, sticky='W', **self._options)
        cancel_button.configure(command=self._cancel_button_clicked)

        # OK button
        ok_button = ttk.Button(config_tool_frame, text='OK')
        ok_button.grid(column=5, row=4, sticky='W', **self._options)
        ok_button.configure(command=self._ok_button_clicked)

    def _validate_entries(self):
        """Validates input to the various fields of the tool configure window.
        :returns True in case input looks all right, else False."""
        ok = self._is_tool_number_valid()
        ok &= self._is_tool_diameter_valid()
        ok &= self._is_tool_feedrate_valid()
        ok &= self._is_tool_speed_valid()
        ok &= self._is_tool_tapered_valid()
        return ok

    def _is_tool_number_valid(self):
        """Check tool number for irregularities
        :returns False if an error is found, else True"""
        try:
            number = self.tool_nr.get()
            if (number < 1) or (number > 99):
                raise tk.TclError
        except tk.TclError:
            self._msgbox.showinfo(title='Tool number warning',
                                  message='Info: Tool Number must be a positive integer below 100')
            return False
        return True

    def _is_tool_diameter_valid(self):
        """Check tool diameter for irregularities
        :returns False if an error is found, else True"""
        try:
            if self.tool_dia.get() <= 0:
                raise tk.TclError
        except tk.TclError:
            self._msgbox.showinfo(title='Tool diameter warning',
                                  message='Info: Tool Diameter must be a positive numerical value.')
            return False
        return True

    def _is_tool_feedrate_valid(self):
        """Check tool feedrate for irregularities
        :returns False if an error is found, else True"""
        try:
            if self.tool_xyfeed.get() < 1 or self.tool_zfeed.get() < 1:
                raise tk.TclError
        except tk.TclError:
            self._msgbox.showinfo(title='Tool Feed warning', message='Info: Tool Feed must be a positive integer.')
            return False
        return True

    def _is_tool_speed_valid(self):
        """Check tool speed for irregularities
        :returns False if an error is found, else True"""
        try:
            if self.tool_speed.get() < 1:
                raise tk.TclError
        except tk.TclError:
            self._msgbox.showinfo(title='Tool speed warning', message='Info: Tool Speed must be a positive integer.')
            return False
        return True

    def _is_tool_tapered_valid(self):
        """Check tool taperedness for irregularities
        :returns False if an error is found, else True"""
        if self.is_tool_tapered.get():
            try:
                self.tool_tip.get()
                if (self.tool_angle.get() < 0) or (self.tool_angle.get() > 180):
                    raise tk.TclError
                if self.tool_tip.get() < 0:
                    raise tk.TclError
            except tk.TclError:
                self._msgbox.showinfo(title='Tapered Tool warning',
                                      message='Info: Tool Angle must be a positive integer \n'
                                              'between 1° and 180°.\n'
                                              'Tool tip width must be >= 0.')
                return False
        else:
            # make sure everything is properly zeroed
            self.tool_angle.set(0)
            self.tool_tip.set(0)
        return True

    # EVENT HANDLERS ----------------------------

    def _checkbox_check(self):
        """Checkbox callback event handler. Updates GUI based on checkbox status"""
        if self.is_tool_tapered.get():
            self.tool_angle_label.grid(column=3, row=2, **self._options)
            self.tool_angle_entry.grid(column=3, row=3, **self._options)
            self.tool_tip_label.grid(column=4, row=2, **self._options)
            self.tool_tip_entry.grid(column=4, row=3, **self._options)
        else:
            self.tool_angle_label.grid_remove()
            self.tool_angle_entry.grid_remove()
            self.tool_tip_label.grid_remove()
            self.tool_tip_entry.grid_remove()
            self.tool_angle.set(0)
            self.tool_tip.set(0)

    def _cancel_button_clicked(self):
        """Button callback event handler. Handles cancel button click."""
        self._destroy()

    def _ok_button_clicked(self):
        """Button callback event handler. Handles OK button click.
        :returns a tool to the main GUI in case all entries have been made OK."""
        if not self._validate_entries():
            return
        # tool created using the dialog
        self._tool = Tool(self.tool_nr.get(), self.tool_name.get(), self.tool_dia.get(), self.tool_xyfeed.get(),
                          self.tool_zfeed.get(), self.tool_speed.get(), self.tool_angle.get(), self.tool_tip.get())
        self._caller.add_or_edit_tool(self._tool)
        self._destroy()

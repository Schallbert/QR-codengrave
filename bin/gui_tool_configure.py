import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror

from bin.gui_helpers import validate_number
from bin.machinify_vector import Tool


class GuiConfigureTool:
    """GUI class that makes a tool configuration window."""
    def __init__(self, main, caller, options, tool=None):
        self._caller = caller
        self._options = options
        self._tool_dialog = tk.Toplevel(main)
        self._tool_dialog.attributes('-topmost', 'true')
        self._tool_dialog.resizable(width=False, height=False)
        self._tool_dialog.geometry('530x195')
        self._tool_dialog.title('Add/Edit tool')
        self._tool_dialog.iconbitmap('../assets/qruwu.ico')

        if tool is None:
            self.tool = Tool()
        else:
            self.tool = tool

        self.frame = self._create_config_tool_frame()

    def _create_config_tool_frame(self):
        """init method that creates the frame with all gui elements"""
        config_tool_frame = tk.Frame(self._tool_dialog, bd=5)
        config_tool_frame['relief'] = 'ridge'
        config_tool_frame.grid(column=0, row=0, sticky='NW', **self._options)
        reg = config_tool_frame.register(validate_number)

        # tool number
        tool_nr_label = tk.Label(config_tool_frame, text='Tool Nr.')
        tool_nr_label.grid(column=0, row=0, **self._options)
        self.tool_nr = tk.IntVar()
        self.tool_nr.set(self.tool.number)
        tool_nr_entry = ttk.Entry(config_tool_frame, textvariable=self.tool_nr, width=5)
        tool_nr_entry.grid(column=0, row=1, **self._options)
        tool_nr_entry.config(validate="key", validatecommand=(reg, '%P'))
        tool_nr_entry.focus()

        # tool name
        tool_name_label = tk.Label(config_tool_frame, text='Tool Name')
        tool_name_label.grid(column=1, row=0, **self._options)
        self.tool_name = tk.StringVar()
        self.tool_name.set(self.tool.name)
        tool_name_entry = ttk.Entry(config_tool_frame, textvariable=self.tool_name)
        tool_name_entry.grid(column=1, row=1, **self._options)

        # tool diameter
        tool_dia_label = tk.Label(config_tool_frame, text='\u2300 [mm]')
        tool_dia_label.grid(column=2, row=0, **self._options)
        self.tool_dia = tk.DoubleVar()
        self.tool_dia.set(self.tool.diameter)
        tool_dia_entry = ttk.Entry(config_tool_frame, textvariable=self.tool_dia, width=5)
        tool_dia_entry.grid(column=2, row=1, **self._options)
        tool_dia_entry.config(validate="key", validatecommand=(reg, '%P'))

        # tool xy feed
        tool_xyfeed_label = tk.Label(config_tool_frame, text='Fxy\u2192 [mm/min]')
        tool_xyfeed_label.grid(column=3, row=0, **self._options)
        self.tool_xyfeed = tk.IntVar()
        self.tool_xyfeed.set(self.tool.fxy)
        tool_xyfeed_entry = ttk.Entry(config_tool_frame, textvariable=self.tool_xyfeed, width=5)
        tool_xyfeed_entry.grid(column=3, row=1, **self._options)
        tool_xyfeed_entry.config(validate="key", validatecommand=(reg, '%P'))

        # tool z feed
        tool_zfeed_label = tk.Label(config_tool_frame, text='Fz\u2193 [mm/min]')
        tool_zfeed_label.grid(column=4, row=0, **self._options)
        self.tool_zfeed = tk.IntVar()
        self.tool_zfeed.set(self.tool.fz)
        tool_zfeed_entry = ttk.Entry(config_tool_frame, textvariable=self.tool_zfeed, width=5)
        tool_zfeed_entry.grid(column=4, row=1, **self._options)
        tool_zfeed_entry.config(validate="key", validatecommand=(reg, '%P'))

        # tool speed
        tool_speed_label = tk.Label(config_tool_frame, text='S\u2B6E [RPM]')
        tool_speed_label.grid(column=5, row=0, **self._options)
        self.tool_speed = tk.IntVar()
        self.tool_speed.set(self.tool.speed)
        tool_speed_entry = ttk.Entry(config_tool_frame, textvariable=self.tool_speed, width=5)
        tool_speed_entry.grid(column=5, row=1, **self._options)
        tool_speed_entry.config(validate="key", validatecommand=(reg, '%P'))

        # tool isTapered
        self.is_tool_tapered = tk.BooleanVar()
        self.is_tool_tapered.set(self.tool.angle != 0)  # checkbox pre-set when tool is tapered
        tool_tapered_check = tk.Checkbutton(config_tool_frame, variable=self.is_tool_tapered, onvalue=True,
                                             offvalue=False, text='Tapered tool / V-cut', command=self._checkbox_check)
        tool_tapered_check.grid(column=1, row=4, **self._options)

        # tool taper angle
        self.tool_angle_label = tk.Label(config_tool_frame, text='Angle \u2314 [°]')
        self.tool_angle = tk.IntVar()
        self.tool_angle.set(self.tool.angle)
        self.tool_angle_entry = ttk.Entry(config_tool_frame, textvariable=self.tool_angle, width=5)
        self.tool_angle_entry.config(validate="key", validatecommand=(reg, '%P'))

        # tool tip width
        self.tool_tip_label = tk.Label(config_tool_frame, text='Tip width [mm]')
        self.tool_tip = tk.DoubleVar()
        self.tool_tip.set(self.tool.tip)
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

        return config_tool_frame

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

    def _validate_entries(self):
        """Validates input to the various fields of the tool configure window.
        :returns True in case input looks all right, else False."""
        try:
            if self.tool_nr.get() < 1:
                raise tk.TclError
        except tk.TclError:
            tk.messagebox.showinfo('Tool number warning', 'Info: Tool Number must be a positive integer.')
            return False
        try:
            if self.tool_dia.get() <= 0:
                raise tk.TclError
        except tk.TclError:
            tk.messagebox.showinfo('Tool diameter warning', 'Info: Tool Diameter must be a positive numerical value.')
            return False
        try:
            if self.tool_xyfeed.get() < 1 or self.tool_zfeed.get() < 1:
                raise tk.TclError
        except tk.TclError:
            tk.messagebox.showinfo('Tool Feed warning', 'Info: Tool Feed must be a positive integer.')
            return False
        try:
            if self.tool_speed.get() < 1:
                raise tk.TclError
        except tk.TclError:
            tk.messagebox.showinfo('Tool speed warning', 'Info: Tool Speed must be a positive integer.')
            return False
        if self.is_tool_tapered.get():
            try:
                self.tool_tip.get()
                if not ((self.tool_angle.get() > 0) and (self.tool_angle.get() < 180)):
                    raise tk.TclError
            except tk.TclError:
                tk.messagebox.showinfo('Tapered Tool warning', 'Info: Tool Angle must be a positive integer \n'
                                                               'between 1° and 180°.\n'
                                                               'Tool tip width must be a positive value.')
                return False
        else:
            # make sure everything is properly zeroed
            self.tool_angle.set(0)
            self.tool_tip.set(0)
        return True

    def _cancel_button_clicked(self):
        """Button callback event handler. Handles cancel button click."""
        self._tool_dialog.destroy()

    def _ok_button_clicked(self):
        """Button callback event handler. Handles OK button click.
        :returns a tool to the main GUI in case all entries have been made OK."""
        if not self._validate_entries():
            return
        # tool created using the dialog
        self.tool = Tool(self.tool_nr.get(), self.tool_name.get(), self.tool_dia.get(), self.tool_xyfeed.get(),
                         self.tool_zfeed.get(), self.tool_speed.get(), self.tool_angle.get(), self.tool_tip.get())
        self._caller.add_or_edit_tool(self.tool)
        self._tool_dialog.destroy()

import tkinter as tk
from tkinter import ttk


class ConfigureTool:
    def __init__(self, master, options):
        self.options = options
        self.add_tool = tk.Toplevel(master)
        self.add_tool.geometry('627x180')
        self.add_tool.title('Add tool')

        frame = self._create_add_tool_frame()

    def _create_add_tool_frame(self):
        add_tool_frame = tk.Frame(self.add_tool, bd=5)
        add_tool_frame['relief'] = 'ridge'
        add_tool_frame.grid(column=0, row=0, sticky='W', **self.options)

        # tool number
        tool_nr_label = ttk.Label(add_tool_frame, text='Tool Nr.')
        tool_nr_label.grid(column=0, row=0, **self.options)
        self.tool_nr = tk.IntVar(0)
        tool_nr_entry = ttk.Entry(add_tool_frame, textvariable=self.tool_nr, width=5)
        tool_nr_entry.grid(column=0, row=1, **self.options)
        tool_nr_entry.focus()

        # tool name
        tool_name_label = ttk.Label(add_tool_frame, text='Tool Name')
        tool_name_label.grid(column=1, row=0, **self.options)
        self.tool_name = tk.StringVar()
        tool_name_entry = ttk.Entry(add_tool_frame, textvariable=self.tool_name)
        tool_name_entry.grid(column=1, row=1, **self.options)

        # tool diameter
        tool_dia_label = ttk.Label(add_tool_frame, text='\u2300 [mm]')
        tool_dia_label.grid(column=2, row=0, **self.options)
        self.tool_dia = tk.IntVar()
        tool_dia_entry = ttk.Entry(add_tool_frame, textvariable=self.tool_dia, width=5)
        tool_dia_entry.grid(column=2, row=1, **self.options)

        # tool xy feed
        tool_xyfeed_label = ttk.Label(add_tool_frame, text='Fxy\u2192 [mm/min]')
        tool_xyfeed_label.grid(column=3, row=0, **self.options)
        self.tool_xyfeed = tk.IntVar()
        tool_xyfeed_entry = ttk.Entry(add_tool_frame, textvariable=self.tool_xyfeed, width=5)
        tool_xyfeed_entry.grid(column=3, row=1, **self.options)

        # tool z feed
        tool_zfeed_label = ttk.Label(add_tool_frame, text='Fz\u2193 [mm/min]')
        tool_zfeed_label.grid(column=4, row=0, **self.options)
        self.tool_zfeed = tk.IntVar()
        tool_zfeed_entry = ttk.Entry(add_tool_frame, textvariable=self.tool_zfeed, width=5)
        tool_zfeed_entry.grid(column=4, row=1, **self.options)

        # tool speed
        tool_speed_label = ttk.Label(add_tool_frame, text='S\u2B6E [RPM]')
        tool_speed_label.grid(column=5, row=0, **self.options)
        self.tool_speed = tk.IntVar()
        tool_speed_entry = ttk.Entry(add_tool_frame, textvariable=self.tool_speed, width=5)
        tool_speed_entry.grid(column=5, row=1, **self.options)

        # tool isTapered
        self.is_tool_tapered = tk.BooleanVar(False)
        tool_tapered_check = ttk.Checkbutton(add_tool_frame, variable=self.is_tool_tapered, onvalue=True,
                                             offvalue=False, text='Tapered tool / V-cut', command=self._checkbox_check)
        tool_tapered_check.grid(column=1, row=4, **self.options)

        # tool taper angle
        self.tool_angle_label = ttk.Label(add_tool_frame, text='Angle \u2314 [°]')
        self.tool_angle = tk.IntVar()
        self.tool_angle_entry = ttk.Entry(add_tool_frame, textvariable=self.tool_angle, width=5)

        # tool tip width
        self.tool_tip_label = ttk.Label(add_tool_frame, text='Tip width [mm]')
        self.tool_tip = tk.IntVar()
        self.tool_tip_entry = ttk.Entry(add_tool_frame, textvariable=self.tool_tip, width=5)

        # Cancel button
        ok_button = ttk.Button(add_tool_frame, text='Cancel')
        ok_button.grid(column=4, row=4, sticky='W', **self.options)
        ok_button.configure(command=self._cancel_button_clicked)

        # OK button
        ok_button = ttk.Button(add_tool_frame, text='OK')
        ok_button.grid(column=5, row=4, sticky='W', **self.options)
        ok_button.configure(command=self._ok_button_clicked)

        return add_tool_frame

    def _checkbox_check(self):
        if self.is_tool_tapered.get():
            self.tool_angle_label.grid(column=3, row=2, **self.options)
            self.tool_angle_entry.grid(column=3, row=3, **self.options)
            self.tool_tip_label.grid(column=4, row=2, **self.options)
            self.tool_tip_entry.grid(column=4, row=3, **self.options)
        else:
            self.tool_angle_label.grid_remove()
            self.tool_angle_entry.grid_remove()
            self.tool_tip_label.grid_remove()
            self.tool_tip_entry.grid_remove()
            self.tool_angle.set(0)
            self.tool_tip.set(0)

    def _cancel_button_clicked(self):
        self.add_tool.destroy()

    def _ok_button_clicked(self):
        self.add_tool.destroy()
import tkinter as tk
from tkinter import ttk

from bin.gui_tool_configure import GuiConfigureTool
from bin.gui_tool_configure import validate_number

from bin.machinify_vector import ToolList, EngraveParams
from bin.persistence import Persistence


class GuiToolManager:
    def __init__(self, root, options):
        """displays the tool handling section within the main gui window"""
        self.root = root
        self.options = options

        self._tool_list = Persistence.load(ToolList())
        self._z_params = Persistence.load(EngraveParams())

        self._tool_frame = self._init_frame_tool_section()

    def add_or_edit_tool(self, tool):
        """callback handler for tool window to return data into main window"""
        self._tool_list.add_or_update(tool)
        self._update_tool_options()
        Persistence.save(self._tool_list)

    def _init_frame_tool_section(self):
        """creates all items within the tool selection frame"""
        tool_section_frame = tk.Frame(bd=5)
        tool_section_frame['relief'] = 'ridge'
        tool_section_frame.grid(column=2, row=1, sticky='W', **self.options)
        reg = tool_section_frame.register(validate_number)

        # Add Tool
        add_tool_button = ttk.Button(tool_section_frame, text='Add/Edit tool')
        add_tool_button.grid(column=1, row=0, sticky='W', **self.options)
        add_tool_button.configure(command=self._add_tool_button_clicked)

        # Remove Tool
        remove_tool_button = ttk.Button(tool_section_frame, text='Remove tool')
        remove_tool_button.grid(column=2, row=0, sticky='W', **self.options)
        remove_tool_button.configure(command=self._remove_tool_button_clicked)

        # Select Tool
        select_tool_label = ttk.Label(tool_section_frame, text='Select tool')
        select_tool_label.grid(column=0, row=1, sticky='E', **self.options)

        self.tool_selection = tk.StringVar()
        self.tool_selection.trace('u', self._tool_selection_changed)
        self.tool_selection.set(self._tool_list.get_selected_tool_description())

        self.tool_dropdown = ttk.OptionMenu(tool_section_frame, self.tool_selection,
                                            *self._tool_list.get_tool_list_string())
        self.tool_dropdown.config(width=30)
        self.tool_dropdown.grid(column=0, row=2, columnspan=3, sticky='W', **self.options)

        # Engrave
        engrave_label = ttk.Label(tool_section_frame, text='Z-engrave depth [mm]')
        engrave_label.grid(column=0, row=3, columnspan=2, sticky='E', **self.options)

        self._engrave = tk.DoubleVar()
        self._engrave.set(self._z_params.get_engrave_depth())

        engrave_entry = ttk.Entry(tool_section_frame, textvariable=self._engrave, width=5)
        engrave_entry.config(validate="key", validatecommand=(reg, '%P'))
        engrave_entry.grid(column=2, row=3, **self.options)
        self._engrave.trace('u', self._engrave_changed)

        # Hover
        hover_label = ttk.Label(tool_section_frame, text='Z-hoverOver [mm]')
        hover_label.grid(column=0, row=4, columnspan=2, sticky='E', **self.options)

        self._hover = tk.DoubleVar()
        self._hover.set(self._z_params.get_hover())

        hover_entry = ttk.Entry(tool_section_frame, textvariable=self._hover, width=5)
        hover_entry.config(validate="key", validatecommand=(reg, '%P'))
        hover_entry.grid(column=2, row=4, **self.options)
        self._hover.trace('u', self._hover_changed())   # following error with 'w': "NoneType Object is not Callable

        # Flyover
        flyover_label = ttk.Label(tool_section_frame, text='Z-flyOver [mm]')
        flyover_label.grid(column=0, row=5, columnspan=2, sticky='E', **self.options)

        self._flyover = tk.IntVar()
        self._flyover.set(self._z_params.get_flyover())

        flyover_entry = ttk.Entry(tool_section_frame, textvariable=self._flyover, width=5)
        flyover_entry.config(validate="key", validatecommand=(reg, '%P'))
        flyover_entry.grid(column=2, row=5, **self.options)
        self._flyover.trace('u', self._flyover_changed())

        return tool_section_frame

    def _update_tool_options(self):
        """callback handler for updating the tool dropdown box"""
        menu = self.tool_dropdown['menu']
        menu.delete(0, 'end')
        options_update = self._tool_list.get_tool_list_string()
        for entry in options_update:
            menu.add_command(label=entry,
                             command=lambda value=entry: self.tool_selection.set(value))

    def _tool_selection_get_to_int(self):
        """helper method to get a tool number from a tool description string
        :returns integer value of corresponding tool number"""
        value = self.tool_selection.get().split('_')[0]
        try:
            int_value = int(value)
            return int_value
        except ValueError:
            #  e.g. when selection is None
            return 0

    # EVENT HANDLERS ----------------------------

    def _add_tool_button_clicked(self):
        """Handle add tool button click event"""
        if self._tool_list.is_tool_in_list(self._tool_selection_get_to_int()):
            GuiConfigureTool(self.root, self, self.options, self._tool_list.get_selected_tool())
        else:
            GuiConfigureTool(self.root, self, self.options)

    def _remove_tool_button_clicked(self):
        """Handle add tool button click event"""
        remove = self._tool_selection_get_to_int()
        if remove == 0:
            return
        self._tool_list.remove(remove)
        self._tool_list.select_tool(None)
        self.tool_selection.set(None)
        Persistence.save(self._tool_list)
        self._update_tool_options()

    def _tool_selection_changed(self, *args):
        """Handle option box for tool selection changed event"""
        tool_number = self._tool_selection_get_to_int()
        self._tool_list.select_tool(tool_number)
        print('DEBUG: tool selection changed to: ' + str(tool_number))
        Persistence.save(self._tool_list)

    def _engrave_changed(self, *args):
        """Event handler for engrave entry change event
        Is able to display a warning when high engrave depth is selected"""
        try:
            self._engrave.get()
        except tk.TclError:
            self._engrave.set(self._z_params.get_engrave_depth())
        self._z_params.set_engrave_depth(self._engrave.get())

    def _hover_changed(self, *args):
        """Event handler for hover entry change event"""
        try:
            self._hover.get()
        except tk.TclError:
            self._hover.set(self._z_params.get_hover())
        self._z_params.set_hover(self._hover.get())

    def _flyover_changed(self, *args):
        """Event handler for flyover entry change event"""
        try:
            self._flyover.get()
        except tk.TclError:
            self._flyover.set(self._z_params.get_flyover())
        self._z_params.set_hover(self._flyover.get())

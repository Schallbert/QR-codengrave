import tkinter as tk
from tkinter import ttk

from bin.gui_tool_configure import ConfigureTool

from bin.machinify_vector import ToolList
from bin.persistence import Persistence


class ToolManager:
    def __init__(self, root, options):
        """displays the tool handling section within the main gui window"""
        self.root = root
        self.options = options

        self._tool_list = Persistence.load(ToolList())
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
        tool_section_frame.grid(column=3, row=1, sticky='N', **self.options)

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
        select_tool_label.grid(column=1, row=1, sticky='E', **self.options)
        self.tool_selection = tk.StringVar()
        self.tool_selection.trace('w', self._tool_selection_changed)
        self.tool_selection.set(self._tool_list.get_selected_tool_description())

        print('DEBUG: tool selection value: ' + self.tool_selection.get())
        self.tool_dropdown = ttk.OptionMenu(tool_section_frame, self.tool_selection,
                                            *self._tool_list.get_tool_list_string())
        self.tool_dropdown.grid(column=2, row=1, columnspan=3, sticky='W', **self.options)

        return tool_section_frame

    def _add_tool_button_clicked(self):
        """Handle add tool button click event"""
        if self._tool_list.is_tool_in_list(self._tool_selection_get_to_int()):
            ConfigureTool(self.root, self, self.options, self._tool_list.get_selected_tool())
        else:
            ConfigureTool(self.root, self, self.options)

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

import tkinter as tk
from tkinter import ttk

from src.gui.gui_tool_configure import GuiConfigureTool

from src.platform.machinify_vector import ToolList


class GuiToolManager:
    def __init__(self, main, msgbox, params, options):
        """displays the tool handling section within the main gui window"""
        self._main = main
        self._msgbox = msgbox
        self._options = options
        self._tool_list = params

        self._config_gui = GuiConfigureTool(self,
                                            self._msgbox,
                                            self._options)

        self._tool_frame = self._init_frame_tool_section()

    def add_or_edit_tool(self, tool):
        """callback handler for tool window to return data into main window"""
        self._tool_list.add_or_update(tool)
        self._update_tool_options()
        self._main.update_status()

    def get_selected_tool(self):
        """Getter function.
        :returns the currently selected tool"""
        return self._tool_list.get_selected_tool()

    def get_tool_list(self):
        """Getter function.
        :returns the tool list"""
        return self._tool_list

    def _init_frame_tool_section(self):
        """creates all items within the tool selection frame"""
        tool_section_frame = tk.LabelFrame(bd=5, text='Select Tool')
        tool_section_frame['relief'] = 'ridge'
        tool_section_frame.grid(column=1, row=0, rowspan=1, sticky='NWSE', **self._options)

        # Add Tool
        add_tool_button = ttk.Button(tool_section_frame, text='Add/Edit tool')
        add_tool_button.grid(column=1, row=0, sticky='W', **self._options)
        add_tool_button.configure(command=self._add_tool_button_clicked)

        # Remove Tool
        remove_tool_button = ttk.Button(tool_section_frame, text='Remove tool')
        remove_tool_button.grid(column=2, row=0, sticky='W', **self._options)
        remove_tool_button.configure(command=self._remove_tool_button_clicked)

        # Select Tool OptionMenu
        self.tool_selection = tk.StringVar()
        self.tool_selection.set(self._tool_list.get_selected_tool_description())

        self.tool_dropdown = ttk.OptionMenu(tool_section_frame, self.tool_selection,
                                            *self._tool_list.get_tool_list_string())
        self.tool_dropdown.config(width=30)
        self.tool_dropdown.grid(column=1, row=1, columnspan=2, sticky='S', **self._options)
        self.tool_selection.trace('w', self._tool_selection_changed)

        return tool_section_frame

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

    def _update_tool_options(self):
        """callback handler for updating the tool dropdown box.
        Basically this method redraws the contents of the dropdown with latest data"""
        menu = self.tool_dropdown['menu']
        menu.delete(0, 'end')
        options_update = self._tool_list.get_tool_list_string()
        for entry in options_update:
            menu.add_command(label=entry,
                             command=lambda value=entry: self.tool_selection.set(value))

    def _add_tool_button_clicked(self):
        """Handle add tool button click event"""
        self._main.update_status('\u27f1 Tool')
        if self._tool_list.is_tool_in_list(self._tool_selection_get_to_int()):
            self._config_gui.set_tool(self._tool_list.get_selected_tool())
        self._config_gui.show()

    def _remove_tool_button_clicked(self):
        """Handle add tool button click event"""
        remove = self._tool_selection_get_to_int()
        if remove == 0:
            return
        self._tool_list.remove(remove)
        self._tool_list.select_tool(None)
        self.tool_selection.set(None)
        self._update_tool_options()

    def _tool_selection_changed(self, *args):
        """Handle option box for tool selection changed event"""
        tool_number = self._tool_selection_get_to_int()
        self._tool_list.select_tool(tool_number)
        self._update_tool_options()  # Call this to not have disappearing entries in List
        self._main.update_status()

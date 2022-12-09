

class Tool:
    """POD container class representing a tool."""
    def __init__(self, number, name, dia, fxy, fz, s, angle=0, tip=0):
        self.number = number
        self.name = name
        self.diameter = dia
        self.fxy = fxy
        self.fz = fz
        self.speed = s
        self.angle = angle
        self.tip = tip

    def get_description(self):
        """Helper method that generates a short tool description from number, name and diameter
        :returns the tool description string"""
        return str(self.number) + '_' + self.name + '_' + str(self.diameter) + 'mm'


class ToolList:
    """A class that represents a list of tools in form of a dictionary.
    Features some helper methods and maintains the selected tool"""
    def __init__(self):
        self.tools = dict()
        self.selected_tool = None

    def add_or_update(self, tool):
        """Adds or updates a tool's values in the list"""
        self.tools.update({tool.number: tool})

    def remove(self, key):
        """Removes a tool from the list when found"""
        if key in self.tools:
            self.tools.pop(key)

    def select_tool(self, key):
        """Selects a tool when found"""
        if key in self.tools:
            self.selected_tool = self.tools.get(key)

    def get_selected_tool(self):
        """Getter method.
        :returns the selected tool"""
        return self.selected_tool

    def get_tool_list_string(self):
        """Compiles a sorted list of tools.
        :returns a list of tool descriptions."""
        tools_list = list()
        for key in sorted(self.tools.keys()):
            tools_list.append(self.tools.get(key).get_description())
        return tools_list

    def is_tool_in_list(self, key):
        """Checks if the requested tool is in the list
        :returns that tool's number"""
        return key in self.tools

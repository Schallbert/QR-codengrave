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
        if self.number < 10:
            numberstr = '0' + str(self.number)
        else:
            numberstr = str(self.number)
        return numberstr + '_' + self.name + '_' + str(self.diameter) + 'mm'


class ToolList:
    """A class that represents a list of tools in form of a dictionary.
    Features some helper methods and maintains the selected tool"""

    def __init__(self):
        self._tools = dict()
        self._selected_tool = None

    def add_or_update(self, tool):
        """Adds or updates a tool's values in the list"""
        self._tools.update({tool.number: tool})

    def remove(self, key):
        """Removes a tool from the list when found"""
        if key in self._tools:
            self._tools.pop(key)

    def select_tool(self, key):
        """Selects a tool when found"""
        if key in self._tools:
            self._selected_tool = self._tools.get(key)
        else:
            self._selected_tool = None

    def get_selected_tool(self):
        """Getter method.
        :returns the selected tool"""
        return self._selected_tool

    def get_selected_tool_description(self):
        """Getter method.
        :returns the selected tool's description string or None when no tool is selected."""
        if self._selected_tool is not None:
            return self._selected_tool.get_description()
        return 'None'

    def get_tool_list_string(self):
        """Compiles a sorted list of tools.
        :returns a list of tool descriptions."""
        tools_list = list()
        for key in sorted(self._tools.keys()):
            tools_list.append(self._tools.get(key).get_description())
        return tools_list

    def is_tool_in_list(self, key):
        """Checks if the requested tool is in the list
        :returns that tool's number"""
        return key in self._tools


class EngraveParams:
    def __init__(self):
        """POD container class representing Z axis data for G01 engraving, G00 hover, G00 flyover commands"""
        self._z_flyover = 15
        self._z_hover = 1
        self._z_engrave = 0.4  # this value will actually be negative because it's below workpiece surface

    def set_flyover(self, flyover):
        self._z_flyover = flyover

    def set_hover(self, hover):
        self._z_hover = hover

    def set_engrave_depth(self, engrave):
        self._z_engrave = engrave

    def get_flyover(self):
        return self._z_flyover

    def get_hover(self):
        return self._z_hover

    def get_engrave_depth(self):
        return self._z_engrave

from bin.vectorize_qr import Point, QrCode


class Tool:
    """POD container class representing a tool."""
    def __init__(self, number=1, name='Name', dia=3.18, fxy=1000, fz=500, s=24000, angle=90, tip=0.1):
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
        if not self._tools:
            #  tool list empty. Enter a dummy tool here so OptionMenu item won't throw
            self.add_or_update(Tool())

        for key in sorted(self._tools.keys()):
            tools_list.append(self._tools.get(key).get_description())
        return tools_list

    def is_tool_in_list(self, key):
        """Checks if the requested tool is in the list
        :returns that tool's number"""
        return key in self._tools


class EngraveParams:
    def __init__(self, engrave=0.4, hover=0.5, flyover=5):
        """POD container class representing Z axis data for G01 engraving, G00 hover, G00 flyover commands"""
        self.z_flyover = flyover
        self.z_hover = hover
        self.z_engrave = engrave  # this value will actually be negative because it's below workpiece surface

class MachinifyVector:
    def __init__(self):
        self._qr_path = None
        self._tool = None
        self._engrave_params = None
        self._xy_zero = None

        self._time_buffer = 1

    def report_data_missing(self):
        if self._qr_path is None:
            return 'QR-code data'
        if self._tool is None:
            return 'Tool data'
        if self._engrave_params is None:
            return 'Engrave parameters'
        if self._xy_zero is None:
            return 'XY Zero offsets'
        return ''

    def set_qr_path(self, path):
        self._qr_path = path

    def set_tool(self, tool):
        self._tool = tool

    def set_engrave_params(self, engraveparams):
        self._engrave_params = engraveparams

    def set_xy_zero(self, xy_zero):
        self._xy_zero = xy_zero

    def get_job_duration_sec(self):
        count_z_moves = 0

        for path in self._qr_path:
            count_z_moves += len(path.get_z_vector())

        xy_moves_mm = self._get_xy_move_per_step() * self._qr_path[0].get_xy_line().get_abs_length() ** 2
        z_moves_mm = count_z_moves * (self._engrave_params.z_hover + self._engrave_params.z_engrave)

        xy_moves_sec = xy_moves_mm / self._tool.fxy * 60 * self._time_buffer
        z_moves_sec = z_moves_mm / self._tool.fz * 60 * self._time_buffer

        return xy_moves_sec + z_moves_sec

    def get_dimension_info(self):
        return tuple((self._get_xy_move_per_step() * self._qr_path[0].get_xy_line().get_abs_length(),
                      self._get_xy_move_per_step()))

    def generate_gcode(self):
        print('x0 = ' + str(self._xy_zero.x) + ' y0 = ' + str(self._xy_zero.y))
        print('engrave = ' + str(self._engrave_params.z_engrave) + ' hover = ' + str(self._engrave_params.z_hover) +
              ' flyover = ' + str(self._engrave_params.z_flyover))

    def _get_xy_move_per_step(self):
        if self._tool.tip > 0:
            return self._tool.tip
        else:
            return self._tool.diameter

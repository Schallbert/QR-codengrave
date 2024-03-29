from io import StringIO
from math import sqrt, tan, pi
from datetime import timedelta

from src.platform.vectorize_helper import Point


class Tool:
    """POD container class representing a tool."""

    def __init__(self, number=1, name='Default', dia=2, fxy=1000, fz=500, s=24000, angle=0, tip=0):
        self.number = number
        self.name = name
        self.diameter = dia
        self.fxy = fxy
        self.fz = fz
        self.speed = s
        self.angle = angle
        self.tip = tip

    def __eq__(self, other):
        eq = (self.number == other.number)
        eq &= (self.name == other.name)
        eq &= (self.diameter == other.diameter)
        eq &= (self.fxy == other.fxy)
        eq &= (self.fz == other.fz)
        eq &= (self.speed == other.speed)
        eq &= (self.angle == other.angle)
        eq &= (self.tip == other.tip)
        return eq

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
        if self._selected_tool is None:
            return 'None'
        return self._selected_tool.get_description()

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

    def __eq__(self, other):
        eq = (self.z_flyover == other.z_flyover)
        eq &= (self.z_hover == other.z_hover)
        eq &= (self.z_engrave == other.z_engrave)
        return eq


class MachinifyVector:
    """Class that processes QR-code path data, tool data, engrave depth data, and Workpiece zero coordinates
    to create a CNC machine readable file containing G-code instructions."""

    def __init__(self, version):
        self._version = version

        self._qr_path = None  # List of LinePath objects
        self._tool = None  # Selected Tool
        self._engrave_params = None  # Z-information for engraving
        self._xy_zero = None  # XY0-offset

        self._project_name = ''
        self._job_duration = timedelta(0)
        self._state = False  # current Z state (True = engraving)
        self._time_buffer = 1.6

    def report_data_missing(self):
        """Reports to GUI in case there's data missing so that G-code cannot be generated.
        :returns a String object that contains info about what's missing,
        or an empty string when everything has been provided."""
        if self._qr_path is None:
            return 'QR-code data'
        if self._tool is None:
            return 'Tool data'
        if self._engrave_params is None:
            return 'Engrave parameters'
        if self._xy_zero is None:
            return 'XY Zero offsets'
        return ''

    def set_project_name(self, text):
        """Setter function. Used for default file naming
        :param text the text to be stored"""
        text = text.replace('https:', '')
        text = text.replace('www.', '')
        text = text.replace('/', '')
        text = text.replace('.', '_')
        if len(text) > 25:
            text = text[0:25]
        self._project_name = text

    def get_project_name(self):
        """Getter function.
        :returns the project name"""
        return self._project_name

    def set_qr_path(self, path):
        """Setter function.
        :param path: a list of QrPathSegment objects"""
        self._qr_path = path

    def set_tool(self, tool):
        """Setter function.
        :param tool: a Tool POD object"""
        self._tool = tool

    def set_engrave_params(self, engraveparams):
        """Setter function.
        :param engraveparams: an EngraveParams POD object"""
        self._engrave_params = engraveparams

    def set_xy_zero(self, xy_zero):
        """Setter function.
        :param xy_zero: a Point POD object"""
        self._xy_zero = xy_zero

    def get_job_duration_sec(self):
        """Calculates the estimated job duration for an engrave path set.
        :returns _job_duration: a timedelta object representing seconds."""
        if self._qr_path is None or self._tool is None:
            return timedelta(0)
        vect = self._qr_path.get_vectors()
        count_z_moves = 2 * len(vect)

        xy_moves_mm = 0
        pos = Point()
        x_length_last = 0
        y_length_last = 0
        for v in vect:
            xy_moves_mm += abs(v.x_length + v.y_length) + \
                           sqrt(abs(v.position.x - (pos.x + x_length_last)) ** 2 +
                                abs(v.position.y - (pos.y + y_length_last)) ** 2)
            pos = v.position
            x_length_last = v.x_length
            y_length_last = v.y_length

        xy_moves_mm *= self._get_xy_move_per_step()
        z_moves_mm = count_z_moves * (self._engrave_params.z_hover + self._engrave_params.z_engrave)

        xy_moves_sec = xy_moves_mm / self._tool.fxy * 60 * self._time_buffer
        z_moves_sec = z_moves_mm / self._tool.fz * 60 * self._time_buffer

        self._job_duration = timedelta(seconds=xy_moves_sec + z_moves_sec)
        self._job_duration -= timedelta(microseconds=self._job_duration.microseconds)
        return self._job_duration

    def get_dimension_info(self):
        """Getter function.
        :returns tuple: returns a tuple of QR engrave dimension and engrave bit size"""
        if self._qr_path is None or self._tool is None:
            return tuple((0, 0))
        return tuple((self._get_xy_move_per_step() * self._qr_path.get_size(),
                      self._get_xy_move_per_step()))

    def generate_gcode(self):
        """Calls G-code boilerplate methods and the engrave method that converts a path into CNC-readable commands.
        :returns gcode: a StringIO object that can be saved to a file."""
        gcode = StringIO()
        gcode.write(self._gcode_header())
        gcode.write(self._gcode_prepare())
        gcode.write(self._gcode_engrave())
        gcode.write(self._gcode_finalize())
        return gcode

    def _get_xy_move_per_step(self):
        """Helper method.
        :returns float: a value representing the tool diameter relevant for engraving."""
        if self._tool.angle > 0:
            tan_angle = tan(self._tool.angle / 360 * pi)  # value range 0 and 1
            dia = self._tool.tip + 2 * self._engrave_params.z_engrave * tan_angle
            if dia >= self._tool.diameter:
                return self._tool.diameter
            return dia
        else:
            return self._tool.diameter

    def _gcode_engrave(self):
        """Converts a list of paths into G-code instructions for the CNC.
        :returns engrave: A String object"""
        engrave = ''
        for path in self._qr_path.get_vectors():
            engrave += self._engrave(path)
        return engrave

    def _engrave(self, line_segment):
        """Converts a QR-code line segment bit state into G-code XYZ moves for the CNC.
        :param line_segment: LineSegment object.
        :returns cmd: a string object"""
        cmd = ''

        # Rapid move: start position of vector
        tool_step = self._get_xy_move_per_step()
        qrpos_x = round(line_segment.position.x * tool_step + self._xy_zero.x, 3)
        qrpos_y = round(-line_segment.position.y * tool_step + self._xy_zero.y, 3)
        cmd += 'G00 X' + str(qrpos_x) + \
               ' Y' + str(qrpos_y) + '\n'
        # Engrave: Z down
        cmd += 'G01 Z-' + str(self._engrave_params.z_engrave) + ' F' + str(self._tool.fz) + '\n'
        # Engrave: move
        if line_segment.y_length != 0:
            cmd += 'G01 Y' + str(round(qrpos_y - line_segment.y_length * tool_step, 3))
            cmd += ' F' + str(self._tool.fxy) + '\n'
        elif line_segment.x_length != 0:
            cmd += 'G01 X' + str(round(qrpos_x + line_segment.x_length * tool_step, 3))
            cmd += ' F' + str(self._tool.fxy) + '\n'
        #  Hover: Z up
        cmd += 'G00 Z' + str(self._engrave_params.z_hover) + '\n'
        return cmd

    def _gcode_header(self):
        """Creates boilerplate code that is sent into the G-code file. It creates human-readable comments to
        identify project information.
        :returns header: a String object"""
        header = '(Project: QR-codengrave_' + self._project_name + ')\n'
        header += '(Created with Schallbert\'s QR-codengrave Version ' + str(self._version) + ')\n'
        header += '(Job duration ca. ' + str(self._job_duration) + ')\n\n'
        header += '(Required tool: ' + self._tool.get_description() + ')\n\n'
        return header

    def _gcode_prepare(self):
        """Creates boilerplate G-code to initialize the CNC with correct tool, spindle speed, and moves to Qr-code's
         targeted position.
         :returns prepare: a String object"""
        prepare = 'G90 \n'  # Set absolute coordinates (modal)
        prepare += 'MSG "Tool: ' + self._tool.get_description() + '"\n'  # Tool message for user
        prepare += 'T' + str(self._tool.number) + ' M06 \n'  # Tool select / change
        prepare += 'M03 S' + str(self._tool.speed) + '\n'  # Set spindle speed

        prepare += 'G00 Z' + str(self._engrave_params.z_flyover) + '\n\n'  # Go to flyover height
        prepare += 'G00 Y0 X0 \n'  # Go to workpiece XY0
        prepare += 'G00 X' + str(self._xy_zero.x) + ' Y' + \
                   str(self._xy_zero.y) + ' \n'  # Go to QR-code begin position
        prepare += 'G00 Z' + str(self._engrave_params.z_hover) + '\n\n'  # Go to hover Z height
        return prepare

    def _gcode_finalize(self):
        """Creates boilerplate G-code to finalize the CNC job. Commands spindle stop, returns to workpiece zero.
        :returns finalize, a String object"""
        finalize = '\nM05 \n'  # Spindle Stop
        finalize += 'G00 Z' + str(self._engrave_params.z_flyover) + '\n'  # Go to flyover height
        finalize += 'G00 Y0 X0 \n'  # Go to workpiece XY0
        finalize += 'M30 \n'  # End of Program
        return finalize

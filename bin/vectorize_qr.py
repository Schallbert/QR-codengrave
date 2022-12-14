from qrcodegen import QrCode
from enum import Enum


class Direction:
    """Enum class associating a DIRECTION on the XY-plane with a number"""
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3
    ERROR = 4


class Point:
    """Defines a point in the XY-plane. POD: No methods, parameters are public."""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Line:
    """Defines a line in the XY-plane. For the purpose of creating paths, a line defined by this class
    never has both a direction in X and Y but can only be orthogonal to the X or Y axis.
    It takes two Points as input."""
    def __init__(self, p_start, p_end):
        self._p_start = p_start
        self._p_end = p_end

        self._length_x = self._p_end.x - self._p_start.x
        self._length_y = self._p_end.y - self._p_start.y
        self._abs_length = abs(self._length_y + self._length_x) + 1

        if self._length_x and self._length_y:
            raise Exception("Error: in this context a line can only either horizontal or vertical")

    def get_direction(self):
        """Getter method.
        :returns a Direction enum representing the direction in which the line is drawn from start to end point.
        :returns ERROR when the line is ill-defined."""
        if self._length_x > 0:
            return Direction.RIGHT
        elif self._length_x < 0:
            return Direction.LEFT
        if self._length_y > 0:
            return Direction.UP
        elif self._length_y < 0:
            return Direction.DOWN
        return Direction.ERROR

    def get_abs_length(self):
        """Getter method.
         :returns the absolute length of the line.
         Length is by +1 longer than the result you'd
        get from calculating |Pend - Pstart| to simplify handling in for loops."""
        return self._abs_length

    def get_p_start(self):
        """Getter method.
         :returns the start point of the line"""
        return self._p_start

    def get_p_end(self):
        """Getter method.
        :returns the end point of the line"""
        return self._p_end


class QrLineData:
    """Data representation for a section of consecutive bits with the same value, optimized for milling.
    NOTE: On __init__, section length is initialized with 'zero' for True's (no move is necessary for first engraving
     command) and with 'one' for False's (as to reach the position of next True, it has to move by one step more)
     :param state in this representation False = mill bit up, and True = mill bit down meaning that True would have the
    surface engraved the size of the bit diameter at specified engraving depth.
    :param start at the start of a new path, the tool doesn't have to move two steps but just one to reach the next
    possible bit state"""
    def __init__(self, state, start=False):
        self._state = state
        self._length = 2
        if start:
            self._length = 1
        if state:
            self._length = 0

    def add_length(self):
        """NOTE: this method is meant to be used inside the VectorizeQR class only to calculate
         increments length of a QrLineData object by 1."""
        self._length += 1

    def finalize(self):
        if not self._state:
            self._length -= 1

    def get_state(self):
        """Getter method.
        :returns True if QRLineData segment shall be engraved and False if not."""
        return self._state

    def get_length(self):
        """Getter method.
        :returns an integer representing the length to pass for the current data state."""
        return self._length


class QrPathSegment:
    """Represents a milling path segment of a QR-code (a line with engraving information for the QR code).
    Data container combining a Line object with the corresponding QrLineData object.
    Inputs are Line and QrLineData.
    """
    def __init__(self, xy_line, z_vector):
        self._xy_line = xy_line
        self._z_vector = z_vector

    def get_xy_line(self):
        """Getter method.
        :returns a Line object.
        Represents a XY-line"""
        return self._xy_line

    def get_z_vector(self):
        """Getter method.
        :returns a QrLineData object.
        Represents the engraving information of the XY-Line."""
        return self._z_vector


def _is_even(number):
    """Helper function.
    :returns True if the number is even, False if uneven."""
    return (number % 2) == 0


def create_spiral(qr_code_size):
    """creates a spiral in form of a list of lines from a qr-code size. The 0th list element is undefined.
       Valid size is between 21 and 177 according to standard.
       The spiral goes clockwise and turns inwards."""
    if (qr_code_size < 21) or (qr_code_size > 177):
        raise Exception("Error: invalid qr_code_size")

    # Line[0] is ill-defined by design.
    # Line[1] always is direction RIGHT and at full length of the code.
    # Reason for size-1: Point0 is also drawn.
    lines = [Line(Point(0, 0), Point(0, 0)),
             Line(Point(0, 0), Point(qr_code_size - 1, 0))]
    for n in range(2, 2 * qr_code_size):
        k = n // 2
        m = qr_code_size - k  # line length of spiral path
        negify = -1
        p_start = lines[n - 1].get_p_end()  # start always is end of last line
        if _is_even(k):
            negify = 1  # every second operation goes either into neg. x or y direction
        if _is_even(n):
            p_end = Point(p_start.x, p_start.y + negify * m)  # direction Y
        else:
            p_end = Point(p_start.x + negify * m, p_start.y)  # direction X
        lines.append(Line(p_start, p_end))

    return lines


class VectorizeQr:
    """Class that converts the information within a QR-code into vectors,
    and finally into a spiral path that can be used by a CAM module to create machine instructions."""
    def __init__(self, qr, border=2):
        self._qr = qr
        if border > 5 or border < 0:
            border = 1
        self._border = border

    def generate_spiral_path(self):
        """Generates a spiral from individual path segments composed of vectors of a QR-code.
        :returns path: a list of QrPathSegment objects"""
        spiral = create_spiral(self._qr.get_size() + 2 * self._border)
        path = []
        for i in range(1, len(spiral)):
            bs = self._qr_bitstream_from_line(spiral[i])
            vect = self._vectorize_bitstream(bs)
            path.append(QrPathSegment(spiral[i], vect))
        return path

    def _qr_bitstream_from_line(self, line):
        """Creates a bitstream from an input line of a QR-code data representation
        :param line: a QR-code data representation (line of bits within the QR-code)
        :returns bitstream: returns an array of bits reflecting the QR code's state at the respective
        point of the line."""
        bitstream = []
        if line.get_direction() == Direction.RIGHT:
            for x in range(line.get_p_start().x, line.get_p_end().x + 1):
                bitstream.append(self._qr.get_module(x, abs(line.get_p_start().y)))
        if line.get_direction() == Direction.LEFT:
            for x in range(line.get_p_start().x, line.get_p_end().x - 1, -1):
                bitstream.append(self._qr.get_module(x, abs(line.get_p_start().y)))
        if line.get_direction() == Direction.UP:
            for y in range(line.get_p_start().y, line.get_p_end().y + 1):
                bitstream.append(self._qr.get_module(line.get_p_start().x, abs(y)))
        if line.get_direction() == Direction.DOWN:
            for y in range(line.get_p_start().y, line.get_p_end().y - 1, -1):
                bitstream.append(self._qr.get_module(line.get_p_start().x, abs(y)))
        return bitstream

    def _vectorize_bitstream(self, bitstream):
        """Creates a QrLineData object from an input bistream
        :param bitstream: an array of bits = a line of the QR-code
        :returns line_vector: A list of QrLineData objects"""
        line_vector = []
        data = QrLineData(bitstream[0], True)
        for bit in range(1, len(bitstream)):
            if bitstream[bit] == data.get_state():
                data.add_length()
            else:
                line_vector.append(data)
                data = QrLineData(bitstream[bit])
        if not data.get_state():
            data.finalize()
        line_vector.append(data)

        return line_vector

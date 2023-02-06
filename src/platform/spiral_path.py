from src.platform.vectorize_helper import Point

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
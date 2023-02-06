class Point:
    """Defines a point in the XY-plane. POD: No methods, parameters are public."""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class LineSegment:
    """Defines a LineSegment in the XY-plane. POD: No Methods, parameters are public."""
    def __init__(self, x_length, y_length, position):
        self.x_length = x_length
        self.y_length = y_length
        self.position = position

    def __eq__(self, other):
        result = True
        result &= (self.x_length == other.x_length)
        result &= (self.y_length == other.y_length)
        result &= (self.position == other.position)
        return result


class QrValueTable:
    def __init__(self):
        self.table = {}
        self.size = 0

    def set_qr(self, qr):
        """Takes a QR-code object and copies its values into a dictionary.
        :param qr: a QrCode object"""
        self.size = qr.get_size()
        for y in range(self.size):
            for x in range(self.size):
                self.table[y, x] = qr.get_module(x, y)

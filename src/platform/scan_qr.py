class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class LineSegment:
    def __init__(self, x, y, position):
        self.x = x
        self.y = y
        self.position = position


class ScanQr:
    def __init__(self, qr):
        self._size = qr.get_size()

        self._qr_todo = {}
        for x in range(self._size):
            for y in range(self._size):
                self._qr_todo[x][y] = qr.get_module(x, y)

    def _get_line(self, row):
        vectors = []
        position = Position(0, row)
        x_length = 1
        y_length = 1

        while position.x < self._size:
            state = self._qr_todo[position.x][row]
            if state:
                while self._qr_todo[x_length][row + y_length]:
                    y_length = y_length + 1
                if y_length > 1:
                    segment = LineSegment(0, y_length, position)
                    vectors.append(segment)
                    self._clear(segment)
                else:
                    x_length = x_length + 1
            else:
                segment = LineSegment(x_length, 0, position)
                vectors.append(segment)
                self._clear(segment)
            position.x = position.x + 1

    def _get_column(self):
        pass

    def _clear(self, segment):
        pass

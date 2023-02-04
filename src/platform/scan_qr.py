class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class LineSegment:
    def __init__(self, x_length, y_length, position):
        self.x_length = x_length
        self.y_length = y_length
        self.position = position


class QrValueTable:
    def __init__(self):
        self.table = {}
        self.size = 0

    def set_qr(self, qr):
        self.size = qr.get_size()
        for y in range(self.size):
            for x in range(self.size):
                self.table[x, y] = qr.get_module(x, y)


class ScanQr:
    def __init__(self, qr_value_table):
        self._qr_todo = qr_value_table

    def get_vectors(self):
        line_list = []
        for line in range(self._qr_todo.size):
            line_list += self._get_line_left_to_right(line)
            # if line + 1 < self._qr_todo.size:
            #    line_list += self._get_line_right_to_left(line + 1)
        return line_list

    def _get_line_left_to_right(self, row):
        """This algorithm walks through a line of the QR-code left to right and line by line to construct vectors
        of coherent bits that are True. If the bit below the currently targeted bit is also True, then a vertical
        line is created. Else, a horizontal line is created."""
        vectors = []
        position = Position(0, row)
        x_length = 0
        y_length = 1

        if row > self._qr_todo.size:
            return

        while position.x < self._qr_todo.size:
            if self._qr_todo.table[row, position.x]:
                x_length = x_length + 1
                if row + y_length < self._qr_todo.size:
                    while self._qr_todo.table[row + y_length, position.x]:
                        y_length = y_length + 1
                    if y_length > 1:
                        segment = LineSegment(0, y_length, Position(position.x, position.y))
                        vectors.append(segment)
                        self._clear_todo(segment)
                        y_length = 1
                        x_length = 0
            elif x_length > 0:
                segment = LineSegment(x_length, 0, Position(position.x - x_length, position.y))
                vectors.append(segment)
                self._clear_todo(segment)
                x_length = 0
            position.x = position.x + 1

        if x_length > 0:
            segment = LineSegment(x_length, 0, Position(position.x - x_length, position.y))
            vectors.append(segment)
            self._clear_todo(segment)

        return vectors

    def _get_line_right_to_left(self, row):
        """This algorithm walks through a line of the QR-code right to left and line by line to construct vectors
        of coherent bits that are True. If the bit below the currently targeted bit is also True, then a vertical
        line is created. Else, a horizontal line is created."""
        vectors = []
        position = Position(self._qr_todo.size, row)
        start_position = Position(self._qr_todo.size, row)
        x_length = 0
        y_length = 1

        if row > self._qr_todo.size:
            return

        while position.x >= 0:
            if self._qr_todo.table[position.x][row]:
                while self._qr_todo.table[x_length][row + y_length]:
                    y_length = y_length + 1
                if y_length > 1:
                    segment = LineSegment(0, y_length, start_position)
                    vectors.append(segment)
                    self._clear_todo(segment)
                    y_length = 1
                else:
                    x_length = x_length + 1
            elif x_length > 0:
                segment = LineSegment(-x_length, 0, start_position)
                vectors.append(segment)
                self._clear_todo(segment)
                x_length = 0
            else:
                start_position.x = position.x - 1
            position.x = position.x - 1
        return vectors

    def _clear_todo(self, segment):
        if segment.x_length == 0:
            for y in range(segment.y_length):
                self._qr_todo.table[segment.position.y + y, segment.position.x] = False
        elif segment.y_length == 0:
            for x in range(segment.x_length):
                self._qr_todo.table[segment.position.y, segment.position.x + x] = False

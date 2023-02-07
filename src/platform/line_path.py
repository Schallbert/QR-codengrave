from src.platform.vectorize_helper import Point, LineSegment


class LinePath:
    def __init__(self, qr_value_table):
        self._qr_todo = qr_value_table
        self._size = qr_value_table.size
        self._line_list = []

    def get_size(self):
        return self._size

    def get_vectors(self):
        """Compiles a list of vectors from the qr-code input that scans the fields
        row-by-row, left-to-right for even line numbers, and right-to-left for uneven line numbers
        to reduce machining time.
        :return line_list: a list of LineSegments"""
        if not self._line_list:
            for line in range(self._size):
                if line % 2:
                    self._line_list += self._get_line_right_to_left(line)
                else:
                    self._line_list += self._get_line_left_to_right(line)
        return self._line_list

    def _get_line_left_to_right(self, row):
        """This algorithm walks through a line of the QR-code left to right and line by line to construct vectors
        of coherent bits that are True. If the bit below the currently targeted bit is also True, then a vertical
        line is created. Else, a horizontal vector is created.
        :param row: int the row in the QR-code to analyze
        :return a list of vectors"""
        vectors = []
        position = Point(0, row)
        x_length = 0
        y_length = 1

        if row >= self._size:
            return vectors

        while position.x < self._size:
            if self._qr_todo.table[row, position.x]:
                x_length += 1
                if x_length == 1:
                    while row + y_length < self._size and self._qr_todo.table[row + y_length, position.x]:
                        y_length += 1
            elif x_length > 0:
                segment = LineSegment(x_length, 0, Point(position.x - x_length, position.y))
                vectors.append(segment)
                self._clear_todo(segment)
                x_length = 0
            if y_length > 1:
                segment = LineSegment(0, y_length, Point(position.x, position.y))
                vectors.append(segment)
                self._clear_todo(segment)
                y_length = 1
            position.x += 1

        if x_length > 0:
            segment = LineSegment(x_length, 0, Point(position.x - x_length, position.y))
            vectors.append(segment)
            self._clear_todo(segment)
        return vectors

    def _get_line_right_to_left(self, row):
        """This algorithm walks through a line of the QR-code right to left and line by line to construct vectors
        of coherent bits that are True. If the bit below the currently targeted bit is also True, then a vertical
        line is created. Else, a horizontal vector is created.
        :param row: the row in the QR-code to analyze
        :return a list of vectors"""
        vectors = []
        position = Point(self._size - 1, row)
        x_length = 0
        y_length = 1

        if row >= self._size:
            return vectors

        while position.x >= 0:
            if self._qr_todo.table[row, position.x]:
                x_length += 1
                while row + y_length < self._size and self._qr_todo.table[row + y_length, position.x]:
                    y_length += 1
            elif x_length > 0:
                segment = LineSegment(-x_length, 0, Point(position.x + x_length, position.y))
                vectors.append(segment)
                self._clear_todo(segment)
                x_length = 0
            if y_length > 1:
                segment = LineSegment(0, y_length, Point(position.x, position.y))
                vectors.append(segment)
                self._clear_todo(segment)
                y_length = 1
                x_length = 0
            position.x -= 1

        position.x = -1
        if x_length > 0:
            segment = LineSegment(-x_length, 0, Point(position.x + x_length, position.y))
            vectors.append(segment)
            self._clear_todo(segment)
        return vectors

    def _clear_todo(self, segment):
        """Method to clear a segment of the QR-code working copy. Clearing is done to not double-engrave
        already completed fields.
        :param segment: A LineSegment object"""
        if segment.x_length == 0:
            for y in range(segment.y_length):
                self._qr_todo.table[segment.position.y + y, segment.position.x] = False
        elif segment.y_length == 0:
            for x in range(segment.x_length):
                self._qr_todo.table[segment.position.y, segment.position.x + x] = False

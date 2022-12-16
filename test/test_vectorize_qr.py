import unittest
from unittest.mock import MagicMock

from qrcodegen import QrCode
from bin.platform.vectorize_qr import Direction, Point, Line, VectorizeQr, create_spiral


class TestLine(unittest.TestCase):

    def test_line_x_calculates_valid_length(self):
        line = Line(Point(0, 0), Point(5, 0))
        self.assertEqual(6, line.get_abs_length())

    def test_line_y_calculates_valid_length(self):
        line = Line(Point(0, 0), Point(0, 9))
        self.assertEqual(10, line.get_abs_length())

    def test_line_calculates_valid_length(self):
        line = Line(Point(0, 0), Point(0, -9))
        self.assertEqual(10, line.get_abs_length())

    def test_line_0_returns_directionerror(self):
        line = Line(Point(0, 0), Point(0, 0))
        self.assertEqual(Direction.ERROR, line.get_direction())
        self.assertEqual(1, line.get_abs_length())

    def test_line_wrong_usage_returns_error(self):
        self.assertRaises(Exception, Line, Point(0, 0), Point(5, 9))

    def test_line_x_positive_direction_returns_right(self):
        line = Line(Point(0, 0), Point(2, 0))
        self.assertEqual(3, line.get_abs_length())
        self.assertEqual(Direction.RIGHT, line.get_direction())

    def test_line_x_negative_direction_returns_left(self):
        line = Line(Point(15, 0), Point(2, 0))
        self.assertEqual(14, line.get_abs_length())
        self.assertEqual(Direction.LEFT, line.get_direction())

    def test_line_y_positive_direction_returns_up(self):
        line = Line(Point(15, 0), Point(15, 24))
        self.assertEqual(25, line.get_abs_length())
        self.assertEqual(Direction.UP, line.get_direction())

    def test_line_y_negative_direction_returns_down(self):
        line = Line(Point(2, 23), Point(2, 0))
        self.assertEqual(24, line.get_abs_length())
        self.assertEqual(Direction.DOWN, line.get_direction())

    def test_create_spiral_undersized_raises(self):
        self.assertRaises(Exception, create_spiral, 20)

    def test_create_spiral_oversized_raises(self):
        self.assertRaises(Exception, create_spiral, 200)

    def test_create_spiral_21_returns_41_paths(self):
        # Path0 is empty, thus not counted
        self.assertEqual(42, len(create_spiral(21)))

    def test_create_spiral_21_line1_ok(self):
        line1 = create_spiral(21)[1]
        self.assertEqual(21, line1.get_abs_length())
        self.assertEqual(20, line1.get_p_end().x)
        self.assertEqual(0, line1.get_p_end().y)
        self.assertEqual(Direction.RIGHT, line1.get_direction())

    def test_create_spiral_21_line2_ok(self):
        line2 = create_spiral(21)[2]
        self.assertEqual(20, line2.get_p_start().x)
        self.assertEqual(0, line2.get_p_start().y)
        self.assertEqual(20, line2.get_p_end().x)
        self.assertEqual(-20, line2.get_p_end().y)
        self.assertEqual(21, line2.get_abs_length())
        self.assertEqual(Direction.DOWN, line2.get_direction())

    def test_create_spiral_21_line3_ok(self):
        line3 = create_spiral(21)[3]
        self.assertEqual(20, line3.get_p_start().x)
        self.assertEqual(-20, line3.get_p_start().y)
        self.assertEqual(0, line3.get_p_end().x)
        self.assertEqual(-20, line3.get_p_end().y)
        self.assertEqual(21, line3.get_abs_length())
        self.assertEqual(Direction.LEFT, line3.get_direction())

    def test_create_spiral_21_line9_ok(self):
        line9 = create_spiral(21)[9]
        self.assertEqual(1, line9.get_p_start().x)
        self.assertEqual(-2, line9.get_p_start().y)
        self.assertEqual(18, line9.get_p_end().x)
        self.assertEqual(-2, line9.get_p_end().y)
        self.assertEqual(18, line9.get_abs_length())
        self.assertEqual(Direction.RIGHT, line9.get_direction())

    def test_create_spiral_21_line40_ok(self):
        line40 = create_spiral(21)[40]
        self.assertEqual(9, line40.get_p_start().x)
        self.assertEqual(-11, line40.get_p_start().y)
        self.assertEqual(9, line40.get_p_end().x)
        self.assertEqual(-10, line40.get_p_end().y)
        self.assertEqual(2, line40.get_abs_length())
        self.assertEqual(Direction.UP, line40.get_direction())

    def test_create_spiral_21_line41_ok(self):
        line41 = create_spiral(21)[41]
        self.assertEqual(9, line41.get_p_start().x)
        self.assertEqual(-10, line41.get_p_start().y)
        self.assertEqual(10, line41.get_p_end().x)
        self.assertEqual(-10, line41.get_p_end().y)
        self.assertEqual(2, line41.get_abs_length())
        self.assertEqual(Direction.RIGHT, line41.get_direction())


class TestPath(unittest.TestCase):
    qr = QrCode.encode_text("schallbert.de", QrCode.Ecc.MEDIUM)
    cam = VectorizeQr(qr, 1)
    test_line_x = Line(Point(0, 0), Point(20, 0))
    test_line_y = Line(Point(10, -13), Point(10, -3))

    def test_bitstream_return_vector_has_correct_length(self):
        self.assertEqual(self.qr.get_size(), len(self.cam._qr_bitstream_from_line(self.test_line_x)))

    # For the next 4 tests, the expectation is only valid for the LAST call within the checked for loop.
    def test_bitstream_qr_input_loop_xpos_correct(self):
        mock_qr = QrCode.encode_text("schallbert.de", QrCode.Ecc.MEDIUM)
        mock_qr.get_module = MagicMock()
        cam = VectorizeQr(mock_qr, 1)
        cam._qr_bitstream_from_line(self.test_line_x)
        mock_qr.get_module.assert_called_with(20, 0)

    def test_bitstream_qr_input_loop_xneg_correct(self):
        mock_qr = QrCode.encode_text("schallbert.de", QrCode.Ecc.MEDIUM)
        mock_qr.get_module = MagicMock()
        cam = VectorizeQr(mock_qr, 1)
        cam._qr_bitstream_from_line(Line(Point(12, -2), Point(10, -2)))
        mock_qr.get_module.assert_called_with(10, 2)

    def test_bitstream_qr_input_loop_ypos_correct(self):
        mock_qr = QrCode.encode_text("schallbert.de", QrCode.Ecc.MEDIUM)
        mock_qr.get_module = MagicMock()
        cam = VectorizeQr(mock_qr, 1)
        cam._qr_bitstream_from_line(Line(Point(12, -2), Point(12, 0)))
        mock_qr.get_module.assert_called_with(12, 0)

    def test_bitstream_qr_input_loop_yneg_correct(self):
        mock_qr = QrCode.encode_text("schallbert.de", QrCode.Ecc.MEDIUM)
        mock_qr.get_module = MagicMock()
        cam = VectorizeQr(mock_qr, 1)
        cam._qr_bitstream_from_line(self.test_line_y)
        mock_qr.get_module.assert_called_with(10, 3)

    def test_qr_line_data_return_vector_has_correct_length(self):
        self.assertEqual(1, len(self.cam._vectorize_bitstream([True, True, True, True, True])))

    def test_qr_line_data_single_pixelFalse_return_vector_has_correct_attribute(self):
        cmd = self.cam._vectorize_bitstream([False])
        # calls with start = true so set to 1, then calls finalize so set back to 0. Edge case.
        self.assertEqual(0, cmd[0].get_length())
        self.assertFalse(cmd[0].get_state())

    def test_qr_line_data_single_pixelTrue_return_vector_has_correct_attribute(self):
        cmd = self.cam._vectorize_bitstream([True])
        self.assertEqual(0, cmd[0].get_length())
        self.assertTrue(cmd[0].get_state())

    def test_qr_line_data_all_true_return_vector_has_correct_attribute(self):
        cmd = self.cam._vectorize_bitstream([True, True, True, True, True])
        self.assertEqual(4, cmd[0].get_length())
        self.assertTrue(cmd[0].get_state())

    def test_qr_line_data_all_false_return_vector_has_correct_attribute(self):
        cmd = self.cam._vectorize_bitstream([False, False, False, False, False])
        self.assertEqual(4, cmd[0].get_length())
        self.assertFalse(cmd[0].get_state())

    def test_qr_line_data_mixed_return_vector_has_correct_attribute(self):
        cmd = self.cam._vectorize_bitstream([False, True, True, True, False, False, True, True, False, True])
        self.assertEqual(6, len(cmd))
        self.assertEqual(2, cmd[1].get_length())
        self.assertEqual(3, cmd[2].get_length())
        self.assertEqual(1, cmd[3].get_length())

    def test_qr_line_data_mixed_return_vector_has_correct_length(self):
        cmd = self.cam._vectorize_bitstream([False, True, True, True, False, False, True, True, False, True])
        self.assertEqual(len(cmd), cmd[1].get_length() + cmd[2].get_length() + cmd[3].get_length())

    def test_pathgen_path_length_ok(self):
        qr = VectorizeQr(self.qr, 0)
        paths = qr.generate_spiral_path()
        self.assertEqual(41, len(paths))

    def test_pathgen_path1_correct(self):
        mock_qr = QrCode.encode_text("schallbert.de", QrCode.Ecc.MEDIUM)
        mock_qr.get_module = MagicMock()
        mock_qr.get_module.return_value = True  # always returns True, so zVector length == qr width
        qr = VectorizeQr(mock_qr, 0)
        paths = qr.generate_spiral_path()
        line_to_check = paths[0].get_xy_line()
        self.assertEqual(Direction.RIGHT, line_to_check.get_direction())
        self.assertEqual(21, line_to_check.get_abs_length())
        self.assertEqual(20, paths[0].get_z_vector()[0].get_length())


if __name__ == '__main__':
    unittest.main()

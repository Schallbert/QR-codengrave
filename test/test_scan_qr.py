import unittest
from unittest.mock import MagicMock

from qrcodegen import QrCode
from src.platform.scan_qr import QrValueTable, ScanQr, LineSegment, Position


class TestQrValueTable(unittest.TestCase):
    def setUp(self):
        self.mock_qr = QrCode.encode_text("schallbert.de", QrCode.Ecc.MEDIUM)
        self.mock_qr.get_module = MagicMock()
        self.mock_qr.get_size = MagicMock()

    def test_qrvaluetable_setqr_size_matches(self):
        self.mock_qr.get_module.return_value = True
        self.mock_qr.get_size.return_value = 21
        table = QrValueTable()
        table.set_qr(self.mock_qr)
        self.assertEqual(21, table.size)

    def test_qrvaluetable_setqr_table_matches_size(self):
        self.mock_qr.get_module.return_value = True
        self.mock_qr.get_size.return_value = 21
        table = QrValueTable()
        table.set_qr(self.mock_qr)
        self.assertEqual(True, table.table[20, 20])

    def test_qrvaluetable_setqr_indexoutofrange_throws(self):
        self.mock_qr.get_module.return_value = False
        self.mock_qr.get_size.return_value = 21
        table = QrValueTable()
        table.set_qr(self.mock_qr)
        self.assertRaises(Exception, table.table, [21, 21])


class TestScanQr(unittest.TestCase):
    def setUp(self):
        # 1 0 1 1 0
        # 0 1 1 0 0
        # 1 1 1 1 1
        # 0 0 0 0 0
        # 0 1 0 1 1
        self.sim_qr = QrValueTable()
        self.sim_qr.table[0, 0] = True
        self.sim_qr.table[0, 1] = False
        self.sim_qr.table[0, 2] = True
        self.sim_qr.table[0, 3] = True
        self.sim_qr.table[0, 4] = False
        self.sim_qr.table[1, 0] = False
        self.sim_qr.table[1, 1] = True
        self.sim_qr.table[1, 2] = True
        self.sim_qr.table[1, 3] = False
        self.sim_qr.table[1, 4] = False
        self.sim_qr.table[2, 0] = True
        self.sim_qr.table[2, 1] = True
        self.sim_qr.table[2, 2] = True
        self.sim_qr.table[2, 3] = True
        self.sim_qr.table[2, 4] = True
        self.sim_qr.table[3, 0] = False
        self.sim_qr.table[3, 1] = False
        self.sim_qr.table[3, 2] = False
        self.sim_qr.table[3, 3] = False
        self.sim_qr.table[3, 4] = False
        self.sim_qr.table[4, 0] = False
        self.sim_qr.table[4, 1] = True
        self.sim_qr.table[4, 2] = False
        self.sim_qr.table[4, 3] = True
        self.sim_qr.table[4, 4] = True
        self.sim_qr.size = 5
        self.scan_qr = ScanQr(self.sim_qr)

    def test_rowoutofrange_returns_0vectors(self):
        vectors = self.scan_qr._get_line_left_to_right(5)
        self.assertEqual(0, len(vectors))

    def test_getlinel2r_line0_returns_3vectors(self):
        vectors = self.scan_qr._get_line_left_to_right(0)
        self.assertEqual(3, len(vectors))

    def test_getlinel2r_line0_vector0_contents_ok(self):
        vectors = self.scan_qr._get_line_left_to_right(0)
        self.assertEqual(1, vectors[0].x_length)
        self.assertEqual(0, vectors[0].y_length)
        self.assertEqual(0, vectors[0].position.x)
        self.assertEqual(0, vectors[0].position.y)

    def test_getlinel2r_line0_vector1_contents_ok(self):
        vectors = self.scan_qr._get_line_left_to_right(0)
        self.assertEqual(0, vectors[1].x_length)
        self.assertEqual(3, vectors[1].y_length)
        self.assertEqual(2, vectors[1].position.x)
        self.assertEqual(0, vectors[1].position.y)

    def test_getlinel2r_line0_vector2_contents_ok(self):
        vectors = self.scan_qr._get_line_left_to_right(0)
        self.assertEqual(1, vectors[2].x_length)
        self.assertEqual(0, vectors[2].y_length)
        self.assertEqual(3, vectors[2].position.x)
        self.assertEqual(0, vectors[2].position.y)

    def test_getlinel2r_line1_returns_2vectors(self):
        vectors = self.scan_qr._get_line_left_to_right(1)
        self.assertEqual(2, len(vectors))

    def test_getlinel2r_line1_vector0_contents_ok(self):
        vectors = self.scan_qr._get_line_left_to_right(1)
        self.assertEqual(0, vectors[0].x_length)
        self.assertEqual(2, vectors[0].y_length)
        self.assertEqual(1, vectors[0].position.x)
        self.assertEqual(1, vectors[0].position.y)

    def test_getlinel2r_line1_vector1_contents_ok(self):
        vectors = self.scan_qr._get_line_left_to_right(1)
        self.assertEqual(0, vectors[1].x_length)
        self.assertEqual(2, vectors[1].y_length)
        self.assertEqual(2, vectors[1].position.x)
        self.assertEqual(1, vectors[1].position.y)

    def test_getlinel2r_line2_returns_1vector(self):
        vectors = self.scan_qr._get_line_left_to_right(2)
        self.assertEqual(1, len(vectors))

    def test_getlinel2r_line2_vector0_contents_ok(self):
        vectors = self.scan_qr._get_line_left_to_right(2)
        self.assertEqual(5, vectors[0].x_length)
        self.assertEqual(0, vectors[0].y_length)
        self.assertEqual(0, vectors[0].position.x)
        self.assertEqual(2, vectors[0].position.y)

    def test_getlinel2r_line3_returns_0vector(self):
        vectors = self.scan_qr._get_line_left_to_right(3)
        self.assertEqual(0, len(vectors))

    def test_getlinel2r_line4_returns_2vectors(self):
        vectors = self.scan_qr._get_line_left_to_right(4)
        self.assertEqual(2, len(vectors))

    def test_getlinel2r_line4_vector0_contents_ok(self):
        vectors = self.scan_qr._get_line_left_to_right(4)
        self.assertEqual(1, vectors[0].x_length)
        self.assertEqual(0, vectors[0].y_length)
        self.assertEqual(1, vectors[0].position.x)
        self.assertEqual(4, vectors[0].position.y)

    def test_getlinel2r_line4_vector1_contents_ok(self):
        vectors = self.scan_qr._get_line_left_to_right(4)
        self.assertEqual(2, vectors[1].x_length)
        self.assertEqual(0, vectors[1].y_length)
        self.assertEqual(3, vectors[1].position.x)
        self.assertEqual(4, vectors[1].position.y)

    def test_getliner2l_line0_returns_2vectors(self):
        vectors = self.scan_qr._get_line_right_to_left(0)
        self.assertEqual(2, len(vectors))

    def test_getliner2l_line0_vector0_contents_ok(self):
        vectors = self.scan_qr._get_line_right_to_left(0)
        self.assertEqual(0, vectors[0].x_length)
        self.assertEqual(3, vectors[0].y_length)
        self.assertEqual(2, vectors[0].position.x)
        self.assertEqual(0, vectors[0].position.y)

    def test_getliner2l_line0_vector1_contents_ok(self):
        vectors = self.scan_qr._get_line_right_to_left(0)
        self.assertEqual(-1, vectors[1].x_length)
        self.assertEqual(0, vectors[1].y_length)
        self.assertEqual(0, vectors[1].position.x)
        self.assertEqual(0, vectors[1].position.y)

    def test_getliner2l_line1_returns_2vectors(self):
        vectors = self.scan_qr._get_line_right_to_left(1)
        self.assertEqual(2, len(vectors))

    def test_getliner2l_line1_vector0_contents_ok(self):
        vectors = self.scan_qr._get_line_right_to_left(1)
        self.assertEqual(0, vectors[0].x_length)
        self.assertEqual(2, vectors[0].y_length)
        self.assertEqual(2, vectors[0].position.x)
        self.assertEqual(1, vectors[0].position.y)

    def test_getliner2l_line1_vector1_contents_ok(self):
        vectors = self.scan_qr._get_line_right_to_left(1)
        self.assertEqual(0, vectors[1].x_length)
        self.assertEqual(2, vectors[1].y_length)
        self.assertEqual(1, vectors[1].position.x)
        self.assertEqual(1, vectors[1].position.y)

    def test_getliner2l_line2_returns_1vector(self):
        vectors = self.scan_qr._get_line_right_to_left(2)
        self.assertEqual(1, len(vectors))

    def test_getliner2l_line2_vector0_contents_ok(self):
        vectors = self.scan_qr._get_line_right_to_left(2)
        self.assertEqual(-5, vectors[0].x_length)
        self.assertEqual(0, vectors[0].y_length)
        self.assertEqual(4, vectors[0].position.x)
        self.assertEqual(2, vectors[0].position.y)

    def test_getliner2l_line3_returns_0vector(self):
        vectors = self.scan_qr._get_line_right_to_left(3)
        self.assertEqual(0, len(vectors))

    def test_getliner2l_line4_returns_2vector(self):
        vectors = self.scan_qr._get_line_right_to_left(4)
        self.assertEqual(2, len(vectors))

    def test_getliner2l_line4_vector0_contents_ok(self):
        vectors = self.scan_qr._get_line_right_to_left(4)
        self.assertEqual(-2, vectors[0].x_length)
        self.assertEqual(0, vectors[0].y_length)
        self.assertEqual(4, vectors[0].position.x)
        self.assertEqual(4, vectors[0].position.y)

    def test_getliner2l_line4_vector1_contents_ok(self):
        vectors = self.scan_qr._get_line_right_to_left(4)
        self.assertEqual(-1, vectors[1].x_length)
        self.assertEqual(0, vectors[1].y_length)
        self.assertEqual(1, vectors[1].position.x)
        self.assertEqual(4, vectors[1].position.y)

    def test_cleartodo_singlepixel_ok(self):
        to_be_cleared = LineSegment(1, 0, Position(0, 0))
        self.scan_qr._clear_todo(to_be_cleared)
        vectors = self.scan_qr._get_line_left_to_right(0)
        self.assertEqual(2, len(vectors))
        self.assertEqual(2, vectors[0].position.x)
        self.assertEqual(3, vectors[1].position.x)

    def test_cleartodo_line_horizontal_ok(self):
        to_be_cleared = LineSegment(2, 0, Position(2, 0))
        self.scan_qr._clear_todo(to_be_cleared)
        vectors = self.scan_qr._get_line_left_to_right(0)
        self.assertEqual(1, len(vectors))
        self.assertEqual(0, vectors[0].position.x)

    def test_cleartodo_fullline_horizontal_ok(self):
        to_be_cleared = LineSegment(5, 0, Position(0, 2))
        self.scan_qr._clear_todo(to_be_cleared)
        vectors = self.scan_qr._get_line_left_to_right(2)
        self.assertEqual(0, len(vectors))

    def test_cleartodo_line_vertical_ok(self):
        to_be_cleared = LineSegment(0, 3, Position(2, 0))
        self.scan_qr._clear_todo(to_be_cleared)
        vectors = self.scan_qr._get_line_left_to_right(0)
        self.assertEqual(2, len(vectors))
        self.assertEqual(0, vectors[0].position.x)
        self.assertEqual(3, vectors[1].position.x)

    def test_getvectors_returns_7vectors(self):
        vectors = self.scan_qr.get_vectors()
        self.assertEqual(7, len(vectors))


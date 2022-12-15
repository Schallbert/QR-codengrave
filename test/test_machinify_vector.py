import unittest
from datetime import timedelta

from bin.machinify_vector import MachinifyVector, Tool, EngraveParams
from bin.vectorize_qr import QrPathSegment, Point, Line, QrLineData, Direction


def set_simple_path_and_tool():
    tool = Tool()
    line = Line(Point(0, 0), Point(0, 21))
    v1 = QrLineData(True)
    v1._length = 7
    v2 = QrLineData(False)
    v2._length = 4
    v3 = QrLineData(True)
    v3._length = 2
    v4 = QrLineData(False)
    v4._length = 7
    v5 = QrLineData(True)
    v5._length = 0
    path = [QrPathSegment(line, [v1, v2, v4, v4, v5]), ]
    machinify = MachinifyVector(1.0)
    machinify.set_tool(tool)
    machinify.set_qr_path(path)
    machinify.set_xy_zero(Point(0, 0))
    machinify.set_engrave_params(EngraveParams())
    return machinify


class TesPublics(unittest.TestCase):

    def test_report_data_missing_qr_none_returns_correct_error(self):
        machinify = MachinifyVector(1.0)
        self.assertEqual('QR-code data', machinify.report_data_missing())

    def test_report_data_missing_tool_none_returns_correct_error(self):
        machinify = MachinifyVector(1.0)
        machinify.set_qr_path(1)
        self.assertEqual('Tool data', machinify.report_data_missing())

    def test_report_data_missing_engrave_none_returns_correct_error(self):
        machinify = MachinifyVector(1.0)
        machinify.set_qr_path(1)
        machinify.set_tool(1)
        self.assertEqual('Engrave parameters', machinify.report_data_missing())

    def test_report_data_missing_engrave_none_returns_correct_error(self):
        machinify = MachinifyVector(1.0)
        machinify.set_qr_path(1)
        machinify.set_tool(1)
        machinify.set_engrave_params(1)
        self.assertEqual('XY Zero offsets', machinify.report_data_missing())

    def test_report_data_missing_happy_path_returns_empty_string(self):
        machinify = MachinifyVector(1.0)
        machinify.set_qr_path(1)
        machinify.set_tool(1)
        machinify.set_engrave_params(1)
        machinify.set_xy_zero(1)
        self.assertEqual('', machinify.report_data_missing())

    def test_project_name_removes_web_identifiers_from_https(self):
        machinify = MachinifyVector(1.0)
        machinify.set_project_name('https://schallbert.de/')
        self.assertEqual('schallbert_de', machinify.get_project_name())

    def test_project_name_removes_web_identifiers_from_www(self):
        machinify = MachinifyVector(1.0)
        machinify.set_project_name('https://www.youtube.com/')
        self.assertEqual('youtube_com', machinify.get_project_name())

    def test_project_name_verylong_truncates_to_25(self):
        machinify = MachinifyVector(1.0)
        machinify.set_project_name('https://stackoverflow.com/questions/19924705/using-regular-expressions')
        self.assertEqual(25, len(machinify.get_project_name()))
        self.assertEqual('stackoverflow_comquestion', machinify.get_project_name())

    def test_duration_machinify_not_defined_returns_0(self):
        machinify = MachinifyVector(1.0)
        self.assertEqual(timedelta(seconds=0), machinify.get_job_duration_sec())

    def test_duration_machinify_5vect_length21_returns_4sec(self):
        machinify = set_simple_path_and_tool()
        t = Tool()
        e = EngraveParams()
        #  Touch every pixel (21^2) with feedXY, plus amount of Z-moves with feedZ of hover + engravedepth
        sec = (21 ** 2 * t.tip / t.fxy + 8 * (e.z_engrave + e.z_hover) / t.fz) * 60
        sec = timedelta(seconds=sec)
        sec -= timedelta(microseconds=sec.microseconds)
        self.assertEqual(sec, machinify.get_job_duration_sec())

    def test_dimensions_no_tool_defined_returns_0(self):
        machinify = MachinifyVector(1.0)
        self.assertEqual(tuple((0, 0)), machinify.get_dimension_info())

    def test_dimensions_machinify_length21_tool100um_returns2mm(self):
        machinify = set_simple_path_and_tool()
        t = Tool()
        self.assertEqual(tuple((21 * t.tip, 0.1)), machinify.get_dimension_info())

    def test_dimensions_machinify_length21_tool8mm_returns168mm(self):
        machinify = set_simple_path_and_tool()
        t = Tool(number=2, name='huge_tool', dia=8, fxy=4000, fz=2000, angle=0, tip=0)
        machinify.set_tool(t)
        self.assertEqual(tuple((21 * t.diameter, 8)), machinify.get_dimension_info())

    def test_linear_move_right_length7_tool100um_returns_x700um(self):
        machinify = set_simple_path_and_tool()
        vect = QrLineData(False, False)
        vect._length = 7
        self.assertEqual('X0.7', machinify._linear_move(vect, Direction.RIGHT))

    def test_linear_move_down_length0_tool100um_returns_x20mm(self):
        machinify = set_simple_path_and_tool()
        vect = QrLineData(True, True)
        vect._length = 200
        self.assertEqual('Y-20.0', machinify._linear_move(vect, Direction.DOWN))

    def test_linear_move_left_length1_tool100um_returns_xminus100um(self):
        machinify = set_simple_path_and_tool()
        vect = QrLineData(True, True)
        vect._length = 1
        self.assertEqual('X-0.1', machinify._linear_move(vect, Direction.LEFT))

    def test_linear_move_up_length0_tool100um_returns_0(self):
        machinify = set_simple_path_and_tool()
        vect = QrLineData(True, True)
        vect._length = 0
        self.assertEqual('Y0.0', machinify._linear_move(vect, Direction.UP))

    def test_linear_move_offset10mmy_up_length12_tool100um_returns_2200um(self):
        machinify = set_simple_path_and_tool()
        machinify._pos = Point(0, 1)
        vect = QrLineData(True, True)
        vect._length = 12
        self.assertEqual('Y2.2', machinify._linear_move(vect, Direction.UP))

    def test_linear_move_offset100mmy_left_length12_tool8mm_returns_neg96mm(self):
        machinify = set_simple_path_and_tool()
        t = Tool(number=2, name='huge_tool', dia=8, fxy=4000, fz=2000, angle=0, tip=0)
        machinify.set_tool(t)
        machinify._pos = Point(0, 100)
        vect = QrLineData(True, True)
        vect._length = 12
        self.assertEqual('X-96', machinify._linear_move(vect, Direction.LEFT))

    def test_move_engrave_up_length10_tool100um_returns_g01y1mm(self):
        machinify = set_simple_path_and_tool()
        vect = QrLineData(True, True)
        vect._length = 10
        self.assertEqual('G01 Y1.0 F1000\n', machinify._move(vect, Direction.UP))

    def test_move_hover_left_length10_tool100um_returns_g00xneg1mm(self):
        machinify = set_simple_path_and_tool()
        vect = QrLineData(False, True)
        vect._length = 10
        self.assertEqual('G00 X-1.0\n', machinify._move(vect, Direction.LEFT))


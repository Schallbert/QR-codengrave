import unittest
from datetime import timedelta

from src.platform.line_path import LinePath
from src.platform.machinify_vector import MachinifyVector, Tool, EngraveParams
from src.platform.vectorize_helper import LineSegment, Point, QrValueTable


def set_path_tool(tool):
    # 1 0 1 1 0
    # 0 1 1 0 0
    # 1 1 1 1 1
    # 0 0 0 0 1
    # 0 0 0 1 1
    sim_qr = QrValueTable()
    sim_qr.table[0, 0] = True
    sim_qr.table[0, 1] = False
    sim_qr.table[0, 2] = True
    sim_qr.table[0, 3] = True
    sim_qr.table[0, 4] = False
    sim_qr.table[1, 0] = False
    sim_qr.table[1, 1] = True
    sim_qr.table[1, 2] = True
    sim_qr.table[1, 3] = False
    sim_qr.table[1, 4] = False
    sim_qr.table[2, 0] = True
    sim_qr.table[2, 1] = True
    sim_qr.table[2, 2] = True
    sim_qr.table[2, 3] = True
    sim_qr.table[2, 4] = True
    sim_qr.table[3, 0] = False
    sim_qr.table[3, 1] = False
    sim_qr.table[3, 2] = False
    sim_qr.table[3, 3] = False
    sim_qr.table[3, 4] = True
    sim_qr.table[4, 0] = False
    sim_qr.table[4, 1] = False
    sim_qr.table[4, 2] = False
    sim_qr.table[4, 3] = True
    sim_qr.table[4, 4] = True
    sim_qr.size = 5
    scan_qr = LinePath(sim_qr)
    machinify = MachinifyVector(1.1)
    machinify.set_tool(tool)
    machinify.set_qr_path(scan_qr)
    machinify.set_xy_zero(Point(0, 0))
    machinify.set_engrave_params(EngraveParams())
    return machinify


class TestMachinify(unittest.TestCase):

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

    def test_report_data_missing_offsets_none_returns_correct_error(self):
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

    def test_duration_machinify_8vect_size5_returns_2sec(self):
        t = Tool(number=1, name='taper', dia=3.18, fxy=1000, fz=500, angle=90, tip=0.1)
        machinify = set_path_tool(t)
        self.assertEqual(timedelta(seconds=1), machinify.get_job_duration_sec())

    def test_dimensions_no_tool_defined_returns_0(self):
        machinify = MachinifyVector(1.0)
        self.assertEqual(tuple((0, 0)), machinify.get_dimension_info())

    def test_dimensions_machinify_length21_tool100um_returns2mm(self):
        t = Tool(number=1, name='taper', dia=3.18, fxy=1000, fz=500, angle=90, tip=0.1)
        machinify = set_path_tool(t)
        self.assertEqual(tuple((5 * t.tip, 0.1)), machinify.get_dimension_info())

    def test_dimensions_machinify_length21_tool8mm_returns168mm(self):
        t = Tool(number=2, name='huge_tool', dia=8, fxy=4000, fz=2000, angle=0, tip=0)
        machinify = set_path_tool(t)
        machinify.set_tool(t)
        self.assertEqual(tuple((5 * t.diameter, 8)), machinify.get_dimension_info())

    def test_engrave_length5_tool100um_returns500um(self):
        t = Tool(number=1, name='taper', dia=3.18, fxy=1000, fz=500, angle=90, tip=0.1)
        machinify = set_path_tool(t)
        machinify.set_tool(t)
        vector = LineSegment(5, 0, Point(0, 0))
        self.assertTrue('G01 X0.5 F1000\n' in machinify._engrave(vector))

    def test_engrave_length5_tool8mm_returns40mm(self):
        t = Tool(number=1, name='big', dia=8, fxy=1000, fz=500, angle=0, tip=0)
        machinify = set_path_tool(t)
        machinify.set_tool(t)
        vector = LineSegment(5, 0, Point(0, 0))
        self.assertTrue('G01 X40 F1000\n' in machinify._engrave(vector))

    def test_engrave_returns_offset_zero_returns_zero(self):
        machinify = set_path_tool(Tool())
        vector = LineSegment(2, 0, Point(0, 0))
        self.assertTrue('G00 X0 Y0\n' in machinify._engrave(vector))

    def test_engrave_returns_xypositioning(self):
        machinify = set_path_tool(Tool())
        vector = LineSegment(-5, 0, Point(9, 4))
        self.assertTrue('G00 X18 Y-8\n' in machinify._engrave(vector))

    def test_engrave_returns_g01negz_engrave_param(self):
        machinify = set_path_tool(Tool())
        vector = LineSegment(2, 0, Point(0, 0))
        self.assertTrue('G01 Z-0.4 F500\n' in machinify._engrave(vector))

    def test_engrave_returns_linearmovecommand(self):
        machinify = set_path_tool(Tool())
        vector = LineSegment(-5, 0, Point(9, 4))
        self.assertTrue('G01 X8 F1000\n' in machinify._engrave(vector))

    def test_engrave_returns_g00z_hover_param(self):
        machinify = set_path_tool(Tool())
        vector = LineSegment(2, 0, Point(0, 0))
        self.assertTrue('G00 Z0.5\n' in machinify._engrave(vector))

    def test_gcode_engrave_dummyqr_offset_returns_correct_path_offsets(self):
        machinify = set_path_tool(Tool())
        xy0 = Point(6.21, -17.21)
        machinify.set_xy_zero(xy0)
        self.assertTrue('G00 X6.21 Y-17.21\n' in machinify._gcode_engrave())

    def test_gcode_engrave_dummyqr_returns_correct_string(self):
        machinify = set_path_tool(Tool())
        self.assertEqual('G00 X0 Y0\n'
                         'G01 Z-0.4 F500\n'
                         'G00 Z0.5\n'
                         'G00 X4 Y0\n'
                         'G01 Z-0.4 F500\n'
                         'G01 Y-4 F1000\n'
                         'G00 Z0.5\n'
                         'G00 X6 Y0\n'
                         'G01 Z-0.4 F500\n'
                         'G00 Z0.5\n'
                         'G00 X2 Y-2\n'
                         'G01 Z-0.4 F500\n'
                         'G01 Y-4 F1000\n'
                         'G00 Z0.5\n'
                         'G00 X0 Y-4\n'
                         'G01 Z-0.4 F500\n'
                         'G00 Z0.5\n'
                         'G00 X6 Y-4\n'
                         'G01 Z-0.4 F500\n'
                         'G01 X8 F1000\n'
                         'G00 Z0.5\n'
                         'G00 X8 Y-6\n'
                         'G01 Z-0.4 F500\n'
                         'G01 Y-8 F1000\n'
                         'G00 Z0.5\n'
                         'G00 X6 Y-8\n'
                         'G01 Z-0.4 F500\n'
                         'G00 Z0.5\n', machinify._gcode_engrave())

    def test_gcode_prepare_sets_correct_tool_number(self):
        tool = Tool(4, 'TestTool', 8, 5200, 2600, 20000)
        engrave_params = EngraveParams(0.5, 1, 10)
        xy0 = Point(5, -5)
        machinify = MachinifyVector(1.0)
        machinify.set_tool(tool)
        machinify.set_xy_zero(xy0)
        machinify.set_engrave_params(engrave_params)
        self.assertEqual('G90 \n'
                         'MSG "Tool: ' + tool.get_description() + '"\n'
                         'T' + str(tool.number) + '\n'
                         'M06 \n'
                         'M03 \n'
                         'S' + str(tool.speed) + '\n', machinify._gcode_prepare().split('G00')[0])

    def test_gcode_prepare_sets_correct_engrave_parameters(self):
        tool = Tool(4, 'TestTool', 8, 5200, 2600, 20000)
        engrave_params = EngraveParams(0.5, 1, 10)
        xy0 = Point(5, -5)
        machinify = MachinifyVector(1.0)
        machinify.set_tool(tool)
        machinify.set_xy_zero(xy0)
        machinify.set_engrave_params(engrave_params)
        self.assertEqual('G00 Z' + str(engrave_params.z_flyover) + '\n\n'
                         'G00 Y0 X0 \n'
                         'G00 X' + str(xy0.x) + ' Y' + str(xy0.y) + ' \n'
                         'G00 Z' + str(engrave_params.z_hover) + '\n\n',
                         machinify._gcode_prepare().split('S' + str(tool.speed) + '\n')[1])

    def test_gcode_finalize_returns_to_xy0_stops_spindle(self):
        engrave_params = EngraveParams(0.5, 1, 10)
        machinify = MachinifyVector(1.0)
        machinify.set_engrave_params(engrave_params)
        self.assertEqual('\nM05 \n'
                         'G00 Z' + str(engrave_params.z_flyover) + '\n'
                         'G00 Y0 X0 \n'
                         'M30 \n', machinify._gcode_finalize())

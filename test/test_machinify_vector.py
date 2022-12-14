import unittest

from bin.machinify_vector import MachinifyVector


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



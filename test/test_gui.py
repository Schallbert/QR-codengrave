import unittest
from unittest.mock import patch

from src.platform.machinify_vector import Tool
from src.gui.gui_tool_configure import GuiConfigureTool


class TestIntegrationCongigureTool(unittest.TestCase):

    @patch('src.gui.gui_tool_manage.GuiToolManager')
    def test_validate_entries_already_existing_tool_as_input_returns_true(self, mock_guitoolmanager):
        tool = Tool(2, 'Test', 4, 1200, 600, 24000)
        config_tool = GuiConfigureTool(None, mock_guitoolmanager, {'padx': 5, 'pady': 5}, tool)
        config_tool._ok_button_clicked()
        mock_guitoolmanager.add_or_edit_tool.assert_called_with(tool)

    @patch('src.gui.gui_tool_manage.GuiToolManager')
    def test_validate_entries_no_tool_as_input_returns_true(self, mock_guitoolmanager):
        tool = Tool()
        config_tool = GuiConfigureTool(None, mock_guitoolmanager, {'padx': 5, 'pady': 5})
        config_tool._ok_button_clicked()
        mock_guitoolmanager.add_or_edit_tool.assert_called_with(tool)

    @patch('src.gui.gui_tool_manage.GuiToolManager')
    def test_validate_entries_invalid_tool_returns_errors(self, mock_guitoolmanager):
        tool = Tool(0, 'Invalid', 0, 0, 0, 0, 18, -1)
        config_tool = GuiConfigureTool(None, mock_guitoolmanager, {'padx': 5, 'pady': 5}, tool)
        config_tool._ok_button_clicked()
        mock_guitoolmanager.add_or_edit_tool.assert_not_called()

class TestIntegrationConfigureEngrave(unittest.TestCase):
    @patch('src.gui.gui_tool_manage.GuiToolManager')
    def test_validate_entries_invalid_tool_returns_errors(self, mock_guitoolmanager):

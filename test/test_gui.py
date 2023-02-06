import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock

from src.helpers.gui_helpers import MsgBox
from src.platform.vectorize_helper import Point
from src.platform.machinify_vector import Tool, ToolList, EngraveParams

from src.gui.gui_tool_configure import GuiConfigureTool
from src.gui.gui_engrave_configure import GuiEngraveConfigure
from src.gui.gui_xy0_configure import GuiConfigureXy0, Offset

from src.gui.gui_tool_manage import GuiToolManager
from src.gui.gui_engrave_manage import GuiEngraveManager
from src.gui.gui_xy0_manage import GuiXy0Manager


class TestIntegrationConfigureTool(unittest.TestCase):
    @patch('src.gui.gui_tool_manage.GuiToolManager')
    def setUp(self, mock_guitoolmanager):
        tk.Tk()  # required to have tk variables properly instantiated
        self.mock_guitoolmanager = mock_guitoolmanager
        self.mock_msg = MsgBox()
        self.mock_msg.showinfo = MagicMock()
        self.config_tool = GuiConfigureTool(self.mock_guitoolmanager, self.mock_msg, {'padx': 5, 'pady': 5})

    def test_add_edit_tool_existing_tool_returns_tool(self):
        tool = Tool(2, 'Test', 4, 1200, 600, 24000)
        self.config_tool.set_tool(tool)
        self.config_tool._ok_button_clicked()
        self.mock_guitoolmanager.add_or_edit_tool.assert_called_with(tool)

    def test_add_edit_tool_no_tool_returns_default(self):
        tool = Tool()
        self.config_tool._ok_button_clicked()
        self.mock_guitoolmanager.add_or_edit_tool.assert_called_with(tool)

    def test_add_edit_tool_invalidtoolnr_shows_warning(self):
        tool = Tool(0, 'Invalid', 3, 1000, 2000, 24000, 0, 0)
        self.config_tool.set_tool(tool)
        self.config_tool._ok_button_clicked()
        self.mock_msg.showinfo.assert_called()

    def test_add_edit_tool_invaliddiameter_shows_warning(self):
        tool = Tool(1, 'Invalid', -3, 1000, 2000, 24000, 0, 0)
        self.config_tool.set_tool(tool)
        self.config_tool._ok_button_clicked()
        self.mock_msg.showinfo.assert_called()

    def test_add_edit_tool_invalidfeed_shows_warning(self):
        tool = Tool(1, 'Invalid', 2, 0, 2000, 24000, 0, 0)
        self.config_tool.set_tool(tool)
        self.config_tool._ok_button_clicked()
        self.mock_msg.showinfo.assert_called()

    def test_add_edit_tool_invalidzfeed_shows_warning(self):
        tool = Tool(1, 'Invalid', 2, 2000, -5, 24000, 0, 0)
        self.config_tool.set_tool(tool)
        self.config_tool._ok_button_clicked()
        self.mock_msg.showinfo.assert_called()

    def test_add_edit_tool_invalidspeedd_shows_warning(self):
        tool = Tool(1, 'Invalid', 2, 2000, 1000, -1, 0, 0)
        self.config_tool.set_tool(tool)
        self.config_tool._ok_button_clicked()
        self.mock_msg.showinfo.assert_called()

    def test_add_edit_tool_invalidangle_shows_warning(self):
        tool = Tool(1, 'Invalid', 2, 2000, 1000, 24000, 182, 0)
        self.config_tool.set_tool(tool)
        self.config_tool._ok_button_clicked()
        self.mock_msg.showinfo.assert_called()

    def test_add_edit_tool_invalidtip_shows_warning(self):
        tool = Tool(1, 'Invalid', 2, 2000, 1000, 24000, 90, -1)
        self.config_tool.set_tool(tool)
        self.config_tool._ok_button_clicked()
        self.mock_msg.showinfo.assert_called()


class TestIntegrationConfigureEngraveParameters(unittest.TestCase):
    @patch('src.gui.gui_engrave_manage.GuiEngraveManager')
    def setUp(self, mock_guiengravemanager):
        tk.Tk()  # required to have tk variables properly instantiated
        self.mock_guiengravemanager = mock_guiengravemanager
        self.mock_msg = MsgBox()
        self.mock_msg.showinfo = MagicMock()
        self.mock_msg.error = MagicMock()
        self.config_engrave = GuiEngraveConfigure(self.mock_guiengravemanager,
                                                  self.mock_msg, {'padx': 5, 'pady': 5})

    def test_validate_entries_already_existing_engraveparams_returns_true(self):
        params = EngraveParams(1, 1, 10)
        self.config_engrave.set_params(params)
        self.config_engrave._ok_button_clicked()
        self.mock_guiengravemanager.set_engrave_parameters.assert_called_with(params)

    def test_validate_entries_default_engraveparams_returns_true(self):
        params = EngraveParams()
        self.config_engrave.set_params(params)
        self.config_engrave._ok_button_clicked()
        self.mock_guiengravemanager.set_engrave_parameters.assert_called_with(params)

    def test_validate_entries_invalidinput_shows_warning(self):
        params = EngraveParams(1, 0.1, 20)
        self.config_engrave.set_params(params)
        self.config_engrave._engrave.set('Only doubles allowed here')
        self.config_engrave._ok_button_clicked()
        self.mock_msg.error.assert_called()

    def test_validate_entries_invalidzhover_shows_warning(self):
        params = EngraveParams(1, 0.1, 20)
        self.config_engrave.set_params(params)
        self.config_engrave._ok_button_clicked()
        self.mock_msg.showinfo.assert_called()

    def test_validate_entries_invalidflyover_shows_warning(self):
        params = EngraveParams(1, 1, 0)
        self.config_engrave.set_params(params)
        self.config_engrave._ok_button_clicked()
        self.mock_msg.showinfo.assert_called()


class TestXy0Configure(unittest.TestCase):
    @patch('src.gui.gui_xy0_manage.GuiXy0Manager')
    def setUp(self, mock_guixy0manager):
        tk.Tk()  # required to have tk variables properly instantiated
        self.mock_guixy0manager = mock_guixy0manager
        self.mock_msg = MsgBox()
        self.mock_msg.error = MagicMock()
        self.config_xy0 = GuiConfigureXy0(self.mock_guixy0manager, self.mock_msg, {'padx': 5, 'pady': 5})

    def test_setxy0_topleft_calculates_correctly(self):
        qr = 10
        d = 1
        offset = Offset.TOPLEFT
        expect = Point(d / 2, -d / 2)
        self.config_xy0.set_params(qr, d, Point())
        self.assertEqual(self.config_xy0._get_xy_offset(offset), expect)

    def test_setxy0_topright_calculates_correctly(self):
        d = 1
        qr = 10
        offset = Offset.TOPRIGHT
        expect = Point(d / 2 - qr, -d / 2)
        self.config_xy0.set_params(qr, d, Point())
        self.assertEqual(self.config_xy0._get_xy_offset(offset), expect)

    def test_setxy0_bottomleft_calculates_correctly(self):
        d = 1
        qr = 10
        offset = Offset.BOTTOMLEFT
        expect = Point(d / 2, qr - d / 2)
        self.config_xy0.set_params(qr, d, Point())
        self.assertEqual(self.config_xy0._get_xy_offset(offset), expect)

    def test_setxy0_bottomright_calculates_correctly(self):
        d = 1
        qr = 10
        offset = Offset.BOTTOMRIGHT
        expect = Point(d / 2 - qr, qr - d / 2)
        self.config_xy0.set_params(qr, d, Point())
        self.assertEqual(self.config_xy0._get_xy_offset(offset), expect)

    def test_setxy0_center_calculates_correctly(self):
        d = 1
        qr = 10
        offset = Offset.CENTER
        expect = Point(d / 2 - qr / 2, qr / 2 - d / 2)
        self.config_xy0.set_params(qr, d, Point())
        self.assertEqual(self.config_xy0._get_xy_offset(offset), expect)

    def test_setxy0_custom_calculates_correctly(self):
        expect = Point(40, 20)
        self.config_xy0._setx0.set(expect.x)
        self.config_xy0._sety0.set(expect.y)
        self.config_xy0._ok_button_clicked()
        self.mock_guixy0manager.set_xy0_parameters.assert_called_with(expect)

    def test_setxy0_already_existing_input_returns_correctly(self):
        expect = Point(-50, -100)
        self.config_xy0.set_params(10, 1, expect)
        self.config_xy0._ok_button_clicked()
        self.mock_guixy0manager.set_xy0_parameters.assert_called_with(expect)

    def test_invalid_input_textbox_shows_error(self):
        self.config_xy0._setx0.set('only_doubles_are_valid_here')
        self.config_xy0._validate_entries()
        self.mock_msg.error.assert_called()


class TestXy0Manage(unittest.TestCase):
    def setUp(self):
        self.mock_msg = MsgBox()
        self.mock_msg.showinfo = MagicMock()

    def test_setxy0_preconditions_not_met_shows_warning(self):
        xy0_manage = GuiXy0Manager(None, self.mock_msg, Point(), {'padx': 5, 'pady': 5})
        xy0_manage._label_clicked()
        self.mock_msg.showinfo.assert_called()


class TestIntegrationMain(unittest.TestCase):
    """The following test simulate a callback from the respective child windows of ToolManager, EngraveManager,
    XY0Manager and check whether the data is correctly stored and the main app updated so the changes are
    propagated."""

    @patch('src.gui.gui.App')
    @patch('builtins.open', create=True)
    def setUp(self, mock_main, mock_open):
        self.mock_main = mock_main

    def test_add_tool_updates_status(self):
        tool = Tool(4, 'TestTool', 6, 3500, 1800, 24000)
        tool_manage = GuiToolManager(self.mock_main, None, ToolList(), {'padx': 5, 'pady': 5})
        tool_manage.add_or_edit_tool(tool)

        tool_manage._tool_list.select_tool(4)
        self.assertEqual(tool.diameter, tool_manage.get_selected_tool().diameter)

        self.mock_main.update_status.assert_called()

    def test_update_tool_updates_status(self):
        tool_manage = GuiToolManager(self.mock_main, None, ToolList(), {'padx': 5, 'pady': 5})

        tool = Tool(4, 'TestTool', 6, 3500, 1800, 24000)
        tool_manage.add_or_edit_tool(tool)

        tool = Tool(4, 'TestTool', 8, 3500, 1800, 24000)
        tool_manage.add_or_edit_tool(tool)
        tool_manage._tool_list.select_tool(4)
        self.assertEqual(tool.diameter, tool_manage.get_selected_tool().diameter)

        self.mock_main.update_status.assert_called()

    def test_remove_tool_updates_status(self):
        tool = Tool(4, 'TestTool', 8, 3500, 1800, 24000)
        tool_manage = GuiToolManager(self.mock_main, None, ToolList(), {'padx': 5, 'pady': 5})
        tool_manage.add_or_edit_tool(tool)

        self.assertTrue(tool_manage._tool_list.is_tool_in_list(4))
        tool_manage._tool_list.select_tool(4)
        # update field in qui
        tool_manage.tool_selection.set(tool_manage._tool_list.get_selected_tool_description())
        tool_manage._remove_tool_button_clicked()
        self.assertFalse(tool_manage._tool_list.is_tool_in_list(4))
        self.mock_main.update_status.assert_called()

    def test_set_default_engrave_params_updates_status(self):
        params = EngraveParams()
        engrave_manage = GuiEngraveManager(self.mock_main, None, EngraveParams(), {'padx': 5, 'pady': 5})
        engrave_manage.set_engrave_parameters(params)

        self.assertEqual(params.z_engrave, engrave_manage.get_engrave_parameters().z_engrave)
        self.assertEqual(params.z_hover, engrave_manage.get_engrave_parameters().z_hover)
        self.assertEqual(params.z_flyover, engrave_manage.get_engrave_parameters().z_flyover)
        self.mock_main.update_status.assert_called()

    def test_set_custom_engrave_params_updates_status(self):
        params = EngraveParams(2, 2, 20)
        engrave_manage = GuiEngraveManager(self.mock_main, None, EngraveParams(), {'padx': 5, 'pady': 5})
        engrave_manage.set_engrave_parameters(params)

        self.assertEqual(params.z_engrave, engrave_manage.get_engrave_parameters().z_engrave)
        self.assertEqual(params.z_hover, engrave_manage.get_engrave_parameters().z_hover)
        self.assertEqual(params.z_flyover, engrave_manage.get_engrave_parameters().z_flyover)
        self.mock_main.update_status.assert_called()

    def test_update_xy0_updates_status(self):
        params = Point(2, 4)
        xy0_manage = GuiXy0Manager(self.mock_main, None, Point(), {'padx': 5, 'pady': 5})
        xy0_manage.set_xy0_parameters(params)

        self.assertEqual(params.x, xy0_manage.get_xy0_parameters().x)
        self.assertEqual(params.y, xy0_manage.get_xy0_parameters().y)
        self.mock_main.update_status.assert_called()

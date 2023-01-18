import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock

from src.helpers.gui_helpers import MsgBox
from src.platform.vectorize_qr import Point
from src.platform.machinify_vector import Tool, EngraveParams
from src.helpers.persistence import Persistence

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
        Persistence.set_mock_msgbox(self.mock_msg)
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
        Persistence.set_mock_msgbox(self.mock_msg)
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
    def setUp(self):
        tk.Tk()  # required to have tk variables properly instantiated
        self.mock_msg = MsgBox()
        self.mock_msg.error = MagicMock()
        Persistence.set_mock_msgbox(self.mock_msg)

    @patch('src.gui.gui_xy0_manage.GuiXy0Manager')
    def test_setxy0_topleft_calculates_correctly(self, mock_guixy0manager):
        d = 1
        qr = 10
        offset = Offset.TOPLEFT
        expect = Point(d / 2, -d / 2)
        config_xy0 = GuiConfigureXy0(None, mock_guixy0manager, None, {'padx': 5, 'pady': 5}, (qr, d))
        config_xy0._xy_option.set(offset)
        config_xy0._radiobutton_selection_changed()
        config_xy0._ok_button_clicked()
        mock_guixy0manager.set_xy0_parameters.assert_called_with(expect)

    @patch('src.gui.gui_xy0_manage.GuiXy0Manager')
    def test_setxy0_topright_calculates_correctly(self, mock_guixy0manager):
        d = 1
        qr = 10
        offset = Offset.TOPRIGHT
        expect = Point(d / 2 - qr, -d / 2)
        config_xy0 = GuiConfigureXy0(None, mock_guixy0manager, None, {'padx': 5, 'pady': 5}, (qr, d))
        config_xy0._xy_option.set(offset)
        config_xy0._radiobutton_selection_changed()
        config_xy0._ok_button_clicked()
        mock_guixy0manager.set_xy0_parameters.assert_called_with(expect)

    @patch('src.gui.gui_xy0_manage.GuiXy0Manager')
    def test_setxy0_bottomleft_calculates_correctly(self, mock_guixy0manager):
        d = 1
        qr = 10
        offset = Offset.BOTTOMLEFT
        expect = Point(d / 2, qr - d / 2)
        config_xy0 = GuiConfigureXy0(None, mock_guixy0manager, None, {'padx': 5, 'pady': 5}, (qr, d))
        config_xy0._xy_option.set(offset)
        config_xy0._radiobutton_selection_changed()
        config_xy0._ok_button_clicked()
        mock_guixy0manager.set_xy0_parameters.assert_called_with(expect)

    @patch('src.gui.gui_xy0_manage.GuiXy0Manager')
    def test_setxy0_bottomright_calculates_correctly(self, mock_guixy0manager):
        d = 1
        qr = 10
        offset = Offset.BOTTOMRIGHT
        expect = Point(d / 2 - qr, qr - d / 2)
        config_xy0 = GuiConfigureXy0(None, mock_guixy0manager, None, {'padx': 5, 'pady': 5}, (qr, d))
        config_xy0._xy_option.set(offset)
        config_xy0._radiobutton_selection_changed()
        config_xy0._ok_button_clicked()
        mock_guixy0manager.set_xy0_parameters.assert_called_with(expect)

    @patch('src.gui.gui_xy0_manage.GuiXy0Manager')
    def test_setxy0_center_calculates_correctly(self, mock_guixy0manager):
        d = 1
        qr = 10
        offset = Offset.CENTER
        expect = Point(d / 2 - qr / 2, qr / 2 - d / 2)
        config_xy0 = GuiConfigureXy0(None, mock_guixy0manager, None, {'padx': 5, 'pady': 5}, (qr, d))
        config_xy0._xy_option.set(offset)
        config_xy0._radiobutton_selection_changed()
        config_xy0._ok_button_clicked()
        mock_guixy0manager.set_xy0_parameters.assert_called_with(expect)

    @patch('src.gui.gui_xy0_manage.GuiXy0Manager')
    def test_setxy0_custom_calculates_correctly(self, mock_guixy0manager):
        d = 2
        qr = 20
        offset = Offset.CUSTOM
        expect = Point(40, 20)
        config_xy0 = GuiConfigureXy0(None, mock_guixy0manager, None, {'padx': 5, 'pady': 5}, (qr, d))
        config_xy0._xy_option.set(offset)
        config_xy0._setx0.set(expect.x)
        config_xy0._sety0.set(expect.y)
        config_xy0._radiobutton_selection_changed()
        config_xy0._ok_button_clicked()
        mock_guixy0manager.set_xy0_parameters.assert_called_with(expect)

    @patch('src.gui.gui_xy0_manage.GuiXy0Manager')
    def test_setxy0_already_existing_input_returns_correctly(self, mock_guixy0manager):
        d = 2
        qr = 20
        offset = Offset.CUSTOM
        expect = Point(-50, -100)
        config_xy0 = GuiConfigureXy0(None, mock_guixy0manager, None, {'padx': 5, 'pady': 5}, (qr, d), expect)
        config_xy0._xy_option.set(offset)
        config_xy0._setx0.set(expect.x)
        config_xy0._sety0.set(expect.y)
        config_xy0._radiobutton_selection_changed()
        config_xy0._ok_button_clicked()
        mock_guixy0manager.set_xy0_parameters.assert_called_with(expect)

    def test_invalid_input_textbox_shows_error(self):
        config_xy0 = GuiConfigureXy0(None, None, self.mock_msg, {'padx': 5, 'pady': 5}, (10, 1))
        config_xy0._setx0.set('only_doubles_are_valid_here')
        config_xy0._validate_entries()
        self.mock_msg.error.assert_called()


class TestXy0Manage(unittest.TestCase):
    def setUp(self):
        self.mock_msg = MsgBox()
        self.mock_msg.showinfo = MagicMock()
        Persistence.set_mock_msgbox(self.mock_msg)

    def test_setxy0_preconditions_not_met_shows_warning(self):
        xy0_manage = GuiXy0Manager(None, self.mock_msg, {'padx': 5, 'pady': 5})
        xy0_manage._label_clicked()
        self.mock_msg.showinfo.assert_called()


class TestIntegrationMain(unittest.TestCase):
    """The following test simulate a callback from the respective child windows of ToolManager, EngraveManager,
    XY0Manager and check whether the data is correctly stored and the main app updated so the changes are
    propagated."""

    @patch('src.gui.gui.App')
    def test_add_tool_updates_status(self, mock_main):
        tool = Tool(4, 'TestTool', 6, 3500, 1800, 24000)
        tool_manage = GuiToolManager(mock_main, None, {'padx': 5, 'pady': 5})
        tool_manage.add_or_edit_tool(tool)

        tool_manage._tool_list.select_tool(4)
        self.assertEqual(tool.diameter, tool_manage.get_selected_tool().diameter)

        mock_main.update_status.assert_called()

    @patch('src.gui.gui.App')
    def test_update_tool_updates_status(self, mock_main):
        tool_manage = GuiToolManager(mock_main, None, {'padx': 5, 'pady': 5})

        tool = Tool(4, 'TestTool', 6, 3500, 1800, 24000)
        tool_manage.add_or_edit_tool(tool)

        tool = Tool(4, 'TestTool', 8, 3500, 1800, 24000)
        tool_manage.add_or_edit_tool(tool)
        tool_manage._tool_list.select_tool(4)
        self.assertEqual(tool.diameter, tool_manage.get_selected_tool().diameter)

        mock_main.update_status.assert_called()

    @patch('src.gui.gui.App')
    def test_remove_tool_updates_status(self, mock_main):
        tool = Tool(4, 'TestTool', 8, 3500, 1800, 24000)
        tool_manage = GuiToolManager(mock_main, None, {'padx': 5, 'pady': 5})
        tool_manage.add_or_edit_tool(tool)

        self.assertTrue(tool_manage._tool_list.is_tool_in_list(4))
        tool_manage._tool_list.select_tool(4)
        # update field in qui
        tool_manage.tool_selection.set(tool_manage._tool_list.get_selected_tool_description())
        tool_manage._remove_tool_button_clicked()
        self.assertFalse(tool_manage._tool_list.is_tool_in_list(4))
        mock_main.update_status.assert_called()

    @patch('src.gui.gui.App')
    def test_set_default_engrave_params_updates_status(self, mock_main):
        params = EngraveParams()
        engrave_manage = GuiEngraveManager(mock_main, None, {'padx': 5, 'pady': 5})
        engrave_manage.set_engrave_parameters(params)

        self.assertEqual(params.z_engrave, engrave_manage.get_engrave_parameters().z_engrave)
        self.assertEqual(params.z_hover, engrave_manage.get_engrave_parameters().z_hover)
        self.assertEqual(params.z_flyover, engrave_manage.get_engrave_parameters().z_flyover)
        mock_main.update_status.assert_called()

    @patch('src.gui.gui.App')
    def test_set_custom_engrave_params_updates_status(self, mock_main):
        params = EngraveParams(2, 2, 20)
        engrave_manage = GuiEngraveManager(mock_main, None, {'padx': 5, 'pady': 5})
        engrave_manage.set_engrave_parameters(params)

        self.assertEqual(params.z_engrave, engrave_manage.get_engrave_parameters().z_engrave)
        self.assertEqual(params.z_hover, engrave_manage.get_engrave_parameters().z_hover)
        self.assertEqual(params.z_flyover, engrave_manage.get_engrave_parameters().z_flyover)
        mock_main.update_status.assert_called()

    @patch('src.gui.gui.App')
    def test_update_xy0_updates_status(self, mock_main):
        params = Point(2, 4)
        xy0_manage = GuiXy0Manager(mock_main, None, {'padx': 5, 'pady': 5})
        xy0_manage.set_xy0_parameters(params)

        self.assertEqual(params.x, xy0_manage.get_xy0_parameters().x)
        self.assertEqual(params.y, xy0_manage.get_xy0_parameters().y)
        mock_main.update_status.assert_called()

    @patch('src.gui.gui.App')
    def test_setxy0_happy_path_updates_status(self, mock_main):
        xy0_manage = GuiXy0Manager(mock_main, None, {'padx': 5, 'pady': 5})
        xy0_manage.set_dimension_info((10, 1))
        xy0_manage._label_clicked()
        mock_main.update_status.assert_called()

import unittest
from unittest.mock import patch

from src.platform.vectorize_qr import Point
from src.platform.machinify_vector import Tool, EngraveParams

from src.gui.gui_tool_configure import GuiConfigureTool
from src.gui.gui_engrave_configure import GuiEngraveConfigure
from src.gui.gui_xy0_configure import GuiConfigureXy0, Offset

from src.gui.gui_tool_manage import GuiToolManager
from src.gui.gui_engrave_manage import GuiEngraveManager
from src.gui.gui_xy0_manage import GuiXy0Manager


class TestIntegrationCongigureTool(unittest.TestCase):

    @patch('src.gui.gui_tool_manage.GuiToolManager')
    def test_add_edit_tool_existing_tool_returns_tool(self, mock_guitoolmanager):
        tool = Tool(2, 'Test', 4, 1200, 600, 24000)
        config_tool = GuiConfigureTool(None, mock_guitoolmanager, {'padx': 5, 'pady': 5}, tool)
        config_tool._ok_button_clicked()
        mock_guitoolmanager.add_or_edit_tool.assert_called_with(tool)

    @patch('src.gui.gui_tool_manage.GuiToolManager')
    def test_add_edit_tool_no_tool_returns_default(self, mock_guitoolmanager):
        tool = Tool()
        config_tool = GuiConfigureTool(None, mock_guitoolmanager, {'padx': 5, 'pady': 5})
        config_tool._ok_button_clicked()
        mock_guitoolmanager.add_or_edit_tool.assert_called_with(tool)

    @patch('src.gui.gui_tool_manage.GuiToolManager')
    def test_add_edit_tool_invalidtoolnr_returns_false(self, mock_guitoolmanager):
        tool = Tool(0, 'Invalid', 3, 1000, 2000, 24000, 0, 0)
        config_tool = GuiConfigureTool(None, mock_guitoolmanager, {'padx': 5, 'pady': 5}, tool)
        config_tool._ok_button_clicked()
        mock_guitoolmanager.add_or_edit_tool.assert_not_called()

    @patch('src.gui.gui_tool_manage.GuiToolManager')
    def test_add_edit_tool_invaliddiameter_returns_false(self, mock_guitoolmanager):
        tool = Tool(1, 'Invalid', -3, 1000, 2000, 24000, 0, 0)
        config_tool = GuiConfigureTool(None, mock_guitoolmanager, {'padx': 5, 'pady': 5}, tool)
        config_tool._ok_button_clicked()
        mock_guitoolmanager.add_or_edit_tool.assert_not_called()

    @patch('src.gui.gui_tool_manage.GuiToolManager')
    def test_add_edit_tool_invalidfeed_returns_false(self, mock_guitoolmanager):
        tool = Tool(1, 'Invalid', 2, 0, 2000, 24000, 0, 0)
        config_tool = GuiConfigureTool(None, mock_guitoolmanager, {'padx': 5, 'pady': 5}, tool)
        config_tool._ok_button_clicked()
        mock_guitoolmanager.add_or_edit_tool.assert_not_called()

    @patch('src.gui.gui_tool_manage.GuiToolManager')
    def test_add_edit_tool_invalidzfeed_returns_false(self, mock_guitoolmanager):
        tool = Tool(1, 'Invalid', 2, 2000, -5, 24000, 0, 0)
        config_tool = GuiConfigureTool(None, mock_guitoolmanager, {'padx': 5, 'pady': 5}, tool)
        config_tool._ok_button_clicked()
        mock_guitoolmanager.add_or_edit_tool.assert_not_called()

    @patch('src.gui.gui_tool_manage.GuiToolManager')
    def test_add_edit_tool_invalidspeed_returns_false(self, mock_guitoolmanager):
        tool = Tool(1, 'Invalid', 2, 2000, 1000, -1, 0, 0)
        config_tool = GuiConfigureTool(None, mock_guitoolmanager, {'padx': 5, 'pady': 5}, tool)
        config_tool._ok_button_clicked()
        mock_guitoolmanager.add_or_edit_tool.assert_not_called()

    @patch('src.gui.gui_tool_manage.GuiToolManager')
    def test_add_edit_tool_invalidangle_returns_false(self, mock_guitoolmanager):
        tool = Tool(1, 'Invalid', 2, 2000, 1000, 24000, 182, 0)
        config_tool = GuiConfigureTool(None, mock_guitoolmanager, {'padx': 5, 'pady': 5}, tool)
        config_tool._ok_button_clicked()
        mock_guitoolmanager.add_or_edit_tool.assert_not_called()

    @patch('src.gui.gui_tool_manage.GuiToolManager')
    def test_add_edit_tool_invalidtip_returns_false(self, mock_guitoolmanager):
        tool = Tool(1, 'Invalid', 2, 2000, 1000, 24000, 90, -1)
        config_tool = GuiConfigureTool(None, mock_guitoolmanager, {'padx': 5, 'pady': 5}, tool)
        config_tool._ok_button_clicked()
        mock_guitoolmanager.add_or_edit_tool.assert_not_called()


class TestIntegrationCongigureEngraveParameters(unittest.TestCase):
    @patch('src.gui.gui_engrave_manage.GuiEngraveManager')
    def test_validate_entries_already_existing_engraveparams_returns_true(self, mock_guiengravemanager):
        params = EngraveParams(1, 1, 10)
        config_engrave = GuiEngraveConfigure(None, mock_guiengravemanager, {'padx': 5, 'pady': 5}, params)
        config_engrave._ok_button_clicked()
        mock_guiengravemanager.set_engrave_parameters.assert_called_with(params)

    @patch('src.gui.gui_engrave_manage.GuiEngraveManager')
    def test_validate_entries_default_engraveparams_returns_true(self, mock_guiengravemanager):
        params = EngraveParams()
        config_engrave = GuiEngraveConfigure(None, mock_guiengravemanager, {'padx': 5, 'pady': 5}, params)
        config_engrave._ok_button_clicked()
        mock_guiengravemanager.set_engrave_parameters.assert_called_with(params)

    @patch('src.gui.gui_engrave_manage.GuiEngraveManager')
    def test_validate_entries_invalidzhover_returns_false(self, mock_guiengravemanager):
        params = EngraveParams(1, 0.1, 20)
        config_engrave = GuiEngraveConfigure(None, mock_guiengravemanager, {'padx': 5, 'pady': 5}, params)
        config_engrave._ok_button_clicked()
        mock_guiengravemanager.set_engrave_parameters.assert_not_called()

    @patch('src.gui.gui_engrave_manage.GuiEngraveManager')
    def test_validate_entries_invalidflyover_returns_false(self, mock_guiengravemanager):
        params = EngraveParams(1, 1, 0)
        config_engrave = GuiEngraveConfigure(None, mock_guiengravemanager, {'padx': 5, 'pady': 5}, params)
        config_engrave._ok_button_clicked()
        mock_guiengravemanager.set_engrave_parameters.assert_not_called()


class TestXy0Configure(unittest.TestCase):
    @patch('src.gui.gui_xy0_manage.GuiXy0Manager')
    def test_setxy0_topleft_calculates_correctly(self, mock_guixy0manager):
        d = 1
        qr = 10
        offset = Offset.TOPLEFT
        expect = Point(d/2, -d/2)
        config_xy0 = GuiConfigureXy0(None, mock_guixy0manager, {'padx': 5, 'pady': 5}, (qr, d))
        config_xy0._xy_option.set(offset)
        config_xy0._radiobutton_selection_changed()
        config_xy0._ok_button_clicked()

        mock_guixy0manager.set_xy0_parameters.assert_called_with(expect)

    @patch('src.gui.gui_xy0_manage.GuiXy0Manager')
    def test_setxy0_topright_calculates_correctly(self, mock_guixy0manager):
        d = 1
        qr = 10
        offset = Offset.TOPRIGHT
        expect = Point(d/2 - qr, -d/2)
        config_xy0 = GuiConfigureXy0(None, mock_guixy0manager, {'padx': 5, 'pady': 5}, (qr, d))
        config_xy0._xy_option.set(offset)
        config_xy0._radiobutton_selection_changed()
        config_xy0._ok_button_clicked()

        mock_guixy0manager.set_xy0_parameters.assert_called_with(expect)

    @patch('src.gui.gui_xy0_manage.GuiXy0Manager')
    def test_setxy0_bottomleft_calculates_correctly(self, mock_guixy0manager):
        d = 1
        qr = 10
        offset = Offset.BOTTOMLEFT
        expect = Point(d/2, qr - d/2)
        config_xy0 = GuiConfigureXy0(None, mock_guixy0manager, {'padx': 5, 'pady': 5}, (qr, d))
        config_xy0._xy_option.set(offset)
        config_xy0._radiobutton_selection_changed()
        config_xy0._ok_button_clicked()

        mock_guixy0manager.set_xy0_parameters.assert_called_with(expect)

    @patch('src.gui.gui_xy0_manage.GuiXy0Manager')
    def test_setxy0_bottomright_calculates_correctly(self, mock_guixy0manager):
        d = 1
        qr = 10
        offset = Offset.BOTTOMRIGHT
        expect = Point(d/2 - qr, qr - d/2)
        config_xy0 = GuiConfigureXy0(None, mock_guixy0manager, {'padx': 5, 'pady': 5}, (qr, d))
        config_xy0._xy_option.set(offset)
        config_xy0._radiobutton_selection_changed()
        config_xy0._ok_button_clicked()

        mock_guixy0manager.set_xy0_parameters.assert_called_with(expect)

    @patch('src.gui.gui_xy0_manage.GuiXy0Manager')
    def test_setxy0_center_calculates_correctly(self, mock_guixy0manager):
        d = 1
        qr = 10
        offset = Offset.CENTER
        expect = Point(d/2 - qr/2, qr/2 - d/2)
        config_xy0 = GuiConfigureXy0(None, mock_guixy0manager, {'padx': 5, 'pady': 5}, (qr, d))
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
        config_xy0 = GuiConfigureXy0(None, mock_guixy0manager, {'padx': 5, 'pady': 5}, (qr, d))
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
        config_xy0 = GuiConfigureXy0(None, mock_guixy0manager, {'padx': 5, 'pady': 5}, (qr, d), expect)
        config_xy0._xy_option.set(offset)
        config_xy0._setx0.set(expect.x)
        config_xy0._sety0.set(expect.y)
        config_xy0._radiobutton_selection_changed()
        config_xy0._ok_button_clicked()

        mock_guixy0manager.set_xy0_parameters.assert_called_with(expect)


class TestIntegrationMain(unittest.TestCase):
    """The following test simulate a callback from the respective child windows of ToolManager, EngraveManager,
    XY0Manager and check whether the data is correctly stored and the main app updated so the changes are
    propagated."""
    @patch('src.gui.gui.App')
    def test_add_tool_updates_status(self, mock_main):
        tool = Tool(4, 'TestTool', 6, 3500, 1800, 24000)
        tool_manage = GuiToolManager(mock_main, {'padx': 5, 'pady': 5})
        tool_manage.add_or_edit_tool(tool)

        tool_manage._tool_list.select_tool(4)
        self.assertEqual(tool.diameter, tool_manage.get_selected_tool().diameter)

        mock_main.update_status.assert_called()

    @patch('src.gui.gui.App')
    def test_update_tool_updates_status(self, mock_main):
        tool_manage = GuiToolManager(mock_main, {'padx': 5, 'pady': 5})

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
        tool_manage = GuiToolManager(mock_main, {'padx': 5, 'pady': 5})
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
        engrave_manage = GuiEngraveManager(mock_main, {'padx': 5, 'pady': 5})
        engrave_manage.set_engrave_parameters(params)

        self.assertEqual(params.z_engrave, engrave_manage.get_engrave_parameters().z_engrave)
        self.assertEqual(params.z_hover, engrave_manage.get_engrave_parameters().z_hover)
        self.assertEqual(params.z_flyover, engrave_manage.get_engrave_parameters().z_flyover)

        mock_main.update_status.assert_called()

    @patch('src.gui.gui.App')
    def test_set_custom_engrave_params_updates_status(self, mock_main):
        params = EngraveParams(2, 2, 20)
        engrave_manage = GuiEngraveManager(mock_main, {'padx': 5, 'pady': 5})
        engrave_manage.set_engrave_parameters(params)

        self.assertEqual(params.z_engrave, engrave_manage.get_engrave_parameters().z_engrave)
        self.assertEqual(params.z_hover, engrave_manage.get_engrave_parameters().z_hover)
        self.assertEqual(params.z_flyover, engrave_manage.get_engrave_parameters().z_flyover)

        mock_main.update_status.assert_called()

    @patch('src.gui.gui.App')
    def test_update_xy0_updates_status(self, mock_main):
        params = Point(2, 4)
        engrave_manage = GuiXy0Manager(mock_main, {'padx': 5, 'pady': 5})
        engrave_manage.set_xy0_parameters(params)

        self.assertEqual(params.x, engrave_manage.get_xy0_parameters().x)
        self.assertEqual(params.y, engrave_manage.get_xy0_parameters().y)

        mock_main.update_status.assert_called()

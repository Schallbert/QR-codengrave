from tkinter.filedialog import asksaveasfile
from shutil import copyfileobj

from bin.gui_generate_qr import *
from bin.gui_tool_manage import *
from bin.gui_generate_gcode import *
from bin.gui_status_bar import *
from bin.gui_engrave_manage import *
from bin.gui_xy0_manage import *

from bin.machinify_vector import MachinifyVector


class App:
    """Main application and entry point for QR-codengrave. Creates a main window that is able to spawn child
    windows on demand for parameter input. Provides the user interface to creating G-code CNC machine instructions
    from Text that is converted into a QR-code."""
    def __init__(self, root):
        self.root = root

        self.version = 1.0

        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('teal.Horizontal.TProgressbar', foreground='black', background='#00A877')
        self.root.iconbitmap('../assets/qruwu.ico')
        self.root.title("EngraveQr")
        self.canvas = tk.Canvas(root)
        self.canvas.config(width=600, height=600)

        self.frame = ttk.Frame(self.root)
        self._options = {'padx': 5, 'pady': 5}

        self._machinify = MachinifyVector(self.version)

        self.gui_qr_generator = GuiGenerateQr(self, self._options)
        self.gui_tool_manager = GuiToolManager(self, self._options)
        self.gui_engrave_params = GuiEngraveManager(self, self._options)
        self.gui_xy0_manager = GuiXy0Manager(self, self._options)
        self.gui_gcode_generator = GuiGenerateGcode(self, self._options)
        self.gui_status_bar = GuiStatusBar(self, self._options)

    def update_status(self, text=''):
        """Called from other parts of the GUI, this method updates the status bar and synchronizes object state
        down to the main application's classes.
        :param text: an optional parameter to display a custom message on the status bar"""
        if text != '':
            self.gui_status_bar.set_status_text(text)
        elif self._collect_necessary_data():
            size = self._machinify.get_dimension_info()
            self.gui_status_bar.set_qr_size(size[0])
            self.gui_xy0_manager.set_dimension_info(size)
            if self._collect_optional_data():
                self.gui_status_bar.set_job_duration(self._machinify.get_job_duration_sec())
                self.gui_status_bar.set_status_ready()
        else:
            self.gui_status_bar.set_status_not_ready()

    def set_project_name(self, text):
        """Setter method.
        :param text: forwards the project's name as a String object to the G-code generating class."""
        self._machinify.set_project_name(text)

    def run_gcode_generator(self):
        """Command to run the G-code generator. To be called by a button within the GUI. In case all relevant data is
        available, has G-code generated and saved to a file."""
        if not self._validate_data():
            return
        self._save_file(self._machinify.generate_gcode())

    def _collect_necessary_data(self):
        """Tries to obtain QR-code paths and tool information from other parts of the GUI.
        Forwards the data to the Machinify module.
        :returns False: if data is not available, else returns True."""
        paths = self.gui_qr_generator.get_qr_spiral_paths()
        tool = self.gui_tool_manager.get_selected_tool()

        if paths is None:
            return False
        self._machinify.set_qr_path(paths)
        if tool is None:
            return False
        self._machinify.set_tool(tool)
        return True

    def _collect_optional_data(self):
        """Tries to obtain Engrave parameters and Workpiece Zero offsets from other parts of the GUI.
        FOrwards the data to the Machinify module.
        :returns False: if the data is not available, else returns True."""
        engrave = self.gui_engrave_params.get_engrave_parameters()
        xy0 = self.gui_xy0_manager.get_xy0_parameters()

        if engrave is None:
            return False
        self._machinify.set_engrave_params(engrave)
        if xy0 is None:
            return False
        self._machinify.set_xy_zero(xy0)
        return True

    def _validate_data(self):
        """Calls Machinify's data check method and raises an error message if not all data is available to generate
        G-code.
        :returns True if all necessary data is available, else returns False."""
        error = self._machinify.report_data_missing()
        if error != '':
            showerror(title='Error: ' + error + ' missing',
                      message='Error: could not locate ' + error + '. \nDid you set the according entries?')
            return False
        return True

    def _save_file(self, gcode):
        """Calls a file save dialog and copies the already generated G-code into that file.
        :param gcode: A StringIO object representing the machine instructions.
        :returns early in case the dialog is cancelled by the user."""
        file = asksaveasfile(mode='w', initialfile=self._machinify.get_project_name() + '.tap',
                             defaultextension='.tap', filetypes=[('CNC gcode', '*.tap'), ('Text Document', '*.txt')])
        if file is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        gcode.seek(0)
        copyfileobj(gcode, file)
        file.close()


if __name__ == '__main__':
    main = tk.Tk()
    app = App(main)
    main.mainloop()

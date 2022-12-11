from bin.gui_generate_qr import *
from bin.gui_tool_manage import *
from bin.gui_generate_gcode import *
from bin.gui_status_bar import *
from bin.gui_engrave_manage import *
from bin.gui_xy0_manage import *

from bin.machinify_vector import MachinifyVector


class App:
    def __init__(self, root):
        self.root = root
        self.style = ttk.Style()
        self.style.theme_use('classic')
        self.style.configure('teal.Horizontal.TProgressbar', foreground='black', background='#00A877')
        self.root.iconbitmap('../assets/qruwu.ico')
        self.root.title("EngraveQr")
        self.canvas = tk.Canvas(root)
        self.canvas.config(width=600, height=600)

        self.frame = ttk.Frame(self.root)
        self._options = {'padx': 5, 'pady': 5}

        self._machinify = MachinifyVector()

        self.gui_qr_generator = GuiGenerateQr(self, self._options)
        self.gui_tool_manager = GuiToolManager(self, self._options)
        self.gui_engrave_params = GuiEngraveManager(self, self._options)
        self.gui_xy0_manager = GuiXy0Manager(self, self._options)
        self.gui_gcode_generator = GuiGenerateGcode(self, self._options)
        self.gui_status_bar = GuiStatusBar(self, self._options)

    def update_status(self, text=''):
        if text != '':
            self.gui_status_bar.set_status_text(text)
        if self._collect_necessary_data():
            self.gui_status_bar.set_qr_size(self._machinify.get_qr_size_mm())
            if self._collect_optional_data():
                self.gui_status_bar.set_job_duration(self._machinify.get_job_duration_sec())
                self.gui_status_bar.set_status_ready()
        else:
            self.gui_status_bar.set_status_not_ready()

    def run_gcode_generator(self):
        if self._validate_data():
            self._machinify.generate_gcode()

    def _collect_necessary_data(self):
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
        error = self._machinify.report_data_missing()
        if error != '':
            showerror(title='Error: ' + error + ' missing', message='Error: could not locate ' + error + '. \n '
                                                                    'Did you set the according entries?')
            return False
        return True


if __name__ == '__main__':
    main = tk.Tk()
    app = App(main)
    main.mainloop()

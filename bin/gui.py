from bin.gui_generate_qr import *
from bin.gui_tool_manage import *
from bin.gui_generate_gcode import *
from bin.gui_status_bar import *
from bin.gui_engrave_params import *

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
        self.options = {'padx': 5, 'pady': 5}

        self._machinify = None

        self.gui_qr_generator = GuiGenerateQr(self, self.options)
        self.gui_tool_manager = GuiToolManager(self, self.options)
        self.gui_status_bar = GuiStatusBar(self, self.options)
        self.gui_engrave_params = GuiEngraveParams(self, self.options)
        self.gui_gcode_generator = GuiGenerateGcode(self, self.gui_qr_generator,
                                                    self.gui_tool_manager, self.options)

    def update_status(self, text=''):
        if text != '':
            self.gui_status_bar.set_status_text(text)
        elif self.gui_qr_generator.is_qr_defined() and self.gui_tool_manager.get_selected_tool() is not None:
            self._collect_data()
            self.gui_status_bar.set_job_duration(self._machinify.get_job_duration_sec())
            self.gui_status_bar.set_qr_size(self._machinify.get_qr_size_mm())
            self.gui_status_bar.set_status_ready()
        else:
            self.gui_status_bar.set_status_not_ready()

    def run_gcode_generator(self):
        if self._machinify is not None:
            self._machinify.generate_gcode()

    def _collect_data(self):
        self._machinify = MachinifyVector(self.gui_qr_generator.get_qr_spiral_paths(),
                                          self.gui_tool_manager.get_selected_tool())
        self._machinify.set_engrave_params(self.gui_tool_manager.get_engrave_params())
        self._machinify.set_xy_zero(self.gui_gcode_generator.get_xy0())


if __name__ == '__main__':
    main = tk.Tk()
    app = App(main)
    main.mainloop()

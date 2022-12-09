from bin.gui_generate_qr import *
from bin.gui_tool_manage import *
from bin.gui_generate_gcode import *


class App:
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap('../assets/qruwu.ico')
        self.root.title("EngraveQr")
        self.canvas = tk.Canvas(root)
        self.canvas.config(width=600, height=600)

        self.frame = ttk.Frame(self.root)
        self.options = {'padx': 5, 'pady': 5}

        self.gui_qr_generator = GuiGenerateQr(self.frame, self.options)
        self.gui_tool_manager = GuiToolManager(self.frame, self.options)
        self.gui_gcode_generator = GuiGenerateGcode(self.frame, self.gui_qr_generator,
                                                    self.gui_tool_manager, self.options)


if __name__ == '__main__':
    main = tk.Tk()
    app = App(main)
    main.mainloop()

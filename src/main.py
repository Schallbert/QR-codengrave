import tkinter as tk

from src.gui.gui import App
from src.resources import app_icon_path

if __name__ == '__main__':
    main = tk.Tk()
    app = App(main)
    main.iconbitmap(bitmap=app_icon_path)
    main.mainloop()

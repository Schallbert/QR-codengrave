from src import assets
import importlib.resources as pkg_resources
from tkinter.messagebox import showerror

try:
    with pkg_resources.path(assets, 'qruwu.ico') as p_icon:
        app_icon_path = p_icon
    with pkg_resources.path(assets, 'qruwu.png') as p_image:
        app_image_path = p_image
    with pkg_resources.path(assets, 'persistence.dat') as p_persistence:
        app_persistence_path = p_persistence
except FileNotFoundError:
    showerror(title='Asset file not found', message='Could not locate file(s) under "src/assets"')
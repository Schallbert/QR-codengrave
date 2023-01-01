from src import assets
import importlib.resources as pkg_resources

with pkg_resources.path(assets, 'qruwu.ico') as p_icon:
    app_icon_path = p_icon
with pkg_resources.path(assets, 'qruwu.png') as p_image:
    app_image_path = p_image
with pkg_resources.path(assets, 'persistence.dat') as p_persistence:
    app_persistence_path = p_persistence


def validate_number(entry):
    """Helper function that is used in validators to check
    that the entered keystroke is a number"""
    if entry == '':
        return True
    try:
        float(entry)
        return True
    except ValueError:
        return False

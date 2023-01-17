app_icon_path = 'src/assets/qruwu.ico'
app_image_path = 'src/assets/qruwu.png'
app_persistence_path = 'src/assets/persistence.dat'


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

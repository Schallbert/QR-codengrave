app_icon_path = '../assets/qruwu.ico'
app_image_path = '../assets/qruwu.png'


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

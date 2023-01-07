from tkinter.messagebox import showinfo, showerror


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


class MsgBox:
    def warning(self, title, message):
        showinfo(title=title, message=message)

    def error(self, title, message):
        showerror(self, title=title, message=message)

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
    """Re-implementation due to testing purposes: With this trick, we are able to mock these windows
    so we do not have to wait for users to manually close the dialog, unblocking the application again."""
    def warning(self, title, message):
        showinfo(title=title, message=message)

    def error(self, title, message):
        showerror(title=title, message=message)

from loguru import logger
from PyQt6.QtWidgets import QMessageBox

def show_error(parent, message: str, title: str = "Error"):
    """Display an error popup in the GUI."""

    logger.error(message)  # log the error
    
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    
    msg_box.exec()

def handle_exceptions(func):
    """Decorator to wrap functions and automatically show GUI error popups."""
    
    def wrapper(*args, **kwargs):
        self = args[0]  # assuming the first arg is a controller with a 'view' attribute
        try:
            return func(*args, **kwargs)
        except Exception as e:
            show_error(getattr(self, 'view', None), str(e))
    return wrapper

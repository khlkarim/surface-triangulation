from functools import wraps
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

def handle_exceptions(custom_message: str | None = None):
    """Decorator to wrap functions and show GUI error popups, with optional custom message."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]  # assuming first arg is a controller with 'view'
            try:
                return func(*args, **kwargs)
            except Exception as e:
                message = custom_message or str(e)
                show_error(getattr(self, 'view', None), message)
        return wrapper
    return decorator

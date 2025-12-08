import sys
from .main_window import MainWindow
from PyQt6.QtWidgets import QApplication

def launch_gui():
    app = QApplication.instance()
    should_exec = False

    if app is None:
        app = QApplication(sys.argv)
        should_exec = True

    window = MainWindow(
        "Surface Triangulation",
        1200,
        700
    )
    window.show()

    if should_exec:
        app.exec()

    return window

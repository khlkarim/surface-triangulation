import sys
from PyQt6.QtWidgets import QApplication
from surface_triangulation.config.app_config import Config
from surface_triangulation.ui.main_window import MainWindow

def create_app() -> QApplication:
    config = Config.get_instance()

    app = QApplication(sys.argv)

    window = MainWindow(
        config.app_name, 
        config.window_width, 
        config.window_height
    )
    window.show()
    
    app.exec()
    return app

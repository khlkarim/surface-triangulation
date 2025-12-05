from vispy.scene import SceneCanvas, TurntableCamera
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox
from surface_triangulation.ui.renderers.vispy.mesh_renderer import MeshRenderer
from surface_triangulation.ui.renderers.vispy.mesh_renderer import RenderMode

class Canvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.canvas = SceneCanvas(keys='interactive', show=True)
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = TurntableCamera(fov=60)

        self.mesh_renderer = MeshRenderer(self.view)

        self.render_mode_dropdown = QComboBox()

        for mode in RenderMode:
            self.render_mode_dropdown.addItem(mode.label, mode)

        self.render_mode_dropdown.setCurrentIndex(0)
        self.mesh_renderer.update_render_mode(RenderMode.POINTS)

        self.render_mode_dropdown.currentIndexChanged.connect(self.on_render_mode_changed)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas.native)
        layout.addWidget(self.render_mode_dropdown)
        self.setLayout(layout)

    def on_render_mode_changed(self, index: int):
        mode = self.render_mode_dropdown.itemData(index)
        if self.mesh_renderer:
            self.mesh_renderer.update_render_mode(mode)

    def set_render_mode(self, mode):
        self.render_mode_dropdown.setCurrentIndex(mode)

    def set_available_render_modes(self):
        pass
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QPushButton, QFormLayout, QVBoxLayout)

from surface_triangulation.config.app_config import Config
from surface_triangulation.ui.views.widgets.input.input_tab import InputTab
from surface_triangulation.ui.views.widgets.input.objective_selector import ObjectiveSelector
from surface_triangulation.ui.views.widgets.input.constraints_selector import ConstraintsSelector

class TriangulationConfig(QDialog):
    def __init__(self):
        super().__init__()
        config = Config.get_instance()

        self.setWindowTitle(config.config_dialog_name)
        self.setMinimumWidth(config.config_dialog_width)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.objective_selector = ObjectiveSelector()
        form_layout.addRow("Objective function:", self.objective_selector)

        self.constraints_selector = ConstraintsSelector()
        form_layout.addRow("Constraints:", self.constraints_selector)

        self.candidate_edges_input = InputTab("Candidate Edges")
        self.candidate_faces_input = InputTab("Candidate Faces")
        self.boundary_edges_input = InputTab("Boundary Edges")

        form_layout.addRow(self.candidate_edges_input)
        form_layout.addRow(self.candidate_faces_input)
        form_layout.addRow(self.boundary_edges_input)

        layout.addLayout(form_layout)

        self.apply_btn = QPushButton("Apply triangulation parameters")
        self.apply_btn.clicked.connect(self.hide_config_popup)

        layout.addWidget(self.apply_btn)

        self.setLayout(layout)

    def get_selected_objective(self):
        return self.objective_selector.get_selected()
    def set_selected_objective(self, objective):
        self.objective_selector.set_selected(objective)

    def set_selected_constraints(self, constraints):
        self.constraints_selector.set_selected(constraints)
    def get_selected_constraints(self):
        return self.constraints_selector.get_selected()

    def hide_config_popup(self):
        if self.isVisible():
            self.hide()

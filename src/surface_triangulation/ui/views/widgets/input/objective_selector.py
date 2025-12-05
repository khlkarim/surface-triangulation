from PyQt6.QtWidgets import (QVBoxLayout, QComboBox, QWidget, QVBoxLayout)
from surface_triangulation.core.models.triangulation_objectives import TriangulationObjective

class ObjectiveSelector(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.combo = QComboBox()
        
        for obj in TriangulationObjective:
            self.combo.addItem(obj.label, obj)
        
        layout.addWidget(self.combo)
        self.setLayout(layout)

    def get_selected(self):
        return self.combo.currentData()
    
    def set_selected(self, objective: TriangulationObjective):
        return self.combo.setCurrentText(objective.label)
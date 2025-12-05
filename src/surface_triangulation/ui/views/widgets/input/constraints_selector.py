from surface_triangulation.core.models.triangulation_contraints import TriangulationConstraint
from PyQt6.QtWidgets import (QVBoxLayout, QListWidget, QListWidgetItem, QAbstractItemView, QWidget, QVBoxLayout)

class ConstraintsSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(125)

        layout = QVBoxLayout()
        
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        for c in TriangulationConstraint:
            item = QListWidgetItem(c.label)
            item.setData(1000, c)
            self.list_widget.addItem(item)
        
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def get_selected(self):
        return [item.data(1000) for item in self.list_widget.selectedItems()]
    
    def set_selected(self, constraints: list[TriangulationConstraint]):
        """Select items in the list widget based on a list of constraints."""
        self.list_widget.clearSelection()  # Clear previous selection

        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item and item.data(1000) in constraints:
                item.setSelected(True)

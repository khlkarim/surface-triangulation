import numpy as np
from loguru import logger
from vispy.scene import Markers, Text, Node

class LabeledPoints(Node):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        logger.debug("Initializing LabeledPoints visual")

        self.points = Markers(parent=self)
        self.label_nodes = []  # store Text visuals

    def update_data(self, verts: np.ndarray):
        logger.debug(f"Updating LabeledPoints with {len(verts)} vertices")

        # Update markers
        if verts.size:
            self.points.set_data(verts)
            logger.debug("Markers updated with vertex positions")
        else:
            self.points.set_data()
            logger.debug("Markers cleared (no vertices)")
            self._clear_labels()
            return

        # Update labels
        self._update_labels(verts)

    def _clear_labels(self):
        logger.debug(f"Clearing {len(self.label_nodes)} existing labels")

        for lbl in self.label_nodes:
            lbl.parent = None
        self.label_nodes = []

    def _update_labels(self, verts):
        logger.debug(f"Updating labels for {len(verts)} vertices")

        # Remove old labels
        self._clear_labels()

        offset = np.array([0, 0.2, 0])  # small vertical offset

        for i, p in enumerate(verts):
            lbl = Text(
                text="v" + str(i),
                pos=p + offset,
                color='white',
                font_size=8
            )
            lbl.parent = self
            self.label_nodes.append(lbl)

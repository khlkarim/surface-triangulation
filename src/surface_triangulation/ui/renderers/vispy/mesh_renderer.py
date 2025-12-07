import numpy as np
from loguru import logger

from vispy.scene import Mesh, Line, XYZAxis
from vispy.visuals.filters.mesh import WireframeFilter
from surface_triangulation.ui.renderers.render_mode import RenderMode
from surface_triangulation.ui.renderers.vispy.labeled.labeled_points import LabeledPoints

class MeshRenderer:
    def __init__(self, parent_viewbox):
        logger.debug("Initializing MeshRenderer and adding visuals to parent viewbox")
        
        # Visuals
        self.axis = XYZAxis()
        
        self.mesh = Mesh()
        wireframe = WireframeFilter()
        self.mesh.attach(wireframe)

        self.points = LabeledPoints()
        self.lines = Line(connect='segments')

        # Add to the parent viewbox
        parent_viewbox.add(self.axis)
        parent_viewbox.add(self.mesh)
        parent_viewbox.add(self.points)
        parent_viewbox.add(self.lines)
        logger.debug("Visuals added: axis, mesh, points, lines")

    def update_data(self, model):
        verts = np.asarray(model.vertices or [], dtype=float)
        edges = np.asarray(model.edges or [], dtype=int)
        faces = np.asarray(model.faces or [], dtype=int)

        logger.debug(f"Updating data: {len(verts)} vertices, {len(edges)} edges, {len(faces)} faces")

        # Update vertices (points)
        if verts.size:
            self.points.update_data(verts)
            logger.debug(f"Points updated with {len(verts)} vertices")
        else:
            self.points.update_data(np.empty((0, 2)))
            logger.debug("Points cleared (no vertices)")

        # Update edges (lines)
        if edges.size:
            line_vertices = verts[edges]
            self.lines.set_data(pos=line_vertices, connect='segments')
            logger.debug(f"Lines updated with {len(edges)} edges")
        else:
            self.lines.set_data(np.empty((0, 2)))
            logger.debug("Lines cleared (no edges)")

        # Update faces (mesh)
        if faces.size:
            self.mesh.set_data(vertices=verts, faces=faces)
            logger.debug(f"Mesh updated with {len(faces)} faces")
        else:
            self.mesh.set_data()
            logger.debug("Mesh cleared (no faces)")

    def update_render_mode(self, mode: RenderMode):
        logger.debug(f"Updating render mode to {mode}")

        self.points.visible = True
        self.lines.visible = mode == RenderMode.LINES
        self.mesh.visible = mode == RenderMode.TRIANGLES
        
        logger.debug(f"Render visibility - points: {self.points.visible}, "
                     f"lines: {self.lines.visible}, mesh: {self.mesh.visible}")

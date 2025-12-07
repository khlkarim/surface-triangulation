import numpy as np
from vispy.scene import Mesh, Line, XYZAxis
from surface_triangulation.ui.renderers.render_mode import RenderMode
from surface_triangulation.ui.renderers.vispy.labeled.labeled_points import LabeledPoints

class MeshRenderer:
    def __init__(self, parent_viewbox):
        # Visuals
        self.axis = XYZAxis()
        self.mesh = Mesh()
        self.points = LabeledPoints()
        self.lines = Line(connect='segments')

        # Add to the parent viewbox
        parent_viewbox.add(self.axis)
        parent_viewbox.add(self.mesh)
        parent_viewbox.add(self.points)
        parent_viewbox.add(self.lines)

    def update_data(self, model):
        verts = np.asarray(model.vertices or [], dtype=float)
        edges = np.asarray(model.edges or [], dtype=int)
        faces = np.asarray(model.faces or [], dtype=int)

        # Update vertices (points)
        self.points.update_data(verts) if verts.size else self.points.update_data(np.empty((0, 2)))

        # Update edges (lines)
        if edges.size:
            line_vertices = verts[edges]
            self.lines.set_data(pos=line_vertices, connect='segments')
        else:
            self.lines.set_data(np.empty((0, 2)))

        # Update faces (mesh)
        if faces.size:
            self.mesh.set_data(vertices=verts, faces=faces)
        else:
            self.mesh.set_data()

    def update_render_mode(self, mode: RenderMode):
        self.points.visible = True
        self.lines.visible = mode == RenderMode.LINES
        self.mesh.visible = mode == RenderMode.TRIANGLES

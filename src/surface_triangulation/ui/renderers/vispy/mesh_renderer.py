import numpy as np
from vispy.scene import Mesh, Markers, Line
from surface_triangulation.ui.renderers.render_mode import RenderMode

class MeshRenderer:
    def __init__(self, parent_viewbox):
        # Visuals
        self.mesh = Mesh()
        self.points = Markers()
        self.lines = Line(connect='segments')

        # Add to the parent viewbox
        parent_viewbox.add(self.mesh)
        parent_viewbox.add(self.points)
        parent_viewbox.add(self.lines)

    def update_data(self, model):
        if not model.hydrated:
            # Hide visuals if model is not ready
            self.mesh.visible = False
            self.points.visible = False
            self.lines.visible = False
            return

        verts = np.asarray(model.vertices or [], dtype=float)
        edges = np.asarray(model.edges or [], dtype=int)
        faces = np.asarray(model.faces or [], dtype=int)

        # Update vertices (points)
        self.points.set_data(verts) if verts.size else self.points.set_data()

        # Update edges (lines)
        if edges.size:
            line_vertices = verts[edges]
            self.lines.set_data(pos=line_vertices, connect='segments')
        else:
            self.lines.set_data()

        # Update faces (mesh)
        if faces.size:
            self.mesh.set_data(vertices=verts, faces=faces)
        else:
            self.mesh.set_data()

    def update_render_mode(self, mode: RenderMode):
        self.points.visible = mode == RenderMode.POINTS
        self.lines.visible = mode == RenderMode.LINES
        self.mesh.visible = mode == RenderMode.TRIANGLES

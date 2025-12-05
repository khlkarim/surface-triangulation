import csv
from io import StringIO
from pathlib import Path
from surface_triangulation.mesh_io.mesh_data import MeshData
from surface_triangulation.ui.models.mesh_model import MeshModel
from surface_triangulation.mesh_io.mesh_loader_registry import MeshLoaderRegistry

class IOService:
    """
    Provides high-level loading/exporting functionality over the MeshModel.
    Uses MeshLoaderRegistry for full mesh operations.
    
    For vertices/faces/edges-only operations, uses a simple TXT/CSV format.
    """

    def __init__(self, loader_registry: MeshLoaderRegistry | None = None):
        self.registry = loader_registry or MeshLoaderRegistry()

    # ---------------------------------------------------------
    # Internal helper
    # ---------------------------------------------------------
    def _ensure_txt_or_csv(self, path: str | Path) -> None:
        ext = Path(path).suffix.lower()
        if ext not in {".txt", ".csv"}:
            raise ValueError(
                f"Invalid file extension '{ext}'. Expected '.txt' or '.csv'."
            )

    # ---------------------------------------------------------
    # Full mesh load/export (delegated to registry)
    # ---------------------------------------------------------
    def load(self, path: str | Path, mesh_model: MeshModel) -> None:
        mesh_data = self.registry.load(path)
        mesh_model.reset(mesh_data.vertices, mesh_data.edges, mesh_data.faces)

    def export(self, path: str | Path, mesh_model: MeshModel) -> None:
        if mesh_model.vertices is None:
            raise ValueError("Can't export mesh containing no vertices.")

        mesh_data = MeshData(
            vertices=mesh_model.vertices,
            faces=mesh_model.faces,
            edges=mesh_model.edges
        )
        self.registry.export(path, mesh_data)

    # ---------------------------------------------------------
    # Vertices-only loading/exporting from TXT
    # ---------------------------------------------------------
    def load_vertices(self, path: str | Path):
        return self.registry.load_vertices(path)

    def export_vertices(self, path: str | Path, mesh_model) -> None:
        self._ensure_txt_or_csv(path)
            
        if mesh_model.vertices is None:
            raise ValueError("Can't export mesh containing no vertices.")

        mesh_data = MeshData(vertices=mesh_model.vertices)
        self.registry.export(path, mesh_data)

    # ---------------------------------------------------------
    # Faces-only loading/exporting from TXT
    # ---------------------------------------------------------
    def load_faces(self, path: str | Path):
        return self.registry.load_faces(path)

    def export_faces(self, path: str | Path, mesh_model) -> None:
        self._ensure_txt_or_csv(path)

        if mesh_model.faces is None:
            raise ValueError("Can't export mesh containing no faces.")

        mesh_data = MeshData(vertices=mesh_model.faces)
        self.registry.export(path, mesh_data)

    # ---------------------------------------------------------
    # Edges-only loading/exporting from TXT
    # ---------------------------------------------------------
    def load_edges(self, path: str | Path):
        return self.registry.load_edges(path)

    def export_edges(self, path: str | Path, mesh_model) -> None:
        self._ensure_txt_or_csv(path)

        if mesh_model.edges is None:
            raise ValueError("Can't export mesh containing no faces.")

        mesh_data = MeshData(vertices=mesh_model.edges)
        self.registry.export(path, mesh_data)

    def parse_csv_to_list(self, csv_string: str):
        csv_file = StringIO(csv_string)
        reader = csv.reader(csv_file)
        result = []
        for row in reader:
            float_row = []
            for value in row:
                float_row.append(float(value))
            result.append(float_row)
        return result

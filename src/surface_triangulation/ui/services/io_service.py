from pathlib import Path
from surface_triangulation.mesh_io.mesh_data import MeshData
from surface_triangulation.ui.models.mesh_model import MeshModel
from surface_triangulation.mesh_io.mesh_loader_registry import MeshLoaderRegistry
from surface_triangulation.utils.csv_parsing import csv_to_list, list_to_csv

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

    def _load_2d_list_from_file(self, path: str | Path) -> list[list]:
        with open(path, "r", newline="") as f:
            csv_string = f.read()
        return csv_to_list(csv_string)

    def _export_2d_list_to_file(self, path: str | Path, data: list[list]) -> None:
        csv_string = list_to_csv(data)
        with open(path, "w", newline="") as f:
            f.write(csv_string)

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
    # Vertices-only loading/exporting from TXT/CSV
    # ---------------------------------------------------------
    def load_vertices(self, path: str | Path):
        rows = self._load_2d_list_from_file(path)
        return [(float(r[0]), float(r[1]), float(r[2])) for r in rows]

    def export_vertices(self, path: str | Path, mesh_model) -> None:
        self._ensure_txt_or_csv(path)
        if mesh_model.vertices is None:
            raise ValueError("Can't export mesh containing no vertices.")
        rows = [list(v) for v in mesh_model.vertices]
        self._export_2d_list_to_file(path, rows)

    # ---------------------------------------------------------
    # Faces-only loading/exporting from TXT/CSV
    # ---------------------------------------------------------
    def load_faces(self, path: str | Path):
        rows = self._load_2d_list_from_file(path)
        return [(int(r[0]), int(r[1]), int(r[2])) for r in rows]

    def export_faces(self, path: str | Path, mesh_model) -> None:
        self._ensure_txt_or_csv(path)
        if mesh_model.faces is None:
            raise ValueError("Can't export mesh containing no faces.")
        rows = [list(f) for f in mesh_model.faces]
        self._export_2d_list_to_file(path, rows)

    # ---------------------------------------------------------
    # Edges-only loading/exporting from TXT/CSV
    # ---------------------------------------------------------
    def load_edges(self, path: str | Path):
        rows = self._load_2d_list_from_file(path)
        return [(int(r[0]), int(r[1])) for r in rows]

    def export_edges(self, path: str | Path, mesh_model) -> None:
        self._ensure_txt_or_csv(path)
        if mesh_model.edges is None:
            raise ValueError("Can't export mesh containing no edges.")
        rows = [list(e) for e in mesh_model.edges]
        self._export_2d_list_to_file(path, rows)

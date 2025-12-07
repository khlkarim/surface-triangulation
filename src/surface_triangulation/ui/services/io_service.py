from pathlib import Path
from loguru import logger
from surface_triangulation.mesh_io.mesh_data import MeshData
from surface_triangulation.ui.models.mesh_model import MeshModel
from surface_triangulation.mesh_io.mesh_loader_registry import MeshLoaderRegistry
from surface_triangulation.utils.csv_parsing import csv_to_list, list_to_csv

class IOService:
    def __init__(self, loader_registry: MeshLoaderRegistry | None = None):
        self.registry = loader_registry or MeshLoaderRegistry()

    # Internal helper
    def _ensure_txt_or_csv(self, path: str | Path) -> None:
        ext = Path(path).suffix.lower()
        if ext not in {".txt", ".csv"}:
            logger.error(f"Invalid file extension '{ext}' for path '{path}'")
            raise ValueError(
                f"Invalid file extension '{ext}'. Expected '.txt' or '.csv'."
            )
        logger.debug(f"File extension '{ext}' is valid for '{path}'")

    def _load_2d_list_from_file(self, path: str | Path) -> list[list]:
        logger.debug(f"Loading 2D list from file '{path}'")
        with open(path, "r", newline="") as f:
            csv_string = f.read()
        rows = csv_to_list(csv_string)
        logger.debug(f"Loaded {len(rows)} rows from file '{path}'")
        return rows

    def _export_2d_list_to_file(self, path: str | Path, data: list[list]) -> None:
        logger.debug(f"Exporting {len(data)} rows to file '{path}'")
        csv_string = list_to_csv(data)
        with open(path, "w", newline="") as f:
            f.write(csv_string)
        logger.debug(f"Exported 2D list to file '{path}'")

    # Full mesh load/export (delegated to registry)
    def load(self, path: str | Path, mesh_model: MeshModel) -> None:
        logger.debug(f"Loading full mesh from '{path}'")
        mesh_data = self.registry.load(path)
        mesh_model.reset(mesh_data.vertices, mesh_data.edges, mesh_data.faces)
        logger.debug(
            f"Mesh loaded: "
            f"{len(mesh_data.vertices or [])} vertices, "
            f"{len(mesh_data.edges or [])} edges, "
            f"{len(mesh_data.faces or [])} faces"
        )

    def export(self, path: str | Path, mesh_model: MeshModel) -> None:
        logger.debug(f"Exporting full mesh to '{path}'")
        if mesh_model.vertices is None:
            logger.error("Cannot export mesh: no vertices present")
            raise ValueError("Can't export mesh containing no vertices.")

        mesh_data = MeshData(
            vertices=mesh_model.vertices,
            faces=mesh_model.faces,
            edges=mesh_model.edges
        )
        self.registry.export(path, mesh_data)
        logger.debug(
            f"Mesh exported successfully: "
            f"{len(mesh_data.vertices or [])} vertices, "
            f"{len(mesh_data.edges or [])} edges, "
            f"{len(mesh_data.faces or [])} faces"
        )

    # Vertices-only loading/exporting from TXT/CSV
    def load_vertices(self, path: str | Path):
        logger.debug(f"Loading vertices from '{path}'")
        rows = self._load_2d_list_from_file(path)
        vertices = [(float(r[0]), float(r[1]), float(r[2])) for r in rows]
        logger.debug(f"Loaded {len(vertices)} vertices")
        return vertices

    def export_vertices(self, path: str | Path, mesh_model) -> None:
        self._ensure_txt_or_csv(path)
        if mesh_model.vertices is None:
            logger.error("Cannot export vertices: no vertices present")
            raise ValueError("Can't export mesh containing no vertices.")
        rows = [list(v) for v in mesh_model.vertices]
        logger.debug(f"Exporting {len(rows)} vertices to '{path}'")
        self._export_2d_list_to_file(path, rows)

    # Faces-only loading/exporting from TXT/CSV
    def load_faces(self, path: str | Path):
        logger.debug(f"Loading faces from '{path}'")
        rows = self._load_2d_list_from_file(path)
        faces = [(int(r[0]), int(r[1]), int(r[2])) for r in rows]
        logger.debug(f"Loaded {len(faces)} faces")
        return faces

    def export_faces(self, path: str | Path, mesh_model) -> None:
        self._ensure_txt_or_csv(path)
        if mesh_model.faces is None:
            logger.error("Cannot export faces: no faces present")
            raise ValueError("Can't export mesh containing no faces.")
        rows = [list(f) for f in mesh_model.faces]
        logger.debug(f"Exporting {len(rows)} faces to '{path}'")
        self._export_2d_list_to_file(path, rows)

    # Edges-only loading/exporting from TXT/CSV
    def load_edges(self, path: str | Path):
        logger.debug(f"Loading edges from '{path}'")
        rows = self._load_2d_list_from_file(path)
        edges = [(int(r[0]), int(r[1])) for r in rows]
        logger.debug(f"Loaded {len(edges)} edges")
        return edges

    def export_edges(self, path: str | Path, mesh_model) -> None:
        self._ensure_txt_or_csv(path)
        if mesh_model.edges is None:
            logger.error("Cannot export edges: no edges present")
            raise ValueError("Can't export mesh containing no edges.")
        rows = [list(e) for e in mesh_model.edges]
        logger.debug(f"Exporting {len(rows)} edges to '{path}'")
        self._export_2d_list_to_file(path, rows)

import csv
import random
import itertools
from pathlib import Path
from typing import List, Tuple


def generate_points(n: int) -> List[Tuple[float, float, float]]:
    """Generate n random points on the XY plane (z=0)."""
    return [(5*random.random()-5/2, 5*random.random()-5/2, 0.0) for _ in range(n)]


def generate_all_edges(n: int) -> List[Tuple[int, int]]:
    """Return all unordered pairs of vertices."""
    return [(i, j) for i, j in itertools.combinations(range(n), 2)]


def generate_all_faces(n: int) -> List[Tuple[int, int, int]]:
    """Return all possible faces (triangles)."""
    return [(min(t), sorted(t)[1], max(t)) for t in itertools.combinations(range(n), 3)]


def get_next_output_folder(base: Path) -> Path:
    """
    Inside `base`, find folders with integer names, pick max + 1.
    """
    base.mkdir(parents=True, exist_ok=True)

    existing = [
        int(folder.name) for folder in base.iterdir()
        if folder.is_dir() and folder.name.isdigit()
    ]

    next_index = max(existing) + 1 if existing else 0
    new_folder = base / str(next_index)
    new_folder.mkdir()

    return new_folder


def write_csv_no_header(path: Path, rows: List[Tuple]):
    """Write CSV *without headers*."""
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)


def main(
    n_points: int = 19,
    output_base: str = "tests/resources/e2e/",
):
    """
    Generates:
      - vertices.csv
      - candidate_edges.csv
      - candidate_faces.csv
    inside tests/resources/e2e/<index>/
    """

    base_path = Path(output_base)
    output_folder = get_next_output_folder(base_path)

    # Generate core data
    vertices = generate_points(n_points)
    edges = generate_all_edges(n_points)
    faces = generate_all_faces(n_points)

    # Write files
    write_csv_no_header(output_folder / "vertices.csv", vertices)
    write_csv_no_header(output_folder / "candidate_edges.csv", edges)
    write_csv_no_header(output_folder / "candidate_faces.csv", faces)

    print(f"Generated triangulation dataset at: {output_folder}")


if __name__ == "__main__":
    main()

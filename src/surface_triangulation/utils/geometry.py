import numpy as np
from typing import List, Tuple
from shapely.strtree import STRtree
from shapely.geometry import MultiPoint
from shapely.geometry import Polygon, LineString

def find_edge_crossings(vertices: List[Tuple[float, float, float]], edges: List[Tuple[int, int]]):
    segments = []
    for (a, b) in edges:
        p1 = vertices[int(a)]
        p2 = vertices[int(b)]
        segments.append(LineString([p1, p2]))

    # Spatial index
    crossings = []
    tree = STRtree(segments)

    for idx, seg in enumerate(segments):
        candidates = tree.query(seg)

        for cand in candidates:
            # Avoid self + double counting
            if cand <= idx:
                continue

            # Check real intersection (not just touching at endpoints)
            if seg.crosses(segments[cand]):
                crossings.append((edges[idx], edges[cand]))

    return crossings

def points_are_planar(vertices: List[Tuple[float, float, float]]) -> bool:
    if len(vertices) <= 3:
        return True  # any 3 or fewer points are planar

    pts = np.asarray(vertices, dtype=float)

    # translate so first point is at origin
    shifted = pts - pts[0]

    # if the rank is <= 2 → points lie in a plane
    return bool(np.linalg.matrix_rank(shifted) <= 2)

def find_triangle_crossings(
    vertices: List[Tuple[float, float, float]],
    faces: List[Tuple[int, int, int]]
) -> List[Tuple[Tuple[int, int, int], Tuple[int, int, int]]]:

    # Drop z-coordinate
    verts_2d = [(x, y) for x, y, _ in vertices]

    # Precompute triangle polygons
    triangles = []
    for f in faces:
        i, j, k = f
        poly = Polygon([verts_2d[i], verts_2d[j], verts_2d[k]])
        triangles.append(poly)

    crossings = []

    # Check pairwise intersections
    n = len(faces)
    for a in range(n):
        A = triangles[a]
        if A is None:
            continue

        for b in range(a + 1, n):
            B = triangles[b]
            if B is None:
                continue

            if A.intersection(B).area > 0:
                crossings.append((faces[a], faces[b]))

    return crossings

def convex_hull_surface(vertices: List[Tuple[float, float, float]]) -> float:
    pts_2d = [(x, y) for x, y, _ in vertices]

    mp = MultiPoint(pts_2d)
    hull = mp.convex_hull

    return hull.area

def get_number_of_vertices_on_boundry(vertices: List[Tuple[float, float, float]]) -> int:
    pts_2d = [(x, y) for x, y, _ in vertices]

    mp = MultiPoint(pts_2d)
    hull = mp.convex_hull

    return len(hull.boundary.coords)-1
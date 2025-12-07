from typing import List, Tuple
from shapely.geometry import LineString
from shapely.strtree import STRtree

def find_edge_crossings(vertices: List[Tuple[float, float, float]], edges: List[Tuple[int, int]]):
    """
    vertices: list of (x, y)
    edges: list of (i, j) indices into vertices
    returns: list of ((i1, j1), (i2, j2)) intersecting edge pairs
    """
    
    # Build geometries
    segments = []
    for (a, b) in edges:
        p1 = vertices[int(a)]
        p2 = vertices[int(b)]
        segments.append(LineString([p1, p2]))

    # Spatial index
    tree = STRtree(segments)

    crossings = []

    for idx, seg in enumerate(segments):
        # Query candidate collisions from tree
        candidates = tree.query(seg)

        for cand in candidates:
            # Avoid self + double counting
            if cand <= idx:
                continue

            # Check real intersection (not just touching at endpoints)
            if seg.crosses(segments[cand]):
                crossings.append((edges[idx], edges[cand]))

    return crossings

from math import cos, sin, radians
import numpy as np
from surface_triangulation.utils.geometry import (
    find_edge_crossings,
    points_are_planar,
    find_triangle_crossings,
    convex_hull_surface
)

# -------------------------------
# Tests for find_edge_crossings
# -------------------------------

def test_find_edge_crossings_no_crossings():
    vertices = [(0.,0,0), (1,0,0), (1,1,0), (0,1,0)]
    edges = [(0,1), (2,3)]
    crossings = find_edge_crossings(vertices, edges)
    assert crossings == []

def test_find_edge_crossings_with_crossing():
    vertices = [(0.,0,0), (1,1,0), (0,1,0), (1,0,0)]
    edges = [(0,1), (2,3)]
    crossings = find_edge_crossings(vertices, edges)
    assert crossings == [(edges[0], edges[1])]

def test_find_edge_crossings_touching_at_endpoint():
    vertices = [(0.,0,0), (1,0,0), (1,1,0)]
    edges = [(0,1), (1,2)]
    crossings = find_edge_crossings(vertices, edges)
    # touching at endpoint should not count
    assert crossings == []

# -------------------------------
# Tests for points_are_planar
# -------------------------------

def test_points_are_planar_trivial():
    pts = [(0.,0,0), (1,0,0), (0,1,0)]
    assert points_are_planar(pts) is True

def test_points_are_planar_planar():
    pts = [(0.,0,0), (1,0,0), (0,1,0), (1,1,0)]
    assert points_are_planar(pts) is True

def test_points_are_planar_non_planar():
    pts = [(0.,0,0), (1,0,0), (0,1,0), (0,0,1)]
    assert points_are_planar(pts) is False

# -------------------------------
# Tests for find_triangle_crossings
# -------------------------------

def test_find_triangle_crossings_no_crossings():
    vertices = [(0,0,0.), (1,0,0), (0,1,0), (2,0,0), (2,1,0), (3,0,0)]
    faces = [(0,1,2), (3,4,5)]
    crossings = find_triangle_crossings(vertices, faces)
    assert crossings == []

def test_find_triangle_crossings_with_crossing():
    s = 1.0
    R = s  # circumradius of a regular hexagon

    vertices = [
        (R * cos(radians(  0)), R * sin(radians(  0)), 0.0),
        (R * cos(radians( 60)), R * sin(radians( 60)), 0.0),
        (R * cos(radians(120)), R * sin(radians(120)), 0.0),
        (R * cos(radians(180)), R * sin(radians(180)), 0.0),
        (R * cos(radians(240)), R * sin(radians(240)), 0.0),
        (R * cos(radians(300)), R * sin(radians(300)), 0.0),
    ]

    faces = [(0,4,5), (3,4,5)]
    crossings = find_triangle_crossings(vertices, faces)
    assert crossings == [(faces[0], faces[1])]

def test_find_triangle_crossings_degenerate():
    vertices = [(0,0,0.), (1,0,0), (2,0,0)]
    faces = [(0,1,2)]
    crossings = find_triangle_crossings(vertices, faces)
    # Degenerate triangle should not cause intersections
    assert crossings == []

# -------------------------------
# Tests for convex_hull_surface
# -------------------------------

def test_convex_hull_surface_square():
    vertices = [(0,0,0.), (1,0,0), (1,1,0), (0,1,0)]
    area = convex_hull_surface(vertices)
    assert np.isclose(area, 1.0)

def test_convex_hull_surface_triangle():
    vertices = [(0,0,0.), (1,0,0), (0,1,0)]
    area = convex_hull_surface(vertices)
    assert np.isclose(area, 0.5)

def test_convex_hull_surface_collinear():
    vertices = [(0,0,0.), (1,0,0), (2,0,0)]
    area = convex_hull_surface(vertices)
    assert area == 0.0

def test_convex_hull_surface_single_point():
    vertices = [(0.,0.,0.)]
    area = convex_hull_surface(vertices)
    assert area == 0.0

import csv
import io
from ast import literal_eval
from typing import List, Any, Tuple

def list_to_csv(data: List[List[Any]]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Convert each element to its repr so types can be restored later
    for row in data:
        writer.writerow([repr(item) for item in row])
    
    return output.getvalue()

def csv_to_list(csv_string: str) -> List[List[Any]]:
    input_io = io.StringIO(csv_string)
    reader = csv.reader(input_io)
    
    result = []
    for row in reader:
        # Use literal_eval to restore the original types
        result.append([literal_eval(item) for item in row])
    
    return result

def csv_to_vertices(csv_string: str) -> List[Tuple[float, float, float]]:
    rows = csv_to_list(csv_string)
    return [(float(row[0]), float(row[1]), float(row[2])) for row in rows]

def csv_to_edges(csv_string: str) -> List[Tuple[int, int]]:
    rows = csv_to_list(csv_string)
    return [(int(row[0]), int(row[1])) for row in rows]

def csv_to_faces(csv_string: str) -> List[Tuple[int, int, int]]:
    rows = csv_to_list(csv_string)
    return [(int(row[0]), int(row[1]), int(row[2])) for row in rows]

def vertices_to_csv(vertices: List[Tuple[float, float, float]]) -> str:
    rows = [[v[0], v[1], v[2]] for v in vertices]
    return list_to_csv(rows)

def edges_to_csv(edges: List[Tuple[int, int]]) -> str:
    rows = [[e[0], e[1]] for e in edges]
    return list_to_csv(rows)

def faces_to_csv(faces: List[Tuple[int, int, int]]) -> str:
    rows = [[f[0], f[1], f[2]] for f in faces]
    return list_to_csv(rows)

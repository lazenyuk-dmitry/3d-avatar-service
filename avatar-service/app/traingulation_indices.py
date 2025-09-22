from mediapipe.python.solutions.face_mesh_connections import FACEMESH_TESSELATION
from collections import defaultdict

edges = list(FACEMESH_TESSELATION)


neighbors = defaultdict(set)
for a, b in edges:
    neighbors[a].add(b)
    neighbors[b].add(a)

triangles = set()


for a in neighbors:
    for b in neighbors[a]:
        for c in neighbors[b]:
            if c in neighbors[a] and a < b < c:
                triangles.add((a, b, c))

TRIANGLES = sorted(triangles)

if __name__ == "__main__":
    print(f"Сгенерировано треугольников: {len(TRIANGLES)}")
    print(TRIANGLES[:10], "...")

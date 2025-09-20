import trimesh
from utils import get_path
from mesh_generator import generate_avatar

output_path = get_path("assets", "output_avatar.glb")

generate_avatar()

mesh = trimesh.load(output_path, force='mesh')

# Проверка основных свойств
print("Количество вершин:", len(mesh.vertices))
print("Количество граней:", len(mesh.faces))
print("Размеры объекта:", mesh.extents)

# Визуализация (если есть GUI)
# mesh.show()

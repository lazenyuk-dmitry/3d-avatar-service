import trimesh
from utils import get_path

output_path = get_path("assets", "output_avatar.glb")
mesh = trimesh.load(output_path, force='mesh')

# Проверка основных свойств
print("Количество вершин:", len(mesh.vertices))
print("Количество граней:", len(mesh.faces))
print("Размеры объекта:", mesh.extents)

# Визуализация (если есть GUI)
# mesh.show()

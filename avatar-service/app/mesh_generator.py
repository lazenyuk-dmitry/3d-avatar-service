import numpy as np
import trimesh
from face_detection import detect_face_landmarks
from traingulation_indices import TRIANGLES


def generate_avatar(input_image: str, output_path: str):
    pts = np.array(detect_face_landmarks(input_image))  # shape (468, 3) в [0..1]

    if pts.shape[0] < 468:
        raise ValueError("Недостаточно точек лица для генерации меша.")

    # Преобразование координат (из image space -> 3D со Y вверх)
    x = pts[:, 0] - 0.5  # центрируем X в 0
    y = 0.5 - pts[:, 1]  # инвертируем Y (теперь вверх)
    z = -pts[:, 2]  # часто нужно инвертировать Z (лицо «наружу»)

    V = np.stack([x, y, z], axis=1)

    V = V - V.mean(axis=0)
    V = V * 100.0

    F = np.array(TRIANGLES, dtype=np.int32)

    mesh = trimesh.Trimesh(vertices=V, faces=F, process=False)
    mesh.fix_normals()
    mesh.export(output_path)
    print(f"Экспортировано: {output_path}")
    return output_path

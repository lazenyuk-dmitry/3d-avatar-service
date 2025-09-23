import numpy as np, trimesh, uuid
from pathlib import Path
from face_detection import detect_face_landmarks
from traingulation_indices import TRIANGLES
from blender_runner import rig_in_blender

def generate_avatar(input_image: str, output_path: str):
    output_path = Path(output_path).resolve()
    temp_face_glb = output_path.with_name(f"face_{uuid.uuid4()}.glb")

    pts = np.array(detect_face_landmarks(input_image))
    if pts.shape[0] < 468:
        raise ValueError("Недостаточно точек лица для генерации меша.")

    x = pts[:, 0] - 0.5
    y = 0.5 - pts[:, 1]
    z = -pts[:, 2]
    V = np.stack([x, y, z], axis=1)
    V = (V - V.mean(axis=0)) * 100.0

    F = np.array(TRIANGLES, dtype=np.int32)
    mesh = trimesh.Trimesh(vertices=V, faces=F, process=False)
    mesh.fix_normals()

    temp_face_glb.parent.mkdir(parents=True, exist_ok=True)
    mesh.export(str(temp_face_glb))
    print(f"[GEN] Temp face glb -> {temp_face_glb}")

    # ВАЖНО: для Blender лучше posix-пути на Windows
    rig_in_blender(
        face_glb=temp_face_glb.as_posix(),
        out_glb=output_path.as_posix(),
        body_glb=Path("assets/base_body.glb").resolve().as_posix()
    )

    print(f"[GEN] Exported final -> {output_path}")
    return str(output_path)

from utils import get_path
import trimesh

def generate_avatar():
  face_mesh_obj = face_mesh()
  body_mesh_obj = body_mesh()
  full_mesh = merge_meshes(face_mesh_obj, body_mesh_obj)
  export_mesh(full_mesh)


def face_mesh():
  asset_path = get_path("assets", "base_head.glb")
  return trimesh.load(asset_path)


def body_mesh():
  asset_path = get_path("assets", "base_body.glb")
  return trimesh.load(asset_path)


def merge_meshes(face_mesh_obj, body_mesh_obj):
  body_mesh_obj.apply_translation([0, -1.5, 0])
  return trimesh.util.concatenate([face_mesh_obj, body_mesh_obj])


def export_mesh(mesh_obj):
  output_path = get_path("assets", "output_avatar.glb")
  mesh_obj.export(output_path)
  print(f"Экспортировано: {output_path}")

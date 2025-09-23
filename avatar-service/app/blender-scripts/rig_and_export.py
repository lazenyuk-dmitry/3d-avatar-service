import bpy, sys, os, math
from mathutils import Euler

argv = sys.argv
argv = argv[argv.index("--") + 1:] if "--" in argv else []
args = {argv[i].lstrip("-"): argv[i+1] for i in range(0, len(argv), 2)}

face_glb = args.get("face_glb")
out_glb  = args.get("out_glb", "avatar_rigged.glb")
body_glb = args.get("body_glb")  # опционально

if not face_glb:
    raise RuntimeError("Не задан --face_glb")

bpy.ops.wm.read_factory_settings(use_empty=True)

# импорт лица
bpy.ops.import_scene.gltf(filepath=face_glb)
face_obj = bpy.context.selected_objects[0]

# арматура
bpy.ops.object.armature_add(enter_editmode=True)
arm_obj = bpy.context.active_object
arm_obj.name = "Armature"
arm = arm_obj.data
bone = arm.edit_bones.new("Head")
bone.head = (0, 0, 0)
bone.tail = (0, 0, 0.3)
bpy.ops.object.mode_set(mode="OBJECT")

# автопривязка
bpy.ops.object.select_all(action="DESELECT")
face_obj.select_set(True)
arm_obj.select_set(True)
bpy.context.view_layer.objects.active = arm_obj
bpy.ops.object.parent_set(type="ARMATURE_AUTO")

# анимация
sc = bpy.context.scene
sc.frame_start = 0
sc.frame_end = 60
arm_obj.rotation_mode = "XYZ"
def key(f, rot): arm_obj.rotation_euler = rot; arm_obj.keyframe_insert(data_path="rotation_euler", frame=f)
key(0,  Euler((0,0,0)))
key(20, Euler((0,0,math.radians(30))))
key(40, Euler((0,0,math.radians(-30))))
key(60, Euler((0,0,0)))

# экспорт
os.makedirs(os.path.dirname(out_glb), exist_ok=True)
bpy.ops.export_scene.gltf(filepath=out_glb, export_format="GLB", export_apply=True)
print(f"[OK] Exported: {out_glb}")

import subprocess
import shutil
from pathlib import Path

BLENDER_BIN = shutil.which("blender") or r"C:\Program Files\Blender Foundation\Blender 4.5\blender.exe"

def rig_in_blender(face_glb: str, out_glb: str, body_glb: str):
    if not Path(BLENDER_BIN).exists():
        raise RuntimeError(f"Blender не найден: {BLENDER_BIN}")

    script_path = (Path(__file__).resolve().parent / "blender-scripts" / "rig_and_export.py").resolve()

    if not script_path.exists():
        raise RuntimeError(f"Blender-скрипт не найден: {script_path}")

    cmd = [
        str(BLENDER_BIN), "-b",
        "--python", str(script_path),
        "--",
        "--face_glb", str(face_glb),
        "--out_glb", str(out_glb),
        "--body_glb", str(body_glb)
    ]

    print(f"[BLENDER CMD]: {' '.join(cmd)}")
    proc = subprocess.run(cmd, capture_output=True, text=True)

    print("[BLENDER STDOUT]\n", proc.stdout)
    print("[BLENDER STDERR]\n", proc.stderr)

    if proc.returncode != 0:
        raise RuntimeError(f"Blender pipeline failed (code {proc.returncode})")

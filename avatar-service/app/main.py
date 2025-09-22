from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from mesh_generator import generate_avatar
from fastapi.responses import JSONResponse
import cv2, mediapipe as mp, tempfile, os
import os
from pathlib import Path, PurePosixPath

app = FastAPI(title="3D Avatar Service")

mp_face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=True)

PUBLIC_DIR = Path("public")
AVATAR_PATH = Path(PUBLIC_DIR, "avatar.glb")

def extract_best_frame(video_path: str):
    """Извлекаем самый чёткий кадр из видео."""
    cap = cv2.VideoCapture(video_path)
    best_frame, best_score = None, -1

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        score = cv2.Laplacian(frame, cv2.CV_64F).var()
        if score > best_score:
            best_score = score
            best_frame = frame

    cap.release()
    return best_frame

def generate_avatar_from_image(image_path: str):
    """Пример: извлекаем ключевые точки лица и возвращаем путь к аватару."""
    img = cv2.imread(image_path)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = mp_face_mesh.process(rgb)

    if not results.multi_face_landmarks:
        raise ValueError("Лицо не найдено")

    # Пример: создаём пустой .glb (для реального проекта подключите Trimesh/PyTorch3D/Blender)
    with open(AVATAR_PATH, "wb") as f:
        f.write(b"glTF placeholder")  # заглушка

    return AVATAR_PATH

# Можно сделать public директорию но тогда оттуда файлы не скачиваются
# app.mount("/public", StaticFiles(directory=PUBLIC_DIR), name="public")

@app.get("/")
def root():
    return {"message": "3D Avatar API is running"}

@app.post("/generate-avatar/")
async def generate_avatar_endpoint(file: UploadFile = File(...)):
    # Определяем временный путь для сохранения входного файла
    suffix = os.path.splitext(file.filename)[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    # Если видео — извлекаем кадр, иначе работаем как с фото
    if suffix.lower() in [".mp4", ".webm", ".avi", ".mov"]:
        frame = extract_best_frame(tmp_path)
        frame_path = tmp_path + "_frame.jpg"
        cv2.imwrite(frame_path, frame)
        avatar_path = generate_avatar_from_image(frame_path)
    else:
        avatar_path = generate_avatar_from_image(tmp_path)

    # Возвращаем путь к готовому аватару (или URL)
    return JSONResponse({"model_url": f"http://localhost:8000/{PurePosixPath(avatar_path)}"})
from fastapi import FastAPI

@app.get("/public/avatar.glb")
async def get_avatar():
    if AVATAR_PATH.exists():
        return FileResponse(AVATAR_PATH, media_type="model/gltf-binary", filename="avatar.glb")
    return {"detail": "Avatar not found"}

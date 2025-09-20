from .face_detection import detect_face_landmarks
import shutil

def generate_avatar(input_path: str, output_path: str):
    print("[] Детектируем лицо...")
    landmarks = detect_face_landmarks('input_path')
    print(f"[] Найдено ключевых точек: {len(landmarks)}")
    # Пока просто копируем заглушку .glb
    sample = "static/sample_output.glb"
    shutil.copy(sample, output_path)

import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh


def detect_face_landmarks(image_path: str):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1) as face_mesh:
        results = face_mesh.process(image_rgb)

        if not results.multi_face_landmarks:
            raise ValueError("Лицо не найдено.")

        landmarks = results.multi_face_landmarks[0]
        points = []
        for lm in landmarks.landmark:
            points.append((lm.x, lm.y, lm.z))

        return points

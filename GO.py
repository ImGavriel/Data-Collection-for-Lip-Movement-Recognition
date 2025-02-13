import cv2
import mediapipe as mp
import numpy as np
import requests  # נוסיף את המודול לשליחת נתונים
import os

SERVER_URL = "https://your-app-name.up.railway.app/upload"


def main():
    word = "מה השעה"  # המילה הנלמדת

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True
    )
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    cap = cv2.VideoCapture(0)
    input("לחצו ENTER כדי להתחיל בהקלטה...")

    frames_data = []
    frame_count = 0

    print("📹 ההקלטה התחילה. כדי לסיים, לחצו SPACE בחלון הוידאו.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    face_landmarks,
                    mp_face_mesh.FACEMESH_LIPS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
                )
                lip_points = [(landmark.x, landmark.y, landmark.z) for landmark in face_landmarks.landmark]
                frames_data.append([frame_count] + np.array(lip_points).flatten().tolist())

        frame_count += 1
        cv2.imshow("Lip Tracking", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 32:
            break

    cap.release()
    cv2.destroyAllWindows()

    if frames_data:
        data_to_send = {
            "word": word,
            "frames": frames_data
        }

        try:
            response = requests.post(SERVER_URL, json=data_to_send)
            print(response.json())  # הצגת תשובת השרת
        except Exception as e:
            print(f"⚠️ שגיאה בשליחת הנתונים לשרת: {e}")
    else:
        print("⚠️ לא נאספו נתונים.")

if __name__ == "__main__":
    main()

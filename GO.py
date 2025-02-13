import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import os

def main():
    # הגדרת המילה להקלטה (שנה את המילה כרצונך)
    word = "מה השעה"
    
    # אתחול MediaPipe לזיהוי נקודות פנים (כולל שפתיים)
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True
    )
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    # יצירת תיקייה לשמירת הנתונים, אם לא קיימת
    os.makedirs("data", exist_ok=True)
    
    # פתיחת מצלמה
    cap = cv2.VideoCapture(0)
    
    # הודעה: הקלטה תתחיל בלחיצה על ENTER
    input("לחצו ENTER כדי להתחיל בהקלטה...")
    
    frames_data = []
    frame_count = 0

    print("📹 ההקלטה התחילה. כדי לסיים, לחצו SPACE בחלון הוידאו.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # המרת התמונה ל-RGB (Mediapipe דורש פורמט זה)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # ציור נקודות השפתיים על המסך (אופציונלי)
                mp_drawing.draw_landmarks(
                    frame,
                    face_landmarks,
                    mp_face_mesh.FACEMESH_LIPS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
                )
                # איסוף קואורדינטות נקודות השפתיים (x, y, z)
                lip_points = [(landmark.x, landmark.y, landmark.z) for landmark in face_landmarks.landmark]
                # שומר את מספר הפריים ואחריו את כל נקודות השפתיים כערכים שטוחים
                frames_data.append([frame_count] + np.array(lip_points).flatten().tolist())

        frame_count += 1
        cv2.imshow("Lip Tracking", frame)

        # בדיקה: אם לוחצים על SPACE (ASCII 32) – סיום ההקלטה
        key = cv2.waitKey(1) & 0xFF
        if key == 32:
            break

    # שחרור המצלמה וסגירת חלונות
    cap.release()
    cv2.destroyAllWindows()

    # שמירת הנתונים לקובץ CSV אם נאספו נתונים
    if frames_data:
        num_points = (len(frames_data[0]) - 1) // 3
        columns = ["frame"]
        for i in range(num_points):
            columns.extend([f"x{i}", f"y{i}", f"z{i}"])
        df = pd.DataFrame(frames_data, columns=columns)
        csv_filename = f"data/{word}.csv"
        df.to_csv(csv_filename, index=False, encoding="utf-8-sig")
        print(f"✅ הנתונים נשמרו בהצלחה בקובץ: {csv_filename}")
    else:
        print("⚠️ לא נאספו נתונים.")

if __name__ == "__main__":
    main()


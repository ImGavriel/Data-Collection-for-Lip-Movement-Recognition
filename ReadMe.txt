תיעוד לפרויקט: איסוף נתונים לזיהוי תנועות שפתיים
1. הקדמה
פרויקט זה מיועד לאיסוף נתונים לתנועה של השפתיים בזמן אמת, תוך שימוש בספריות OpenCV ו-Mediapipe לזיהוי נקודות הפנים (עם דגש על השפתיים). הנתונים שנאספים נשמרים כקובץ CSV בתיקייה בשם data. המידע יכול לשמש לאימון מודלים לזיהוי תנועות שפתיים.

2. דרישות
ספריות ותלויות (Dependencies)
יש להתקין את הספריות הבאות:

Python 3.8 ומעלה
OpenCV – לטעינת ועיבוד תמונות (וידאו)
MediaPipe – לזיהוי נקודות פנים, עם דגש על זיהוי שפתיים
NumPy – לעיבוד נתונים בצורה וקטורית
Pandas – לטיפול ושמירת הנתונים כקבצי CSV
os – (מודול מובנה) לעבודה עם מערכת הקבצים
רשימת ההתקנות (באמצעות pip)
ניתן להתקין את כל הספריות הדרושות באמצעות הפקודות הבאות (יש לפתוח טרמינל/Command Prompt):

bash
Copy
Edit
pip install opencv-python mediapipe numpy pandas
הערה: מודול os הוא מודול מובנה ב-Python, ואין צורך להתקין אותו.

3. הוראות התקנה והרצה
התקן את Python 3.8+
ודא ש-Python מותקן במחשב שלך. ניתן להוריד מהאתר python.org.

התקן את הספריות הדרושות
הפעל את הפקודות הבאות בטרמינל:

bash
Copy
Edit
pip install opencv-python mediapipe numpy pandas
שמור את הקוד
שמור את הקוד בקובץ, לדוגמה: GO.py.

הרץ את הקוד
פתח טרמינל ועבור לתיקייה בה נמצא הקובץ, והריץ:

bash
Copy
Edit
python GO.py
כאשר הקוד יפעל, הוא:

יפעיל את המצלמה.
יחכה ללחיצה על Enter כדי להתחיל בהקלטה.
יעקוב אחרי תנועות השפתיים בזמן אמת, יציג חלון עם המעקב.
יפסיק את ההקלטה כאשר תלחץ על SPACE.
ישמור את הנתונים בקובץ CSV בתיקייה data עם שם הקובץ המבוסס על המילה שהוגדרה (מה השעה.csv).
4. הסבר הקוד
4.1. יבוא ספריות:
python
Copy
Edit
import cv2                # ספריית OpenCV לעיבוד תמונה ווידאו
import mediapipe as mp    # ספריית Mediapipe לזיהוי נקודות פנים (Face Mesh)
import numpy as np        # ספריית NumPy לעבודה עם מערכים ונתונים מתמטיים
import pandas as pd       # ספריית Pandas לטיפול בנתונים ושמירתם כקבצי CSV
import os                 # מודול לעבודה עם מערכת הקבצים (יצירת תיקיות, ניהול נתיבים וכו')
4.2. פונקציית main:
python
Copy
Edit
def main():
    # הגדרת המילה להקלטה (ניתן לשנות לפי צורך)
    word = "מה השעה"
כאן מוגדרת המילה שתשמש גם כשם הקובץ שבו ישמרו הנתונים.
4.3. אתחול Mediapipe:
python
Copy
Edit
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True
    )
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
אתחול מודל FaceMesh של Mediapipe לזיהוי נקודות פנים (עם דגש על שפתיים).
4.4. יצירת תיקייה לשמירת הנתונים:
python
Copy
Edit
    os.makedirs("data", exist_ok=True)
יוצר תיקייה בשם data אם היא לא קיימת, שבה ישמרו קבצי ה-CSV.
4.5. פתיחת המצלמה והתחלת ההקלטה:
python
Copy
Edit
    cap = cv2.VideoCapture(0)
    input("לחצו ENTER כדי להתחיל בהקלטה...")
פתיחת מצלמה (0 – המצלמה הראשית) והמתנה ללחיצת Enter.
4.6. איסוף הנתונים:
python
Copy
Edit
    frames_data = []
    frame_count = 0
    print("📹 ההקלטה התחילה. כדי לסיים, לחצו SPACE בחלון הוידאו.")
אתחול משתנים לאיסוף הנתונים, ומספר הפריים.
4.7. לולאת הקלטה:
python
Copy
Edit
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
קריאת פריים מהמצלמה, המרה ל-RGB (נדרש על ידי Mediapipe) ועיבוד הפריים לזיהוי נקודות פנים.
4.8. עיבוד ותצוגה:
python
Copy
Edit
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
אם נמצאו נקודות פנים, מציירים את נקודות השפתיים על הפריים ואוספים את הקואורדינטות (x, y, z) עבור כל נקודה.
הנתונים מאוחסנים כמערך שבו הפריים הראשון הוא מספר הפריים ואחריו הקואורדינטות (בתצורה שטוחה).
4.9. עדכון והצגת הפריים:
python
Copy
Edit
        frame_count += 1
        cv2.imshow("Lip Tracking", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 32:
            break
עדכון מספר הפריים והצגת חלון עם התמונה.
אם תלחץ על SPACE (ASCII 32), הלולאה נפסקת.
4.10. סיום ההקלטה:
python
Copy
Edit
    cap.release()
    cv2.destroyAllWindows()
שחרור המצלמה וסגירת כל חלונות התצוגה.
4.11. שמירת הנתונים כקובץ CSV:
python
Copy
Edit
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
אם נאספו נתונים, נבנה DataFrame עם כותרות לעמודות (העמודה הראשונה היא "frame", ואחריה העמודות עבור כל נקודת מעקב).
הקובץ נשמר בתיקייה data עם שם המבוסס על המילה (לדוגמה, "מה השעה.csv").
מדפיס הודעה על הצלחת השמירה או אזהרה אם לא נאספו נתונים.
5. סיכום
הקוד:

עוקב אחרי תנועת השפתיים בזמן אמת.
מציג את המעקב על חלון וידאו.
אוסף את הנתונים בכל פריים ושומר אותם במבנה CSV.
יוצר תיקייה בשם data לשמירת קבצי הנתונים.
מה יש להתקין?
Python 3.8+
OpenCV (opencv-python)
MediaPipe
NumPy
Pandas
ניתן להתקין את כל הספריות באמצעות:

bash
Copy
Edit
pip install opencv-python mediapipe numpy pandas
6. הוראות הפעלה
התקן את כל הספריות.
שמור את הקוד בקובץ (לדוגמה, GO.py).
הפעל את הקובץ:
bash
Copy
Edit
python GO.py
לחץ על Enter כדי להתחיל בהקלטה.
לחץ על SPACE כדי לעצור את ההקלטה.
הנתונים ישמרו כקובץ CSV בתיקייה data.

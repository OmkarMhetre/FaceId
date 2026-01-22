import cv2
import face_recognition
import numpy as np
from backend.db.mysql_utils import get_all_faces
from backend.db.attendance_utils import mark_attendance

def load_known_faces():
    known_faces = get_all_faces()
    encodings = []
    names = []

    for name, encoding_bytes in known_faces:
        encoding = np.frombuffer(encoding_bytes, dtype=np.float64)
        encodings.append(encoding)
        names.append(name)

    return encodings, names


KNOWN_ENCODINGS, KNOWN_NAMES = load_known_faces()


def recognize_faces(image_bytes: bytes):
    np_img = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    results = []

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        name = "Unknown"
        color = "red"

        if KNOWN_ENCODINGS:
            distances = face_recognition.face_distance(KNOWN_ENCODINGS, face_encoding)
            min_index = np.argmin(distances)

            if distances[min_index] < 0.6:
                name = KNOWN_NAMES[min_index]
                color = "green"

                mark_attendance(name)

        results.append({
            "name": name,
            "color": color,
            "box": {
                "top": top,
                "right": right,
                "bottom": bottom,
                "left": left
            }
        })

    return results

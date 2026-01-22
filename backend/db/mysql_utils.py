import numpy as np
from backend.db.db import get_db_connection

def add_face_to_db(name: str, encoding: np.ndarray):
    conn = get_db_connection()
    cursor = conn.cursor()

    if isinstance(encoding, np.ndarray):
        encoding_bytes = encoding.tobytes()
    else:
        encoding_bytes = encoding  # already bytes, use as-is

    query = "INSERT INTO faces (name, encoding) VALUES (%s, %s)"
    cursor.execute(query, (name, encoding_bytes))

    conn.commit()
    cursor.close()
    conn.close()


def get_all_faces():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name, encoding FROM faces")
    rows = cursor.fetchall()

    faces = []
    for name, encoding_blob in rows:
        encoding = np.frombuffer(encoding_blob, dtype=np.float64)  # ✅ bytes → numpy array

        faces.append((name, encoding))

    cursor.close()
    conn.close()

    return faces

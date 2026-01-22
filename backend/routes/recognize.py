import pymysql
from fastapi import APIRouter, UploadFile, File
from backend.face.recognize_service import recognize_faces
from backend.db.db import get_db_connection

router = APIRouter()

@router.post("/recognize")
async def recognize_face(image: UploadFile = File(...)):
    image_bytes = await image.read()
    results = recognize_faces(image_bytes)
    return {"faces": results}

@router.get("/attendance")
def get_attendance():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            name,
            DATE_FORMAT(date, '%d-%m-%Y') AS date,
            TIME_FORMAT(time, '%h:%i %p') AS time
        FROM attendance
        ORDER BY date DESC, time DESC
    """)

    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return records

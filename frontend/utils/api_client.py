import requests
import cv2


BASE_URL = "http://127.0.0.1:8000"

def send_frame_to_backend(frame):
    _, buffer = cv2.imencode(".jpg", frame)
    files = {"image": ("frame.jpg", buffer.tobytes(), "image/jpeg")}

    response = requests.post(f"{BASE_URL}/recognize", files=files, timeout=5)
    response.raise_for_status()
    return response.json()


def get_attendance():
    """
    Fetch attendance records from backend
    """
    try:
        response = requests.get(f"{BASE_URL}/attendance")
        response.raise_for_status()
        return response.json()   # list of rows
    except Exception as e:
        print("Attendance API error:", e)
        return []
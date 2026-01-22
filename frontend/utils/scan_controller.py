import cv2
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel
from frontend.utils.api_client import send_frame_to_backend
import frontend.utils.record_controller as record_controller

recognized_faces = {}

cap = None
timer = None


def on_scan_clicked(ui):
    global cap, timer

    ui.tabWid.setCurrentIndex(1)
    ui.btn_admin.hide()
    ui.btn_record.hide()
    ui.close_cam.clicked.connect(lambda: stop_camera(ui))

    scan_tab = ui.tabWid.widget(1)

    cap = cv2.VideoCapture(0)

    timer = QTimer(scan_tab)
    timer.timeout.connect(lambda: scan_frame(ui.tabWid))
    timer.start(100)


def scan_frame(tabWid):
    global cap

    lbl_video = tabWid.findChild(QLabel, "lbl_camera")
    lbl_name = tabWid.findChild(QLabel, "lbl_name")

    ret, frame = cap.read()
    if not ret:
        return

    try:
        result = send_frame_to_backend(frame)
        faces = result.get("faces", [])

        for face in faces:
            box = face["box"]
            name = face["name"]
            color = (0, 255, 0) if face["color"] == "green" else (0, 0, 255)

            top = box["top"]
            right = box["right"]
            bottom = box["bottom"]
            left = box["left"]

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)


            cv2.putText(
                frame, name, (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2
            )

            lbl_name.setText(name)

    except Exception as e:
        print("Backend error:", e)

    h, w, ch = frame.shape
    qt_img = QImage(frame.data, w, h, w * ch, QImage.Format_BGR888)
    lbl_video.setPixmap(QPixmap.fromImage(qt_img))

def stop_camera(ui):
    global cap, timer

    if timer:
        timer.stop()
        timer = None

    if cap:
        cap.release()
        cap = None

    cv2.destroyAllWindows()
    print("Camera stopped")
    ui.btn_admin.show()
    ui.btn_record.show()
    record_controller.on_record_clicked(ui)

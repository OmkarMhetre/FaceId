import mimetypes

import requests
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtGui import QPixmap


def add_face(ui):

        face_name = ui.u_name.text().strip()
        if not face_name:
            QMessageBox.warning(ui, "Input Error", "Please enter a name first.")
            return

        file_path, _ = QFileDialog.getOpenFileName(
            ui,  # IMPORTANT
            "Select Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )

        print("Dialog returned:", file_path)  # Debug

        if not file_path:
            return

        pixmap = QPixmap(file_path)
        ui.image.setPixmap(pixmap.scaled(ui.image.width(), ui.image.height()))

        ui.selected_image_path = file_path
        ui.selected_face_name = face_name


def upload_to_api(ui):
    if not hasattr(ui, "selected_image_path"):
        QMessageBox.warning(ui, "Error", "Please select an image first.")
        return

    url = "http://127.0.0.1:8000/add-face"

    mime_type, _ = mimetypes.guess_type(ui.selected_image_path)
    if not mime_type:
        mime_type = "image/jpeg"  # fallback

    with open(ui.selected_image_path, "rb") as f:
        files = {
            "image": (
                ui.selected_image_path.split("/")[-1],  # filename
                f,
                mime_type
            )
        }
        data = {"name": ui.selected_face_name}

        response = requests.post(url, files=files, data=data)

    if response.status_code == 200:
        QMessageBox.information(ui, "Success", "Face uploaded successfully!")
    else:
        QMessageBox.warning(ui, "Failed", response.text)

    # ✅ Proper cleanup
    ui.u_name.clear()
    ui.image.clear()
    del ui.selected_image_path
    ui.selected_face_name = ""
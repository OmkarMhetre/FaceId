import requests
from PySide6.QtWidgets import QMessageBox

def on_admin_clicked(ui):
    ui.tabWid.setCurrentIndex(3)

    def login_click():
        username = ui.username.text()
        password = ui.password.text()
        print("Username:", username, "Password:", password)
        if not username or not password:
            QMessageBox.warning(None, "Input Error", "Enter username and password")
            return

        try:
            # Send POST request to FastAPI login endpoint
            response = requests.post(
                "http://127.0.0.1:8000/login",
                json={"username": username, "password": password}
            )

            if response.status_code != 200:
                QMessageBox.warning(None, "Login Failed", response.json().get("detail", "Unknown error"))
                return

            data = response.json()

            if data["role"] != "ADMIN":
                QMessageBox.warning(None, "Access Denied", "Only admin can log in")
                return

            QMessageBox.information(None, "Success", f"Admin {username} logged in!")

            ui.tabWid.setCurrentIndex(4)

        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))

    ui.btn_login.clicked.connect(login_click)






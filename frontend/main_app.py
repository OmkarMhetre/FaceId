import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QCoreApplication
from utils.scan_controller import on_scan_clicked
from utils.admin_controller import on_admin_clicked
from utils.record_controller import on_record_clicked
from utils.add_face_controller import *
from ui import res

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui_file = QFile("ui/main_ui.ui")

        ui_file.open(QFile.OpenModeFlag.ReadOnly)
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.setCentralWidget(self.ui)

        # Hide tabs
        self.ui.tabWid.tabBar().hide()
        self.ui.tabWid.setCurrentIndex(0)

        self.showFullScreen()
        self.show()
        self.ui.closeBtn.clicked.connect(QCoreApplication.quit)
        self.ui.minBtn.clicked.connect(self.showMinimized)

        self.ui.btn_scan.clicked.connect(
            lambda: on_scan_clicked(self.ui)
        )

        self.ui.btn_record.clicked.connect(
            lambda: on_record_clicked(self.ui)

        )

        self.ui.btn_admin.clicked.connect(
            lambda: on_admin_clicked(self.ui)
        )

        self.ui.btn_add_face.clicked.connect(lambda: add_face(self.ui))
        self.ui.btn_upload.clicked.connect(lambda: upload_to_api(self.ui))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

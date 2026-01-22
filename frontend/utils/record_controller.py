
from frontend.utils.attendance_controller import load_attendance

def on_record_clicked(ui):

    ui.tabWid.setCurrentIndex(2)
    load_attendance(ui.tableView)

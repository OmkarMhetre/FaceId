from PySide6.QtGui import QStandardItemModel, QStandardItem
from frontend.utils.api_client import get_attendance


def load_attendance(tableView):
    data = get_attendance()

    model = QStandardItemModel()
    model.setHorizontalHeaderLabels(["Name", "Date", "Time"])

    for row in data:
        name, date, time = row   # 👈 tuple unpacking

        model.appendRow([
            QStandardItem(str(name)),
            QStandardItem(str(date)),
            QStandardItem(str(time))
        ])

    tableView.setModel(model)
    tableView.resizeColumnsToContents()

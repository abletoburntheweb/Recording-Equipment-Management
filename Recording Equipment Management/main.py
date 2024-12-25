import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from add_equipment_dialog import AddEquipmentDialog
from edit_equipment_dialog import EditEquipmentDialog
from styles import main_window, sidebar, back_button, add_button, table_widget


class StudioWindow(QWidget):
    def __init__(self, studio_name="Студия 1"):
        super().__init__()
        self.studio_name = studio_name
        self.layout = QVBoxLayout(self)

        self.header_layout = QHBoxLayout()
        self.header_label = QLabel(f"Студия: {studio_name}")
        self.header_label.setStyleSheet("QLabel { font-size: 20px; color: #333; }")
        self.header_layout.addWidget(self.header_label)

        self.add_button = QPushButton("Добавить оборудование")
        self.add_button.setStyleSheet(add_button())
        self.add_button.clicked.connect(self.open_add_equipment_dialog)
        self.header_layout.addWidget(self.add_button)

        self.header_layout.addStretch()
        self.layout.addLayout(self.header_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Наименование", "Код", "Артикул", "Тип", "Состояние"])
        self.table.setStyleSheet(table_widget())
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(40)

        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.table.doubleClicked.connect(self.edit_equipment)

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.layout.addWidget(self.table)

    def edit_equipment(self, index):
        row = index.row()

        name = self.table.item(row, 0).text()
        code = self.table.item(row, 1).text()
        article = self.table.item(row, 2).text()
        item_type = self.table.item(row, 3).text()
        status = self.table.item(row, 4).text()

        dialog = EditEquipmentDialog(
            name=name,
            code=code,
            article=article,
            equipment_type=item_type,
            condition=status,
            parent=self
        )

        if dialog.exec_() == QDialog.Accepted:
            self.table.setItem(row, 0, QTableWidgetItem(dialog.name))
            self.table.setItem(row, 1, QTableWidgetItem(dialog.code))
            self.table.setItem(row, 2, QTableWidgetItem(dialog.article))
            self.table.setItem(row, 3, QTableWidgetItem(dialog.equipment_type))
            self.table.setItem(row, 4, QTableWidgetItem(dialog.condition))

    def open_add_equipment_dialog(self):
        dialog = AddEquipmentDialog(self)
        if dialog.exec_() == QDialog.Accepted:

            name = dialog.name_input.text()
            code = dialog.code_input.text()
            article = dialog.article_input.text()
            status = dialog.get_status()
            item_type = dialog.type_input.currentText()

            row_count = self.table.rowCount()
            self.table.insertRow(row_count)
            self.table.setItem(row_count, 0, QTableWidgetItem(name))
            self.table.setItem(row_count, 1, QTableWidgetItem(code))
            self.table.setItem(row_count, 2, QTableWidgetItem(article))
            self.table.setItem(row_count, 3, QTableWidgetItem(item_type))
            self.table.setItem(row_count, 4, QTableWidgetItem(status))


class Studio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Учет оборудования звукозаписи")
        self.setGeometry(100, 100, 1280, 720)
        self.setStyleSheet(main_window())

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.studio_window = StudioWindow()
        self.layout.addWidget(self.studio_window)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    studio = Studio()
    studio.show()
    sys.exit(app.exec_())

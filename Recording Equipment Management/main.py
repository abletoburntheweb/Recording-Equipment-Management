import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox, QHeaderView, QStackedWidget, QFrame, QDialog, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from add_equipment_dialog import AddEquipmentDialog
from styles import main_window, sidebar, studios_button, equipment_button, back_button, add_button, table_widget


class Studios(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Учет оборудования звукозаписи")
        self.setGeometry(100, 100, 1280, 720)
        self.setStyleSheet(main_window())

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet(sidebar())
        self.sidebar_layout = QVBoxLayout(self.sidebar)

        self.studios_button = QPushButton("Студии")
        self.studios_button.setStyleSheet(studios_button())
        self.studios_button.clicked.connect(self.show_studios)
        self.sidebar_layout.addWidget(self.studios_button)

        self.equipment_button = QPushButton("Оборудование")
        self.equipment_button.setStyleSheet(equipment_button())
        self.equipment_button.clicked.connect(self.show_equipment)
        self.sidebar_layout.addWidget(self.equipment_button)

        self.layout.addWidget(self.sidebar)

        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.studios_widget = QWidget()
        self.studios_layout = QVBoxLayout(self.studios_widget)

        self.studio_buttons = [
            QPushButton("Студия 1"),
            QPushButton("Студия 2"),
            QPushButton("Студия 3")
        ]

        for button in self.studio_buttons:
            button.clicked.connect(self.open_studio)
            button.setStyleSheet(studios_button())
            self.studios_layout.addWidget(button)

        self.stacked_widget.addWidget(self.studios_widget)

        self.studio_windows = {}
        self.last_studio = None

    def open_studio(self):
        sender = self.sender()
        studio_name = sender.text()
        if studio_name not in self.studio_windows:
            self.studio_windows[studio_name] = StudioWindow(studio_name)
            self.studio_windows[studio_name].back_to_studios.connect(self.show_studios)
        self.stacked_widget.addWidget(self.studio_windows[studio_name])
        self.stacked_widget.setCurrentWidget(self.studio_windows[studio_name])
        self.last_studio = studio_name

    def show_studios(self):
        self.stacked_widget.setCurrentWidget(self.studios_widget)

    def show_equipment(self):
        if self.last_studio and self.last_studio in self.studio_windows:
            self.stacked_widget.setCurrentWidget(self.studio_windows[self.last_studio])


class StudioWindow(QWidget):
    back_to_studios = pyqtSignal()

    def __init__(self, studio_name):
        super().__init__()
        self.studio_name = studio_name
        self.layout = QVBoxLayout(self)

        self.header_layout = QHBoxLayout()
        self.header_label = QLabel(f"Студия: {studio_name}")
        self.header_label.setStyleSheet("QLabel { font-size: 20px; color: #333; }")
        self.header_layout.addWidget(self.header_label)

        self.back_button = QPushButton("Назад к студиям")
        self.back_button.setStyleSheet(back_button())
        self.back_button.clicked.connect(self.back_to_studios.emit)
        self.header_layout.addWidget(self.back_button)

        self.add_button = QPushButton("Добавить оборудование")
        self.add_button.setStyleSheet(add_button())
        self.add_button.clicked.connect(self.open_add_equipment_dialog)
        self.header_layout.addWidget(self.add_button)

        self.header_layout.addStretch()
        self.layout.addLayout(self.header_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Наименование", "Код", "Артикул", "Кол-во", "Тип"])
        self.table.setStyleSheet(table_widget())
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(40)

        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.layout.addWidget(self.table)

    def open_add_equipment_dialog(self):
        dialog = AddEquipmentDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            name = dialog.name_input.text()
            code = dialog.code_input.text()
            article = dialog.article_input.text()
            quantity = dialog.quantity_input.text()
            item_type = dialog.type_input.currentText()

            row_count = self.table.rowCount()
            self.table.insertRow(row_count)
            self.table.setItem(row_count, 0, QTableWidgetItem(name))
            self.table.setItem(row_count, 1, QTableWidgetItem(code))
            self.table.setItem(row_count, 2, QTableWidgetItem(article))
            self.table.setItem(row_count, 3, QTableWidgetItem(quantity))
            self.table.setItem(row_count, 4, QTableWidgetItem(item_type))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    studios = Studios()
    studios.show()
    sys.exit(app.exec_())

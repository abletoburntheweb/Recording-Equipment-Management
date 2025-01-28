from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from styles import add_item_dialog

class AddItemDialog(QDialog):
    def __init__(self, table_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить элемент")
        self.setGeometry(200, 200, 400, 200)

        self.setStyleSheet(add_item_dialog())

        self.layout = QVBoxLayout(self)
        self.table_name = table_name

        placeholders = {
            "brand": "Введите название бренда",
            "color": "Введите название цвета",
            "type": "Введите название типа",
            "model": "Введите название модели",
        }

        placeholder_text = placeholders.get(table_name, "Введите значение")

        title_label = QLabel("Добавить элемент")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 36, QFont.Bold))
        self.layout.addWidget(title_label)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText(placeholder_text)
        self.layout.addWidget(self.input_field)

        if self.table_name == "brand":
            self.country_field = QLineEdit(self)
            self.country_field.setPlaceholderText("Введите страну")
            self.layout.addWidget(self.country_field)

        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("ОК")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        self.layout.addLayout(button_layout)

    def get_inputs(self):
        # Если добавляется бренд, возвращаем два поля
        if self.table_name == "brand":
            return self.input_field.text(), self.country_field.text()
        return self.input_field.text(), None

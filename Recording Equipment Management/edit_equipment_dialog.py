from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QComboBox, QTextEdit, QPushButton, QVBoxLayout,
                             QHBoxLayout, QGridLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class EditEquipmentDialog(QDialog):
    def __init__(self, name="", brand="", country="", supplier="", condition="", serial_number="",
                 code="", article="", quantity="1", equipment_type="Гитара", color="Красный", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактирование оборудования")
        self.setFixedSize(1280, 720)

        # Присваиваем переданные данные в свойства
        self.name = name
        self.brand = brand
        self.country = country
        self.supplier = supplier
        self.condition = condition
        self.serial_number = serial_number
        self.code = code
        self.article = article
        self.quantity = quantity
        self.equipment_type = equipment_type
        self.color = color

        # Устанавливаем интерфейс и стили
        self.setup_ui()
        self.apply_styles()

    def set_values(self, name, code, article, quantity, item_type):
        # Устанавливаем значения в поля
        self.title.setText(name)
        self.code_field.setText(code)
        self.article_field.setText(article)
        self.quantity_field.setText(quantity)
        self.type_combobox.setCurrentText(item_type)

    def setup_ui(self):
        # Основной макет
        main_layout = QVBoxLayout(self)

        # Верхний макет: заголовок и изображение
        top_layout = QHBoxLayout()
        self.title = QLineEdit(self.name)
        self.title.setAlignment(Qt.AlignCenter)
        self.image_label = QLabel("Изображение")
        self.image_label.setObjectName("image_label")
        self.image_label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(self.image_label, 2)
        top_layout.addWidget(self.title, 3)

        # Средний макет: описание и таблица
        middle_layout = QHBoxLayout()
        self.description = QTextEdit("Описание")
        self.description.setReadOnly(False)

        self.details_layout = QGridLayout()

        self.details_layout.addWidget(QLabel("Общие сведения"), 0, 0, 1, 2)
        self.add_label_and_field("Бренд", self.brand, 1, self.details_layout)
        self.add_label_and_field("Страна", self.country, 2, self.details_layout)
        self.add_label_and_field("Поставщик", self.supplier, 3, self.details_layout)
        self.add_label_and_field("Состояние", self.condition, 4, self.details_layout)
        self.add_label_and_field("Серийный номер", self.serial_number, 5, self.details_layout)
        self.code_field = QLineEdit(self.code)
        self.details_layout.addWidget(QLabel("Код"), 6, 0)
        self.details_layout.addWidget(self.code_field, 6, 1)
        self.article_field = QLineEdit(self.article)
        self.details_layout.addWidget(QLabel("Артикул"), 7, 0)
        self.details_layout.addWidget(self.article_field, 7, 1)
        self.quantity_field = QLineEdit(self.quantity)
        self.details_layout.addWidget(QLabel("Количество"), 8, 0)
        self.details_layout.addWidget(self.quantity_field, 8, 1)

        # Поля для редактирования "Тип" и "Цвет"
        self.type_label = QLabel("Тип")
        self.type_combobox = QComboBox()
        self.type_combobox.addItems(["Гитара", "Бас-гитара", "Ударные", "Микрофон"])
        self.type_combobox.setCurrentText(self.equipment_type)

        self.color_label = QLabel("Цвет")
        self.color_combobox = QComboBox()
        self.color_combobox.addItems(["Красный", "Синий", "Зеленый", "Чёрный"])
        self.color_combobox.setCurrentText(self.color)

        self.details_layout.addWidget(self.type_label, 9, 0)
        self.details_layout.addWidget(self.type_combobox, 9, 1)
        self.details_layout.addWidget(self.color_label, 10, 0)
        self.details_layout.addWidget(self.color_combobox, 10, 1)

        middle_layout.addWidget(self.description, 1)
        middle_layout.addLayout(self.details_layout, 1)

        # Нижний макет: кнопки
        bottom_layout = QHBoxLayout()
        self.delete_button = QPushButton("Удалить")
        self.save_button = QPushButton("Сохранить")
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.delete_button)
        bottom_layout.addWidget(self.save_button)

        # Добавление макетов в основной макет
        main_layout.addLayout(top_layout)
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(bottom_layout)

    def add_label_and_field(self, label_text, field_text, row, layout):
        label = QLabel(label_text)
        field = QLineEdit(field_text)
        field.setAlignment(Qt.AlignLeft)
        layout.addWidget(label, row, 0)
        layout.addWidget(field, row, 1)

    def apply_styles(self):
        self.setStyleSheet(
            """
            QWidget {
                background-color: #f8f8f8;
            }

            QLabel {
                font-family: Arial, sans-serif;
                font-size: 14px;
            }

            QLineEdit {
                font-family: Arial, sans-serif;
                font-size: 16px;
                font-weight: bold;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px;
                background-color: white;
            }

            QTextEdit {
                font-family: Arial, sans-serif;
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px;
                background-color: white;
                color: black;
            }

            QComboBox {
                font-family: Arial, sans-serif;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px;
                background-color: white;
            }

            QPushButton {
                font-family: Arial, sans-serif;
                font-size: 14px;
                border: none;
                padding: 8px 16px;
                background-color: #007BFF;
                color: white;
                border-radius: 4px;
            }

            QPushButton:hover {
                background-color: #0056b3;
            }

            QPushButton:pressed {
                background-color: #004080;
            }

            QLineEdit:read-only, QTextEdit:read-only {
                background-color: #eaeaea;
            }

            #image_label {
                border: 2px solid #000;
                background-color: #d3d3d3;
                font-size: 18px;
                font-weight: bold;
                color: black;
                text-align: center;
            }
            """
        )


from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox
from PyQt5.QtGui import QFont
from styles import add_equipment_dialog


class AddEquipmentDialog(QDialog):
    def __init__(self, parent=None, name="", code="", article="", quantity="", item_type="Микрофон"):
        super().__init__(parent)
        self.setWindowTitle("Добавить оборудование")
        self.setFixedSize(400, 350)
        self.setStyleSheet(add_equipment_dialog())

        self.layout = QVBoxLayout(self)

        self.name_layout = QHBoxLayout()
        self.name_label = QLabel("Наименование:")
        self.name_label.setFont(QFont("Arial", 12))
        self.name_input = QLineEdit(name)
        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.name_input)
        self.layout.addLayout(self.name_layout)

        self.code_layout = QHBoxLayout()
        self.code_label = QLabel("Код:")
        self.code_label.setFont(QFont("Arial", 12))
        self.code_input = QLineEdit(code)
        self.code_layout.addWidget(self.code_label)
        self.code_layout.addWidget(self.code_input)
        self.layout.addLayout(self.code_layout)

        self.article_layout = QHBoxLayout()
        self.article_label = QLabel("Артикул:")
        self.article_label.setFont(QFont("Arial", 12))
        self.article_input = QLineEdit(article)
        self.article_layout.addWidget(self.article_label)
        self.article_layout.addWidget(self.article_input)
        self.layout.addLayout(self.article_layout)

        self.quantity_layout = QHBoxLayout()
        self.quantity_label = QLabel("Кол-во:")
        self.quantity_label.setFont(QFont("Arial", 12))
        self.quantity_input = QLineEdit(quantity)
        self.quantity_layout.addWidget(self.quantity_label)
        self.quantity_layout.addWidget(self.quantity_input)
        self.layout.addLayout(self.quantity_layout)

        self.type_layout = QHBoxLayout()
        self.type_label = QLabel("Тип:")
        self.type_label.setFont(QFont("Arial", 12))
        self.type_input = QComboBox()
        self.type_input.addItems(["Микрофон", "Микшер", "Колонка", "Другое"])
        self.type_input.setCurrentText(item_type)
        self.type_layout.addWidget(self.type_label)
        self.type_layout.addWidget(self.type_input)
        self.layout.addLayout(self.type_layout)

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        self.ok_button = QPushButton("Добавить")
        self.ok_button.setObjectName("ok_button")
        self.button_layout.addWidget(self.ok_button)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.setObjectName("cancel_button")
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addStretch()
        self.layout.addLayout(self.button_layout)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)


        if name or code or article or quantity or item_type != "Микрофон":
            self.setWindowTitle("Редактировать оборудование")
            self.ok_button.setText("Сохранить")
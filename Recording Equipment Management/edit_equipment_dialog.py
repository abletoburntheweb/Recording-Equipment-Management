from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QComboBox, QTextEdit, QPushButton, QVBoxLayout,
                             QHBoxLayout, QGridLayout, QRadioButton, QMessageBox, QButtonGroup)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import styles

class EditEquipmentDialog(QDialog):
    def __init__(self, name="", brand="", country="", supplier="", condition="", serial_number="",
                 code="", article="", equipment_type="Гитара", color="Красный", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактирование оборудования")
        self.setFixedSize(1280, 720)

        self.name = name
        self.brand = brand
        self.country = country
        self.supplier = supplier
        self.condition = condition
        self.serial_number = serial_number
        self.code = code
        self.article = article
        self.equipment_type = equipment_type
        self.color = color

        self.setup_ui()
        self.apply_styles()
        self.connect_buttons()

        self.set_values(name, code, article, equipment_type, condition)

    def set_values(self, name, code, article, equipment_type, condition):
        self.title.setText(name)
        self.code_field.setText(code)
        self.article_field.setText(article)
        self.type_combobox.setCurrentText(equipment_type)

        if condition == "Новое":
            self.new_condition.setChecked(True)
        elif condition == "Б/У":
            self.used_condition.setChecked(True)
        elif condition == "Поврежденное":
            self.damaged_condition.setChecked(True)
        else:
            self.new_condition.setChecked(False)
            self.used_condition.setChecked(False)
            self.damaged_condition.setChecked(False)

    def save_equipment(self):
        self.name = self.title.text()
        self.brand = self.brand_combobox.currentText()
        self.country = self.country_combobox.currentText()
        self.supplier = self.supplier_field.text()

        if self.new_condition.isChecked():
            self.condition = "Новое"
        elif self.used_condition.isChecked():
            self.condition = "Б/У"
        elif self.damaged_condition.isChecked():
            self.condition = "Поврежденное"
        else:
            self.condition = ""

        self.equipment_type = self.type_combobox.currentText()
        self.serial_number = self.serial_field.text()
        self.code = self.code_field.text()
        self.article = self.article_field.text()
        self.color = self.color_combobox.currentText()

        print(f"Сохранённое состояние: {self.condition}")
        print(f"Сохранённый тип: {self.equipment_type}")

        self.accept()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()

        self.image_label = QLabel("Изображение")
        self.image_label.setObjectName("image_label")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(300, 300)
        self.image_label.setStyleSheet("border: 1px solid #999; font-size: 18px; color: gray;")

        title_layout = QVBoxLayout()
        self.title = QLineEdit(self.name)
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        self.title.setFixedHeight(40)
        title_layout.addWidget(self.title)
        title_layout.addStretch()

        top_layout.addWidget(self.image_label, 2)
        top_layout.addLayout(title_layout, 3)

        middle_layout = QHBoxLayout()

        self.description = QTextEdit()
        self.description.setPlaceholderText("Описание")
        self.description.setAlignment(Qt.AlignCenter)
        self.description.setStyleSheet("border: 1px solid #999; font-size: 18px; color: gray;")
        self.description.setFixedHeight(300)

        self.details_layout = QGridLayout()
        self.details_layout.setHorizontalSpacing(20)

        self.details_layout.addWidget(QLabel("Код"), 0, 0)
        self.code_field = QLineEdit(self.code)
        self.details_layout.addWidget(self.code_field, 0, 1)

        self.details_layout.addWidget(QLabel("Артикул"), 0, 2)
        self.article_field = QLineEdit(self.article)
        self.details_layout.addWidget(self.article_field, 0, 3)

        self.details_layout.addWidget(QLabel("Тип"), 1, 0)
        self.type_combobox = QComboBox()
        self.type_combobox.addItems(["Гитара", "Бас-гитара", "Ударные", "Микрофон"])
        self.type_combobox.setCurrentText(self.equipment_type)
        self.details_layout.addWidget(self.type_combobox, 1, 1)

        self.details_layout.addWidget(QLabel("Бренд"), 1, 2)
        self.brand_combobox = QComboBox()
        self.brand_combobox.addItems(["Yamaha", "Gibson", "Fender", "Roland"])
        self.brand_combobox.setCurrentText(self.brand)
        self.details_layout.addWidget(self.brand_combobox, 1, 3)

        self.details_layout.addWidget(QLabel("Страна"), 2, 0)
        self.country_combobox = QComboBox()
        self.country_combobox.addItems(["США", "Япония", "Германия", "Китай"])
        self.country_combobox.setCurrentText(self.country)
        self.details_layout.addWidget(self.country_combobox, 2, 1)

        self.details_layout.addWidget(QLabel("Поставщик"), 2, 2)
        self.supplier_field = QLineEdit(self.supplier)
        self.details_layout.addWidget(self.supplier_field, 2, 3)

        self.details_layout.addWidget(QLabel("Состояние"), 3, 0, 1, 1)
        self.condition_group = QButtonGroup(self)
        self.new_condition = QRadioButton("Новое")
        self.used_condition = QRadioButton("Б/У")
        self.damaged_condition = QRadioButton("Поврежденное")

        condition_buttons_layout = QHBoxLayout()
        condition_buttons_layout.addWidget(self.new_condition)
        condition_buttons_layout.addWidget(self.used_condition)
        condition_buttons_layout.addWidget(self.damaged_condition)
        self.details_layout.addLayout(condition_buttons_layout, 3, 1, 1, 3)

        self.details_layout.addWidget(QLabel("Серийный номер"), 4, 0)
        self.serial_field = QLineEdit(self.serial_number)
        self.details_layout.addWidget(self.serial_field, 4, 1)

        self.details_layout.addWidget(QLabel("Цвет"), 4, 2)
        self.color_combobox = QComboBox()
        self.color_combobox.addItems(["Красный", "Синий", "Зеленый", "Чёрный"])
        self.details_layout.addWidget(self.color_combobox, 4, 3)

        middle_layout.addWidget(self.description, 1)
        middle_layout.addLayout(self.details_layout, 2)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.setObjectName("cancel_button")
        bottom_layout = QHBoxLayout()

        self.delete_button = QPushButton("Удалить")
        self.delete_button.setObjectName("delete_button")

        self.save_button = QPushButton("Сохранить")
        self.save_button.setObjectName("save_button")

        bottom_layout.addStretch()
        bottom_layout.addWidget(self.cancel_button)
        bottom_layout.addWidget(self.delete_button)
        bottom_layout.addWidget(self.save_button)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(bottom_layout)

    def connect_buttons(self):
        self.delete_button.clicked.connect(self.delete_equipment)
        self.save_button.clicked.connect(self.save_equipment)
        self.cancel_button.clicked.connect(self.reject)

    def delete_equipment(self):
        reply = QMessageBox.question(
            self, 'Подтверждение удаления', 'Вы уверены, что хотите удалить это оборудование?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.parent().table.removeRow(self.parent().table.currentRow())
            self.accept()

    def apply_styles(self):
        self.setStyleSheet(styles.edit_equipment_dialog())

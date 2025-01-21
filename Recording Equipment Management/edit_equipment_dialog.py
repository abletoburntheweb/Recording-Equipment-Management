import os

from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QComboBox, QTextEdit, QPushButton, QVBoxLayout,
                             QHBoxLayout, QGridLayout, QRadioButton, QMessageBox, QButtonGroup)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import styles


class EditEquipmentDialog(QDialog):
    def __init__(self, name="", brand="", country="", supplier="", condition="", serial_number="",
                 code="", equipment_type="Гитара", color="Красный", parent=None):
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
        self.equipment_type = equipment_type
        self.color = color

        self.setup_ui()
        self.apply_styles()
        self.connect_buttons()

        self.set_values(name, code, serial_number, equipment_type, condition)

    def set_values(self, name, code, serial_number, equipment_type, condition):
        self.title.setText(name)
        self.code_field.setText(code)
        self.serial_field.setText(serial_number)
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
        is_valid = True

        # Проверяем обязательные поля
        if not self.title.text().strip():
            self.title.setPlaceholderText("Поле не может быть пустым")
            self.title.setStyleSheet("border: 1px solid red;")
            is_valid = False
        else:
            self.title.setStyleSheet("")

        if not self.code_field.text().strip():
            self.code_field.setPlaceholderText("Поле не может быть пустым")
            self.code_field.setStyleSheet("border: 1px solid red;")
            is_valid = False
        else:
            self.code_field.setStyleSheet("")

        if not self.serial_field.text().strip():
            self.serial_field.setPlaceholderText("Поле не может быть пустым")
            self.serial_field.setStyleSheet("border: 1px solid red;")
            is_valid = False
        else:
            self.serial_field.setStyleSheet("")

        if not self.type_combobox.currentText().strip():
            self.type_combobox.setStyleSheet("border: 1px solid red;")
            is_valid = False
        else:
            self.type_combobox.setStyleSheet("")

        if is_valid:
            # Присваиваем значения
            self.name = self.title.text().strip()  # Название
            self.code = self.code_field.text().strip()  # Код оборудования
            self.serial_number = self.serial_field.text().strip()  # Серийный номер
            self.equipment_type = self.type_combobox.currentText().strip()  # Тип оборудования
            self.color = self.color_combobox.currentText().strip()  # Цвет оборудования
            self.brand = self.brand_combobox.currentText().strip()  # Бренд оборудования
            self.supplier = self.supplier_field.currentText().strip()  # Поставщик оборудования

            # Определяем состояние
            if self.new_condition.isChecked():
                self.condition = "Новое"
            elif self.used_condition.isChecked():
                self.condition = "Б/У"
            elif self.damaged_condition.isChecked():
                self.condition = "Поврежденное"
            else:
                self.condition = ""

            print(f"Сохранённое состояние: {self.condition}")
            print(f"Сохранённый тип: {self.equipment_type}")
            print(f"Сохранённый код: {self.code}")
            print(f"Сохранённый поставщик: {self.supplier}")

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

        self.details_layout.addWidget(QLabel("Серийный номер"), 0, 2)
        self.serial_field = QLineEdit(self.serial_number)
        self.details_layout.addWidget(self.serial_field, 0, 3)

        self.details_layout.addWidget(QLabel("Тип"), 1, 0)
        self.type_combobox = QComboBox()
        self.details_layout.addWidget(self.type_combobox, 1, 1)

        self.details_layout.addWidget(QLabel("Цвет"), 1, 2)
        self.color_combobox = QComboBox()
        self.details_layout.addWidget(self.color_combobox, 1, 3)

        self.details_layout.addWidget(QLabel("Бренд"), 2, 0)
        self.brand_combobox = QComboBox()
        self.details_layout.addWidget(self.brand_combobox, 2, 1)

        self.details_layout.addWidget(QLabel("Страна"), 2, 2)
        self.country_combobox = QComboBox()
        self.details_layout.addWidget(self.country_combobox, 2, 3)

        self.details_layout.addWidget(QLabel("Поставщик"), 3, 0)
        self.supplier_field = QComboBox()
        self.details_layout.addWidget(self.supplier_field, 3, 1)

        self.details_layout.addWidget(QLabel("Состояние"), 3, 2)
        self.condition_group = QButtonGroup(self)
        self.new_condition = QRadioButton("Новое")
        self.used_condition = QRadioButton("Б/У")
        self.damaged_condition = QRadioButton("Поврежденное")

        condition_buttons_layout = QHBoxLayout()
        condition_buttons_layout.addWidget(self.new_condition)
        condition_buttons_layout.addWidget(self.used_condition)
        condition_buttons_layout.addWidget(self.damaged_condition)
        self.details_layout.addLayout(condition_buttons_layout, 3, 3)

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

        self.load_data_from_db()

    def load_data_from_db(self):
        try:
            connection = self.parent().connection
            cursor = connection.cursor()


            cursor.execute("SELECT type_name FROM type")
            self.type_combobox.addItems([row[0] for row in cursor.fetchall()])


            cursor.execute("SELECT color_name FROM color")
            self.color_combobox.addItems([row[0] for row in cursor.fetchall()])


            cursor.execute("SELECT brand_name FROM brand")
            self.brand_combobox.addItems([row[0] for row in cursor.fetchall()])


            if self.brand:
                self.brand_combobox.setCurrentText(self.brand)


            cursor.execute("SELECT supplier_name FROM supplier")
            self.supplier_field.addItems([row[0] for row in cursor.fetchall()])


            if self.supplier:
                self.supplier_field.setCurrentText(self.supplier)


            cursor.execute("SELECT image_path FROM equipment WHERE serial_number = %s", (self.serial_number,))
            result = cursor.fetchone()
            if result:
                image_path = os.path.join("images", result[0])
                if os.path.exists(image_path):
                    pixmap = QPixmap(image_path)
                    self.image_label.setPixmap(
                        pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    print(f"Файл изображения не найден: {image_path}")
            else:
                print("Изображение не указано в базе данных.")

            cursor.close()
        except Exception as e:
            print(f"Ошибка загрузки данных из базы: {e}")

    def connect_buttons(self):
        self.delete_button.clicked.connect(self.delete_equipment)
        self.save_button.clicked.connect(self.save_equipment)
        self.cancel_button.clicked.connect(self.reject)

    def delete_equipment(self):
        reply = QMessageBox(self)
        reply.setWindowTitle("Подтверждение удаления")
        reply.setText("Вы уверены, что хотите удалить это оборудование?")
        reply.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply.button(QMessageBox.Yes).setText("Да")
        reply.button(QMessageBox.No).setText("Нет")
        reply.setDefaultButton(QMessageBox.No)

        if reply.exec() == QMessageBox.Yes:
            try:
                connection = self.parent().connection
                cursor = connection.cursor()

                cursor.execute("DELETE FROM equipment WHERE serial_number = %s", (self.serial_number,))
                connection.commit()
                cursor.close()

                print(f"Оборудование с серийным номером {self.serial_number} успешно удалено!")
                QMessageBox.information(self, "Удаление", "Оборудование успешно удалено.")
                self.accept()
                self.load_data_from_db()

            except Exception as e:
                print(f"Ошибка при удалении оборудования: {e}")
                QMessageBox.critical(self, "Ошибка",
                                     "Не удалось удалить оборудование. Проверьте соединение с базой данных.")

    def apply_styles(self):
        self.setStyleSheet(styles.edit_equipment_dialog())

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QComboBox, QFileDialog, QGroupBox, QRadioButton, QButtonGroup, QMessageBox
)
import psycopg2
import shutil
import os
from config import DB_CONFIG
from styles import add_equipment_dialog


class AddEquipmentDialog(QDialog):
    def __init__(self, parent=None, name="", code="", serial_number="", item_type="",
                 image_path="", brand="", country="", supplier="", status="Новое", color=""):
        super().__init__(parent)
        self.setWindowTitle("Добавить оборудование")
        self.setFixedSize(700, 700)
        self.setWindowIcon(QIcon("equipment.ico"))

        self.setStyleSheet(add_equipment_dialog())
        self.layout = QVBoxLayout(self)

        main_group = QGroupBox("Основные параметры")
        main_layout = QVBoxLayout()
        main_group.setLayout(main_layout)

        name_layout = QHBoxLayout()
        self.name_label = QLabel("Наименование:")
        self.name_input = QLineEdit(name)
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_input)
        main_layout.addLayout(name_layout)

        code_serial_layout = QHBoxLayout()
        self.code_label = QLabel("Код:")
        self.code_input = QLineEdit(code)
        code_serial_layout.addWidget(self.code_label)
        code_serial_layout.addWidget(self.code_input)

        self.serial_number_label = QLabel("Серийный номер:")
        self.serial_number_input = QLineEdit(serial_number)
        code_serial_layout.addWidget(self.serial_number_label)
        code_serial_layout.addWidget(self.serial_number_input)
        main_layout.addLayout(code_serial_layout)

        quantity_type_layout = QHBoxLayout()
        self.type_label = QLabel("Тип:")
        self.type_input = QComboBox()
        self.type_input.setEditable(True)
        self.type_input.addItems(self.fetch_from_db("SELECT type_name FROM type"))
        self.type_input.setCurrentText(item_type)
        quantity_type_layout.addWidget(self.type_label)
        quantity_type_layout.addWidget(self.type_input)

        self.status_label = QLabel("Состояние:")
        self.status_group = QButtonGroup(self)
        self.new_status = QRadioButton("Новое")
        self.used_status = QRadioButton("Б/У")
        self.damaged_status = QRadioButton("Поврежденное")

        if status == "Новое":
            self.new_status.setChecked(True)
        elif status == "Б/У":
            self.used_status.setChecked(True)
        elif status == "Поврежденное":
            self.damaged_status.setChecked(True)

        self.status_group.addButton(self.new_status)
        self.status_group.addButton(self.used_status)
        self.status_group.addButton(self.damaged_status)

        status_buttons_layout = QVBoxLayout()
        status_buttons_layout.addWidget(self.new_status)
        status_buttons_layout.addWidget(self.used_status)
        status_buttons_layout.addWidget(self.damaged_status)

        quantity_type_layout.addWidget(self.status_label)
        quantity_type_layout.addLayout(status_buttons_layout)
        main_layout.addLayout(quantity_type_layout)
        self.layout.addWidget(main_group)

        additional_group = QGroupBox("Дополнительные параметры")
        additional_layout = QVBoxLayout()
        additional_group.setLayout(additional_layout)

        image_layout = QHBoxLayout()
        self.image_label = QLabel("Изображение:")
        self.image_input = QLineEdit(image_path)
        self.image_input.setReadOnly(True)
        self.image_button = QPushButton("Выбрать")
        self.image_button.clicked.connect(self.select_image)
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(self.image_input)
        image_layout.addWidget(self.image_button)
        additional_layout.addLayout(image_layout)

        brand_country_layout = QHBoxLayout()
        self.brand_label = QLabel("Бренд:")
        self.brand_input = QComboBox()
        self.brand_input.setEditable(True)
        self.brand_input.addItems(self.fetch_from_db("SELECT brand_name FROM brand"))
        self.brand_input.setCurrentText(brand)
        self.brand_input.currentTextChanged.connect(self.update_country_field)

        self.country_label = QLabel("Страна:")
        self.country_input = QComboBox()
        self.country_input.setEditable(True)
        self.update_country_field(self.brand_input.currentText())

        brand_country_layout.addWidget(self.brand_label)
        brand_country_layout.addWidget(self.brand_input)
        brand_country_layout.addWidget(self.country_label)
        brand_country_layout.addWidget(self.country_input)
        additional_layout.addLayout(brand_country_layout)

        supplier_color_layout = QHBoxLayout()
        self.supplier_label = QLabel("Поставщик:")
        self.supplier_input = QComboBox()
        self.supplier_input.setEditable(True)
        self.supplier_input.addItems(self.fetch_from_db("SELECT supplier_name FROM supplier"))
        self.supplier_input.setCurrentText(supplier)
        supplier_color_layout.addWidget(self.supplier_label)
        supplier_color_layout.addWidget(self.supplier_input)

        self.color_label = QLabel("Цвет:")
        self.color_input = QComboBox()
        self.color_input.setEditable(True)
        self.color_input.addItems(self.fetch_from_db("SELECT color_name FROM color"))
        self.color_input.setCurrentText(color)
        supplier_color_layout.addWidget(self.color_label)
        supplier_color_layout.addWidget(self.color_input)
        additional_layout.addLayout(supplier_color_layout)

        self.layout.addWidget(additional_group)

        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.setObjectName("cancel_button")
        self.ok_button = QPushButton("Добавить")
        self.ok_button.setObjectName("ok_button")

        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        self.layout.addLayout(button_layout)

        self.ok_button.clicked.connect(self.save_equipment)
        self.cancel_button.clicked.connect(self.reject)

        if any([name, code, serial_number, item_type, image_path, brand, country, supplier, status, color]):
            self.setWindowTitle("Редактировать оборудование")
            self.ok_button.setText("Сохранить")

    def get_status(self):
        if self.new_status.isChecked():
            return "Новое"
        elif self.used_status.isChecked():
            return "Б/У"
        elif self.damaged_status.isChecked():
            return "Поврежденное"
        return None

    def fetch_from_db(self, query):
        conn = None
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            with conn.cursor() as cur:
                cur.execute(query)
                return [row[0] for row in cur.fetchall()]
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def select_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "",
                                                   "Images (*.png *.xpm *.jpg *.jpeg *.bmp);;All Files (*)",
                                                   options=options)
        if file_path:
            images_dir = os.path.join(os.getcwd(), "images")
            if not os.path.exists(images_dir):
                os.makedirs(images_dir)

            file_name = os.path.basename(file_path)
            destination_path = os.path.join(images_dir, file_name)

            if os.path.abspath(file_path) == os.path.abspath(destination_path):
                self.image_input.setText(destination_path)
                print(f"Файл уже находится в целевой директории: {destination_path}")
                return

            try:
                shutil.copy(file_path, destination_path)
                self.image_input.setText(destination_path)
                print(f"Файл скопирован в {destination_path}")
            except Exception as e:
                print(f"Ошибка при копировании файла: {e}")

    def save_equipment(self):
        is_valid = True

        if not self.name_input.text().strip():
            self.name_input.setPlaceholderText("Поле не может быть пустым")
            self.name_input.setStyleSheet("border: 1px solid red;")
            is_valid = False
        else:
            self.name_input.setStyleSheet("")

        if not self.code_input.text().strip():
            self.code_input.setPlaceholderText("Поле не может быть пустым")
            self.code_input.setStyleSheet("border: 1px solid red;")
            is_valid = False
        else:
            self.code_input.setStyleSheet("")

        serial_number = self.serial_number_input.text().strip()
        if not serial_number:
            self.serial_number_input.setPlaceholderText("Поле не может быть пустым")
            self.serial_number_input.setStyleSheet("border: 1px solid red;")
            is_valid = False
        else:
            if self.is_serial_number_exists(serial_number):
                QMessageBox.warning(self, "Ошибка", f"Серийный номер {serial_number} уже существует.")
                self.serial_number_input.setStyleSheet("border: 1px solid red;")
                is_valid = False
            else:
                self.serial_number_input.setStyleSheet("")

        if not self.type_input.currentText().strip():
            self.type_input.setStyleSheet("border: 1px solid red;")
            is_valid = False
        else:
            self.type_input.setStyleSheet("")

        if not self.get_status():
            self.new_status.setStyleSheet("color: red;")
            self.used_status.setStyleSheet("color: red;")
            self.damaged_status.setStyleSheet("color: red;")
            is_valid = False
        else:
            self.new_status.setStyleSheet("")
            self.used_status.setStyleSheet("")
            self.damaged_status.setStyleSheet("")

        image_path = self.image_input.text().strip()
        if image_path:
            if not os.path.exists(image_path):
                self.image_input.setStyleSheet("border: 1px solid red;")
                print("Файл изображения не существует.")
                is_valid = False
            else:
                valid_extensions = (".png", ".jpg", ".jpeg", ".bmp")
                if not image_path.lower().endswith(valid_extensions):
                    self.image_input.setStyleSheet("border: 1px solid red;")
                    print("Файл изображения имеет недопустимый формат.")
                    is_valid = False
                else:
                    self.image_input.setStyleSheet("")
        else:
            self.image_input.setStyleSheet("")

        if not is_valid:
            print("Обязательные поля не заполнены. Добавление не выполнено.")
            return

        name = self.name_input.text().strip()
        code = self.code_input.text().strip()
        serial_number = self.serial_number_input.text().strip()
        item_type = self.type_input.currentText().strip()
        status = self.get_status()
        brand = self.brand_input.currentText().strip()
        country = self.country_input.currentText().strip()
        supplier = self.supplier_input.currentText().strip()
        color = self.color_input.currentText().strip()

        print(
            f"Передаём данные в save_to_db: Name: {name}, Code: {code}, Serial: {serial_number}, Type: {item_type}, Status: {status}, Brand: {brand}, Country: {country}, Supplier: {supplier}, Color: {color}, Image Path: {image_path}"
        )

        self.parent().save_to_db(
            name=name,
            code=code,
            serial_number=serial_number,
            item_type=item_type,
            status=status,
            brand=brand,
            country=country,
            supplier=supplier,
            color=color,
            image_path=image_path
        )

        self.accept()

    def add_country_to_brand(self, country):
        query = "INSERT INTO brand (country) VALUES (%s) ON CONFLICT DO NOTHING"
        conn = None
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            with conn.cursor() as cur:
                cur.execute(query, (country,))
                conn.commit()
        except Exception as e:
            print(f"Ошибка добавления страны в базу данных: {e}")
        finally:
            if conn:
                conn.close()

    def is_in_db(self, table, column, value):
        query = f"SELECT COUNT(*) FROM {table} WHERE {column} = %s"
        conn = None
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            with conn.cursor() as cur:
                cur.execute(query, (value,))
                return cur.fetchone()[0] > 0
        except Exception as e:
            print(f"Ошибка проверки в базе данных: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def update_country_field(self, brand_name):
        query = "SELECT country FROM brand WHERE brand_name = %s"
        conn = None
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            with conn.cursor() as cur:
                cur.execute(query, (brand_name,))
                result = cur.fetchone()
                if result:
                    self.country_input.clear()
                    self.country_input.addItem(result[0])
        except Exception as e:
            print(f"Ошибка обновления поля 'Страна': {e}")
        finally:
            if conn:
                conn.close()

    def add_to_db(self, table, column, value):
        query = f"INSERT INTO {table} ({column}) VALUES (%s)"
        conn = None
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            with conn.cursor() as cur:
                cur.execute(query, (value,))
                conn.commit()
        except Exception as e:
            print(f"Ошибка добавления в базу данных: {e}")
        finally:
            if conn:
                conn.close()

    def is_serial_number_exists(self, serial_number):
        query = "SELECT COUNT(*) FROM equipment WHERE serial_number = %s"
        conn = None
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            with conn.cursor() as cur:
                cur.execute(query, (serial_number,))
                count = cur.fetchone()[0]
                print(f"Количество записей с этим серийным номером: {count}")
                return count > 0
        except Exception as e:
            print(f"Ошибка проверки серийного номера: {e}")
            return False
        finally:
            if conn:
                conn.close()
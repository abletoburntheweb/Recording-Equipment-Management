from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QFileDialog, QGroupBox, QRadioButton, QButtonGroup
from PyQt5.QtGui import QFont
from styles import add_equipment_dialog


class AddEquipmentDialog(QDialog):
    def __init__(self, parent=None, name="", code="", article="", item_type="Микрофон",
                 image_path="", brand="Brand A", country="USA", supplier="", status="Новое", serial_number="", color="Red"):
        super().__init__(parent)
        self.setWindowTitle("Добавить оборудование")
        self.setFixedSize(700, 700)
        self.setStyleSheet(add_equipment_dialog())

        self.layout = QVBoxLayout(self)

        main_group = QGroupBox("Основные параметры")
        main_layout = QVBoxLayout()
        main_group.setLayout(main_layout)

        name_layout = QHBoxLayout()
        self.name_label = QLabel("Наименование:")
        self.name_label.setFont(QFont("Arial", 14))
        self.name_input = QLineEdit(name)
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_input)
        main_layout.addLayout(name_layout)

        code_article_layout = QHBoxLayout()
        self.code_label = QLabel("Код:")
        self.code_label.setFont(QFont("Arial", 14))
        self.code_input = QLineEdit(code)
        code_article_layout.addWidget(self.code_label)
        code_article_layout.addWidget(self.code_input)

        self.article_label = QLabel("Артикул:")
        self.article_label.setFont(QFont("Arial", 14))
        self.article_input = QLineEdit(article)
        code_article_layout.addWidget(self.article_label)
        code_article_layout.addWidget(self.article_input)
        main_layout.addLayout(code_article_layout)

        quantity_type_layout = QHBoxLayout()
        self.type_label = QLabel("Тип:")
        self.type_label.setFont(QFont("Arial", 14))
        self.type_input = QComboBox()
        self.type_input.addItems(["Микрофон", "Микшер", "Колонка", "Другое"])
        self.type_input.setCurrentText(item_type)
        quantity_type_layout.addWidget(self.type_label)
        quantity_type_layout.addWidget(self.type_input)

        self.status_label = QLabel("Состояние:")
        self.status_label.setFont(QFont("Arial", 14))

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
        self.image_label.setFont(QFont("Arial", 14))
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
        self.brand_label.setFont(QFont("Arial", 14))
        self.brand_input = QComboBox()
        self.brand_input.addItems(["Brand A", "Brand B", "Brand C"])
        self.brand_input.setCurrentText(brand)
        brand_country_layout.addWidget(self.brand_label)
        brand_country_layout.addWidget(self.brand_input)

        self.country_label = QLabel("Страна:")
        self.country_label.setFont(QFont("Arial", 14))
        self.country_input = QComboBox()
        self.country_input.addItems(["США", "Германия", "Япония", "Китай"])
        self.country_input.setCurrentText(country)
        brand_country_layout.addWidget(self.country_label)
        brand_country_layout.addWidget(self.country_input)
        additional_layout.addLayout(brand_country_layout)

        supplier_layout = QHBoxLayout()
        self.supplier_label = QLabel("Поставщик:")
        self.supplier_label.setFont(QFont("Arial", 14))
        self.supplier_input = QLineEdit(supplier)
        supplier_layout.addWidget(self.supplier_label)
        supplier_layout.addWidget(self.supplier_input)
        additional_layout.addLayout(supplier_layout)

        serial_color_layout = QHBoxLayout()
        self.serial_number_label = QLabel("Серийный номер:")
        self.serial_number_label.setFont(QFont("Arial", 14))
        self.serial_number_input = QLineEdit(serial_number)
        serial_color_layout.addWidget(self.serial_number_label)
        serial_color_layout.addWidget(self.serial_number_input)

        self.color_label = QLabel("Цвет:")
        self.color_label.setFont(QFont("Arial", 14))
        self.color_input = QComboBox()
        self.color_input.addItems(["Красный", "Синий", "Зеленый", "Желтый"])
        self.color_input.setCurrentText(color)
        serial_color_layout.addWidget(self.color_label)
        serial_color_layout.addWidget(self.color_input)
        additional_layout.addLayout(serial_color_layout)

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

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        if any([name, code, article, item_type != "Микрофон", image_path, brand, country, supplier, status, serial_number, color]):
            self.setWindowTitle("Редактировать оборудование")
            self.ok_button.setText("Сохранить")

    def select_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.xpm *.jpg *.jpeg);;All Files (*)", options=options)
        if file_path:
            self.image_input.setText(file_path)

    def get_status(self):
        selected_button = self.status_group.checkedButton()
        return selected_button.text() if selected_button else ""

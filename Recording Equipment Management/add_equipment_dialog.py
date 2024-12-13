from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QFileDialog, QGroupBox, QFormLayout
from PyQt5.QtGui import QFont
from styles import add_equipment_dialog

class AddEquipmentDialog(QDialog):
    def __init__(self, parent=None, name="", code="", article="", quantity="", item_type="Микрофон",
                 image_path="", brand="", country="", supplier="", status="", serial_number="", color=""):
        super().__init__(parent)
        self.setWindowTitle("Добавить оборудование")
        self.setFixedSize(700, 700)  # Увеличиваем размер окна
        self.setStyleSheet(add_equipment_dialog())

        self.layout = QVBoxLayout(self)

        # Основные параметры
        main_group = QGroupBox("Основные параметры")
        main_layout = QVBoxLayout()
        main_group.setLayout(main_layout)

        # Наименование
        name_layout = QHBoxLayout()
        self.name_label = QLabel("Наименование:")
        self.name_label.setFont(QFont("Arial", 12))
        self.name_input = QLineEdit(name)
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_input)
        main_layout.addLayout(name_layout)

        # Код и Артикул
        code_article_layout = QHBoxLayout()
        self.code_label = QLabel("Код:")
        self.code_label.setFont(QFont("Arial", 12))
        self.code_input = QLineEdit(code)
        code_article_layout.addWidget(self.code_label)
        code_article_layout.addWidget(self.code_input)

        self.article_label = QLabel("Артикул:")
        self.article_label.setFont(QFont("Arial", 12))
        self.article_input = QLineEdit(article)
        code_article_layout.addWidget(self.article_label)
        code_article_layout.addWidget(self.article_input)
        main_layout.addLayout(code_article_layout)

        # Кол-во и Тип
        quantity_type_layout = QHBoxLayout()
        self.quantity_label = QLabel("Кол-во:")
        self.quantity_label.setFont(QFont("Arial", 12))
        self.quantity_input = QLineEdit(quantity)
        quantity_type_layout.addWidget(self.quantity_label)
        quantity_type_layout.addWidget(self.quantity_input)

        self.type_label = QLabel("Тип:")
        self.type_label.setFont(QFont("Arial", 12))
        self.type_input = QComboBox()
        self.type_input.addItems(["Микрофон", "Микшер", "Колонка", "Другое"])
        self.type_input.setCurrentText(item_type)
        quantity_type_layout.addWidget(self.type_label)
        quantity_type_layout.addWidget(self.type_input)
        main_layout.addLayout(quantity_type_layout)

        self.layout.addWidget(main_group)

        # Дополнительные параметры
        additional_group = QGroupBox("Дополнительные параметры")
        additional_layout = QVBoxLayout()
        additional_group.setLayout(additional_layout)

        # Изображение
        image_layout = QHBoxLayout()
        self.image_label = QLabel("Изображение:")
        self.image_label.setFont(QFont("Arial", 12))
        self.image_input = QLineEdit(image_path)
        self.image_input.setReadOnly(True)
        self.image_button = QPushButton("Выбрать")
        self.image_button.clicked.connect(self.select_image)
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(self.image_input)
        image_layout.addWidget(self.image_button)
        additional_layout.addLayout(image_layout)

        # Бренд и Страна
        brand_country_layout = QHBoxLayout()
        self.brand_label = QLabel("Бренд:")
        self.brand_label.setFont(QFont("Arial", 12))
        self.brand_input = QLineEdit(brand)
        brand_country_layout.addWidget(self.brand_label)
        brand_country_layout.addWidget(self.brand_input)

        self.country_label = QLabel("Страна:")
        self.country_label.setFont(QFont("Arial", 12))
        self.country_input = QLineEdit(country)
        brand_country_layout.addWidget(self.country_label)
        brand_country_layout.addWidget(self.country_input)
        additional_layout.addLayout(brand_country_layout)

        # Поставщик и Состояние
        supplier_status_layout = QHBoxLayout()
        self.supplier_label = QLabel("Поставщик:")
        self.supplier_label.setFont(QFont("Arial", 12))
        self.supplier_input = QLineEdit(supplier)
        supplier_status_layout.addWidget(self.supplier_label)
        supplier_status_layout.addWidget(self.supplier_input)

        self.status_label = QLabel("Состояние:")
        self.status_label.setFont(QFont("Arial", 12))
        self.status_input = QLineEdit(status)
        supplier_status_layout.addWidget(self.status_label)
        supplier_status_layout.addWidget(self.status_input)
        additional_layout.addLayout(supplier_status_layout)

        # Серийный номер и Цвет
        serial_color_layout = QHBoxLayout()
        self.serial_number_label = QLabel("Серийный номер:")
        self.serial_number_label.setFont(QFont("Arial", 12))
        self.serial_number_input = QLineEdit(serial_number)
        serial_color_layout.addWidget(self.serial_number_label)
        serial_color_layout.addWidget(self.serial_number_input)

        self.color_label = QLabel("Цвет:")
        self.color_label.setFont(QFont("Arial", 12))
        self.color_input = QLineEdit(color)
        serial_color_layout.addWidget(self.color_label)
        serial_color_layout.addWidget(self.color_input)
        additional_layout.addLayout(serial_color_layout)

        self.layout.addWidget(additional_group)

        # Кнопки
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

        # Изменяем текст кнопки, если переданы начальные значения
        if name or code or article or quantity or item_type != "Микрофон" or image_path or brand or country or supplier or status or serial_number or color:
            self.setWindowTitle("Редактировать оборудование")
            self.ok_button.setText("Сохранить")

    def select_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.xpm *.jpg *.jpeg);;All Files (*)", options=options)
        if file_path:
            self.image_input.setText(file_path)
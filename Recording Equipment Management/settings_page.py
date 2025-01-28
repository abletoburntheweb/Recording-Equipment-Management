from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from styles import table_widget, combo_box, add_button, back_button
from add_item_dialog import AddItemDialog  # Импортируем диалоговое окно


class SettingsPage(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки списков")
        self.setGeometry(100, 100, 1280, 720)

        self.layout = QVBoxLayout(self)

        title_label = QLabel("Настройки списков")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 32, QFont.Bold))
        self.layout.addWidget(title_label)

        combo_layout = QHBoxLayout()
        combo_label = QLabel("Выберите список:")
        combo_label.setFont(QFont("Arial", 24))
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Поставщик", "Бренд", "Цвет", "Тип"])
        self.combo_box.currentIndexChanged.connect(self.load_items)
        self.combo_box.setStyleSheet(combo_box())
        combo_layout.addWidget(combo_label)
        combo_layout.addWidget(self.combo_box)
        self.layout.addLayout(combo_layout)

        self.list_widget = QTableWidget()
        self.list_widget.setColumnCount(2)
        self.list_widget.setHorizontalHeaderLabels(["ID", "Значение"])
        self.list_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.list_widget.setStyleSheet(table_widget())
        self.list_widget.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.list_widget)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить")
        self.add_button.setStyleSheet(add_button())
        self.add_button.clicked.connect(self.add_item)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.setStyleSheet(back_button())
        self.delete_button.clicked.connect(self.delete_item)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        self.layout.addLayout(button_layout)

        self.connection = parent.connection
        self.load_items()

    def load_items(self):
        if not self.connection:
            QMessageBox.critical(self, "Ошибка", "Нет соединения с базой данных.")
            return

        table_mapping = {
            "Поставщик": ("supplier", "supplier_id", "supplier_name"),
            "Бренд": ("brand", "brand_id", "brand_name", "country"),
            "Цвет": ("color", "color_id", "color_name"),
            "Тип": ("type", "type_id", "type_name"),
        }

        selected_list = self.combo_box.currentText()
        mapping = table_mapping[selected_list]

        try:
            cursor = self.connection.cursor()

            if selected_list == "Бренд":
                cursor.execute(
                    """
                    SELECT brand_id, brand_name, country
                    FROM brand
                    ORDER BY brand_id
                    """
                )
                rows = cursor.fetchall()

                self.list_widget.setColumnCount(3)
                self.list_widget.setHorizontalHeaderLabels(["ID", "Бренд", "Страна"])
            else:
                table, id_column, name_column = mapping[:3]
                cursor.execute(f"SELECT {id_column}, {name_column} FROM {table} ORDER BY {id_column}")
                rows = cursor.fetchall()

                self.list_widget.setColumnCount(2)
                self.list_widget.setHorizontalHeaderLabels(["ID", "Значение"])

            cursor.close()

            self.list_widget.setRowCount(0)
            for row in rows:
                row_count = self.list_widget.rowCount()
                self.list_widget.insertRow(row_count)
                for col, value in enumerate(row):
                    self.list_widget.setItem(row_count, col, QTableWidgetItem(str(value)))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки данных: {e}")

    def add_item(self):
        selected_list = self.combo_box.currentText()
        table_mapping = {
            "Поставщик": "supplier",
            "Бренд": "brand",
            "Цвет": "color",
            "Тип": "type",
        }
        table = table_mapping[selected_list]

        dialog = AddItemDialog(table_name=table, parent=self)
        if dialog.exec() == QDialog.Accepted:
            item_name, country = dialog.get_inputs()
            if not item_name:
                QMessageBox.warning(self, "Ошибка", "Поле с именем не может быть пустым.")
                return

            try:
                cursor = self.connection.cursor()

                if table == "brand":
                    if not country:
                        QMessageBox.warning(self, "Ошибка", "Поле со страной не может быть пустым.")
                        return
                    cursor.execute(
                        "INSERT INTO brand (brand_name, country) VALUES (%s, %s)",
                        (item_name, country)
                    )
                else:
                    cursor.execute(
                        f"INSERT INTO {table} ({table}_name) VALUES (%s)",
                        (item_name,)
                    )

                self.connection.commit()
                cursor.close()
                self.load_items()
                QMessageBox.information(self, "Успех", "Элемент добавлен.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка добавления элемента: {e}")

    def delete_item(self):
        selected_row = self.list_widget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите элемент для удаления.")
            return

        selected_list = self.combo_box.currentText()
        table_mapping = {
            "Поставщик": "supplier",
            "Бренд": "brand",
            "Цвет": "color",
            "Тип": "type",
        }
        table = table_mapping[selected_list]

        item_id = self.list_widget.item(selected_row, 0).text()
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"DELETE FROM {table} WHERE {table}_id = %s", (item_id,))
            self.connection.commit()
            cursor.close()
            self.load_items()
            QMessageBox.information(self, "Успех", "Элемент удален.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка удаления элемента: {e}")

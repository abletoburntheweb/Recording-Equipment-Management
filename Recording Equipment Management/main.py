import sys
import psycopg2
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel, \
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QLineEdit
from PyQt5.QtCore import Qt
from add_equipment_dialog import AddEquipmentDialog
from edit_equipment_dialog import EditEquipmentDialog
from styles import main_window, add_button, table_widget, search_box, search_button
from config import DB_CONFIG


class Studio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Учет оборудования звукозаписи")
        self.setGeometry(100, 100, 1280, 720)
        self.setStyleSheet(main_window())

        self.connection = self.get_db_connection()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        header_layout = QHBoxLayout()
        self.header_label = QLabel("Студия: Студия 1")
        self.header_label.setStyleSheet("QLabel { font-size: 20px; color: #333; }")
        header_layout.addWidget(self.header_label)

        self.add_button = QPushButton("Добавить оборудование")
        self.add_button.setStyleSheet(add_button())
        self.add_button.clicked.connect(self.open_add_equipment_dialog)
        header_layout.addWidget(self.add_button)

        header_layout.addStretch()
        layout.addLayout(header_layout)

        search_layout = QHBoxLayout()
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Поиск...")
        self.search_field.setStyleSheet(search_box())
        search_layout.addWidget(self.search_field)

        self.search_button = QPushButton("Поиск")
        self.search_button.setStyleSheet(add_button())
        self.search_button.clicked.connect(self.search_table)
        search_layout.addWidget(self.search_button)

        layout.addLayout(search_layout)


        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Наименование", "Код", "Серийный номер", "Тип", "Состояние"])
        self.table.setColumnHidden(0, True)
        self.table.setStyleSheet(table_widget())
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.doubleClicked.connect(self.edit_equipment)

        layout.addWidget(self.table)

        self.load_data_from_db()

    def search_table(self):
        query = self.search_field.text().lower()
        for row in range(self.table.rowCount()):
            match = False
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item and query in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)
    def get_db_connection(self):
        try:
            connection = psycopg2.connect(**DB_CONFIG)
            return connection
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
            return None

    def load_data_from_db(self):
        if not self.connection:
            return

        try:
            cursor = self.connection.cursor()
            query = """
            SELECT 
                e.equipment_id,           -- ID оборудования
                e.name AS equipment_name, -- Наименование
                e.code,                   -- Код
                e.serial_number,          -- Серийный номер
                t.type_name,              -- Тип
                e.condition,              -- Состояние
                c.color_name,             -- Цвет
                s.supplier_name           -- Поставщик
            FROM equipment e
            LEFT JOIN type t ON e.type_id = t.type_id
            LEFT JOIN color c ON e.color_id = c.color_id
            LEFT JOIN supplier s ON e.supplier_id = s.supplier_id;
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            self.table.setRowCount(0)

            for row in rows:
                row_count = self.table.rowCount()
                self.table.insertRow(row_count)

                self.table.setItem(row_count, 0, QTableWidgetItem(str(row[0])))
                self.table.setItem(row_count, 1, QTableWidgetItem(row[1]))
                self.table.setItem(row_count, 2, QTableWidgetItem(row[2] or "—"))
                self.table.setItem(row_count, 3, QTableWidgetItem(row[3] or "—"))
                self.table.setItem(row_count, 4, QTableWidgetItem(row[4] or "—"))
                self.table.setItem(row_count, 5, QTableWidgetItem(row[5] or "—"))
                self.table.setItem(row_count, 6, QTableWidgetItem(row[6] or "—"))
                self.table.setItem(row_count, 7, QTableWidgetItem(row[7] or "—"))

            cursor.close()
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")

    def open_add_equipment_dialog(self):
        dialog = AddEquipmentDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            name = dialog.name_input.text()
            code = dialog.code_input.text()
            serial_number = dialog.serial_number_input.text()
            item_type = dialog.type_input.currentText()
            status = dialog.get_status()


            row_count = self.table.rowCount()
            self.table.insertRow(row_count)
            self.table.setItem(row_count, 1, QTableWidgetItem(name))
            self.table.setItem(row_count, 2, QTableWidgetItem(code))
            self.table.setItem(row_count, 3, QTableWidgetItem(serial_number))
            self.table.setItem(row_count, 4, QTableWidgetItem(item_type))
            self.table.setItem(row_count, 5, QTableWidgetItem(status))

            self.save_to_db(name, code, serial_number, item_type, status)
            self.load_data_from_db()

    def save_to_db(self, name, code, serial_number, type_name, condition):
        if not self.connection:
            return

        try:
            cursor = self.connection.cursor()

            cursor.execute("SELECT type_id FROM type WHERE type_name = %s", (type_name,))
            type_id = cursor.fetchone()
            if not type_id:
                print(f"Тип оборудования '{type_name}' не найден в базе данных!")
                return

            cursor.execute(
                """
                INSERT INTO equipment (name, code, serial_number, type_id, condition)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (name, code, serial_number, type_id[0], condition)
            )
            self.connection.commit()
            cursor.close()

            print("Оборудование успешно добавлено в базу данных.")
            print(f"Добавлено оборудование: {name}, {code}, {serial_number}, {type_name}, {condition}")
        except Exception as e:
            self.connection.rollback()
            print(f"Ошибка сохранения данных: {e}")

    def edit_equipment(self, index):
        row = index.row()
        item = self.table.item(row, 0)
        if item is None:
            print(f"Ошибка: Ячейка ID пуста в строке {row}")
            return

        equipment_id = item.text()
        print(f"Редактирование оборудования с ID: {equipment_id}")

        try:
            cursor = self.connection.cursor()
            query = """
            SELECT 
                e.equipment_id,           -- ID оборудования
                e.name AS equipment_name, -- Наименование
                e.code,                   -- Код
                e.serial_number,          -- Серийный номер
                t.type_name,              -- Тип
                c.color_name,             -- Цвет
                b.brand_name,             -- Бренд
                s.supplier_name,          -- Поставщик
                e.condition               -- Состояние
            FROM equipment e
            LEFT JOIN type t ON e.type_id = t.type_id
            LEFT JOIN color c ON e.color_id = c.color_id
            LEFT JOIN brand b ON e.brand_id = b.brand_id
            LEFT JOIN supplier s ON e.supplier_id = s.supplier_id
            WHERE e.equipment_id = %s;
            """
            cursor.execute(query, (equipment_id,))
            data = cursor.fetchone()
            cursor.close()

            if data:
                dialog = EditEquipmentDialog(
                    name=data[1],
                    code=data[2],
                    serial_number=data[3],
                    equipment_type=data[4],
                    color=data[5],
                    brand=data[6],
                    supplier=data[7],
                    condition=data[8],
                    parent=self
                )

                if dialog.exec_() == QDialog.Accepted:
                    self.table.setItem(row, 1, QTableWidgetItem(dialog.name))
                    self.table.setItem(row, 2, QTableWidgetItem(dialog.code))
                    self.table.setItem(row, 3, QTableWidgetItem(dialog.serial_number))
                    self.table.setItem(row, 4, QTableWidgetItem(dialog.equipment_type))
                    self.table.setItem(row, 5, QTableWidgetItem(dialog.color))
                    self.table.setItem(row, 6, QTableWidgetItem(dialog.brand))
                    self.table.setItem(row, 7, QTableWidgetItem(dialog.supplier))
                    self.table.setItem(row, 8, QTableWidgetItem(dialog.condition))

                    self.update_db(
                        equipment_id,
                        dialog.name,
                        dialog.serial_number,
                        dialog.equipment_type,
                        dialog.color,
                        dialog.brand,
                        dialog.supplier,
                        dialog.condition,
                        dialog.code
                    )
                    self.load_data_from_db()

        except Exception as e:
            print(f"Ошибка загрузки данных для редактирования: {e}")

    def update_db(self, equipment_id, name, serial_number, equipment_type, condition, brand, code=None, color=None,
                  supplier=None):
        if not self.connection:
            print("Нет соединения с базой данных.")
            return

        if not name or not serial_number or not equipment_type or not brand:
            print("Ошибка: Обязательные поля не заполнены.")
            return

        try:
            cursor = self.connection.cursor()

            cursor.execute("SELECT type_id FROM type WHERE type_name = %s", (equipment_type,))
            type_id = cursor.fetchone()
            if not type_id:
                print(f"Тип '{equipment_type}' не найден в базе данных!")
                return

            cursor.execute("SELECT brand_id FROM brand WHERE brand_name = %s", (brand,))
            brand_id = cursor.fetchone()
            if not brand_id:
                cursor.execute("INSERT INTO brand (brand_name) VALUES (%s) RETURNING brand_id", (brand,))
                brand_id = cursor.fetchone()
                self.connection.commit()

            color_id = None
            if color:
                cursor.execute("SELECT color_id FROM color WHERE color_name = %s", (color,))
                color_id = cursor.fetchone()
                if not color_id:
                    cursor.execute("INSERT INTO color (color_name) VALUES (%s) RETURNING color_id", (color,))
                    color_id = cursor.fetchone()
                    self.connection.commit()

            supplier_id = None
            if supplier:
                cursor.execute("SELECT supplier_id FROM supplier WHERE supplier_name = %s", (supplier,))
                supplier_id = cursor.fetchone()
                if not supplier_id:
                    cursor.execute("INSERT INTO supplier (supplier_name) VALUES (%s) RETURNING supplier_id",
                                   (supplier,))
                    supplier_id = cursor.fetchone()
                    self.connection.commit()

            cursor.execute(
                """
                UPDATE equipment
                SET 
                    name = %s,
                    serial_number = %s,
                    type_id = %s,
                    condition = %s,
                    brand_id = %s,
                    code = %s,
                    color_id = %s,
                    supplier_id = %s
                WHERE 
                    equipment_id = %s
                """,
                (
                    name,
                    serial_number,
                    type_id[0],
                    condition,
                    brand_id[0],
                    code,
                    color_id[0] if color_id else None,
                    supplier_id[0] if supplier_id else None,
                    equipment_id,
                )
            )
            self.connection.commit()
            cursor.close()
            print(f"Данные оборудования с ID {equipment_id} успешно обновлены.")
        except Exception as e:
            self.connection.rollback()
            print(f"Ошибка обновления данных: {e}")


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    studio = Studio()
    studio.show()
    sys.exit(app.exec_())

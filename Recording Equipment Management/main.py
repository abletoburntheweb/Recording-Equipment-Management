import sys
import psycopg2
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel, \
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog
from PyQt5.QtCore import Qt
from add_equipment_dialog import AddEquipmentDialog
from edit_equipment_dialog import EditEquipmentDialog
from styles import main_window, add_button, table_widget
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
                e.name AS equipment_name,  -- Наименование
                b.brand_name AS code,      -- Код (например, бренд оборудования)
                e.serial_number,           -- Серийный номер
                t.type_name,               -- Тип оборудования
                e.condition                -- Состояние (Новое, Б/У, Поврежденное)
            FROM equipment e
            LEFT JOIN type t ON e.type_id = t.type_id
            LEFT JOIN brand b ON e.brand_id = b.brand_id;
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            self.table.setRowCount(0)

            for row in rows:
                row_count = self.table.rowCount()
                self.table.insertRow(row_count)

                self.table.setItem(row_count, 1, QTableWidgetItem(row[0]))
                self.table.setItem(row_count, 2, QTableWidgetItem(row[1]))
                self.table.setItem(row_count, 3, QTableWidgetItem(row[2]))
                self.table.setItem(row_count, 4, QTableWidgetItem(row[3]))
                self.table.setItem(row_count, 5, QTableWidgetItem(row[4]))

            cursor.close()
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")

    def open_add_equipment_dialog(self):
        dialog = AddEquipmentDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            name = dialog.name_input.text()
            code = dialog.code_input.text()
            serial_number = dialog.serial_number_input.text()
            status = dialog.get_status()
            item_type = dialog.type_input.currentText()

            row_count = self.table.rowCount()
            self.table.insertRow(row_count)
            self.table.setItem(row_count, 0, QTableWidgetItem(name))
            self.table.setItem(row_count, 1, QTableWidgetItem(code))
            self.table.setItem(row_count, 2, QTableWidgetItem(serial_number))
            self.table.setItem(row_count, 3, QTableWidgetItem(item_type))
            self.table.setItem(row_count, 4, QTableWidgetItem(status))

            self.save_to_db(name, code, serial_number, item_type, status)

    def save_to_db(self, name, code, serial_number, item_type, status):
        if not self.connection:
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                INSERT INTO equipment (name, code, serial_number, equipment_type, condition)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (name, code, serial_number, item_type, status)
            )
            self.connection.commit()
            cursor.close()
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")

    def edit_equipment(self, index):
        row = index.row()
        equipment_id = self.table.item(row, 0).text()

        try:
            cursor = self.connection.cursor()
            query = """
            SELECT 
                e.name AS equipment_name,  -- Наименование
                'Новое' AS code,           -- Код
                e.serial_number,           -- Серийный номер
                t.type_name,               -- Тип оборудования
                c.color_name               -- Состояние
            FROM equipment e
            LEFT JOIN type t ON e.type_id = t.type_id
            LEFT JOIN brand b ON e.brand_id = b.brand_id
            LEFT JOIN color c ON e.color_id = c.color_id;
            """
            cursor.execute(query, (equipment_id,))
            data = cursor.fetchone()
            cursor.close()

            if data:
                dialog = EditEquipmentDialog(
                    name=data[0],
                    serial_number=data[1],
                    condition=data[2],
                    equipment_type=data[3],
                    brand=data[4],
                    color=data[5],
                    supplier=data[6],
                    parent=self
                )
                if dialog.exec_() == QDialog.Accepted:
                    self.table.setItem(row, 0, QTableWidgetItem(dialog.name))
                    self.table.setItem(row, 1, QTableWidgetItem(dialog.serial_number))
                    self.table.setItem(row, 2, QTableWidgetItem(dialog.equipment_type))
                    self.table.setItem(row, 3, QTableWidgetItem(dialog.condition))

                    self.update_db(equipment_id, dialog.name, dialog.serial_number,
                                   dialog.equipment_type, dialog.condition,
                                   dialog.brand, dialog.color, dialog.supplier)

        except Exception as e:
            print(f"Ошибка загрузки данных для редактирования: {e}")

    def update_db(self, equipment_id, name, serial_number, equipment_type, condition, brand, color, supplier):
        if not self.connection:
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                UPDATE equipment
                SET 
                    name = %s,
                    serial_number = %s,
                    type_id = (SELECT type_id FROM type WHERE type_name = %s),
                    condition = %s,
                    brand_id = (SELECT brand_id FROM brand WHERE brand_name = %s),
                    color_id = (SELECT color_id FROM color WHERE color_name = %s),
                    supplier_id = (SELECT supplier_id FROM supplier WHERE supplier_name = %s)
                WHERE 
                    equipment_id = %s
                """,
                (name, serial_number, equipment_type, condition, brand, color, supplier, equipment_id)
            )
            self.connection.commit()
            cursor.close()
        except Exception as e:
            print(f"Ошибка обновления данных: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    studio = Studio()
    studio.show()
    sys.exit(app.exec_())

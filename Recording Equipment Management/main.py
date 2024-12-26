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
    e.equipment_id,           -- ID оборудования
    e.name AS equipment_name, -- Наименование
    e.code,                   -- Код
    e.serial_number,          -- Серийный номер
    t.type_name,              -- Тип
    e.condition               -- Состояние
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

                self.table.setItem(row_count, 0, QTableWidgetItem(str(row[0])))  # ID
                self.table.setItem(row_count, 1, QTableWidgetItem(row[1]))      # Наименование
                self.table.setItem(row_count, 2, QTableWidgetItem(row[2]))      # Код
                self.table.setItem(row_count, 3, QTableWidgetItem(row[3]))      # Серийный номер
                self.table.setItem(row_count, 4, QTableWidgetItem(row[4]))      # Тип
                self.table.setItem(row_count, 5, QTableWidgetItem(row[5]))      # Состояние

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
            self.table.setItem(row_count, 1, QTableWidgetItem(name))  # Наименование
            self.table.setItem(row_count, 2, QTableWidgetItem(code))  # Код
            self.table.setItem(row_count, 3, QTableWidgetItem(serial_number))  # Серийный номер
            self.table.setItem(row_count, 4, QTableWidgetItem(item_type))  # Тип
            self.table.setItem(row_count, 5, QTableWidgetItem(status))  # Состояние

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
    e.condition               -- Состояние
FROM equipment e
LEFT JOIN type t ON e.type_id = t.type_id
LEFT JOIN brand b ON e.brand_id = b.brand_id;
            """
            cursor.execute(query, (equipment_id,))
            data = cursor.fetchone()
            cursor.close()

            if data:
                dialog = EditEquipmentDialog(
                    name=data[1],  # Наименование
                    code=data[2],  # Код бренда
                    serial_number=data[3],  # Серийный номер
                    equipment_type=data[4],  # Тип оборудования
                    condition=data[5],  # Состояние
                    parent=self
                )
                if dialog.exec_() == QDialog.Accepted:
                    self.table.setItem(row, 1, QTableWidgetItem(dialog.name))
                    self.table.setItem(row, 2, QTableWidgetItem(dialog.serial_number))
                    self.table.setItem(row, 3, QTableWidgetItem(dialog.equipment_type))
                    self.table.setItem(row, 4, QTableWidgetItem(dialog.condition))

                    self.update_db(equipment_id, dialog.name, dialog.serial_number,
                                   dialog.equipment_type, dialog.condition, dialog.brand)
                    self.load_data_from_db()

        except Exception as e:
            print(f"Ошибка загрузки данных для редактирования: {e}")

    def update_db(self, equipment_id, name, serial_number, equipment_type, condition, brand):
        if not self.connection:
            return

        if not name or not serial_number or not equipment_type:
            print("Ошибка: Обязательные поля не заполнены.")
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
                    brand_id = (SELECT brand_id FROM brand WHERE brand_name = %s)
                WHERE 
                    equipment_id = %s
                """,
                (name, serial_number, equipment_type, condition, brand, equipment_id)
            )
            self.connection.commit()
            cursor.close()
        except Exception as e:
            self.connection.rollback()
            print(f"Ошибка обновления данных: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    studio = Studio()
    studio.show()
    sys.exit(app.exec_())

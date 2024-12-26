def main_window():
    return """
    QMainWindow { background-color: #f0f0f0; }
    QLabel { font-size: 14px; }
    """


def sidebar():
    return """
    QFrame { background-color: #333; }
    """


def studios_button():
    return """
    QPushButton { 
    background-color: #4CAF50; 
    color: white; 
    border: none; 
    padding: 10px 20px; 
    text-align: center; 
    text-decoration: none; 
    display: inline-block; 
    font-size: 16px; 
    margin: 4px 2px; 
    cursor: pointer; 
    border-radius: 8px; 
    }
    QPushButton:hover { background-color: #45a049; }
    QPushButton:pressed { background-color: #3e8e41; }
    """


def equipment_button():
    return """
    QPushButton { 
    background-color: #555; 
    color: white; 
    border: none; 
    padding: 10px 20px; 
    text-align: center; 
    text-decoration: none; 
    display: inline-block; 
    font-size: 16px; 
    margin: 4px 2px; 
    cursor: pointer; 
    border-radius: 8px; 
    }
    QPushButton:hover { background-color: #777; }
    QPushButton:pressed { background-color: #444; }
    """


def back_button():
    return """
    QPushButton { 
    background-color: #008CBA; 
    color: white; 
    border: none; 
    padding: 10px 20px; 
    text-align: center; 
    text-decoration: none; 
    display: inline-block; 
    font-size: 16px; 
    margin: 4px 2px; 
    cursor: pointer; 
    border-radius: 8px; 
    }
    QPushButton:hover { background-color: #006B8E; }
    QPushButton:pressed { background-color: #005A71; }
    """


def add_button():
    return """
    QPushButton { 
    background-color: #008CBA; 
    color: white; border: 
    none; padding: 10px 20px; 
    text-align: center; 
    text-decoration: none; 
    display: inline-block; 
    font-size: 16px; margin: 4px 2px; 
    cursor: pointer; 
    border-radius: 8px; }
    QPushButton:hover { background-color: #006B8E; }
    QPushButton:pressed { background-color: #005A71; }
    """


def line_edit():
    return """
    QLineEdit { border: 1px solid #ccc; border-radius: 4px; padding: 5px; }
    """


def combo_box():
    return """
    QComboBox { border: 1px solid #ccc; border-radius: 4px; padding: 5px; }
    """


def table_widget():
    return """
    QTableWidget { border: 1px solid #ccc; border-radius: 8px; }
    QTableWidget::item { padding: 5px; }
    QHeaderView::section { background-color: #f0f0f0; border: 1px solid #ccc; padding: 5px; }
    """


def dialog():
    return """
    QDialog { background-color: #ffffff; }
    QDialog QLabel { font-size: 14px; color: #333; }
    """


def dialog_button():
    return """
    QPushButton { 
    background-color: #008CBA; 
    color: white; border: none; 
    padding: 10px 20px; text-align: center; 
    text-decoration: none; display: 
    inline-block; 
    font-size: 16px; 
    margin: 4px 2px; 
    cursor: pointer; 
    border-radius: 8px; }
    QPushButton:hover { background-color: #006B8E; }
    QPushButton:pressed { background-color: #005A71; }
    """


def dialog_cancel_button():
    return """
    QPushButton#cancel_button { background-color: #f44336; }
    QPushButton#cancel_button:hover { background-color: #d32f2f; }
    QPushButton#cancel_button:pressed { background-color: #b71c1c; }
    """


def add_equipment_dialog():
    return """
    QDialog {
        background-color: #ffffff;
        padding: 20px;
    }
    QDialog QLabel {
        font-size: 14px;
        color: #333;
        padding-right: 10px;
        width: 120px; 
        text-align: right;
    }
    QLineEdit, QComboBox {
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 5px;
        font-size: 18px;
        width: 200px; 
    }
    QPushButton {
        background-color: #008CBA;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 14px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
    }
    QPushButton:hover {
        background-color: #006B8E;
    }
    QPushButton:pressed {
        background-color: #005A71;
    }
    QPushButton#cancel_button {
        background-color: #f44336;
        color: white;
    }
    QPushButton#cancel_button:hover {
        background-color: #d32f2f;
    }
    QPushButton#cancel_button:pressed {
        background-color: #b71c1c;
    }
    """
def search_box():
    return """
    QLineEdit {
        border: 2px solid #ccc;
        border-radius: 20px;
        padding: 10px 15px;
        font-size: 16px;
        color: #333;
        background-color: #f9f9f9;
        width: 300px;
        transition: border-color 0.3s ease;
    }
    QLineEdit:focus {
        border-color: #4CAF50;
        outline: none;
        background-color: #ffffff;
    }

    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        font-size: 16px;
        cursor: pointer;
        border-radius: 20px;
        transition: background-color 0.3s ease, transform 0.2s;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    QPushButton:pressed {
        background-color: #388e3c;
        transform: scale(0.98);
    }

    QFrame#search_frame {
        background-color: #ffffff;
        border: 2px solid #eee;
        border-radius: 25px;
        padding: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    QLabel {
        font-size: 18px;
        color: #333;
        font-weight: bold;
        margin-right: 10px;
    }

    QScrollBar:vertical {
        border: none;
        background: #eaeaea;
        width: 10px;
    }
    QScrollBar::handle:vertical {
        background: #ccc;
        border-radius: 5px;
    }
    QScrollBar::handle:vertical:hover {
        background: #bbb;
    }
    """
def search_button():
    return """
    QPushButton {
        font-size: 16px;
        padding: 8px 16px;
        color: white;
        background-color: #0078d4;
        border: none;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: #005a9e;
    }
    QPushButton:pressed {
        background-color: #003f6d;
    }
    """

def edit_equipment_dialog():
    return """
    QDialog {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    QDialog QLabel {
        font-size: 16px;
        color: #444;
        padding-right: 15px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    QLineEdit, QComboBox {
        border: 2px solid #ccc;
        border-radius: 8px;
        padding: 8px 10px;
        font-size: 18px;
        background-color: #ffffff;
        width: 250px;
    }
    QLineEdit:focus, QComboBox:focus {
        border-color: #4CAF50;
        outline: none;
    }
    QDialog QLineEdit#title_field {
        margin-top: -300px; 
        font-size: 18px;
        font-weight: bold;
        padding: 10px;
        background-color: #ffffff;
        border: 2px solid #4CAF50;
        border-radius: 8px;
    }
    QPushButton {
        border: none;
        padding: 12px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 14px;
        margin: 6px 4px;
        cursor: pointer;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    QPushButton:hover {
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    QPushButton:pressed {
        box-shadow: 0 3px 5px rgba(0, 0, 0, 0.2);
    }
    QPushButton#delete_button {
        background-color: #f44336;
        color: white;
    }
    QPushButton#delete_button:hover {
        background-color: #d32f2f;
    }
    QPushButton#delete_button:pressed {
        background-color: #b71c1c;
    }
    QPushButton#save_button {
        background-color: #4CAF50;
        color: white;
    }
    QPushButton#save_button:hover {
        background-color: #45a049;
    }
    QPushButton#save_button:pressed {
        background-color: #388e3c;
    }
    QPushButton#cancel_button {
        background-color: #008CBA;
        color: white;
    }
    QPushButton#cancel_button:hover {
        background-color: #006B8E;
    }
    QPushButton#cancel_button:pressed {
        background-color: #005A71;
    }
    QPushButton:disabled {
        background-color: #ccc;
        color: #666;
        cursor: not-allowed;
    }
    QDialog QTextEdit {
        border: 2px solid #ccc;
        border-radius: 8px;
        padding: 10px;
        font-size: 14px;
        background-color: #ffffff;
    }
    QDialog QTextEdit:focus {
        border-color: #4CAF50;
    }
    QDialog QScrollBar:vertical {
        border: none;
        background: #eaeaea;
        width: 10px;
    }
    QDialog QScrollBar::handle:vertical {
        background: #ccc;
        border-radius: 5px;
    }
    QDialog QScrollBar::handle:vertical:hover {
        background: #bbb;
    }
    QDialog QLabel#header_label {
        font-size: 20px;
        color: #333;
        margin-bottom: 20px;
        font-weight: bold;
        text-align: center;
    }
    QRadioButton {
        font-size: 20px;
        padding: 8px;
        spacing: 10px;
    }
    """

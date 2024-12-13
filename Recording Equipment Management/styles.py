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
        font-size: 14px;
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
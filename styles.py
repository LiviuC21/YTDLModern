# styles.py

# Define the standard QSS stylesheet string variable for PyQt6 UI
DARK_STYLE = """
QMainWindow {
    background-color: #18181b;
}

QWidget {
    background-color: #27272a;
    border-radius: 8px;
    padding: 10px;
}

QLineEdit {
    background-color: #27272a;
    border: 1px solid #3f3f46;
    border-radius: 8px;
    padding: 8px;
    color: #ffffff;
}

QLineEdit:hover {
    border: 1px solid #3b82f6;
}

QPushButton {
    background-color: #3b82f6;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    color: #ffffff;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #2563eb;
}

QComboBox {
    background-color: #27272a;
    border: 1px solid #3f3f46;
    border-radius: 8px;
    padding: 8px;
    color: #ffffff;
}

QComboBox:hover {
    border: 1px solid #3b82f6;
}

QComboBox QAbstractItemView {
    background-color: #27272a;
    border: 1px solid #3f3f46;
    border-radius: 8px;
    color: #ffffff;
}

QProgressBar {
    background-color: #27272a;
    border: 1px solid #3f3f46;
    border-radius: 8px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #3b82f6;
    border-radius: 8px;
}

QLabel {
    color: #ffffff;
    padding: 5px;
}
"""

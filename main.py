# main.py

import sys
from PyQt6.QtWidgets import QApplication
from gui import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Apply high DPI scaling settings if needed
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

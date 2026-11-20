# gui.py

import os
from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QComboBox, QPushButton, QFileDialog, QProgressBar,
    QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt
from styles import DARK_STYLE
from downloader import DownloadWorker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet(DARK_STYLE)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.title_label = QLabel("YouTube Downloader", self)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Lipește link-ul YouTube aici...")
        self.layout.addWidget(self.url_input)

        self.format_combo = QComboBox(self)
        self.format_combo.addItems(["MP4 (Video)", "MP3 (Audio)"])
        self.layout.addWidget(self.format_combo)

        self.folder_layout = QHBoxLayout()
        self.folder_input = QLineEdit(self)
        self.folder_input.setReadOnly(True)
        self.folder_input.setText(os.path.expanduser("~/Downloads"))
        self.folder_layout.addWidget(self.folder_input)

        self.folder_button = QPushButton("Răsfoiește...", self)
        self.folder_button.clicked.connect(self.select_folder)
        self.folder_layout.addWidget(self.folder_button)

        self.layout.addLayout(self.folder_layout)

        self.noplaylist_checkbox = QCheckBox('Descarcă doar videoclipul, nu tot playlist-ul', self)
        self.noplaylist_checkbox.setChecked(True)
        self.layout.addWidget(self.noplaylist_checkbox)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(True)
        self.layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Așteaptă comenză...", self)
        self.layout.addWidget(self.status_label)

        self.download_button = QPushButton("Descarcă", self)
        self.download_button.clicked.connect(self.start_download)

        self.stop_button = QPushButton('Oprește descărcarea', self)
        self.stop_button.setObjectName('stop_button')
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_download)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.download_button)
        self.button_layout.addWidget(self.stop_button)
        self.layout.addLayout(self.button_layout)

        self.download_worker = None

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Selectează directorul")
        if folder_path:
            self.folder_input.setText(folder_path)

    def start_download(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Eroare", "URL-ul YouTube nu poate fi gol.")
            return

        output_path = self.folder_input.text()
        format_type = self.format_combo.currentText().split(' ')[0]
        noplaylist = self.noplaylist_checkbox.isChecked()

        self.download_button.setEnabled(False)
        self.url_input.setEnabled(False)
        self.folder_input.setEnabled(False)
        self.folder_button.setEnabled(False)
        self.format_combo.setEnabled(False)
        self.noplaylist_checkbox.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.download_worker = DownloadWorker(url, output_path, format_type, noplaylist)
        self.download_worker.progress_updated.connect(self.update_progress)
        self.download_worker.download_finished.connect(self.download_finished)
        self.download_worker.start()

    def update_progress(self, percent, speed, eta, status):
        self.progress_bar.setValue(int(percent))
        self.status_label.setText(f"Progres: {percent:.2f}% - Viteză: {speed} - ETA: {eta} - Statut: {status}")

    def stop_download(self):
        if self.download_worker and self.download_worker.isRunning():
            self.download_worker.stop()
            self.status_label.setText('Se oprește descărcarea...')

    def download_finished(self, success, message):
        self.download_button.setEnabled(True)
        self.url_input.setEnabled(True)
        self.folder_input.setEnabled(True)
        self.folder_button.setEnabled(True)
        self.format_combo.setEnabled(True)
        self.noplaylist_checkbox.setEnabled(True)
        self.stop_button.setEnabled(False)

        if success:
            QMessageBox.information(self, "Succes", message)
        else:
            QMessageBox.critical(self, "Eroare", message)

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

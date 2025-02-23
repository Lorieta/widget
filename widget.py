from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QInputDialog, QMessageBox
from datetime import datetime
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window setup: Qt.Tool hides the window icon from the taskbar
        self.setWindowTitle("HOURS REMAINING IN YOUR LIFE")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(300, 100)

        # Label setup
        self.widget = QLabel("000")
        font = self.widget.font()
        font.setPointSize(30)
        self.widget.setFont(font)
        self.widget.setStyleSheet("color: white;")
        self.widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.widget)

        # Initial end date
        self.end_date = datetime(2025, 6, 1, 1, 1, 1, 342380)

        # Timer setup
        QTimer(self, timeout=self.update_label).start(1000)

        # Set position in top-right corner
        screen = QApplication.primaryScreen()
        geometry = screen.availableGeometry()
        self.move(geometry.width() - self.width(), 0)

        # Add click-to-change functionality
        self.widget.mousePressEvent = self.change_end_date

    def update_label(self):
        remaining_time = self.end_date - datetime.now()
        if remaining_time.total_seconds() <= 0:
            self.widget.setText("Time's up!")
        else:
            hours = remaining_time.days * 24 + remaining_time.seconds // 3600
            seconds = remaining_time.seconds % 60
            self.widget.setText(f"{hours} : {seconds}")

    def change_end_date(self, event):
        new_date_str, ok = QInputDialog.getText(
            self, "Change End Date", "Enter new end date and time (YYYY-MM-DD HH:MM:SS):"
        )
        if ok and new_date_str:
            try:
                self.end_date = datetime.strptime(new_date_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                QMessageBox.warning(self, "Error", "Invalid date format. Try again!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

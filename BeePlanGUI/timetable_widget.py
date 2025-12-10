from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtCore import Qt

class TimetableWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.hours = ["09:20", "10:20", "11:20", "12:20",
                      "13:20", "14:20", "15:20", "16:20"]

        grid = QGridLayout()

        # Gün başlıkları
        for j, day in enumerate(self.days):
            label = QLabel(day)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-weight: bold;")
            grid.addWidget(label, 0, j + 1)

        # Saat başlıkları
        for i, hour in enumerate(self.hours):
            label = QLabel(hour)
            label.setAlignment(Qt.AlignCenter)
            grid.addWidget(label, i + 1, 0)

        # Hücreler
        self.cells = {}
        for i, hour in enumerate(self.hours):
            for j, day in enumerate(self.days):
                cell = QLabel("")
                cell.setAlignment(Qt.AlignCenter)
                cell.setStyleSheet(
                    "border: 1px solid gray; min-width: 120px; min-height: 40px;"
                )
                self.cells[(day, hour)] = cell
                grid.addWidget(cell, i + 1, j + 1)

        self.setLayout(grid)

    def place_course(self, day, hour, text, color="#FFD43B"):
        cell = self.cells[(day, hour)]
        cell.setText(text)
        cell.setStyleSheet(
            f"background-color: {color}; border: 1px solid black; font-weight: bold;"
        )

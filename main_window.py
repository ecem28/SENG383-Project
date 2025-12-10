from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QHBoxLayout
)
from PyQt5.QtCore import Qt

from gui.timetable_widget import TimetableWidget
from logic.beeplan_scheduler import BeePlanScheduler


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BeePlan – Course Scheduling System")
        self.resize(1300, 850)

        # ANA WIDGET
        main_widget = QWidget()
        main_widget.setStyleSheet("""
            background-color: #f7f7f7;
        """)
        main_layout = QVBoxLayout()

        # =====================
        #     HEADER TITLE
        # =====================
        title = QLabel("BeePlan – Course Scheduler")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 600;
            color: #333;
            padding: 20px;
        """)
        main_layout.addWidget(title)

        # =====================
        #  WEEKLY TIMETABLE
        # =====================
        self.timetable = TimetableWidget()
        main_layout.addWidget(self.timetable)

        # =====================
        #       BUTTONS
        # =====================
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        # Generate Button
        self.generate_btn = QPushButton("Generate Schedule")
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px 25px;
                border-radius: 8px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # Report Button
        self.report_btn = QPushButton("View Report")
        self.report_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 12px 25px;
                border-radius: 8px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)

        button_layout.addWidget(self.generate_btn)
        button_layout.addWidget(self.report_btn)

        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # ANA LAYOUT'U SET ET
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Scheduler
        self.beeplan_scheduler = BeePlanScheduler()

        # Button event
        self.generate_btn.clicked.connect(self.run_scheduler)

    # =====================
    #   GENERATE RUNNER
    # =====================
    def run_scheduler(self):
        results = self.beeplan_scheduler.generate_schedule()

        # Önce eski tabloyu temizle
        if hasattr(self.timetable, "clear_table"):
            self.timetable.clear_table()

        # Yeni dersleri yerleştir
        for item in results:
            self.timetable.place_course(
                item["day"],
                item["hour"],
                item["course"]
            )


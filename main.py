import tkinter as tk
from sidebar import Sidebar
from login_page import LoginPage
from dashboard_page import DashboardPage
from course_selection_page import CourseSelectionPage
from generate_schedule_page import GenerateSchedulePage
from timetable_page import TimetablePage
from reports_page import ReportsPage

class BeePlanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BeePlan – Ders Planlama Sistemi")
        self.geometry("1300x750")

        self.generated_schedule = None

        self.sidebar = Sidebar(self, self.on_sidebar_click)
        self.sidebar.pack(side="left", fill="y")

        self.main_area = tk.Frame(self, bg="#FFFBEA")
        self.main_area.pack(side="right", fill="both", expand=True)

        self.current_page = None
        self.show_page("login")

    def show_page(self, page_name, data=None):
        if page_name == "generate_schedule" and data is not None:
            self.generated_schedule = data

        page_map = {
            "login": LoginPage,
            "dashboard": DashboardPage,
            "course_selection": CourseSelectionPage,
            "generate_schedule": GenerateSchedulePage,
            "timetable": TimetablePage,
            "reports": ReportsPage,
            "logout": LoginPage,
        }

        page_class = page_map.get(page_name)

        if self.current_page is not None:
            self.current_page.destroy()

        if page_name == "generate_schedule":
            if self.generated_schedule is None:
                self.current_page = CourseSelectionPage(self.main_area, self)
            else:
                self.current_page = GenerateSchedulePage(self.main_area, self, self.generated_schedule)
        elif page_name == "timetable":
            self.current_page = TimetablePage(self.main_area, self, self.generated_schedule)
        else:
            self.current_page = page_class(self.main_area, self)

        self.current_page.pack(fill="both", expand=True)

    def on_sidebar_click(self, page_name):
        self.show_page(page_name)

if __name__ == "__main__":
    app = BeePlanApp()
    app.mainloop()
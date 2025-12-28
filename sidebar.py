import tkinter as tk

class Sidebar(tk.Frame):
    def __init__(self, parent, change_page_callback):
        super().__init__(parent, bg="#FFE23F", width=200)
        self.change_page_callback = change_page_callback

        self.pack_propagate(False)

        title = tk.Label(self, text="BeePlan", font=("Arial", 24, "bold"), bg="#FFE23F")
        title.pack(pady=20)

        buttons = [
            ("Login", "login"),
            ("Dashboard", "dashboard"),
            ("Course Selection", "course_selection"),
            ("Generate Schedule", "generate_schedule"),
            ("Timetable", "timetable"),
            ("Reports", "reports"),
            ("Logout", "logout")
        ]

        for text, page in buttons:
            btn = tk.Button(
                self,
                text=text,
                font=("Arial", 14, "bold"),
                width=20,
                bg="#FFF27C",
                command=lambda p=page: self.change_page_callback(p)
            )
            btn.pack(pady=5)

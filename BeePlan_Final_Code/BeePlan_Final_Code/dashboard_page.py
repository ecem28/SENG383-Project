import tkinter as tk


class DashboardPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#FCF8E3")

        tk.Label(self, text="Dashboard",
                 font=("Arial", 32, "bold"),
                 bg="#FCF8E3").pack(pady=40)

        tk.Label(self, text="Welcome, Coordinator!",
                 font=("Arial", 20),
                 bg="#FCF8E3").pack()

import tkinter as tk
from tkinter import messagebox

class LoginPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#FFF7D6")
        self.app = app

        tk.Label(self, text="Welcome to BeePlan",
                 font=("Arial", 24, "bold"), bg="#FFF7D6").pack(pady=30)

        tk.Label(self, text="Username:", bg="#FFF7D6").pack()
        self.username_entry = tk.Entry(self, width=25)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password:", bg="#FFF7D6").pack()
        self.password_entry = tk.Entry(self, show="*", width=25)
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", bg="#F4C542", fg="black",
                  command=self.check_login).pack(pady=20)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "123":
            self.app.show_page("course_selection")
        else:
            messagebox.showerror("Login Failed", "Wrong username or password!")

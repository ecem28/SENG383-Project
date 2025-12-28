import tkinter as tk


class GenerateSchedulePage(tk.Frame):
    def __init__(self, parent, app, schedule):
        super().__init__(parent, bg="#FFF7D6")
        self.app = app
        self.schedule = schedule

        tk.Label(self, text="Weekly Schedule",
                 font=("Arial", 28, "bold"),
                 bg="#FFF7D6").pack(pady=20)

        if not schedule:
            tk.Label(self, text="No schedule generated.",
                     font=("Arial", 18),
                     bg="#FFF7D6").pack()
            return

        # TABLO
        table = tk.Frame(self, bg="#FFF7D6")
        table.pack(pady=20)

        days = ["Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        # Header row
        for i, d in enumerate(days):
            tk.Label(table, text=d, font=("Arial", 14, "bold"), width=18,
                     bg="#F4C542").grid(row=0, column=i)

        hours = list(schedule["Monday"].keys())

        for r, hour in enumerate(hours, start=1):
            tk.Label(table, text=hour, font=("Arial", 12), width=18,
                     bg="#FFF2BF").grid(row=r, column=0)

            for c, day in enumerate(days[1:], start=1):
                value = schedule[day][hour]

                bg = "white"
                if value == "EXAM BLOCK":
                    bg = "#FFB3B3"
                elif value != "---":
                    bg = "#C8F7C5"

                tk.Label(table, text=value, font=("Arial", 11),
                         width=18, height=4, bg=bg, relief="solid").grid(row=r, column=c)

        tk.Button(self, text="Back to Course Selection",
                  font=("Arial", 14), bg="#F4C542",
                  command=lambda: app.show_page("course_selection")
                  ).pack(pady=30)

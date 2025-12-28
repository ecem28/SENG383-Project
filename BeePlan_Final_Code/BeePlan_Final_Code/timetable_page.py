import tkinter as tk


class TimetablePage(tk.Frame):
    def __init__(self, parent, app, schedule=None):
        super().__init__(parent, bg="#FCF8E3")
        self.app = app
        self.schedule = schedule

        # Başlık
        tk.Label(self, text="Weekly Timetable Summary",
                 font=("Arial", 30, "bold"),
                 bg="#FCF8E3").pack(pady=20)

        # Eğer henüz bir program oluşturulmamışsa uyarı ver
        if not self.schedule:
            tk.Label(self, text="No schedule generated yet. Please go to Course Selection.",
                     font=("Arial", 14), bg="#FCF8E3", fg="red").pack(pady=50)
        else:
            self.render_timetable()

        # Alt Buton
        tk.Button(self, text="Back to Course Selection",
                  bg="#F6C400", font=("Arial", 14, "bold"),
                  command=lambda: app.show_page("course_selection")
                  ).pack(side="bottom", pady=30)

    def render_timetable(self):
        # Ders bloklarını içine koyacağımız kaydırılabilir alan veya container
        container = tk.Frame(self, bg="#FCF8E3")
        container.pack(pady=10, fill="both", expand=True)

        # Renk paleti (Dersleri ayırt etmek için)
        colors = ["#AED6F1", "#F9E79F", "#D2B4DE", "#F5B7B1", "#ABEBC6"]
        color_map = {}
        color_index = 0

        # Verileri işle: Hangi ders hangi gün/saatte?
        # schedule yapısı: {gün: {saat: ders_bilgisi}}
        summary_data = {}

        for day, hours in self.schedule.items():
            for hour, info in hours.items():
                if info != "---" and info != "EXAM BLOCK":
                    if info not in summary_data:
                        summary_data[info] = []
                    summary_data[info].append(f"{day} {hour}")

        # Dersleri ekrana bas
        for lesson_info, times in summary_data.items():
            # Ders başına benzersiz renk ata
            if lesson_info not in color_map:
                color_map[lesson_info] = colors[color_index % len(colors)]
                color_index += 1

            frame = tk.Frame(container, bg=color_map[lesson_info], bd=2, relief="ridge")
            frame.pack(fill="x", padx=100, pady=5)

            # Ders adı ve Hoca (info içindeki \n karakterlerini temizle veya kullan)
            display_text = lesson_info.replace("\n", " | ")
            tk.Label(frame, text=display_text,
                     bg=color_map[lesson_info], font=("Arial", 12, "bold")).pack(pady=5)

            # Zaman aralıklarını yan yana yaz
            time_text = "Slots: " + ", ".join(times)
            tk.Label(frame, text=time_text,
                     bg=color_map[lesson_info], font=("Arial(10)")).pack(pady=5)

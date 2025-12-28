import tkinter as tk
from tkinter import ttk, messagebox


class CourseSelectionPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#FFF7D6")
        self.app = app

        tk.Label(self, text="Course Selection",
                 font=("Arial", 26, "bold"),
                 bg="#FFF7D6").pack(pady=20)

        # ---- DERS LİSTESİ TABLOSU [cite: 4, 5, 7] ----
        columns = ("code", "name", "instructor", "theory", "lab", "capacity", "room")
        self.table = ttk.Treeview(self, columns=columns, show="headings", height=8)

        for col in columns:
            self.table.heading(col, text=col.capitalize())
            self.table.column(col, width=130, anchor="center")

        self.table.pack(pady=20)

        # Örnek Ders Verileri [cite: 7]
        sample_courses = [
            ("SENG303", "Software Testing", "S. Esmelioğlu", 2, 2, 40, "Lab-1"),
            ("SENG315", "Concurrent Programming", "B. Avenoğlu", 3, 0, 50, "F-210"),
            ("SENG301", "Project Management", "S. Tunç", 2, 2, 40, "Lab-2"),
            ("SENG383", "Software Project III", "M. Tolun", 3, 2, 40, "Lab-1")
        ]

        for row in sample_courses:
            self.table.insert("", "end", values=row)

        # ---- BUTONLAR [cite: 21] ----
        btn_frame = tk.Frame(self, bg="#FFF7D6")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Add Course", bg="#7ED957", width=15, font=("Arial", 12),
                  command=self.add_course).grid(row=0, column=0, padx=10)

        tk.Button(btn_frame, text="Delete Selected", bg="#FF7070", width=15, font=("Arial", 12),
                  command=self.delete_selected).grid(row=0, column=1, padx=10)

        tk.Button(btn_frame, text="Generate Schedule", bg="#F4C542", width=18, font=("Arial", 14),
                  command=self.generate_schedule).grid(row=1, column=0, columnspan=2, pady=15)

    def add_course(self):
        popup = tk.Toplevel(self)
        popup.title("Add Course")
        popup.geometry("360x420")
        popup.config(bg="#FFF7D6")
        fields = ["Code", "Name", "Instructor", "Theory", "Lab", "Capacity", "Room"]
        entries = {}
        for i, f in enumerate(fields):
            tk.Label(popup, text=f, bg="#FFF7D6").grid(row=i, column=0, pady=5, padx=10)
            ent = tk.Entry(popup, width=25)
            ent.grid(row=i, column=1)
            entries[f] = ent

        def save_course():
            data = [entries[f].get() for f in fields]
            if any(x.strip() == "" for x in data):
                messagebox.showerror("Error", "All fields must be filled!")
                return
            self.table.insert("", "end", values=data)
            popup.destroy()

        tk.Button(popup, text="Add", bg="#7ED957", command=save_course).grid(row=len(fields), column=0, columnspan=2,
                                                                             pady=20)

    def delete_selected(self):
        selected = self.table.selection()
        for item in selected:
            self.table.delete(item)

    def generate_schedule(self):
        courses = []
        for child in self.table.get_children():
            row = self.table.item(child)["values"]
            courses.append(row)

        if not courses:
            messagebox.showerror("Error", "No courses available!")
            return

        schedule = self.create_schedule(courses)
        self.app.show_page("generate_schedule", schedule)

    # -----------------------------------------------------------------------------------
    # GELİŞMİŞ BLOK YERLEŞTİRME VE DERS BÖLME ALGORİTMASI [cite: 31, 32]
    # -----------------------------------------------------------------------------------
    def create_schedule(self, courses):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        hours = [
            "09:20-10:10", "10:20-11:10", "11:20-12:10", "12:20-13:10",
            "13:20-14:10", "14:20-15:10", "15:20-16:10", "16:20-17:10",
        ]
        EXAM_BLOCK = ["13:20-14:10", "14:20-15:10"]  # Cuma Sınav Arası

        # 1. Boş program ve Sınav Bloğu rezervasyonu
        schedule = {d: {h: "---" for h in hours} for d in days}
        for h in EXAM_BLOCK:
            schedule["Friday"][h] = "EXAM BLOCK"

        instructor_load = {d: {} for d in days}
        current_day_idx = 0

        for code, name, inst, th, lab, cap, room in courses:
            try:
                total_hours = int(th) + int(lab)
            except ValueError:
                continue

            text = f"{code}\n{inst}\n{room}"
            placed_hours = 0

            # SENG383 gibi 4 saati aşan dersler için bölerek yerleştirme mantığı
            attempts = 0
            while placed_hours < total_hours and attempts < 10:
                day = days[current_day_idx % 5]
                load = instructor_load[day].get(inst, 0)

                # Hocanın o gün için kalan ders saati sınırı (Max 4 saat)
                available_for_inst = 4 - load

                if available_for_inst > 0:
                    # Gün içindeki müsait (---) slotları bul
                    free_slots = [h for h in hours if schedule[day][h] == "---"]

                    # O gün yerleştirilebilecek maksimum miktar
                    can_place = min(available_for_inst, len(free_slots), total_hours - placed_hours)

                    for i in range(can_place):
                        schedule[day][free_slots[i]] = text
                        placed_hours += 1
                        load += 1

                    instructor_load[day][inst] = load

                # Dersin tamamı bitmediyse bir sonraki güne geç [cite: 32]
                if placed_hours < total_hours:
                    current_day_idx += 1
                attempts += 1

            # Bir ders bittikten sonra denge için gün sayacını artır
            current_day_idx += 1

        return schedule

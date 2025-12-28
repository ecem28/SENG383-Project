import tkinter as tk
from tkinter import ttk

class ReportsPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#FCF8E3")
        self.app = app

        tk.Label(self, text="Doğrulama Raporları", font=("Arial", 32, "bold"), bg="#FCF8E3").pack(pady=30)
        tk.Label(self, text="Sistem kuralları ve kısıtlamaları denetler.", font=("Arial", 12, "italic"), bg="#FCF8E3").pack(pady=5)

        columns = ("tip", "ders", "mesaj", "durum")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        self.tree.heading("tip", text="İhlal Tipi")
        self.tree.heading("ders", text="İlgili Ders/Kişi")
        self.tree.heading("mesaj", text="Detaylar")
        self.tree.heading("durum", text="Önem Derecesi")
        self.tree.pack(pady=20, padx=20)

        self.generate_report_data()

    def generate_report_data(self):
        # Dokümandaki kurallara göre Türkçeleştirilmiş veriler [cite: 24, 25, 26, 29]
        violations = [
            ("Kapasite Sorunu", "SENG301", "Laboratuvar kapasitesi (40) sınırda.", "Uyarı"),
            ("Teori/Lab Sırası", "SENG303", "Laboratuvar oturumu teoriden önce planlanmış."),
            ("Eğitmen Yükü", "B. Avenoğlu", "Bir günde 4 saatten fazla teorik ders.", "İhlal"),
            ("Cuma Bloğu", "Tüm Dersler", "13:20-15:10 bloğu boş bırakıldı.", "Başarılı")
        ]
        for v in violations:
            self.tree.insert("", "end", values=v)
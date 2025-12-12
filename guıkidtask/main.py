import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from math import floor

# --------------------------------------
# Basit veri yapıları ve depo (JSON)
# --------------------------------------

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")
WISHES_FILE = os.path.join(DATA_DIR, "wishes.json")

def ensure_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump([
                {"id": 1, "username": "ayse", "role": "CHILD"},
                {"id": 2, "username": "anne", "role": "PARENT"},
                {"id": 3, "username": "veli", "role": "TEACHER"}
            ], f, ensure_ascii=False, indent=2)
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    if not os.path.exists(WISHES_FILE):
        with open(WISHES_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

def read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Hizmetler
class TaskService:
    def __init__(self):
        self.tasks = read_json(TASKS_FILE)

    def save(self):
        write_json(TASKS_FILE, self.tasks)

    def list_for_user(self, user_id):
        return [t for t in self.tasks if t["assignedUserId"] == user_id]

    def add(self, title, desc, due, points, assigned_user_id):
        new_id = max([t["id"] for t in self.tasks], default=100) + 1
        self.tasks.append({
            "id": new_id, "title": title, "description": desc, "dueDate": due,
            "points": points, "status": "PENDING", "assignedUserId": assigned_user_id,
            "avgRating": 0.0
        })
        self.save()

    def mark_completed(self, task_id, user_id):
        for t in self.tasks:
            if t["id"] == task_id and t["assignedUserId"] == user_id:
                t["status"] = "COMPLETED"
                self.save()
                break

    def approve_with_rating(self, task_id, rating):
        for t in self.tasks:
            if t["id"] == task_id:
                t["status"] = "APPROVED"
                t["avgRating"] = rating if t["avgRating"] == 0 else (t["avgRating"] + rating) / 2.0
                self.save()
                break

    def total_points_approved(self, user_id):
        return sum(t["points"] for t in self.tasks
                   if t["assignedUserId"] == user_id and t["status"] == "APPROVED")

    def avg_rating_for_user(self, user_id):
        ratings = [t["avgRating"] for t in self.tasks
                   if t["assignedUserId"] == user_id and t["avgRating"] > 0]
        return sum(ratings) / len(ratings) if ratings else 0.0

class WishService:
    def __init__(self):
        self.wishes = read_json(WISHES_FILE)

    def save(self):
        write_json(WISHES_FILE, self.wishes)

    def list_for_user(self, user_id):
        return [w for w in self.wishes if w["requestedUserId"] == user_id]

    def add(self, name, wtype, cost, req_level, requested_user_id):
        new_id = max([w["id"] for w in self.wishes], default=200) + 1
        self.wishes.append({
            "id": new_id, "name": name, "type": wtype, "cost": cost,
            "requiredLevel": req_level, "status": "PENDING", "requestedUserId": requested_user_id
        })
        self.save()

    def approve(self, wish_id):
        for w in self.wishes:
            if w["id"] == wish_id:
                w["status"] = "APPROVED"
                self.save()
                break

    def reject(self, wish_id):
        for w in self.wishes:
            if w["id"] == wish_id:
                w["status"] = "REJECTED"
                self.save()
                break

# Puan/Seviye
def compute_level(total_points, avg_rating):
    by_points = total_points // 50
    by_rating = min(5, max(0, int(avg_rating)))
    return max(1, by_points + by_rating)

# --------------------------------------
# Tkinter Uygulama ve Paneller
# --------------------------------------

class KidTaskApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("KidTask")
        self.geometry("900x600")

        ensure_files()

        self.current_user = None  # dict: {"id":..., "username":..., "role":...}
        self.users = read_json(USERS_FILE)

        self.task_service = TaskService()
        self.wish_service = WishService()

        # Container ve frame’ler
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (LoginView, DashboardView, TasksView, WishesView, ProgressView):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginView")

    def show_frame(self, name):
        frame = self.frames[name]
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()

    def login(self, username, role):
        # Basit eşleştirme: rol’e göre id
        role = role.upper()
        role_to_id = {"CHILD": 1, "PARENT": 2, "TEACHER": 3}
        user_id = role_to_id.get(role, 1)
        self.current_user = {"id": user_id, "username": username, "role": role}
        self.show_frame("DashboardView")

class LoginView(ttk.Frame):
    def __init__(self, parent, controller: KidTaskApp):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Giriş", font=("Segoe UI", 18, "bold")).pack(pady=20)

        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="Kullanıcı Adı").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        self.username = ttk.Entry(form, width=25)
        self.username.grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(form, text="Rol").grid(row=1, column=0, padx=6, pady=6, sticky="e")
        self.role = ttk.Combobox(form, values=["CHILD", "PARENT", "TEACHER"], state="readonly", width=22)
        self.role.current(0)
        self.role.grid(row=1, column=1, padx=6, pady=6)

        ttk.Button(self, text="Login", command=self.on_login).pack(pady=10)

    def on_login(self):
        u = self.username.get().strip()
        r = self.role.get().strip()
        if not u:
            messagebox.showwarning("Uyarı", "Kullanıcı adı giriniz")
            return
        self.controller.login(u, r)

class DashboardView(ttk.Frame):
    def __init__(self, parent, controller: KidTaskApp):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="KidTask Dashboard", font=("Segoe UI", 18, "bold")).pack(pady=20)

        grid = ttk.Frame(self)
        grid.pack(pady=10)

        ttk.Button(grid, text="Tasks", width=20,
                   command=lambda: controller.show_frame("TasksView")).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(grid, text="Wishes", width=20,
                   command=lambda: controller.show_frame("WishesView")).grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(grid, text="Progress", width=20,
                   command=lambda: controller.show_frame("ProgressView")).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(grid, text="Logout", width=20,
                   command=lambda: controller.show_frame("LoginView")).grid(row=1, column=1, padx=10, pady=10)

    def on_show(self):
        pass

class TasksView(ttk.Frame):
    def __init__(self, parent, controller: KidTaskApp):
        super().__init__(parent)
        self.controller = controller

        top = ttk.Frame(self)
        top.pack(fill="x", pady=8)

        ttk.Label(top, text="Görevler", font=("Segoe UI", 16, "bold")).pack(side="left", padx=10)
        ttk.Button(top, text="Geri", command=lambda: controller.show_frame("DashboardView")).pack(side="right", padx=10)

        # Tablo
        cols = ("ID", "Title", "Due", "Points", "Status", "Rating")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=15)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120)
        self.tree.pack(fill="both", expand=True, padx=10, pady=6)

        # Butonlar
        bar = ttk.Frame(self)
        bar.pack(fill="x", padx=10, pady=6)
        ttk.Button(bar, text="Add Task", command=self.add_task).pack(side="left", padx=6)
        ttk.Button(bar, text="Mark Completed", command=self.complete_task).pack(side="left", padx=6)
        ttk.Button(bar, text="Approve + Rate", command=self.approve_rate).pack(side="left", padx=6)

    def on_show(self):
        self.refresh()

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        uid = self.controller.current_user["id"]
        for t in self.controller.task_service.list_for_user(uid):
            self.tree.insert("", "end", values=(
                t["id"], t["title"], t["dueDate"], t["points"], t["status"], round(t["avgRating"], 2)
            ))

    def add_task(self):
        d = tk.Toplevel(self)
        d.title("New Task")
        d.geometry("360x260")
        f = ttk.Frame(d); f.pack(padx=10, pady=10, fill="both", expand=True)

        ttk.Label(f, text="Title").grid(row=0, column=0, sticky="e"); title = ttk.Entry(f); title.grid(row=0, column=1)
        ttk.Label(f, text="Description").grid(row=1, column=0, sticky="e"); desc = ttk.Entry(f); desc.grid(row=1, column=1)
        ttk.Label(f, text="Due (yyyy-mm-dd)").grid(row=2, column=0, sticky="e"); due = ttk.Entry(f); due.insert(0, "2025-12-15"); due.grid(row=2, column=1)
        ttk.Label(f, text="Points").grid(row=3, column=0, sticky="e"); pts = ttk.Entry(f); pts.insert(0, "10"); pts.grid(row=3, column=1)

        def ok():
            try:
                p = int(pts.get().strip())
                uid = self.controller.current_user["id"]
                self.controller.task_service.add(title.get().strip(), desc.get().strip(), due.get().strip(), p, uid)
                self.refresh(); d.destroy()
            except ValueError:
                messagebox.showerror("Hata", "Points sayısal olmalı")
        ttk.Button(f, text="OK", command=ok).grid(row=4, column=0, pady=8)
        ttk.Button(f, text="Cancel", command=d.destroy).grid(row=4, column=1, pady=8)

    def complete_task(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Bilgi", "Bir görev seçin"); return
        task_id = int(self.tree.item(sel[0])["values"][0])
        uid = self.controller.current_user["id"]
        self.controller.task_service.mark_completed(task_id, uid)
        self.refresh()

    def approve_rate(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Bilgi", "Bir görev seçin"); return
        val = self.tree.item(sel[0])["values"]
        task_id = int(val[0])

        # Rol kontrol: Parent/Teacher onay verebilir
        role = self.controller.current_user["role"]
        if role not in ("PARENT", "TEACHER"):
            messagebox.showwarning("Uyarı", "Sadece ebeveyn/öğretmen onay verebilir")
            return

        r = tk.simpledialog.askfloat("Rating", "0-5 arası puan:", minvalue=0.0, maxvalue=5.0)
        if r is None:
            return
        self.controller.task_service.approve_with_rating(task_id, float(r))
        self.refresh()

class WishesView(ttk.Frame):
    def __init__(self, parent, controller: KidTaskApp):
        super().__init__(parent)
        self.controller = controller

        top = ttk.Frame(self); top.pack(fill="x", pady=8)
        ttk.Label(top, text="Dilekler", font=("Segoe UI", 16, "bold")).pack(side="left", padx=10)
        ttk.Button(top, text="Geri", command=lambda: controller.show_frame("DashboardView")).pack(side="right", padx=10)

        cols = ("ID", "Name", "Type", "Cost", "ReqLevel", "Status")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=15)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120)
        self.tree.pack(fill="both", expand=True, padx=10, pady=6)

        bar = ttk.Frame(self); bar.pack(fill="x", padx=10, pady=6)
        ttk.Button(bar, text="Add Wish", command=self.add_wish).pack(side="left", padx=6)
        ttk.Button(bar, text="Approve", command=self.approve).pack(side="left", padx=6)
        ttk.Button(bar, text="Reject", command=self.reject).pack(side="left", padx=6)

    def on_show(self):
        self.refresh()

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        uid = self.controller.current_user["id"]
        for w in self.controller.wish_service.list_for_user(uid):
            self.tree.insert("", "end", values=(w["id"], w["name"], w["type"], w["cost"], w["requiredLevel"], w["status"]))

    def add_wish(self):
        d = tk.Toplevel(self); d.title("New Wish"); d.geometry("360x240")
        f = ttk.Frame(d); f.pack(padx=10, pady=10, fill="both", expand=True)

        ttk.Label(f, text="Name").grid(row=0, column=0, sticky="e"); name = ttk.Entry(f); name.grid(row=0, column=1)
        ttk.Label(f, text="Type").grid(row=1, column=0, sticky="e"); ttype = ttk.Combobox(f, values=["PRODUCT","ACTIVITY"], state="readonly"); ttype.current(0); ttype.grid(row=1, column=1)
        ttk.Label(f, text="Cost").grid(row=2, column=0, sticky="e"); cost = ttk.Entry(f); cost.insert(0,"100"); cost.grid(row=2, column=1)
        ttk.Label(f, text="Required Level").grid(row=3, column=0, sticky="e"); rlevel = ttk.Entry(f); rlevel.insert(0,"1"); rlevel.grid(row=3, column=1)

        def ok():
            try:
                c = int(cost.get().strip()); rl = int(rlevel.get().strip())
                uid = self.controller.current_user["id"]
                self.controller.wish_service.add(name.get().strip(), ttype.get().strip(), c, rl, uid)
                self.refresh(); d.destroy()
            except ValueError:
                messagebox.showerror("Hata", "Cost/Level sayısal olmalı")
        ttk.Button(f, text="OK", command=ok).grid(row=4, column=0, pady=8)
        ttk.Button(f, text="Cancel", command=d.destroy).grid(row=4, column=1, pady=8)

    def approve(self):
        role = self.controller.current_user["role"]
        if role not in ("PARENT", "TEACHER"):
            messagebox.showwarning("Uyarı", "Sadece ebeveyn/öğretmen onay verebilir")
            return
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Bilgi", "Bir dilek seçin"); return
        wid = int(self.tree.item(sel[0])["values"][0])
        self.controller.wish_service.approve(wid)
        self.refresh()

    def reject(self):
        role = self.controller.current_user["role"]
        if role not in ("PARENT", "TEACHER"):
            messagebox.showwarning("Uyarı", "Sadece ebeveyn/öğretmen red verebilir")
            return
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Bilgi", "Bir dilek seçin"); return
        wid = int(self.tree.item(sel[0])["values"][0])
        self.controller.wish_service.reject(wid)
        self.refresh()

class ProgressView(ttk.Frame):
    def __init__(self, parent, controller: KidTaskApp):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="İlerleme & Puanlar", font=("Segoe UI", 16, "bold")).pack(pady=20)

        mid = ttk.Frame(self); mid.pack(pady=10)
        ttk.Label(mid, text="Toplam Puan").grid(row=0, column=0, padx=8, pady=6)
        self.points_bar = ttk.Progressbar(mid, orient="horizontal", length=400, mode="determinate", maximum=500)
        self.points_bar.grid(row=0, column=1, padx=8, pady=6)
        self.level_label = ttk.Label(mid, text="Level: 1")
        self.level_label.grid(row=1, column=0, columnspan=2, pady=8)

        ttk.Button(self, text="Geri", command=lambda: controller.show_frame("DashboardView")).pack(pady=10)

    def on_show(self):
        uid = self.controller.current_user["id"]
        total_points = self.controller.task_service.total_points_approved(uid)
        avg_rating = self.controller.task_service.avg_rating_for_user(uid)
        level = compute_level(total_points, avg_rating)
        self.points_bar["value"] = total_points
        self.level_label.configure(text=f"Level: {level} (avg rating: {avg_rating:.1f})")

if __name__ == "__main__":
    app = KidTaskApp()
    app.mainloop()

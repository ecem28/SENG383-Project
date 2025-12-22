import tkinter as tk
from tkinter import ttk, messagebox
import json, os

# ------------------ Utils ------------------
def ensure_data_dir():
    if not os.path.exists("data"):
        os.makedirs("data")

# ------------------ Base data service ------------------
class DataService:
    def __init__(self, filename):
        ensure_data_dir()
        self.filename = filename
        if not os.path.exists(filename):
            with open(filename, "w", encoding="utf-8") as f:
                json.dump([], f)

    def load(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

# ------------------ Services ------------------
class UserService(DataService):
    def __init__(self, filename="data/users.json"):
        super().__init__(filename)
        users = self.load()
        if not users:
            # Default demo users
            self.save([
                {"id": 1, "username": "ecem", "role": "child", "points": 0},
                {"id": 2, "username": "veli", "role": "parent", "points": 0},
                {"id": 3, "username": "teacher", "role": "teacher", "points": 0}
            ])

    def find(self, username, role):
        for u in self.load():
            if u["username"] == username and u["role"] == role:
                return u
        return None

    def list_children(self):
        return [u for u in self.load() if u["role"] == "child"]

    def get_by_id(self, user_id):
        for u in self.load():
            if u["id"] == user_id:
                return u
        return None

    def update_points(self, user_id, delta):
        users = self.load()
        for u in users:
            if u["id"] == user_id:
                u["points"] = max(0, u["points"] + delta)
        self.save(users)

class TaskService(DataService):
    def __init__(self, filename="data/tasks.json"):
        super().__init__(filename)

    def add(self, title, desc, due, points, assignedUserId):
        tasks = self.load()
        new_task = {
            "id": (tasks[-1]["id"] + 1) if tasks else 1,
            "title": title,
            "desc": desc,
            "due": due,
            "points": int(points),
            "status": "PENDING",
            "assignedUserId": assignedUserId
        }
        tasks.append(new_task)
        self.save(tasks)

    def list_for_user(self, user_id):
        return [t for t in self.load() if t["assignedUserId"] == user_id]

    def list_all_for_child(self, child_id):
        return self.list_for_user(child_id)

    def update_status(self, task_id, status):
        tasks = self.load()
        for t in tasks:
            if t["id"] == task_id:
                t["status"] = status
        self.save(tasks)

    def get_by_id(self, task_id):
        for t in self.load():
            if t["id"] == task_id:
                return t
        return None

class WishService(DataService):
    def __init__(self, filename="data/wishes.json"):
        super().__init__(filename)

    def add(self, title, desc, points, user_id):
        wishes = self.load()
        new_wish = {
            "id": (wishes[-1]["id"] + 1) if wishes else 1,
            "title": title,
            "desc": desc,
            "points": int(points),
            "status": "PENDING",
            "userId": user_id
        }
        wishes.append(new_wish)
        self.save(wishes)

    def list_for_user(self, user_id):
        return [w for w in self.load() if w["userId"] == user_id]

    def update_status(self, wish_id, status):
        wishes = self.load()
        for w in wishes:
            if w["id"] == wish_id:
                w["status"] = status
        self.save(wishes)

    def get_by_id(self, wish_id):
        for w in self.load():
            if w["id"] == wish_id:
                return w
        return None

# ------------------ App ------------------
class KidTaskApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("KidTask GUI")
        self.geometry("720x480")
        self.current_user = None

        self.user_service = UserService()
        self.task_service = TaskService()
        self.wish_service = WishService()

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginView, DashboardView, TasksView, WishesView, ProgressView, ParentChildTasksView):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show("LoginView")

    def show(self, name):
        frame = self.frames[name]
        if hasattr(frame, "refresh"):
            frame.refresh()
        frame.tkraise()

# ------------------ Views ------------------
class LoginView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Login", font=("Arial", 16, "bold")).pack(pady=10)

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Username:").grid(row=0, column=0, sticky="e")
        self.username = tk.Entry(form, width=25)
        self.username.grid(row=0, column=1, padx=5)

        tk.Label(form, text="Role:").grid(row=1, column=0, sticky="e")
        self.role = ttk.Combobox(form, values=["child", "parent", "teacher"], state="readonly", width=22)
        self.role.current(0)
        self.role.grid(row=1, column=1, padx=5)

        tk.Button(self, text="Login", command=self.login).pack(pady=10)

    def login(self):
        user = self.controller.user_service.find(self.username.get().strip(), self.role.get())
        if not user:
            messagebox.showerror("Login error", "User not found")
            return
        self.controller.current_user = user
        self.controller.show("DashboardView")

class DashboardView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.header = tk.Label(self, text="Dashboard", font=("Arial", 16, "bold"))
        self.header.pack(pady=10)

        nav = tk.Frame(self)
        nav.pack(pady=10)

        tk.Button(nav, text="Tasks", width=16, command=lambda: controller.show("TasksView")).grid(row=0, column=0, padx=5)
        tk.Button(nav, text="Wishes", width=16, command=lambda: controller.show("WishesView")).grid(row=0, column=1, padx=5)
        tk.Button(nav, text="Progress", width=16, command=lambda: controller.show("ProgressView")).grid(row=0, column=2, padx=5)

        # Parent-only view of child tasks
        tk.Button(nav, text="Child tasks (parent)", width=16, command=lambda: controller.show("ParentChildTasksView")).grid(row=1, column=0, columnspan=3, pady=8)

        tk.Button(self, text="Logout", command=lambda: controller.show("LoginView")).pack(pady=8)

    def refresh(self):
        user = self.controller.current_user
        self.header.config(text=f"Dashboard — {user['username']} ({user['role']})")
        

class TasksView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Tasks", font=("Arial", 14, "bold")).pack(pady=6)
        self.listbox = tk.Listbox(self, height=12)
        self.listbox.pack(fill="both", expand=True, padx=10)

        btns = tk.Frame(self)
        btns.pack(pady=8)
        tk.Button(btns, text="Add task (parent)", command=self.add_task).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Mark completed (child)", command=self.complete_task).grid(row=0, column=1, padx=5)
        tk.Button(btns, text="Back", command=lambda: controller.show("DashboardView")).grid(row=0, column=2, padx=5)

    def refresh(self):
        self.listbox.delete(0, tk.END)
        uid = self.controller.current_user["id"]
        tasks = self.controller.task_service.list_for_user(uid)
        for t in tasks:
            self.listbox.insert(tk.END, f"[#{t['id']}] {t['title']} — {t['status']} ({t['points']} pts)")

    def add_task(self):
        if self.controller.current_user["role"] not in ["parent", "teacher"]:
            messagebox.showerror("Permission", "Only parents or teachers can add tasks")
            return

        win = tk.Toplevel(self)
        win.title("New task")
        form = tk.Frame(win); form.pack(padx=10, pady=10)

        tk.Label(form, text="Title").grid(row=0, column=0, sticky="e")
        title = tk.Entry(form, width=28); title.grid(row=0, column=1)

        tk.Label(form, text="Description").grid(row=1, column=0, sticky="e")
        desc = tk.Entry(form, width=28); desc.grid(row=1, column=1)

        tk.Label(form, text="Due").grid(row=2, column=0, sticky="e")
        due = tk.Entry(form, width=28); due.grid(row=2, column=1)

        tk.Label(form, text="Points").grid(row=3, column=0, sticky="e")
        points = tk.Entry(form, width=28); points.grid(row=3, column=1)

        tk.Label(form, text="Assign to child").grid(row=4, column=0, sticky="e")
        children = self.controller.user_service.list_children()
        child_display = [f"{c['id']} — {c['username']}" for c in children] or ["No children"]
        child_combo = ttk.Combobox(form, values=child_display, state="readonly", width=26)
        if children:
            child_combo.current(0)
        child_combo.grid(row=4, column=1)

        def save():
            if not children:
                messagebox.showerror("No child", "No child users found")
                return
            try:
                pts = int(points.get())
            except ValueError:
                messagebox.showerror("Points", "Points must be an integer")
                return
            sel = child_combo.get()
            child_id = int(sel.split("—")[0].strip())
            self.controller.task_service.add(title.get(), desc.get(), due.get(), pts, child_id)
            win.destroy()
            self.refresh()

        tk.Button(form, text="Save", command=save).grid(row=5, column=0, columnspan=2, pady=8)

    def complete_task(self):
        user = self.controller.current_user
        if user["role"] != "child":
            messagebox.showerror("Permission", "Only children can complete tasks")
            return
        sel = self.listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        tasks = self.controller.task_service.list_for_user(user["id"])
        task = tasks[idx]
        if task["status"] != "PENDING":
            messagebox.showinfo("Info", "Task not pending")
            return
        self.controller.task_service.update_status(task["id"], "COMPLETED")
        self.controller.user_service.update_points(user["id"], task["points"])
        self.refresh()
        messagebox.showinfo("Done", f"Completed: {task['title']} (+{task['points']} pts)")

class WishesView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Wishes", font=("Arial", 14, "bold")).pack(pady=6)
        self.listbox = tk.Listbox(self, height=12)
        self.listbox.pack(fill="both", expand=True, padx=10)

        btns = tk.Frame(self); btns.pack(pady=8)
        tk.Button(btns, text="Add wish (child)", command=self.add_wish).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Approve wish (parent)", command=self.approve_wish).grid(row=0, column=1, padx=5)
        tk.Button(btns, text="Back", command=lambda: controller.show("DashboardView")).grid(row=0, column=2, padx=5)

    def refresh(self):
        self.listbox.delete(0, tk.END)
        user = self.controller.current_user
        wishes = self.controller.wish_service.list_for_user(user["id"])
        for w in wishes:
            self.listbox.insert(tk.END, f"[#{w['id']}] {w['title']} — {w['status']} ({w['points']} pts)")

    def add_wish(self):
        user = self.controller.current_user
        if user["role"] != "child":
            messagebox.showerror("Permission", "Only children can add wishes")
            return

        win = tk.Toplevel(self)
        win.title("New wish")
        form = tk.Frame(win); form.pack(padx=10, pady=10)

        tk.Label(form, text="Title").grid(row=0, column=0, sticky="e")
        title = tk.Entry(form, width=28); title.grid(row=0, column=1)

        tk.Label(form, text="Description").grid(row=1, column=0, sticky="e")
        desc = tk.Entry(form, width=28); desc.grid(row=1, column=1)

        tk.Label(form, text="Points").grid(row=2, column=0, sticky="e")
        points = tk.Entry(form, width=28); points.grid(row=2, column=1)

        def save():
            try:
                pts = int(points.get())
            except ValueError:
                messagebox.showerror("Points", "Points must be an integer")
                return
            self.controller.wish_service.add(title.get(), desc.get(), pts, user["id"])
            win.destroy()
            self.refresh()

        tk.Button(form, text="Save", command=save).grid(row=3, column=0, columnspan=2, pady=8)

    def approve_wish(self):
        user = self.controller.current_user
        if user["role"] != "parent":
            messagebox.showerror("Permission", "Only parents can approve wishes")
            return
        # Parent tüm çocukların wish'lerini tek listede görsün:
        all_wishes = []
        for c in self.controller.user_service.list_children():
            for w in self.controller.wish_service.list_for_user(c["id"]):
                all_wishes.append(w)

        sel = self.listbox.curselection()
        if not sel or not all_wishes:
            return
        idx = sel[0]
        wish = all_wishes[idx]
        if wish["status"] != "PENDING":
            messagebox.showinfo("Info", "Only PENDING wishes can be approved")
            return
        self.controller.wish_service.update_status(wish["id"], "APPROVED")
        messagebox.showinfo("Approved", f"Wish approved: {wish['title']}")
        self.refresh()

    


class ParentChildTasksView(tk.Frame):
    """Parent view to inspect a selected child's tasks and wishes."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Parent — Child Overview", font=("Arial", 14, "bold")).pack(pady=6)

        top = tk.Frame(self); top.pack(pady=6)
        tk.Label(top, text="Select child:").grid(row=0, column=0, sticky="e")
        self.child_combo = ttk.Combobox(top, values=[], state="readonly", width=24)
        self.child_combo.grid(row=0, column=1, padx=6)

        tk.Button(top, text="Load", command=self.load_child).grid(row=0, column=2, padx=6)
        tk.Button(top, text="Back", command=lambda: controller.show("DashboardView")).grid(row=0, column=3, padx=6)

        panes = tk.Frame(self); panes.pack(fill="both", expand=True, padx=10, pady=6)
        left = tk.Frame(panes); left.pack(side="left", fill="both", expand=True)
        right = tk.Frame(panes); right.pack(side="left", fill="both", expand=True)

        tk.Label(left, text="Child tasks").pack()
        self.tasks_list = tk.Listbox(left, height=10)
        self.tasks_list.pack(fill="both", expand=True, pady=4)

        tk.Label(right, text="Child wishes").pack()
        self.wishes_list = tk.Listbox(right, height=10)
        self.wishes_list.pack(fill="both", expand=True, pady=4)

        actions = tk.Frame(self); actions.pack(pady=8)
        tk.Button(actions, text="Approve selected task", command=self.approve_task).grid(row=0, column=0, padx=6)
        tk.Button(actions, text="Approve selected wish", command=self.approve_wish).grid(row=0, column=1, padx=6)

    def refresh(self):
        # Populate children combo
        children = self.controller.user_service.list_children()
        self.children_cache = children
        self.child_combo["values"] = [f"{c['id']} — {c['username']}" for c in children]

    def parse_selected_child_id(self):
        sel = self.child_combo.get()
        if not sel:
            return None
        try:
            return int(sel.split("—")[0].strip())
        except Exception:
            return None

    def load_child(self):
        child_id = self.parse_selected_child_id()
        if not child_id:
            messagebox.showerror("Select child", "Please select a child")
            return

        # Load tasks
        self.tasks_list.delete(0, tk.END)
        tasks = self.controller.task_service.list_all_for_child(child_id)
        self.child_tasks_cache = tasks
        for t in tasks:
            self.tasks_list.insert(tk.END, f"[#{t['id']}] {t['title']} — {t['status']} ({t['points']} pts)")

        # Load wishes
        self.wishes_list.delete(0, tk.END)
        wishes = self.controller.wish_service.list_for_user(child_id)
        self.child_wishes_cache = wishes
        for w in wishes:
            self.wishes_list.insert(tk.END, f"[#{w['id']}] {w['title']} — {w['status']} ({w['points']} pts)")

    def approve_task(self):
        user = self.controller.current_user
        if user["role"] not in ["parent", "teacher"]:
            messagebox.showerror("Permission", "Only parents or teachers can approve tasks")
            return

        sel = self.tasks_list.curselection()
        if not sel:
            return
        idx = sel[0]
        task = self.child_tasks_cache[idx]
        if task["status"] != "COMPLETED":
            messagebox.showinfo("Info", "Task must be COMPLETED to approve")
            return
        self.controller.task_service.update_status(task["id"], "APPROVED")
        messagebox.showinfo("Approved", f"Task approved: {task['title']}")
        self.load_child()

    def approve_wish(self):
        user = self.controller.current_user
        if user["role"] != "parent":
            messagebox.showerror("Permission", "Only parents can approve wishes")
            return
        sel = self.wishes_list.curselection()
        if not sel:
            return
        idx = sel[0]
        wish = self.child_wishes_cache[idx]
        if wish["status"] != "PENDING":
            messagebox.showinfo("Info", "Only PENDING wishes can be approved")
            return
        self.controller.wish_service.update_status(wish["id"], "APPROVED")
        messagebox.showinfo("Approved", f"Wish approved: {wish['title']}")
        self.load_child()

class ProgressView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Progress", font=("Arial", 14, "bold")).pack(pady=6)
        self.info = tk.Label(self, text="—", font=("Arial", 12))
        self.info.pack(pady=4)

        self.listbox = tk.Listbox(self, height=12)
        self.listbox.pack(fill="both", expand=True, padx=10)

        tk.Button(self, text="Back", command=lambda: controller.show("DashboardView")).pack(pady=8)

    def refresh(self):
        user = self.controller.current_user
        self.info.config(text=f"{user['username']} — role: {user['role']} — points: {user['points']}")
        self.listbox.delete(0, tk.END)

        if user["role"] == "child":
            tasks = self.controller.task_service.list_for_user(user["id"])
            for t in tasks:
                self.listbox.insert(tk.END, f"[#{t['id']}] {t['title']} — {t['status']} ({t['points']} pts)")
            wishes = self.controller.wish_service.list_for_user(user["id"])
            for w in wishes:
                self.listbox.insert(tk.END, f"WISH: {w['title']} — {w['status']} ({w['points']} pts)")

        elif user["role"] in ["parent", "teacher"]:
            children = self.controller.user_service.list_children()
            for c in children:
                self.listbox.insert(tk.END, f"--- {c['username']} --- Points: {c['points']}")
                tasks = self.controller.task_service.list_for_user(c["id"])
                for t in tasks:
                    self.listbox.insert(tk.END, f"[#{t['id']}] {t['title']} — {t['status']} ({t['points']} pts)")
                wishes = self.controller.wish_service.list_for_user(c["id"])
                for w in wishes:
                    self.listbox.insert(tk.END, f"WISH: {w['title']} — {w['status']} ({w['points']} pts)")

        else:
            self.listbox.insert(tk.END, "Progress shows child tasks when child is logged in.")

    



# ------------------ Run ------------------
if __name__ == "__main__":
    app = KidTaskApp()
    app.mainloop()

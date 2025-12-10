class User:
    def __init__(self, username, role):
        if role not in ["parent", "child"]:
            raise ValueError("Role must be 'parent' or 'child'.")

        self.username = username
        self.role = role
        self.points = 0
        self.tasks = []  # child için görev listesi

    def __repr__(self):
        return f"<User {self.username}, role={self.role}, points={self.points}>"

    def complete_task(self, task):
        if self.role != "child":
            raise PermissionError("Only children can complete tasks.")

        if task not in self.tasks:
            return "This task is not assigned to you."

        if task.completed:
            return "Task already completed."

        task.completed = True
        self.points += task.points

        return f"Task '{task.title}' completed! +{task.points} points earned."

    def list_tasks(self):
        if self.role != "child":
            return "Only children have task lists."

        if not self.tasks:
            return "No tasks assigned."

        return [f"{task.title} - {'Done' if task.completed else 'Pending'}"
                for task in self.tasks]


class Task:
    def __init__(self, title, difficulty, points):
        self.title = title
        self.difficulty = difficulty
        self.points = points
        self.completed = False  # başlangıçta tamamlanmamış

    def complete(self):
        if self.completed:
            return "Task is already completed."
        self.completed = True
        return "Task completed successfully."

    def __repr__(self):
        return f"<Task {self.title}, difficulty={self.difficulty}, points={self.points}, completed={self.completed}>"


def assign_task(parent, child, task):
    if parent.role != "parent":
        raise PermissionError("Only parents can assign tasks.")

    child.tasks.append(task)

    return f"Task '{task.title}' assigned to {child.username}."


def view_child_tasks(parent, child):
    if parent.role != "parent":
        raise PermissionError("Only parents can view child tasks.")

    if not child.tasks:
        return "Child has no tasks."

    return [f"{task.title} - {'Done' if task.completed else 'Pending'}"
            for task in child.tasks]

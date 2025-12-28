# scheduler.py

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

TIMES = [
    "09:20-10:10",
    "10:20-11:10",
    "11:20-12:10",
    "12:20-13:10",
    "13:20-14:10",
    "14:20-15:10",
    "15:20-16:10",
    "16:20-17:10",
]

class Scheduler:
    def generate_schedule(self, selected_courses):
        schedule = {
            day: {time: None for time in TIMES}
            for day in DAYS
        }

        for course in selected_courses:
            hours_left = course["theory"] + course["lab"]

            for day in DAYS:
                for time in TIMES:
                    if schedule[day][time] is None and hours_left > 0:
                        schedule[day][time] = (
                            f"{course['code']}\n"
                            f"{course['name']}\n"
                            f"{course['instructor']}"
                        )
                        hours_left -= 1

                    if hours_left == 0:
                        break
                if hours_left == 0:
                    break

        return schedule

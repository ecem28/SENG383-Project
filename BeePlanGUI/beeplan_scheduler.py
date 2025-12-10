import json
import random

class BeePlanScheduler:

    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    HOURS = ["09:20", "10:20", "11:20", "12:20", "13:20", "14:20", "15:20", "16:20"]

    def __init__(self):
        # JSON verilerini yükle
        self.courses = self.load_json("data/curriculum.json")
        self.instructors = self.load_json("data/instructors.json")
        self.common_courses = self.load_json("data/common_courses.json")

        # Timetable boş
        self.schedule = {day: {hour: None for hour in self.HOURS} for day in self.DAYS}

    def load_json(self, path):
        """JSON dosyası yükleme"""
        try:
            with open(path, "r") as f:
                return json.load(f)
        except:
            return {}

    # =============================
    #  AŞAMA 2: KURALLAR
    # =============================

    def is_friday_exam_block(self, day, hour):
        """Cuma 13:20–15:10 arası ders konamaz."""
        if day == "Friday" and hour in ["13:20", "14:20"]:
            return False
        return True

    def instructor_available(self, course, day, hour):
        """Hoca o saatte uygun mu? (JSON'a göre)"""
        instructor = self.courses[course]["instructor"]
        available = self.instructors.get(instructor, {}).get("available", [])
        return f"{day} {hour}" in available

    def teacher_daily_limit(self, course, day):
        """Aynı gün 4 saatten fazla teori veremez."""
        instructor = self.courses[course]["instructor"]
        count = 0

        for hour in self.HOURS:
            placed = self.schedule[day].get(hour)
            if placed and placed["instructor"] == instructor:
                count += 1

        return count < 4

    def no_overlap(self, day, hour):
        """Bir hücre doluysa yerleştirme yapılamaz."""
        return self.schedule[day][hour] is None

    # =============================
    #  AŞAMA 3: ANA ALGORİTMA (BASİT)
    # =============================

    def generate_schedule(self):
        """
        Şu anki versiyon:
        – Tüm dersleri sırayla boş uygun slotlara yerleştirir.
        – Kuralların temel versiyonunu uygular.
        Sonraki adım: backtracking + ileri düzey kurallar.
        """

        for course_name, info in self.courses.items():

            placed = False

            for day in self.DAYS:
                for hour in self.HOURS:

                    if not self.is_friday_exam_block(day, hour):
                        continue

                    if not self.no_overlap(day, hour):
                        continue

                    if not self.instructor_available(course_name, day, hour):
                        continue

                    if not self.teacher_daily_limit(course_name, day):
                        continue

                    # YERLEŞTİR
                    self.schedule[day][hour] = {
                        "course": course_name,
                        "instructor": info["instructor"]
                    }

                    placed = True
                    break

                if placed:
                    break

        # GUI'ye gönderilecek format:
        output = []
        for day in self.DAYS:
            for hour in self.HOURS:
                cell = self.schedule[day][hour]
                if cell:
                    output.append({
                        "course": cell["course"],
                        "day": day,
                        "hour": hour
                    })

        return output

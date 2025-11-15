# Services/schedule_exporter.py

import csv

class ScheduleExporter:
    """
    Eksportuje listę obiektów Schedule do pliku CSV (UTF-8 with BOM).
    """

    @staticmethod
    def export_to_csv(schedules, filename):
        fieldnames = [
            "date", "day_of_week", "start_time", "end_time",
            "code", "subject", "type", "group",
            "teacher", "building", "room", "student_count"
        ]

        with open(filename, mode='w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for s in schedules:
                writer.writerow({
                    "date":           s.date.isoformat(),
                    "day_of_week":    s.day_of_week or "",
                    "start_time":     s.start_time.strftime("%H:%M"),
                    "end_time":       s.end_time.strftime("%H:%M"),
                    "code":           s.code or "",
                    "subject":        s.subject or "",
                    "type":           s.type or "",
                    "group":          s.group or "",
                    "teacher":        s.teacher or "",
                    "building":       s.building or "",
                    "room":           s.room or "",
                    "student_count":  s.student_count or 0
                })
